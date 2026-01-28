#!/usr/bin/env python3
"""
Knight Online Demo - Standalone Installer v1.0
Downloads and installs the game from GitHub Releases.
Can be distributed as a single executable.
"""

import os
import sys
import json
import threading
import subprocess
import zipfile
import ssl
import ctypes
from pathlib import Path
from datetime import datetime

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    import urllib.request
    import urllib.error
except ImportError:
    print("Error: Required modules not found")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

CONFIG = {
    "name": "Knight Online Demo",
    "version": "1.0.0",
    "github_repo": "rubarx/KnightOnline-Demo",
    "github_api": "https://api.github.com/repos/rubarx/KnightOnline-Demo/releases/latest",
    "game_exe": "KnightOnLine.exe",
    "launcher_exe": "KO-Demo-Launcher.exe",
    "default_install_path": "C:\\Games\\KnightOnline-Demo",
}

# Colors - Dark theme
class C:
    BG = "#0d1117"
    BG2 = "#161b22"
    BG3 = "#21262d"
    GOLD = "#f0b429"
    RED = "#f85149"
    BLUE = "#58a6ff"
    GREEN = "#3fb950"
    ORANGE = "#d29922"
    TEXT = "#c9d1d9"
    DIM = "#8b949e"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_ssl_context():
    ctx = ssl.create_default_context()
    return ctx

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def create_shortcut(target_path, shortcut_path, description="", icon_path=None):
    """Create a Windows shortcut (.lnk file)"""
    try:
        import winreg
        # Use PowerShell to create shortcut (works without extra dependencies)
        ps_script = f'''
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "{target_path}"
$Shortcut.WorkingDirectory = "{os.path.dirname(target_path)}"
$Shortcut.Description = "{description}"
$Shortcut.Save()
'''
        subprocess.run(["powershell", "-Command", ps_script],
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        return True
    except:
        return False

# ============================================================================
# GITHUB API
# ============================================================================

class GitHubAPI:
    @staticmethod
    def get_latest_release():
        """Fetch latest release info from GitHub"""
        try:
            ctx = get_ssl_context()
            req = urllib.request.Request(
                CONFIG["github_api"],
                headers={
                    "User-Agent": f"KODemo-Installer/{CONFIG['version']}",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            print(f"GitHub API error: {e}")
            return None

    @staticmethod
    def parse_release(release_data):
        """Parse release data into usable format"""
        if not release_data:
            return None

        zip_asset = None
        for asset in release_data.get("assets", []):
            if asset["name"].endswith(".zip"):
                zip_asset = asset
                break

        if not zip_asset:
            return None

        return {
            "tag": release_data.get("tag_name", "v1.0.0"),
            "version": release_data.get("tag_name", "v1.0.0").lstrip("v"),
            "name": release_data.get("name", "Release"),
            "body": release_data.get("body", ""),
            "published_at": release_data.get("published_at", ""),
            "download_url": zip_asset["browser_download_url"],
            "size_bytes": zip_asset["size"],
            "size_mb": round(zip_asset["size"] / (1024 * 1024), 1),
            "filename": zip_asset["name"]
        }

# ============================================================================
# INSTALLER
# ============================================================================

class Installer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{CONFIG['name']} - Installer")
        self.root.geometry("600x450")
        self.root.minsize(550, 400)
        self.root.configure(bg=C.BG)
        self.root.resizable(True, True)

        # State
        self.installing = False
        self.install_path = Path(CONFIG["default_install_path"])
        self.release_info = None
        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        self.create_start_menu = tk.BooleanVar(value=True)
        self.launch_after_install = tk.BooleanVar(value=True)

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 600) // 2
        y = (self.root.winfo_screenheight() - 450) // 2
        self.root.geometry(f"600x450+{x}+{y}")

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Gold.Horizontal.TProgressbar",
                       background=C.GOLD, troughcolor=C.BG3)

        # Build UI
        self.build_ui()

        # Fetch release info
        self.root.after(100, self.fetch_release_info)

    def build_ui(self):
        # === HEADER ===
        header = tk.Frame(self.root, bg=C.BG2, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=C.BG2)
        title_frame.pack(pady=20)

        tk.Label(title_frame, text="KNIGHT ONLINE",
                font=("Arial", 22, "bold"), fg=C.GOLD, bg=C.BG2).pack(side="left")
        tk.Label(title_frame, text=" DEMO",
                font=("Arial", 22, "bold"), fg=C.GREEN, bg=C.BG2).pack(side="left")

        tk.Label(header, text="Installer",
                font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack()

        # === MAIN CONTENT ===
        main = tk.Frame(self.root, bg=C.BG)
        main.pack(fill="both", expand=True, padx=30, pady=20)

        # Release info
        info_frame = tk.Frame(main, bg=C.BG2)
        info_frame.pack(fill="x", pady=(0, 15))

        tk.Label(info_frame, text="RELEASE INFO",
                font=("Arial", 10, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(12, 5))

        self.info_label = tk.Label(info_frame, text="Fetching from GitHub...",
                                  font=("Arial", 10), fg=C.TEXT, bg=C.BG2, justify="left")
        self.info_label.pack(anchor="w", padx=15, pady=(0, 12))

        # Install path
        path_frame = tk.Frame(main, bg=C.BG2)
        path_frame.pack(fill="x", pady=(0, 15))

        tk.Label(path_frame, text="INSTALL LOCATION",
                font=("Arial", 10, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(12, 5))

        path_row = tk.Frame(path_frame, bg=C.BG2)
        path_row.pack(fill="x", padx=15, pady=(0, 12))

        self.path_entry = tk.Entry(path_row, font=("Arial", 10), bg=C.BG3, fg=C.TEXT,
                                  insertbackground=C.TEXT, relief="flat", width=45)
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.path_entry.insert(0, str(self.install_path))

        tk.Button(path_row, text="Browse", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=10,
                 command=self.browse_path).pack(side="right", padx=(10, 0))

        # Options
        options_frame = tk.Frame(main, bg=C.BG2)
        options_frame.pack(fill="x", pady=(0, 15))

        tk.Label(options_frame, text="OPTIONS",
                font=("Arial", 10, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(12, 5))

        opts = tk.Frame(options_frame, bg=C.BG2)
        opts.pack(anchor="w", padx=15, pady=(0, 12))

        tk.Checkbutton(opts, text="Create Desktop shortcut",
                      variable=self.create_desktop_shortcut,
                      font=("Arial", 10), fg=C.TEXT, bg=C.BG2,
                      selectcolor=C.BG3, activebackground=C.BG2,
                      activeforeground=C.TEXT).pack(anchor="w")

        tk.Checkbutton(opts, text="Create Start Menu entry",
                      variable=self.create_start_menu,
                      font=("Arial", 10), fg=C.TEXT, bg=C.BG2,
                      selectcolor=C.BG3, activebackground=C.BG2,
                      activeforeground=C.TEXT).pack(anchor="w")

        tk.Checkbutton(opts, text="Launch game after installation",
                      variable=self.launch_after_install,
                      font=("Arial", 10), fg=C.TEXT, bg=C.BG2,
                      selectcolor=C.BG3, activebackground=C.BG2,
                      activeforeground=C.TEXT).pack(anchor="w")

        # Progress (hidden initially)
        self.progress_frame = tk.Frame(main, bg=C.BG2)

        self.progress_text = tk.Label(self.progress_frame, text="",
                                     font=("Arial", 10), fg=C.TEXT, bg=C.BG2)
        self.progress_text.pack(anchor="w", padx=15, pady=(12, 8))

        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                           style="Gold.Horizontal.TProgressbar",
                                           length=400, mode='determinate')
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 12))

        # === FOOTER ===
        footer = tk.Frame(self.root, bg=C.BG2, height=70)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        # Buttons
        btn_frame = tk.Frame(footer, bg=C.BG2)
        btn_frame.pack(pady=18)

        tk.Button(btn_frame, text="Cancel", font=("Arial", 11),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=25, pady=5,
                 command=self.root.quit).pack(side="left", padx=10)

        self.install_btn = tk.Button(btn_frame, text="INSTALL",
                                    font=("Arial", 11, "bold"),
                                    fg=C.BG, bg=C.GOLD,
                                    activeforeground=C.BG, activebackground="#f5c542",
                                    relief="flat", padx=35, pady=5,
                                    command=self.start_install)
        self.install_btn.pack(side="left", padx=10)

    def browse_path(self):
        path = filedialog.askdirectory(initialdir=str(self.install_path))
        if path:
            self.install_path = Path(path)
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, str(self.install_path))

    def fetch_release_info(self):
        def fetch():
            release_data = GitHubAPI.get_latest_release()
            release = GitHubAPI.parse_release(release_data)
            if release:
                self.root.after(0, lambda: self.update_release_info(release))
            else:
                self.root.after(0, self.show_fetch_error)

        threading.Thread(target=fetch, daemon=True).start()

    def update_release_info(self, release):
        self.release_info = release
        info_text = f"Version: {release['version']}\n"
        info_text += f"Size: {release['size_mb']} MB\n"
        info_text += f"File: {release['filename']}"
        self.info_label.config(text=info_text, fg=C.GREEN)

    def show_fetch_error(self):
        self.info_label.config(text="Could not connect to GitHub.\nCheck your internet connection.", fg=C.RED)
        self.install_btn.config(state="disabled")

    def start_install(self):
        if not self.release_info:
            messagebox.showerror("Error", "Release information not available.")
            return

        # Update install path from entry
        self.install_path = Path(self.path_entry.get())

        # Confirm
        size = self.release_info["size_mb"]
        result = messagebox.askyesno(
            "Confirm Installation",
            f"Install Knight Online Demo?\n\n"
            f"Version: {self.release_info['version']}\n"
            f"Size: {size} MB\n"
            f"Location: {self.install_path}\n\n"
            "Continue?"
        )
        if not result:
            return

        self.installing = True
        self.install_btn.config(text="Installing...", state="disabled")
        self.progress_frame.pack(fill="x", pady=(0, 15))
        self.progress_text.config(text="Starting download...")
        self.progress_bar["value"] = 0

        threading.Thread(target=self.do_install, daemon=True).start()

    def do_install(self):
        try:
            # Create install directory
            self.update_status("Creating directories...")
            self.install_path.mkdir(parents=True, exist_ok=True)

            # Download
            self.update_status("Downloading from GitHub...")
            url = self.release_info["download_url"]
            zip_path = self.install_path / "download.zip"
            total = self.release_info["size_bytes"]

            ctx = get_ssl_context()
            req = urllib.request.Request(url, headers={
                "User-Agent": f"KODemo-Installer/{CONFIG['version']}"
            })

            response = urllib.request.urlopen(req, timeout=300, context=ctx)
            downloaded = 0
            block_size = 1024 * 256

            with open(zip_path, 'wb') as f:
                while True:
                    block = response.read(block_size)
                    if not block:
                        break
                    f.write(block)
                    downloaded += len(block)
                    pct = min(100, (downloaded / total) * 100)
                    mb = downloaded / (1024 * 1024)
                    total_mb = total / (1024 * 1024)
                    self.root.after(0, lambda p=pct, m=mb, t=total_mb:
                                   self.update_progress(p, f"Downloading: {m:.1f} / {t:.1f} MB ({p:.0f}%)"))

            response.close()

            # Extract
            self.update_status("Extracting files...")
            self.root.after(0, lambda: self.progress_bar.configure(mode='indeterminate'))
            self.root.after(0, lambda: self.progress_bar.start(10))

            with zipfile.ZipFile(zip_path, 'r') as zf:
                names = zf.namelist()

                # Check for root folder in zip
                root_folder = None
                if names and '/' in names[0]:
                    potential_root = names[0].split('/')[0]
                    if all(n.startswith(potential_root + '/') or n == potential_root + '/' for n in names):
                        root_folder = potential_root

                zf.extractall(self.install_path)

                # Move files from subfolder if needed
                if root_folder:
                    import shutil
                    subfolder = self.install_path / root_folder
                    if subfolder.exists() and subfolder.is_dir():
                        for item in subfolder.iterdir():
                            dest = self.install_path / item.name
                            if dest.exists():
                                if dest.is_file():
                                    dest.unlink()
                                elif dest.is_dir():
                                    shutil.rmtree(dest)
                            shutil.move(str(item), str(dest))
                        try:
                            subfolder.rmdir()
                        except:
                            pass

            # Clean up zip
            zip_path.unlink()

            # Save version info
            version_file = self.install_path / "version.json"
            with open(version_file, "w") as f:
                json.dump({
                    "version": self.release_info["version"],
                    "tag": self.release_info["tag"],
                    "installed_at": datetime.now().isoformat()
                }, f, indent=2)

            # Create shortcuts
            self.update_status("Creating shortcuts...")
            launcher_path = self.install_path / CONFIG["launcher_exe"]

            if not launcher_path.exists():
                # Fallback to game exe if launcher not in package
                launcher_path = self.install_path / CONFIG["game_exe"]

            if self.create_desktop_shortcut.get():
                desktop = Path(os.path.expanduser("~")) / "Desktop"
                shortcut = desktop / "Knight Online Demo.lnk"
                create_shortcut(str(launcher_path), str(shortcut), "Knight Online Demo")

            if self.create_start_menu.get():
                start_menu = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Start Menu" / "Programs"
                if start_menu.exists():
                    shortcut = start_menu / "Knight Online Demo.lnk"
                    create_shortcut(str(launcher_path), str(shortcut), "Knight Online Demo")

            self.root.after(0, self.install_complete)

        except Exception as e:
            self.root.after(0, lambda: self.install_error(str(e)))

    def update_status(self, text):
        self.root.after(0, lambda: self.progress_text.config(text=text))

    def update_progress(self, pct, text):
        self.progress_bar["value"] = pct
        self.progress_text.config(text=text)

    def install_complete(self):
        self.installing = False
        self.progress_bar.stop()
        self.progress_bar.configure(mode='determinate')
        self.progress_bar["value"] = 100
        self.progress_text.config(text="Installation complete!", fg=C.GREEN)
        self.install_btn.config(text="DONE", state="normal", command=self.root.quit)

        messagebox.showinfo("Success",
                           f"Knight Online Demo installed successfully!\n\n"
                           f"Location: {self.install_path}")

        # Launch if requested
        if self.launch_after_install.get():
            launcher = self.install_path / CONFIG["launcher_exe"]
            if not launcher.exists():
                launcher = self.install_path / CONFIG["game_exe"]

            if launcher.exists():
                try:
                    os.chdir(str(self.install_path))
                    subprocess.Popen([str(launcher)])
                except:
                    pass

            self.root.quit()

    def install_error(self, error):
        self.installing = False
        self.progress_bar.stop()
        self.progress_bar.configure(mode='determinate')
        self.progress_text.config(text="Installation failed!", fg=C.RED)
        self.install_btn.config(text="RETRY", state="normal", command=self.start_install)
        messagebox.showerror("Error", f"Installation failed:\n\n{error}")

    def run(self):
        self.root.mainloop()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    app = Installer()
    app.run()
