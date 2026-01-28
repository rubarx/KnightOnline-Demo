#!/usr/bin/env python3
"""
Knight Online Demo - Auto-Update Launcher v1.0
- Automatic update from GitHub Releases
- Version checking on startup
- Professional UI
"""

import os
import sys
import json
import threading
import subprocess
import zipfile
import ssl
import hashlib
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
    "server_ip": "127.0.0.1",  # Default local, can be changed
    "server_port": 15100,
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
# SSL CONTEXT
# ============================================================================

def get_ssl_context():
    ctx = ssl.create_default_context()
    return ctx

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
                    "User-Agent": f"KODemo-Launcher/{CONFIG['version']}",
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

        # Find the ZIP asset
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
# LAUNCHER
# ============================================================================

class Launcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(CONFIG["name"])
        self.root.geometry("750x500")
        self.root.minsize(650, 450)
        self.root.configure(bg=C.BG)
        self.root.resizable(True, True)

        # State
        self.downloading = False
        self.install_path = self.get_install_path()
        self.local_version = None
        self.remote_release = None
        self.update_available = False

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 750) // 2
        y = (self.root.winfo_screenheight() - 500) // 2
        self.root.geometry(f"750x500+{x}+{y}")

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Gold.Horizontal.TProgressbar",
                       background=C.GOLD, troughcolor=C.BG3)

        # Build UI
        self.build_ui()

        # Check game and updates
        self.root.after(100, self.check_game)
        self.root.after(300, self.check_for_updates)

    def get_install_path(self):
        current = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
        # Check if we're in launcher/src, go up to main folder
        if current.name == "src" and current.parent.name == "launcher":
            return current.parent.parent
        if (current / CONFIG["game_exe"]).exists():
            return current
        if (current / "Data").exists():
            return current
        return current

    def get_local_version(self):
        """Read local version file"""
        version_file = self.install_path / "version.json"
        if version_file.exists():
            try:
                with open(version_file, "r") as f:
                    return json.load(f)
            except:
                pass
        return None

    def save_local_version(self, version_data):
        """Save local version file"""
        version_file = self.install_path / "version.json"
        try:
            with open(version_file, "w") as f:
                json.dump(version_data, f, indent=2)
        except:
            pass

    def build_ui(self):
        # === HEADER ===
        header = tk.Frame(self.root, bg=C.BG2, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Title with icon placeholder
        title_frame = tk.Frame(header, bg=C.BG2)
        title_frame.pack(side="left", padx=20, pady=12)

        tk.Label(title_frame, text="KNIGHT ONLINE",
                font=("Arial", 20, "bold"), fg=C.GOLD, bg=C.BG2).pack(side="left")
        tk.Label(title_frame, text=" DEMO",
                font=("Arial", 20, "bold"), fg=C.GREEN, bg=C.BG2).pack(side="left")

        self.status_label = tk.Label(header, text="Checking...",
                                    font=("Arial", 9), fg=C.DIM, bg=C.BG2)
        self.status_label.pack(side="right", padx=20)

        # === MAIN CONTENT ===
        main = tk.Frame(self.root, bg=C.BG)
        main.pack(fill="both", expand=True, padx=20, pady=15)

        # Left panel
        left = tk.Frame(main, bg=C.BG)
        left.pack(side="left", fill="both", expand=True)

        # Hero section
        hero = tk.Frame(left, bg=C.BG2, relief="flat")
        hero.pack(fill="x", pady=(0, 12))

        tk.Label(hero, text="Custom Features Demo",
                font=("Arial", 14, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(15, 5))

        features_text = """Town Button (G) - Quick teleport to town
Auto-Pot (Insert) - Automatic HP/MP potion usage
Skill Macros (Numpad 1-6) - Pre-configured combos
Extended Hotkeys (1-0) - 10 skill slots"""

        tk.Label(hero, text=features_text, font=("Arial", 10),
                fg=C.TEXT, bg=C.BG2, justify="left").pack(anchor="w", padx=15, pady=(0, 15))

        # Status section
        status_frame = tk.Frame(left, bg=C.BG2)
        status_frame.pack(fill="x", pady=(0, 12))

        tk.Label(status_frame, text="STATUS",
                font=("Arial", 10, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(12, 8))

        # Client status row
        row1 = tk.Frame(status_frame, bg=C.BG2)
        row1.pack(fill="x", padx=15, pady=2)
        tk.Label(row1, text="Client:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        self.client_status = tk.Label(row1, text="Checking...",
                                     font=("Arial", 10, "bold"), fg=C.DIM, bg=C.BG2)
        self.client_status.pack(side="right")

        # Version row
        row2 = tk.Frame(status_frame, bg=C.BG2)
        row2.pack(fill="x", padx=15, pady=2)
        tk.Label(row2, text="Version:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        self.version_status = tk.Label(row2, text="...",
                                      font=("Arial", 10, "bold"), fg=C.DIM, bg=C.BG2)
        self.version_status.pack(side="right")

        # Latest release row
        row3 = tk.Frame(status_frame, bg=C.BG2)
        row3.pack(fill="x", padx=15, pady=(2, 12))
        tk.Label(row3, text="Latest:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        self.latest_status = tk.Label(row3, text="Checking GitHub...",
                                     font=("Arial", 10), fg=C.DIM, bg=C.BG2)
        self.latest_status.pack(side="right")

        # Update notification (hidden initially)
        self.update_frame = tk.Frame(left, bg=C.ORANGE)

        self.update_label = tk.Label(self.update_frame, text="",
                                    font=("Arial", 10, "bold"), fg=C.BG, bg=C.ORANGE)
        self.update_label.pack(side="left", padx=12, pady=10)

        self.update_btn = tk.Button(self.update_frame, text="UPDATE NOW",
                                   font=("Arial", 9, "bold"), fg=C.ORANGE, bg=C.BG,
                                   relief="flat", padx=12, command=self.apply_update)
        self.update_btn.pack(side="right", padx=12, pady=6)

        # Progress (hidden initially)
        self.progress_frame = tk.Frame(left, bg=C.BG2)

        self.progress_text = tk.Label(self.progress_frame, text="",
                                     font=("Arial", 9), fg=C.TEXT, bg=C.BG2)
        self.progress_text.pack(anchor="w", padx=15, pady=(12, 6))

        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                           style="Gold.Horizontal.TProgressbar",
                                           length=300, mode='determinate')
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 12))

        # Right panel - Release Notes
        right = tk.Frame(main, bg=C.BG2, width=230)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        tk.Label(right, text="RELEASE NOTES",
                font=("Arial", 10, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=12, pady=(12, 8))

        self.notes_label = tk.Label(right, text="Loading...", font=("Arial", 9),
                                   fg=C.TEXT, bg=C.BG2, justify="left", wraplength=200)
        self.notes_label.pack(anchor="w", padx=12, pady=5)

        # === FOOTER ===
        footer = tk.Frame(self.root, bg=C.BG2, height=75)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        # Buttons left
        btns = tk.Frame(footer, bg=C.BG2)
        btns.pack(side="left", padx=20, pady=18)

        tk.Button(btns, text="GitHub", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=10,
                 command=self.open_github).pack(side="left", padx=(0, 6))
        tk.Button(btns, text="Settings", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=10,
                 command=self.open_settings).pack(side="left", padx=(0, 6))
        tk.Button(btns, text="Reinstall", font=("Arial", 9),
                 fg=C.TEXT, bg=C.RED, relief="flat", padx=10,
                 command=self.force_reinstall).pack(side="left")

        # Play button
        self.play_btn = tk.Button(footer, text="PLAY",
                                 font=("Arial", 14, "bold"),
                                 fg=C.BG, bg=C.GOLD,
                                 activeforeground=C.BG, activebackground="#f5c542",
                                 relief="flat", width=14, height=2,
                                 command=self.on_play)
        self.play_btn.pack(side="right", padx=20, pady=12)

    def check_game(self):
        game_exe = self.install_path / CONFIG["game_exe"]
        if game_exe.exists():
            self.client_status.config(text="Installed", fg=C.GREEN)
            self.play_btn.config(text="PLAY")

            # Get local version
            self.local_version = self.get_local_version()
            if self.local_version and "version" in self.local_version:
                ver = self.local_version.get("version", "?")
                self.version_status.config(text=f"v{ver}", fg=C.GREEN)
            else:
                self.version_status.config(text="v1.0.0", fg=C.GREEN)
        else:
            self.client_status.config(text="Not Installed", fg=C.RED)
            self.version_status.config(text="-", fg=C.DIM)
            self.play_btn.config(text="INSTALL")

    def check_for_updates(self):
        """Check for updates from GitHub Releases"""
        def fetch():
            release_data = GitHubAPI.get_latest_release()
            release = GitHubAPI.parse_release(release_data)

            if release:
                self.root.after(0, lambda: self.process_release_info(release))
            else:
                self.root.after(0, lambda: self.update_notes_error())

        threading.Thread(target=fetch, daemon=True).start()

    def process_release_info(self, release):
        """Process release info from GitHub"""
        self.remote_release = release
        self.status_label.config(text="Connected to GitHub", fg=C.GREEN)

        # Update latest version display
        self.latest_status.config(text=f"v{release['version']} ({release['size_mb']}MB)", fg=C.BLUE)

        # Update release notes
        notes = f"Version: {release['version']}\n"
        notes += f"Size: {release['size_mb']} MB\n\n"

        # Parse body (first 300 chars)
        body = release.get("body", "").strip()
        if body:
            # Clean markdown
            body = body.replace("##", "").replace("**", "").replace("*", "")
            if len(body) > 280:
                body = body[:280] + "..."
            notes += body
        else:
            notes += "Custom features demo release."

        self.notes_label.config(text=notes)

        # Check if update needed
        game_exe = self.install_path / CONFIG["game_exe"]
        if game_exe.exists():
            self.check_client_update(release)

    def check_client_update(self, release):
        """Check if client needs update"""
        remote_version = release.get("version", "0.0.0")
        local_version = "0.0.0"

        if self.local_version:
            local_version = self.local_version.get("version", "0.0.0")

        # Simple version comparison
        def version_tuple(v):
            v = v.lstrip("v")
            return tuple(map(int, v.split("-")[0].split(".")))

        try:
            if version_tuple(remote_version) > version_tuple(local_version):
                self.update_available = True
                self.update_label.config(text=f"Update available: v{local_version} -> v{remote_version}")
                self.version_status.config(text=f"v{local_version} (update available)", fg=C.ORANGE)
                self.update_frame.pack(fill="x", pady=(0, 12))
        except:
            pass

    def update_notes_error(self):
        self.status_label.config(text="GitHub unavailable", fg=C.RED)
        self.latest_status.config(text="Offline", fg=C.RED)
        self.notes_label.config(text="Could not connect to GitHub.\n\nCheck your internet connection.")

    def on_play(self):
        if self.downloading:
            return

        game_exe = self.install_path / CONFIG["game_exe"]
        if game_exe.exists():
            self.launch_game()
        else:
            self.install_game()

    def apply_update(self):
        """Apply available update"""
        if not self.update_available or not self.remote_release:
            return

        self.download_release(self.remote_release)

    def download_release(self, release):
        """Download and install release from GitHub"""
        self.downloading = True
        self.update_frame.pack_forget()
        self.play_btn.config(text="...", state="disabled")
        self.progress_frame.pack(fill="x", pady=(0, 12))
        self.progress_text.config(text="Downloading from GitHub...")
        self.progress_bar["value"] = 0

        def download():
            try:
                url = release["download_url"]
                zip_path = self.install_path / "update.zip"

                # Ensure install path exists
                self.install_path.mkdir(parents=True, exist_ok=True)

                ctx = get_ssl_context()
                req = urllib.request.Request(url, headers={
                    "User-Agent": f"KODemo-Launcher/{CONFIG['version']}"
                })

                response = urllib.request.urlopen(req, timeout=120, context=ctx)
                total = release["size_bytes"]

                downloaded = 0
                block_size = 1024 * 256  # 256KB blocks

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
                        self.root.after(0, lambda p=pct, m=mb, t=total_mb: self.update_progress(p, m, t))

                response.close()

                # Extract
                self.update_ui("Extracting files...")
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    # Get all file names
                    names = zf.namelist()

                    # Check if files are in a subfolder
                    root_folder = None
                    if names and '/' in names[0]:
                        potential_root = names[0].split('/')[0]
                        if all(n.startswith(potential_root + '/') or n == potential_root + '/' for n in names):
                            root_folder = potential_root

                    zf.extractall(self.install_path)

                    # Move files from subfolder if needed
                    if root_folder:
                        subfolder = self.install_path / root_folder
                        if subfolder.exists() and subfolder.is_dir():
                            import shutil
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

                zip_path.unlink()

                # Update local version
                new_version = {
                    "version": release.get("version", "1.0.0"),
                    "tag": release.get("tag", "v1.0.0"),
                    "updated_at": datetime.now().isoformat()
                }
                self.save_local_version(new_version)
                self.local_version = new_version

                self.root.after(0, self.update_complete)

            except Exception as e:
                self.root.after(0, lambda: self.download_error(str(e)))

        threading.Thread(target=download, daemon=True).start()

    def update_complete(self):
        """Update completed successfully"""
        self.downloading = False
        self.update_available = False
        self.progress_frame.pack_forget()
        self.play_btn.config(text="PLAY", state="normal")
        self.check_game()
        messagebox.showinfo("Update Complete", "Game updated successfully!")

    def launch_game(self):
        game_exe = self.install_path / CONFIG["game_exe"]

        # Create Server.ini if needed
        try:
            ini = self.install_path / "Server.ini"
            if not ini.exists():
                with open(ini, "w") as f:
                    f.write("[Server]\n")
                    f.write("Count=1\n")
                    f.write(f"IP0={CONFIG['server_ip']}\n")
                    f.write("\n")
                    f.write("[Version]\n")
                    f.write("Files=1299\n")
        except:
            pass

        try:
            os.chdir(str(self.install_path))
            if sys.platform == "win32":
                subprocess.Popen([str(game_exe)])
            else:
                subprocess.Popen(["wine", str(game_exe)])
            self.root.after(1000, self.root.iconify)
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch game:\n{e}")

    def install_game(self):
        """First time installation"""
        if not self.remote_release:
            messagebox.showinfo("Please wait", "Fetching release info from GitHub...")
            return

        size = self.remote_release.get("size_mb", 334)
        version = self.remote_release.get("version", "1.0.0")

        result = messagebox.askyesno(
            "Install Knight Online Demo",
            f"Download and install the Demo client?\n\n"
            f"Version: v{version}\n"
            f"Size: ~{size} MB\n"
            f"Folder: {self.install_path}\n\n"
            "Continue?"
        )
        if result:
            self.download_release(self.remote_release)

    def update_ui(self, text):
        self.root.after(0, lambda: self.progress_text.config(text=text))

    def update_progress(self, pct, mb, total_mb):
        self.progress_bar["value"] = pct
        self.progress_text.config(text=f"Downloading: {mb:.1f} / {total_mb:.1f} MB ({pct:.0f}%)")

    def download_error(self, error):
        self.downloading = False
        self.progress_frame.pack_forget()
        self.play_btn.config(text="INSTALL", state="normal")
        self.check_game()
        messagebox.showerror("Download Error", f"Download failed:\n\n{error}")

    def force_reinstall(self):
        """Force reinstall the client"""
        if self.downloading:
            return

        result = messagebox.askyesno(
            "Reinstall",
            "Do you want to reinstall the client?\n\n"
            "This will download and reinstall all game files.\n\n"
            "Continue?"
        )
        if not result:
            return

        # Delete local version to force full reinstall
        version_file = self.install_path / "version.json"
        if version_file.exists():
            try:
                version_file.unlink()
            except:
                pass
        self.local_version = None

        # Start download
        if self.remote_release:
            self.download_release(self.remote_release)
        else:
            messagebox.showinfo("Please wait", "Fetching release info from GitHub...")
            self.check_for_updates()

    def open_github(self):
        import webbrowser
        webbrowser.open(f"https://github.com/{CONFIG['github_repo']}")

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Settings")
        win.geometry("400x320")
        win.configure(bg=C.BG)
        win.transient(self.root)
        win.grab_set()

        # Center
        win.update_idletasks()
        x = self.root.winfo_x() + 175
        y = self.root.winfo_y() + 90
        win.geometry(f"400x320+{x}+{y}")

        tk.Label(win, text="SETTINGS", font=("Arial", 14, "bold"),
                fg=C.GOLD, bg=C.BG).pack(pady=15)

        tk.Label(win, text="Install folder:", font=("Arial", 10),
                fg=C.DIM, bg=C.BG).pack(anchor="w", padx=20)
        tk.Label(win, text=str(self.install_path), font=("Arial", 9),
                fg=C.TEXT, bg=C.BG, wraplength=360).pack(anchor="w", padx=20, pady=5)

        tk.Button(win, text="Change folder", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat",
                 command=lambda: self.change_path(win)).pack(anchor="w", padx=20, pady=10)

        # Server settings
        tk.Label(win, text="Server IP:", font=("Arial", 10),
                fg=C.DIM, bg=C.BG).pack(anchor="w", padx=20, pady=(10, 0))

        self.server_entry = tk.Entry(win, font=("Arial", 10), bg=C.BG3, fg=C.TEXT,
                                    insertbackground=C.TEXT, relief="flat", width=30)
        self.server_entry.pack(anchor="w", padx=20, pady=5)
        self.server_entry.insert(0, CONFIG["server_ip"])

        # Version info
        ver_text = f"Launcher: v{CONFIG['version']}"
        if self.local_version:
            ver_text += f"\nClient: v{self.local_version.get('version', '?')}"
        tk.Label(win, text=ver_text, font=("Arial", 9), fg=C.DIM, bg=C.BG).pack(pady=15)

        btn_frame = tk.Frame(win, bg=C.BG)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Save", font=("Arial", 10),
                 fg=C.BG, bg=C.GREEN, relief="flat", padx=20,
                 command=lambda: self.save_settings(win)).pack(side="left", padx=5)

        tk.Button(btn_frame, text="Close", font=("Arial", 10),
                 fg=C.BG, bg=C.GOLD, relief="flat", padx=20,
                 command=win.destroy).pack(side="left", padx=5)

    def save_settings(self, win):
        new_ip = self.server_entry.get().strip()
        if new_ip:
            CONFIG["server_ip"] = new_ip
        win.destroy()

    def change_path(self, win):
        path = filedialog.askdirectory(initialdir=str(self.install_path))
        if path:
            self.install_path = Path(path)
            self.local_version = self.get_local_version()
            self.check_game()
            win.destroy()
            self.open_settings()

    def run(self):
        self.root.mainloop()

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    app = Launcher()
    app.run()
