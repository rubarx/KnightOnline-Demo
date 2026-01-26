#!/usr/bin/env python3
"""
AI Knight Online - Professional Launcher v2.4
- Automatic update system (auto-downloads updates)
- Server status from API
- Version checking on startup
- Patch support
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
    "name": "AI Knight Online",
    "version": "2.5.0",
    "server_ip": "game.ai-nexus.net",
    "server_port": 15100,
    "website_url": "https://ko.ai-nexus.net",
    "version_url": "https://ko.ai-nexus.net/downloads/version.json",
    "discord_url": "https://discord.gg/aiknightonline",
    "game_exe": "KnightOnLine.exe",
}

# Colors
class C:
    BG = "#0a0a12"
    BG2 = "#12121f"
    BG3 = "#1a1a2e"
    GOLD = "#d4af37"
    RED = "#cc3333"
    BLUE = "#3366cc"
    GREEN = "#00cc66"
    ORANGE = "#ff9933"
    TEXT = "#ffffff"
    DIM = "#888899"

# ============================================================================
# SSL CONTEXT
# ============================================================================

def get_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

# ============================================================================
# LAUNCHER
# ============================================================================

class Launcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(CONFIG["name"])
        self.root.geometry("800x550")
        self.root.minsize(700, 500)
        self.root.configure(bg=C.BG)
        self.root.resizable(True, True)

        # State
        self.downloading = False
        self.install_path = self.get_install_path()
        self.local_version = None
        self.remote_version = None
        self.update_available = False
        self.update_info = None

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - 800) // 2
        y = (self.root.winfo_screenheight() - 550) // 2
        self.root.geometry(f"800x550+{x}+{y}")

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Gold.Horizontal.TProgressbar",
                       background=C.GOLD, troughcolor=C.BG3)

        # Build UI
        self.build_ui()

        # Check game and updates
        self.root.after(100, self.check_game)
        self.root.after(200, self.check_for_updates)
        self.root.after(500, self.check_server)

    def get_install_path(self):
        current = Path(os.path.dirname(os.path.abspath(sys.argv[0])))
        if (current / CONFIG["game_exe"]).exists():
            return current
        if (current / "Data").exists():
            return current
        if sys.platform == "win32":
            return Path(os.environ.get("LOCALAPPDATA", "C:\\")) / "AI Knight Online"
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
        header = tk.Frame(self.root, bg=C.BG2, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="AI KNIGHT ONLINE",
                font=("Arial", 24, "bold"), fg=C.GOLD, bg=C.BG2).pack(side="left", padx=20, pady=15)

        self.status_label = tk.Label(header, text="Connexion...",
                                    font=("Arial", 10), fg=C.DIM, bg=C.BG2)
        self.status_label.pack(side="right", padx=20)

        # === MAIN CONTENT ===
        main = tk.Frame(self.root, bg=C.BG)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel
        left = tk.Frame(main, bg=C.BG)
        left.pack(side="left", fill="both", expand=True)

        # Hero
        hero = tk.Frame(left, bg=C.BG2)
        hero.pack(fill="x", pady=(0, 10))

        tk.Label(hero, text="Bienvenue sur AI Knight Online!",
                font=("Arial", 16, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(15, 5))
        tk.Label(hero, text="Le premier serveur Knight Online avec Intelligence Artificielle",
                font=("Arial", 10), fg=C.TEXT, bg=C.BG2).pack(anchor="w", padx=15)

        # Nations
        nations = tk.Frame(hero, bg=C.BG2)
        nations.pack(anchor="w", padx=15, pady=10)
        tk.Label(nations, text=" KARUS ", font=("Arial", 10, "bold"),
                fg=C.TEXT, bg=C.RED).pack(side="left")
        tk.Label(nations, text=" vs ", font=("Arial", 10),
                fg=C.GOLD, bg=C.BG2).pack(side="left", padx=5)
        tk.Label(nations, text=" EL MORAD ", font=("Arial", 10, "bold"),
                fg=C.TEXT, bg=C.BLUE).pack(side="left")

        # Server Status
        status_frame = tk.Frame(left, bg=C.BG2)
        status_frame.pack(fill="x", pady=(0, 10))

        tk.Label(status_frame, text="SERVEUR",
                font=("Arial", 11, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=15, pady=(10, 5))

        row1 = tk.Frame(status_frame, bg=C.BG2)
        row1.pack(fill="x", padx=15, pady=2)
        tk.Label(row1, text="Etat:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        self.server_status = tk.Label(row1, text="Verification...",
                                     font=("Arial", 10, "bold"), fg=C.DIM, bg=C.BG2)
        self.server_status.pack(side="right")

        row2 = tk.Frame(status_frame, bg=C.BG2)
        row2.pack(fill="x", padx=15, pady=2)
        tk.Label(row2, text="Adresse:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        tk.Label(row2, text=f"{CONFIG['server_ip']}:{CONFIG['server_port']}",
                font=("Arial", 10), fg=C.GOLD, bg=C.BG2).pack(side="right")

        row3 = tk.Frame(status_frame, bg=C.BG2)
        row3.pack(fill="x", padx=15, pady=2)
        tk.Label(row3, text="Client:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        self.client_status = tk.Label(row3, text="Verification...",
                                     font=("Arial", 10, "bold"), fg=C.DIM, bg=C.BG2)
        self.client_status.pack(side="right")

        row4 = tk.Frame(status_frame, bg=C.BG2)
        row4.pack(fill="x", padx=15, pady=(2, 10))
        tk.Label(row4, text="Version:", font=("Arial", 10), fg=C.DIM, bg=C.BG2).pack(side="left")
        self.version_status = tk.Label(row4, text="...",
                                      font=("Arial", 10, "bold"), fg=C.DIM, bg=C.BG2)
        self.version_status.pack(side="right")

        # Update notification (hidden initially)
        self.update_frame = tk.Frame(left, bg=C.ORANGE)

        self.update_label = tk.Label(self.update_frame, text="",
                                    font=("Arial", 10, "bold"), fg=C.BG, bg=C.ORANGE)
        self.update_label.pack(side="left", padx=10, pady=8)

        self.update_btn = tk.Button(self.update_frame, text="METTRE A JOUR",
                                   font=("Arial", 9, "bold"), fg=C.ORANGE, bg=C.BG,
                                   relief="flat", padx=10, command=self.apply_update)
        self.update_btn.pack(side="right", padx=10, pady=5)

        # Progress (hidden initially)
        self.progress_frame = tk.Frame(left, bg=C.BG2)

        self.progress_text = tk.Label(self.progress_frame, text="",
                                     font=("Arial", 9), fg=C.TEXT, bg=C.BG2)
        self.progress_text.pack(anchor="w", padx=15, pady=(10, 5))

        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                           style="Gold.Horizontal.TProgressbar",
                                           length=300, mode='determinate')
        self.progress_bar.pack(fill="x", padx=15, pady=(0, 10))

        # Right panel - News
        right = tk.Frame(main, bg=C.BG2, width=250)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        tk.Label(right, text="ACTUALITES",
                font=("Arial", 11, "bold"), fg=C.GOLD, bg=C.BG2).pack(anchor="w", padx=10, pady=(10, 5))

        self.news_label = tk.Label(right, text="Chargement...", font=("Arial", 9),
                                  fg=C.TEXT, bg=C.BG2, justify="left", wraplength=220)
        self.news_label.pack(anchor="w", padx=10, pady=5)

        # === FOOTER ===
        footer = tk.Frame(self.root, bg=C.BG2, height=80)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        # Buttons left
        btns = tk.Frame(footer, bg=C.BG2)
        btns.pack(side="left", padx=20, pady=20)

        tk.Button(btns, text="Site Web", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=10,
                 command=self.open_website).pack(side="left", padx=(0, 5))
        tk.Button(btns, text="S'inscrire", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=10,
                 command=self.open_register).pack(side="left", padx=(0, 5))
        tk.Button(btns, text="Parametres", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat", padx=10,
                 command=self.open_settings).pack(side="left", padx=(0, 5))
        tk.Button(btns, text="Reinstaller", font=("Arial", 9),
                 fg=C.TEXT, bg=C.RED, relief="flat", padx=10,
                 command=self.force_reinstall).pack(side="left")

        # Play button
        self.play_btn = tk.Button(footer, text="JOUER",
                                 font=("Arial", 16, "bold"),
                                 fg=C.BG, bg=C.GOLD,
                                 activeforeground=C.BG, activebackground="#e8c84a",
                                 relief="flat", width=15, height=2,
                                 command=self.on_play)
        self.play_btn.pack(side="right", padx=20, pady=15)

    def check_game(self):
        game_exe = self.install_path / CONFIG["game_exe"]
        if game_exe.exists():
            self.client_status.config(text="Installe", fg=C.GREEN)
            self.play_btn.config(text="JOUER")

            # Get local version
            self.local_version = self.get_local_version()
            if self.local_version and "client" in self.local_version:
                ver = self.local_version["client"].get("version", "?")
                self.version_status.config(text=f"v{ver}", fg=C.GREEN)
            else:
                self.version_status.config(text="v1.0.0", fg=C.GREEN)
        else:
            self.client_status.config(text="Non installe", fg=C.RED)
            self.version_status.config(text="-", fg=C.DIM)
            self.play_btn.config(text="INSTALLER")

    def check_for_updates(self):
        """Check for client updates"""
        def fetch():
            try:
                ctx = get_ssl_context()
                req = urllib.request.Request(
                    CONFIG["version_url"],
                    headers={"User-Agent": f"AIKOLauncher/{CONFIG['version']}"}
                )
                with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                    data = json.loads(r.read().decode('utf-8'))
                    self.root.after(0, lambda: self.process_version_info(data))
            except Exception as e:
                print(f"Update check failed: {e}")
                self.root.after(0, lambda: self.update_news_default())

        threading.Thread(target=fetch, daemon=True).start()

    def process_version_info(self, data):
        """Process version info from server"""
        self.remote_version = data

        # Update news
        if "client" in data and "changelog" in data["client"]:
            changelog = data["client"]["changelog"]
            news_text = "Derniere mise a jour:\n\n"
            for item in changelog[:5]:
                news_text += f"- {item}\n"
            news_text += f"\nVersion: {data['client'].get('version', '?')}"
            news_text += f"\nDate: {data['client'].get('date', '?')}"
            self.news_label.config(text=news_text)
        else:
            self.update_news_default()

        # Update server info
        if "server" in data:
            CONFIG["server_ip"] = data["server"].get("ip", CONFIG["server_ip"])
            CONFIG["server_port"] = data["server"].get("port", CONFIG["server_port"])

        # Check if update needed
        game_exe = self.install_path / CONFIG["game_exe"]
        if game_exe.exists():
            self.check_client_update(data)

    def check_client_update(self, data):
        """Check if client needs update and auto-update"""
        if "client" not in data:
            return

        remote_build = data["client"].get("build", 0)
        local_build = 0

        if self.local_version and "client" in self.local_version:
            local_build = self.local_version["client"].get("build", 0)

        if remote_build > local_build:
            self.update_available = True
            self.update_info = data

            remote_ver = data["client"].get("version", "?")
            local_ver = "1.0.0"
            if self.local_version and "client" in self.local_version:
                local_ver = self.local_version["client"].get("version", "1.0.0")

            self.update_label.config(text=f"Mise a jour: v{local_ver} -> v{remote_ver}")
            self.version_status.config(text=f"v{local_ver} (MAJ auto)", fg=C.ORANGE)

            # AUTO-UPDATE: Start update automatically after 2 seconds
            self.root.after(2000, self.auto_apply_update)

    def update_news_default(self):
        news = """Bienvenue!

Le serveur est ouvert.

Fonctionnalites:
- GM IA 24/7 (/gm)
- NPCs intelligents
- Events quotidiens

Lunar War tous les jours
Castle Siege le dimanche"""
        self.news_label.config(text=news)

    def check_server(self):
        """Check server status from version.json"""
        def fetch():
            try:
                # Use version.json to check server status
                if self.remote_version and "server" in self.remote_version:
                    status = self.remote_version["server"].get("status", "unknown")
                    if status == "online":
                        self.root.after(0, lambda: self.server_status.config(text="EN LIGNE", fg=C.GREEN))
                        self.root.after(0, lambda: self.status_label.config(text="Connecte", fg=C.GREEN))
                    else:
                        self.root.after(0, lambda: self.server_status.config(text="HORS LIGNE", fg=C.RED))
                        self.root.after(0, lambda: self.status_label.config(text="Deconnecte", fg=C.RED))
                else:
                    # Fallback: try to reach the website
                    ctx = get_ssl_context()
                    req = urllib.request.Request(
                        CONFIG["version_url"],
                        headers={"User-Agent": f"AIKOLauncher/{CONFIG['version']}"}
                    )
                    with urllib.request.urlopen(req, timeout=5, context=ctx) as r:
                        self.root.after(0, lambda: self.server_status.config(text="EN LIGNE", fg=C.GREEN))
                        self.root.after(0, lambda: self.status_label.config(text="Connecte", fg=C.GREEN))
            except Exception as e:
                self.root.after(0, lambda: self.server_status.config(text="HORS LIGNE", fg=C.RED))
                self.root.after(0, lambda: self.status_label.config(text="Deconnecte", fg=C.RED))

        threading.Thread(target=fetch, daemon=True).start()
        self.root.after(30000, self.check_server)

    def on_play(self):
        if self.downloading:
            return

        game_exe = self.install_path / CONFIG["game_exe"]
        if game_exe.exists():
            self.launch_game()
        else:
            self.install_game()

    def auto_apply_update(self):
        """Automatically apply update without asking"""
        if not self.update_available or not self.update_info or self.downloading:
            return

        # Check for patches first
        if "patches" in self.update_info and self.update_info["patches"]:
            local_build = 0
            if self.local_version and "client" in self.local_version:
                local_build = self.local_version["client"].get("build", 0)

            applicable_patches = [
                p for p in self.update_info["patches"]
                if p.get("from_build", 0) == local_build
            ]

            if applicable_patches:
                self.download_patch(applicable_patches[0])
                return

        # Full update - automatic
        client_info = self.update_info["client"]
        self.download_update(client_info)

    def apply_update(self):
        """Apply available update (manual trigger)"""
        if not self.update_available or not self.update_info:
            return

        # Check for patches first
        if "patches" in self.update_info and self.update_info["patches"]:
            # Find applicable patches
            local_build = 0
            if self.local_version and "client" in self.local_version:
                local_build = self.local_version["client"].get("build", 0)

            applicable_patches = [
                p for p in self.update_info["patches"]
                if p.get("from_build", 0) == local_build
            ]

            if applicable_patches:
                # Apply patch instead of full download
                patch = applicable_patches[0]
                result = messagebox.askyesno(
                    "Mise a jour",
                    f"Appliquer le patch?\n\n"
                    f"Version: {patch.get('version', '?')}\n"
                    f"Taille: ~{patch.get('size_mb', '?')} MB\n\n"
                    "Continuer?"
                )
                if result:
                    self.download_patch(patch)
                return

        # Full update
        client_info = self.update_info["client"]
        result = messagebox.askyesno(
            "Mise a jour",
            f"Telecharger la mise a jour complete?\n\n"
            f"Version: {client_info.get('version', '?')}\n"
            f"Taille: ~{client_info.get('size_mb', '?')} MB\n\n"
            "Continuer?"
        )
        if result:
            self.download_update(client_info)

    def download_patch(self, patch_info):
        """Download and apply a patch"""
        self.downloading = True
        self.update_frame.pack_forget()
        self.play_btn.config(text="...", state="disabled")
        self.progress_frame.pack(fill="x", pady=(0, 10))
        self.progress_text.config(text="Telechargement du patch...")
        self.progress_bar["value"] = 0

        def download():
            try:
                url = patch_info["url"]
                patch_path = self.install_path / "patch.zip"

                ctx = get_ssl_context()
                req = urllib.request.Request(url, headers={
                    "User-Agent": f"AIKOLauncher/{CONFIG['version']}"
                })

                response = urllib.request.urlopen(req, timeout=60, context=ctx)
                total = int(response.headers.get('content-length', 0))
                if total == 0:
                    total = patch_info.get("size_mb", 10) * 1024 * 1024

                downloaded = 0
                block_size = 1024 * 256

                with open(patch_path, 'wb') as f:
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

                # Verify hash if provided (auto-detect MD5 vs SHA256)
                if "hash" in patch_info and patch_info["hash"]:
                    self.update_ui("Verification du patch...")
                    with open(patch_path, "rb") as f:
                        content = f.read()
                        h = patch_info["hash"]
                        if len(h) == 64:  # SHA256
                            file_hash = hashlib.sha256(content).hexdigest()
                        else:  # MD5
                            file_hash = hashlib.md5(content).hexdigest()
                    if file_hash != patch_info["hash"]:
                        self.root.after(0, lambda: self.download_error("Hash invalide - fichier corrompu"))
                        patch_path.unlink()
                        return

                # Extract patch
                self.update_ui("Application du patch...")
                with zipfile.ZipFile(patch_path, 'r') as zf:
                    zf.extractall(self.install_path)

                patch_path.unlink()

                # Update local version
                new_version = {
                    "client": {
                        "version": patch_info.get("version", "1.0.1"),
                        "build": patch_info.get("to_build", 1),
                        "date": patch_info.get("date", "")
                    }
                }
                self.save_local_version(new_version)
                self.local_version = new_version

                self.root.after(0, self.update_complete)

            except Exception as e:
                self.root.after(0, lambda: self.download_error(str(e)))

        threading.Thread(target=download, daemon=True).start()

    def download_update(self, client_info):
        """Download full update"""
        self.downloading = True
        self.update_frame.pack_forget()
        self.play_btn.config(text="...", state="disabled")
        self.progress_frame.pack(fill="x", pady=(0, 10))
        self.progress_text.config(text="Telechargement de la mise a jour...")
        self.progress_bar["value"] = 0

        def download():
            try:
                url = client_info["url"]
                zip_path = self.install_path / "update.zip"

                ctx = get_ssl_context()
                req = urllib.request.Request(url, headers={
                    "User-Agent": f"AIKOLauncher/{CONFIG['version']}"
                })

                response = urllib.request.urlopen(req, timeout=60, context=ctx)
                total = int(response.headers.get('content-length', 0))
                if total == 0:
                    total = client_info.get("size_mb", 354) * 1024 * 1024

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
                        self.root.after(0, lambda p=pct, m=mb, t=total_mb: self.update_progress(p, m, t))

                response.close()

                # Verify hash if provided (auto-detect MD5 vs SHA256)
                if "hash" in client_info and client_info["hash"]:
                    self.update_ui("Verification de l'integrite...")
                    with open(zip_path, "rb") as f:
                        content = f.read()
                        h = client_info["hash"]
                        if len(h) == 64:  # SHA256
                            file_hash = hashlib.sha256(content).hexdigest()
                        else:  # MD5
                            file_hash = hashlib.md5(content).hexdigest()
                    if file_hash != client_info["hash"]:
                        self.root.after(0, lambda: self.download_error("Hash invalide - fichier corrompu"))
                        zip_path.unlink()
                        return

                # Extract
                self.update_ui("Installation de la mise a jour...")
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    names = zf.namelist()
                    if names and '/' in names[0]:
                        root_folder = names[0].split('/')[0]
                    else:
                        root_folder = None

                    zf.extractall(self.install_path)

                    if root_folder:
                        subfolder = self.install_path / root_folder
                        if subfolder.exists() and subfolder.is_dir():
                            for item in subfolder.iterdir():
                                dest = self.install_path / item.name
                                if dest.exists():
                                    if dest.is_file():
                                        dest.unlink()
                                    elif dest.is_dir():
                                        import shutil
                                        shutil.rmtree(dest)
                                item.rename(dest)
                            try:
                                subfolder.rmdir()
                            except:
                                pass

                zip_path.unlink()

                # Update local version
                new_version = {
                    "client": {
                        "version": client_info.get("version", "1.0.0"),
                        "build": client_info.get("build", 1),
                        "date": client_info.get("date", "")
                    }
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
        self.play_btn.config(text="JOUER", state="normal")
        self.check_game()
        messagebox.showinfo("Mise a jour", "Mise a jour installee avec succes!")

    def launch_game(self):
        game_exe = self.install_path / CONFIG["game_exe"]

        # Create server.ini
        try:
            ini = self.install_path / "server.ini"
            with open(ini, "w") as f:
                f.write(f"[Server]\n")
                f.write(f"ip={CONFIG['server_ip']}\n")
                f.write(f"serverport={CONFIG['server_port']}\n")
        except:
            pass

        try:
            os.chdir(str(self.install_path))
            if sys.platform == "win32":
                subprocess.Popen([str(game_exe)])
            else:
                subprocess.Popen(["wine", str(game_exe)])
            self.root.iconify()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lancer le jeu:\n{e}")

    def install_game(self):
        """First time installation"""
        # Fetch version info if not already done
        if not self.remote_version:
            messagebox.showinfo("Patientez", "Recuperation des informations...")
            return

        client_info = self.remote_version.get("client", {})
        size = client_info.get("size_mb", 354)

        result = messagebox.askyesno(
            "Installation",
            f"Telecharger le client Knight Online?\n\n"
            f"Taille: ~{size} MB\n"
            f"Dossier: {self.install_path}\n\n"
            "Continuer?"
        )
        if not result:
            return

        self.downloading = True
        self.play_btn.config(text="...", state="disabled")
        self.progress_frame.pack(fill="x", pady=(0, 10))
        self.progress_text.config(text="Demarrage du telechargement...")
        self.progress_bar["value"] = 0

        threading.Thread(target=lambda: self.download_update(client_info), daemon=True).start()

    def update_ui(self, text):
        self.root.after(0, lambda: self.progress_text.config(text=text))

    def update_progress(self, pct, mb, total_mb):
        self.progress_bar["value"] = pct
        self.progress_text.config(text=f"Telechargement: {mb:.1f} / {total_mb:.1f} MB ({pct:.0f}%)")

    def download_error(self, error):
        self.downloading = False
        self.progress_frame.pack_forget()
        self.play_btn.config(text="INSTALLER", state="normal")
        self.check_game()
        messagebox.showerror("Erreur", f"Telechargement echoue:\n\n{error}")

    def force_reinstall(self):
        """Force reinstall the client"""
        if self.downloading:
            return

        result = messagebox.askyesno(
            "Reinstallation",
            "Voulez-vous reinstaller le client complet?\n\n"
            "Cela va telecharger et reinstaller tous les fichiers du jeu.\n\n"
            "Continuer?"
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

        # Fetch remote version and start download
        if self.remote_version and "client" in self.remote_version:
            self.download_update(self.remote_version["client"])
        else:
            messagebox.showinfo("Patientez", "Recuperation des informations du serveur...")
            self.check_for_updates()

    def open_website(self):
        import webbrowser
        webbrowser.open(CONFIG["website_url"])

    def open_register(self):
        import webbrowser
        webbrowser.open(f"{CONFIG['website_url']}/register")

    def open_settings(self):
        win = tk.Toplevel(self.root)
        win.title("Parametres")
        win.geometry("400x300")
        win.configure(bg=C.BG)
        win.transient(self.root)
        win.grab_set()

        # Center
        win.update_idletasks()
        x = self.root.winfo_x() + 200
        y = self.root.winfo_y() + 125
        win.geometry(f"400x300+{x}+{y}")

        tk.Label(win, text="PARAMETRES", font=("Arial", 14, "bold"),
                fg=C.GOLD, bg=C.BG).pack(pady=15)

        tk.Label(win, text="Dossier d'installation:", font=("Arial", 10),
                fg=C.DIM, bg=C.BG).pack(anchor="w", padx=20)
        tk.Label(win, text=str(self.install_path), font=("Arial", 9),
                fg=C.TEXT, bg=C.BG, wraplength=360).pack(anchor="w", padx=20, pady=5)

        tk.Button(win, text="Changer le dossier", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat",
                 command=lambda: self.change_path(win)).pack(anchor="w", padx=20, pady=10)

        tk.Label(win, text=f"Serveur: {CONFIG['server_ip']}:{CONFIG['server_port']}",
                font=("Arial", 10), fg=C.GOLD, bg=C.BG).pack(pady=10)

        # Version info
        ver_text = f"Launcher: v{CONFIG['version']}"
        if self.local_version and "client" in self.local_version:
            ver_text += f"\nClient: v{self.local_version['client'].get('version', '?')}"
        tk.Label(win, text=ver_text, font=("Arial", 9), fg=C.DIM, bg=C.BG).pack(pady=5)

        tk.Button(win, text="Verifier les mises a jour", font=("Arial", 9),
                 fg=C.TEXT, bg=C.BG3, relief="flat",
                 command=lambda: [win.destroy(), self.check_for_updates()]).pack(pady=5)

        tk.Button(win, text="Fermer", font=("Arial", 10),
                 fg=C.BG, bg=C.GOLD, relief="flat", padx=20,
                 command=win.destroy).pack(pady=10)

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
