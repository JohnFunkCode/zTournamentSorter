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
    build_clients_from_config,
    create_spreadsheet,
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
) -> Optional[str]:

    clients: GoogleClients = None
    config_path: str = "./GoogleSheetReaderWriter/config/config.yaml"
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

    all_dojos = colorado + out_of_state

    # try:
    #     gsheet_app = _get_gsheet_app()
    # except WorkingGuideGoogleSheetError as exc:
    #     logging.warning("%s", exc)
    #     return None
    #
    # normalized_df = _prepare_dataframe(dataframe, expected_columns=gsheet_app.EXPECTED_COLUMNS)
    # resolved_config = _resolve_config_path(config_path)
    config_path = _resolve_config_path(config_path)


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
            f"event=spreadsheet_created spreadsheet_id={spreadsheet_id} title={spreadsheet_title}"
        )

    deleted_tabs = 0
    if not created_new:
        deleted_tabs = _delete_all_tabs_except_first(clients, spreadsheet_id)

    tab_metadata = _list_sheet_tab_metadata(clients, spreadsheet_id)
    if not tab_metadata:
        raise RuntimeError("Spreadsheet has no tabs after cleanup.")

    first_tab_id = int(tab_metadata[0]["sheetId"])

    # Overwrite tabs deterministically each run.
    for idx, timeslot in enumerate(working_guilde_list):
        sheet_title = _timeslot_sheet_title(timeslot, idx)
        if idx == 0:
            rename_sheet_tab(clients, spreadsheet_id, first_tab_id, sheet_title)
        else:
            add_sheet_tab(clients, spreadsheet_id, sheet_title)
        # then write the data to the sheet
        write_data_to_tournament_score_sheet(clients, spreadsheet_id, sheet_title, timeslot, all_dojos)


    share_spreadsheet(clients, spreadsheet_id, cfg.share_emails, role=share_role)

    logging.getLogger(__name__).info(
        f"event=spreadsheet_updated spreadsheet_id={spreadsheet_id} created_new={created_new} deleted_tabs={deleted_tabs} tabs_written={len(working_guilde_list)}",
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
    if not path.exists():
        raise WorkingGuideGoogleSheetError(
            f"Google Sheet config not found at {path}. Set {CONFIG_ENV_VAR} or pass config_path explicitly."
        )
    return path
