# translations_tk.py

TRANSLATIONS = {
    "en": {
        "window_title": "Pcsx2 Pnach Tool",
        "input_instructions_label": "RAW Codes and Descriptions (Optional):",
        "input_instructions_text": """Enter RAW codes (XXXXXXXX YYYYYYYY) and/or descriptions.
A line that does not look like a RAW code will be treated as a description for the next code.
Example:
Max Money
2030B968 FFFFFFFF
Infinite Lives
10123456 00000009""",
        "raw_input_placeholder_tk": """Paste your RAW codes here, one per line (e.g., 20XXXXXX XXXXXXXX)
You can add descriptions on preceding lines.""",
        "pnach_output_label": "PNACH Output (Preview):",
        "convert_button": "Convert to PNACH",
        "save_as_button": "Save PNACH As...",
        "clear_button": "Clear Fields",
        "file_menu": "File",
        "options_menu": "Options",
        "language_menu": "Language",
        "help_menu": "Help",
        "exit_action": "Exit",
        "system_language_action": "System Language",
        "french_action": "French",
        "english_action": "English",
        "about_action": "About",
        "about_dialog_title": "About Pcsx2 Pnach Tool",
        "about_dialog_text": """Pcsx2 Pnach Tool (Tkinter version)

A simple tool to convert PS2 RAW codes to PNACH format.
Allows adding descriptions to codes.

Developed by: [Your Name/Paynssj4]
License: MIT License""",
        "no_input_warning_title": "No Input",
        "no_input_warning_text": "Please enter RAW codes.",
        "conversion_success_title": "Conversion Successful",
        "conversion_success_text": "RAW codes converted to PNACH format.",
        "no_valid_code_warning_title": "No Valid Codes",
        "no_valid_code_warning_text": "No valid RAW codes were found for conversion.",
        "no_valid_code_with_desc_text": "// {description} (No valid RAW code found after this description)",
        "no_code_to_export_warning_title": "Nothing to Export",
        "no_code_to_export_warning_text": "There is no PNACH data to export.",
        "game_name_input_dialog_title": "Game Name for PNACH",
        "game_name_input_dialog_label": "Enter the game title (e.g., My Game Title):",
        "export_cancelled_title": "Export Cancelled",
        "export_cancelled_no_name_text": "PNACH export cancelled (game name missing).",
        "game_crc_input_dialog_title": "Game CRC for PNACH",
        "game_crc_input_dialog_label": "Enter the 8-digit hexadecimal CRC of the game (e.g., A1B2C3D4):",
        "export_cancelled_no_crc_text": "PNACH export cancelled (CRC missing).",
        "invalid_crc_error_title": "Invalid CRC",
        "invalid_crc_error_text": "CRC must be an 8-character hexadecimal string.",
        "save_pnach_dialog_title": "Save PNACH file",
        "pnach_file_filter": "PNACH Files (*.pnach);;All Files (*.*)",
        "file_saved_success_title": "File Saved",
        "file_saved_success_text_tk": """PNACH file saved successfully:
{filepath}""",
        "save_error_title": "Save Error",
        "save_error_text": """Could not save PNACH file:
{error}""",
        "gametitle_default": "Game Name Here [SLUS_XXX.XX/SLES_XXX.XX]",
        "comment_default": "Codes converted by Pcsx2 Pnach Tool (Tk)"
    },
    "fr": {
        "window_title": "Pcsx2 Pnach Tool",
        "input_instructions_label": "Codes RAW et Descriptions (Optionnel) :",
        "input_instructions_text": """Entrez les codes RAW (XXXXXXXX YYYYYYYY) et/ou les descriptions.
Une ligne qui ne ressemble pas à un code RAW sera traitée comme une description pour le code suivant.
Exemple:
Max Argent
2030B968 FFFFFFFF
Vies Infinies
10123456 00000009""",
        "raw_input_placeholder_tk": """Collez vos codes RAW ici, un par ligne (ex: 20XXXXXX XXXXXXXX)
Vous pouvez ajouter des descriptions sur les lignes précédentes.""",
        "pnach_output_label": "Sortie PNACH (Prévisualisation) :",
        "convert_button": "Convertir en PNACH",
        "save_as_button": "Enregistrer PNACH sous...",
        "clear_button": "Effacer les champs",
        "file_menu": "Fichier",
        "options_menu": "Options",
        "language_menu": "Langue",
        "help_menu": "Aide",
        "exit_action": "Quitter",
        "system_language_action": "Langue du système",
        "french_action": "Français",
        "english_action": "Anglais",
        "about_action": "À propos",
        "about_dialog_title": "À propos de Pcsx2 Pnach Tool",
        "about_dialog_text": """Pcsx2 Pnach Tool (version Tkinter)

Un outil simple pour convertir les codes PS2 RAW au format PNACH.
Permet d'ajouter des descriptions aux codes.

Développé par : [Votre Nom/Paynssj4]
Licence : MIT License""",
        "no_input_warning_title": "Aucune entrée",
        "no_input_warning_text": "Veuillez entrer des codes RAW.",
        "conversion_success_title": "Conversion réussie",
        "conversion_success_text": "Codes RAW convertis au format PNACH.",
        "no_valid_code_warning_title": "Aucun code valide",
        "no_valid_code_warning_text": "Aucun code RAW valide n'a été trouvé pour la conversion.",
        "no_valid_code_with_desc_text": "// {description} (Aucun code RAW valide trouvé après cette description)",
        "no_code_to_export_warning_title": "Rien à exporter",
        "no_code_to_export_warning_text": "Il n'y a aucune donnée PNACH à exporter.",
        "game_name_input_dialog_title": "Nom du Jeu pour PNACH",
        "game_name_input_dialog_label": "Entrez le nom du jeu (ex: Mon Super Jeu):",
        "export_cancelled_title": "Exportation annulée",
        "export_cancelled_no_name_text": "Exportation PNACH annulée (nom du jeu manquant).",
        "game_crc_input_dialog_title": "CRC du Jeu pour PNACH",
        "game_crc_input_dialog_label": "Entrez le CRC hexadécimal à 8 chiffres du jeu (ex: A1B2C3D4):",
        "export_cancelled_no_crc_text": "Exportation PNACH annulée (CRC manquant).",
        "invalid_crc_error_title": "CRC Invalide",
        "invalid_crc_error_text": "Le CRC doit être une chaîne hexadécimale de 8 caractères.",
        "save_pnach_dialog_title": "Sauvegarder le fichier PNACH",
        "pnach_file_filter": "Fichiers PNACH (*.pnach);;Tous les fichiers (*.*)",
        "file_saved_success_title": "Fichier enregistré",
        "file_saved_success_text_tk": """Fichier PNACH sauvegardé avec succès :
{filepath}""",
        "save_error_title": "Erreur de Sauvegarde",
        "save_error_text": """Impossible de sauvegarder le fichier PNACH :
{error}""",
        "gametitle_default": "Nom du Jeu Ici [SLUS_XXX.XX/SLES_XXX.XX]",
        "comment_default": "Codes convertis par Pcsx2 Pnach Tool (Tk)"
    }
}

# Langue actuelle (sera définie par l'application au démarrage)
CURRENT_LANG = "en"

def get_text(key, **kwargs):
    lang_dict = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS["en"])
    text = lang_dict.get(key)

    if text is None and CURRENT_LANG != "en":
        text = TRANSLATIONS["en"].get(key, key)
    elif text is None and CURRENT_LANG == "en":
        text = key

    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text
