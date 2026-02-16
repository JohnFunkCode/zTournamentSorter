# GUI/headercorrector/header_corrector_dialog.py
import os
import csv
import re
import chardet
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import reports.FileHandlingUtilities



# Regex-based auto-mapping (first match wins)
AUTO_MAP_PATTERNS = [
    (re.compile(r".*Registrant.*", re.I), "Registrant_ID"),
    (re.compile(r".*Reg\s*ID.*", re.I), "Registrant_ID"),
    (re.compile(r"^ID$", re.I), "Registrant_ID"),
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
    (re.compile(r".*Ticket.*|.*Spectator.*|.*Gen.*Adm.*", re.I), "Spectator_Tickets"),
]

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

UNASSIGNED = "— Select —"
SEP_CHAR = "│"
CHECK = "✓ "
QMARK = "? "

class HeaderCorrectorDialog(ttk.Frame):
    def __init__(self, parent_toplevel: tk.Toplevel, app_container, on_done):
        super().__init__(parent_toplevel)
        self.parent_tl = parent_toplevel
        self.app = app_container
        self.on_done = on_done

        self.parent_tl.title("Correct Column Headers")
        self.parent_tl.transient(app_container.winfo_toplevel())
        self.parent_tl.grab_set()

        self.csv_path = getattr(self.app, "input_data_filename", None)
        self.source_encoding = "utf-8-sig"
        self.original_headers = []
        self.preview_rows = []
        self.assigned = {}
        self.display_cols = []
        self.popup = None
        self._popup_var = None

        outer = ttk.Frame(self.parent_tl, padding=12)
        outer.pack(fill="both", expand=True)

        toolbar = ttk.Frame(outer)
        toolbar.pack(fill="x", pady=(0, 6))
        ttk.Button(toolbar, text="Auto Map", command=self.auto_assign_common).pack(side="left")
        ttk.Button(toolbar, text="Save & Continue", command=self._export_and_finish).pack(side="left")

        self.remaining_label = ttk.Label(outer, text="")
        self._remaining_default_fg = self.remaining_label.cget("foreground")
        self.remaining_label.pack(fill="x", pady=(0, 6))

        table_container = ttk.Frame(outer)
        table_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_container, show="headings", height=22)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Treeview", rowheight=26)
        self.tree.tag_configure("oddrow", background="#f7f7fb")
        self.tree.tag_configure("evenrow", background="#ffffff")

        self._load_csv()
        self._update_remaining_label()

    def _load_csv(self):
        if not self.csv_path or not os.path.isfile(self.csv_path):
            messagebox.showerror("Error", "CSV file not found.")
            return
        try:
            with open(self.csv_path, "rb") as f:
                sniff = f.read(4096)
            enc = chardet.detect(sniff).get("encoding") or "utf-8"
            self.source_encoding = enc
            with open(self.csv_path, "r", newline="", encoding=enc, errors="replace") as f:
                rows = list(csv.reader(f))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV:\n{e}")
            return
        if not rows:
            messagebox.showerror("Error", "CSV is empty.")
            return

        rows = self._prune_empty_columns(rows)
        self.original_headers = rows[0]
        self.preview_rows = rows
        self.assigned.clear()
        self._rebuild_table()

    def _prune_empty_columns(self, rows):
        # Normalize lengths
        max_len = max(len(r) for r in rows)
        for r in rows:
            if len(r) < max_len:
                r.extend([""] * (max_len - len(r)))
        header = rows[0]
        data_rows = rows[1:]
        keep_indices = []
        for i, h in enumerate(header):
            hdr_blank = (h.strip() == "")
            data_blank = all((row[i].strip() == "") for row in data_rows)
            if not (hdr_blank and data_blank):
                keep_indices.append(i)
        # if len(keep_indices) != max_len:
        #     pruned = max_len - len(keep_indices)
        #     try:
        #         messagebox.showinfo("Pruned Columns", f"Removed {pruned} completely empty column(s).")
        #     except Exception:
        #         pass
        new_rows = []
        for r in rows:
            new_rows.append([r[i] for i in keep_indices])
        return new_rows

    def auto_assign_common(self):
        if not self.original_headers:
            return
        taken = {v for v in self.assigned.values() if v in VALID_HEADERS}
        made = []
        for idx, raw in enumerate(self.original_headers):
            if idx in self.assigned and self.assigned[idx] in VALID_HEADERS:
                continue
            txt = (raw or "").strip()
            if not txt:
                continue
            for patt, target in AUTO_MAP_PATTERNS:
                if patt.match(txt) and target not in taken:
                    self.assigned[idx] = target
                    taken.add(target)
                    made.append((idx, raw, target))
                    break
        self._update_headings_only()
        self._update_remaining_label()
        if made:
            # Show all auto-mapped canonical column names (no truncation)
            targets = [tgt for _, _, tgt in made]
            msg = "\n".join(f"  • {t}" for t in targets)
            messagebox.showinfo("Auto Map", f"Auto-assigned {len(targets)} column(s):\n{msg}")
        else:
            messagebox.showinfo("Auto Map", "No additional columns were auto-assigned.")

    def _heading_title_for(self, col_index: int) -> str:
        chosen = self.assigned.get(col_index, UNASSIGNED)
        base = chosen if chosen != UNASSIGNED else self.original_headers[col_index]
        return (CHECK if chosen in VALID_HEADERS else QMARK) + base

    def _rebuild_table(self):
        self.display_cols.clear()
        n = len(self.original_headers)
        for i in range(n):
            self.display_cols.append(("data", i))
            if i != n - 1:
                self.display_cols.append(("sep", None))

        col_ids = [f"C{i}" for i in range(len(self.display_cols))]
        self.tree["columns"] = col_ids

        for disp_i, (kind, data_idx) in enumerate(self.display_cols):
            cid = col_ids[disp_i]
            if kind == "data":
                title = self._heading_title_for(data_idx)
                self.tree.heading(cid, text=title,
                                  command=lambda ix=data_idx: self._open_popup(ix))
                self.tree.column(cid, width=max(120, min(260, len(title) * 9)),
                                 stretch=True, anchor="w")
            else:
                self.tree.heading(cid, text="")
                self.tree.column(cid, width=6, stretch=False, anchor="center")

        for item in self.tree.get_children():
            self.tree.delete(item)

        for r_index, row in enumerate(self.preview_rows):
            padded = (row + [""] * len(self.original_headers))[:len(self.original_headers)]
            values = []
            for kind, data_idx in self.display_cols:
                if kind == "data":
                    values.append(padded[data_idx])
                else:
                    values.append(SEP_CHAR)
            tag = "evenrow" if (r_index % 2 == 0) else "oddrow"
            self.tree.insert("", "end", values=values, tags=(tag,))

    def _update_headings_only(self):
        for disp_i, (kind, data_idx) in enumerate(self.display_cols):
            if kind != "data":
                continue
            cid = self.tree["columns"][disp_i]
            title = self._heading_title_for(data_idx)
            self.tree.heading(cid, text=title,
                              command=lambda ix=data_idx: self._open_popup(ix))
            self.tree.column(cid, width=max(120, min(260, len(title) * 9)))

    def _open_popup(self, col_index: int):
        self._close_popup()
        self.popup = tk.Toplevel(self.parent_tl)
        self.popup.transient(self.parent_tl)
        self.popup.attributes("-topmost", True)

        x = self.winfo_pointerx() + 8
        y = self.winfo_pointery() + 8
        sw = self.parent_tl.winfo_screenwidth()
        sh = self.parent_tl.winfo_screenheight()
        w = 320
        h = 140
        if x + w > sw - 4:
            x = sw - w - 4
        if y + h > sh - 4:
            y = sh - h - 4
        self.popup.geometry(f"{w}x{h}+{x}+{y}")
        self.popup.grab_set()

        frame = ttk.Frame(self.popup, padding=10, relief="solid", borderwidth=1)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame,
                  text=f"File header: {self.original_headers[col_index]}",
                  font=("", 9, "italic")).pack(anchor="w", pady=(0, 6))

        current = self.assigned.get(col_index, UNASSIGNED)
        options = [UNASSIGNED] + self._available_valid_headers_for(col_index)

        raw_orig = self.original_headers[col_index]
        if raw_orig not in options and raw_orig not in VALID_HEADERS:
            options.append(raw_orig)

        self._popup_var = tk.StringVar(value=current)
        cb = ttk.Combobox(frame, values=options, textvariable=self._popup_var,
                          state="readonly", width=34)
        cb.pack(anchor="w")
        self.popup.focus_set()

        btns = ttk.Frame(frame)
        btns.pack(anchor="w", pady=(10, 0))
        ttk.Button(btns, text="OK",
                   command=lambda: self._apply_choice(col_index, self._popup_var.get())
                   ).pack(side="left")
        ttk.Button(btns, text="Cancel",
                   command=self._close_popup).pack(side="left", padx=6)

        cb.bind("<<ComboboxSelected>>",
                lambda _e: self._apply_choice(col_index, self._popup_var.get()))
        self.popup.bind("<Escape>", lambda _e: self._close_popup())

    def _apply_choice(self, idx: int, choice: str):
        if choice == UNASSIGNED:
            self.assigned.pop(idx, None)
        else:
            if choice in VALID_HEADERS:
                other = self._find_column_with_header(choice)
                if other is not None and other != idx:
                    self.assigned.pop(other, None)
                self.assigned[idx] = choice
            else:
                self.assigned.pop(idx, None)
        self._close_popup()
        self._update_headings_only()
        self._update_remaining_label()

    def _close_popup(self):
        if self.popup:
            try:
                self.popup.destroy()
            except Exception:
                pass
            self.popup = None
            self._popup_var = None
            try:
                self.parent_tl.grab_set()
            except Exception:
                pass

    def _update_remaining_label(self):
        remaining = [h for h in VALID_HEADERS if h not in self._assigned_valid_set()]
        if remaining:
            self.remaining_label.config(text="Remaining: " + ", ".join(remaining), foreground="red")
        else:
            self.remaining_label.config(text="All valid headers assigned.", foreground=self._remaining_default_fg)

    def _build_corrected_headers(self):
        corrected = []
        for idx, original in enumerate(self.original_headers):
            chosen = self.assigned.get(idx, UNASSIGNED)
            corrected.append(chosen if chosen != UNASSIGNED else original)
        return corrected

    def _export_and_finish(self):
        if not self.original_headers:
            messagebox.showerror("Error", "No data loaded.")
            return
        corrected = self._build_corrected_headers()

        out_dir = getattr(self.app, "tournament_output_folder_path", None) \
                  or os.path.dirname(self.csv_path) or "."
        os.makedirs(out_dir, exist_ok=True)
        stem, _ = os.path.splitext(os.path.basename(self.csv_path))
        # out_path = os.path.join(out_dir, f"{stem}-FixedHeaders.csv")
        next_file = reports.FileHandlingUtilities.next_versioned_filename(str(self.csv_path))
        out_path = os.path.join(out_dir, next_file)

        try:
            with open(self.csv_path, "r", newline="", encoding=self.source_encoding, errors="replace") as f:
                rows = list(csv.reader(f))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to re-read original file:\n{e}")
            return
        if not rows:
            messagebox.showerror("Error", "Source file empty.")
            return

        rows = self._prune_empty_columns(rows)
        data_rows = rows[1:]

        try:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(corrected)
                w.writerows(data_rows)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write corrected file:\n{e}")
            return

        self.app.input_data_filename = out_path
        messagebox.showinfo("Saved", f"Corrected file saved:\n{out_path}")
        self._finish()

    def _finish(self):
        # Release any grabs, then destroy this dialog, then schedule the callback on the main loop
        try:
            self.parent_tl.grab_release()
        except Exception:
            pass
        try:
            self.parent_tl.destroy()
        except Exception:
            pass
        if callable(self.on_done):
            try:
                # Schedule on the main event loop to avoid running during teardown
                self.after(0, self.on_done)
            except Exception:
                try:
                    self.parent_tl.after(0, self.on_done)
                except Exception:
                    pass

    def _cancel(self):
        if messagebox.askyesno("Cancel", "Cancel header correction?"):
            self._finish()

    def _assigned_valid_set(self):
        return {v for v in self.assigned.values() if v in VALID_HEADERS}

    def _available_valid_headers_for(self, idx: int):
        current = self.assigned.get(idx, UNASSIGNED)
        taken = self._assigned_valid_set()
        avail = [h for h in VALID_HEADERS if (h not in taken) or (h == current)]
        if not avail:
            avail = VALID_HEADERS.copy()
        return avail

    def _find_column_with_header(self, header: str):
        for cidx, val in self.assigned.items():
            if val == header:
                return cidx
        return None
