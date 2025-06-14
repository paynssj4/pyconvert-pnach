import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
import os
import locale
import translations_tk # Assurez-vous que translations_tk.py est dans le même répertoire

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
        self.geometry("700x650") # Augmenté légèrement la hauteur pour les instructions
        
        icon_path = "Pcsx2_Pnach_Tool.ico" 
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except tk.TclError:
                print(f"Avertissement : Impossible de charger l'icône {icon_path}. Assurez-vous que c'est un format .ico valide.")
        else:
            print(f"Avertissement : Fichier d'icône {icon_path} non trouvé.")

        self.current_pnach_items = []

        self._create_menubar()
        self.create_widgets() 
        self._update_ui_texts() 
        
    def _apply_dark_theme(self):
        self.configure(bg=DARK_BG)
        style = ttk.Style(self)
        try:
            style.theme_use('clam') 
        except tk.TclError:
            print("Avertissement : Le thème 'clam' n'est pas disponible, utilisation du thème par défaut.")

        style.configure('.', background=DARK_BG, foreground=DARK_FG, fieldbackground=DARK_INSERT_BG)
        style.configure('TFrame', background=DARK_BG)
        style.configure('TLabel', background=DARK_BG, foreground=DARK_FG)
        style.configure('TButton', background=DARK_BUTTON_BG, foreground=DARK_BUTTON_FG, borderwidth=1)
        style.map('TButton',
            background=[('active', DARK_SELECT_BG), ('pressed', DARK_SELECT_BG)],
            foreground=[('active', DARK_BUTTON_FG)])
        style.configure('TEntry', fieldbackground=DARK_INSERT_BG, foreground=DARK_FG, insertcolor=DARK_FG)
        style.configure('TScrollbar', background=DARK_BUTTON_BG, troughcolor=DARK_BG, arrowcolor=DARK_FG)
        style.configure('TLabelframe', background=DARK_BG, foreground=DARK_FG, bordercolor=DARK_FG)
        style.configure('TLabelframe.Label', background=DARK_BG, foreground=DARK_FG)


    def _get_system_language(self):
        try:
            # Utiliser locale.getlocale() après setlocale pour une approche plus moderne
            current_locale_tuple = locale.getlocale(locale.LC_CTYPE) # Ou locale.getlocale()
            if current_locale_tuple and current_locale_tuple[0]:
                lang_code = current_locale_tuple[0].split('_')[0]
                if lang_code in translations_tk.TRANSLATIONS: 
                    return lang_code
        except Exception:
            pass 
        return "en" # Langue par défaut

    def _create_menubar(self):
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        # Définir le label initialement ici
        self.menubar.add_cascade(label=translations_tk.get_text("file_menu"), menu=self.file_menu)
        self.file_menu.add_command(label="", command=self.save_as_file, state="disabled") # Label et état mis à jour plus tard
        self.file_menu.add_separator() 
        self.file_menu.add_command(label="", command=self.quit) # Label mis à jour plus tard

        options_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label=translations_tk.get_text("options_menu"), menu=options_menu) # Définir le label initialement ici
        
        self.language_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label=translations_tk.get_text("language_menu"), menu=self.language_menu) # Définir le label initialement ici
        
        self.lang_var = tk.StringVar(value=self.current_language)
        system_lang_val = self._get_system_language() 

        self.language_menu.add_radiobutton(
            label=translations_tk.get_text("system_language_action"), variable=self.lang_var, # Définir le label initialement ici
            value=system_lang_val, 
            command=lambda: self._set_language(system_lang_val, is_system=True)
        )
        self.language_menu.add_radiobutton(
            label=translations_tk.get_text("french_action"), variable=self.lang_var, value="fr", # Définir le label initialement ici
            command=lambda: self._set_language("fr")
        )
        self.language_menu.add_radiobutton(
            label=translations_tk.get_text("english_action"), variable=self.lang_var, value="en", # Définir le label initialement ici
            command=lambda: self._set_language("en")
        )
        self._update_language_menu_radio_state()

        self.help_menu = tk.Menu(self.menubar, tearoff=0) 
        self.menubar.add_cascade(label=translations_tk.get_text("help_menu"), menu=self.help_menu) # Définir le label initialement ici
        self.help_menu.add_command(label=translations_tk.get_text("about_action"), command=self.show_about_dialog) # Définir le label initialement ici

    def _update_language_menu_radio_state(self):
        system_lang_code = self._get_system_language()
        if self._is_system_language_selected:
             self.lang_var.set(system_lang_code)
        else:
            self.lang_var.set(self.current_language)

    def _set_language(self, lang_code, is_system=False):
        actual_lang_to_set = lang_code
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
            # Si la langue système n'est pas supportée, on reste sur 'en' mais on garde la sélection "système"
            if is_system and actual_lang_to_set not in translations_tk.TRANSLATIONS:
                 self._is_system_language_selected = True
            else:
                 self._is_system_language_selected = False


        self._update_ui_texts()
        self._update_language_menu_radio_state()

    def _update_ui_texts(self):
        self.title(translations_tk.get_text("window_title"))
        
        # Mise à jour des labels des menus
        # Utiliser les indices numériques directs (0, 1, 2) pour les cascades principales
        try:
            self.menubar.entryconfig(0, label=translations_tk.get_text("file_menu")) # Fichier
            self.menubar.entryconfig(1, label=translations_tk.get_text("options_menu"))# Options
            self.menubar.entryconfig(2, label=translations_tk.get_text("help_menu"))   # Aide
        except tk.TclError as e:
            # Ce try-except est un contournement si le theming cause toujours des conflits
            print(f"Avertissement : Impossible de mettre à jour les labels de la barre de menu principale : {e}")

        self.file_menu.entryconfig(0, label=translations_tk.get_text("save_as_button"))
        self.file_menu.entryconfig(2, label=translations_tk.get_text("exit_action"))

        self.language_menu.entryconfig(0, label=translations_tk.get_text("system_language_action"))
        self.language_menu.entryconfig(1, label=translations_tk.get_text("french_action"))
        self.language_menu.entryconfig(2, label=translations_tk.get_text("english_action"))
        self.help_menu.entryconfig(0, label=translations_tk.get_text("about_action"))

        # Mise à jour des widgets
        if hasattr(self, 'input_frame'):
            self.input_frame.config(text=translations_tk.get_text("input_instructions_label"))
        if hasattr(self, 'instructions_label'):
            self.instructions_label.config(text=translations_tk.get_text("input_instructions_text"))
            # Simuler un placeholder pour ScrolledText n'est pas direct. Les instructions sont au-dessus.
        if hasattr(self, 'output_frame'):
            self.output_frame.config(text=translations_tk.get_text("pnach_output_label"))
        if hasattr(self, 'convert_button'):
            self.convert_button.config(text=translations_tk.get_text("convert_button"))
        if hasattr(self, 'clear_button'):
            self.clear_button.config(text=translations_tk.get_text("clear_button"))
        
        self.update_save_as_state() 

    def create_widgets(self):
        main_container = ttk.Frame(self, padding="10")
        main_container.pack(expand=True, fill=tk.BOTH)

        # --- Input Group ---
        self.input_frame = ttk.LabelFrame(main_container, text="RAW Codes and Descriptions (Optional):", padding="10")
        self.input_frame.pack(expand=True, fill=tk.BOTH, pady=(0,10))

        self.instructions_label = ttk.Label(self.input_frame, text="Instructions here...", wraplength=650, justify=tk.LEFT)
        self.instructions_label.pack(pady=(0,5), anchor="w")

        self.input_text = scrolledtext.ScrolledText(self.input_frame, height=10, width=80, relief=tk.FLAT, bd=2)
        self.input_text.pack(expand=True, fill=tk.BOTH, pady=(0,5))
        self.input_text.configure(bg=DARK_INSERT_BG, fg=DARK_FG, insertbackground=DARK_FG, selectbackground=DARK_SELECT_BG)
        
        # --- Output Group ---
        self.output_frame = ttk.LabelFrame(main_container, text="PNACH Output (Preview):", padding="10")
        self.output_frame.pack(expand=True, fill=tk.BOTH, pady=(5,10))

        self.output_text = scrolledtext.ScrolledText(self.output_frame, height=10, width=80, relief=tk.FLAT, bd=2, state="disabled")
        self.output_text.pack(expand=True, fill=tk.BOTH)
        self.output_text.configure(bg=DARK_INSERT_BG, fg=DARK_FG, insertbackground=DARK_FG, selectbackground=DARK_SELECT_BG)

        # --- Buttons ---
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(0,5))

        self.convert_button = ttk.Button(button_frame, text="Convert", command=self.convert_input)
        self.convert_button.pack(side=tk.LEFT, padx=(0,5))

        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=(0,5))


    def convert_input(self):
        raw_input_text = self.input_text.get("1.0", tk.END).strip()
        self.current_pnach_items = []
        
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        
        self.update_save_as_state() # Désactive "Enregistrer sous" initialement

        if not raw_input_text:
            messagebox.showwarning(
                translations_tk.get_text("no_input_warning_title"),
                translations_tk.get_text("no_input_warning_text")
            )
            return

        input_lines = raw_input_text.splitlines()
        pnach_output_lines = [
            f"gametitle={translations_tk.get_text('gametitle_default')}",
            f"comment={translations_tk.get_text('comment_default')}",
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
                pnach_output_lines.append(f"patch=1,EE,{addr_hex},extended,{val_hex}") # Ajout de 'extended'
                current_description = None
            else:
                current_description = cleaned_line 

        if self.current_pnach_items:
            self.output_text.config(state="normal")
            self.output_text.insert("1.0", "\n".join(pnach_output_lines))
            self.output_text.config(state="disabled")
            self.update_save_as_state() # Active "Enregistrer sous"
            messagebox.showinfo(
                translations_tk.get_text("conversion_success_title"),
                translations_tk.get_text("conversion_success_text")
            )
        else:
            no_valid_text = translations_tk.get_text("no_valid_code_warning_text")
            if current_description:
                 no_valid_text = translations_tk.get_text("no_valid_code_with_desc_text", description=current_description)
            
            self.output_text.config(state="normal")
            self.output_text.insert("1.0", no_valid_text)
            self.output_text.config(state="disabled")
            messagebox.showwarning(
                translations_tk.get_text("no_valid_code_warning_title"),
                no_valid_text # Utiliser le texte potentiellement modifié
            )

    def save_as_file(self):
        if not self.current_pnach_items:
            messagebox.showwarning(
                translations_tk.get_text("no_code_to_export_warning_title"),
                translations_tk.get_text("no_code_to_export_warning_text")
            )
            return

        game_title_input = simpledialog.askstring(
            translations_tk.get_text("game_name_input_dialog_title"),
            translations_tk.get_text("game_name_input_dialog_label"),
            parent=self
        )
        if not game_title_input or not game_title_input.strip():
            messagebox.showinfo(
                translations_tk.get_text("export_cancelled_title"),
                translations_tk.get_text("export_cancelled_no_name_text")
            )
            return

        game_crc_input = simpledialog.askstring(
            translations_tk.get_text("game_crc_input_dialog_title"),
            translations_tk.get_text("game_crc_input_dialog_label"),
            parent=self
        )
        if not game_crc_input or not game_crc_input.strip():
            messagebox.showinfo(
                translations_tk.get_text("export_cancelled_title"),
                translations_tk.get_text("export_cancelled_no_crc_text")
            )
            return

        game_crc_cleaned = game_crc_input.strip().upper()
        if not (len(game_crc_cleaned) == 8 and all(c in "0123456789ABCDEF" for c in game_crc_cleaned)):
            messagebox.showerror(
                translations_tk.get_text("invalid_crc_error_title"),
                translations_tk.get_text("invalid_crc_error_text")
            )
            return

        pnach_content_lines = [f"gametitle={game_title_input.strip()}"]
        pnach_content_lines.append(translations_tk.get_text("comment_default"))
        pnach_content_lines.append("")

        for desc, addr, val in self.current_pnach_items:
            if desc:
                pnach_content_lines.append(f"// {desc}")
            pnach_content_lines.append(f"patch=1,EE,{addr},extended,{val}") 

        filepath = filedialog.asksaveasfilename(
            title=translations_tk.get_text("save_pnach_dialog_title"),
            defaultextension=".pnach",
            initialfile=f"{game_crc_cleaned}.pnach",
            filetypes=[(translations_tk.get_text("pnach_file_filter").split(";;")[0].split("(")[0].strip(), 
                        translations_tk.get_text("pnach_file_filter").split(";;")[0].split("(")[1].replace(")", "")),
                       (translations_tk.get_text("pnach_file_filter").split(";;")[1].split("(")[0].strip(),
                        translations_tk.get_text("pnach_file_filter").split(";;")[1].split("(")[1].replace(")", ""))]
        )

        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("\n".join(pnach_content_lines))
                messagebox.showinfo(
                    translations_tk.get_text("file_saved_success_title"),
                    translations_tk.get_text("file_saved_success_text_tk", filepath=filepath)
                )
            except Exception as e:
                messagebox.showerror(
                    translations_tk.get_text("save_error_title"),
                    translations_tk.get_text("save_error_text", error=e)
                )
    
    def clear_fields(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        self.current_pnach_items = []
        self.update_save_as_state()

    def show_about_dialog(self):
        messagebox.showinfo(
            translations_tk.get_text("about_dialog_title"),
            translations_tk.get_text("about_dialog_text"),
            parent=self
        )

    def update_save_as_state(self):
        # Utiliser l'index 0 pour "Enregistrer PNACH sous..."
        if self.current_pnach_items:
            self.file_menu.entryconfig(0, state="normal")
        else:
            self.file_menu.entryconfig(0, state="disabled")

if __name__ == "__main__":
    try:
        # Essayer de définir la locale pour correspondre au système
        # Cela peut aider avec certains aspects de l'internationalisation si Tk le supporte
        locale.setlocale(locale.LC_ALL, '') 
    except locale.Error as e:
        print(f"Avertissement : Impossible de définir la locale système : {e}")

    app = Pcsx2PnachToolTk()
    app.mainloop()
