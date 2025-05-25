# 🔐 SQLCipherConverter

Convert Normal SQLite db to SQLCipher Encrypted Database ( Selected Tables only ) 

A simple cross-platform Python GUI tool to:

- Open an existing **SQLite database**
- Select specific **tables/views**
- Export them into a new, **SQLCipher-encrypted SQLite database**

---

## 📦 Features

- ✅ Open `.db`, `.sqlite`, or `.sqlite3` files
- ✅ List all tables and views
- ✅ Select multiple items for export
- ✅ Set a custom encryption password
- ✅ Save as a new encrypted SQLite database using SQLCipher

---

## 🧰 Requirements

Before running the app, ensure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- `tkinter` (comes with standard Python installations)
- `pysqlcipher3` – for SQLCipher support

Install dependencies via pip:

```bash
pip install pysqlcipher3
```

> ⚠️ On Windows: You may need to install **Microsoft Visual C++ Build Tools** first.  
> See: [Visual Studio C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
> 
> If you are unable to compile pysqlcipher3 yourself, download from https://pypi.org/project/sqlcipher3-wheels/#files
---

## ▶️ How to Run

1. Clone or download the project:
   ```bash
   git clone https://github.com/yourusername/sqlciphercoverter.git
   cd sqlciphercoverter
   ```

2. Run the app:
   ```bash
   python sqlciphercoverter.py
   ```

---

## 🖥️ Usage Guide

1. Click **"Open DB"** to load an SQLite file.
2. From the list, select one or more tables/views to export.
3. Click **"Export to Encrypted DB"**, enter a password.
4. Choose a location to save the new encrypted database.

---

## 📁 Project Structure

```
sqlite-encryptor-gui/
│
├── sqlciphercoverter.py       # Main application script
└── README.md                  # This file
```

---

## 💬 Notes

- The app copies both schema and data from selected **tables**.
- **Views** are copied by schema only — no data is inserted.
- Works best with smaller databases due to in-memory operations.
- For large databases or production use, consider optimizing performance and adding progress indicators.

---

## 📎 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributing

Contributions are welcome! If you'd like to improve the app (e.g., add batch processing, dark mode, or export logs), feel free to open a pull request.
