# python
import os
import csv
import re
import chardet
import tkinter as tk
from tkinter import ttk, messagebox

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
    (re.compile(r".*Ticket.*|.*Spectator.*", re.I), "Spectator_Tickets"),
]

VALID_HEADERS = [
    "Registrant_ID","First_Name","Last_Name","Gender","Dojo","Out_of_State_Dojo",
    "Age","Weight","Height","Division","Rank","Events","Weapons","Spectator_Tickets"
]

UNASSIGNED = "— Select —"
CHECK = "✓ "
QMARK = "? "
SEP_CHAR = "│"

class HeaderCorrectorDialog(ttk.Frame):
    def __init__(self, parent_toplevel: tk.Toplevel, app_container, on_done):
        super().__init__(parent_toplevel)
        self.parent_tl = parent_toplevel
        self.app = app_container
        self.on_done = on_done
        self.parent_tl.title("Correct Column Headers")
        self.parent_tl.transient(app_container)
        self.parent_tl.grab_set()

        self.csv_path = self.app.input_data_filename
        self.original_headers = []
        self.preview_rows = []
        self.assigned = {}
        self.display_cols = []
        self.popup = None
        self.source_encoding = "utf-8-sig"

        outer = ttk.Frame(self.parent_tl, padding=12)
        outer.pack(fill="both", expand=True)
        toolbar = ttk.Frame(outer)
        toolbar.pack(fill="x", pady=(0,6))
        ttk.Button(toolbar, text="Auto Map", command=self.auto_assign_common).pack(side="left")
        ttk.Button(toolbar, text="Save & Continue", command=self._export_and_finish).pack(side="left")
        # ttk.Button(toolbar, text="Cancel", command=self._cancel).pack(side="right", padx=(0,8))

        self.remaining_label = ttk.Label(outer, text="")
        self.remaining_label.pack(fill="x", pady=(0,6))

        table_container = ttk.Frame(outer)
        table_container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(table_container, show="headings", height=22)
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
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

        self.bind_all("<Button-1>", self._maybe_close_popup, add="+")
        self._load_csv()
        self._update_remaining_label()

    # ---------- Load ----------
    def _load_csv(self):
        if not self.csv_path or not os.path.isfile(self.csv_path):
            messagebox.showerror("Error", "CSV file not found.")
            self._cancel()
            return
        try:
            with open(self.csv_path, "rb") as f:
                raw = f.read(4096)
            enc = chardet.detect(raw).get("encoding") or "utf-8"
            self.source_encoding = enc
            with open(self.csv_path, "r", newline="", encoding=enc, errors="replace") as f:
                rows = list(csv.reader(f))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read CSV:\n{e}")
            self._cancel()
            return
        if not rows:
            messagebox.showerror("Error", "CSV is empty.")
            self._cancel()
            return
        self.original_headers = rows[0]
        self.preview_rows = rows
        self._rebuild_table()

    # ---------- Auto map ----------
    def auto_assign_common(self):
        if not self.original_headers:
            return
        taken = {v for v in self.assigned.values() if v in VALID_HEADERS}
        made_details = []  # (col_index, original_raw, mapped_header)
        for idx, raw in enumerate(self.original_headers):
            if idx in self.assigned and self.assigned[idx] in VALID_HEADERS:
                continue
            t = (raw or "").strip()
            if not t:
                continue
            for patt, target in AUTO_MAP_PATTERNS:
                if patt.match(t) and target not in taken:
                    self.assigned[idx] = target
                    taken.add(target)
                    made_details.append((idx, raw, target))
                    break

        self._update_headings_only()
        self._update_remaining_label()

        if made_details:
            # Show all auto-mapped columns (no limit); strip surrounding whitespace
            lines = [
                f"  • Col {col_idx + 1}: \"{orig.strip()}\" → {mapped}"
                for (col_idx, orig, mapped) in made_details
            ]

            messagebox.showinfo(
                "Auto Map",
                f"Auto-assigned {len(made_details)} column(s):\n" + "\n".join(lines)
            )
        else:
            messagebox.showinfo("Auto Map", "No additional columns were auto-assigned.")

    # ---------- Table ----------
    def _heading_title_for(self, idx):
        chosen = self.assigned.get(idx, UNASSIGNED)
        base = chosen if chosen != UNASSIGNED else self.original_headers[idx]
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
        for disp_i, (kind, d_i) in enumerate(self.display_cols):
            cid = col_ids[disp_i]
            if kind == "data":
                title = self._heading_title_for(d_i)
                self.tree.heading(cid, text=title, command=lambda ix=d_i: self._on_header_click(ix))
                self.tree.column(cid, width=max(120, min(260, len(title)*9)), stretch=True, anchor="w")
            else:
                self.tree.heading(cid, text="")
                self.tree.column(cid, width=6, stretch=False)
        for r in self.tree.get_children():
            self.tree.delete(r)
        for r_index, r in enumerate(self.preview_rows):
            row_vals = []
            src = (r + [""]*len(self.original_headers))[:len(self.original_headers)]
            for kind, d_i in self.display_cols:
                row_vals.append(src[d_i] if kind == "data" else SEP_CHAR)
            tag = "evenrow" if r_index % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row_vals, tags=(tag,))

    def _update_headings_only(self):
        for disp_i,(kind,d_i) in enumerate(self.display_cols):
            if kind != "data": continue
            cid = self.tree["columns"][disp_i]
            t = self._heading_title_for(d_i)
            self.tree.heading(cid, text=t, command=lambda ix=d_i: self._on_header_click(ix))
            self.tree.column(cid, width=max(120, min(260, len(t)*9)))

    # ---------- Popup ----------
    def _on_header_click(self, data_col_index: int):
        self._close_popup()
        self.popup = tk.Toplevel(self.parent_tl)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        x = self.winfo_pointerx() + 6
        y = self.winfo_pointery() + 6
        self.popup.geometry(f"+{x}+{y}")
        frame = ttk.Frame(self.popup, padding=8, relief="solid", borderwidth=1)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text=f"File header: {self.original_headers[data_col_index]}", font=("",9,"italic")).pack(anchor="w", pady=(0,6))
        current = self.assigned.get(data_col_index, UNASSIGNED)
        taken = {v for v in self.assigned.values() if v in VALID_HEADERS and v != current}
        options = [UNASSIGNED] + [h for h in VALID_HEADERS if h not in taken]
        var = tk.StringVar(value=current)
        cb = ttk.Combobox(frame, values=options, textvariable=var, state="readonly", width=28)
        cb.pack(anchor="w")
        cb.focus_set()
        btns = ttk.Frame(frame); btns.pack(pady=(8,0))
        ttk.Button(btns, text="OK", command=lambda: self._apply_choice(data_col_index, var.get())).pack(side="left")
        ttk.Button(btns, text="Cancel", command=self._close_popup).pack(side="left", padx=6)
        cb.bind("<<ComboboxSelected>>", lambda _e: self._apply_choice(data_col_index, var.get()))
        self.popup.bind("<Escape>", lambda _e: self._close_popup())

    def _apply_choice(self, idx, choice):
        if choice == UNASSIGNED:
            self.assigned.pop(idx, None)
        else:
            self.assigned[idx] = choice
        self._close_popup()
        self._update_headings_only()
        self._update_remaining_label()

    def _maybe_close_popup(self, event):
        if not self.popup: return
        w = event.widget
        if w is self.popup or str(w).startswith(str(self.popup)):
            return
        self._close_popup()

    def _close_popup(self):
        if self.popup:
            try: self.popup.destroy()
            except Exception: pass
            self.popup = None

    # ---------- Status / Export ----------
    def _update_remaining_label(self):
        remaining = [h for h in VALID_HEADERS if h not in {v for v in self.assigned.values() if v in VALID_HEADERS}]
        self.remaining_label.config(
            text=("Remaining: " + ", ".join(remaining)) if remaining else "All valid headers assigned."
        )

    def _build_corrected_headers(self):
        corrected = []
        for i, original in enumerate(self.original_headers):
            chosen = self.assigned.get(i, UNASSIGNED)
            corrected.append(chosen if (chosen != UNASSIGNED) else original)
        return corrected

    def _export_and_finish(self):
        if not self.original_headers:
            messagebox.showerror("Error", "Nothing loaded.")
            return
        corrected = self._build_corrected_headers()
        out_dir = self.app.tournament_output_folder_path or os.path.dirname(self.csv_path)
        os.makedirs(out_dir, exist_ok=True)
        stem, _ = os.path.splitext(os.path.basename(self.csv_path))
        out_path = os.path.join(out_dir, f"{stem}-FixedHeaders.csv")
        # Read full file again with detected encoding
        try:
            with open(self.csv_path, "r", newline="", encoding=self.source_encoding, errors="replace") as f:
                rows = list(csv.reader(f))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to re-read file:\n{e}")
            return
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
        try: self.parent_tl.grab_release()
        except Exception: pass
        self.parent_tl.destroy()
        if callable(self.on_done):
            self.on_done()

    def _cancel(self):
        if messagebox.askyesno("Cancel", "Cancel header correction?"):
            self._finish()