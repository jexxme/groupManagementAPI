# LBV - Lerngruppen Bildung und Verwaltung API

Die LBV (Lerngruppen Bildung und Verwaltung) API ist eine RESTful-Webanwendung, die entwickelt wurde, um die Verwaltung von Lerngruppen und Benutzern zu erleichtern. Sie ermöglicht die Erstellung, Aktualisierung und Löschung von Benutzern, Gruppen, Terminen und Beziehungen zwischen Benutzern und Gruppen. Diese Dokumentation bietet eine umfassende Übersicht über die verfügbaren Endpunkte, ihre Verwendung und die erwarteten Datenstrukturen.

## Inhaltsverzeichnis

1. [Allgemeine Informationen](#allgemeine-informationen)
2. [Installation](#installation)
3. [Verwendung](#verwendung)
4. [Dashboard](#dashboard)
5. [Benutzer (Users)](#benutzer-users)
   - [Erstellen eines Benutzers](#erstellen-eines-benutzers)
   - [Erstellen eines Administrators](#erstellen-eines-administrators)
   - [Abrufen aller Benutzer](#abrufen-aller-benutzer)
   - [Abrufen eines einzelnen Benutzers](#abrufen-eines-einzelnen-benutzers)
   - [Aktualisieren eines Benutzers](#aktualisieren-eines-benutzers)
   - [Löschen eines Benutzers](#löschen-eines-benutzers)
6. [Gruppen (Groups)](#gruppen-groups)
   - [Erstellen einer Gruppe](#erstellen-einer-gruppe)
   - [Abrufen aller Gruppen](#abrufen-aller-gruppen)
   - [Abrufen einer einzelnen Gruppe](#abrufen-einer-einzelnen-gruppe)
   - [Aktualisieren einer Gruppe](#aktualisieren-einer-gruppe)
   - [Löschen einer Gruppe](#löschen-einer-gruppe)
7. [Termine (Dates)](#termine-dates)
   - [Erstellen eines Termins](#erstellen-eines-termins)
   - [Abrufen aller Termine](#abrufen-aller-termine)
   - [Abrufen eines einzelnen Termins](#abrufen-eines-einzelnen-termins)
   - [Aktualisieren eines Termins](#aktualisieren-eines-termins)
   - [Löschen eines Termins](#löschen-eines-termins)
8. [Benutzer in Gruppen (UsersInGroups)](#benutzer-in-gruppen-usersingroups)
   - [Hinzufügen eines Benutzers zu einer Gruppe](#hinzufügen-eines-benutzers-zu-einer-gruppe)
   - [Abrufen aller Benutzer in einer Gruppe](#abrufen-aller-benutzer-in-einer-gruppe)
   - [Aktualisieren des Startdatums eines Benutzers in einer Gruppe](#aktualisieren-des-startdatums-eines-benutzers-in-einer-gruppe)
   - [Entfernen eines Benutzers aus einer Gruppe](#entfernen-eines-benutzers-aus-einer-gruppe)
9. [Authentifizierung](#authentifizierung)
10. [Tests](#tests)
11. [Öffentliche API](#öffentliche-api)


## Allgemeine Informationen

Die LBV-API wurde entwickelt, um die Verwaltung von Lerngruppen und Benutzern in einer Bildungsumgebung zu unterstützen. Sie bietet folgende Hauptfunktionen:

- **Benutzerverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Benutzerkonten.
- **Gruppenverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Lerngruppen.
- **Terminverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Terminen für Lerngruppen.
- **Verwaltung von Benutzern in Gruppen:** Hinzufügen, Abrufen, Aktualisieren und Entfernen von Benutzern in Gruppen.

Die API verwendet das JSON-Format für Anfragen und Antworten.

Die Authtifikation erfolgt über JWT-Token. Es gibt zwei verschiedene Arten von Benutzern: Administratoren und normale Benutzer. Administratoren haben erweiterte Rechte, wie z.B. das Löschen und Bearbeiten von Benutzerkonten.

Die LBV-API wurde mit Python und Flask entwickelt. Sie verwendet eine SQLite-Datenbank, um Benutzer- und Gruppendaten zu speichern.

## Installation

Befolgen Sie diese Schritte, um die LBV-API auf Ihrem lokalen System einzurichten und auszuführen.

#### Schritt 1: Klonen des Repositories
Zuerst müssen Sie das LBV-API-Repository von GitHub auf Ihren Computer klonen. Öffnen Sie ein Terminal und führen Sie den folgenden Befehl aus:

```bash
git clone https://github.com/jexxme/groupManagementAPI
```

#### Schritt 2: Installieren der Abhängigkeiten
Wechseln Sie in das Verzeichnis des geklonten Repositories und installieren Sie die erforderlichen Python-Pakete mit pip. Diese Pakete sind in der `requirements.txt` Datei aufgelistet.

```bash
cd groupManagementAPI
pip install -r requirements.txt
```

#### Schritt 3: Einrichten der Umgebungsvariablen
Erstellen Sie eine `.env`-Datei im Wurzelverzeichnis des Projekts, um Ihre Umgebungsvariablen sicher zu speichern. Fügen Sie insbesondere den JWT Secret Key hinzu:

1. Erstellen Sie eine neue Datei namens `.env` im Hauptverzeichnis des Projekts.
2. Fügen Sie die folgende Zeile hinzu und ersetzen Sie `IhrGeheimerSchlüssel` durch Ihren eigenen sicheren Schlüssel:

   ```
   JWT_SECRET_KEY=IhrGeheimerSchlüssel
   ```

#### Schritt 4: Starten der Anwendung
Nachdem Sie die Umgebungsvariablen eingerichtet haben, können Sie die Anwendung starten. Führen Sie dazu den folgenden Befehl im Wurzelverzeichnis des Projekts aus:

```bash
python run.py
```



Die API sollte nun auf `http://localhost:5000` gestartet sein.

Das Dashboard ist unter `http://localhost:5000/` oder `http://localhost:5000/dashboard` erreichbar.

## Dashboard

Das Dashboard ist eine webbasierte Benutzeroberfläche für Administratoren, mit der Sie die LBV-API verwalten können. Es bietet eine Übersicht über die Datenbank und ermöglicht das Erstellen, Aktualisieren und Löschen von Benutzern, Gruppen, Terminen und Benutzern in Gruppen. Das Dashboard ist unter `http://localhost:5000/dashboard` verfügbar.

## Verwendung

Die LBV-API ermöglicht die Verwaltung von Benutzern, Gruppen, Terminen und Benutzern in Gruppen über RESTful-Endpunkte. Jeder Endpunkt akzeptiert HTTP-Anfragemethoden wie GET, POST, PUT und DELETE. Die API erwartet JSON-Daten in den Anfragen und gibt JSON-Antworten zurück.

## Benutzer (Users)


### Erstellen eines Benutzers

- **Endpoint:** `/users`
- **Methode:** `POST`

Erstellt einen neuen Benutzer. Die E-Mail-Adresse des Benutzers muss das Format `@gso.schule.koeln` aufweisen. Außerdem wird überprüft, ob die E-Mail-Adresse bereits existiert. Wenn ja, wird ein Fehler zurückgegeben.

**Anforderungs-JSON-Format:**

```json
{
    "email": "benutzer@gso.schule.koeln",
    "firstName": "Vorname",
    "password": "Passwort"
}
```

**Erfolgsantwort:**

- **Code:** 201 (Created)
- **Inhalt:** 
  ```json
  { "message": "Neuer Benutzer erstellt" }
  ```

**Fehlerantwort bei ungültiger E-Mail-Adresse:**

- **Code:** 400 (Bad Request)
- **Inhalt:** 
  ```json
  { "message": "Es sind nur E-Mails von @gso.schule.koeln erlaubt" }
  ```

**Fehlerantwort bei bereits existierender E-Mail-Adresse:**

- **Code:** 409 (Conflict)
- **Inhalt:** 
  ```json
  { "message": "Ein Benutzer mit dieser E-Mail-Adresse existiert bereits" }
  ```

**Beispiel:**

- **Anfrage:**

  ```json
  {
      "email": "max.mustermann@gso.schule.koeln",
      "firstName": "Max",
      "password": "meinPasswort123"
  }
  ```

- **Antwort bei Erfolg:**

  ```json
  { "message": "Neuer Benutzer erstellt" }
  ```

- **Antwort bei ungültiger E-Mail-Adresse:**

  ```json
  { "message": "Es sind nur E-Mails von @gso.schule.koeln erlaubt" }
  ```

- **Antwort bei bereits existierender E-Mail-Adresse:**

  ```json
  { "message": "Ein Benutzer mit dieser E-Mail-Adresse existiert bereits" }
  ```


### Erstellen eines Administrators

- **Endpoint:** `/admin`
- **Methode:** `POST`

Erstellt einen neuen Administrator. Diese Aktion erfordert Administratorrechte. Gibt eine Bestätigungsnachricht zurück, wenn der Administrator erfolgreich erstellt wurde.

**Anforderungen:**

- Der anfragende Benutzer muss über Administratorrechte verfügen.
- Die Anfrage muss über einen gültigen JWT-Token mit entsprechenden Administratorrechten verfügen.
- Für mehr Details siehe [Authentifizierung](#authentifizierung).

**Anforderungs-JSON-Format:**

```json
{
    "email": "admin@example.com",
    "firstName": "Admin",
    "password": "sicheresPasswort"
}
```

**Erfolgsantwort:**

- **Code:** 201 (Created)
- **Inhalt:** 
  ```json
  { "message": "Neuer Admin erstellt" }
  ```

**Fehlerantwort:**

- **Code:** 401 (Unauthorized) / 403 (Forbidden)
- **Inhalt:** 
  ```json
  { "message": "Unauthorized: Administratorrechte erforderlich" }
  ```

**Beispiel:**

- **Anfrage:**

  ```json
  {
      "email": "neuer.admin@example.com",
      "firstName": "NeuerAdmin",
      "password": "adminPasswort123"
  }
  ```

- **Antwort bei Erfolg:**

  ```json
  { "message": "Neuer Admin erstellt" }
  ```

- **Antwort bei fehlender Autorisierung:**

  ```json
  { "message": "Unauthorized: Administratorrechte erforderlich" }
  ```

### Abrufen aller Benutzer

- **Endpoint:** `/users`
- **Methode:** `GET`

Ruft eine Liste aller Benutzer ab. Jeder Benutzer wird mit seiner Benutzer-ID, E-Mail-Adresse, dem Vornamen, dem Passwort und seinem Admin-Status zurückgegeben.

**Anforderungen:**

- Wird noch herausgefunden...

**Erfolgsantwort:**

- **Code:** 200 (OK)
- **Inhalt:** Liste aller Benutzer in JSON-Format
  ```json
  [
      {
          "userID": 1,
          "email": "benutzer1@example.com",
          "firstName": "Max",
          "password": "passwort123",
          "isAdmin": false
      },
      {
          "userID": 2,
          "email": "benutzer2@example.com",
          "firstName": "Anna",
          "password": "passwort321",
          "isAdmin": true
      }
      // Weitere Benutzer...
  ]
  ```

**Beispiel für die Verwendung:**

Eine GET-Anfrage an den Endpoint `/users` liefert die Liste aller Benutzer in der Datenbank:

```bash
curl -X GET http://127.0.0.1:5000/users
```

### Abrufen eines einzelnen Benutzers

- **Endpoint:** `/users/<userID>`
- **Methode:** `GET`

Gibt die Details eines einzelnen Benutzers anhand seiner `userID` zurück.

### Aktualisieren eines Benutzers

- **Endpoint:** `/users/<userID>`
- **Methode:** `PUT`

Aktualisiert die Details eines Benutzers anhand seiner `userID`. Geben Sie die zu aktualisierenden Felder im JSON-Format an.

**JSON-Daten:**

```json
{
    "email": "neue-email@example.com",
    "firstName": "Neuer Vorname",
    "password": "neuesPasswort123",
    "isAdmin": true
}
```

### Löschen eines Benutzers

- **Endpoint:** `/users/<userID>`
- **Methode:** `DELETE`

Löscht einen Benutzer anhand seiner `userID`.

## Gruppen (Groups)

### Erstellen einer Gruppe

- **Endpoint:** `/groups`
- **Methode:** `POST`

Erstellt eine neue Lerngruppe und gibt eine Bestätigungsnachricht zurück.

**JSON-Daten:**



```json
{
    "ownerID": 1,
    "title": "Mathematik Lerngruppe",
    "description": "Eine Gruppe für Mathematikstudenten",
    "maxUsers": 10
}
```

### Abrufen aller Gruppen

- **Endpoint:** `/groups`
- **Methode:** `GET`

Gibt eine Liste aller Lerngruppen zurück.

### Abrufen einer einzelnen Gruppe

- **Endpoint:** `/groups/<groupID>`
- **Methode:** `GET`

Gibt die Details einer einzelnen Lerngruppe anhand ihrer `groupID` zurück.

### Aktualisieren einer Gruppe

- **Endpoint:** `/groups/<groupID>`
- **Methode:** `PUT`

Aktualisiert die Details einer Lerngruppe anhand ihrer `groupID`. Geben Sie die zu aktualisierenden Felder im JSON-Format an.

**JSON-Daten:**

```json
{
    "title": "Neuer Gruppenname",
    "description": "Neue Beschreibung",
    "maxUsers": 15
}
```

### Löschen einer Gruppe

- **Endpoint:** `/groups/<groupID>`
- **Methode:** `DELETE`

Löscht eine Lerngruppe anhand ihrer `groupID`.

## Termine (Dates)

### Erstellen eines Termins

- **Endpoint:** `/dates`
- **Methode:** `POST`

Erstellt einen neuen Termin für eine Lerngruppe und gibt eine Bestätigungsnachricht zurück.

**JSON-Daten:**

```json
{
    "groupID": 1,
    "date": "2023-12-25 14:00:00",
    "place": "Raum A",
    "maxUsers": 20
}
```

### Abrufen aller Termine

- **Endpoint:** `/dates`
- **Methode:** `GET`

Gibt eine Liste aller Termine zurück.

### Abrufen eines einzelnen Termins

- **Endpoint:** `/dates/<dateID>`
- **Methode:** `GET`

Gibt die Details eines einzelnen Termins anhand seiner `dateID` zurück.

### Aktualisieren eines Termins

- **Endpoint:** `/dates/<dateID>`
- **Methode:** `PUT`

Aktualisiert die Details eines Termins anhand seiner `dateID`. Geben Sie die zu aktualisierenden Felder im JSON-Format an.

**JSON-Daten:**

```json
{
    "date": "2023-12-26 15:30:00",
    "place": "Raum B",
    "maxUsers": 25
}
```

### Löschen eines Termins

- **Endpoint:** `/dates/<dateID>`
- **Methode:** `DELETE`

Löscht einen Termin anhand seiner `dateID`.

## Benutzer in Gruppen (UsersInGroups)

### Hinzufügen eines Benutzers zu einer Gruppe

- **Endpoint:** `/users_in_groups`
- **Methode:** `POST`

Fügt einen Benutzer zu einer Lerngruppe hinzu und gibt eine Bestätigungsnachricht zurück.

**JSON-Daten:**

```json
{
    "userID": 1,
    "groupID": 1,
    "startingDate": "2023-12-01"
}
```

### Abrufen aller Gruppen denen ein User zugewiesen ist

- **Endpoint:** `/users_in_groups/<userID>`
- **Methode:** `GET`

Gibt eine Liste aller Lerngruppen zurück, denen ein Benutzer basierend auf seiner `userID` zugewiesen ist.

### Abrufen aller Benutzer die in einer Gruppe sind 
Siehe /groups/members TODO

### Aktualisieren des Startdatums eines Benutzers in einer Gruppe

- **Endpoint:** `/users_in_groups/<userID>/<groupID>`
- **Methode:** `PUT`

Aktualisiert das Startdatum eines Benutzers in einer Lerngruppe basierend auf seiner `userID` und `groupID`. Geben Sie das neue Datum im JSON-Format an.

**JSON-Daten:**

```json
{
    "startingDate": "2023-12-02"
}
```


### Entfernen eines Benutzers aus einer Gruppe

- **Endpoint:** `/users_in_groups/<userID>/<groupID>`
- **Methode:** `DELETE`

Entfernt einen Benutzer aus einer Lerngruppe basierend auf seiner `userID` und `groupID`.

## Authentifizierung

Die Authentifizierung in der LBV-API ist ein entscheidender Aspekt, um die Sicherheit und Integrität der Anwendung zu gewährleisten. Es wird ein JWT (JSON Web Token)-basiertes Authentifizierungssystem verwendet, das sicherstellt, dass nur berechtigte Benutzer Zugriff auf bestimmte Endpunkte haben. Nachfolgend finden Sie Details zur Implementierung und Verwendung der Authentifizierungsfunktionen.

### Login und JWT-Token

- **Endpoint:** `/login`
- **Methode:** `POST`

Beim Login wird ein JWT-Token generiert, das für nachfolgende Anfragen verwendet wird. Der Token enthält die Benutzer-ID und die Rolle des Benutzers (Admin oder regulärer Benutzer).

**JSON-Daten für Login-Anfrage:**

```json
{
    "email": "benutzer@example.com",
    "password": "Passwort"
}
```

### Token-Verwendung

- Der JWT-Token muss bei jeder Anfrage, die eine Authentifizierung erfordert, im `Authorization`-Header mit dem Präfix `Bearer` mitgeschickt werden.
- Das System unterscheidet zwischen normalen Benutzern und Administratoren. Administratoren haben erweiterte Berechtigungen, wie z.B. das Löschen und Bearbeiten anderer Benutzerkonten.

### Authentifizierung an Endpunkten

- **Admin-spezifische Endpunkte:** Einige Endpunkte sind nur für Administratoren zugänglich. Diese Endpunkte erfordern einen JWT-Token mit Admin-Rechten.
- **Benutzerspezifische Endpunkte:** Benutzer können ihre eigenen Kontodetails sehen und aktualisieren. Ein JWT-Token, das die Identität des Benutzers bestätigt, ist erforderlich.
- **Öffentliche Endpunkte:** Einige Endpunkte, wie das Erstellen eines neuen Benutzerkontos, erfordern keine Authentifizierung.

### Beispiel für eine authentifizierte Anfrage in JavaScript:

```javascript
const url = "http://localhost:5000/beispiel-endpunkt";
const headers = {
    'Authorization': 'Bearer Ihr_JWT_Token_Hier'
};

fetch(url, { headers: headers })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Fehler bei der Anfrage:', error));
```

### Beispiel für eine authentifizierte Anfrage in Python:

```python
import requests

url = "http://localhost:5000/beispiel-endpunkt"
headers = {
    'Authorization': 'Bearer Ihr_JWT_Token_Hier'
}
response = requests.get(url, headers=headers)
```

### Sicherheitshinweise

- Der JWT-Token sollte geheim gehalten und sicher aufbewahrt werden.
- Passwörter werden verschlüsselt gespeichert. Die Übertragung von Passwörtern sollte stets über sichere Verbindungen erfolgen.

Diese Authentifizierungsmechanismen tragen dazu bei, die LBV-API sicher und zuverlässig für  Benutzer zu machen. Sie sorgen dafür, dass jeder Benutzer nur auf die für ihn bestimmten Ressourcen und Funktionen zugreifen kann.

## Tests
Die Testfälle werden nachfolgend nach Kategorie gruppiert und beschrieben, um einen klaren Überblick über die entsprechenden Testfunktionen zu bieten.

### Authentifizierung (/tests/auth/)
| Testdatei                 | Testbeschreibung                                      |
|---------------------------|-------------------------------------------------------|
| `test_add_admin_to_db.py` | Überprüft das Hinzufügen eines Administrators zur Datenbank. |
| `test_admin_login.py`     | Überprüft den Login-Prozess für Administratoren.              |
| `test_user_login.py`      | Überprüft den Login-Prozess für Benutzer.                      |

### Termine (/tests/dates)
| Testdatei                | Testbeschreibung                                      |
|--------------------------|-------------------------------------------------------|
| `test_add_date.py`       | Überprüft das Hinzufügen eines Datums.                         |
| `test_delete_date.py`    | Überprüft das Löschen eines Datums.                            |
| `test_get_dates.py`      | Überprüft das Abrufen aller Daten.                             |
| `test_get_single_date.py`| Überprüft das Abrufen eines einzelnen Datums.                  |
| `test_update_a_date.py`  | Überprüft das Aktualisieren eines Datums.                      |

### Gruppen (/tests/groups)
| Testdatei                        | Testbeschreibung                                      |
|----------------------------------|-------------------------------------------------------|
| `test_create_group.py`           | Überprüft das Erstellen einer Gruppe.                          |
| `test_delete_group.py`           | Überprüft das Löschen einer Gruppe.                            |
| `test_get_all_members_of_group.py` | Überprüft das Abrufen aller Mitglieder einer Gruppe.       |
| `test_get_group.py`              | Überprüft das Abrufen der Details einer Gruppe.                |
| `test_get_groups.py`             | Überprüft das Abrufen aller Gruppen.                           |
| `test_update_group.py`           | Überprüft das Aktualisieren einer Gruppeninformation.          |

### Benutzer (/tests/users)
| Testdatei            | Testbeschreibung                                      |
|----------------------|-------------------------------------------------------|
| `test_add_user.py`   | Überprüft das Hinzufügen eines Benutzers.                      |
| `test_update_user.py`| Überprüft das Aktualisieren eines Benutzerprofils.             |

### Benutzer in Gruppen (/tests/users_in_groups)
| Testdatei                           | Testbeschreibung                                      |
|-------------------------------------|-------------------------------------------------------|
| `test_create_user_in_group.py`      | Überprüft das Hinzufügen eines Benutzers zu einer Gruppe.      |
| `test_delete_user_in_group.py`      | Überprüft das Entfernen eines Benutzers aus einer Gruppe.      |
| `test_get_all_members_of_group.py`  | Überprüft das Abrufen aller Mitglieder einer Gruppe.       |
| `test_read_all_groups_of_a_user.py` | Überprüft das Abrufen aller Gruppen, zu denen ein Benutzer gehört. |
| `test_read_all_users_in_all_groups.py` | Überprüft das Abrufen aller Benutzer in allen Gruppen.   |
| `test_read_single_user_in_group.py` | Überprüft das Abrufen der Informationen eines einzelnen Benutzers in einer Gruppe. |

## Öffentliche API

### Aktuelles Deployment

In diesem Abschnitt wird der Prozess des Deployments der Flask-API auf einem AWS EC2-Instance detailliert beschrieben. Dies beinhaltet die Einrichtung des Servers, der Sicherheitskonfiguration, der Flask-Anwendung, von Nginx als Reverse Proxy, Supervisor zur Prozessverwaltung und die Einrichtung von HTTPS.

#### 1. AWS EC2-Instance einrichten
- **EC2-Instance erstellen:**
  - Wählen Sie das gewünschte Amazon Machine Image (AMI) und den Instance-Typ (z.B. t2.micro).
  - Konfigurieren Sie die Instance-Details, Storage, Tags und die Sicherheitsgruppe.
  - Erlauben Sie den SSH-Zugriff (Port 22), HTTP (Port 80) und HTTPS (Port 443) in den Sicherheitsgruppeneinstellungen.

- **Zugriff auf die EC2-Instance:**
  - Verbinden Sie sich via SSH: `ssh -i /pfad/zum/key.pem ubuntu@ec2-instance-ip`.

#### 2. Flask-Anwendung einrichten
- **Abhängigkeiten installieren:**
  - Aktualisieren Sie die Paketlisten: `sudo apt-get update`.
  - Installieren Sie Python, Pip und andere benötigte Pakete.

- **Flask-App auf EC2-Instance übertragen:**
  - Verwenden Sie SCP, FTP oder Git, um Ihre Flask-App-Dateien auf die EC2-Instance zu übertragen.

- **Flask-App testen:**
  - Führen Sie die Flask-App aus und überprüfen Sie den Zugriff über `http://ec2-instance-ip:port`.

#### 3. Nginx als Reverse Proxy einrichten
- **Nginx installieren:**
  - `sudo apt-get install nginx`.

- **Nginx konfigurieren:**
  - Erstellen Sie eine Konfigurationsdatei in `/etc/nginx/sites-available/` und verlinken Sie sie mit `/etc/nginx/sites-enabled/`.
  - Beispielkonfiguration:

    ```
    server {
        listen 80;
        server_name ihre_domain_oder_ip;

        location / {
            proxy_pass http://localhost:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

  - Überprüfen Sie die Konfiguration mit `sudo nginx -t` und starten Sie Nginx neu: `sudo systemctl restart nginx`.

#### 4. Supervisor zur Prozessverwaltung einrichten
- **Supervisor installieren:**
  - `sudo apt-get install supervisor`.

- **Supervisor-Konfiguration für Flask-App:**
  - Erstellen Sie eine Konfigurationsdatei in `/etc/supervisor/conf.d/`.
  - Beispielkonfiguration:

    ```
    [program:myflaskapp]
    command=/pfad/zur/venv/bin/gunicorn -w 4 run:app -b localhost:5000
    directory=/pfad/zur/flask-app
    user=ubuntu
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/myflaskapp/myflaskapp.err.log
    stdout_logfile=/var/log/myflaskapp/myflaskapp.out.log
    ```

  - Führen Sie `sudo supervisorctl reread`, `sudo supervisorctl update` und `sudo supervisorctl start myflaskapp` aus.

#### 5. HTTPS mit Let's Encrypt und Certbot einrichten
- **Certbot installieren:**
  - `sudo apt-get install certbot python3-certbot-nginx`.

- **SSL-Zertifikat erhalten und einrichten:**
  - Führen Sie `sudo certbot --nginx` aus und folgen Sie den Anweisungen.

- **Automatische Erneuerung einrichten:**
  - Testen Sie den Erneuerungsprozess mit `sudo certbot renew --dry-run`.

#### 6. Zusätzliche Befehle und Überprüfungen
- **Nginx Konfiguration testen:**
  - `sudo nginx -t`.

- **Nginx neu starten:**
  - `sudo systemctl restart nginx`.

- **Supervisor Status überprüfen:**
  - `sudo supervisorctl status myflaskapp`.
