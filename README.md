# FISI Toolkit

Ein umfassendes Werkzeug für IT-Fachinformatiker mit Netzwerk-, Speicher- und Logik-Berechnungen.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-PolyForm%20NC%20%2F%20Commercial-orange.svg)

## 📋 Features

### 📊 Einheiten-Rechner
- **Binäre Einheiten**: Bit, Byte, KiB, MiB, GiB, TiB (1024er-Basis)
- **Dezimale Äquivalente**: KB, MB, GB, TB (1000er-Basis)
- **Live-Berechnung**: Ergebnisse während der Eingabe

### 🔢 Logik-Tab
- **32-Bit Matrix**: Interaktive Bit-Manipulation
- **Echtzeit-Konvertierung**: Hex ↔ Dezimal ↔ Binär
- **Visuelle Darstellung**: Bits nach Bytes gruppiert

### 🌐 Netzwerk-Tab
- **IP/Subnetz-Rechner**: Berechnet Netzwerkadresse, Broadcast, Hostbereich
- **Binäre Visualisierung**: Zeigt UND-Verknüpfung von IP und Subnetzmaske
- **Clipboard-Integration**: Kopiere Ergebnisse mit einem Klick

### 💾 Speicher-Tab
- **RAID-Rechner**: Unterstützt RAID 0, 1, 5, 6, 10
- **Kapazitätsberechnung**: Brutto, Netto, Effizienz
- **Fehlertoleranz**: Zeigt maximale Ausfallsicherheit

### 🧱 OSI Schichtmodell
- Klar & kompakt: Lerne die 7 OSI-Schichten mit einfachen Erklärungen und praxisnahen Beispielen.
- Praxisorientiert: Verstehe, wie reale Netzwerkprotokolle (z. B. TCP/IP, HTTP, DNS) den einzelnen Schichten zugeordnet sind.
- Offline verfügbar: Ideal zum Lernen und Nachschlagen – direkt vom USB-Stick, jederzeit ohne Internet.

### ⚙️ Einstellungen
- **Design-Modi**: System, Light, Dark
- **UI-Skalierung**: 80% - 120%
- **Kollabierbare Sidebar**: Mehr Platz für Inhalte

## 🚀 Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### Anwendung starten
```bash
python fisi_toolkit.py
```

## 📦 Standalone-EXE erstellen

Erstelle eine portable EXE-Datei ohne Python-Installation:

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile fisi_toolkit.py
```

Die EXE findest du dann unter `dist/fisi_toolkit.exe`

## 🖥️ Systemanforderungen

- **Betriebssystem**: Windows 10/11, macOS, Linux
- **RAM**: Mindestens 100 MB
- **Festplatte**: ~50 MB für Standalone-EXE

## 📸 Screenshots

### Netzwerk-Tab
Berechne IP-Adressen und Subnetze mit visueller Binärdarstellung.

### Logik-Tab
Interaktive 32-Bit-Matrix für Hex/Dez/Bin-Konvertierung.

### Einheiten-Rechner
Vergleiche binäre und dezimale Speichereinheiten.

## 🛠️ Technologie-Stack

- **GUI Framework**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- **Clipboard**: [pyperclip](https://github.com/asweigart/pyperclip)
- **Build Tool**: PyInstaller

## 📝 Lizenz

Dieses Projekt ist unter der Dual-Licensing Model lizensiert - siehe [LICENSE](LICENSE) Datei für Details.

## 👤 Autor

**Ivan Krznaric-Bertic**

- LinkedIn: [Ivan Krznaric-Bertic](https://www.linkedin.com/in/ivan-krznaric-bertic-60ab5333b)
- GitHub: [@Whitefox75](https://github.com/Whitefox75)

## 🤝 Beiträge

Beiträge, Issues und Feature-Requests sind willkommen!

1. Fork das Projekt
2. Erstelle deinen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 🙏 Danksagungen

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) für das moderne UI-Framework
- Alle Mitwirkenden und Tester

## 📚 Weitere Ressourcen

- [Dokumentation](docs/)
- [Changelog](CHANGELOG.md)
- [FAQ](docs/FAQ.md)

---

⭐ Wenn dir dieses Projekt gefällt, gib ihm einen Stern auf GitHub!
