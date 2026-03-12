# Todo List

Une application en ligne de commande pour gérer ses tâches avec des niveaux de priorité.

## Fonctionnalités

- Ajouter une tâche avec une description et une priorité (haute, moyenne, basse)
- Afficher toutes les tâches avec leur priorité et leur date de création
- Supprimer une tâche par son numéro
- Sauvegarde automatique dans un fichier JSON

## Installation

### Prérequis

- Python 3.6 ou supérieur

### Cloner le projet

```bash
git clone https://github.com/Nanfer11/todo-list.git
cd todo-list
```

Aucune dépendance externe à installer, le projet utilise uniquement la bibliothèque standard Python.

## Utilisation

Toutes les commandes s'exécutent depuis la racine du projet.

### Ajouter une tâche

```bash
python src/todo.py ajouter <description> [priorité]
```

La priorité est optionnelle, elle vaut `moyenne` par défaut. Valeurs possibles : `haute`, `moyenne`, `basse`.

```bash
# Ajouter une tâche avec priorité moyenne (par défaut)
python src/todo.py ajouter "Lire la documentation"

# Ajouter une tâche avec priorité haute
python src/todo.py ajouter "Corriger le bug de connexion" haute

# Ajouter une tâche avec priorité basse
python src/todo.py ajouter "Ranger le bureau" basse
```

### Afficher les tâches

```bash
python src/todo.py liste
```

Exemple de sortie :

```
  1. [HAUTE]  [12/03/2026 09:00] Corriger le bug de connexion
  2. [MOY.]   [12/03/2026 09:05] Lire la documentation
  3. [BASSE]  [12/03/2026 09:10] Ranger le bureau
```

### Supprimer une tâche

```bash
python src/todo.py supprimer <numéro>
```

```bash
# Supprimer la tâche numéro 2
python src/todo.py supprimer 2
```

## Structure du projet

```
todo-list/
├── src/
│   └── todo.py        # Code source principal
├── data/
│   └── taches.json    # Sauvegarde des tâches
├── tests/             # Tests (à venir)
├── docs/              # Documentation (à venir)
└── README.md
```
