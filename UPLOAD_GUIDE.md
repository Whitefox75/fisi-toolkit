# GitHub Upload Guide

## 📋 Checkliste vor dem Upload

✅ Alle Dateien erstellt:
- [x] `.gitignore` - Verhindert Upload von Build-Dateien
- [x] `README.md` - Projekt-Beschreibung
- [x] `requirements.txt` - Python-Abhängigkeiten
- [x] `LICENSE` - MIT-Lizenz
- [x] `CHANGELOG.md` - Versions-Historie

## 🚀 Schritt-für-Schritt Anleitung

### 1. GitHub Repository erstellen

1. Gehe zu [github.com](https://github.com)
2. Klicke auf "+" → "New repository"
3. Repository-Name: `fisi-toolkit`
4. Beschreibung: "IT-Fachinformatiker Toolkit mit Netzwerk-, Speicher- und Logik-Berechnungen"
5. **WICHTIG**: Wähle "Public" oder "Private"
6. **NICHT** "Initialize with README" ankreuzen (haben wir schon!)
7. Klicke "Create repository"

### 2. Git initialisieren (falls noch nicht geschehen)

Öffne PowerShell im Projekt-Ordner:

```powershell
cd C:\Users\Ivan\.gemini\antigravity\scratch\fisi_toolkit
git init
```

### 3. Dateien hinzufügen

```powershell
git add .
git commit -m "Initial commit: FISI Toolkit v1.0.0"
```

### 4. Mit GitHub verbinden

Ersetze `DEIN_USERNAME` mit deinem GitHub-Benutzernamen:

```powershell
git remote add origin https://github.com/DEIN_USERNAME/fisi-toolkit.git
git branch -M main
git push -u origin main
```

### 5. Optional: Release erstellen

1. Gehe zu deinem Repository auf GitHub
2. Klicke "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: "FISI Toolkit v1.0.0 - Initial Release"
5. Beschreibung: Kopiere aus CHANGELOG.md
6. **Wichtig**: Lade die `fisi_toolkit.exe` aus `dist/` hoch!
7. Klicke "Publish release"

## 📝 Was wird NICHT hochgeladen?

Dank `.gitignore` werden folgende Dateien automatisch ausgeschlossen:
- `__pycache__/` - Python Cache
- `build/` - PyInstaller Build-Dateien
- `dist/` - Die fertige EXE (wird als Release hochgeladen)
- `*.spec` - PyInstaller Spec-Dateien
- Test-Dateien

## 🔒 Wichtige Hinweise

### Sensible Daten
- ✅ Keine Passwörter oder API-Keys im Code
- ✅ Keine persönlichen Daten
- ✅ Keine internen Firmen-Informationen

### Best Practices
- Schreibe aussagekräftige Commit-Messages
- Nutze Branches für neue Features (`git checkout -b feature/neue-funktion`)
- Erstelle Pull Requests für größere Änderungen
- Halte README.md aktuell

## 🎯 Nach dem Upload

### Repository-Einstellungen optimieren

1. **Topics hinzufügen** (unter "About"):
   - `python`
   - `tkinter`
   - `customtkinter`
   - `networking`
   - `calculator`
   - `it-tools`

2. **GitHub Pages aktivieren** (optional):
   - Settings → Pages
   - Source: "Deploy from branch"
   - Branch: `main` / `docs`

3. **Beschreibung hinzufügen**:
   "IT-Fachinformatiker Toolkit mit Netzwerk-, Speicher- und Logik-Berechnungen"

4. **Website hinzufügen**:
   Dein LinkedIn-Profil oder Portfolio

## 🐛 Troubleshooting

### "Permission denied (publickey)"
```powershell
# Nutze HTTPS statt SSH:
git remote set-url origin https://github.com/DEIN_USERNAME/fisi-toolkit.git
```

### "Updates were rejected"
```powershell
# Hole zuerst die neuesten Änderungen:
git pull origin main --rebase
git push origin main
```

### Große Dateien (>100MB)
Die EXE sollte unter 50MB sein. Falls größer:
- Nutze GitHub Releases für die EXE
- Lade sie NICHT in den main Branch

## ✅ Fertig!

Dein Repository ist jetzt live unter:
`https://github.com/DEIN_USERNAME/fisi-toolkit`

Teile den Link mit:
- Kommilitonen
- Auf LinkedIn
- In IT-Communities
- Im Lebenslauf als Portfolio-Projekt

---

**Viel Erfolg! 🚀**
