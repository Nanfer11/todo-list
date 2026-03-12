import json
import sys
from datetime import datetime
from pathlib import Path

FICHIER_TACHES = Path(__file__).parent / "taches.json"
PRIORITES_VALIDES = ("haute", "moyenne", "basse")
AFFICHAGE_PRIORITE = {"haute": "[HAUTE]", "moyenne": "[MOY.]", "basse": "[BASSE]"}


def charger_taches():
    if FICHIER_TACHES.exists():
        return json.loads(FICHIER_TACHES.read_text(encoding="utf-8"))
    return []


def sauvegarder_taches(taches):
    FICHIER_TACHES.write_text(json.dumps(taches, ensure_ascii=False, indent=2), encoding="utf-8")


def ajouter_tache(description, priorite="moyenne"):
    if priorite not in PRIORITES_VALIDES:
        print(f"Erreur : priorité invalide '{priorite}'. Choisir parmi : haute, moyenne, basse.")
        sys.exit(1)
    taches = charger_taches()
    tache = {
        "description": description,
        "priorite": priorite,
        "date_creation": datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    taches.append(tache)
    sauvegarder_taches(taches)
    print(f"Tâche ajoutée ({priorite}) : {description}")


def afficher_taches():
    taches = charger_taches()
    if not taches:
        print("Aucune tâche pour le moment.")
        return
    for i, tache in enumerate(taches, start=1):
        priorite = tache.get("priorite", "moyenne")
        label = AFFICHAGE_PRIORITE[priorite]
        print(f"  {i}. {label} [{tache['date_creation']}] {tache['description']}")


def supprimer_tache(numero):
    taches = charger_taches()
    if numero < 1 or numero > len(taches):
        print(f"Numéro invalide : {numero}")
        return
    supprimee = taches.pop(numero - 1)
    sauvegarder_taches(taches)
    print(f"Tâche supprimée : {supprimee['description']}")


def afficher_aide():
    print("Usage :")
    print("  python todo.py ajouter <description> [priorité]  Ajouter une tâche (priorité : haute, moyenne, basse)")
    print("  python todo.py liste                              Afficher toutes les tâches")
    print("  python todo.py supprimer <numéro>                Supprimer une tâche par son numéro")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        afficher_aide()
        sys.exit(0)

    commande = sys.argv[1]

    if commande == "ajouter":
        if len(sys.argv) < 3:
            print("Erreur : précise une description pour la tâche.")
            sys.exit(1)
        # Dernière arg = priorité si elle fait partie des valeurs valides
        if sys.argv[-1] in PRIORITES_VALIDES and len(sys.argv) > 3:
            priorite = sys.argv[-1]
            description = " ".join(sys.argv[2:-1])
        else:
            priorite = "moyenne"
            description = " ".join(sys.argv[2:])
        ajouter_tache(description, priorite)

    elif commande == "liste":
        afficher_taches()

    elif commande == "supprimer":
        if len(sys.argv) < 3 or not sys.argv[2].isdigit():
            print("Erreur : précise le numéro de la tâche à supprimer.")
            sys.exit(1)
        supprimer_tache(int(sys.argv[2]))

    else:
        print(f"Commande inconnue : {commande}")
        afficher_aide()
        sys.exit(1)
