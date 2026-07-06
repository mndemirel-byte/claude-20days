# -*- coding: utf-8 -*-
"""
Günlük çıktı: JSON (app render) + HTML (standalone/offline kopya)
PDF ve MD üretilmez.

Kullanım:
  python build.py 1        →  Gün 1: json + html
  python build.py index    →  index.html (program ana sayfası)
  python build.py all      →  mevcut tüm günler + index
"""
import sys, os, importlib

BASE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(BASE, "output")
os.makedirs(OUT, exist_ok=True)

from generators import manifest, render_html, render_json
from generators.html_template import PAGE, CSS   # CSS artık tokens.css'ten geliyor


def built_days():
    """content/ içinde tanımlı günleri döndürür."""
    days = set()
    for d in manifest.DAYS:
        if os.path.exists(os.path.join(BASE, "content", f"gun{d['day']:02d}.py")):
            days.add(d["day"])
    return days


def build_day(day: int, built: set):
    mod  = importlib.import_module(f"content.gun{day:02d}")
    L    = mod.LESSON
    stem = manifest.filename(day)            # ör. gun01-claude-code-nedir-kurulum

    # JSON — app render kaynağı
    json_path = os.path.join(OUT, stem + ".json")
    render_json.render(L, json_path)

    # HTML — standalone / offline / önizleme
    html_path = os.path.join(OUT, stem + ".html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(render_html.render(L, built_days=built))

    print(f"✓ Gün {day}: {stem}.json + .html")
    return stem


def build_index(built: set):
    rows = []
    cur_week = None
    for d in manifest.DAYS:
        if d["week"] != cur_week:
            cur_week = d["week"]
            rows.append(f'<div class="wk-h">{manifest.WEEK_TITLES[cur_week]}</div>')
        num  = f'<span class="n">{d["day"]:02d}</span>'
        tier = f'<span class="ti">{d["tier"]}</span>' if d["tier"] else ""
        if d["day"] in built:
            href = manifest.filename(d["day"]) + ".html"
            rows.append(
                f'<a class="card" href="{href}" data-day="{d["day"]}">'
                f'{num}<span class="tt">{d["title"]}</span>{tier}'
                f'<span class="st" data-status></span></a>')
        else:
            rows.append(
                f'<div class="card locked">{num}'
                f'<span class="tt">{d["title"]}</span>{tier}'
                f'<span class="soon">yakında</span></div>')

    extra_css = """
.hero{max-width:820px;margin:0 auto;padding:54px 34px 8px}
.hero .eyebrow{font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-ink)}
.hero h1{font-family:var(--serif);font-size:42px;line-height:1.1;margin:10px 0 8px}
.hero p{font-size:17px;color:var(--ink-soft);max-width:640px}
.track{max-width:820px;margin:8px auto 0;padding:0 34px}
.track .bar{height:10px;background:var(--line);border-radius:99px;overflow:hidden;margin:18px 0 6px}
.track .bar>span{display:block;height:100%;width:0;background:var(--accent);transition:width .4s}
.track .lab{font-size:13px;color:var(--ink-soft)}
.grid{max-width:820px;margin:26px auto 80px;padding:0 34px}
.wk-h{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);margin:26px 4px 10px}
.card{display:flex;align-items:center;gap:14px;background:var(--surface);border:1px solid var(--line);
  border-radius:14px;padding:15px 18px;margin:9px 0;text-decoration:none;color:var(--ink)}
a.card:hover{border-color:var(--accent);transform:translateY(-1px);transition:.15s}
.card .n{font-family:var(--serif);font-size:22px;font-weight:700;color:var(--accent);min-width:34px}
.card .tt{font-weight:600;flex:1}
.card .ti{font-size:12px;color:var(--accent-ink);background:var(--kp-bg);border:1px solid var(--kp-br);
  border-radius:99px;padding:2px 10px}
.card.locked{opacity:.6}
.card .soon{font-size:12px;color:var(--ink-faint)}
.card .st{font-size:13px;color:#5c8a4a;font-weight:700;min-width:18px;text-align:right}
"""
    index_js = """
(function(){
  var done=0, total=0;
  document.querySelectorAll('.card[data-day]').forEach(function(c){
    total++;
    var d=c.getAttribute('data-day');
    try{
      if(localStorage.getItem('ccedu:v1:dayDone:'+d)==='1'){
        done++;
        var s=c.querySelector('[data-status]'); if(s) s.textContent='✓ tamam';
      }
    }catch(e){}
  });
  var pct=total ? Math.round(done*100/total) : 0;
  var bar=document.querySelector('.track .bar>span');
  var lab=document.querySelector('.track .lab');
  var tb=document.querySelector('.topbar .prog>span');
  var tl=document.querySelector('.topbar .proglabel');
  if(bar) bar.style.width=pct+'%';
  if(lab) lab.textContent=done+' / 20 gün tamamlandı  ·  %'+pct;
  if(tb)  tb.style.width=pct+'%';
  if(tl)  tl.textContent='%'+pct;
})();
"""
    content = (
        f'<div class="hero">'
        f'<div class="eyebrow">20 Günlük Program · v2.0 · {len(built)}/20 hazır</div>'
        f'<h1>Claude Code Master Eğitim Programı</h1>'
        f'<p>Sıfırdan master seviyeye: kurulum ve temel kullanımdan multi-agent orkestrasyona kadar, '
        f'dört kademeli gerçek proje ile öğren. Her gün ~2–3 saat.</p></div>'
        f'<div class="track"><div class="bar"><span></span></div><div class="lab"></div></div>'
        f'<div class="grid">{"".join(rows)}</div>'
        f'<div class="foot" style="max-width:820px;margin:0 auto;padding:0 34px 40px">'
        f'Claude Code Master Eğitim Programı · Temmuz 2026</div>'
    )
    page = (PAGE
            .replace("%%TITLE%%", "Claude Code Master Eğitim Programı")
            .replace("%%CSS%%",   CSS + extra_css)
            .replace("%%JS%%",    index_js)
            .replace("%%DAY%%",   "0")
            .replace("%%SIDEBAR%%", '<h2>Program</h2><div class="sub">Ana sayfa</div>')
            .replace("%%CONTENT%%", content))
    # Index'te sidebar gizle → tam genişlik
    page = page.replace(
        '<div class="layout">',
        '<div class="layout" style="grid-template-columns:1fr">')
    page = page.replace(
        '<aside class="sidebar"><h2>Program</h2><div class="sub">Ana sayfa</div></aside>', '')
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("✓ index.html")


if __name__ == "__main__":
    arg   = sys.argv[1] if len(sys.argv) > 1 else "all"
    built = built_days()
    if arg == "index":
        build_index(built)
    elif arg == "all":
        for d in sorted(built):
            build_day(d, built)
        build_index(built)
    else:
        build_day(int(arg), built)
        build_index(built)
