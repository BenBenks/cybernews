# CyberNews – Sicheres IT-Sicherheits-Portal

Ein modulares, datenbankgestütztes Webportal zur Aggregation und Verwaltung aktueller Cybersecurity-Meldungen. Entwickelt mit Python, Flask und SQLite unter besonderer Berücksichtigung gängiger Best Practices zur Absicherung von Webanwendungen (OWASP Top 10) sowie restriktiver Secret-Isolation.

---

## Inhaltsverzeichnis
- [Architektur & Features](#architektur--features)
- [Sicherheitskonzept](#sicherheitskonzept)
- [Projektstruktur](#projektstruktur)
- [Voraussetzungen](#voraussetzungen)
- [Installation & Schnellstart](#installation--schnellstart)
- [Konfiguration (.env)](#konfiguration-env)
- [Branching & Versionskontrolle](#branching--versionskontrolle)

---

## Architektur & Features

* **MVC-Muster:** Klare Trennung von Datenbankschnittstelle (database.py), Routing- und Businesslogik (app.py) sowie Präsentationsschicht (templates/, static/).
* **News-Dashboard:** Dynamisches Rendern von Featured Articles, kategoriebasiertem Filtern (Data Breaches, Cyber Attacks, Vulnerabilities, AppSec) und Volltextsuche.
* **Dynamisches Routing:** Detailansichten einzelner Artikel über parametrisierte Routen (/article/<id>).
* **Rollenbasierte Zugriffskontrolle (RBAC):** Passwortgeschützter Administrationsbereich (/admin) zur Erstellung und Verwaltung von News-Beiträgen.

---

## Sicherheitskonzept

1. **Umgebungs- und Dependency-Isolation:**
   * Betrieb in einer gekapselten virtuellen Umgebung (.venv).
   * Exaktes Version-Pinning aller Pakete in requirements.txt zur Vermeidung von Inkompatibilitäten und Supply-Chain-Risiken.
2. **Secret Management:**
   * Striktes Auslagern kryptografischer Schlüssel (SECRET_KEY) aus dem Sourcecode in lokale .env-Dateien via python-dotenv.
   * Bereitstellung einer neutralen .env.example-Vorlage mit generischen Platzhaltern für Deployments.
3. **Session- & Cookie-Hardening:**
   * SESSION_COOKIE_HTTPONLY = True: Verhindert das Auslesen von Sitzungs-Cookies via JavaScript (XSS-Mitigation).
   * SESSION_COOKIE_SAMESITE = 'Lax': Effektiver Basisschutz gegen Cross-Site Request Forgery (CSRF).
4. **Datenbank- & Abfragesicherheit:**
   * Verwendung parametrisierter SQL-Queries (?-Platzhalter) zur Unterbindung von SQL-Injections.
   * Irreversibles Hashing von Benutzerpasswörtern mittels werkzeug.security (Scrypt mit Salt).
5. **Leak-Prävention (.gitignore):**
   * Ausschluss von Secrets (.env), Datenbanken (*.db), virtuellen Umgebungen (.venv/) und Logfiles aus der Git-Historie.

---

## Projektstruktur

```text
cybernews/
├── .venv/                   # Lokale virtuelle Python-Umgebung (git-ignored)
├── static/
│   ├── css/
│   │   └── style.css        # Zentrales Stylesheet (Dark Theme)
│   └── js/
│       └── main.js          # Clientseitige Skripte
├── templates/
│   ├── base.html            # Basis-Template mit Master-Layout
│   ├── index.html           # Aggregator-Dashboard & News-Grid
│   ├── article.html         # Detailansicht für Einzelbeiträge
│   ├── admin.html           # Administrations- und Eingabemaske
│   └── login.html           # Authentifizierungsansicht
├── .env                     # Lokale Secrets (git-ignored)
├── .env.example             # Öffentliche Konfigurations-Schablone
├── .gitignore               # Ausschlussregeln für Versionskontrolle
├── app.py                   # Flask-Backend & Routing-Logik
├── database.py              # Datenbankschema & Seed-Initialisierung
├── cybernews.db             # Lokale SQLite-Datenbank (git-ignored)
└── requirements.txt         # Festgeschriebene Abhängigkeiten

---

---

## Voraussetzungen

* Python 3.10 oder höher
* PowerShell oder Bash-kompatibles Terminal
* Git

---

## Installation & Schnellstart

### 1. Repository klonen & Verzeichnis aufrufen
```powershell
git clone <repository-url>
cd cybernews
```

### 2. Virtuelle Umgebung erstellen und aktivieren
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Abhängigkeiten installieren
```powershell
pip install -r requirements.txt
```

### 4. Umgebungskonfiguration anlegen
Kopiere die Vorlage .env.example in eine neue .env-Datei und trage den geheimen Schlüssel ein:
```powershell
# Kopieren der Schablone
Copy-Item .env.example .env

# Generierung eines sicheren Hex-Schlüssels (Beispiel via Python)
python -c "import secrets; print(secrets.token_hex(32))"
```
Trage den erzeugten Hex-String in deiner lokalen .env als SECRET_KEY ein.

### 5. Datenbank initialisieren
```powershell
python database.py
```
*(Legt cybernews.db an, erzeugt die Relationen users und articles und richtet Standard-Datensätze ein.)*

### 6. Anwendung starten
```powershell
python app.py
```
Die Anwendung ist anschließend im Browser erreichbar unter: `http://127.0.0.1:5000`

---

## Konfiguration (.env)

| Variable | Beschreibung | Standardwert / Beispiel |
| :--- | :--- | :--- |
| `SECRET_KEY` | Kryptografischer Signaturschlüssel für Sitzungstoken | *Zufälliger 64-Zeichen Hex-Wert* |
| `FLASK_ENV` | Modus der Laufzeitumgebung | `development` |
| `FLASK_DEBUG` | Aktiviert interaktiven Debugger und Autoreload | `1` |

---

## Branching & Versionskontrolle

Das Repository folgt einer isolierten Branch-Strategie:
* **`main`:** Stabiler Produktionszweig für geprüfte Releases.
* **`develop`:** Aktiver Arbeits- und Entwicklungszweig.

```powershell
# Wechsel auf den Entwicklungs-Branch
git switch develop
```