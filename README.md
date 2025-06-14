# Pcsx2 Pnach Tool

`Pcsx2 Pnach Tool` est un utilitaire simple pour convertir des fichiers PNACH. Il fournit une interface graphique pour faciliter le processus.

## Capture d'écran

![Capture d'écran de Pcsx2 Pnach Tool](https://raw.githubusercontent.com/paynssj4/pyconvert-pnach/main/Pcsx2%20Pnach%20Tool.jpg)

## Compilation

### Windows

Pour compiler `Pcsx2_Pnach_Tool.py` en un exécutable unique sous Windows, vous pouvez utiliser Nuitka. Assurez-vous d'avoir Nuitka, PySide6, et un compilateur C compatible (comme MinGW ou celui fourni avec Visual Studio) installés dans votre environnement Python.

La commande de base pour la compilation est la suivante, en incluant l'icône de l'application (assurez-vous que `Pcsx2 Pnach Tool.ico` est dans le même répertoire) :

```powershell
python -m nuitka --onefile --windows-disable-console --enable-plugin=pyside6 --windows-icon-from-ico="Pcsx2 Pnach Tool.ico" --output-dir=.\dist --output-filename="Pcsx2 Pnach Tool" Pcsx2_Pnach_Tool.py
```

Cela générera un fichier `Pcsx2 Pnach Tool.exe` dans le sous-dossier `dist`.

#### Exécution (Windows)

Après la compilation, vous trouverez l'exécutable `Pcsx2 Pnach Tool.exe` dans le dossier `dist` (créé à la racine de votre projet).
Pour lancer l'application :
1. Ouvrez l'explorateur de fichiers et naviguez jusqu'au dossier `dist`.
2. Double-cliquez sur `Pcsx2 Pnach Tool.exe`.

Ou depuis le terminal PowerShell, si vous êtes à la racine du projet :
```powershell
.\dist\"Pcsx2 Pnach Tool.exe"
```

### Linux

Pour compiler `Pcsx2_Pnach_Tool.py` en un exécutable unique sous Linux (par exemple, via WSL), vous pouvez utiliser Nuitka. Assurez-vous d'avoir Nuitka, PySide6, un compilateur C (comme GCC), et l'outil `patchelf` installés dans votre environnement Python/Linux.

1.  Installez `patchelf` si ce n'est pas déjà fait (exemple pour les distributions basées sur Debian/Ubuntu) :
    ```bash
    sudo apt update
    sudo apt install patchelf
    ```
2.  Assurez-vous que PySide6 est installé dans votre environnement virtuel :
    ```bash
    pip install PySide6
    ```
3.  Compilez avec Nuitka:
       
    ```bash
    python -m nuitka --onefile --enable-plugin=pyside6 --output-dir=./dist --output-filename="Pcsx2 Pnach Tool" Pcsx2_Pnach_Tool.py
    ```

Cela générera un fichier exécutable nommé `Pcsx2 Pnach Tool` dans le sous-dossier `dist`.

#### Exécution (Linux)

Après la compilation, vous trouverez l'exécutable `Pcsx2 Pnach Tool` dans le dossier `dist` (créé à la racine de votre projet).
Pour lancer l'application depuis le terminal, si vous êtes à la racine du projet :
1. Naviguez vers le dossier de sortie :
   ```bash
   cd dist
   ```
2. Rendez l'exécutable exécutable (si ce n'est pas déjà le cas) :
   ```bash
   chmod +x "Pcsx2 Pnach Tool"
   ```
3. Lancez l'application :
   ```bash
   ./"Pcsx2 Pnach Tool"
   ```

## Licence

Ce projet est sous licence GPL v3. Voir le fichier `LICENSE` pour plus de détails.
