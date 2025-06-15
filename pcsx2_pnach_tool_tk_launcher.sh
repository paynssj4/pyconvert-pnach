#!/bin/sh
# Script de lancement pour Pcsx2 Pnach Tool (Tkinter)

# Définir le PYTHONPATH pour inclure le répertoire de l'application si nécessaire
# export PYTHONPATH=/app/share/pcsx2_pnach_tool_tk:$PYTHONPATH

# Exécuter l'application Python
python3 /app/share/pcsx2_pnach_tool_tk/pcsx2_pnach_tool_tk.py "$@"
