# LBV - Lerngruppen Bildung und Verwaltung API

Die LBV (Lerngruppen Bildung und Verwaltung) API ist eine RESTful-Webanwendung, die entwickelt wurde, um die Verwaltung von Lerngruppen und Benutzern zu erleichtern. Sie ermöglicht die Erstellung, Aktualisierung und Löschung von Benutzern, Gruppen und Terminen. Diese Dokumentation bietet eine umfassende Übersicht über die verfügbaren Endpunkte, ihre Verwendung und die erwarteten Datenstrukturen.

## Inhaltsverzeichnis

1. [Allgemeine Informationen](#allgemeine-informationen)
2. [Installation](#installation)
3. [Verwendung](#verwendung)
4. [Benutzer (Users)](#benutzer-users)
   - [Erstellen eines Benutzers](#erstellen-eines-benutzers)
   - [Abrufen aller Benutzer](#abrufen-aller-benutzer)
   - [Abrufen eines einzelnen Benutzers](#abrufen-eines-einzelnen-benutzers)
   - [Aktualisieren eines Benutzers](#aktualisieren-eines-benutzers)
   - [Löschen eines Benutzers](#löschen-eines-benutzers)
5. [Gruppen (Groups)](#gruppen-groups)
   - [Erstellen einer Gruppe](#erstellen-einer-gruppe)
   - [Abrufen aller Gruppen](#abrufen-aller-gruppen)
   - [Abrufen einer einzelnen Gruppe](#abrufen-einer-einzelnen-gruppe)
   - [Aktualisieren einer Gruppe](#aktualisieren-einer-gruppe)
   - [Löschen einer Gruppe](#löschen-einer-gruppe)
6. [Termine (Dates)](#termine-dates)
   - [Erstellen eines Termins](#erstellen-eines-termins)
   - [Abrufen aller Termine](#abrufen-aller-termine)
   - [Abrufen eines einzelnen Termins](#abrufen-eines-einzelnen-termins)
   - [Aktualisieren eines Termins](#aktualisieren-eines-termins)
   - [Löschen eines Termins](#löschen-eines-termins)

## Allgemeine Informationen

Die LBV-API wurde entwickelt, um die Verwaltung von Lerngruppen und Benutzern in einer Bildungsumgebung zu unterstützen. Sie bietet folgende Hauptfunktionen:

- **Benutzerverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Benutzerkonten.
- **Gruppenverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Lerngruppen.
- **Terminverwaltung:** Erstellen, Aktualisieren, Abrufen und Löschen von Terminen für Lerngruppen.

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

Die LBV-API ermöglicht die Verwaltung von Benutzern, Gruppen und Terminen über RESTful-Endpunkte. Jeder Endpunkt akzeptiert HTTP-Anfragemethoden wie GET, POST, PUT und DELETE. Die API erwartet JSON-Daten in den Anfragen und gibt JSON-Antworten zurück.

## Benutzer (Users)

### Erstellen eines Benutzers

- **Endpoint:** `/users`
- **Methode:** `POST`

Erstellt einen neuen Benutzer und gibt eine Bestätigungsnachricht zurück.

**JSON-Daten:**

```json
{
    "email": "benutzer@example.com",
    "firstName": "Vorname",
    "password": "Passwort",
    "isAdmin": false
}
```

### Abrufen aller Benutzer

- **Endpoint:** `/users`
- **Methode:** `GET`

Gibt eine Liste aller Benutzer zurück.

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
- **Methode

:** `POST`

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

## Authentifizierung

_Wurde noch nicht implementiert_

## Beispiele

_TODO_
