import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
import translations_tk
import locale
import os # Ajouté pour la compatibilité potentielle de l'icône

DARK_BG = "#2E2E2E"
DARK_FG = "#FFFFFF"
DARK_INSERT_BG = "#3E3E3E"
DARK_BUTTON_BG = "#555555"
DARK_BUTTON_FG = "#FFFFFF"
DARK_SELECT_BG = "#4A4A4A"

class Pcsx2PnachToolTk(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.current_language = self._get_system_language()
        translations_tk.CURRENT_LANG = self.current_language
        self._is_system_language_selected = True

        self._apply_dark_theme()

        self.title(translations_tk.get_text("window_title"))
        self.geometry("700x600")
        
        # Assurez-vous que le nom du fichier d'icône ici correspond EXACTEMENT
        # au nom de votre fichier .ico dans le même répertoire que le script.
        # L'erreur précédente indiquait "Pcsx2_Pnach_Tool.ico" (avec underscores).
        icon_path = "Pcsx2_Pnach_Tool.ico" 
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except tk.TclError:
                print(f"Avertissement : Impossible de charger l'icône '{icon_path}'. Format non supporté ou fichier corrompu.")
        else:
            print(f"Avertissement : Fichier d'icône '{icon_path}' non trouvé.")

        self.current_pnach_items = [] # Initialisation avant _update_ui_texts

        self._create_menubar()
        self.create_widgets() # Crée les widgets avant de mettre à jour leurs textes
        self._update_ui_texts() # Met à jour les textes après la création
        
        # self.update_save_as_state() est déjà appelé à la fin de _update_ui_texts

    def _apply_dark_theme(self):
        self.configure(bg=DARK_BG)
        style = ttk.Style(self)
        try:
            current_theme = style.theme_use()
            if 'clam' in style.theme_names():
                style.theme_use('clam')
            elif 'vista' in style.theme_names() and os.name == 'nt': 
                style.theme_use('vista')
        except tk.TclError:
            print("Avertissement : Problème lors de la tentative de changement de thème ttk. Utilisation du thème par défaut.")

        style.configure('.', background=DARK_BG, foreground=DARK_FG, fieldbackground=DARK_INSERT_BG)
        style.configure('TFrame', background=DARK_BG)
        style.configure('TLabel', background=DARK_BG, foreground=DARK_FG)
        style.configure('TButton', background=DARK_BUTTON_BG, foreground=DARK_BUTTON_FG, borderwidth=1)
        style.map('TButton',
            background=[('active', DARK_SELECT_BG), ('pressed', DARK_SELECT_BG)],
            foreground=[('active', DARK_BUTTON_FG)])
        style.configure('TEntry', fieldbackground=DARK_INSERT_BG, foreground=DARK_FG, insertcolor=DARK_FG)
        style.configure('TScrollbar', background=DARK_BUTTON_BG, troughcolor=DARK_BG, arrowcolor=DARK_FG)
        
        # Pour les menus tk standard (non-ttk)
        # Commenter toutes les options globales pour les menus pour éviter les conflits
        # self.option_add('*Menu.background', DARK_BUTTON_BG)
        # self.option_add('*Menu.foreground', DARK_FG)
        # self.option_add('*Menu.activeBackground', DARK_SELECT_BG)
        # self.option_add('*Menu.activeForeground', DARK_FG)
        # self.option_add('*Menu.disabledForeground', '#888888')

    def _get_system_language(self):
        try:
            lang_code, _ = locale.getdefaultlocale() 
            if lang_code:
                lang_code = lang_code.split('_')[0]
                if lang_code in translations_tk.TRANSLATIONS:
                    return lang_code
        except Exception:
            pass
        return "en" 

    def _create_menubar(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=translations_tk.get_text("file_menu"), menu=self.file_menu)
        self.file_menu.add_command(label=translations_tk.get_text("save_as_button"), command=self.save_as_file)
        self.file_menu.add_separator() 
        self.file_menu.add_command(label=translations_tk.get_text("exit_action"), command=self.quit)

        options_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=translations_tk.get_text("options_menu"), menu=options_menu)
        
        self.language_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label=translations_tk.get_text("language_menu"), menu=self.language_menu)
        
        self.lang_var = tk.StringVar(value=self.current_language)
        system_lang_val = self._get_system_language() 

        self.language_menu.add_radiobutton(
            label=translations_tk.get_text("system_language_action"), variable=self.lang_var, 
            value=system_lang_val, 
            command=lambda: self._set_language(system_lang_val, is_system=True)
        )
        self.language_menu.add_radiobutton(
            label=translations_tk.get_text("french_action"), variable=self.lang_var, value="fr", 
            command=lambda: self._set_language("fr")
        )
        self.language_menu.add_radiobutton(
            label=translations_tk.get_text("english_action"), variable=self.lang_var, value="en", 
            command=lambda: self._set_language("en")
        )
        self._update_language_menu_radio_state()

        self.help_menu = tk.Menu(self.menubar, tearoff=0) 
        self.menubar.add_cascade(label=translations_tk.get_text("help_menu"), menu=self.help_menu)
        self.help_menu.add_command(label=translations_tk.get_text("about_action"), command=self.show_about_dialog)

    def _update_language_menu_radio_state(self):
        system_lang_code = self._get_system_language()
        if self._is_system_language_selected:
            self.lang_var.set(system_lang_code) 
        else:
            self.lang_var.set(self.current_language)

    def _set_language(self, lang_code, is_system=False):
        if is_system:
            self._is_system_language_selected = True
            actual_lang_to_set = self._get_system_language()
        else:
            self._is_system_language_selected = False
            actual_lang_to_set = lang_code

        if actual_lang_to_set in translations_tk.TRANSLATIONS:
            translations_tk.CURRENT_LANG = actual_lang_to_set
            self.current_language = actual_lang_to_set
        else: 
            translations_tk.CURRENT_LANG = "en" 
            self.current_language = "en"
            if is_system:
                 self._is_system_language_selected = True
            else: 
                 self._is_system_language_selected = False

        self._update_ui_texts()
        self._update_language_menu_radio_state()

    def _update_ui_texts(self):
        self.title(translations_tk.get_text("window_title"))
        
        try:
            self.menubar.entryconfig(0, label=translations_tk.get_text("file_menu"))
            self.menubar.entryconfig(1, label=translations_tk.get_text("options_menu"))
            self.menubar.entryconfig(2, label=translations_tk.get_text("help_menu"))
        except tk.TclError as e:
            print(f"Avertissement : Impossible de mettre à jour les labels de la barre de menu principale : {e}")

        self.file_menu.entryconfig(0, label=translations_tk.get_text("save_as_button"))
        self.file_menu.entryconfig(2, label=translations_tk.get_text("exit_action"))

        options_menu_widget = self.menubar.nametowidget(self.menubar.entrycget(1, "menu"))
        if options_menu_widget:
             options_menu_widget.entryconfig(0, label=translations_tk.get_text("language_menu"))

        self.language_menu.entryconfig(0, label=translations_tk.get_text("system_language_action"))
        self.language_menu.entryconfig(1, label=translations_tk.get_text("french_action"))
        self.language_menu.entryconfig(2, label=translations_tk.get_text("english_action"))

        if self.help_menu: 
            self.help_menu.entryconfig(0, label=translations_tk.get_text("about_action"))

        if hasattr(self, 'input_label'):
            self.input_label.config(text=translations_tk.get_text("cheat_codes_label"))
        if hasattr(self, 'output_label'):
            self.output_label.config(text=translations_tk.get_text("pnach_output_label"))
        if hasattr(self, 'convert_button'):
            self.convert_button.config(text=translations_tk.get_text("convert_button"))
        if hasattr(self, 'clear_button'):
            self.clear_button.config(text=translations_tk.get_text("clear_button"))
        
        self.update_save_as_state() 

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        self.input_label = ttk.Label(main_frame, text=translations_tk.get_text("cheat_codes_label"))
        self.input_label.pack(pady=(0,5), anchor="w")

        self.input_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, relief=tk.FLAT, bd=2)
        self.input_text.pack(expand=True, fill=tk.BOTH, pady=(0,10))
        self.input_text.configure(bg=DARK_INSERT_BG, fg=DARK_FG, insertbackground=DARK_FG, selectbackground=DARK_SELECT_BG)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0,10))

        self.convert_button = ttk.Button(button_frame, text=translations_tk.get_text("convert_button"), command=self.convert_input)
        self.convert_button.pack(side=tk.LEFT, padx=(0,5))

        self.clear_button = ttk.Button(button_frame, text=translations_tk.get_text("clear_button"), command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=(0,5))
        
        self.output_label = ttk.Label(main_frame, text=translations_tk.get_text("pnach_output_label"))
        self.output_label.pack(pady=(0,5), anchor="w")

        self.output_text = scrolledtext.ScrolledText(main_frame, height=15, width=80, state=tk.DISABLED, relief=tk.FLAT, bd=2)
        self.output_text.pack(expand=True, fill=tk.BOTH)
        self.output_text.configure(bg=DARK_INSERT_BG, fg=DARK_FG, selectbackground=DARK_SELECT_BG)

    def convert_input(self):
        raw_input_text = self.input_text.get("1.0", tk.END).strip()
        
        self.current_pnach_items = [] 
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        if not raw_input_text:
            messagebox.showwarning(
                translations_tk.get_text("no_input_warning_title"), 
                translations_tk.get_text("no_input_warning_text"),
                parent=self
            )
            self.output_text.config(state=tk.DISABLED)
            self.update_save_as_state()
            return

        input_lines = raw_input_text.splitlines()
        current_description = None
        temp_pnach_output_lines = [] 

        for line in input_lines:
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
                self.current_pnach_items.append({"desc": current_description, "addr": addr_hex, "val": val_hex})
                if current_description:
                    temp_pnach_output_lines.append(f"// {current_description}")
                temp_pnach_output_lines.append(f"patch=1,EE,{addr_hex},extended,{val_hex}") 
                current_description = None
            else:
                current_description = cleaned_line 

        if self.current_pnach_items:
            self.output_text.insert("1.0", "\n".join(temp_pnach_output_lines))
            messagebox.showinfo(
                translations_tk.get_text("conversion_success_title"), 
                translations_tk.get_text("conversion_success_text"),
                parent=self
            )
        else:
            msg_if_no_code = translations_tk.get_text("no_valid_code_warning_text")
            if current_description:
                 msg_if_no_code = translations_tk.get_text("no_valid_code_with_desc_text", description=current_description)
                 self.output_text.insert("1.0", msg_if_no_code) 
            
            messagebox.showwarning(
                translations_tk.get_text("no_valid_code_warning_title"),
                translations_tk.get_text("no_valid_code_warning_text") if not current_description else msg_if_no_code,
                parent=self
            )
        
        self.output_text.config(state=tk.DISABLED)
        self.update_save_as_state()

    def save_as_file(self):
        if not self.current_pnach_items:
            messagebox.showwarning(
                translations_tk.get_text("no_code_to_export_warning_title"), 
                translations_tk.get_text("no_code_to_export_warning_text"), 
                parent=self
            )
            return

        game_title = simpledialog.askstring(
            translations_tk.get_text("game_name_input_dialog_title"), 
            translations_tk.get_text("game_name_input_dialog_label"),
            parent=self
        )
        if not game_title: 
            messagebox.showinfo(
                translations_tk.get_text("export_cancelled_title"), 
                translations_tk.get_text("export_cancelled_no_name_text"), 
                parent=self
            )
            return

        game_crc = simpledialog.askstring(
            translations_tk.get_text("game_crc_input_dialog_title"),
            translations_tk.get_text("game_crc_input_dialog_label"),
            parent=self
        )
        if not game_crc: 
            messagebox.showinfo(
                translations_tk.get_text("export_cancelled_title"), 
                translations_tk.get_text("export_cancelled_no_crc_text"), 
                parent=self
            )
            return
        
        game_crc = game_crc.strip().upper()
        if not (len(game_crc) == 8 and all(c in "0123456789ABCDEF" for c in game_crc)):
            messagebox.showerror(
                translations_tk.get_text("invalid_crc_error_title"), 
                translations_tk.get_text("invalid_crc_error_text"), 
                parent=self
            )
            return
        
        pnach_content = f"gametitle={game_title.strip()}\ncomment={translations_tk.get_text('comment_default')}\n\n"
        for item in self.current_pnach_items:
            desc_comment = f"// {item['desc']}" if item['desc'] else ""
            pnach_content += f"patch=1,EE,{item['addr']},extended,{item['val']} {desc_comment}\n"

        suggested_filename = f"{game_crc}.pnach"
        
        try:
            pnach_filter_text = translations_tk.get_text("pnach_file_filter").split(';;')[0].split('(')[0].strip()
            all_files_text = translations_tk.get_text("all_files_filter_tk")
        except Exception: 
            pnach_filter_text = "PNACH files"
            all_files_text = "All files"

        file_types_list = [
            (pnach_filter_text, "*.pnach"),
            (all_files_text, "*.*") 
        ]

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pnach",
            filetypes=file_types_list,
            initialfile=suggested_filename,
            title=translations_tk.get_text("save_pnach_dialog_title"),
            parent=self
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(pnach_content)
                
                success_msg_key = "file_saved_success_text_tk" 
                msg = translations_tk.get_text(success_msg_key, filepath=filepath)
                if msg == success_msg_key: 
                    msg = translations_tk.get_text("file_saved_success") + f"\n({filepath})"

                messagebox.showinfo(
                    translations_tk.get_text("file_saved_success_title"), 
                    msg, 
                    parent=self
                )
            except Exception as e:
                messagebox.showerror(
                    translations_tk.get_text("save_error_title"), 
                    translations_tk.get_text("save_error_text", error=str(e)), 
                    parent=self
                )
    
    def clear_fields(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.current_pnach_items = []
        self.update_save_as_state()

    def show_about_dialog(self):
        about_title = translations_tk.get_text("about_dialog_title")
        about_message = translations_tk.get_text("about_dialog_text")
        messagebox.showinfo(about_title, about_message, parent=self)

    def update_save_as_state(self):
        if hasattr(self, 'file_menu'): 
            if self.current_pnach_items:
                self.file_menu.entryconfig(0, state=tk.NORMAL)
            else:
                self.file_menu.entryconfig(0, state=tk.DISABLED)

if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_ALL, '')  
    except locale.Error as e:
        print(f"Avertissement : Impossible de définir la locale système par défaut : {e}")
        print("La détection de la langue système pourrait ne pas fonctionner comme prévu.")

    app = Pcsx2PnachToolTk()
    app.mainloop()
