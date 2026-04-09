from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import json
import logging
from pathlib import Path
import re
import threading
import time
from typing import Any, Dict, Iterable, List, Optional, Protocol, Sequence, Tuple

import google.auth
import keyring
import pandas as pd
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials as UserCredentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from keyring.errors import KeyringError, PasswordDeleteError
from .config import AppConfig

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
KEYRING_SERVICE_NAME = "gsheet-rw"
SHEETS_WRITE_LIMIT_PER_MINUTE = 50 # Google's actual limit is 60
SHEETS_WRITE_WINDOW_SECONDS = 60.0
SHEETS_WRITE_MIN_SLEEP_SECONDS = 2.0
_sheets_write_timestamps: deque[float] = deque()
_sheets_write_lock = threading.Lock()


def _wait_for_sheets_write_slot() -> None:
    logger = logging.getLogger(__name__)
    while True:
        sleep_seconds = 0.0
        with _sheets_write_lock:
            now = time.monotonic()
            while _sheets_write_timestamps and now - _sheets_write_timestamps[0] >= SHEETS_WRITE_WINDOW_SECONDS:
                _sheets_write_timestamps.popleft()

            if len(_sheets_write_timestamps) < SHEETS_WRITE_LIMIT_PER_MINUTE:
                _sheets_write_timestamps.append(now)
                return

            oldest = _sheets_write_timestamps[0]
            sleep_seconds = max(
                SHEETS_WRITE_MIN_SLEEP_SECONDS,
                SHEETS_WRITE_WINDOW_SECONDS - (now - oldest),
            )

        logger.info(
            "Pausing %.1f seconds to stay within the Google Sheets write quota (%s writes/minute/user).",
            sleep_seconds,
            SHEETS_WRITE_LIMIT_PER_MINUTE,
        )
        time.sleep(sleep_seconds)


def _execute_with_retry(
    request: Any,
    *,
    max_attempts: int = 7,
    base_delay_seconds: float = 1.0,
    is_sheets_write: bool = False,
) -> Any:
    logger = logging.getLogger(__name__)
    delay = base_delay_seconds
    last_error: Optional[Exception] = None
    for attempt in range(1, max_attempts + 1):
        try:
            if is_sheets_write:
                _wait_for_sheets_write_slot()
            return request.execute()
        except HttpError as exc:
            status = getattr(getattr(exc, "resp", None), "status", None)
            if status not in (403, 429, 500, 503):
                raise
            last_error = exc
            if attempt >= max_attempts:
                raise
            logger.warning(
                "Google asked us to slow down.  attempt=%s status=%s sleep_seconds=%.1f",
                attempt,
                status,
                delay,
            )
            time.sleep(delay)
            delay = min(delay * 2, 64.0)
    if last_error:
        raise last_error


@dataclass
class GoogleClients:
    sheets: Any
    drive: Any
    principal_email: Optional[str] = None


class GoogleClientsProtocol(Protocol):
    sheets: Any
    drive: Any
    principal_email: Optional[str]


class OrphanNamedRangeError(RuntimeError):
    """Raised when Google rejects a named range as duplicate but does not expose it via the API."""

    def __init__(self, spreadsheet_id: str, range_name: str):
        super().__init__(
            "Google Sheets rejected named range "
            f"{range_name!r} in spreadsheet {spreadsheet_id} because the name already exists, "
            "but the existing range could not be read through the API. "
            "This usually indicates an orphaned named range."
        )
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name


def _oauth_token_key(token_path: Path) -> str:
    return str(token_path)


def _escape_drive_query_literal(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def _oauth_principal(creds: Optional[UserCredentials]) -> str:
    account = getattr(creds, "account", "") if creds else ""
    return account or "(unknown_oauth_user)"


def _load_oauth_client_id(client_secret_path: Path) -> Optional[str]:
    try:
        payload = json.loads(client_secret_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None

    for section_name in ("installed", "web"):
        section = payload.get(section_name)
        if isinstance(section, dict):
            client_id = str(section.get("client_id") or "").strip()
            if client_id:
                return client_id
    return None


def clear_cached_oauth_token(
    cfg: AppConfig,
    *,
    clear_filesystem_fallback: bool = False,
) -> Dict[str, bool]:
    if (cfg.auth_mode or "service_account").strip().lower() != "oauth":
        raise ValueError("clear_cached_oauth_token requires auth_mode='oauth'")
    if not cfg.oauth_token_path:
        raise ValueError("oauth_token_path is required for oauth mode")

    logger = logging.getLogger(__name__)
    token_path = Path(cfg.oauth_token_path).expanduser().resolve()
    deleted_keyring = False
    deleted_filesystem = False

    try:
        keyring.delete_password(KEYRING_SERVICE_NAME, _oauth_token_key(token_path))
        deleted_keyring = True
        logger.info("oauth_token_deleted=keyring path=%s", token_path)
    except PasswordDeleteError:
        logger.info("oauth_token_deleted=keyring path=%s skipped=not_found", token_path)
    except KeyringError as exc:
        logger.warning("oauth_token_keyring_delete_failed=true path=%s error=%s", token_path, exc)

    if clear_filesystem_fallback and token_path.exists():
        token_path.unlink()
        deleted_filesystem = True
        logger.info("oauth_token_deleted=filesystem path=%s", token_path)

    return {
        "keyring_deleted": deleted_keyring,
        "filesystem_deleted": deleted_filesystem,
    }


def get_auth_status(cfg: AppConfig) -> Dict[str, Any]:
    mode = (cfg.auth_mode or "service_account").strip().lower()
    status: Dict[str, Any] = {
        "auth_mode": mode,
    }

    if mode == "oauth":
        client_secret_path = Path(cfg.oauth_client_secret_json).expanduser().resolve() if cfg.oauth_client_secret_json else None
        token_path = Path(cfg.oauth_token_path).expanduser().resolve() if cfg.oauth_token_path else None
        keyring_has_token = False
        keyring_error = None

        if token_path is not None:
            try:
                keyring_has_token = keyring.get_password(
                    KEYRING_SERVICE_NAME,
                    _oauth_token_key(token_path),
                ) is not None
            except KeyringError as exc:
                keyring_error = str(exc)

        status.update(
            {
                "oauth_client_secret_path": str(client_secret_path) if client_secret_path else None,
                "oauth_client_secret_exists": client_secret_path.exists() if client_secret_path else False,
                "oauth_token_path": str(token_path) if token_path else None,
                "oauth_token_file_exists": token_path.exists() if token_path else False,
                "keyring_service": KEYRING_SERVICE_NAME,
                "keyring_has_token": keyring_has_token,
            }
        )
        if keyring_error:
            status["keyring_error"] = keyring_error
        return status

    if mode == "service_account":
        service_account_path = Path(cfg.service_account_json).expanduser().resolve() if cfg.service_account_json else None
        status.update(
            {
                "service_account_json_path": str(service_account_path) if service_account_path else None,
                "service_account_json_exists": service_account_path.exists() if service_account_path else False,
            }
        )
        return status

    status["adc_uses_application_default_credentials"] = True
    return status


def _store_oauth_credentials(
    creds: UserCredentials,
    token_path: Path,
    *,
    write_filesystem: bool = False,
) -> None:
    logger = logging.getLogger(__name__)
    token_json = creds.to_json()

    try:
        keyring.set_password(KEYRING_SERVICE_NAME, _oauth_token_key(token_path), token_json)
        logger.info("oauth_token_persisted=keyring path=%s", token_path)
    except KeyringError as exc:
        logger.warning("oauth_token_keyring_write_failed=true path=%s error=%s", token_path, exc)
        write_filesystem = True

    if write_filesystem:
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(token_json, encoding="utf-8")
        logger.info("oauth_token_persisted=filesystem path=%s", token_path)


def _load_oauth_credentials(token_path: Path) -> Optional[UserCredentials]:
    logger = logging.getLogger(__name__)

    try:
        token_json = keyring.get_password(KEYRING_SERVICE_NAME, _oauth_token_key(token_path))
    except KeyringError as exc:
        logger.warning("oauth_token_keyring_read_failed=true path=%s error=%s", token_path, exc)
        token_json = None

    if token_json:
        try:
            token_info = json.loads(token_json)
            logger.info("oauth_token_source=keyring path=%s", token_path)
            return UserCredentials.from_authorized_user_info(token_info, SCOPES)
        except (TypeError, ValueError) as exc:
            logger.warning("oauth_token_keyring_invalid=true path=%s error=%s", token_path, exc)

    if token_path.exists():
        try:
            logger.info("oauth_token_source=filesystem path=%s", token_path)
            creds = UserCredentials.from_authorized_user_file(str(token_path), SCOPES)
            _store_oauth_credentials(creds, token_path, write_filesystem=False)
            return creds
        except ValueError as exc:
            logger.warning(
                "oauth_token_filesystem_invalid=true path=%s error=%s action=browser_reauth",
                token_path,
                exc,
            )

    return None


def build_clients(service_account_json_path: str) -> GoogleClients:
    """Service-account only (legacy entrypoint)."""
    creds = ServiceAccountCredentials.from_service_account_file(service_account_json_path, scopes=SCOPES)
    logging.getLogger(__name__).info(
        "auth_mode=service_account principal=%s", creds.service_account_email
    )
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    return GoogleClients(sheets=sheets, drive=drive, principal_email=creds.service_account_email)


def build_clients_from_config(cfg: AppConfig) -> GoogleClients:
    """Build Sheets/Drive clients using service account, OAuth, or ADC."""
    mode = (cfg.auth_mode or "service_account").strip().lower()

    if mode == "service_account":
        if not cfg.service_account_json:
            raise ValueError("service_account_json is required for service_account mode")
        return build_clients(str(cfg.service_account_json))

    if mode == "adc":
        creds, project_id = google.auth.default(scopes=SCOPES)
        logging.getLogger(__name__).info(
            "auth_mode=adc project=%s", project_id or "(unknown)"
        )
        sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)
        principal_email = str(getattr(creds, "service_account_email", "") or "").strip() or None
        return GoogleClients(sheets=sheets, drive=drive, principal_email=principal_email)

    if mode != "oauth":
        raise ValueError("auth_mode must be 'service_account', 'oauth', or 'adc'")

    if not cfg.oauth_client_secret_json or not cfg.oauth_token_path:
        raise ValueError("oauth_client_secret_json and oauth_token_path are required for oauth mode")

    if not cfg.oauth_client_secret_json.exists():
        raise FileNotFoundError(
            f"OAuth client secret JSON not found at {cfg.oauth_client_secret_json}. "
            "Set oauth_client_secret_json in config/config.yaml. "
            "Relative paths in config are resolved from the config file directory."
        )

    token_path = Path(cfg.oauth_token_path).expanduser().resolve()
    creds = _load_oauth_credentials(token_path)
    expected_client_id = _load_oauth_client_id(cfg.oauth_client_secret_json)

    if creds and expected_client_id:
        cached_client_id = str(getattr(creds, "client_id", "") or "").strip()
        if cached_client_id and cached_client_id != expected_client_id:
            logging.getLogger(__name__).warning(
                "oauth_token_client_mismatch=true path=%s action=browser_reauth "
                "message=\"cached token was created for a different OAuth client\"",
                token_path,
            )
            creds = None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _store_oauth_credentials(creds, token_path)
        except RefreshError as exc:
            logging.getLogger(__name__).warning(
                "oauth_token_refresh_failed=true path=%s error=%s action=browser_reauth "
                "message=\"cached token could not be refreshed; sign in again\"",
                token_path,
                exc,
            )
            creds = None

    if not creds or not creds.valid:
        logger = logging.getLogger(__name__)
        if creds:
            logger.info(
                "oauth_reauth_required=true path=%s message=\"browser window will open for Google sign-in\"",
                token_path,
            )
        else:
            logger.info(
                "oauth_signin_required=true path=%s message=\"browser window will open for Google sign-in\"",
                token_path,
            )
        flow = InstalledAppFlow.from_client_secrets_file(str(cfg.oauth_client_secret_json), SCOPES)
        creds = flow.run_local_server(port=0)
        _store_oauth_credentials(creds, token_path)

    logging.getLogger(__name__).info(
        "auth_mode=oauth principal=%s token_path=%s",
        _oauth_principal(creds),
        token_path,
    )
    sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    principal_email = str(getattr(creds, "account", "") or "").strip() or None
    return GoogleClients(sheets=sheets, drive=drive, principal_email=principal_email)


def build_protected_range_editor_accounts(
    clients: GoogleClientsProtocol,
    configured_accounts: Sequence[str],
) -> list[str]:
    merged_accounts: list[str] = []
    seen_accounts: set[str] = set()

    for account in list(configured_accounts) + [str(getattr(clients, "principal_email", "") or "").strip()]:
        normalized_account = str(account).strip()
        if not normalized_account:
            continue
        normalized_key = normalized_account.casefold()
        if normalized_key in seen_accounts:
            continue
        seen_accounts.add(normalized_key)
        merged_accounts.append(normalized_account)

    return merged_accounts


def create_spreadsheet(
    clients: GoogleClients,
    title: str,
    worksheet_title: str = "Sheet1",
    drive_folder_id: Optional[str] = None,
) -> Tuple[str, int]:
    """Create a spreadsheet and return (spreadsheet_id, sheet_id)."""
    if drive_folder_id:
        try:
            created = _execute_with_retry(
                clients.drive.files().create(
                    body={
                        "name": title,
                        "mimeType": "application/vnd.google-apps.spreadsheet",
                        "parents": [drive_folder_id],
                    },
                    fields="id",
                    supportsAllDrives=True,
                )
            )
        except HttpError as e:
            logger = logging.getLogger(__name__)
            logger.error(
                "event=drive_create_error status=%s reason=%s content=%s",
                e.resp.status,
                getattr(e.resp, "reason", None),
                e.content.decode("utf-8", errors="replace"),
            )
            if getattr(e.resp, "status", None) in (403, 404):
                logger.warning(
                    "Drive folder %s is not accessible to the current Google account. "
                    "Creating spreadsheet %r in the account root instead.",
                    drive_folder_id,
                    title,
                )
                return create_spreadsheet(
                    clients=clients,
                    title=title,
                    worksheet_title=worksheet_title,
                    drive_folder_id=None,
                )
            raise

        spreadsheet_id = created["id"]

        meta = clients.sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets(properties(sheetId,title))",
        ).execute()
        first = meta["sheets"][0]["properties"]
        sheet_id = int(first["sheetId"])
        default_title = first.get("title", "")

        if worksheet_title and default_title != worksheet_title:
            _execute_with_retry(
                clients.sheets.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={
                        "requests": [
                            {
                                "updateSheetProperties": {
                                    "properties": {"sheetId": sheet_id, "title": worksheet_title},
                                    "fields": "title",
                                }
                            }
                        ]
                    },
                ),
                is_sheets_write=True,
            )

        return spreadsheet_id, sheet_id

    spreadsheet_body: Dict[str, Any] = {
        "properties": {"title": title},
        "sheets": [{"properties": {"title": worksheet_title}}],
    }

    try:
        spreadsheet = _execute_with_retry(
            clients.sheets.spreadsheets().create(
                body=spreadsheet_body,
                fields="spreadsheetId,sheets(properties(sheetId))",
            ),
            is_sheets_write=True,
        )
    except HttpError as e:
        logging.getLogger(__name__).error(
            "event=sheets_create_error status=%s reason=%s content=%s",
            e.resp.status,
            getattr(e.resp, "reason", None),
            e.content.decode("utf-8", errors="replace"),
        )
        raise

    spreadsheet_id = spreadsheet["spreadsheetId"]
    sheet_id = spreadsheet["sheets"][0]["properties"]["sheetId"]
    return spreadsheet_id, sheet_id


def add_sheet_tab(
    clients: GoogleClients,
    spreadsheet_id: str,
    title: str,
) -> int:
    resp = _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [{"addSheet": {"properties": {"title": title}}}]},
        ),
        is_sheets_write=True,
    )
    replies = resp.get("replies", [])
    if not replies:
        raise RuntimeError("Failed to add new sheet tab.")
    return int(replies[0]["addSheet"]["properties"]["sheetId"])


def rename_sheet_tab(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
    new_title: str,
) -> None:
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [
                    {
                        "updateSheetProperties": {
                            "properties": {"sheetId": sheet_id, "title": new_title},
                            "fields": "title",
                        }
                    }
                ]
            },
        ),
        is_sheets_write=True,
    )


def clear_sheet_values(
    clients: GoogleClients,
    spreadsheet_id: str,
    worksheet_title: str,
) -> None:
    _execute_with_retry(
        clients.sheets.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=_a1_range(worksheet_title, "A:ZZZ"),
            body={},
        ),
        is_sheets_write=True,
    )


def move_sheet_tab_to_index(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
    index: int,
) -> None:
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [
                    {
                        "updateSheetProperties": {
                            "properties": {"sheetId": sheet_id, "index": index},
                            "fields": "index",
                        }
                    }
                ]
            },
        ),
        is_sheets_write=True,
    )


def delete_all_named_ranges(
    clients: GoogleClients,
    spreadsheet_id: str,
) -> int:
    logger = logging.getLogger(__name__)

    def _read_named_ranges(read_label: str) -> list[dict[str, Any]]:
        meta = _execute_with_retry(
            clients.sheets.spreadsheets().get(
                spreadsheetId=spreadsheet_id,
                fields=(
                    "spreadsheetId,"
                    "namedRanges(namedRangeId,name,range(sheetId,startRowIndex,endRowIndex,startColumnIndex,endColumnIndex))"
                ),
            )
        )
        if "namedRanges" not in meta:
            keys = sorted(list(meta.keys()))
            if keys != ["spreadsheetId"]:
                logger.warning(
                    "Google Sheets returned an unexpected response while checking named ranges for spreadsheet %s (%s): keys=%s",
                    spreadsheet_id,
                    read_label,
                    keys,
                )
        return list(meta.get("namedRanges", []))

    initial_named_ranges = _read_named_ranges("initial")
    if not initial_named_ranges:
        logger.info("Removed 0 existing named ranges from spreadsheet %s.", spreadsheet_id)
        return 0

    deleted_count = 0
    remaining_named_ranges = initial_named_ranges
    for attempt in range(1, 4):
        named_range_ids = [
            str(nr.get("namedRangeId", "")).strip()
            for nr in remaining_named_ranges
            if str(nr.get("namedRangeId", "")).strip()
        ]
        if not named_range_ids:
            logger.info("Removed %s existing named ranges from spreadsheet %s.", deleted_count, spreadsheet_id)
            return deleted_count

        chunk_size = 200
        for start in range(0, len(named_range_ids), chunk_size):
            chunk_ids = named_range_ids[start:start + chunk_size]
            requests = [{"deleteNamedRange": {"namedRangeId": nr_id}} for nr_id in chunk_ids]
            _execute_with_retry(
                clients.sheets.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={"requests": requests},
                ),
                is_sheets_write=True,
            )
            deleted_count += len(chunk_ids)

        remaining_named_ranges = _read_named_ranges(f"post_attempt_{attempt}")
        if not remaining_named_ranges:
            logger.info("Removed %s existing named ranges from spreadsheet %s.", len(initial_named_ranges), spreadsheet_id)
            return len(initial_named_ranges)

        logger.warning(
            "Named range cleanup retry %s for spreadsheet %s: %s ranges still remain.",
            attempt,
            spreadsheet_id,
            len(remaining_named_ranges),
        )

    remaining_names = [
        str(nr.get("name", "")).strip()
        for nr in remaining_named_ranges[:10]
        if str(nr.get("name", "")).strip()
    ]
    raise RuntimeError(
        "Named range reset failed. "
        f"Spreadsheet {spreadsheet_id} still has {len(remaining_named_ranges)} named ranges after deletion attempts. "
        f"Examples: {remaining_names}"
    )


def delete_all_protected_ranges(
    clients: GoogleClients,
    spreadsheet_id: str,
) -> int:
    meta = _execute_with_retry(
        clients.sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields=(
                "sheets("
                "properties(sheetId,title),"
                "protectedRanges(protectedRangeId,warningOnly,range(sheetId,startRowIndex,endRowIndex,startColumnIndex,endColumnIndex))"
                ")"
            ),
        )
    )

    protected_range_ids: list[int] = []
    sample_ranges: list[str] = []
    for sheet in meta.get("sheets", []):
        props = sheet.get("properties", {})
        sheet_title = str(props.get("title", "")).strip() or "(untitled)"
        for protected_range in sheet.get("protectedRanges", []):
            protected_range_id = protected_range.get("protectedRangeId")
            if protected_range_id is None:
                continue
            protected_range_ids.append(int(protected_range_id))
    if not protected_range_ids:
        logging.getLogger(__name__).info("Removed 0 existing protected ranges from spreadsheet %s.", spreadsheet_id)
        return 0

    chunk_size = 200
    for start in range(0, len(protected_range_ids), chunk_size):
        chunk_ids = protected_range_ids[start:start + chunk_size]
        _execute_with_retry(
            clients.sheets.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={
                    "requests": [
                        {"deleteProtectedRange": {"protectedRangeId": protected_range_id}}
                        for protected_range_id in chunk_ids
                    ]
                },
            ),
            is_sheets_write=True,
        )

    remaining_meta = _execute_with_retry(
        clients.sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets(protectedRanges(protectedRangeId))",
        )
    )
    remaining = sum(len(sheet.get("protectedRanges", [])) for sheet in remaining_meta.get("sheets", []))
    if remaining:
        raise RuntimeError(
            "Protected range reset failed. "
            f"Spreadsheet {spreadsheet_id} still has {remaining} protected ranges after deletion."
        )

    logging.getLogger(__name__).info(
        "Removed %s existing protected ranges from spreadsheet %s.",
        len(protected_range_ids),
        spreadsheet_id,
    )
    return len(protected_range_ids)


def get_named_ranges_by_name(
    clients: GoogleClientsProtocol,
    spreadsheet_id: str,
) -> dict[str, dict[str, Any]]:
    meta = _execute_with_retry(
        clients.sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields=(
                "namedRanges("
                "namedRangeId,"
                "name,"
                "range(sheetId,startRowIndex,endRowIndex,startColumnIndex,endColumnIndex)"
                ")"
            ),
        )
    )
    named_ranges: dict[str, dict[str, Any]] = {}
    for named_range in meta.get("namedRanges", []):
        name = str(named_range.get("name", "")).strip()
        if not name:
            continue
        named_ranges[name.casefold()] = named_range
    return named_ranges


def spreadsheet_exists(clients: GoogleClients, spreadsheet_id: str) -> bool:
    try:
        clients.drive.files().get(
            fileId=spreadsheet_id,
            fields="id",
            supportsAllDrives=True,
        ).execute()
        return True
    except HttpError as e:
        if getattr(e.resp, "status", None) == 404:
            return False
        raise


def resolve_drive_folder_id_by_name(clients: GoogleClients, folder_name: str) -> str:
    escaped_folder_name = _escape_drive_query_literal(folder_name)
    try:
        resp = clients.drive.files().list(
            q=(
                "mimeType='application/vnd.google-apps.folder' "
                f"and name='{escaped_folder_name}' and trashed=false"
            ),
            fields="files(id,name)",
            includeItemsFromAllDrives=True,
            supportsAllDrives=True,
        ).execute()
    except HttpError as e:
        if getattr(e.resp, "status", None) == 403:
            raise PermissionError(
                f"Access denied while searching for Drive folder '{folder_name}'."
            ) from e
        raise
    folders = resp.get("files", [])
    if not folders:
        raise ValueError(f"Drive folder not found: '{folder_name}'")
    if len(folders) > 1:
        ids = ", ".join(f["id"] for f in folders)
        raise ValueError(f"Multiple Drive folders named '{folder_name}' found. IDs: {ids}")
    return str(folders[0]["id"])


def write_dataframe(
    clients: GoogleClients,
    spreadsheet_id: str,
    worksheet_title: str,
    df: pd.DataFrame,
) -> None:
    values: List[List[Any]] = [list(df.columns)] + df.astype(object).where(pd.notnull(df), "").values.tolist()
    body = {"values": values}
    range_name = _a1_range(worksheet_title, "A1")
    _execute_with_retry(
        clients.sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,
        ),
        is_sheets_write=True,
    )

    sheet_id = _get_sheet_id(clients, spreadsheet_id, worksheet_title)

    requests = [
        {
            "updateSheetProperties": {
                "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount",
            }
        },
        {"setBasicFilter": {"filter": {"range": {"sheetId": sheet_id}}}},
    ]
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests},
        ),
        is_sheets_write=True,
    )

### Backup
# def write_data_to_tournament_score_sheet(
#     clients: GoogleClients,
#     spreadsheet_id: str,
#     worksheet_title: str,
#     timeslot: list[list[str]],
#     all_dojos: list[str]
# ) -> None:
#     dojo_start_col = 7  # G
#     dojo_start_col_index = dojo_start_col - 1  # zero-based
#
#     timeslot_values = timeslot
#
#     raw_value_updates = [
#         {
#             "range": _a1_range(worksheet_title, "A1"),
#             "values": timeslot_values,
#         }
#     ]
#
#     sum_row = len(timeslot_values) + 1
#     has_sum_formulas = bool(all_dojos)
#
#     if all_dojos:
#         dojo_values = [all_dojos]
#         raw_value_updates.append(
#             {
#                 "range": _a1_range(worksheet_title, "G2"),
#                 "values": dojo_values,
#             }
#         )
#
#         # Place summation formulas on the row immediately after the timeslot rows.
#         def _column_letter(col_num: int) -> str:
#             letters = []
#             while col_num > 0:
#                 col_num, remainder = divmod(col_num - 1, 26)
#                 letters.append(chr(65 + remainder))
#             return "".join(reversed(letters))
#
#         if sum_row <= 2:
#             formula_row = ["=0" for _ in all_dojos]
#         else:
#             formula_row = []
#             for offset in range(len(all_dojos)):
#                 col_letter = _column_letter(dojo_start_col + offset)
#                 formula_row.append(f"=SUM({col_letter}2:{col_letter}{sum_row - 1})")
#
#         formula_body = {"values": [formula_row]}
#         formula_range_name = _a1_range(worksheet_title, f"G{sum_row}")
#         _execute_with_retry(
#             clients.sheets.spreadsheets().values().update(
#                 spreadsheetId=spreadsheet_id,
#                 range=formula_range_name,
#                 valueInputOption="USER_ENTERED",
#                 body=formula_body,
#             )
#         )
#
#     _execute_with_retry(
#         clients.sheets.spreadsheets().values().batchUpdate(
#             spreadsheetId=spreadsheet_id,
#             body={
#                 "valueInputOption": "RAW",
#                 "data": raw_value_updates,
#             },
#         )
#     )
#
#     data_max_cols = max((len(row) for row in timeslot_values), default=0)
#     dojo_max_col = dojo_start_col_index + len(all_dojos)
#     total_columns = max(6, data_max_cols, dojo_max_col)
#     total_rows = max(len(timeslot_values), 2, sum_row if has_sum_formulas else 0)
#     unprotected_last_n = max(0, total_columns - 6)
#     sheet_id = _get_sheet_id(clients, spreadsheet_id, worksheet_title)
#
#     auto_resize_columns(
#         clients=clients,
#         spreadsheet_id=spreadsheet_id,
#         sheet_id=sheet_id,
#         total_columns=total_columns,
#     )
#     shade_columns_except_last_n(
#         clients=clients,
#         spreadsheet_id=spreadsheet_id,
#         sheet_id=sheet_id,
#         total_columns=total_columns,
#         unprotected_last_n=unprotected_last_n,
#         total_rows=total_rows,
#     )
#     protect_columns_except_last_n(
#         clients=clients,
#         spreadsheet_id=spreadsheet_id,
#         sheet_id=sheet_id,
#         total_columns=total_columns,
#         unprotected_last_n=unprotected_last_n,
#         allowed_editor_emails=[],
#     )
#
#     format_requests = [
#         {
#             "repeatCell": {
#                 "range": {
#                     "sheetId": sheet_id,
#                     "startRowIndex": 0,
#                     "endRowIndex": 1,
#                     "startColumnIndex": 0,
#                     "endColumnIndex": 1,
#                 },
#                 "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 18}}},
#                 "fields": "userEnteredFormat.textFormat(bold,fontSize)",
#             }
#         },
#         {
#             "repeatCell": {
#                 "range": {
#                     "sheetId": sheet_id,
#                     "startRowIndex": 1,
#                     "endRowIndex": 2,
#                     "startColumnIndex": 0,
#                     "endColumnIndex": total_columns,
#                 },
#                 "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
#                 "fields": "userEnteredFormat.textFormat.bold",
#             }
#         },
#     ]
#
#     if all_dojos:
#         format_requests.append(
#             {
#                 "repeatCell": {
#                     "range": {
#                         "sheetId": sheet_id,
#                         "startRowIndex": 1,
#                         "endRowIndex": 2,
#                         "startColumnIndex": dojo_start_col_index,
#                         "endColumnIndex": dojo_start_col_index + len(all_dojos),
#                     },
#                     "cell": {"userEnteredFormat": {"textRotation": {"angle": 90}}},
#                     "fields": "userEnteredFormat.textRotation.angle",
#                 }
#             }
#         )
#         format_requests.append(
#             {
#                 "repeatCell": {
#                     "range": {
#                         "sheetId": sheet_id,
#                         "startRowIndex": sum_row - 1,
#                         "endRowIndex": sum_row,
#                         "startColumnIndex": dojo_start_col_index,
#                         "endColumnIndex": dojo_start_col_index + len(all_dojos),
#                     },
#                     "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
#                     "fields": "userEnteredFormat.textFormat.bold",
#                 }
#             }
#         )
#         format_requests.append(
#             {
#                 "repeatCell": {
#                     "range": {
#                         "sheetId": sheet_id,
#                         "startRowIndex": sum_row - 1,
#                         "endRowIndex": sum_row,
#                         "startColumnIndex": 0,
#                         "endColumnIndex": total_columns,
#                     },
#                     "cell": {
#                         "userEnteredFormat": {
#                             "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85}
#                         }
#                     },
#                     "fields": "userEnteredFormat.backgroundColor",
#                 }
#             }
#         )
#         format_requests.append(
#             {
#                 "addProtectedRange": {
#                     "protectedRange": {
#                         "range": {
#                             "sheetId": sheet_id,
#                             "startRowIndex": sum_row - 1,
#                             "endRowIndex": sum_row,
#                             "startColumnIndex": 0,
#                             "endColumnIndex": total_columns,
#                         },
#                         "description": "Protected sum row.",
#                         "warningOnly": False,
#                         "editors": {"users": []},
#                     }
#                 }
#             }
#         )
#
#     if all_dojos:
#         rotated_dojo_col_width_px = 48
#         format_requests.append(
#             {
#                 "updateDimensionProperties": {
#                     "range": {
#                         "sheetId": sheet_id,
#                         "dimension": "COLUMNS",
#                         "startIndex": dojo_start_col_index,
#                         "endIndex": dojo_start_col_index + len(all_dojos),
#                     },
#                     "properties": {"pixelSize": rotated_dojo_col_width_px},
#                     "fields": "pixelSize",
#                 }
#             }
#         )
#
#     _execute_with_retry(
#         clients.sheets.spreadsheets().batchUpdate(
#             spreadsheetId=spreadsheet_id,
#             body={"requests": format_requests},
#         )
#     )
#
#
## END Backup


#  write_data_to_tournament_score_sheet(clients, spreadsheet_id, sheet_title, timeslot)
def write_data_to_tournament_score_sheet(
    clients: GoogleClients,
    spreadsheet_id: str,
    worksheet_title: str,
    timeslot: list[list[str]],
    all_dojos: list[str],
    protected_range_editor_emails: Sequence[str],
) -> None:
    logger = logging.getLogger(__name__)
    dojo_start_col = 7  # G
    dojo_start_col_index = dojo_start_col - 1  # zero-based

    timeslot_values = timeslot

    raw_value_updates = [
        {
            "range": _a1_range(worksheet_title, "A1"),
            "values": timeslot_values,
        }
    ]

    sum_row = len(timeslot_values) + 1
    has_sum_formulas = bool(all_dojos)

    if all_dojos:
        dojo_values = [all_dojos]
        raw_value_updates.append(
            {
                "range": _a1_range(worksheet_title, "G2"),
                "values": dojo_values,
            }
        )

        # Place summation formulas on the row immediately after the timeslot rows.
        def _column_letter(col_num: int) -> str:
            letters = []
            while col_num > 0:
                col_num, remainder = divmod(col_num - 1, 26)
                letters.append(chr(65 + remainder))
            return "".join(reversed(letters))

        if sum_row <= 2:
            formula_row = ["=0" for _ in all_dojos]
        else:
            formula_row = []
            for offset in range(len(all_dojos)):
                col_letter = _column_letter(dojo_start_col + offset)
                formula_row.append(f"=SUM({col_letter}2:{col_letter}{sum_row - 1})")

        raw_value_updates.append(
            {
                "range": _a1_range(worksheet_title, f"G{sum_row}"),
                "values": [formula_row],
            }
        )

    _execute_with_retry(
        clients.sheets.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": raw_value_updates,
            },
        ),
        is_sheets_write=True,
    )

    data_max_cols = max((len(row) for row in timeslot_values), default=0)
    dojo_max_col = dojo_start_col_index + len(all_dojos)
    total_columns = max(6, data_max_cols, dojo_max_col)
    total_rows = max(len(timeslot_values), 2, sum_row if has_sum_formulas else 0)
    unprotected_last_n = max(0, total_columns - 6)
    sheet_id = _get_sheet_id(clients, spreadsheet_id, worksheet_title)

    auto_resize_columns(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
    )
    shade_columns_except_last_n(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
        unprotected_last_n=unprotected_last_n,
        total_rows=total_rows,
    )
    protect_columns_except_last_n(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
        unprotected_last_n=unprotected_last_n,
        allowed_editor_emails=protected_range_editor_emails,
    )

    format_requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                },
                "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 18}}},
                "fields": "userEnteredFormat.textFormat(bold,fontSize)",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 2,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_columns,
                },
                "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                "fields": "userEnteredFormat.textFormat.bold",
            }
        },
    ]
    named_range_specs: list[dict[str, Any]] = []

    if all_dojos:
        format_requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                        "startColumnIndex": dojo_start_col_index,
                        "endColumnIndex": dojo_start_col_index + len(all_dojos),
                    },
                    "cell": {"userEnteredFormat": {"textRotation": {"angle": 90}}},
                    "fields": "userEnteredFormat.textRotation.angle",
                }
            }
        )
        format_requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": sum_row - 1,
                        "endRowIndex": sum_row,
                        "startColumnIndex": dojo_start_col_index,
                        "endColumnIndex": dojo_start_col_index + len(all_dojos),
                    },
                    "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                    "fields": "userEnteredFormat.textFormat.bold",
                }
            }
        )
        format_requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": sum_row - 1,
                        "endRowIndex": sum_row,
                        "startColumnIndex": 0,
                        "endColumnIndex": total_columns,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85}
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor",
                }
            }
        )
        format_requests.append(
            {
                "addProtectedRange": {
                    "protectedRange": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": sum_row - 1,
                            "endRowIndex": sum_row,
                            "startColumnIndex": 0,
                            "endColumnIndex": total_columns,
                        },
                        "description": "Protected sum row.",
                        "warningOnly": False,
                        "editors": {"users": list(protected_range_editor_emails)},
                    }
                }
            }
        )

    if all_dojos:
        rotated_dojo_col_width_px = 24  #was 48
        format_requests.append(
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": dojo_start_col_index,
                        "endIndex": dojo_start_col_index + len(all_dojos),
                    },
                    "properties": {"pixelSize": rotated_dojo_col_width_px},
                    "fields": "pixelSize",
                }
            }
        )
        seen_named_range_names: set[str] = set()
        for offset, dojo_name in enumerate(all_dojos):
            candidate_name = build_tournament_score_named_range_name(
                worksheet_title=worksheet_title,
                sheet_id=sheet_id,
                dojo_name=dojo_name,
            )
            candidate_name_key = candidate_name.casefold()
            if not candidate_name:
                logger.error(
                    "Skipping named range creation for worksheet '%s' because dojo name %r produced an empty range name.",
                    worksheet_title,
                    dojo_name,
                )
                continue
            if candidate_name_key in seen_named_range_names:
                logger.warning(
                    "Skipping duplicate named range '%s' while preparing worksheet '%s'.",
                    candidate_name,
                    worksheet_title,
                )
                continue
            seen_named_range_names.add(candidate_name_key)
            named_range_specs.append(
                {
                    "name": candidate_name,
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": sum_row - 1,
                        "endRowIndex": sum_row,
                        "startColumnIndex": dojo_start_col_index + offset,
                        "endColumnIndex": dojo_start_col_index + offset + 1,
                    },
                }
            )

    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": format_requests},
        ),
        is_sheets_write=True,
    )

    created_named_ranges = 0
    named_range_requests = [
        {
            "addNamedRange": {
                "namedRange": {
                    "name": named_range_spec["name"],
                    "range": named_range_spec["range"],
                }
            }
        }
        for named_range_spec in named_range_specs
    ]
    if named_range_requests:
        try:
            resp = _execute_with_retry(
                clients.sheets.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id,
                    body={"requests": named_range_requests},
                ),
                is_sheets_write=True,
            )
            created_named_ranges = len(resp.get("replies", [])) if isinstance(resp, dict) else len(named_range_requests)
        except HttpError as exc:
            status = getattr(getattr(exc, "resp", None), "status", None)
            content = getattr(exc, "content", b"")
            message = content.decode("utf-8", errors="replace") if isinstance(content, (bytes, bytearray)) else str(exc)
            if status == 400 and "Cannot add named range with name" in message:
                logger.error(
                    "Google Sheets rejected one or more named ranges for worksheet '%s' because a range name already exists. "
                    "The request was sent in one batch; inspect the generated names if this persists.",
                    worksheet_title,
                )
            else:
                logger.error(
                    "Named range creation failed for worksheet '%s' (status=%s): %s",
                    worksheet_title,
                    status,
                    message,
                )
            raise
    logger.info(
        "Worksheet '%s' uploaded with %s named ranges.",
        worksheet_title,
        created_named_ranges,
    )


def write_tournament_score_totals_sheet(
    clients: GoogleClients,
    spreadsheet_id: str,
    worksheet_title: str,
    values: list[list[str]],
    dojo_names: list[str],
    protected_range_editor_emails: Sequence[str],
) -> None:
    body = {"values": values}
    _execute_with_retry(
        clients.sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=_a1_range(worksheet_title, "A1"),
            valueInputOption="USER_ENTERED",
            body=body,
        ),
        is_sheets_write=True,
    )

    sheet_id = _get_sheet_id(clients, spreadsheet_id, worksheet_title)
    total_columns = max((len(row) for row in values), default=0)
    total_rows = len(values)
    if total_columns <= 0 or total_rows <= 0:
        return

    auto_resize_columns(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
    )
    shade_columns_except_last_n(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
        unprotected_last_n=0,
        total_rows=total_rows,
    )

    requests = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1,
                        "frozenColumnCount": 1,
                    },
                },
                    "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_columns,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85},
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold,backgroundColor)",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": total_columns,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textRotation": {"angle": 90},
                    }
                },
                "fields": "userEnteredFormat.textRotation.angle",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": total_rows - 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True},
                        "backgroundColor": {"red": 0.93, "green": 0.93, "blue": 0.93},
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold,backgroundColor)",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": total_rows - 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": total_columns,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {"type": "NUMBER", "pattern": "0"},
                    }
                },
                "fields": "userEnteredFormat.numberFormat",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": total_rows - 1,
                    "endRowIndex": total_rows,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_columns,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 14},
                        "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85},
                        "borders": {
                            "top": {
                                "style": "SOLID_THICK",
                                "color": {"red": 0.0, "green": 0.0, "blue": 0.0},
                            }
                        },
                    }
                },
                "fields": "userEnteredFormat(textFormat.bold,textFormat.fontSize,backgroundColor,borders.top)",
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 1,
                    "endIndex": total_columns,
                },
                "properties": {"pixelSize": 24}, # was 48
                "fields": "pixelSize",
            }
        },
    ]
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests},
        ),
        is_sheets_write=True,
    )

    protect_columns_except_last_n(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
        unprotected_last_n=0,
        allowed_editor_emails=protected_range_editor_emails,
    )

    if dojo_names and total_rows >= 2:
        logger = logging.getLogger(__name__)
        total_row_index = total_rows - 1
        existing_named_ranges = get_named_ranges_by_name(clients, spreadsheet_id)
        seen_total_named_range_names: set[str] = set()
        for offset, dojo_name in enumerate(dojo_names):
            range_name = build_tournament_score_total_named_range_name(dojo_name)
            if not range_name:
                logger.warning(
                    "Skipping total named range for dojo %r because the generated range name is empty.",
                    dojo_name,
                )
                continue

            range_name_key = range_name.casefold()
            if range_name_key in seen_total_named_range_names:
                logger.warning(
                    "Skipping duplicate total named range %r for dojo %r on worksheet %r.",
                    range_name,
                    dojo_name,
                    worksheet_title,
                )
                continue
            seen_total_named_range_names.add(range_name_key)

            target_range = {
                "sheetId": sheet_id,
                "startRowIndex": total_row_index,
                "endRowIndex": total_row_index + 1,
                "startColumnIndex": offset + 1,
                "endColumnIndex": offset + 2,
            }

            existing_named_range = existing_named_ranges.get(range_name_key)
            request_body: dict[str, Any]
            if existing_named_range:
                request_body = {
                    "requests": [
                        {
                            "updateNamedRange": {
                                "namedRange": {
                                    "namedRangeId": existing_named_range["namedRangeId"],
                                    "name": range_name,
                                    "range": target_range,
                                },
                                "fields": "name,range",
                            }
                        }
                    ]
                }
            else:
                request_body = {
                    "requests": [
                        {
                            "addNamedRange": {
                                "namedRange": {
                                    "name": range_name,
                                    "range": target_range,
                                }
                            }
                        }
                    ]
                }

            try:
                _execute_with_retry(
                    clients.sheets.spreadsheets().batchUpdate(
                        spreadsheetId=spreadsheet_id,
                        body=request_body,
                    ),
                    is_sheets_write=True,
                )
            except HttpError as exc:
                status = getattr(getattr(exc, "resp", None), "status", None)
                message = str(exc)
                if status != 400 or "already exists" not in message:
                    raise

                existing_named_ranges = get_named_ranges_by_name(clients, spreadsheet_id)
                existing_named_range = existing_named_ranges.get(range_name_key)
                if not existing_named_range:
                    raise OrphanNamedRangeError(spreadsheet_id, range_name) from exc

                _execute_with_retry(
                    clients.sheets.spreadsheets().batchUpdate(
                        spreadsheetId=spreadsheet_id,
                        body={
                            "requests": [
                                {
                                    "updateNamedRange": {
                                        "namedRange": {
                                            "namedRangeId": existing_named_range["namedRangeId"],
                                            "name": range_name,
                                            "range": target_range,
                                        },
                                        "fields": "name,range",
                                    }
                                }
                            ]
                        },
                    ),
                    is_sheets_write=True,
                )


def write_tournament_score_leaderboard_sheet(
    clients: GoogleClients,
    spreadsheet_id: str,
    worksheet_title: str,
    dojo_names: list[str],
    protected_range_editor_emails: Sequence[str],
) -> None:
    formula = _build_leaderboard_formula(dojo_names)
    values: list[list[str]] = [
        ["Dojo", "Total Points"],
        [formula],
    ]
    _execute_with_retry(
        clients.sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=_a1_range(worksheet_title, "A1"),
            valueInputOption="USER_ENTERED",
            body={"values": values},
        ),
        is_sheets_write=True,
    )

    sheet_id = _get_sheet_id(clients, spreadsheet_id, worksheet_title)
    total_columns = 2
    total_rows = max(len(dojo_names) + 1, 2)
    shade_columns_except_last_n(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
        unprotected_last_n=0,
        total_rows=total_rows,
    )
    requests = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1,
                    },
                },
                "fields": "gridProperties.frozenRowCount",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2,
                },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {"bold": True, "fontSize": 14},
                            "backgroundColor": {"red": 0.85, "green": 0.85, "blue": 0.85},
                        }
                    },
                "fields": "userEnteredFormat(textFormat.bold,textFormat.fontSize,backgroundColor)",
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": total_rows,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_columns,
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"fontSize": 14},
                    }
                },
                "fields": "userEnteredFormat.textFormat.fontSize",
            }
        },
    ]
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests},
        ),
        is_sheets_write=True,
    )
    auto_resize_columns(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
    )
    protect_columns_except_last_n(
        clients=clients,
        spreadsheet_id=spreadsheet_id,
        sheet_id=sheet_id,
        total_columns=total_columns,
        unprotected_last_n=0,
        allowed_editor_emails=protected_range_editor_emails,
    )


def build_tournament_score_named_range_name(
    worksheet_title: str,
    sheet_id: int,
    dojo_name: str,
) -> str:
    sheet_name_prefix = _to_named_range_name(worksheet_title)
    named_range_prefix = _to_named_range_name(f"{sheet_name_prefix}_{sheet_id}")
    dojo_name_suffix = _to_named_range_name(dojo_name)
    return _to_named_range_name(f"{named_range_prefix}_{dojo_name_suffix}")


def build_tournament_score_total_named_range_name(dojo_name: str) -> str:
    return _to_named_range_name(f"{dojo_name}-Total")


def _build_leaderboard_formula(dojo_names: list[str]) -> str:
    if not dojo_names:
        return '=SORT({"",0},2,FALSE)'

    rows: list[str] = []
    for dojo_name in dojo_names:
        escaped_dojo_name = str(dojo_name).replace('"', '""')
        total_named_range = build_tournament_score_total_named_range_name(dojo_name)
        rows.append(f'{{"{escaped_dojo_name}",{total_named_range}}}')
    return f"=SORT({{{';'.join(rows)}}},2,FALSE)"


def _a1_range(worksheet_title: str, cell: str) -> str:
    escaped_title = str(worksheet_title).replace("'", "''")
    return f"'{escaped_title}'!{cell}"


def _to_named_range_name(value: str) -> str:
    name = str(value).strip()
    name = re.sub(r"[^A-Za-z0-9_]", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        return ""
    if re.match(r"^[0-9]", name):
        name = f"_{name}"
    if re.match(r"^[A-Za-z]+[0-9]+$", name):
        name = f"_{name}"
    return name

def auto_resize_columns(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
    total_columns: int,
) -> None:
    if total_columns <= 0:
        return
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [
                    {
                        "autoResizeDimensions": {
                            "dimensions": {
                                "sheetId": sheet_id,
                                "dimension": "COLUMNS",
                                "startIndex": 0,
                                "endIndex": total_columns,
                            }
                        }
                    }
                ]
            },
        ),
        is_sheets_write=True,
    )


def get_column_pixel_sizes(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
) -> List[int]:
    meta = clients.sheets.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        includeGridData=True,
        fields="sheets(properties(sheetId),data.columnMetadata(pixelSize))",
    ).execute()
    for sheet in meta.get("sheets", []):
        props = sheet.get("properties", {})
        if int(props.get("sheetId", -1)) != sheet_id:
            continue
        data = sheet.get("data", [])
        if not data:
            return []
        col_meta = data[0].get("columnMetadata", [])
        return [int(cm.get("pixelSize", 100)) for cm in col_meta]
    return []


def set_column_pixel_size(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
    column_index: int,
    pixel_size: int,
) -> None:
    if column_index < 0:
        return
    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={
                "requests": [
                    {
                        "updateDimensionProperties": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "COLUMNS",
                                "startIndex": column_index,
                                "endIndex": column_index + 1,
                            },
                            "properties": {"pixelSize": pixel_size},
                            "fields": "pixelSize",
                        }
                    }
                ]
            },
        ),
        is_sheets_write=True,
    )


def protect_columns_except_last_n(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
    total_columns: int,
    unprotected_last_n: int,
    allowed_editor_emails: Sequence[str],
) -> None:
    protected_end = max(0, total_columns - unprotected_last_n)
    if protected_end <= 0:
        return

    req = {
        "addProtectedRange": {
            "protectedRange": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": protected_end,
                },
                "description": "Protected: all columns except the last editable columns.",
                "warningOnly": False,
                "editors": {"users": list(allowed_editor_emails)},
            }
        }
    }

    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [req]},
        ),
        is_sheets_write=True,
    )


def shade_columns_except_last_n(
    clients: GoogleClients,
    spreadsheet_id: str,
    sheet_id: int,
    total_columns: int,
    unprotected_last_n: int,
    total_rows: int,
    time_row_indexes: Optional[Iterable[int]] = None,
    *,
    protected_rgb: Optional[Tuple[float, float, float]] = None,
    unprotected_rgb: Optional[Tuple[float, float, float]] = None,
) -> None:
    protected_end = max(0, total_columns - unprotected_last_n)
    if total_columns <= 0 or total_rows <= 0:
        return

    protected_light = _hex_to_rgb("#d9d9d9")
    protected_dark = _hex_to_rgb("#b7b7b7")
    unprotected_light = _hex_to_rgb("#cfe2f3")
    unprotected_dark = _hex_to_rgb("#9fc5e8")
    protected_color = protected_rgb or protected_light
    unprotected_color = unprotected_rgb or unprotected_light

    time_rows = set(time_row_indexes or [])
    requests = []
    for row in range(total_rows):
        if row in time_rows:
            requests.append(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row,
                            "endRowIndex": row + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": total_columns,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
                                "textFormat": {"fontSize": 18},
                            }
                        },
                        "fields": "userEnteredFormat(backgroundColor,textFormat.fontSize)",
                    }
                }
            )
            continue

        is_even = row % 2 == 0
        protected_row = protected_color if is_even else protected_dark
        unprotected_row = unprotected_color if is_even else unprotected_dark

        if protected_end > 0:
            requests.append(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row,
                            "endRowIndex": row + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": protected_end,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": protected_row[0],
                                    "green": protected_row[1],
                                    "blue": protected_row[2],
                                }
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                }
            )

        if protected_end < total_columns:
            requests.append(
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row,
                            "endRowIndex": row + 1,
                            "startColumnIndex": protected_end,
                            "endColumnIndex": total_columns,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {
                                    "red": unprotected_row[0],
                                    "green": unprotected_row[1],
                                    "blue": unprotected_row[2],
                                }
                            }
                        },
                        "fields": "userEnteredFormat.backgroundColor",
                    }
                }
            )

    border = {
        "style": "SOLID_THICK",
        "width": 2,
        "color": {"red": 0.6, "green": 0.6, "blue": 0.6},
    }
    requests.append(
        {
            "updateBorders": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 0,
                    "endRowIndex": total_rows,
                    "startColumnIndex": 0,
                    "endColumnIndex": total_columns,
                },
                "innerHorizontal": border,
                "innerVertical": {"style": "NONE"},
                "top": {"style": "NONE"},
                "bottom": border,
                "left": {"style": "NONE"},
                "right": {"style": "NONE"},
            }
        }
    )

    _execute_with_retry(
        clients.sheets.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": requests},
        ),
        is_sheets_write=True,
    )


def _hex_to_rgb(value: str) -> Tuple[float, float, float]:
    cleaned = value.lstrip("#")
    if len(cleaned) != 6:
        raise ValueError(f"Invalid hex color: {value}")
    r = int(cleaned[0:2], 16) / 255.0
    g = int(cleaned[2:4], 16) / 255.0
    b = int(cleaned[4:6], 16) / 255.0
    return (r, g, b)


def share_spreadsheet(
    clients: GoogleClients,
    spreadsheet_id: str,
    emails: Sequence[str],
    role: str = "writer",
) -> None:
    logger = logging.getLogger(__name__)
    for email in emails:
        perm_body = {"type": "user", "role": role, "emailAddress": email}
        _execute_with_retry(
            clients.drive.permissions().create(
                fileId=spreadsheet_id,
                body=perm_body,
                sendNotificationEmail=True,
                fields="id",
                supportsAllDrives=True,
            )
        )
        logger.info(
            "event=share_permission spreadsheet_id=%s role=%s email=%s",
            spreadsheet_id,
            role,
            email,
        )


def read_sheet_to_dataframe(
    clients: GoogleClients,
    spreadsheet_id: str,
    worksheet_title: str,
) -> pd.DataFrame:
    try:
        resp = clients.sheets.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=_a1_range(worksheet_title, "A1:ZZZ"),
        ).execute()
    except HttpError as e:
        if getattr(e.resp, "status", None) == 404:
            raise FileNotFoundError(
                f"Spreadsheet '{spreadsheet_id}' or worksheet '{worksheet_title}' was not found, "
                "or the OAuth account used by this app does not have access to it."
            ) from e
        raise
    values = resp.get("values", [])
    if not values:
        return pd.DataFrame()

    headers = values[0]
    rows = values[1:]
    max_len = max(len(headers), *(len(r) for r in rows)) if rows else len(headers)
    headers = headers + [""] * (max_len - len(headers))
    normalized_rows = [r + [""] * (max_len - len(r)) for r in rows]
    return pd.DataFrame(normalized_rows, columns=headers)


def _get_sheet_id(clients: GoogleClients, spreadsheet_id: str, worksheet_title: str) -> int:
    try:
        meta = clients.sheets.spreadsheets().get(
            spreadsheetId=spreadsheet_id,
            fields="sheets(properties(sheetId,title))",
        ).execute()
    except HttpError as e:
        if getattr(e.resp, "status", None) == 404:
            raise FileNotFoundError(
                f"Spreadsheet '{spreadsheet_id}' was not found, or the OAuth account used by this app "
                "does not have access to it."
            ) from e
        raise
    for s in meta.get("sheets", []):
        props = s.get("properties", {})
        if props.get("title") == worksheet_title:
            return int(props["sheetId"])
    raise ValueError(f"Worksheet '{worksheet_title}' not found in spreadsheet {spreadsheet_id}")
