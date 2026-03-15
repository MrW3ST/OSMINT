# Overpass Extractor

Outil local d'extraction et de transformation de données OpenStreetMap via l'API Overpass.
Interface web avec thème clair / Dracula dark.

---

## Fonctionnalités

- **Générateur de requête** — formulaire simple (ville + type de lieu) qui produit automatiquement la requête Overpass QL
- **Exécution directe** — envoie la requête à l'API Overpass et récupère les résultats (formats `[out:json]` et `[out:csv]` supportés)
- **Sélection des champs** — cocher/décocher : Nom, Téléphone, Type de lieu, Latitude, Longitude
- **Transformation des numéros** — 3 formats au choix :
  - Brut : `+33 2 41 21 09 21`
  - Normalisé : `02 41 21 09 21`
  - Masqué : `02 ** ** ** **`
- **Export** — TXT (tabulations), CSV (compatible Excel, BOM UTF-8), JSON
- **Aperçu live** — tableau des 100 premiers résultats, mis à jour en temps réel
- **Thème** — clair ou Dracula dark, mémorisé entre les sessions

---

## Installation

**Prérequis :** Python 3.10+

```bash
cd extract_overpass_phonenumber
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
extract_overpass_phonenumber/
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
