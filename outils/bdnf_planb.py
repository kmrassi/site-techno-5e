# Ajoute le « Plan B » (installer BDnF depuis le Drive) à la page Installer BDnF. Usage : python3 bdnf_planb.py <page.html>
import sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
DRIVE="https://drive.google.com/file/d/1w5sgu7g0HJgxvk0L0_h232tahA8jdP-3/view?usp=drive_link"
# 1) le lien de l'étape 1 renvoie vers le plan B
old_li=s[s.index('<li><label><input type="checkbox"> <span>💡 <b>Ça ne marche pas ?</b>'):]
old_li=old_li[:old_li.index('</li>')+5]
new_li=('<li class="planb-li">💡 <b>Le téléchargement ne marche pas ?</b> Utilise le '
 '<a href="#planB"><b>Plan B : BDnF depuis le Drive du professeur</b></a> (en bas de la page).</li>')
s=s.replace(old_li,new_li)
css="""<style>
.planb{background:#fff8ec;border:3px dashed #f2a33a;border-radius:18px;padding:18px 18px 6px;margin:28px 0}
.planb>h2{margin:0 0 6px;color:#b45309}.planb .step{background:#fff}
.planb .num{background:#f2a33a!important}
.planb-li{list-style:none;background:#fff3cd;border-radius:10px;padding:8px 12px;margin-top:8px}
.mock{border:1px solid #cbd5e1;border-radius:10px;overflow:hidden;font:14px system-ui,sans-serif;max-width:520px;margin:10px 0 4px;box-shadow:0 4px 12px rgba(0,0,0,.08);background:#fff}
.mock .bar{background:#e2e8f0;padding:6px 10px;font-size:12px;color:#475569;display:flex;gap:6px;align-items:center}
.mock .bar i{width:10px;height:10px;border-radius:50%;background:#cbd5e1;display:inline-block}
.mock .in{padding:12px 14px}
.mock .row{display:flex;align-items:center;gap:10px;padding:7px 8px;border-radius:6px}
.mock .hl{outline:3px solid #e11d48;outline-offset:1px;background:#fff1f2}
.mock .menu{border:1px solid #cbd5e1;border-radius:8px;box-shadow:0 6px 16px rgba(0,0,0,.12);width:230px;margin:6px 0 0 40px;background:#fff}
.mock .menu div{padding:6px 12px}.mock .gbtn{display:inline-block;background:#1a73e8;color:#fff;border-radius:6px;padding:6px 14px;font-weight:600}
.mock .arrow{color:#e11d48;font-weight:800}
</style>
"""
planb=f"""<section class="planb" id="planB"><h2>📥 Plan B : installer BDnF depuis le Drive du professeur</h2>
<p>À utiliser seulement si le site de la BnF ne marche pas. Connecte-toi d'abord avec ton compte <b>ert.tn</b>.</p>

<section class="step"><div class="num">B1</div><div class="body"><h2>Télécharger le fichier</h2><ul>
<li><label><input type="checkbox"> <span>Clique sur ce lien : <a href="{DRIVE}" target="_blank" rel="noopener"><code>📥 BDnF sur le Drive</code></a></span></label></li>
<li><label><input type="checkbox"> <span>En haut à droite, clique sur la flèche <b>⬇ Télécharger</b>.</span></label></li>
<li><label><input type="checkbox"> <span>Un message dit que Google ne peut pas vérifier le fichier (il est gros). Clique sur <b>Télécharger quand même</b>.</span></label></li>
<li><label><input type="checkbox"> <span>Attends la fin du téléchargement (le fichier est gros : environ 120 Mo).</span></label></li></ul>
<div class="mock"><div class="bar"><i></i><i></i><i></i>&nbsp;drive.google.com</div><div class="in">
<div class="row" style="justify-content:space-between"><span>🗜️ BDnF-Portable-x64-….zip</span><span class="hl" style="padding:2px 8px;border-radius:6px">⬇</span></div>
<div style="border-top:1px solid #e2e8f0;margin-top:8px;padding-top:10px">Impossible de rechercher des virus dans ce fichier…<br><br><span class="gbtn hl">Télécharger quand même</span></div></div></div>
</div></section>

<section class="step"><div class="num">B2</div><div class="body"><h2>Extraire le fichier (ouvrir la « valise »)</h2><ul>
<li><label><input type="checkbox"> <span>Ouvre le dossier <b>Téléchargements</b>.</span></label></li>
<li><label><input type="checkbox"> <span>Fais un <b>clic droit</b> sur <b>BDnF-Portable-x64-….zip</b>.</span></label></li>
<li><label><input type="checkbox"> <span>Clique sur <b>Extraire tout…</b></span></label></li>
<li><label><input type="checkbox"> <span>Clique sur <b>Parcourir</b>, choisis <b>Documents</b> puis <b>5eme</b>, puis clique sur <b>Extraire</b>.</span></label></li></ul>
<div class="mock"><div class="bar"><i></i><i></i><i></i>&nbsp;📁 Téléchargements</div><div class="in">
<div class="row hl">🗜️ BDnF-Portable-x64-….zip <span class="arrow">← clic droit</span></div>
<div class="menu"><div>Ouvrir</div><div>Partager</div><div class="hl" style="font-weight:600">Extraire tout…</div></div></div></div>
</div></section>

<section class="step"><div class="num">B3</div><div class="body"><h2>Ouvrir le bon dossier</h2>
<p class="note">Il y a parfois <b>deux</b> dossiers « BDnF-Portable-x64 » l'un dans l'autre : ouvre-les jusqu'à voir le fichier <b>BDNF</b>.</p><ul>
<li><label><input type="checkbox"> <span>Double-clique sur le dossier <b>BDnF-Portable-x64</b>.</span></label></li>
<li><label><input type="checkbox"> <span>Tu vois le fichier <b>BDNF</b> et un dossier <b>BDNF_Data</b> ? C'est le bon endroit.</span></label></li></ul>
<div class="mock"><div class="bar"><i></i><i></i><i></i>&nbsp;📁 Documents › 5eme › BDnF-Portable-x64</div><div class="in">
<div class="row">📁 BDNF_Data</div><div class="row">📁 MonoBleedingEdge</div>
<div class="row hl"><b>🟦 BDNF</b> <span class="arrow">← double-clic</span></div>
<div class="row" style="color:#64748b">⚙️ UnityCrashHandler64</div><div class="row" style="color:#64748b">⚙️ UnityPlayer.dll</div></div></div>
</div></section>

<section class="step"><div class="num">B4</div><div class="body"><h2>Lancer BDnF</h2><ul>
<li><label><input type="checkbox"> <span><b>Double-clique</b> sur <b>BDNF</b>. L'application s'ouvre ! 🎉</span></label></li>
<li><label><input type="checkbox"> <span>⚠️ Ne clique pas sur <b>UnityCrashHandler64</b> : ce n'est pas le bon fichier.</span></label></li></ul>
<p>💡 La prochaine fois : va dans <b>Documents › 5eme › BDnF-Portable-x64</b> et double-clique sur <b>BDNF</b>.</p>
</div></section>
</section>
"""
if 'id="planB"' not in s:
    s=s.replace('<div class="help">',planb+'<div class="help">',1)
    s=s.replace('</head>',css+'</head>',1)
open(p,'w',encoding='utf-8').write(s)
