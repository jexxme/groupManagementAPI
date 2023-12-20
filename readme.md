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
TODO Tests
10. [Beispiele](#beispiele)


## Allgemeine Informationen

Die LBV-API wurde entwickelt, um die Verwaltung von Lerngruppen und Benutzern in einer Bildungsumgebung zu unterstützen. Sie bietet folgende Hauptfunktionen:

- **Benutzerverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Benutzerkonten.
- **Gruppenverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Lerngruppen.
- **Terminverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Terminen für Lerngruppen.
- **Verwaltung von Benutzern in Gruppen:** Hinzufügen, Abrufen, Aktualisieren und Entfernen von Benutzern in Gruppen.

Die API verwendet das JSON-Format für Anfragen und Antworten.

## Installation

1. Klone das LBV-API-Repository von GitHub:

   ```bash
   git clone https://github.com/jexxme/apiForOSP
   ```

2. Installiere die erforderlichen Python-Pakete aus der `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

3. Führe die Anwendung aus:

   ```bash
   python run.py
   ```

Die API sollte nun auf `http://localhost:5000` gestartet sein.

## Verwendung

Die LBV-API ermöglicht die Verwaltung von Benutzern, Gruppen, Terminen und Benutzern in Gruppen über RESTful-Endpunkte. Jeder Endpunkt akzeptiert HTTP-Anfragemethoden wie GET, POST, PUT und DELETE. Die API erwartet JSON-Daten in den Anfragen und gibt JSON-Antworten zurück.

## Benutzer (Users)

### Erstellen eines Benutzers

- **Endpoint:** `/users`
- **Methode:** `POST`

Erstellt einen neuen Benutzer. Die E-Mail-Adresse des Benutzers muss das Format `@gso.schule.koeln` aufweisen. Gibt eine Bestätigungsnachricht zurück, wenn der Benutzer erfolgreich erstellt wurde. Andernfalls wird eine Fehlermeldung ausgegeben, falls die E-Mail-Adresse nicht dem erforderlichen Muster entspricht.

**Anforderungs-JSON-Format:**

```json
{
    "email": "benutzer@gso.schule.koeln",
    "firstName": "Vorname",
    "password": "Passwort",
    "isAdmin": false
}
```

**Erfolgsantwort:**

- **Code:** 201 (Created)
- **Inhalt:** 
  ```json
  { "message": "Neuer Benutzer erstellt" }
  ```

**Fehlerantwort:**

- **Code:** 400 (Bad Request)
- **Inhalt:** 
  ```json
  { "message": "Es sind nur E-Mails von @gso.schule.koeln erlaubt" }
  ```

**Beispiel:**

- **Anfrage:**

  ```json
  {
      "email": "max.mustermann@gso.schule.koeln",
      "firstName": "Max",
      "password": "meinPasswort123",
      "isAdmin": false
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

### Erstellen eines Administrators

- **Endpoint:** `/admin`
- **Methode:** `POST`

Erstellt einen neuen Administrator. Diese Aktion erfordert Administratorrechte. Gibt eine Bestätigungsnachricht zurück, wenn der Administrator erfolgreich erstellt wurde.

**Anforderungen:**

- Der anfragende Benutzer muss über Administratorrechte verfügen.
- Die Anfrage muss über einen gültigen JWT-Token mit entsprechenden Administratorrechten verfügen.

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

### Abrufen aller Benutzer in einer Gruppe

- **Endpoint:** `/users_in_groups/<groupID>`
- **Methode:** `GET`

Gibt eine Liste aller Benutzer in einer Lerngruppe zurück, basierend auf der `groupID`.

### Aktualisieren des Startdatums eines Benutzers in einer Gruppe

- **Endpoint:** `/users_in_groups/<userID>/<groupID>`
- **Methode:** `PUT`

Aktualisiert das Startdatum eines Benutzers in einer Gruppe basierend auf seiner `userID` und `groupID`. Geben Sie das zu aktualisierende Startdatum im JSON-Format an.

**JSON-Daten:**

```json
{
    "startingDate": "2023-12-15"
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

### Beispiel für eine authentifizierte Anfrage:

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


## TODO
-Alle Routen durch JWT-Token schützen 
-Bisher erst nach dem Login

## Beispiele

_TODO_