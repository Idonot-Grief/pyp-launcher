# 🐍📦 PyP – Making Python Simpler

**PyP** is a portable, modular format for packaging and launching Python programs without requiring Python to be installed.

Forget about `pip`, virtual environments, and broken dependencies. With PyP, everything your program needs—scripts, modules, wheels, and assets—is bundled in one compact `.pyp` file, ready to run anywhere.

> 💡 “It’s not just easy for users, but developers too. Equality is the key.” –DevFlix

---

## 🌟 Features

- **🛠 Developer Friendly** – Build apps with just `script.py` and your `.whl` files. No CLI. No terminal.
- **👤 User Friendly** – Use the launcher and navigate to the file and select it. That’s it.
- **📦 Self-Contained** – All dependencies included inside the `.pyp`. No Python install needed.
- **🚀 Native-like Execution** – PyP programs launch just like standalone Python apps.
- **🔌 Modular Structure** – Organize assets and libraries cleanly, making dev work efficient and portable.
- **📴 Fully Offline** – Works 100% without internet. Perfect for air-gapped or legacy systems.

---

## 📁 .pyp Structure

A `.pyp` file is simply a `.zip` archive with this structure:

```
your-app.pyp
│
├── script.py            # 🔰 Main entrypoint of your app
├── config.json          # 📄 Any file in root is extracted alongside script.py
├── index.html           # 🌐 Assets like HTML/TXT/etc are placed here
│
└── modules/             # 📦 Contains .whl files for external libraries
    ├── numpy-1.26.4.whl
    └── flask-2.3.3.whl
```

---

## 🧃 Getting Started

1. Use the provided **PyP project template folder**.
2. Drop your `script.py` and assets in the root.
3. Put your `.whl` dependencies inside `modules/`.
4. Run the **PyP Builder** (no terminal needed) to generate your `.pyp` file.
5. Double-click to launch with the **PyP Launcher**. Enjoy.

---

## 🔧 PyP Launcher

The `PyPLauncher.exe` runs `.pyp` files by:
- Extracting files to a temp directory.
- Installing/loading `.whl` files from `modules/` in a virtual runtime.
- Running `script.py` as the main app.

It requires no external Python and works on Windows 8.1 through Windows 11. (Can go older if the PY source is run on an existing os matching Python install.)
---

## 📦 Build Tools

Coming soon:
- 🖱 GUI-based `.pyp` packager
- 🗂 Explorer integration: Right-click → “Build PyP Package”
- 🧊 Option to freeze into single `.exe`

---

## 🔒 Why PyP?

You control your runtime.  
You don’t rely on system Python.  
Your app **just works**.

---

## ❤️ Credits

Made with care by DevFlix.  
Icon drawn entirely in Scratch's bitmap editor 😎 (somehow)

> “PyP is how Python *should* feel: portable, plug-and-play, peaceful.”

---

## 🐍 License

MIT. You own your apps. PyP just helps them breathe. (View the license file for more info.)
