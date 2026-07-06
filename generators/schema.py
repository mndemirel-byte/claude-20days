"""
Ortak ders şeması (tek kaynak) + blok yapıcı yardımcılar.

Her gün, content/gunXX.py içinde bir LESSON sözlüğü tanımlar.
Üç renderer (md / html / pdf) bu tek kaynaktan çıktı üretir.

--- LESSON şeması ------------------------------------------------------------
LESSON = {
  "day": int,                 # 1..20
  "total_days": 20,
  "week": int,                # 1..4
  "slug": str,                # dosya adı için ascii slug
  "title": str,
  "tagline": str,             # tema cümlesi
  "intro": str,               # kısa giriş paragrafı
  "tier": str|None,           # "🟢 Kademe 1" gibi rozet, ya da None
  "date_label": str,          # PDF/HTML altbilgi tarih etiketi

  "flow": [ {"phase","dur","desc"} ],     # Bugünün Akışı (öğrenciye görünür LLD)
  "prerequisites": [str],                  # ön koşul
  "tools_needed": [str],                   # gerekli araç
  "objectives": [str],                     # öğrenme hedefleri

  "sections": [ {"num": "BÖLÜM 1", "title": "...", "blocks": [block,...]} ],

  "prompts": [ {"title","prompt","note"?} ],   # prompt & şablon kütüphanesi

  "challenge": {
      "title": str,
      "task": str,
      "requirements": [str],               # görev gereksinimleri
      "success": [str],                    # başarı kriterleri
      "solution": {                        # çözüm rehberi (YENİ)
          "intro": str,
          "prompts": [ {"title","prompt"} ],   # önerilen prompt zinciri
          "notes": [str],                       # kontrol noktaları / ipuçları
          "pitfalls": [str],                    # sık hatalar
      },
  },

  "takeaways": [str],
  "reading": { "official": [{"label","url"}], "community": [...], "extra": [...] },
  "next_preview": str,
  "checklist": [str],
}

--- Blok tipleri (sections[].blocks[]) --------------------------------------
Aşağıdaki yardımcılar dict döndürür; üç renderer de bu tipleri anlar.
"""


def h(text):
    """Alt başlık (ör. '1.1 Claude Code Nedir?')."""
    return {"t": "h", "text": text}


def p(text):
    """Paragraf."""
    return {"t": "p", "text": text}


def keypoint(text):
    """Önemli/Key Point vurgu kutusu."""
    return {"t": "keypoint", "text": text}


def tip(text):
    """İpucu kutusu."""
    return {"t": "tip", "text": text}


def warn(text):
    """Dikkat/uyarı kutusu."""
    return {"t": "warn", "text": text}


def bullets(items):
    """Madde listesi."""
    return {"t": "list", "items": list(items)}


def steps(items):
    """Numaralı adımlar."""
    return {"t": "steps", "items": list(items)}


def code(text, lang=""):
    """Kod bloğu (mono)."""
    return {"t": "code", "lang": lang, "text": text.rstrip("\n")}


def table(headers, rows):
    """Tablo. headers: [str], rows: [[str,...],...]."""
    return {"t": "table", "headers": list(headers), "rows": [list(r) for r in rows]}
