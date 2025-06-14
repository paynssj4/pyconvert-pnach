# pyconvert-pnach

`pyconvert-pnach` est un utilitaire simple pour convertir des fichiers PNACH. Il fournit une interface graphique pour faciliter le processus.

## Compilation

Pour compiler `pyconvert_pnacher.py` en un exécutable unique sous Windows, vous pouvez utiliser Nuitka. Assurez-vous d'avoir Nuitka et un compilateur C compatible (comme MinGW ou celui fourni avec Visual Studio) installés.

La commande de base pour la compilation est la suivante (en supposant que vous utilisez PySide6 pour l'interface graphique) :

```bash
python -m nuitka --onefile --windows-disable-console --enable-plugin=pyside6 pyconvert_pnacher.py
```

Cela générera un fichier `pyconvert_pnacher.exe`. Avec l'option `--onefile`, Nuitka s'efforce de créer un seul exécutable autonome.

## Licence

Ce projet est fourni sans licence restrictive spécifique. Étant donné sa nature et sa simplicité, vous êtes libre de l'utiliser, de le modifier et de le distribuer. Si vous souhaitez formaliser cela, vous pouvez envisager d'ajouter une licence permissive telle que la [licence MIT](https://opensource.org/licenses/MIT) ou de le déclarer comme étant dans le [domaine public (Unlicense)](https://unlicense.org/).
