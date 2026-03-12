import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

FICHIER_TACHES = Path(__file__).parent.parent / "data" / "taches.json"
DOSSIER_STATIC = Path(__file__).parent / "static"
PRIORITES_VALIDES = ("haute", "moyenne", "basse")
PORT = 8000


def charger_taches():
    if FICHIER_TACHES.exists():
        return json.loads(FICHIER_TACHES.read_text(encoding="utf-8"))
    return []


def sauvegarder_taches(taches):
    FICHIER_TACHES.write_text(json.dumps(taches, ensure_ascii=False, indent=2), encoding="utf-8")


class GestionnaireTaches(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    def envoyer_json(self, code, donnees):
        contenu = json.dumps(donnees, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(contenu))
        self.end_headers()
        self.wfile.write(contenu)

    def do_GET(self):
        chemin = urlparse(self.path).path

        if chemin == "/" or chemin == "/index.html":
            fichier = DOSSIER_STATIC / "index.html"
            contenu = fichier.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(contenu))
            self.end_headers()
            self.wfile.write(contenu)

        elif chemin == "/api/taches":
            self.envoyer_json(200, charger_taches())

        else:
            self.envoyer_json(404, {"erreur": "Page introuvable"})

    def do_POST(self):
        if self.path != "/api/taches":
            self.envoyer_json(404, {"erreur": "Route introuvable"})
            return

        longueur = int(self.headers.get("Content-Length", 0))
        corps = json.loads(self.rfile.read(longueur).decode("utf-8"))

        description = corps.get("description", "").strip()
        priorite = corps.get("priorite", "moyenne")

        if not description:
            self.envoyer_json(400, {"erreur": "La description est obligatoire."})
            return
        if priorite not in PRIORITES_VALIDES:
            self.envoyer_json(400, {"erreur": f"Priorité invalide : {priorite}"})
            return

        taches = charger_taches()
        tache = {
            "description": description,
            "priorite": priorite,
            "date_creation": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        taches.append(tache)
        sauvegarder_taches(taches)
        self.envoyer_json(201, tache)

    def do_DELETE(self):
        chemin = urlparse(self.path).path
        parties = chemin.strip("/").split("/")

        # Attend /api/taches/<numero>
        if len(parties) != 3 or parties[0] != "api" or parties[1] != "taches":
            self.envoyer_json(404, {"erreur": "Route introuvable"})
            return

        try:
            numero = int(parties[2])
        except ValueError:
            self.envoyer_json(400, {"erreur": "Numéro invalide"})
            return

        taches = charger_taches()
        if numero < 1 or numero > len(taches):
            self.envoyer_json(400, {"erreur": f"Numéro invalide : {numero}"})
            return

        supprimee = taches.pop(numero - 1)
        sauvegarder_taches(taches)
        self.envoyer_json(200, {"message": f"Tâche supprimée : {supprimee['description']}"})


if __name__ == "__main__":
    serveur = HTTPServer(("localhost", PORT), GestionnaireTaches)
    print(f"Serveur démarré sur http://localhost:{PORT}")
    print("Appuyez sur Ctrl+C pour arrêter.")
    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrêté.")
        sys.exit(0)
