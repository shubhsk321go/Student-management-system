import os
import sqlite3
import csv
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

DB_NAME = "todo.db"

STATUSES = ["To Do", "In Progress", "Completed"]


def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Offline To‑Do List (SQLite)")
        self.root.geometry("1000x620")
        self.root.minsize(900, 560)

        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row
        self.setup_db()

        self.build_ui()
        self.refresh_tasks()

    # ---------------- DB ---------------- #
    def setup_db(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'To Do',
                notes TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def create_task(self, title, status, notes):
        cur = self.conn.cursor()
        now = get_now()
        cur.execute(
            "INSERT INTO tasks (title, status, notes, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (title, status, notes, now, now),
        )
        self.conn.commit()

    def update_task(self, task_id, title=None, status=None, notes=None):
        fields = []
        values = []
        if title is not None:
            fields.append("title = ?")
            values.append(title)
        if status is not None:
            fields.append("status = ?")
            values.append(status)
        if notes is not None:
            fields.append("notes = ?")
            values.append(notes)
        fields.append("updated_at = ?")
        values.append(get_now())
        values.append(task_id)
        sql = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"
        cur = self.conn.cursor()
        cur.execute(sql, values)
        self.conn.commit()

    def delete_task(self, task_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def fetch_tasks(self, status_filter="All", search_term=""):
        cur = self.conn.cursor()
        base = "SELECT * FROM tasks"
        clauses = []
        params = []
        if status_filter != "All":
            clauses.append("status = ?")
            params.append(status_filter)
        if search_term:
            clauses.append("(title LIKE ? OR notes LIKE ?)")
            like = f"%{search_term}%"
            params.extend([like, like])
        if clauses:
            base += " WHERE " + " AND ".join(clauses)
        base += " ORDER BY CASE status WHEN 'To Do' THEN 0 WHEN 'In Progress' THEN 1 ELSE 2 END, updated_at DESC"
        cur.execute(base, params)
        return cur.fetchall()

    # ---------------- UI ---------------- #
    def build_ui(self):
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Header
        header = ttk.Frame(self.root, padding=(12, 10))
        header.grid(row=0, column=0, columnspan=2, sticky="nsew")
        title_lbl = ttk.Label(header, text="Offline To‑Do List", font=("Segoe UI", 16, "bold"))
        title_lbl.pack(side=tk.LEFT)

        # Search + Filter bar
        bar = ttk.Frame(self.root, padding=(10, 6))
        bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        bar.columnconfigure(3, weight=1)

        ttk.Label(bar, text="Status:").grid(row=0, column=0, padx=(0, 6))
        self.filter_status = ttk.Combobox(bar, values=["All"] + STATUSES, state="readonly", width=14)
        self.filter_status.set("All")
        self.filter_status.grid(row=0, column=1)
        self.filter_status.bind("<<ComboboxSelected>>", lambda e: self.refresh_tasks())

        ttk.Label(bar, text="Search:").grid(row=0, column=2, padx=(12, 6))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(bar, textvariable=self.search_var)
        search_entry.grid(row=0, column=3, sticky="ew")
        search_entry.bind("<KeyRelease>", lambda e: self.refresh_tasks())

        clear_btn = ttk.Button(bar, text="Clear", command=self.clear_search)
        clear_btn.grid(row=0, column=4, padx=(6, 0))

        # Main layout
        left = ttk.Frame(self.root, padding=10)
        right = ttk.Frame(self.root, padding=(0, 10, 10, 10))
        left.grid(row=2, column=0, sticky="nsew")
        right.grid(row=2, column=1, sticky="nsew")
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        right.rowconfigure(0, weight=1)

        # Left panel (form)
        card = ttk.LabelFrame(left, text="Task Details")
        card.pack(fill="both", expand=False)

        ttk.Label(card, text="Title:").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(card, textvariable=self.title_var, width=40)
        self.title_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=(0, 8), pady=(8, 4))

        ttk.Label(card, text="Status:").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        self.status_var = tk.StringVar(value=STATUSES[0])
        self.status_cb = ttk.Combobox(card, textvariable=self.status_var, values=STATUSES, state="readonly", width=18)
        self.status_cb.grid(row=1, column=1, sticky="w", padx=(0, 8), pady=4)

        ttk.Label(card, text="Notes:").grid(row=2, column=0, sticky="nw", padx=8, pady=(4, 8))
        self.notes_txt = ScrolledText(card, width=40, height=10, wrap=tk.WORD)
        self.notes_txt.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(0, 8), pady=(4, 8))
        card.columnconfigure(1, weight=1)
        card.rowconfigure(2, weight=1)

        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=10)
        self.add_update_btn = ttk.Button(btns, text="Add Task", command=self.add_or_update_task)
        self.add_update_btn.pack(side=tk.LEFT)
        ttk.Button(btns, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=6)

        # Right panel (list)
        list_frame = ttk.LabelFrame(right, text="Tasks")
        list_frame.grid(row=0, column=0, sticky="nsew")
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        cols = ("id", "title", "status", "created", "updated")
        self.tree = ttk.Treeview(list_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("status", text="Status")
        self.tree.heading("created", text="Created")
        self.tree.heading("updated", text="Last Updated")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=300)
        self.tree.column("status", width=110, anchor="center")
        self.tree.column("created", width=130, anchor="center")
        self.tree.column("updated", width=140, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())

        # Actions under list
        actions = ttk.Frame(right)
        actions.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        for i in range(6):
            actions.columnconfigure(i, weight=1)

        ttk.Button(actions, text="Edit", command=self.edit_selected).grid(row=0, column=0, sticky="ew", padx=3)
        ttk.Button(actions, text="Delete", command=self.delete_selected).grid(row=0, column=1, sticky="ew", padx=3)
        ttk.Button(actions, text="Mark To Do", command=lambda: self.quick_status("To Do")).grid(row=0, column=2, sticky="ew", padx=3)
        ttk.Button(actions, text="Mark In Progress", command=lambda: self.quick_status("In Progress")).grid(row=0, column=3, sticky="ew", padx=3)
        ttk.Button(actions, text="Mark Completed", command=lambda: self.quick_status("Completed")).grid(row=0, column=4, sticky="ew", padx=3)
        ttk.Button(actions, text="Export CSV", command=self.export_csv).grid(row=0, column=5, sticky="ew", padx=3)

        # Footer (count)
        self.count_var = tk.StringVar(value="0 tasks")
        ttk.Label(self.root, textvariable=self.count_var, padding=(10, 6)).grid(row=3, column=0, columnspan=2, sticky="w")

        # Style tweaks
        style = ttk.Style()
        try:
            self.root.call("source", "azure.tcl")
            style.theme_use("azure")
        except Exception:
            pass  # fall back to default theme if azure not available

    # ---------------- Helpers ---------------- #
    def clear_search(self):
        self.search_var.set("")
        self.filter_status.set("All")
        self.refresh_tasks()

    def clear_form(self):
        self.title_var.set("")
        self.status_var.set(STATUSES[0])
        self.notes_txt.delete("1.0", tk.END)
        self.tree.selection_remove(self.tree.selection())
        self.add_update_btn.configure(text="Add Task")

    def refresh_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = self.fetch_tasks(self.filter_status.get(), self.search_var.get().strip())
        for r in rows:
            self.tree.insert("", tk.END, values=(r["id"], r["title"], r["status"], r["created_at"], r["updated_at"]))
        self.count_var.set(f"{len(rows)} task(s)")

    def add_or_update_task(self):
        title = self.title_var.get().strip()
        if not title:
            messagebox.showwarning("Missing title", "Please enter a task title.")
            return
        status = self.status_var.get()
        notes = self.notes_txt.get("1.0", tk.END).strip()
        sel = self.tree.selection()
        if sel:
            task_id = self.tree.item(sel[0], "values")[0]
            self.update_task(task_id, title=title, status=status, notes=notes)
            messagebox.showinfo("Updated", "Task updated successfully.")
        else:
            self.create_task(title, status, notes)
            messagebox.showinfo("Added", "Task added successfully.")
        self.refresh_tasks()
        self.clear_form()

    def on_tree_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        task_id = vals[0]
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        r = cur.fetchone()
        if r:
            self.title_var.set(r["title"])
            self.status_var.set(r["status"])
            self.notes_txt.delete("1.0", tk.END)
            self.notes_txt.insert(tk.END, r["notes"])
            self.add_update_btn.configure(text="Update Task")

    def edit_selected(self):
        # Same as selecting; focus form for editing
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to edit.")
            return
        self.on_tree_select()
        self.title_entry.focus_set()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task to delete.")
            return
        vals = self.tree.item(sel[0], "values")
        task_id, title = vals[0], vals[1]
        if messagebox.askyesno("Delete", f"Delete task: {title}? This cannot be undone."):
            self.delete_task(task_id)
            self.refresh_tasks()
            self.clear_form()

    def quick_status(self, status):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("No selection", "Please select a task first.")
            return
        task_id = self.tree.item(sel[0], "values")[0]
        self.update_task(task_id, status=status)
        self.refresh_tasks()

    def export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="tasks_export.csv",
            title="Export tasks to CSV",
        )
        if not path:
            return
        rows = self.fetch_tasks(self.filter_status.get(), self.search_var.get().strip())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Status", "Notes", "Created", "Updated"])
            for r in rows:
                writer.writerow([r["id"], r["title"], r["status"], r["notes"], r["created_at"], r["updated_at"]])
        messagebox.showinfo("Exported", f"Exported {len(rows)} task(s) to\n{path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
