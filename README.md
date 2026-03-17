# OSMINT

> **Outil local d'extraction et de transformation de données OpenStreetMap via l'API Overpass.**
> Interface web avec thème clair / Dracula dark — by **MrW3ST**

---

## Fonctionnalités

- **Générateur de requête** — formulaire simple (ville + type de lieu) qui produit automatiquement la requête Overpass QL
- **Exécution directe** — envoie la requête à l'API Overpass et récupère les résultats (formats `[out:json]` et `[out:csv]` supportés)
- **Sélection des champs** — cocher/décocher : Nom, Téléphone, Type de lieu, Latitude, Longitude
- **Transformation des numéros** — 3 formats au choix :
- **Export** — TXT (tabulations), CSV (compatible Excel, BOM UTF-8), JSON
- **Aperçu live** — tableau des 100 premiers résultats, mis à jour en temps réel
- **Thème** — clair ou Dracula dark, mémorisé entre les sessions

---

## Installation

**Prérequis :** Python 3.10+

```bash
cd OSMINT
pip install -r requirements.txt
```

---

## Lancement

```bash
python3 app.py
```

Le navigateur s'ouvre automatiquement sur `http://localhost:5000`.
Pour quitter, utilisez le bouton **✕ Quitter** dans l'interface.

---

## Utilisation

### 1. Générer une requête automatiquement

Remplir le formulaire en haut de page :

| Champ | Exemple |
|---|---|
| Ville / Zone | `Angers` |
| Type de lieu | `Restaurant`, `Pharmacie`, `Hôtel`… |
| Personnalisé | Clé OSM + Valeur (ex: `shop` / `florist`) |

Cocher **"Seulement les lieux avec numéro de téléphone"** pour ne récupérer que les entrées avec un contact.
Cliquer **⚡ Générer la requête** — le textarea se remplit automatiquement.

> Le nom de ville doit correspondre exactement à celui d'OpenStreetMap.
> En cas de doute, vérifier sur [openstreetmap.org](https://www.openstreetmap.org).

### 2. Exécuter manuellement

Coller directement une requête Overpass QL dans le textarea. Les formats `[out:json]` et `[out:csv(...)]` sont tous les deux acceptés.

Cliquer **▶ Exécuter la requête**.

### 3. Configurer l'export

- **Champs** — sélectionner les colonnes à inclure
- **Format téléphone** — choisir entre brut, normalisé ou masqué
- **Format fichier** — TXT, CSV ou JSON

Cliquer **↓ Exporter** pour télécharger le fichier.

---

## Structure du projet

```
OSMINT/
├── app.py               # Serveur Flask + parsing JSON/CSV Overpass
├── requirements.txt
└── templates/
    └── index.html       # Interface complète (HTML/CSS/JS)
```

---

## Dépendances

| Package | Rôle |
|---|---|
| `flask` | Serveur web local |
| `requests` | Appels à l'API Overpass |

---

## Notes

- L'API Overpass est publique et gratuite — éviter les requêtes trop larges (grande bbox + pas de filtre) qui peuvent dépasser le timeout de 90s.
- Les numéros courts (type `3631`) sont ignorés lors de la normalisation.
- Les lignes sans aucune valeur sont automatiquement exclues de l'export.

---

---

# OSMINT — English

> **Local tool for extracting and transforming OpenStreetMap data via the Overpass API.**
> Web interface with light / Dracula dark theme — by **MrW3ST**

---

## Features

- **Query generator** — simple form (city + place type) that automatically builds the Overpass QL query
- **Direct execution** — sends the query to the Overpass API and retrieves results (both `[out:json]` and `[out:csv]` formats supported)
- **Field selection** — toggle on/off: Name, Phone, Place type, Latitude, Longitude
- **Phone number formatting**:
- **Export** — TXT (tab-separated), CSV (Excel-compatible, UTF-8 BOM), JSON
- **Live preview** — table of the first 100 results, updated in real time
- **Theme** — light or Dracula dark, remembered between sessions

---

## Installation

**Requirements:** Python 3.10+

```bash
cd OSMINT
pip install -r requirements.txt
```

---

## Running

```bash
python3 app.py
```

The browser opens automatically at `http://localhost:5000`.
To quit, use the **✕ Quit** button in the interface.

---

## Usage

### 1. Auto-generate a query

Fill in the form at the top of the page:

| Field | Example |
|---|---|
| City / Area | `Angers` |
| Place type | `Restaurant`, `Pharmacy`, `Hotel`… |
| Custom | OSM key + value (e.g. `shop` / `florist`) |

Check **"Only places with a phone number"** to retrieve only entries with a contact.
Click **⚡ Generate query** — the textarea fills automatically.

> The city name must match exactly how it appears on OpenStreetMap.
> If unsure, check on [openstreetmap.org](https://www.openstreetmap.org).

### 2. Run a query manually

Paste any Overpass QL query directly into the textarea. Both `[out:json]` and `[out:csv(...)]` formats are accepted.

Click **▶ Run query**.

### 3. Configure the export

- **Fields** — select which columns to include
- **Phone format** — choose between raw, normalized, or masked
- **File format** — TXT, CSV, or JSON

Click **↓ Export** to download the file.

---

## Project structure

```
OSMINT/
├── app.py               # Flask server + Overpass JSON/CSV parsing
├── requirements.txt
└── templates/
    └── index.html       # Full interface (HTML/CSS/JS)
```

---

## Dependencies

| Package | Role |
|---|---|
| `flask` | Local web server |
| `requests` | Overpass API calls |

---

## Notes

- The Overpass API is public and free — avoid overly broad queries (large bounding box + no filter) that may exceed the 90s timeout.
- Short numbers (e.g. `3631`) are ignored during normalization.
- Rows with no values are automatically excluded from the export.
