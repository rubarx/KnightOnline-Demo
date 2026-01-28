# Knight Online Demo - Documentation Technique

## Apercu du Projet

Fork de Open-KO/KnightOnline avec fonctionnalites custom pour demonstration.
Ce projet est compile via GitHub Actions et distribue avec un launcher auto-update.

**Repository** : https://github.com/rubarx/KnightOnline-Demo
**Branche principale** : `demo`
**Derniere release** : v1.2.0-demo
**Page de telechargement** : `website/index.html` (a deployer sur ton domaine)

---

## Fonctionnalites Custom Implementees

### 1. Town Button (Touche G)
- **Fichiers** : `src/Client/WarFare/UITownButtons.h`, `UITownButtons.cpp`
- **Fonction** : Bouton unique pour teleportation rapide en ville via commande `/town`
- **Keybind** : `KM_TOGGLE_TOWN_BUTTONS = DIK_G` dans GameDef.h

### 2. Auto-Pot System (Touche Insert)
- **Fichiers** : `src/Client/WarFare/AutoPotManager.h`, `AutoPotManager.cpp`
- **Fonction** : Utilisation automatique des potions HP/MP
- **Configuration** :
  - HP threshold : 50% (declenchement si HP < 50%)
  - MP threshold : 30% (declenchement si MP < 30%)
  - Cooldown : 1.0s entre chaque utilisation
- **Keybind** : `KM_TOGGLE_AUTOPOT = DIK_INSERT` dans GameDef.h

### 3. Skill Macros (Numpad 1-6)
- **Fichiers** : `src/Client/WarFare/MacroManager.h`, `MacroManager.cpp`
- **Fonction** : Macros de skills pre-configurees sur le pave numerique
- **Keybinds** : `KM_MACRO1` a `KM_MACRO6` = `DIK_NUMPAD1` a `DIK_NUMPAD6`

### 4. Extended Hotkeys
- **Fichier** : `src/Client/WarFare/GameDef.h`
- **Modification** : `MAX_SKILL_IN_HOTKEY = 10` (au lieu de 8)
- **Touches** : 1-0 pour 10 slots de skills

---

## Integration dans GameProcMain

### GameProcMain.h - Declarations ajoutees
```cpp
class CUITownButtons* m_pUITownButtons;
class CAutoPotManager* m_pAutoPotManager;
class CMacroManager* m_pMacroManager;

void CommandToggleUITownButtons();
```

### GameProcMain.cpp - Modifications
1. **Includes** : UITownButtons.h, AutoPotManager.h, MacroManager.h
2. **Constructeur** : Allocation des managers
3. **Destructeur** : Liberation memoire
4. **Tick()** : Appel des Tick() pour AutoPot et Macro
5. **ProcessUIKeyInput()** : Gestion des keybinds G, Insert, Numpad 1-6
6. **InitUI()** : Initialisation de UITownButtons

---

## Launcher Auto-Update

### Fichiers
- `launcher/src/demo_launcher.py` - Code source Python/Tkinter
- `launcher/build_launcher.bat` - Script de compilation local

### Fonctionnalites
- Interface graphique professionnelle (theme sombre)
- Verification automatique des releases GitHub au demarrage
- Telechargement avec barre de progression
- Extraction et installation automatique
- Configuration du serveur dans les parametres
- Fichier `version.json` local pour suivi des versions

### Configuration (dans demo_launcher.py)
```python
CONFIG = {
    "name": "Knight Online Demo",
    "version": "1.0.0",
    "github_repo": "rubarx/KnightOnline-Demo",
    "github_api": "https://api.github.com/repos/rubarx/KnightOnline-Demo/releases/latest",
    "game_exe": "KnightOnLine.exe",
    "server_ip": "127.0.0.1",
    "server_port": 15100,
}
```

### Workflow de mise a jour
1. Launcher demarre -> verifie GitHub API
2. Compare version locale (version.json) avec derniere release
3. Si mise a jour disponible -> notification orange
4. Telechargement automatique ou manuel
5. Extraction du ZIP dans le dossier d'installation
6. Mise a jour de version.json

---

## Installer Standalone

### Fichiers
- `installer/KO-Demo-Installer.py` - Code source Python/Tkinter
- `installer/build_installer.bat` - Script de compilation local

### Fonctionnalites
- Executable leger (~12 MB) distribuable seul
- Telecharge le jeu complet depuis GitHub Releases
- Interface d'installation avec choix du dossier
- Barre de progression pendant le telechargement
- Creation automatique de raccourcis (Bureau + Menu Demarrer)
- Lancement du jeu apres installation

### Utilisation
1. L'utilisateur telecharge uniquement `KO-Demo-Setup.exe`
2. Lance l'installer -> choisit le dossier d'installation
3. L'installer telecharge ~335 MB depuis GitHub
4. Extrait, cree les raccourcis, lance le jeu

### Avantage
Permet de distribuer un petit fichier de 12 MB au lieu du ZIP complet de 335 MB.
L'installer telecharge toujours la derniere version depuis GitHub.

---

## Page Web de Telechargement

### Fichier
- `website/index.html` - Page HTML/CSS/JS complete

### Fonctionnalites
- Design professionnel theme sombre
- Recupere automatiquement la derniere release via GitHub API
- Deux options de telechargement :
  - **Installer** (~12 MB) - Recommande
  - **Package complet** (~335 MB)
- Affiche les features custom
- Liens vers GitHub

### Deploiement
Copier `website/index.html` sur ton serveur web (ko.ai-nexus.net ou autre).
La page est autonome, pas de dependances externes sauf Google Fonts.

---

## GitHub Actions Workflow

### Fichier : `.github/workflows/build_demo_release.yml`

### Declencheurs
- Push sur branche `demo`
- Creation de tag `v*`
- Declenchement manuel (workflow_dispatch)

### Etapes du build
1. Checkout code avec submodules
2. Setup Python 3.11
3. Installation PyInstaller
4. **Build Launcher** : `pyinstaller --onefile --windowed demo_launcher.py`
5. **Build Installer** : `pyinstaller --onefile --windowed KO-Demo-Installer.py`
6. Setup MSBuild
7. **Build Client** : `msbuild /p:Configuration="Release" /p:Platform="x64" Client.slnx`
8. Creation du package (copie exe, launcher, assets, README)
9. Creation ZIP
10. Upload artifacts (ZIP + Installer)
11. Creation release GitHub avec les 2 fichiers (si tag)

### Fichiers de release
```
Release GitHub contient 2 fichiers :

1. KO-Demo-Setup.exe          (~12 MB - Installer standalone)
   └── Telecharge et installe tout automatiquement

2. KnightOnline-Demo-x64.zip  (~335 MB - Package complet)
   ├── KO-Demo-Launcher.exe   (11.7 MB - Launcher auto-update)
   ├── KnightOnLine.exe       (4.3 MB - Client du jeu)
   ├── Launch-Demo.bat        (Script batch simple)
   ├── README.txt             (Instructions)
   ├── Chr/                   (Assets personnages)
   ├── Data/                  (Donnees du jeu)
   ├── Obj/                   (Objets 3D)
   ├── Sfx/                   (Effets sonores)
   ├── Texture/               (Textures)
   └── UI_US/                 (Interface utilisateur)
```

---

## Fichiers Modifies vs OpenKO Original

### Nouveaux fichiers (src/Client/WarFare/)
| Fichier | Description |
|---------|-------------|
| UITownButtons.h | Header bouton /town |
| UITownButtons.cpp | Implementation |
| AutoPotManager.h | Header auto-pot |
| AutoPotManager.cpp | Implementation |
| MacroManager.h | Header macros |
| MacroManager.cpp | Implementation |

### Fichiers modifies
| Fichier | Modifications |
|---------|---------------|
| GameProcMain.h | Declarations des managers |
| GameProcMain.cpp | Init, Tick, Keybinds |
| GameDef.h | MAX_SKILL_IN_HOTKEY=10, nouveaux keybinds |
| WarFare.Core.vcxproj | Ajout des nouveaux fichiers au projet |

### Assets
| Fichier | Description |
|---------|-------------|
| assets/Client/UI_US/co_townbuttons_us.uif | Interface bouton town |

### Outils
| Fichier | Description |
|---------|-------------|
| tools/uif_tool.py | Generateur de fichiers .uif pour Linux |

---

## Procedure de Release

### Creer une nouvelle version
```bash
cd /home/rubar/ko-project/KnightOnline-Demo

# 1. Faire les modifications
# 2. Commit
git add .
git commit -m "Description des changements

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 3. Push
git push origin demo

# 4. Creer et pusher le tag
git tag -a v1.2.0-demo -m "Description de la release"
git push origin v1.2.0-demo
```

### Verifier le build
```bash
# Voir les workflows en cours
gh run list --limit 5

# Suivre un workflow specifique
gh run watch <run-id>

# Voir la release
gh release view v1.2.0-demo
```

---

## Submodules

Le projet utilise des submodules pour les assets :
- `assets/Client` -> rubarx/ko-client-assets-demo

### Mise a jour des submodules
```bash
git submodule update --init --recursive
```

---

## Corrections de Build Appliquees

### Erreur LNK2001 (symboles non resolus)
- **Cause** : Fichiers sources non inclus dans vcxproj
- **Solution** : Ajout des ClCompile/ClInclude dans WarFare.Core.vcxproj

### Erreur C2365 (ITEM_CLASS_POTION redefinition)
- **Cause** : Constante deja definie dans ItemDef.h
- **Solution** : Commentaire de la definition locale dans AutoPotManager.cpp

### Erreur C2039 (iMSPMax not member)
- **Cause** : Mauvais nom de champ
- **Solution** : Remplacement de iMSP/iMSPMax par iMP/iMPMax

---

## URLs Importantes

- **Repository** : https://github.com/rubarx/KnightOnline-Demo
- **Releases** : https://github.com/rubarx/KnightOnline-Demo/releases
- **Latest Release** : https://github.com/rubarx/KnightOnline-Demo/releases/latest
- **Actions** : https://github.com/rubarx/KnightOnline-Demo/actions
- **OpenKO Original** : https://github.com/Open-KO/KnightOnline

---

## Notes pour le Developpement

### Compilation locale (Windows)
1. Ouvrir `Client.slnx` dans Visual Studio 2022
2. Configuration : Release x64
3. Build Solution

### Test du launcher
```bash
cd launcher/src
python demo_launcher.py
```

### Build du launcher en executable
```bash
cd launcher
./build_launcher.bat  # Windows
# ou
cd launcher/src && pyinstaller --onefile --windowed demo_launcher.py
```
