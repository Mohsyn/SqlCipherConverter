import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, MULTIPLE
import sqlite3
from sqlcipher3 import dbapi2 as sqlcipher


class SQLiteEncryptorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite Encryptor")

        # Variables
        self.source_db_path = None
        self.conn = None
        self.tables = []

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Select SQLite DB File:").pack(pady=5)
        tk.Button(self.root, text="Open DB", command=self.open_db).pack(pady=5)

        self.table_listbox_frame = tk.Frame(self.root)
        self.table_listbox_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(self.table_listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.table_listbox = Listbox(self.table_listbox_frame, selectmode=MULTIPLE, yscrollcommand=self.scrollbar.set)
        self.table_listbox.pack(fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.table_listbox.yview)

        tk.Button(self.root, text="Export to Encrypted DB", command=self.export_to_encrypted).pack(pady=10)

    def open_db(self):
        file_path = filedialog.askopenfilename(filetypes=[("SQLite DB Files", "*.db *.sqlite *.sqlite3")])
        if not file_path:
            return

        try:
            self.conn = sqlite3.connect(file_path)
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view');")
            self.tables = [row[0] for row in cursor.fetchall()]
            self.source_db_path = file_path

            self.table_listbox.delete(0, tk.END)
            for table in self.tables:
                self.table_listbox.insert(tk.END, table)

            cursor.close()
            messagebox.showinfo("Success", "Database opened successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open database:\n{e}")

    def export_to_encrypted(self):
        selected_indices = self.table_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select at least one table/view.")
            return

        selected_tables = [self.tables[i] for i in selected_indices]
        password = self.ask_password()
        if not password:
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite DB Files", "*.db")])
        if not save_path:
            return

        try:
            # Create encrypted DB
            enc_conn = sqlcipher.connect(save_path)
            enc_conn.execute(f"PRAGMA key = '{password}';")
            enc_conn.execute("PRAGMA cipher_version;")  # Just to test connection

            # Copy schema and data
            cursor = self.conn.cursor()
            for table in selected_tables:
                # Get schema
                cursor.execute(f"SELECT sql FROM sqlite_master WHERE name='{table}' AND type IN ('table','view');")
                schema = cursor.fetchone()[0]
                enc_conn.execute(schema)

                # If it's a table, copy data
                if "CREATE TABLE" in schema:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    col_count = len(cursor.description)
                    placeholders = ",".join("?" * col_count)
                    enc_conn.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)

            enc_conn.commit()
            enc_conn.close()
            messagebox.showinfo("Success", "Encrypted database created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export:\n{e}")

    def ask_password(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Set Password")
        dialog.geometry("300x100")
        dialog.grab_set()

        tk.Label(dialog, text="Enter encryption password:").pack(pady=5)
        password_entry = tk.Entry(dialog, show="*")
        password_entry.pack(pady=5)

        result = {"value": None}

        def submit():
            result["value"] = password_entry.get()
            dialog.destroy()

        tk.Button(dialog, text="OK", command=submit).pack()
        self.root.wait_window(dialog)
        return result["value"]


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLiteEncryptorApp(root)
    root.mainloop()