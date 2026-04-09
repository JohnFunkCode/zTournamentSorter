from __future__ import annotations

import logging
import os
import pathlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
import pandas as pd
import re


from GoogleSheetReaderWriter.gsheet_rw.sheets_client import (
    add_sheet_tab,
    auto_resize_columns,
    build_protected_range_editor_accounts,
    build_tournament_score_named_range_name,
    build_clients_from_config,
    clear_sheet_values,
    create_spreadsheet,
    delete_all_named_ranges,
    delete_all_protected_ranges,
    get_column_pixel_sizes,
    read_sheet_to_dataframe,
    move_sheet_tab_to_index,
    rename_sheet_tab,
    resolve_drive_folder_id_by_name,
    shade_columns_except_last_n,
    protect_columns_except_last_n,
    set_column_pixel_size,
    share_spreadsheet,
    spreadsheet_exists,
    write_dataframe,
    write_tournament_score_leaderboard_sheet,
    write_tournament_score_totals_sheet,
    OrphanNamedRangeError,
    GoogleClientsProtocol,
    GoogleClients, write_data_to_tournament_score_sheet
)

from GoogleSheetReaderWriter.gsheet_rw.registry import get_registered_id, load_registry, save_registry, set_registered_id

DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[1]
    / "GoogleSheetReaderWriter"
    / "config"
    / "config.yaml"
)
CONFIG_ENV_VAR = "GSHEET_RW_CONFIG_PATH"


class WorkingGuideGoogleSheetError(RuntimeError):
    """Raised when uploading the working guide data to Sheets fails."""


FALLBACK_EXPECTED_COLUMNS = [
    "Division",
    "Rank",
    "Age",
    "Last Name",
    "Ring #",
    "Competitor Count",
    "Judge Assigned",
    "Comments",
]


def _get_gsheet_app():
    from GoogleSheetReaderWriter.gsheet_rw import app as gsheet_app
    # try:
    #     from GoogleSheetReaderWriter.gsheet_rw import app as gsheet_app
    # except ModuleNotFoundError as exc:
    #     raise WorkingGuideGoogleSheetError(
    #         "Google Sheets integration is unavailable because a dependency is missing: "
    #         f"{exc.name}. Install the Google client dependencies or disable uploads."
    #     ) from exc
    return gsheet_app


def upload_tournament_score_data(
    working_guilde_list: list[list[list[str]]],
    dojo_list_directory: Union[str, pathlib.Path],
    *,
    _allow_recreate_on_orphan: bool = True,
) -> Optional[str]:

    clients: GoogleClients = None
    config_path: Optional[str | Path] = None
    share_role: str = "writer"
    unprotected_last_n: int = 2


    if working_guilde_list is None or len(working_guilde_list) == 0:
        logging.info("Working guide list is empty; skipping Google Sheet upload.")
        return None

    # Validate expected structure: timeslots -> rows -> cells.
    if isinstance(working_guilde_list, pd.DataFrame):
        raise TypeError(
            "upload_tournament_score_data expected timeslot list data, but received a DataFrame. "
            "Pass working_guide_list, not working_guide_dataframe."
        )
    first_timeslot = working_guilde_list[0]
    if isinstance(first_timeslot, str) or not isinstance(first_timeslot, list):
        raise TypeError(
            "upload_tournament_score_data expected list[list[list[str]]]. "
            "Each timeslot must be a list of rows."
        )

    # Read the list of Dojos from 'ParticipatingDojos.csv' in the dojo_list_directory
    import csv

    colorado = []
    out_of_state = []

    dojo_list_directory = Path(dojo_list_directory)
    participating_dojos_path = dojo_list_directory / "ParticipatingDojos.csv"
    with open(participating_dojos_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dojo = row["DOJO"].strip()
            group = row["GROUP"].strip()

            if group == "Colorado":
                colorado.append(dojo)
            elif group == "Out of State":
                out_of_state.append(dojo)

    colorado.sort()
    out_of_state.sort()

    all_dojos = _deduplicate_dojo_names(colorado + out_of_state)

    # try:
    #     gsheet_app = _get_gsheet_app()
    # except WorkingGuideGoogleSheetError as exc:
    #     logging.warning("%s", exc)
    #     return None
    #
    # normalized_df = _prepare_dataframe(dataframe, expected_columns=gsheet_app.EXPECTED_COLUMNS)
    # resolved_config = _resolve_config_path(config_path)
    try:
        config_path = _resolve_config_path(config_path)
    except WorkingGuideGoogleSheetError as exc:
        logging.warning("%s Upload skipped.", exc)
        return None


    # tmp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
    # tmp_file.close()
    # tmp_path = Path(tmp_file.name)

    from GoogleSheetReaderWriter.gsheet_rw.app import AppConfig
    cfg = AppConfig.load(config_path)
    drive_folder_id = cfg.drive_folder_id
    spreadsheet_title = cfg.tournament_score_spreadsheet_title
    worksheet_title = cfg.tournament_score_worksheet_title

    if not drive_folder_id:
        raise ValueError("Missing drive folder name. Provide drive_folder_name or set it in config/config.yaml.")

    if not spreadsheet_title:
        raise ValueError("Missing spreadsheet title. Provide sheet_title or set spreadsheet_title in config/config.yaml.")

    if not worksheet_title:
        raise ValueError("Missing worksheet title. Provide worksheet_title or set worksheet_title in config/config.yaml.")

    if clients is None:
        clients = build_clients_from_config(cfg)
    protected_range_editor_emails = build_protected_range_editor_accounts(
        clients,
        cfg.protected_range_editor_accounts or [cfg.owner_email],
    )
    registry_path = (
        Path(config_path).expanduser().resolve().parent.parent / "data" / "sheet_registry.yaml"
    )
    registry = load_registry(registry_path)

    registry_key = drive_folder_id
    # drive_folder_id = None
    # if folder_name != "root":
    #     drive_folder_id = resolve_drive_folder_id_by_name(clients, folder_name)

    existing_id = get_registered_id(registry, registry_key, spreadsheet_title)
    if existing_id and not spreadsheet_exists(clients, existing_id):
        existing_id = None

    created_new = False
    if existing_id:
        spreadsheet_id = existing_id
    else:
        spreadsheet_id, _ = create_spreadsheet(
            clients=clients,
            title=spreadsheet_title,
            worksheet_title=worksheet_title,
            drive_folder_id=drive_folder_id,
        )
        set_registered_id(registry, registry_key, spreadsheet_title, spreadsheet_id)
        save_registry(registry_path, registry)
        created_new = True
        logging.getLogger(__name__).info(
            "Created tournament score spreadsheet '%s' (id=%s).",
            spreadsheet_title,
            spreadsheet_id,
        )

    try:
        deleted_tabs = 0
        deleted_named_ranges = delete_all_named_ranges(clients, spreadsheet_id)
        deleted_protected_ranges = delete_all_protected_ranges(clients, spreadsheet_id)
        if not created_new:
            deleted_tabs = _delete_all_tabs_except_first(clients, spreadsheet_id)

        tab_metadata = _list_sheet_tab_metadata(clients, spreadsheet_id)
        if not tab_metadata:
            raise RuntimeError("Spreadsheet has no tabs after cleanup.")

        first_tab_id = int(tab_metadata[0]["sheetId"])

        # Overwrite tabs deterministically each run.
        used_sheet_titles: set[str] = set()
        timeslot_tab_info: list[dict[str, int | str]] = []
        for idx, timeslot in enumerate(working_guilde_list):
            sheet_title = _make_unique_sheet_title(
                _timeslot_sheet_title(timeslot, idx),
                used_sheet_titles,
            )
            if idx == 0:
                rename_sheet_tab(clients, spreadsheet_id, first_tab_id, sheet_title)
                sheet_id = first_tab_id
                clear_sheet_values(clients, spreadsheet_id, sheet_title)
            else:
                sheet_id = add_sheet_tab(clients, spreadsheet_id, sheet_title)
            write_data_to_tournament_score_sheet(
                clients,
                spreadsheet_id,
                sheet_title,
                timeslot,
                all_dojos,
                protected_range_editor_emails,
            )
            timeslot_tab_info.append({"title": sheet_title, "sheet_id": sheet_id})

        totals_sheet_title = "Totals"
        totals_sheet_id = add_sheet_tab(clients, spreadsheet_id, totals_sheet_title)
        write_tournament_score_totals_sheet(
            clients=clients,
            spreadsheet_id=spreadsheet_id,
            worksheet_title=totals_sheet_title,
            values=_build_totals_sheet_values(timeslot_tab_info, all_dojos),
            dojo_names=all_dojos,
            protected_range_editor_emails=protected_range_editor_emails,
        )
        move_sheet_tab_to_index(
            clients=clients,
            spreadsheet_id=spreadsheet_id,
            sheet_id=totals_sheet_id,
            index=len(timeslot_tab_info),
        )

        leaderboard_sheet_title = "Leader Board"
        leaderboard_sheet_id = add_sheet_tab(clients, spreadsheet_id, leaderboard_sheet_title)
        write_tournament_score_leaderboard_sheet(
            clients=clients,
            spreadsheet_id=spreadsheet_id,
            worksheet_title=leaderboard_sheet_title,
            dojo_names=all_dojos,
            protected_range_editor_emails=protected_range_editor_emails,
        )
        move_sheet_tab_to_index(
            clients=clients,
            spreadsheet_id=spreadsheet_id,
            sheet_id=leaderboard_sheet_id,
            index=len(timeslot_tab_info) + 1,
        )
    except OrphanNamedRangeError as exc:
        if not _allow_recreate_on_orphan:
            raise

        replacement_spreadsheet_id, _ = create_spreadsheet(
            clients=clients,
            title=spreadsheet_title,
            worksheet_title=worksheet_title,
            drive_folder_id=drive_folder_id,
        )
        set_registered_id(registry, registry_key, spreadsheet_title, replacement_spreadsheet_id)
        save_registry(registry_path, registry)
        logging.getLogger(__name__).warning(
            "Spreadsheet %s contains orphaned named ranges that block reset (example: %s). "
            "Created replacement spreadsheet %s and retrying the tournament score upload there.",
            spreadsheet_id,
            exc.range_name,
            replacement_spreadsheet_id,
        )
        return upload_tournament_score_data(
            working_guilde_list,
            dojo_list_directory,
            _allow_recreate_on_orphan=False,
        )


    share_spreadsheet(clients, spreadsheet_id, cfg.share_emails, role=share_role)

    logging.getLogger(__name__).info(
        "Tournament score spreadsheet ready: id=%s, tabs_written=%s, tabs_deleted=%s, "
        "named_ranges_deleted=%s, protected_ranges_deleted=%s, dojos=%s.",
        spreadsheet_id,
        len(working_guilde_list) + 2,
        deleted_tabs,
        deleted_named_ranges,
        deleted_protected_ranges,
        len(all_dojos),
    )
    return spreadsheet_id

def _timestamp_tab_title() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _latest_timestamp_tab_title(clients, spreadsheet_id: str) -> str:
    titles = _list_sheet_titles(clients, spreadsheet_id)
    parsed = []
    for title in titles:
        try:
            parsed.append((datetime.strptime(title, "%Y-%m-%d %H:%M:%S"), title))
        except ValueError:
            continue
    if not parsed:
        raise ValueError("No timestamp-named sheets found. Provide worksheet_title explicitly.")
    parsed.sort()
    return parsed[-1][1]


def _list_sheet_titles(clients, spreadsheet_id: str) -> list[str]:
    meta = clients.sheets.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        fields="sheets(properties(title))",
    ).execute()
    return [s.get("properties", {}).get("title", "") for s in meta.get("sheets", [])]


def _extract_timeslot_label(timeslot: list[list[str]]) -> str:
    """Return a readable label like '9:00 a.m.' from a timeslot payload."""
    if isinstance(timeslot, list) and timeslot:
        first_row = timeslot[0]
        if isinstance(first_row, list) and first_row:
            label = str(first_row[0]).strip()
            if label:
                return label
        label = str(first_row).strip()
        if label:
            return label
    return "Unknown"


def _sanitize_sheet_title(title: str) -> str:
    """Google Sheets titles cannot include: : \\ / ? * [ ] and must be <=100 chars."""
    sanitized = re.sub(r'[:\\/?*\[\]]', "-", str(title)).strip()
    if not sanitized:
        sanitized = "Timeslot"
    return sanitized[:100]


def _list_sheet_tab_metadata(clients, spreadsheet_id: str) -> list[dict]:
    meta = clients.sheets.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        fields="sheets(properties(sheetId,title,index))",
    ).execute()
    tabs = [s.get("properties", {}) for s in meta.get("sheets", [])]
    tabs.sort(key=lambda x: int(x.get("index", 0)))
    return tabs


def _delete_all_tabs_except_first(clients, spreadsheet_id: str) -> int:
    tabs = _list_sheet_tab_metadata(clients, spreadsheet_id)
    if len(tabs) <= 1:
        return 0

    requests = [
        {"deleteSheet": {"sheetId": int(tab["sheetId"])}}
        for tab in tabs[1:]
    ]
    clients.sheets.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests},
    ).execute()
    return len(requests)


def _timeslot_sheet_title(timeslot: list[list[str]], index: int) -> str:
    label = _extract_timeslot_label(timeslot)
    # return _sanitize_sheet_title(f"Timeslot {index + 1:02d} - {label}")
    return _sanitize_sheet_title(f"{label}")


def _make_unique_sheet_title(base_title: str, used_titles: set[str]) -> str:
    candidate = _sanitize_sheet_title(base_title)
    if candidate not in used_titles:
        used_titles.add(candidate)
        return candidate

    suffix_index = 2
    while True:
        suffix = f" ({suffix_index})"
        truncated_base = candidate[: max(0, 100 - len(suffix))].rstrip()
        deduped = f"{truncated_base}{suffix}"
        if deduped not in used_titles:
            used_titles.add(deduped)
            logging.getLogger(__name__).warning(
                "Duplicate timeslot tab title '%s' renamed to '%s' to keep sheet names unique.",
                candidate,
                deduped,
            )
            return deduped
        suffix_index += 1


def _time_row_indexes(df: pd.DataFrame) -> list[int]:
    if df.empty or df.shape[1] == 0:
        return []
    first_col = df.iloc[:, 0].astype(str).fillna("")
    rows: list[int] = []
    for idx, value in enumerate(first_col.tolist()):
        if _looks_like_time(value):
            # +1 to account for header row in the sheet.
            rows.append(idx + 1)
    return rows


def _looks_like_time(value: str) -> bool:
    v = value.strip().lower()
    if not v:
        return False
    time_re = r"\d{1,2}:\d{2}"
    ampm_re = r"(a\.?m\.?|p\.?m\.?|am|pm)"
    noon_re = r"(noon)"
    patterns = [
        rf"^{time_re}\s*{ampm_re}$",
        rf"^{time_re}\s*{noon_re}$",
        rf"^{noon_re}$",
    ]
    return any(re.match(p, v) for p in patterns)


def _build_totals_sheet_values(
    timeslot_tab_info: list[dict[str, int | str]],
    all_dojos: list[str],
) -> list[list[str]]:
    values: list[list[str]] = [["Timeslot"] + list(all_dojos)]
    for timeslot_info in timeslot_tab_info:
        sheet_title = str(timeslot_info["title"])
        sheet_id = int(timeslot_info["sheet_id"])
        row = [sheet_title]
        for dojo_name in all_dojos:
            named_range_name = build_tournament_score_named_range_name(
                worksheet_title=sheet_title,
                sheet_id=sheet_id,
                dojo_name=dojo_name,
            )
            row.append(f"={named_range_name}")
        values.append(row)

    total_row_index = len(values) + 1
    totals_row = ["Total"]
    for column_index in range(2, len(all_dojos) + 2):
        column_letter = _column_number_to_letter(column_index)
        totals_row.append(f"=SUM({column_letter}2:{column_letter}{total_row_index - 1})")
    values.append(totals_row)
    return values


def _column_number_to_letter(column_number: int) -> str:
    letters: list[str] = []
    while column_number > 0:
        column_number, remainder = divmod(column_number - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def _deduplicate_dojo_names(dojo_names: list[str]) -> list[str]:
    logger = logging.getLogger(__name__)
    seen_counts: dict[str, int] = {}
    used_names: set[str] = set()
    resolved_names: list[str] = []

    for original_name in dojo_names:
        base_name = str(original_name).strip()
        lookup_key = base_name.casefold()
        count = seen_counts.get(lookup_key, 0) + 1
        seen_counts[lookup_key] = count

        candidate_name = base_name if count == 1 else f"{base_name}-{count}"
        candidate_key = candidate_name.casefold()
        while candidate_key in used_names:
            count += 1
            seen_counts[lookup_key] = count
            candidate_name = f"{base_name}-{count}"
            candidate_key = candidate_name.casefold()

        if candidate_name != base_name:
            logger.warning(
                "Duplicate dojo name '%s' renamed to '%s' for spreadsheet export.",
                base_name,
                candidate_name,
            )

        used_names.add(candidate_key)
        resolved_names.append(candidate_name)

    return resolved_names


def _widen_columns_by_header(
    clients,
    spreadsheet_id: str,
    sheet_id: int,
    headers: list[str],
) -> None:
    targets = [
        ("Judge Assigned", 2),
        ("Comments", 4),
    ]
    sizes = get_column_pixel_sizes(clients, spreadsheet_id, sheet_id)
    for name, multiplier in targets:
        if name not in headers:
            continue
        idx = headers.index(name)
        base = sizes[idx] if idx < len(sizes) else 100
        set_column_pixel_size(clients, spreadsheet_id, sheet_id, idx, int(base * multiplier))




# def _prepare_dataframe(dataframe: pd.DataFrame, *, expected_columns) -> pd.DataFrame:
#     if not expected_columns:
#         expected_columns = FALLBACK_EXPECTED_COLUMNS
#     expected_columns = list(expected_columns)
#     normalized_df = dataframe.copy()
#
#     for column in expected_columns:
#         if column not in normalized_df.columns:
#             normalized_df[column] = ""
#
#     normalized_df = normalized_df[expected_columns]
#     normalized_df = normalized_df.fillna("")
#     return normalized_df


def _resolve_config_path(candidate: Optional[str | Path]) -> Path:
    configured = candidate or os.environ.get(CONFIG_ENV_VAR) or DEFAULT_CONFIG_PATH
    path = Path(configured).expanduser()
    if not path.is_absolute():
        path = (Path(__file__).resolve().parents[1] / path).resolve()
    else:
        path = path.resolve()
    if not path.exists():
        raise WorkingGuideGoogleSheetError(
            f"Google Sheet config not found at {path}. Set {CONFIG_ENV_VAR} or pass config_path explicitly."
        )
    return path
