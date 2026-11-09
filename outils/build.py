#!/usr/bin/env python3
"""Construit le site Technologie 5e à partir de l'export du Google Site."""
import json, os, re, shutil, sys

SRC = sys.argv[1]
OUT = sys.argv[2]
D = json.load(open(SRC, encoding="utf-8"))

def code(i, j=0):
    return [b for b in D[i]["blocks"] if b["k"] == "code"][j]["code"]

def drives(i):
    return [b for b in D[i]["blocks"] if b["k"] == "drive"]

def imgs(i):
    return [b["u"] for b in D[i]["blocks"] if b["k"] == "img"]

BACK = ('<a href="../index.html" style="position:fixed;bottom:16px;left:16px;z-index:99999;'
        'background:#0f5c4d;color:#fff;padding:10px 16px;border-radius:24px;'
        'font:600 14px system-ui,sans-serif;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.25)">'
        '← Retour au site</a>')

GC = '<script data-goatcounter="https://mrassi-techno5e.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'

def write_activity(rel, html, title):
    if "<html" not in html[:400].lower():
        html = ('<!DOCTYPE html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
                f'<title>{title}</title>\n</head>\n<body>\n{html}\n</body>\n</html>\n')
    if "</body>" in html:
        k = html.rfind("</body>")
        html = html[:k] + BACK + "\n" + GC + html[k:]
    else:
        html += BACK + GC
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(html)
    return rel

# ---------- types de documents Drive ----------
def dtype(name):
    n = name.lower()
    if n.endswith(".mp4"): return "VIDEO"
    if "synth" in n: return "SYNTHESE"
    if "correct" in n or "corrige" in n: return "CORRIGE"
    if "tuto" in n or "televerser" in n: return "TUTO"
    if "evaluation" in n: return "EVAL"
    if n.endswith(".pdf"): return "DOC"
    return "FICHIER"

def pretty(name):
    n = re.sub(r"^Drive, ", "", name).strip()
    n = re.sub(r"\.(pdf|mp4|ods|fls|url)$", "", n, flags=re.I)
    n = n.replace("_", " ").replace("  ", " ").strip()
    n = n.replace("D4INFORMATION", "D'INFORMATION").replace(" d erreur", " d'erreur")
    return n[:1].upper() + n[1:]

def ext(name):
    m = re.search(r"\.(\w+)$", name)
    return m.group(1).upper() if m else ""

def doc(b, titre=None, sous=None, typ=None):
    name = re.sub(r"^Drive, ", "", b["name"])
    t = typ or dtype(name)
    e = ext(name)
    s = sous or {"VIDEO": "Vidéo", "FICHIER": f"Fichier {e} à télécharger"}.get(t, f"Document {e}".strip())
    mode = "dl" if e in ("ODS", "FLS", "URL") else "view"
    return {"k": t, "t": titre or pretty(name), "s": s, "drive": b["id"], "mode": mode}

def act(rel, html, titre, sous, typ="ACTIVITE"):
    write_activity(rel, html, titre)
    return {"k": typ, "t": titre, "s": sous, "h": rel}

# ---------- contenu ----------
S = []

# ===== Séquence 1 =====
s1 = {"id": "seq1", "n": "1", "t": "Les données numériques",
      "o": ["Savoir où sont rangées les données numériques (ordinateur, clé USB, cloud…)",
            "Ranger ses fichiers dans des dossiers bien nommés (l'arborescence)",
            "Connaître les unités de taille d'un fichier : octet, Ko, Mo, Go",
            "Se protéger : mots de passe solides, repérer le phishing",
            "Respecter le travail des autres : plagiat et droit d'auteur"],
      "seances": []}
p = drives(2)
s1["seances"].append({"t": "Séance 1 — Où sont les données numériques ?", "items": [
    act("seq1/01_Activite_Classeur_numerique_localisation_donnees.html", code(2),
        "Classeur numérique & localisation des données", "Activité interactive de la séance"),
    doc(p[0], "Activité 1 — Le classeur numérique", "Fiche d'activité (PDF)", "DOC"),
    doc(p[1], "Activité 2 — Où sont les données ?", "Fiche d'activité (PDF)", "DOC"),
    doc(p[2], "Diaporama de la séance 1", "Document (PDF)", "DOC"),
    doc(p[3], "Activité 2 — Les données numériques", "Document (PDF)", "DOC"),
    act("seq1/02_Tuto_Drive.html", code(3), "Tuto Drive", "Je crée mes dossiers de Technologie pas à pas", "TUTO"),
    doc(drives(3)[0], "Arborescence du Drive de Technologie 5e", "Modèle à suivre (PDF)", "DOC"),
    act("seq1/03_Tuto_video_Organiser_mon_Drive.html", code(4), "Tuto vidéo — Organiser mon Drive", "Je regarde et je fais pareil", "TUTO"),
    doc(drives(4)[0], "Vidéo : bien tenir son Drive en 5e", "Vidéo", "VIDEO"),
    act("seq1/04_Jeu_Range_l_armoire_arborescence.html", code(5), "Range l'armoire ! Le jeu de l'arborescence", "Exercice interactif", "JEU"),
    act("seq1/05_Synthese_Arborescence_Drive.html", code(6), "Synthèse — L'arborescence du Drive", "Je retiens l'essentiel de la séance 1", "SYNTHESE"),
    doc(drives(6)[0], "L'armoire et l'arborescence", "Synthèse (PDF)", "SYNTHESE"),
    doc(drives(6)[1], "Conversion des octets", "Exercice (PDF)", "DOC"),
]})
p = drives(7)
s1["seances"].append({"t": "Séance 2 — Cybersécurité", "items": [
    act("seq1/06_Seance2_Fichiers_taille_mots_de_passe.html", code(7), "Fichiers, taille & mots de passe", "Activité interactive de la séance 2"),
    doc(p[0], "Présentation : la cybersécurité", "Diaporama (PDF)", "DOC"),
    doc(p[1], "Les mots de passe", "Document (PDF)", "DOC"),
    doc(p[2], "Politique de gestion des mots de passe", "Document (PDF)", "DOC"),
    doc(p[3], "Que faire en cas de cyberattaque ?", "Document (PDF)", "DOC"),
    act("seq1/07_Synthese_Seance2_Cybersecurite.html", code(8), "Synthèse — Fichiers, taille et mots de passe", "Je retiens l'essentiel de la séance 2", "SYNTHESE"),
]})
p = drives(9)
s1["seances"].append({"t": "Séance 3 — Le phishing (hameçonnage)", "items": [
    act("seq1/08_Seance3_Phishing_hameconnage.html", code(9), "Phishing & hameçonnage", "Activité interactive de la séance 3"),
    doc(p[0], "Le phishing", "Diaporama (PDF)", "DOC"),
    doc(p[1], "Cyberattaque avec Netsim", "Document (PDF)", "DOC"),
    doc(p[2], "L'hameçonnage : comment pêcher un naïf ?", "Vidéo", "VIDEO"),
    doc(p[3], "Le faux message « Réception colis »", "Vidéo", "VIDEO"),
    act("seq1/09_Synthese_Seance3_Phishing.html", code(10), "Synthèse — Le phishing", "Je retiens l'essentiel de la séance 3", "SYNTHESE"),
]})
p = drives(11)
s1["seances"].append({"t": "Séances 4 et 5 — Plagiat et droit d'auteur (Hadopi)",
    "note": ["Le logiciel BDnF s'installe directement sur la clé USB."], "items": [
    act("seq1/10_Installer_BDnF.html", code(11, 0), "Installer BDnF", "Je mets le logiciel de BD sur ma clé USB", "LOGICIEL"),
    act("seq1/11_BDnF_BD_cyberharcelement.html", code(11, 1), "Fabrique ta BD sur le cyberharcèlement", "Activité avec le logiciel BDnF"),
    doc(p[0], "Le plagiat", "Diaporama (PDF)", "DOC"),
    doc(p[2], "Fiche 1 — Qu'est-ce qu'une œuvre protégée ?", "Synthèse (PDF)", "SYNTHESE"),
    doc(p[4], "Fiche 6 — Trouver des ressources sur Internet", "Synthèse (PDF)", "SYNTHESE"),
    doc(p[3], "Fiche 7 — Le téléchargement illégal", "Synthèse (PDF)", "SYNTHESE"),
    doc(p[5], "Plagiat : une fraude courante", "Lien à ouvrir", "FICHIER"),
    doc(p[6], "Le plagiat expliqué en vidéo", "Vidéo", "VIDEO"),
    doc(p[7], "Hadopi en vidéo", "Vidéo", "VIDEO"),
    doc(p[1], "Évaluation de la séquence", "Évaluation (PDF)", "EVAL"),
]})
s1["seances"].append({"t": "📝 Préparer l'évaluation", "items": [
    act("seq1/12_Fiche_revision_Fichiers_dossiers_cybersecurite.html", code(12),
        "Fiche de révision — Fichiers, dossiers & cybersécurité", "Tout ce qu'il faut savoir pour l'évaluation", "SYNTHESE"),
]})
S.append(s1)

# ===== Séquence 2 =====
s2 = {"id": "seq2", "n": "2", "t": "Le réseau informatique",
      "o": ["Reconnaître le matériel d'un réseau : ordinateur, switch, routeur, serveur",
            "Comprendre à quoi sert une adresse IP",
            "Simuler un petit réseau avec le logiciel Filius",
            "Ajouter un ordinateur dans un réseau et lui donner une adresse"],
      "seances": []}
p = drives(14)
s2["seances"].append({"t": "Séance 1 — Découvrir le réseau", "img": imgs(14), "items": [
    doc(p[0], "Fiche de la séance 1", "Document (PDF)", "DOC"),
    doc(p[1], "Le réseau du collège PMF", "Fiche (PDF)", "DOC"),
    {"k": "VIDEO", "t": "Vidéo : comment fonctionne un réseau ?", "s": "Vidéo YouTube", "yt": "5AVY6E-7yCc"},
]})
p = drives(15)
s2["seances"].append({"t": "Séance 2 — Le réseau du collège", "img": imgs(15),
    "note": ["Le logiciel Filius sert à simuler un réseau. Tu peux l'installer à la maison avec le lien ci-dessous."],
    "links": [["💾 Télécharger Filius (site officiel)", "https://freischlad.name/Herunterladen"]], "items": [
    act("seq2/01_Seance2_Reseau_informatique_du_college.html", code(15), "Le réseau informatique du collège", "Activité interactive de la séance 2"),
    doc(p[0], "Fiche de la séance 2", "Document (PDF)", "DOC"),
    doc(p[1], "Le masque et l'adresse IP", "Fiche (PDF)", "DOC"),
    doc(p[2], "Le matériel du réseau", "Fiche (PDF)", "DOC"),
]})
p = drives(16)
s2["seances"].append({"t": "Séance 3 — Ajouter un ordinateur au réseau", "items": [
    act("seq2/02_Seance3_Ajouter_station_adresser_reseau.html", code(16), "Ajouter une station et donner les adresses", "Activité interactive de la séance 3"),
    doc(p[0], "Fiche de la séance 3", "Document (PDF)", "DOC"),
    doc(p[1], "Entraînement : masque et adresse IP", "Exercices (PDF)", "DOC"),
    doc(p[2], "Fichier Filius du réseau", "Fichier .fls à ouvrir avec Filius", "FICHIER"),
]})
p = drives(17)
s2["seances"].append({"t": "🧠 Synthèse de la séquence", "items": [
    act("seq2/03_Synthese_Reseaux_informatiques.html", code(17), "Synthèse — Les réseaux informatiques", "Je retiens l'essentiel de la séquence", "SYNTHESE"),
    doc(p[0], "L'architecture d'un réseau et d'Internet", "Synthèse (PDF)", "SYNTHESE"),
    doc(p[1], "L'adressage IP", "Synthèse (PDF)", "SYNTHESE"),
]})
S.append(s2)

# ===== Séquence 3 =====
s3 = {"id": "seq3", "n": "3", "t": "Modélisation 3D : support de sac à dos",
      "o": ["Découvrir les procédés de fabrication",
            "Dessiner une pièce en 3D avec Onshape",
            "Tester la solidité d'une pièce (test de flexion)",
            "Choisir un matériau et une épaisseur adaptés",
            "Exporter sa pièce pour l'imprimer en 3D (fichier STL)"],
      "seances": []}
s3["seances"].append({"t": "Séances 0, 1 et 2 — Les procédés de fabrication",
    "note": [D[19]["blocks"][1]["t"], D[19]["blocks"][2]["t"]], "items": [
    doc(drives(19)[0], "Les procédés de fabrication", "Corrigé (PDF)", "CORRIGE"),
]})
s3["seances"].append({"t": "Initiation à Onshape", "img": imgs(21),
    "note": ["Crée ton compte Onshape avec ton adresse mail ert."],
    "links": [["🧊 Aller sur Onshape (créer mon compte)", "https://www.onshape.com/fr/"]], "items": [
    doc(drives(21)[0], "Cours : la modélisation 3D avec Onshape", "Cours (PDF)", "DOC"),
    doc(drives(22)[0], "Tuto vidéo Onshape", "Vidéo", "VIDEO"),
    doc(drives(23)[0], "Simulation : la force et les matériaux", "Vidéo", "VIDEO"),
    doc(drives(24)[0], "Tutoriel : modifier l'épaisseur", "Tutoriel (PDF)", "TUTO"),
    doc(drives(24)[1], "Tutoriel : changer le matériau", "Tutoriel (PDF)", "TUTO"),
    doc(drives(24)[2], "Tutoriel : exporter en STL", "Tutoriel (PDF)", "TUTO"),
]})
s3["seances"].append({"t": "Séance 3 — Le test de flexion",
    "note": [D[25]["blocks"][2]["t"]], "items": [
    doc(drives(25)[0], "Déroulement de la séance 3", "Document (PDF)", "DOC"),
    doc(drives(25)[1], "Document élève — séance 3", "Fiche d'activité (PDF)", "DOC"),
    doc(drives(27)[0], "Le plugin de simulation sur Onshape", "Vidéo", "VIDEO"),
    doc(drives(26)[0], "Synthèse de la séance 3", "Synthèse (PDF)", "SYNTHESE"),
]})
s3["seances"].append({"t": "Séance 4",
    "note": [D[28]["blocks"][2]["t"]], "items": [
    doc(drives(28)[0], "Déroulement de la séance", "Document (PDF)", "DOC"),
    doc(drives(28)[1], "Document élève", "Fiche d'activité (PDF)", "DOC"),
    doc(drives(29)[0], "Synthèse de la séance 4", "Synthèse (PDF)", "SYNTHESE"),
    doc(drives(29)[1], "La mise en forme des matériaux", "Synthèse (PDF)", "SYNTHESE"),
]})
s3["seances"].append({"t": "Séance 5",
    "note": [D[30]["blocks"][2]["t"]], "items": [
    doc(drives(30)[0], "Déroulement de la séance", "Document (PDF)", "DOC"),
    doc(drives(30)[1], "Document élève", "Fiche d'activité (PDF)", "DOC"),
    doc(drives(31)[0], "Synthèse de la séance 5", "Synthèse (PDF)", "SYNTHESE"),
]})
s3["seances"].append({"t": "✅ Correction de la séquence", "items": [
    doc(drives(32)[0], "Correction : le support de sac", "Corrigé (PDF)", "CORRIGE"),
]})
S.append(s3)

# ===== Séquence 4 =====
s4 = {"id": "seq4", "n": "4", "t": "Le robot mBot",
      "o": ["Décrire le robot : ses fonctions et ses solutions techniques",
            "Reconnaître la chaîne d'information et la chaîne d'énergie",
            "Programmer le robot avec mBlock et téléverser le programme",
            "Mesurer une distance avec le capteur à ultrasons",
            "Suivre un protocole et calculer un pourcentage d'erreur"],
      "seances": []}
s4["seances"].append({"t": "Introduction — Description du robot",
    "note": ["Complète les fonctions techniques du robot à l'aide du document. Range ton travail dans ton Drive, comme d'habitude."], "items": [
    doc(drives(34)[0], "La nomenclature du robot mBot", "Document (PDF)", "DOC"),
    doc(drives(34)[1], "Des fonctions aux solutions techniques", "Document (PDF)", "DOC"),
]})
s4["seances"].append({"t": "Séance 1 — Mesurer une distance", "items": [
    doc(drives(35)[0], "Déroulement de la séance 1", "Document (PDF)", "DOC"),
    doc(drives(35)[1], "Téléverser un programme dans le mBot", "Tutoriel mBlock (PDF)", "TUTO"),
    doc(drives(36)[0], "La chaîne d'information et d'énergie du mBot", "Document (PDF)", "DOC"),
]})
p = drives(37)
s4["seances"].append({"t": "Séance 2", "items": [
    doc(p[0], "Déroulement de la séance 2", "Document (PDF)", "DOC"),
    doc(p[2], "Suivre un protocole", "Fiche méthode (PDF)", "TUTO"),
    doc(p[3], "Téléverser un programme dans le mBot", "Tutoriel mBlock (PDF)", "TUTO"),
    doc(p[1], "Éléments de synthèse — séance 2", "Synthèse (PDF)", "SYNTHESE"),
]})
p = drives(38)
s4["seances"].append({"t": "Séance 3 — Le protocole expérimental", "items": [
    doc(p[0], "Déroulement de la séance 3", "Document (PDF)", "DOC"),
    doc(p[2], "Calculer un pourcentage d'erreur", "Fiche méthode (PDF)", "TUTO"),
    doc(p[3], "Tableur : calcul du pourcentage d'erreur", "Fichier .ods à télécharger", "FICHIER"),
    doc(p[4], "Faire un graphique sur Google Sheets", "Vidéo", "VIDEO"),
    doc(p[1], "Éléments de synthèse — séance 3", "Synthèse (PDF)", "SYNTHESE"),
    act("seq4/01_Synthese_Protocole_capteur_ultrasons.html", code(39), "Synthèse — Le protocole avec le capteur à ultrasons", "Je retiens l'essentiel de la séance 3", "SYNTHESE"),
]})
s4["seances"].append({"t": "🧠 Synthèse de la séquence", "items": [
    act("seq4/02_Synthese_Fonctions_solutions_capteurs.html", code(40), "Synthèse — Fonctions, solutions et capteurs", "Je retiens l'essentiel de la séquence", "SYNTHESE"),
]})
S.append(s4)

data = json.dumps(S, ensure_ascii=False, indent=0)
tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index_template.html"), encoding="utf-8").read()
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(tpl.replace("/*DATA*/[]", data))
open(os.path.join(OUT, ".nojekyll"), "w").write("")
n = sum(len(x["items"]) for s in S for x in s["seances"])
print("ressources:", n, "activités HTML:", sum(1 for s in S for x in s["seances"] for i in x["items"] if "h" in i))
