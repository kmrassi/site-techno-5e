#!/usr/bin/env python3
"""Post-traitement des pages d'activité (appelé à la fin de build.py, ou seul) :
- ajoute des ancres (id) sur les quiz pour pouvoir y aller directement depuis le site ;
- ajoute un petit script qui, si l'adresse contient #ancre, ouvre le bon onglet et descend jusqu'au quiz ;
- le bouton « Retour au site » ramène à la séance d'où vient l'activité.
Usage : python3 outils/ameliorer.py <dossier_du_site>
"""
import json, os, re, sys

# fichier -> [(texte à trouver, texte de remplacement)]
ANCRES = {
    "seq1/06_Seance2_Fichiers_taille_mots_de_passe.html": [
        ("<h2>🧩 Quiz autocorrigé — Fichier &amp; taille", '<h2 id="quiz-taille">🧩 Quiz autocorrigé — Fichier &amp; taille'),
        ("<h2>🧩 Quiz autocorrigé — Mots de passe &amp; sécurité", '<h2 id="quiz-mdp">🧩 Quiz autocorrigé — Mots de passe &amp; sécurité'),
    ],
    "seq1/08_Seance3_Phishing_hameconnage.html": [
        ("<h2>🧩 Quiz autocorrigé — Phishing &amp; hameçonnage", '<h2 id="quiz-phishing">🧩 Quiz autocorrigé — Phishing &amp; hameçonnage'),
    ],
    "seq1/12_Fiche_revision_Fichiers_dossiers_cybersecurite.html": [
        ("<h3>🧠 Exercice 1 — QCM", '<h3 id="quiz">🧠 Exercice 1 — QCM'),
    ],
}

OPENER = """<script id="ouvre-ancre">(function(){function go(){var h=decodeURIComponent(location.hash.slice(1));if(!h)return;var el=document.getElementById(h);if(!el)return;
for(var n=el;n&&n!==document.body;n=n.parentElement){if(!n.id)continue;var t=document.querySelector('[aria-controls="'+n.id+'"],[data-pane="'+n.id+'"],[data-tab="'+n.id+'"],[data-target="#'+n.id+'"],[data-target="'+n.id+'"]');if(t&&t!==el)t.click();}
setTimeout(function(){el.scrollIntoView({behavior:"smooth",block:"start"});el.style.transition="box-shadow .4s";el.style.boxShadow="0 0 0 4px #f2a33a";setTimeout(function(){el.style.boxShadow=""},2500)},150)}
window.addEventListener("load",function(){setTimeout(go,250)});window.addEventListener("hashchange",go)})();</script>
"""

def run(out):
    # où est rangée chaque activité ? (pour le bouton retour)
    h = open(os.path.join(out, "index.html"), encoding="utf-8").read()
    s = h.index("const S=") + 8
    S = json.loads(h[s:h.index("];", s) + 1])
    retour = {}
    for q in S:
        for j, x in enumerate(q["seances"]):
            for it in x["items"]:
                if "h" in it:
                    retour.setdefault(it["h"].split("#")[0], f"{q['id']}-{j}")
    for root, _, files in os.walk(out):
        for f in files:
            if not f.endswith(".html") or root == out:
                continue
            p = os.path.join(root, f)
            rel = os.path.relpath(p, out).replace(os.sep, "/")
            html = open(p, encoding="utf-8").read()
            for a, b in ANCRES.get(rel, []):
                if b not in html:
                    html = html.replace(a, b, 1)
            if rel in retour:
                html = re.sub(r'href="\.\./index\.html(#[^"]*)?"(\s+style="position:fixed)',
                              f'href="../index.html#{retour[rel]}"\\2', html)
                html = html.replace("← Retour au site</a>", "← Retour à la séance</a>")
            if rel == "seq1/10_Installer_BDnF.html" and 'id="planB"' not in html:
                open(p, "w", encoding="utf-8").write(html)
                import subprocess
                subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "bdnf_planb.py"), p], check=True)
                html = open(p, encoding="utf-8").read()
            if 'id="ouvre-ancre"' not in html:
                k = html.rfind("</body>")
                html = html[:k] + OPENER + html[k:] if k >= 0 else html + OPENER
            open(p, "w", encoding="utf-8").write(html)

if __name__ == "__main__":
    run(sys.argv[1])
