"""
PyConvert Pnacher: Outil de conversion de codes RAW PS2 en format PNACH.
"""
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox, QFileDialog, QInputDialog, QGroupBox,
    QMenuBar
)
from PySide6.QtGui import QAction, QPalette, QColor
from PySide6.QtCore import Qt
import sys
import os

class PyConvertPnacher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyConvert Pnacher")
        self.setMinimumSize(700, 500)
        self._apply_dark_theme()
        self._init_ui()
        self.current_pnach_items = []

    def _apply_dark_theme(self):
        app = QApplication.instance()
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(45, 45, 45))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(60, 120, 200))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)

    def _init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("&Fichier")

        export_action = QAction("&Exporter PNACH...", self)
        export_action.triggered.connect(self.export_to_pnach)
        self.export_action_ref = export_action
        self.export_action_ref.setEnabled(False)
        file_menu.addAction(export_action)

        exit_action = QAction("&Quitter", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("&Aide")
        about_action = QAction("À &propos", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

        input_group = QGroupBox("Codes RAW et Descriptions (Optionnel)")
        input_layout = QVBoxLayout(input_group)
        input_instructions = QLabel("Entrez les codes RAW (XXXXXXXX YYYYYYYY) et/ou les descriptions.\n"
                                    "Une ligne qui ne ressemble pas à un code RAW sera traitée comme une description pour le code suivant.\n"
                                    "Exemple:\n"
                                    "// Max Argent\n"
                                    "2030B968 FFFFFFFF\n"
                                    "// Vies Infinies\n"
                                    "10123456 00000009")
        input_instructions.setWordWrap(True)
        input_layout.addWidget(input_instructions)
        self.txt_raw_input = QTextEdit()
        self.txt_raw_input.setPlaceholderText("Collez vos codes RAW ici, un par ligne (ex: 20XXXXXX XXXXXXXX)\n"
                                             "Vous pouvez ajouter des descriptions sur les lignes précédentes.")
        input_layout.addWidget(self.txt_raw_input)
        main_layout.addWidget(input_group)

        pnach_group = QGroupBox("Format PNACH (Prévisualisation)")
        pnach_layout = QVBoxLayout(pnach_group)
        self.txt_pnach_output = QTextEdit()
        self.txt_pnach_output.setReadOnly(True)
        pnach_layout.addWidget(self.txt_pnach_output)
        main_layout.addWidget(pnach_group)

        btn_layout = QHBoxLayout()
        self.btn_convert = QPushButton("Convertir en PNACH")
        self.btn_convert.clicked.connect(self.process_conversion)
        btn_layout.addWidget(self.btn_convert)

        self.btn_clear = QPushButton("Effacer")
        self.btn_clear.clicked.connect(self.clear_fields)
        btn_layout.addWidget(self.btn_clear)
        
        main_layout.addLayout(btn_layout)
        self.setCentralWidget(central_widget)

    def process_conversion(self):
        raw_input_text = self.txt_raw_input.toPlainText().strip()
        self.current_pnach_items = []
        self.txt_pnach_output.clear()
        self.export_action_ref.setEnabled(False)

        if not raw_input_text:
            QMessageBox.warning(self, "Aucune entrée", "Veuillez entrer des codes RAW.")
            return

        input_lines = raw_input_text.splitlines()
        pnach_output_lines = [
            "gametitle=Nom du Jeu Ici [SLUS_XXX.XX/SLES_XXX.XX]",
            "comment=Codes convertis par PyConvert Pnacher",
            ""
        ]
        
        current_description = None

        for line_num, line in enumerate(input_lines, 1):
            cleaned_line = line.strip()
            if not cleaned_line:
                continue

            parts = cleaned_line.split()
            is_valid_raw_code = False
            addr_hex, val_hex = "", ""

            if len(parts) == 2:
                try:
                    if len(parts[0]) == 8 and len(parts[1]) == 8:
                        int(parts[0], 16) 
                        int(parts[1], 16)
                        addr_hex = parts[0].upper()
                        val_hex = parts[1].upper()
                        is_valid_raw_code = True
                except ValueError:
                    is_valid_raw_code = False
            
            if is_valid_raw_code:
                self.current_pnach_items.append((current_description, addr_hex, val_hex))
                if current_description:
                    pnach_output_lines.append(f"// {current_description}")
                pnach_output_lines.append(f"patch=1,EE,{addr_hex},{val_hex}")
                current_description = None
            else:
                current_description = cleaned_line 

        if self.current_pnach_items:
            self.txt_pnach_output.setPlainText("\n".join(pnach_output_lines))
            self.export_action_ref.setEnabled(True)
            QMessageBox.information(self, "Conversion Réussie", "Codes RAW convertis au format PNACH.")
        else:
            if current_description:
                 self.txt_pnach_output.setPlainText(f"// {current_description} (Aucun code RAW valide trouvé après cette description)")
            QMessageBox.warning(self, "Aucun code valide", "Aucun code RAW valide n'a été trouvé pour la conversion.")

    def export_to_pnach(self):
        if not self.current_pnach_items:
            QMessageBox.warning(self, "Aucun code", "Aucun code PNACH à exporter.")
            return

        game_title_input, ok_title = QInputDialog.getText(self, "Nom du Jeu pour PNACH", 
                                                          "Entrez le crc du jeu (ex: B54C0319):")
        if not ok_title or not game_title_input.strip():
            QMessageBox.information(self, "Annulé", "Exportation PNACH annulée (nom du jeu manquant).")
            return

        game_crc_input, ok_crc = QInputDialog.getText(self, "CRC du Jeu pour PNACH", 
                                                      "Entrez le CRC hexadécimal à 8 chiffres du jeu (ex: A1B2C3D4):")
        if not ok_crc or not game_crc_input.strip():
            QMessageBox.information(self, "Annulé", "Exportation PNACH annulée (CRC manquant).")
            return

        game_crc_cleaned = game_crc_input.strip().upper()
        if not (len(game_crc_cleaned) == 8 and all(c in "0123456789ABCDEF" for c in game_crc_cleaned)):
            QMessageBox.critical(self, "CRC Invalide", "Le CRC doit être une chaîne hexadécimale de 8 caractères.")
            return

        pnach_content_lines = [f"gametitle={game_title_input.strip()}"]
        pnach_content_lines.append("comment=Codes convertis par PyConvert Pnacher")
        pnach_content_lines.append("")

        for desc, addr, val in self.current_pnach_items:
            if desc:
                pnach_content_lines.append(f"// {desc}")
            pnach_content_lines.append(f"patch=1,EE,{addr},extended,{val}") 

        filepath, _ = QFileDialog.getSaveFileName(
            self, 
            "Sauvegarder le fichier PNACH", 
            f"{game_crc_cleaned}.pnach",
            "Fichiers PNACH (*.pnach);;Tous les fichiers (*)"
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(pnach_content_lines))
                QMessageBox.information(self, "Succès", f"Fichier PNACH sauvegardé avec succès:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur de Sauvegarde", f"Impossible de sauvegarder le fichier PNACH:\n{e}")

    def clear_fields(self):
        self.txt_raw_input.clear()
        self.txt_pnach_output.clear()
        self.current_pnach_items = []
        self.export_action_ref.setEnabled(False)

    def show_about_dialog(self):
        about_text = (
            "PyConvert Pnacher\n\n"
            "Un outil simple pour convertir les codes PS2 RAW au format PNACH.\n"
            "Portage en Python de concepts issus de PCSX2CE (PCSX2 Cheat Editor).\n\n"
            "Développé par : [Paynssj4]\n"
            "Licence : MIT License\n\n"
            "Ce logiciel est fourni sans garantie."
        )
        QMessageBox.about(self, "À propos de PyConvert Pnacher", about_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PyConvertPnacher()
    win.show()
    sys.exit(app.exec())