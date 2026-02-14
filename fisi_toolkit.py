import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math
import ipaddress
import pyperclip
import random

# Konfiguration des Erscheinungsbildes
ctk.set_appearance_mode("System")  # Standard: System (Light/Dark je nach OS)
ctk.set_default_color_theme("blue")  # Standard-Theme: Blau

class NetworkTab(ctk.CTkFrame):
    """
    Tab für Netzwerk-Berechnungen.
    Funktionen:
    - IP/Subnetz-Rechner
    - Visuelle Darstellung der UND-Verknüpfung (Binär)
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Grid-Layout Konfiguration
        self.grid_columnconfigure(1, weight=1)

        # Überschrift
        self.label_title = ctk.CTkLabel(self, text="IP & Subnetz Rechner", font=("Arial", 20, "bold"))
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Eingabe IP-Adresse
        self.label_ip = ctk.CTkLabel(self, text="IP-Adresse:")
        self.label_ip.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_ip = ctk.CTkEntry(self, placeholder_text="z.B. 192.168.178.1")
        self.entry_ip.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Eingabe Subnetzmaske (CIDR)
        self.label_cidr = ctk.CTkLabel(self, text="CIDR (z.B. 24):")
        self.label_cidr.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.slider_cidr = ctk.CTkSlider(self, from_=0, to=32, number_of_steps=32, command=self.update_cidr_label)
        self.slider_cidr.set(24) # Standardwert
        self.slider_cidr.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        self.label_cidr_val = ctk.CTkLabel(self, text="/24")
        self.label_cidr_val.grid(row=2, column=2, padx=10, pady=5)

        # Berechnen Button
        self.btn_calc = ctk.CTkButton(self, text="Berechnen", command=self.calculate_network)
        self.btn_calc.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Ergebnisse Bereich (Scrollable Frame für Cards)
        self.result_frame = ctk.CTkScrollableFrame(self)
        self.result_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        # Helper Funktion für Cards (Click-to-Copy)
        def create_card(parent, title, value_var, row, col, color=None):
            card = ctk.CTkFrame(parent)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            # Hover Effekt simulieren
            def on_enter(e): card.configure(border_width=1, border_color="gray50")
            def on_leave(e): card.configure(border_width=0)
            card.bind("<Enter>", on_enter)
            card.bind("<Leave>", on_leave)

            # Copy Funktion
            def copy_card(e):
                val = value_var.get()
                if val and val != "---":
                    pyperclip.copy(val)
                    lbl_val.configure(text_color="green")
                    self.after(500, lambda: lbl_val.configure(text_color=color if color else ("black", "white")))

            card.bind("<Button-1>", copy_card)
            
            lbl_title = ctk.CTkLabel(card, text=title, font=("Arial", 12, "bold"), text_color="gray70")
            lbl_title.pack(anchor="w", padx=10, pady=(5,0))
            lbl_title.bind("<Button-1>", copy_card)
            
            # WICHTIG: Text color standard setzen damit sichtbar
            lbl_val = ctk.CTkLabel(card, textvariable=value_var, font=("Consolas", 14), text_color=color if color else ("black", "white"))
            lbl_val.pack(anchor="w", padx=10, pady=(0,5))
            lbl_val.bind("<Button-1>", copy_card)
            
            return card

        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(1, weight=1)

        # Variablen für Ergebnisse
        self.var_net_id = ctk.StringVar(value="---")
        self.var_broadcast = ctk.StringVar(value="---")
        self.var_first_ip = ctk.StringVar(value="---")
        self.var_last_ip = ctk.StringVar(value="---")
        self.var_hosts = ctk.StringVar(value="---")
        self.var_mask = ctk.StringVar(value="---")
        
        self.var_bin_ip = ctk.StringVar(value="")
        self.var_bin_mask = ctk.StringVar(value="")
        self.var_bin_net = ctk.StringVar(value="")

        # Cards erstellen
        create_card(self.result_frame, "Netzwerk-ID", self.var_net_id, 0, 0, "#1f6aa5")
        create_card(self.result_frame, "Broadcast", self.var_broadcast, 0, 1)
        create_card(self.result_frame, "Erste IP", self.var_first_ip, 1, 0)
        create_card(self.result_frame, "Letzte IP", self.var_last_ip, 1, 1)
        create_card(self.result_frame, "Nutzer Hosts", self.var_hosts, 2, 0)
        create_card(self.result_frame, "Subnetzmaske", self.var_mask, 2, 1)

        ctk.CTkLabel(self.result_frame, text="(Klicke auf die Werte zum Kopieren)", font=("Arial", 10), text_color="gray60").grid(row=2, column=2, sticky="e", padx=10)

        # Binäre Visualisierung Bereich
        self.lbl_bin_title = ctk.CTkLabel(self.result_frame, text="Binäre Analyse", font=("Arial", 14, "bold"))
        self.lbl_bin_title.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        self.frame_bin = ctk.CTkFrame(self.result_frame)
        self.frame_bin.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        ctk.CTkLabel(self.frame_bin, text="IP Adresse:", width=100, anchor="e").grid(row=0, column=0, padx=5, pady=2)
        ctk.CTkLabel(self.frame_bin, textvariable=self.var_bin_ip, font=("Consolas", 12)).grid(row=0, column=1, sticky="w")
        
        ctk.CTkLabel(self.frame_bin, text="Subnetzmaske:", width=100, anchor="e").grid(row=1, column=0, padx=5, pady=2)
        ctk.CTkLabel(self.frame_bin, textvariable=self.var_bin_mask, font=("Consolas", 12)).grid(row=1, column=1, sticky="w")
        
        sep = ctk.CTkFrame(self.frame_bin, height=2, fg_color="gray")
        sep.grid(row=2, column=1, sticky="ew", pady=2)
        
        ctk.CTkLabel(self.frame_bin, text="Netzwerk:", width=100, anchor="e").grid(row=3, column=0, padx=5, pady=2)
        ctk.CTkLabel(self.frame_bin, textvariable=self.var_bin_net, font=("Consolas", 12), text_color="#1f6aa5").grid(row=3, column=1, sticky="w")

        # Copy Button (verschoben)
        self.btn_copy = ctk.CTkButton(self, text="Ergebnisse Kopieren", command=self.copy_results, width=100)
        self.btn_copy.grid(row=5, column=0, columnspan=3, pady=10)

    def update_cidr_label(self, value):
        self.label_cidr_val.configure(text=f"/{int(value)}")

    def calculate_network(self):
        ip_str = self.entry_ip.get()
        cidr = int(self.slider_cidr.get())

        try:
            # Erstelle Netzwerk-Objekt
            network = ipaddress.IPv4Network(f"{ip_str}/{cidr}", strict=False)
            
            # Update Variablen
            self.var_net_id.set(str(network.network_address))
            self.var_mask.set(str(network.netmask))
            self.var_broadcast.set(str(network.broadcast_address))
            
            num_hosts = network.num_addresses - 2 if network.num_addresses > 2 else 0
            self.var_hosts.set(f"{num_hosts:,}".replace(",", "."))
            
            self.var_first_ip.set(str(list(network.hosts())[0]) if num_hosts > 0 else "N/A")
            self.var_last_ip.set(str(list(network.hosts())[-1]) if num_hosts > 0 else "N/A")

            # Binäre Darstellung
            ip_obj = ipaddress.IPv4Address(ip_str)
            ip_bin = f"{int(ip_obj):032b}"
            mask_bin = f"{int(network.netmask):032b}"
            net_bin = f"{int(network.network_address):032b}"
            
            def format_bin(b): return ".".join([b[i:i+8] for i in range(0, 32, 8)])
            
            self.var_bin_ip.set(f"{format_bin(ip_bin)}  ({ip_str})")
            self.var_bin_mask.set(f"{format_bin(mask_bin)}  (AND)")
            self.var_bin_net.set(f"{format_bin(net_bin)}  (=)")

        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige IP-Adresse!\n{e}")

    def copy_results(self):
        try:
            text = f"Netzwerk: {self.var_net_id.get()}\n"
            text += f"Maske: {self.var_mask.get()}\n"
            text += f"Broadcast: {self.var_broadcast.get()}\n"
            text += f"Hosts: {self.var_hosts.get()}\n"
            text += f"Range: {self.var_first_ip.get()} - {self.var_last_ip.get()}"
            pyperclip.copy(text)
            messagebox.showinfo("Kopiert", "Wichtige Daten wurden kopiert!")
        except Exception as e:
            messagebox.showerror("Fehler", str(e))

class StorageTab(ctk.CTkFrame):
    """
    Tab für Speicher-Berechnungen (RAID).
    Funktionen:
    - RAID 0, 1, 5, 6, 10
    - Berechnung Brutto/Netto Kapazität
    - Anzeige der Verschnitt/Paritäts-Infos
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)

        self.label_title = ctk.CTkLabel(self, text="RAID Kalkulator", font=("Arial", 20, "bold"))
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # RAID Level Auswahl
        self.label_raid = ctk.CTkLabel(self, text="RAID Level:")
        self.label_raid.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.option_raid = ctk.CTkOptionMenu(self, values=["RAID 0", "RAID 1", "RAID 5", "RAID 6", "RAID 10"])
        self.option_raid.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Festplatten Anzahl
        self.label_disks = ctk.CTkLabel(self, text="Anzahl Festplatten:")
        self.label_disks.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_disks = ctk.CTkEntry(self, placeholder_text="Mind. je nach RAID")
        self.entry_disks.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Kapazität pro Disk
        self.label_size = ctk.CTkLabel(self, text="Größe pro Disk (GB):")
        self.label_size.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_size = ctk.CTkEntry(self, placeholder_text="z.B. 1000")
        self.entry_size.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Berechnen Button
        self.btn_calc = ctk.CTkButton(self, text="Berechnen", command=self.calculate_raid)
        self.btn_calc.grid(row=4, column=0, columnspan=2, pady=15, padx=10, sticky="ew")

        # Ergebnisse Bereich (Cards)
        self.result_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.result_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(5, weight=1)

        def create_card(parent, title, value_var, row, col):
            card = ctk.CTkFrame(parent)
            card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            lbl_title = ctk.CTkLabel(card, text=title, font=("Arial", 12, "bold"), text_color="gray70")
            lbl_title.pack(anchor="w", padx=10, pady=(5,0))
            
            lbl_val = ctk.CTkLabel(card, textvariable=value_var, font=("Consolas", 14))
            lbl_val.pack(anchor="w", padx=10, pady=(0,5))
            return card

        self.result_frame.grid_columnconfigure(0, weight=1)
        self.result_frame.grid_columnconfigure(1, weight=1)

        # Variablen
        self.var_brutto = ctk.StringVar(value="---")
        self.var_netto = ctk.StringVar(value="---")
        self.var_effizienz = ctk.StringVar(value="---")
        self.var_toleranz = ctk.StringVar(value="---")
        self.var_formel = ctk.StringVar(value="---")

        create_card(self.result_frame, "Brutto Kapazität", self.var_brutto, 0, 0)
        create_card(self.result_frame, "Netto Kapazität", self.var_netto, 0, 1)
        create_card(self.result_frame, "Effizienz", self.var_effizienz, 1, 0)
        create_card(self.result_frame, "Ausfallsicherheit", self.var_toleranz, 1, 1)
        
        # Formel Card (Full Width)
        card_formula = ctk.CTkFrame(self.result_frame)
        card_formula.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        ctk.CTkLabel(card_formula, text="Verwendete Formel", font=("Arial", 12, "bold"), text_color="gray70").pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(card_formula, textvariable=self.var_formel, font=("Consolas", 14, "italic")).pack(anchor="w", padx=10, pady=(0,5))

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=6, column=0, columnspan=2, pady=5)

    def calculate_raid(self):
        raid_type = self.option_raid.get()
        self.error_label.configure(text="")
        
        try:
            num_disks = int(self.entry_disks.get())
            size_disk = float(self.entry_size.get())
        except ValueError:
            self.error_label.configure(text="Bitte gültige Zahlen eingeben!")
            return

        net_capacity = 0
        fault_tolerance = ""
        formula = ""
        valid = True
        msg = ""

        if raid_type == "RAID 0":
            if num_disks < 2: valid, msg = False, "Min. 2 Disks"
            net_capacity = num_disks * size_disk
            fault_tolerance = "Keine (0 Disks)"
            formula = f"{num_disks} * {size_disk:g} GB = {net_capacity:g} GB"
        elif raid_type == "RAID 1":
            if num_disks < 2: valid, msg = False, "Min. 2 Disks"
            net_capacity = size_disk 
            fault_tolerance = f"{num_disks-1} Disks (Spiegelung)"
            formula = f"{size_disk:g} GB (Spiegelung)"
        elif raid_type == "RAID 5":
            if num_disks < 3: valid, msg = False, "Min. 3 Disks"
            net_capacity = (num_disks - 1) * size_disk
            fault_tolerance = "1 Disk"
            formula = f"({num_disks} - 1) * {size_disk:g} GB = {net_capacity:g} GB"
        elif raid_type == "RAID 6":
            if num_disks < 4: valid, msg = False, "Min. 4 Disks"
            net_capacity = (num_disks - 2) * size_disk
            fault_tolerance = "2 Disks"
            formula = f"({num_disks} - 2) * {size_disk:g} GB = {net_capacity:g} GB"
        elif raid_type == "RAID 10":
            if num_disks < 4 or num_disks % 2 != 0: valid, msg = False, "Min. 4 Disks, gerade Anzahl"
            net_capacity = (num_disks / 2) * size_disk
            fault_tolerance = "Bis zu n/2 (Sub-Array)"
            formula = f"({num_disks} / 2) * {size_disk:g} GB = {net_capacity:g} GB"

        if not valid:
            self.error_label.configure(text=f"Fehler: {msg}")
        else:
            brutto = num_disks * size_disk
            efficiency = (net_capacity / brutto) * 100
            
            self.var_brutto.set(f"{brutto:.2f} GB")
            self.var_netto.set(f"{net_capacity:.2f} GB")
            self.var_effizienz.set(f"{efficiency:.1f} %")
            self.var_toleranz.set(fault_tolerance)
            self.var_formel.set(formula)


class LogicTab(ctk.CTkFrame):
    """
    Tab für Logik-Berechnungen (Hex/Dez/Bin).
    Funktionen:
    - Bit-Matrix (32 Bits & 64 Bits)
    - Echtzeit-Umrechnung
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label_title = ctk.CTkLabel(self, text="Bit-Matrix & Konverter", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=10)

        # Container für die Eingabefelder
        self.frame_inputs = ctk.CTkFrame(self)
        self.frame_inputs.pack(pady=10, padx=10, fill="x")

        # Dezimal
        self.label_dec = ctk.CTkLabel(self.frame_inputs, text="Dezimal:")
        self.label_dec.grid(row=0, column=0, padx=5, pady=5)
        self.entry_dec = ctk.CTkEntry(self.frame_inputs)
        self.entry_dec.grid(row=0, column=1, padx=5, pady=5)
        self.entry_dec.bind("<KeyRelease>", self.on_dec_change)

        # Hex
        self.label_hex = ctk.CTkLabel(self.frame_inputs, text="Hex:")
        self.label_hex.grid(row=0, column=2, padx=5, pady=5)
        self.entry_hex = ctk.CTkEntry(self.frame_inputs)
        self.entry_hex.grid(row=0, column=3, padx=5, pady=5)
        self.entry_hex.bind("<KeyRelease>", self.on_hex_change)

        # Binär
        self.label_bin = ctk.CTkLabel(self.frame_inputs, text="Binär (32-Bit):")
        self.label_bin.grid(row=0, column=4, padx=5, pady=5)
        self.entry_bin = ctk.CTkEntry(self.frame_inputs, width=220)
        self.entry_bin.grid(row=0, column=5, padx=5, pady=5)
        self.entry_bin.bind("<KeyRelease>", self.on_bin_change)

        # Matrix Container
        self.frame_matrix_container = ctk.CTkFrame(self)
        self.frame_matrix_container.pack(pady=10, padx=10, fill="both", expand=True)

        # 32-Bit Matrix (nur noch diese)
        ctk.CTkLabel(self.frame_matrix_container, text="32-Bit Matrix (Integer)", font=("Arial", 14, "bold")).pack(pady=(5,0))
        self.create_bit_matrix(self.frame_matrix_container, 32, "bits32", height=140)

        self.current_value = 0

    def create_bit_matrix(self, parent, bit_count, attr_prefix, height):
        scroll = ctk.CTkScrollableFrame(parent, orientation="horizontal", height=height)
        scroll.pack(fill="x", padx=5, pady=5)
        
        bits = [0] * bit_count  # Initialize all bits to 0
        buttons = []
        
        setattr(self, f"{attr_prefix}_state", bits)
        setattr(self, f"{attr_prefix}_btns", buttons)

        inner_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        inner_frame.pack()

        for i in range(bit_count):
            byte_group = i // 8
            bit_in_byte = i % 8
            
            if bit_in_byte == 0:
                frame_byte = ctk.CTkFrame(inner_frame, fg_color="transparent")
                frame_byte.pack(side="left", padx=5)
                
                byte_num = (bit_count // 8) - 1 - byte_group
                ctk.CTkLabel(frame_byte, text=f"Byte {byte_num}", font=("Arial", 10, "bold")).pack()
                
                frame_bits_in_byte = ctk.CTkFrame(frame_byte, fg_color="transparent")
                frame_bits_in_byte.pack()
            
            frame_single = ctk.CTkFrame(frame_bits_in_byte, fg_color="transparent")
            frame_single.pack(side="left", padx=1)

            # bit_index is the actual bit position (MSB to LSB)
            bit_index = bit_count - 1 - i
            btn = ctk.CTkButton(
                frame_single, text="0", width=28, height=28, fg_color="gray", font=("Arial", 11, "bold"),
                command=lambda idx=bit_index, p=attr_prefix: self.toggle_bit(idx, p)
            )
            btn.pack()
            
            val = 2**(7-bit_in_byte)
            ctk.CTkLabel(frame_single, text=str(val), font=("Arial", 8), text_color="gray60").pack()
            
            buttons.append(btn)

    def toggle_bit(self, bit_index, attr_prefix):
        """Toggle a bit at the given position (0 = LSB, 31 = MSB)"""
        bits = getattr(self, f"{attr_prefix}_state")
        
        # Toggle the bit directly at bit_index
        bits[bit_index] = 1 - bits[bit_index]
        
        # Calculate value from bits
        val = 0
        for i in range(len(bits)):
            if bits[i]:
                val += 2**i
            
        self.current_value = val
        self.update_gui(source="matrix32")

    def update_matrix_gui(self, attr_prefix):
        """Update button display based on bit state"""
        bits = getattr(self, f"{attr_prefix}_state")
        btns = getattr(self, f"{attr_prefix}_btns")
        bit_count = len(bits)
        
        for i, btn in enumerate(btns):
            # Button i corresponds to bit (bit_count - 1 - i)
            bit_idx = bit_count - 1 - i
            state = bits[bit_idx]
            btn.configure(text="1" if state else "0", fg_color="#1f6aa5" if state else "gray")

    def update_bits_from_value(self, val, bit_count, attr_prefix):
        """Update bit array from integer value"""
        bits = getattr(self, f"{attr_prefix}_state")
        for i in range(bit_count):
            bits[i] = (val >> i) & 1

    def update_gui(self, source=None):
        if source != "dec":
            self.entry_dec.delete(0, "end")
            self.entry_dec.insert(0, str(self.current_value))
        if source != "hex":
            self.entry_hex.delete(0, "end")
            self.entry_hex.insert(0, f"{self.current_value:X}")
        if source != "bin":
            self.entry_bin.delete(0, "end")
            self.entry_bin.insert(0, f"{self.current_value:b}")
            
        if source in ["dec", "hex", "bin"]:
             self.update_bits_from_value(self.current_value, 32, "bits32")
        
        self.update_matrix_gui("bits32")

    def on_dec_change(self, event):
        txt = self.entry_dec.get()
        if not txt: return
        try:
            val = int(txt)
            if val > 0xFFFFFFFF: val = 0xFFFFFFFF
            self.current_value = val
            self.update_bits_from_value(val, 32, "bits32")
            self.update_gui(source="dec")
        except ValueError: pass

    def on_hex_change(self, event):
        txt = self.entry_hex.get()
        if not txt: return
        try:
            val = int(txt, 16)
            if val > 0xFFFFFFFF: val = 0xFFFFFFFF
            self.current_value = val
            self.update_bits_from_value(val, 32, "bits32")
            self.update_gui(source="hex")
        except ValueError: pass

    def on_bin_change(self, event):
        txt = self.entry_bin.get()
        if not txt: return
        try:
            val = int(txt, 2)
            if val > 0xFFFFFFFF: val = 0xFFFFFFFF
            self.current_value = val
            self.update_bits_from_value(val, 32, "bits32")
            self.update_gui(source="bin")
        except ValueError: pass


class SettingsTab(ctk.CTkFrame):
    """
    Tab für Einstellungen (Design, Skalierung).
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label_title = ctk.CTkLabel(self, text="Einstellungen", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=20)

        # Erscheinungsbild
        self.frame_appearance = ctk.CTkFrame(self)
        self.frame_appearance.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.frame_appearance, text="Erscheinungsbild:", font=("Arial", 14)).pack(side="left", padx=20, pady=10)
        self.option_appearance = ctk.CTkOptionMenu(self.frame_appearance, values=["System", "Light", "Dark"],
                                                   command=self.change_appearance)
        self.option_appearance.set(ctk.get_appearance_mode())
        self.option_appearance.pack(side="right", padx=20, pady=10)

        # Skalierung
        self.frame_scaling = ctk.CTkFrame(self)
        self.frame_scaling.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.frame_scaling, text="UI Skalierung:", font=("Arial", 14)).pack(side="left", padx=20, pady=10)
        self.option_scaling = ctk.CTkOptionMenu(self.frame_scaling, values=["80%", "90%", "100%", "110%", "120%"],
                                                command=self.change_scaling)
        self.option_scaling.set("100%")
        self.option_scaling.pack(side="right", padx=20, pady=10)

    def change_appearance(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)



class UnitConverterTab(ctk.CTkFrame):
    """
    Tab für Einheiten-Umrechnung (Bit, Byte, KiB, etc.).
    Features: Live-Berechnung, detaillierte Aufschlüsselung.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.label_title = ctk.CTkLabel(self, text="Einheiten-Rechner", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=10)

        # Input Area
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(pady=10, padx=10, fill="x")

        self.entry_val = ctk.CTkEntry(self.frame_input, placeholder_text="Wert eingeben...")
        self.entry_val.pack(side="left", padx=10, expand=True, fill="x")
        self.entry_val.bind("<KeyRelease>", self.calculate)
        
        self.units = ["Bit", "Byte", "KiB", "MiB", "GiB", "TiB"]
        self.option_unit = ctk.CTkOptionMenu(self.frame_input, values=self.units, command=lambda x: self.calculate())
        self.option_unit.pack(side="left", padx=10)

        # Output Area (Scrollable)
        self.frame_results = ctk.CTkScrollableFrame(self)
        self.frame_results.pack(pady=10, padx=10, fill="both", expand=True)
        self.frame_results.grid_columnconfigure(0, weight=1)

        # Dictionary für Label Referenzen
        self.result_widgets = {}

        # Initialisierung der Zeilen für jede Einheit
        for i, u in enumerate(self.units):
            card = ctk.CTkFrame(self.frame_results)
            card.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            
            # Titel (z.B. "Mebibyte (MiB)")
            long_names = {
                "Bit": "Bit (b)", "Byte": "Byte (B)", 
                "KiB": "Kibibyte (KiB)", "MiB": "Mebibyte (MiB)", 
                "GiB": "Gibibyte (GiB)", "TiB": "Tebibyte (TiB)"
            }
            
            lbl_title = ctk.CTkLabel(card, text=long_names[u], font=("Arial", 12, "bold"), text_color="gray70")
            lbl_title.pack(anchor="w", padx=10, pady=(5,0))
            
            # Wert (Formatiert)
            lbl_val = ctk.CTkLabel(card, text="---", font=("Consolas", 14))
            lbl_val.pack(anchor="w", padx=10, pady=(0,0))
            
            # Rechenweg/Dezimal Info
            lbl_info = ctk.CTkLabel(card, text="", font=("Arial", 10), text_color="gray60")
            lbl_info.pack(anchor="w", padx=10, pady=(0,5))

            self.result_widgets[u] = {
                "val": lbl_val,
                "info": lbl_info
            }

    def calculate(self, event=None):
        val_str = self.entry_val.get()
        src_unit = self.option_unit.get()

        if not val_str:
            for u in self.units:
                self.result_widgets[u]["val"].configure(text="---")
                self.result_widgets[u]["info"].configure(text="")
            return

        try:
            val = float(val_str)
        except ValueError:
            return

        # Basis: Bit
        bits = 0
        if src_unit == "Bit": bits = val
        elif src_unit == "Byte": bits = val * 8
        elif src_unit == "KiB": bits = val * 8 * 1024
        elif src_unit == "MiB": bits = val * 8 * 1024**2
        elif src_unit == "GiB": bits = val * 8 * 1024**3
        elif src_unit == "TiB": bits = val * 8 * 1024**4

        # Berechne alle Einheiten (Binär)
        conversions = {
            "Bit":  (bits, "Basis"),
            "Byte": (bits / 8, "/ 8"),
            "KiB":  (bits / (8 * 1024), "/ 8 / 1024"),
            "MiB":  (bits / (8 * 1024**2), r"/ 8 / 1024²"),
            "GiB":  (bits / (8 * 1024**3), r"/ 8 / 1024³"),
            "TiB":  (bits / (8 * 1024**4), r"/ 8 / 1024⁴")
        }
        
        # Dezimal-Äquivalente (1000er Basis)
        decimal_conversions = {
            "Bit":  bits,
            "Byte": bits / 8,
            "KiB":  bits / (8 * 1000),      # KB
            "MiB":  bits / (8 * 1000**2),   # MB
            "GiB":  bits / (8 * 1000**3),   # GB
            "TiB":  bits / (8 * 1000**4)    # TB
        }

        for u in self.units:
            res_val, formula = conversions[u]
            dec_val = decimal_conversions[u]
            
            # Formatierung Binär
            txt_val = f"{res_val:,.10f}".rstrip("0").rstrip(".") if res_val % 1 != 0 else f"{int(res_val):,}"
            
            # Info mit Dezimal-Äquivalent
            if u == "Bit":
                txt_info = "Basiswert"
            elif u == "Byte":
                txt_info = "8 Bits = 1 Byte"
            else:
                # Zeige Dezimal-Äquivalent (KB, MB, GB, TB) - 1000er Basis
                dec_unit = u.replace("i", "")  # KiB -> KB, MiB -> MB, etc.
                dec_formatted = f"{dec_val:,.10f}".rstrip("0").rstrip(".") if dec_val % 1 != 0 else f"{int(dec_val):,}"
                txt_info = f"≈ {dec_formatted} {dec_unit} (Dezimal, 1000er-Basis)"
            
            self.result_widgets[u]["val"].configure(text=txt_val)
            self.result_widgets[u]["info"].configure(text=txt_info)



class InfoTab(ctk.CTkFrame):
    """
    Info Tab mit Credits und Links.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        import webbrowser

        self.pack_propagate(False) # Prevent shrinking

        self.label_title = ctk.CTkLabel(self, text="Über das FISI Toolkit", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=(40, 20))

        self.label_author = ctk.CTkLabel(self, text="Erstellt von Ivan Krznaric-Bertic", font=("Arial", 16))
        self.label_author.pack(pady=10)

        self.btn_linkedin = ctk.CTkButton(self, text="LinkedIn Profil", 
                                          command=lambda: webbrowser.open("www.linkedin.com/in/ivan-krznaric-bertic"))
        self.btn_linkedin.pack(pady=10)

        self.btn_github = ctk.CTkButton(self, text="GitHub Profil", 
                                        command=lambda: webbrowser.open("https://github.com/Whitefox75"))
        self.btn_github.pack(pady=10)



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Fenster Konfiguration
        self.title("FISI Toolkit - IT Fachinformatiker Werkzeuge")
        self.geometry("1000x700")
        self.minsize(800, 600)

        # Grid Layout 1x2 (Sidebar + Main Content)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_expanded = True
        self.sidebar_width_expanded = 140
        self.sidebar_width_collapsed = 45

        self.sidebar_frame = ctk.CTkFrame(self, width=self.sidebar_width_expanded, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)  # Prevent children from resizing the frame
        self.sidebar_frame.grid_rowconfigure(6, weight=1) # Spacer pushes bottom elements down
        
        # Toggle Button
        self.btn_toggle = ctk.CTkButton(self.sidebar_frame, text="☰", width=30, height=30, fg_color="transparent", 
                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        command=self.toggle_sidebar)
        self.btn_toggle.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Logo / Title (fix truncation by using grid_remove instead of grid_forget)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FISI Toolkit", font=ctk.CTkFont(size=16, weight="bold"))
        self.logo_label.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")

        # Navigation Buttons
        self.nav_buttons = {}
        self.current_frame = None
        
        # Format: (Text, Icon/Short, Name, Class)
        self.btn_data = [
            ("Netzwerk", "N", "network", NetworkTab),
            ("Speicher", "S", "storage", StorageTab),
            ("Logik", "L", "logic", LogicTab),
            ("Einheiten", "E", "converter", UnitConverterTab),
            ("Einstellungen", "⚙", "settings", SettingsTab), 
            ("Info", "i", "info", InfoTab)
        ]

        self.frames = {}
        
        # Layout Order: 1..5 for Tools, 7=Settings, 8=Info. 6 is Spacer.
        # We need to map list index to row index manually to pu Settings/Info at bottom
        
        for i, (text, short, name, cls) in enumerate(self.btn_data):
            # Init Frame
            self.frames[name] = cls(self)
            
            # Determine Row
            # Tools: row 2-5
            # Settings: row 7
            # Info: row 8
            if name == "settings": row = 7
            elif name == "info": row = 8
            else: row = i + 2  # Start at row 2 to leave room for title
            
            btn = ctk.CTkButton(self.sidebar_frame, corner_radius=0, height=40, border_spacing=10, text=text,
                                fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                anchor="w", command=lambda n=name: self.select_frame(n))
            btn.grid(row=row, column=0, sticky="ew")
            self.nav_buttons[name] = btn


        # Sidebar Options (Bottom) - REMOVED (Duplicate)
        # self.appearance_mode_label = ...
        # self.appearance_mode_optionemenu = ...
        # self.scaling_label = ...
        # self.scaling_optionemenu = ...

        # Start with Network
        self.select_frame("network")

    def select_frame(self, name):
        # Update Buttons
        for n, btn in self.nav_buttons.items():
            if n == name:
                btn.configure(fg_color=("gray75", "gray25"), text_color=("black", "white"))
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

        # Switch Frame
        if self.current_frame:
            self.current_frame.grid_forget()
        
        self.current_frame = self.frames[name]
        self.current_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar_width_expanded = self.sidebar_frame.winfo_width() # Save current if needed, or just use const
            self.sidebar_frame.configure(width=self.sidebar_width_collapsed)
            
            # Hide texts, show only icons/short
            self.logo_label.grid_forget()
            # self.appearance_mode_label.grid_forget()
            # self.appearance_mode_optionemenu.grid_forget()
            # self.scaling_label.grid_forget()
            # self.scaling_optionemenu.grid_forget()
            self.btn_toggle.grid(padx=5) # Adjust padding

            for name, btn in self.nav_buttons.items():
                # Find short text from data
                short = next((d[1] for d in self.btn_data if d[2] == name), name[0])
                btn.configure(text=short, anchor="center")
            
            self.sidebar_expanded = False
        else:
            self.sidebar_frame.configure(width=self.sidebar_width_expanded)
            
            # Show texts
            self.logo_label.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
            # self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
            # self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
            # self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
            # self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
            self.btn_toggle.grid(padx=10)

            for name, btn in self.nav_buttons.items():
                # Find full text
                text = next((d[0] for d in self.btn_data if d[2] == name), name)
                btn.configure(text=text, anchor="w")
                
            self.sidebar_expanded = True


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

if __name__ == "__main__":
    app = App()
    app.mainloop()
