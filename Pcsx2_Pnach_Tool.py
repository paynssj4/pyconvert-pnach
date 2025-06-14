"""
PyConvert Pnacher: Outil de conversion de codes RAW PS2 en format PNACH.
"""
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTextEdit, QPushButton, QMessageBox, QFileDialog, QInputDialog, QGroupBox,
    QMenuBar
)
from PySide6.QtGui import QAction, QPalette, QColor, QIcon
from PySide6.QtCore import Qt, QLocale
import sys
import os
import locale
from translations import TRANSLATIONS

class PyConvertPnacher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_language = self._get_system_language()
        self._is_system_language_selected = True
        self.setWindowIcon(QIcon("Pcsx2 Pnach Tool.ico"))
        self.setMinimumSize(700, 500)
        self._apply_dark_theme()
        self._init_ui()
        self.current_pnach_items = []

    def _apply_dark_theme(self):
        app = QApplication.instance()
        if not app:
            pass 
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

        self._create_menubar()

        self.input_group = QGroupBox() 
        input_layout = QVBoxLayout(self.input_group)
        self.input_instructions = QLabel() 
        self.input_instructions.setWordWrap(True)
        input_layout.addWidget(self.input_instructions)
        self.txt_raw_input = QTextEdit()
        input_layout.addWidget(self.txt_raw_input)
        main_layout.addWidget(self.input_group)

        self.pnach_group = QGroupBox() 
        pnach_layout = QVBoxLayout(self.pnach_group)
        self.txt_pnach_output = QTextEdit()
        self.txt_pnach_output.setReadOnly(True)
        pnach_layout.addWidget(self.txt_pnach_output)
        main_layout.addWidget(self.pnach_group)

        btn_layout = QHBoxLayout()
        self.btn_convert = QPushButton() 
        self.btn_convert.clicked.connect(self.process_conversion)
        btn_layout.addWidget(self.btn_convert)

        self.btn_clear = QPushButton() 
        self.btn_clear.clicked.connect(self.clear_fields)
        btn_layout.addWidget(self.btn_clear)
        
        main_layout.addLayout(btn_layout)
        self.setCentralWidget(central_widget)
        self._update_ui_texts()

    def _get_system_language(self):
        try:
            q_locale = QLocale.system().name() 
            lang_code = q_locale.split('_')[0]
            if lang_code in TRANSLATIONS:
                return lang_code
        except Exception:
            pass 

        try:
            lang_code, _ = locale.getdefaultlocale() 
            if lang_code:
                lang_code = lang_code.split('_')[0]
                if lang_code in TRANSLATIONS:
                    return lang_code
        except Exception:
            pass 
        return "en"

    def _translate(self, key, **kwargs):
        return TRANSLATIONS.get(self.current_language, TRANSLATIONS["en"]).get(key, key).format(**kwargs)

    def _create_menubar(self):
        menubar = self.menuBar()
        
        self.file_menu = menubar.addMenu("")
        self.export_action = QAction("", self)
        self.export_action.triggered.connect(self.export_to_pnach)
        self.export_action.setEnabled(False)
        self.file_menu.addAction(self.export_action)
        self.exit_action = QAction("", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.options_menu = menubar.addMenu("")
        self.language_menu = self.options_menu.addMenu("")

        self.system_lang_action = QAction("", self)
        self.system_lang_action.setCheckable(True)
        self.system_lang_action.triggered.connect(lambda: self._set_language(self._get_system_language(), is_system=True))
        self.language_menu.addAction(self.system_lang_action)

        self.french_action = QAction("", self)
        self.french_action.setCheckable(True)
        self.french_action.triggered.connect(lambda: self._set_language("fr"))
        self.language_menu.addAction(self.french_action)

        self.english_action = QAction("", self)
        self.english_action.setCheckable(True)
        self.english_action.triggered.connect(lambda: self._set_language("en"))
        self.language_menu.addAction(self.english_action)
        
        self.help_menu = menubar.addMenu("")
        self.about_action = QAction("", self)
        self.about_action.triggered.connect(self.show_about_dialog)
        self.help_menu.addAction(self.about_action)

        self._update_language_actions_checked_state()


    def _update_language_actions_checked_state(self):
        self.system_lang_action.setChecked(False)
        self.french_action.setChecked(False)
        self.english_action.setChecked(False)

        system_lang_code = self._get_system_language()
        if self.current_language == system_lang_code and self._is_system_language_selected:
             self.system_lang_action.setChecked(True)
        elif self.current_language == "fr":
            self.french_action.setChecked(True)
        elif self.current_language == "en":
            self.english_action.setChecked(True)
        else: 
            if system_lang_code in ["fr", "en"]:
                 if system_lang_code == "fr": self.french_action.setChecked(True)
                 else: self.english_action.setChecked(True)
            else:
                 self.english_action.setChecked(True)


    def _set_language(self, lang_code, is_system=False):
        if is_system:
            self._is_system_language_selected = True
            actual_lang_to_set = self._get_system_language()
        else:
            self._is_system_language_selected = False
            actual_lang_to_set = lang_code

        if actual_lang_to_set in TRANSLATIONS:
            self.current_language = actual_lang_to_set
        else: 
            self.current_language = "en"
            if is_system and actual_lang_to_set not in TRANSLATIONS:
                self._is_system_language_selected = True 
            else:
                self._is_system_language_selected = False

        self._update_ui_texts()
        self._update_language_actions_checked_state()


    def _update_ui_texts(self):
        self.setWindowTitle(self._translate("window_title"))
        
        self.file_menu.setTitle(self._translate("file_menu"))
        self.export_action.setText(self._translate("export_pnach_action"))
        self.exit_action.setText(self._translate("exit_action"))
        
        self.options_menu.setTitle(self._translate("options_menu"))
        self.language_menu.setTitle(self._translate("language_menu"))
        self.system_lang_action.setText(self._translate("system_language_action"))
        self.french_action.setText(self._translate("french_action"))
        self.english_action.setText(self._translate("english_action"))

        self.help_menu.setTitle(self._translate("help_menu"))
        self.about_action.setText(self._translate("about_action"))

        self.input_group.setTitle(self._translate("input_group_title"))
        self.input_instructions.setText(self._translate("input_instructions"))
        self.txt_raw_input.setPlaceholderText(self._translate("raw_input_placeholder"))
        self.pnach_group.setTitle(self._translate("pnach_group_title"))

        self.btn_convert.setText(self._translate("convert_button"))
        self.btn_clear.setText(self._translate("clear_button"))
        

    def process_conversion(self):
        raw_input_text = self.txt_raw_input.toPlainText().strip()
        self.current_pnach_items = []
        self.txt_pnach_output.clear()
        self.export_action.setEnabled(False)

        if not raw_input_text:
            QMessageBox.warning(self, self._translate("no_input_warning_title"), self._translate("no_input_warning_text"))
            return

        input_lines = raw_input_text.splitlines()
        pnach_output_lines = [
            f"gametitle={self._translate('gametitle_default')}",
            f"comment={self._translate('comment_default')}",
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
            self.export_action.setEnabled(True)
            QMessageBox.information(self, self._translate("conversion_success_title"), self._translate("conversion_success_text"))
        else:
            if current_description:
                 self.txt_pnach_output.setPlainText(self._translate("no_valid_code_with_desc_text", description=current_description))
            QMessageBox.warning(self, self._translate("no_valid_code_warning_title"), self._translate("no_valid_code_warning_text"))

    def export_to_pnach(self):
        if not self.current_pnach_items:
            QMessageBox.warning(self, self._translate("no_code_to_export_warning_title"), self._translate("no_code_to_export_warning_text"))
            return

        game_title_input, ok_title = QInputDialog.getText(self, self._translate("game_name_input_dialog_title"), 
                                                          self._translate("game_name_input_dialog_label"))
        if not ok_title or not game_title_input.strip():
            QMessageBox.information(self, self._translate("export_cancelled_title"), self._translate("export_cancelled_no_name_text"))
            return

        game_crc_input, ok_crc = QInputDialog.getText(self, self._translate("game_crc_input_dialog_title"), 
                                                      self._translate("game_crc_input_dialog_label"))
        if not ok_crc or not game_crc_input.strip():
            QMessageBox.information(self, self._translate("export_cancelled_title"), self._translate("export_cancelled_no_crc_text"))
            return

        game_crc_cleaned = game_crc_input.strip().upper()
        if not (len(game_crc_cleaned) == 8 and all(c in "0123456789ABCDEF" for c in game_crc_cleaned)):
            QMessageBox.critical(self, self._translate("invalid_crc_error_title"), self._translate("invalid_crc_error_text"))
            return

        pnach_content_lines = [f"gametitle={game_title_input.strip()}"]
        pnach_content_lines.append(self._translate("comment_default"))
        pnach_content_lines.append("")

        for desc, addr, val in self.current_pnach_items:
            if desc:
                pnach_content_lines.append(f"// {desc}")
            pnach_content_lines.append(f"patch=1,EE,{addr},extended,{val}") 

        filepath, _ = QFileDialog.getSaveFileName(
            self, 
            self._translate("save_pnach_dialog_title"),
            f"{game_crc_cleaned}.pnach",
            self._translate("pnach_file_filter")
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(pnach_content_lines))
                QMessageBox.information(self, self._translate("file_saved_success_title"), self._translate("file_saved_success_text", filepath=filepath))
            except Exception as e:
                QMessageBox.critical(self, self._translate("save_error_title"), self._translate("save_error_text", error=e))

    def clear_fields(self):
        self.txt_raw_input.clear()
        self.txt_pnach_output.clear()
        self.current_pnach_items = []
        self.export_action.setEnabled(False)

    def show_about_dialog(self):
        QMessageBox.about(self, self._translate("about_dialog_title"), self._translate("about_dialog_text"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        print("Warning: Could not set system default locale.") 
    win = PyConvertPnacher()
    win.show()
    sys.exit(app.exec())