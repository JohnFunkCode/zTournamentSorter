#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSV Header Corrector — macOS/Tk safe with ✓ / ? marks
-----------------------------------------------------
- Click table headers to assign correct names via a popup dropdown.
- Assigned headers are prefixed with "✓ ", unassigned with "? ".
- Options shrink as you assign valid headers (no duplicates).
- Vertical separator columns "│" and zebra striping for readability.
- Status label lists the names of remaining (unassigned) valid headers.
"""

import csv
import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import chardet

import re

# Regex-based auto-mapping from common variants to VALID_HEADERS.
# Order matters: first match wins.
AUTO_MAP_PATTERNS = [
    (re.compile(r".*Registrant.*", re.I), "Registrant_ID"),
    (re.compile(r".*Reg\s*ID.*", re.I), "Registrant_ID"),
    (re.compile(r"^ID$", re.I), "Registrant_ID"),
    # (re.compile(r".*Registrant_ID.*", re.I), "Registrant_ID"),
    (re.compile(r".*\bF\s*Name\b.*", re.I), "First_Name"),
    (re.compile(r".*First.*", re.I), "First_Name"),
    (re.compile(r".*\bL\s*Name\b.*", re.I), "Last_Name"),
    (re.compile(r".*Last.*", re.I), "Last_Name"),
    (re.compile(r".*Gender.*|.*Sex.*", re.I), "Gender"),
    (re.compile(r"Dojo|Studio|.*Select.*Your.*Studio.*|.*Select.*Your.*Dojo.*", re.I), "Dojo"),
    (re.compile(r".*Out.*State.*", re.I), "Out_of_State_Dojo"),
    (re.compile(r".*Age.*", re.I), "Age"),
    (re.compile(r".*Weight.*", re.I), "Weight"),
    (re.compile(r".*Height.*", re.I), "Height"),
    (re.compile(r".*\bDiv(ision)?\b.*", re.I), "Division"),
    (re.compile(r".*Rank.*", re.I), "Rank"),
    (re.compile(r".*Events.*|.*category.*|.*Cat(egory)?.*|.*Forms.*|.*Spar.*|.*Tech.*", re.I), "Events"),
    (re.compile(r".*Weapon.*", re.I), "Weapons"),
    (re.compile(r".*Ticket.*|.*Spectator.*", re.I), "Spectator_Tickets"),
]

def _normalize(s: str) -> str:
    return (s or "").strip()

VALID_HEADERS = [
    "Registrant_ID",
    "First_Name",
    "Last_Name",
    "Gender",
    "Dojo",
    "Out_of_State_Dojo",
    "Age",
    "Weight",
    "Height",
    "Division",
    "Rank",
    "Events",
    "Weapons",
    "Spectator_Tickets",
]

DEFAULT_ATTACHED_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "RegExp_LizTrialFile_20250425-FixedHeaders.csv",
)

UNASSIGNED = "— Select —"
SEP_CHAR = "│"     # Unicode thin vertical bar
CHECK = "✓ "
QMARK = "? "


class HeaderCorrectorApp(tk.Tk):
    def __init__(self, initial_path: str = None):
        super().__init__()
        self.title("CSV Header Corrector — macOS safe")
        self.geometry("1600x900")
        self.minsize(1200, 700)
        self.option_add("*Font", ("Segoe UI", 11))

        self.csv_path = None
        self.original_headers = []
        self.preview_rows = []
        self.assigned = {}  # col_index -> chosen header (or UNASSIGNED)

        self.popup = None

        # Top toolbar
        toolbar = ttk.Frame(self, padding=(10, 8))
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.path_label = ttk.Label(toolbar, text="No file loaded", width=100)
        self.path_label.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(toolbar, text="Open CSV…", command=self.open_csv).pack(side=tk.LEFT)
        ttk.Button(toolbar, text="Export Corrected CSV", command=self.export_csv).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(toolbar, text="Assign All (Auto-map)", command=self.auto_assign_common).pack(side=tk.LEFT, padx=(8, 0))

        # (status moved below instructions)

        # Instructions
        help_text = """Click a data column header to assign its correct name.
Assigned columns show a ✓ prefix; unassigned show a ? prefix.
Thin '│' columns are visual separators only. First 10 rows shown below."""
        ttk.Label(self, text=help_text, padding=(10, 0), justify="left").pack(side=tk.TOP, anchor="w")

        # Status row (remaining headers) just above the column headers
        status_frame = ttk.Frame(self, padding=(10, 6))
        status_frame.pack(side=tk.TOP, fill=tk.X)
        self.remaining_label = ttk.Label(status_frame, text="", justify="left")
        self.remaining_label.pack(side=tk.LEFT)

        # Table container
        table_container = ttk.Frame(self, padding=(10, 10))
        table_container.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_container, show="headings", height=22)
        self.tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        # Styling
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Treeview", rowheight=26)
        self.tree.tag_configure("oddrow", background="#f7f7fb")
        self.tree.tag_configure("evenrow", background="#ffffff")

        # Display column mapping: [("data", idx) or ("sep", None), ...]
        self.display_cols = []

        if initial_path and os.path.exists(initial_path):
            self.load_csv(initial_path)
        elif os.path.exists(DEFAULT_ATTACHED_PATH):
            self.load_csv(DEFAULT_ATTACHED_PATH)

        # Close popup when clicking elsewhere
        self.bind_all("<Button-1>", self._maybe_close_popup, add="+")

        # setup encoding detection
        self.source_encoding = "utf-8-sig"  # default/fallback


    # ---------- Auto-assign using regex patterns ----------
    def auto_assign_common(self):
        """
        Try to assign unassigned columns by matching original header text against common patterns.
        Will not overwrite columns you've already assigned. Skips targets already taken.
        """
        if not self.original_headers:
            messagebox.showinfo("Nothing to assign", "Open a CSV first.")
            return

        made = []
        taken = {v for v in self.assigned.values() if v in VALID_HEADERS}
        for idx, raw in enumerate(self.original_headers):
            if idx in self.assigned and self.assigned[idx] in VALID_HEADERS:
                continue  # user already assigned
            text = _normalize(raw)
            if not text:
                continue
            for patt, target in AUTO_MAP_PATTERNS:
                if patt.match(text) and target in VALID_HEADERS and target not in taken:
                    self.assigned[idx] = target
                    taken.add(target)
                    made.append((idx, raw, target))
                    break  # first match wins

        self._update_headings_only()
        self._update_remaining_label()

        if made:
            # Show a short summary (cap at 10 entries to keep it readable)
            sample = "\n".join([f"  • Col {i+1}: \"{o}\" → {t}" for i, o, t in made[:10]])
            more = "" if len(made) <= 10 else f"\n  …and {len(made)-10} more."
            messagebox.showinfo("Auto-assign complete", f"Assigned {len(made)} column(s):\n{sample}{more}")
        else:
            messagebox.showinfo("Auto-assign complete", "No additional columns were auto-assigned.")

    # ---------- CSV I/O ----------
    def open_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if path:
            self.load_csv(path)

    # def load_csv(self, path: str):
    #     try:
    #         with open(path, "r", newline="", encoding="utf-8-sig") as f:
    #             reader = csv.reader(f)
    #             rows = list(reader)
    def load_csv(self, path: str):
        try:
            with open(path, "rb") as f:
                rawdata = f.read(4096)
            result = chardet.detect(rawdata)
            encoding = result.get("encoding") or "utf-8"
            self.source_encoding = encoding  # store for later export/readback

            with open(path, "r", newline="", encoding=encoding) as f:
                reader = csv.reader(f)
                rows = list(reader)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CSV:\n{e}")
            return

        if not rows:
            messagebox.showerror("Error", "CSV appears to be empty.")
            return

        self.csv_path = path
        self.path_label.config(text=f"Loaded: {path}")
        self.original_headers = rows[0]
        self.preview_rows = rows
        self.assigned.clear()
        self._rebuild_table()
        self._update_remaining_label()

    # ---------- Helpers ----------
    def _assigned_valid_set(self):
        return {v for v in self.assigned.values() if v in VALID_HEADERS}

    def _available_valid_headers_for(self, idx: int):
        current = self.assigned.get(idx, UNASSIGNED)
        assigned = self._assigned_valid_set()
        return [h for h in VALID_HEADERS if (h not in assigned) or (h == current)]

    def _heading_title_for(self, idx: int) -> str:
        chosen = self.assigned.get(idx, UNASSIGNED)
        base = chosen if chosen != UNASSIGNED else self.original_headers[idx]
        if chosen in VALID_HEADERS:
            return CHECK + base
        return QMARK + base

    # ---------- Table building ----------
    def _rebuild_table(self):
        self.display_cols.clear()
        n = len(self.original_headers)
        for i in range(n):
            self.display_cols.append(("data", i))
            if i != n - 1:
                self.display_cols.append(("sep", None))

        col_ids = [f"COL{i}" for i in range(len(self.display_cols))]
        self.tree["columns"] = col_ids

        for disp_idx, (kind, data_idx) in enumerate(self.display_cols):
            colid = col_ids[disp_idx]
            if kind == "data":
                title = self._heading_title_for(data_idx)
                self.tree.heading(colid, text=title, command=lambda ix=data_idx: self._on_header_click(ix))
                self.tree.column(colid, width=max(120, min(260, len(title) * 9)), stretch=True, anchor="w")
            else:
                self.tree.heading(colid, text="")
                self.tree.column(colid, width=6, stretch=False, anchor="center")

        # Fill rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        for r_index, r in enumerate(self.preview_rows):
            src = (r + [""] * len(self.original_headers))[: len(self.original_headers)]
            values = []
            for kind, data_idx in self.display_cols:
                if kind == "data":
                    values.append(src[data_idx])
                else:
                    values.append(SEP_CHAR)
            tag = "evenrow" if (r_index % 2 == 0) else "oddrow"
            self.tree.insert("", "end", values=values, tags=(tag,))

    def _update_headings_only(self):
        for disp_idx, (kind, data_idx) in enumerate(self.display_cols):
            if kind != "data":
                continue
            colid = self.tree["columns"][disp_idx]
            title = self._heading_title_for(data_idx)
            self.tree.heading(colid, text=title, command=lambda ix=data_idx: self._on_header_click(ix))
            self.tree.column(colid, width=max(120, min(260, len(title) * 9)), stretch=True, anchor="w")

    # ---------- Popup for header selection ----------
    def _on_header_click(self, data_col_index: int):
        self._close_popup()

        self.popup = tk.Toplevel(self)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        x = self.winfo_pointerx() + 8
        y = self.winfo_pointery() + 8
        self.popup.geometry(f"+{x}+{y}")

        popup_frame = ttk.Frame(self.popup, padding=8, relief="solid", borderwidth=1)
        popup_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            popup_frame,
            text=f"File header: {self.original_headers[data_col_index]}",
            font=("", 9, "italic"),
        ).pack(anchor="w", pady=(0, 6))

        options = [UNASSIGNED] + self._available_valid_headers_for(data_col_index)
        original = self.original_headers[data_col_index]
        if original not in options:
            options.append(original)

        var = tk.StringVar(value=self.assigned.get(data_col_index, UNASSIGNED))
        cb = ttk.Combobox(popup_frame, textvariable=var, values=options, state="readonly", width=30)
        cb.pack(anchor="w")
        cb.focus_set()

        btns = ttk.Frame(popup_frame)
        btns.pack(fill=tk.X, pady=(8, 0))
        ttk.Button(btns, text="OK", command=lambda: self._apply_choice(data_col_index, var.get())).pack(side=tk.LEFT)
        ttk.Button(btns, text="Cancel", command=self._close_popup).pack(side=tk.LEFT, padx=(6, 0))

        cb.bind("<<ComboboxSelected>>", lambda _e: self._apply_choice(data_col_index, var.get()))
        self.popup.bind("<Escape>", lambda _e: self._close_popup())

    def _apply_choice(self, data_col_index: int, choice: str):
        if choice == UNASSIGNED:
            if data_col_index in self.assigned:
                del self.assigned[data_col_index]
        else:
            self.assigned[data_col_index] = choice

        self._close_popup()
        self._update_headings_only()
        self._update_remaining_label()

    def _maybe_close_popup(self, event):
        if self.popup is None:
            return
        widget = event.widget
        if widget is self.popup or str(widget).startswith(str(self.popup)):
            return
        self._close_popup()

    def _close_popup(self):
        if self.popup is not None:
            try:
                self.popup.destroy()
            except Exception:
                pass
            self.popup = None

    # ---------- Status & Export ----------
    def _update_remaining_label(self):
        remaining = [h for h in VALID_HEADERS if h not in {v for v in self.assigned.values() if v in VALID_HEADERS}]
        if remaining:
            self.remaining_label.config(text="Remaining headers: " + ", ".join(remaining))
        else:
            self.remaining_label.config(text="All valid headers assigned (or intentionally left as original).")

    def export_csv(self):
        if not self.csv_path:
            messagebox.showwarning("No file", "Open a CSV first.")
            return

        corrected = []
        for i, original in enumerate(self.original_headers):
            chosen = self.assigned.get(i, UNASSIGNED)
            corrected.append(chosen if chosen != UNASSIGNED else original)

        # Read full CSV using original detected encoding
        read_encoding = getattr(self, "source_encoding", "utf-8-sig")
        try:
            with open(self.csv_path, "r", newline="", encoding=read_encoding) as f:
                reader = list(csv.reader(f))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV for export:\n{e}")
            return

        if not reader:
            messagebox.showerror("Error", "CSV appears empty; nothing to export.")
            return

        data_rows = reader[1:]

        base, ext = os.path.splitext(self.csv_path)
        suggested = base + "_corrected" + ext
        out_path = filedialog.asksaveasfilename(
            title="Save corrected CSV",
            initialfile=os.path.basename(suggested),
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not out_path:
            return

        try:
            # Always write UTF-8
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(corrected)
                w.writerows(data_rows)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write corrected CSV:\n{e}")
            return

        messagebox.showinfo("Export complete", f"Saved corrected CSV:\n{out_path}")

def main():
    initial = None
    if len(sys.argv) > 1:
        candidate = sys.argv[1]
        if os.path.exists(candidate):
            initial = candidate
    elif os.path.exists(DEFAULT_ATTACHED_PATH):
        initial = DEFAULT_ATTACHED_PATH

    app = HeaderCorrectorApp(initial_path=initial)
    app.mainloop()


if __name__ == "__main__":
    main()
