# Pcsx2 Pnach Tool

`Pcsx2 Pnach Tool` est un utilitaire simple pour convertir des fichiers PNACH. Il fournit une interface graphique pour faciliter le processus.

## Compilation

### Windows

Pour compiler `Pcsx2_Pnach_Tool.py` en un exécutable unique sous Windows, vous pouvez utiliser Nuitka. Assurez-vous d'avoir Nuitka, PySide6, et un compilateur C compatible (comme MinGW ou celui fourni avec Visual Studio) installés dans votre environnement Python.

La commande de base pour la compilation est la suivante, en incluant l'icône de l'application (assurez-vous que `Pcsx2 Pnach Tool.ico` est dans le même répertoire) :

```powershell
python -m nuitka --onefile --windows-disable-console --enable-plugin=pyside6 --windows-icon-from-ico="Pcsx2 Pnach Tool.ico" --output-dir=.\dist --output-filename="Pcsx2 Pnach Tool" Pcsx2_Pnach_Tool.py
```

Cela générera un fichier `Pcsx2 Pnach Tool.exe` dans le sous-dossier `dist`.

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

## Licence

Ce projet est fourni sans licence restrictive spécifique. Étant donné sa nature et sa simplicité, vous êtes libre de l'utiliser, de le modifier et de le distribuer. Si vous souhaitez formaliser cela, vous pouvez envisager d'ajouter une licence permissive telle que la [licence MIT](https://opensource.org/licenses/MIT) ou de le déclarer comme étant dans le [domaine public (Unlicense)](https://unlicense.org/).
