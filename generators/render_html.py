# -*- coding: utf-8 -*-
"""LESSON -> self-contained HTML (açık tema, Anthropic paleti)."""
import html
from . import manifest
from .html_template import PAGE, CSS, JS


def esc(s):
    return html.escape(str(s), quote=True)


def _inline(s):
    """Metin içi **kalın** ve `kod` desteği."""
    import re
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)
    return s


def _block(b):
    t = b["t"]
    if t == "h":
        return f'<h3 class="sub">{_inline(b["text"])}</h3>'
    if t == "p":
        return f"<p>{_inline(b['text'])}</p>"
    if t in ("keypoint", "tip", "warn"):
        cls = {"keypoint": "kp", "tip": "tip", "warn": "warn"}[t]
        lbl = {"keypoint": "🔑 Önemli", "tip": "💡 İpucu", "warn": "⚠️ Dikkat"}[t]
        return f'<div class="callout {cls}"><span class="lbl">{lbl}</span>{_inline(b["text"])}</div>'
    if t == "list":
        items = "".join(f"<li>{_inline(i)}</li>" for i in b["items"])
        return f"<ul>{items}</ul>"
    if t == "steps":
        items = "".join(f"<li>{_inline(i)}</li>" for i in b["items"])
        return f"<ol>{items}</ol>"
    if t == "code":
        return f'<pre><code>{esc(b["text"])}</code></pre>'
    if t == "table":
        head = "".join(f"<th>{_inline(h)}</th>" for h in b["headers"])
        rows = ""
        for r in b["rows"]:
            rows += "<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>"
        return f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"
    return ""


def _sidebar(day, built_days):
    out = ['<h2>Claude Code Master</h2><div class="sub">20 Günlük Eğitim · v2.0</div>']
    cur_week = None
    for d in manifest.DAYS:
        if d["week"] != cur_week:
            cur_week = d["week"]
            out.append(f'<div class="wk">{manifest.WEEK_TITLES[cur_week]}</div>')
            out.append('<nav class="dnav">')
        num = f'<span class="num">{d["day"]:02d}</span>'
        tier = f'<span class="tier">{d["tier"]}</span>' if d["tier"] else ""
        title = esc(d["title"])
        if d["day"] == day:
            out.append(f'<span class="cur">{num}<span>{title}</span>{tier}</span>')
        elif d["day"] in built_days:
            href = manifest.filename(d["day"]) + ".html"
            out.append(f'<a href="{href}">{num}<span>{title}</span>{tier}</a>')
        else:
            out.append(f'<span class="locked" title="yakında">{num}<span>{title}</span>{tier}</span>')
        # haftanın son günündeyse nav'ı kapat
        idx = manifest.DAYS.index(d)
        if idx == len(manifest.DAYS) - 1 or manifest.DAYS[idx + 1]["week"] != cur_week:
            out.append("</nav>")
    return "".join(out)


def _pager(day, total, built_days):
    prev_ok = day > 1 and (day - 1) in built_days
    next_ok = day < total and (day + 1) in built_days
    prev_html = '<a class="disabled">&nbsp;</a>'
    next_html = '<a class="next disabled">&nbsp;</a>'
    if prev_ok:
        d = manifest.DAYS[day - 2]
        prev_html = (f'<a href="{manifest.filename(day-1)}.html"><div class="dir">← Önceki</div>'
                     f'<div class="tt">Gün {day-1}</div><div>{esc(d["title"])}</div></a>')
    if next_ok:
        d = manifest.DAYS[day]
        next_html = (f'<a class="next" href="{manifest.filename(day+1)}.html"><div class="dir">Sonraki →</div>'
                     f'<div class="tt">Gün {day+1}</div><div>{esc(d["title"])}</div></a>')
    return f'<div class="pager">{prev_html}{next_html}</div>'


def render(L, built_days=None):
    if built_days is None:
        built_days = {L["day"]}
    built_days = set(built_days)
    c = []
    a = c.append

    tier = f'<div class="tierbadge">{esc(L["tier"])}</div>' if L.get("tier") else ""
    a(f'<div class="eyebrow">{manifest.WEEK_TITLES[L["week"]]} · Gün {L["day"]:02d} / {L["total_days"]}</div>')
    a(tier)
    a(f'<h1>{esc(L["title"])}</h1>')
    a(f'<p class="tagline">“{esc(L["tagline"])}”</p>')
    a(f'<p class="intro">{_inline(L["intro"])}</p>')

    # Bugünün Akışı
    a('<h2 class="sec"><span class="k">DERS PLANI</span>⏱️ Bugünün Akışı</h2>')
    a('<div class="flow">')
    for f in L["flow"]:
        a(f'<div class="step"><div class="ph">{esc(f["phase"])}</div>'
          f'<div class="du">{esc(f["dur"])}</div><div class="de">{_inline(f["desc"])}</div></div>')
    a('</div>')
    if L.get("prerequisites"):
        a(f'<div class="meta"><strong>Ön koşul:</strong> {_inline("; ".join(L["prerequisites"]))}</div>')
    if L.get("tools_needed"):
        a(f'<div class="meta"><strong>Gerekli araçlar:</strong> {_inline("; ".join(L["tools_needed"]))}</div>')

    # Hedefler
    a('<h2 class="sec"><span class="k">HEDEFLER</span>🎯 Öğrenme Hedefleri</h2>')
    a("<ol>" + "".join(f"<li>{_inline(o)}</li>" for o in L["objectives"]) + "</ol>")

    # Bölümler
    for s in L["sections"]:
        a(f'<h2 class="sec"><span class="k">{esc(s["num"])}</span>{esc(s["title"])}</h2>')
        for b in s["blocks"]:
            a(_block(b))

    # Prompt kütüphanesi
    if L.get("prompts"):
        a('<h2 class="sec"><span class="k">KÜTÜPHANE</span>🧰 Prompt & Şablon Kütüphanesi</h2>')
        for pr in L["prompts"]:
            note = f'<div class="note">{_inline(pr["note"])}</div>' if pr.get("note") else ""
            a(f'<div class="prompt"><button class="copybtn">kopyala</button>'
              f'<div class="pt">{esc(pr["title"])}</div>'
              f'<pre><code>{esc(pr["prompt"])}</code></pre>{note}</div>')

    # Challenge + çözüm
    ch = L["challenge"]
    a('<h2 class="sec"><span class="k">CHALLENGE</span>🏆 Günün Challenge\'ı</h2>')
    a('<div class="challenge">')
    a(f'<h3>{esc(ch["title"])}</h3><p>{_inline(ch["task"])}</p>')
    if ch.get("requirements"):
        a("<p><strong>Gereksinimler:</strong></p><ul>" +
          "".join(f"<li>{_inline(r)}</li>" for r in ch["requirements"]) + "</ul>")
    a('<p><strong>Başarı Kriterleri:</strong></p><ul class="checks">')
    for i, r in enumerate(ch["success"]):
        a(f'<li><label><input type="checkbox" data-k="succ{i}"><span>{_inline(r)}</span></label></li>')
    a('</ul></div>')

    sol = ch["solution"]
    a('<div class="solution"><h3 class="sub">✅ Çözüm Rehberi</h3>')
    a(f'<p>{_inline(sol["intro"])}</p>')
    if sol.get("prompts"):
        a("<p><strong>Önerilen prompt zinciri:</strong></p>")
        for pr in sol["prompts"]:
            a(f'<div class="prompt"><button class="copybtn">kopyala</button>'
              f'<div class="pt">{esc(pr["title"])}</div>'
              f'<pre><code>{esc(pr["prompt"])}</code></pre></div>')
    if sol.get("notes"):
        a("<p><strong>Kontrol noktaları:</strong></p><ul>" +
          "".join(f"<li>{_inline(n)}</li>" for n in sol["notes"]) + "</ul>")
    if sol.get("pitfalls"):
        a("<p><strong>Sık yapılan hatalar:</strong></p><ul>" +
          "".join(f"<li>⚠️ {_inline(pf)}</li>" for pf in sol["pitfalls"]) + "</ul>")
    a('</div>')

    # Takeaway
    a('<h2 class="sec"><span class="k">ÖZET</span>📌 Takeaway\'ler</h2>')
    a("<ol>" + "".join(f"<li>{_inline(t)}</li>" for t in L["takeaways"]) + "</ol>")

    # Okuma
    a('<h2 class="sec"><span class="k">KAYNAKLAR</span>📚 Ekstra Okuma</h2>')
    r = L["reading"]
    if r.get("official"):
        a("<p><strong>Resmi Dokümantasyon (⭐ zorunlu):</strong></p><ul>")
        for x in r["official"]:
            a(f'<li>⭐ <a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["label"])}</a></li>')
        a("</ul>")
    if r.get("community"):
        a("<p><strong>Topluluk (önerilen):</strong></p><ul>")
        for x in r["community"]:
            a(f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["label"])}</a></li>')
        a("</ul>")
    if r.get("extra"):
        a("<p><strong>Ek kaynaklar:</strong></p><ul>")
        for x in r["extra"]:
            a(f'<li><a href="{esc(x["url"])}" target="_blank" rel="noopener">{esc(x["label"])}</a></li>')
        a("</ul>")
    if L["day"] < L["total_days"]:
        a(f'<div class="callout tip"><span class="lbl">Yarın (Gün {L["day"]+1})</span>{_inline(L["next_preview"])}</div>')

    # Self-assessment
    a('<h2 class="sec"><span class="k">SELF-ASSESSMENT</span>☑️ Kontrol Listesi</h2>')
    a('<p>Günü tamamlamadan önce hepsini işaretle — ilerlemen üstteki çubuğa yansır.</p>')
    a('<ul class="checks">')
    for i, c2 in enumerate(L["checklist"]):
        a(f'<li><label><input type="checkbox" data-k="final{i}" data-final="1"><span>{_inline(c2)}</span></label></li>')
    a('</ul>')

    a(_pager(L["day"], L["total_days"], built_days))
    a(f'<div class="foot">Claude Code Master Eğitim Programı · Gün {L["day"]}/{L["total_days"]} · {esc(L["date_label"])}</div>')

    page = (PAGE
            .replace("%%TITLE%%", esc(f'Gün {L["day"]} — {L["title"]} · Claude Code Master'))
            .replace("%%CSS%%", CSS)
            .replace("%%JS%%", JS)
            .replace("%%DAY%%", str(L["day"]))
            .replace("%%SIDEBAR%%", _sidebar(L["day"], built_days))
            .replace("%%CONTENT%%", "".join(c)))
    return page
