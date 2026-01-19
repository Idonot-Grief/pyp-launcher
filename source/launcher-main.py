import os
import zipfile
import hashlib
import tempfile
import shutil
import sys
import runpy

PAGE_SIZE = 25

def md5_of_file(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def extract_pyp(pyp_path, temp_dir):
    with zipfile.ZipFile(pyp_path, 'r') as z:
        z.extractall(temp_dir)

def install_wheels_into_sys_path(modules_path, site_packages_path):
    for fname in os.listdir(modules_path):
        if fname.endswith('.whl'):
            full_path = os.path.join(modules_path, fname)
            print(f"[+] Installing: {fname}")
            with zipfile.ZipFile(full_path, 'r') as z:
                z.extractall(site_packages_path)

    if site_packages_path not in sys.path:
        sys.path.insert(0, site_packages_path)

def copy_side_files(extracted_path, target_appdata_path):
    for item in os.listdir(extracted_path):
        if item not in ("modules", "script.py"):
            src = os.path.join(extracted_path, item)
            dest = os.path.join(target_appdata_path, item)
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dest)
            except Exception as e:
                print(f"[!] Failed to copy {item}: {e}")

def console_file_browser(start_dir):
    current_dir = os.path.abspath(start_dir)
    page = 0

    while True:
        try:
            entries = sorted(os.listdir(current_dir))
        except PermissionError:
            print("[!] Permission denied.")
            current_dir = os.path.dirname(current_dir)
            continue

        total_pages = max(1, (len(entries) + PAGE_SIZE - 1) // PAGE_SIZE)
        start_idx = page * PAGE_SIZE
        end_idx = start_idx + PAGE_SIZE
        shown_entries = entries[start_idx:end_idx]

        print(f"\n📁 {current_dir}")
        print(f"📄 Page {page + 1} / {total_pages}")
        for i, entry in enumerate(shown_entries, start=start_idx):
            full = os.path.join(current_dir, entry)
            typ = "[DIR]" if os.path.isdir(full) else "     "
            print(f"{i:4}: {typ} {entry}")

        print("\nCommands: [number], n=next, p=prev, ..=up, q=quit")
        choice = input("Choose: ").strip().lower()

        if choice == "q":
            return None
        elif choice == "n" and page < total_pages - 1:
            page += 1
        elif choice == "p" and page > 0:
            page -= 1
        elif choice == "..":
            parent = os.path.dirname(current_dir)
            if parent != current_dir:
                current_dir = parent
                page = 0
        elif choice.isdigit():
            index = int(choice)
            if 0 <= index < len(entries):
                selected = os.path.join(current_dir, entries[index])
                if os.path.isdir(selected):
                    current_dir = selected
                    page = 0
                elif selected.endswith(".pyp"):
                    return selected
                else:
                    print("❌ Not a .pyp file.")
            else:
                print("❌ Invalid index.")
        else:
            print("❌ Invalid input.")

def safe_rmtree(path):
    # Remove all files and directories without deep recursion to avoid max recursion errors
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            try:
                os.unlink(os.path.join(root, name))
            except Exception:
                pass
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                if os.path.islink(dir_path):
                    os.unlink(dir_path)  # unlink symlink, don't recurse into
                else:
                    os.rmdir(dir_path)
            except Exception:
                pass
    try:
        os.rmdir(path)
    except Exception:
        pass

def main():
    print("📦 Select a .pyp file:")
    pyp_file = console_file_browser(os.getcwd())
    if not pyp_file:
        print("❌ No file selected.")
        return

    temp_dir = tempfile.mkdtemp()
    try:
        extract_pyp(pyp_file, temp_dir)

        script_path = os.path.join(temp_dir, "script.py")
        if not os.path.exists(script_path):
            print("❌ ERROR: script.py not found in root of .pyp file.")
            return

        script_md5 = md5_of_file(script_path)
        appdata_path = os.path.join(os.getenv("APPDATA", "/tmp/pypdata"), script_md5)
        os.makedirs(appdata_path, exist_ok=True)
        copy_side_files(temp_dir, appdata_path)

        modules_path = os.path.join(temp_dir, "modules")
        site_packages_path = os.path.join(temp_dir, "site-packages")
        os.makedirs(site_packages_path, exist_ok=True)

        if os.path.exists(modules_path):
            install_wheels_into_sys_path(modules_path, site_packages_path)

        os.chdir(temp_dir)
        sys.argv = [script_path]  # simulate script argv[0]
        print(f"\n▶ Running {script_path}...\n")
        try:
            runpy.run_path(script_path, run_name="__main__")
        except Exception as e:
            print(f"\n❌ Error while running script.py: {e}")
    finally:
        safe_rmtree(temp_dir)

if __name__ == "__main__":
    main()
