# PRODUCT.md — Claude Code Master Eğitim Platformu

**Ürün:** 20 günlük Claude Code eğitimini, ders eklendikçe büyüyen bir statik web sitesi olarak yayınlar.
**Versiyon:** 2.0 (statik, auth yok) · **Tarih:** Temmuz 2026
**Stack:** Statik HTML/CSS/JS · GitHub Pages veya Vercel (ücretsiz) · Python pipeline (içerik üretimi)

---

## 1. Vizyon

Her gün bir ders eklenir; site otomatik büyür. Ziyaretçi giriş yapmadan tüm içeriğe erişir.
İlerleme takibi tarayıcıda (`localStorage`) tutulur — sunucu, veritabanı, kimlik doğrulama yok.

## 2. Mimari (tek cümle)

```
content/gunNN.py  →  python build.py  →  output/*.html  →  GitHub / Vercel  →  internet
```

Pipeline zaten kurulu ve çalışıyor. "Platform" bu pipeline'ın çıktısını barındıran statik bir host.

## 3. Sayfalar

| Sayfa | Dosya | İçerik |
|-------|-------|--------|
| Ana sayfa | `index.html` | 20 günlük ızgara, genel ilerleme çubuğu, kilitli/açık kartlar |
| Ders sayfası | `gunNN-slug.html` | Tam ders içeriği; sidebar, etkileşimli checklist, kopyala butonları |

Her iki sayfa da `python build.py` ile `output/` klasörüne üretilir.

## 4. İçerik Ekleme Akışı

```bash
# 1. İçeriği yaz
vim content/gun02.py          # LESSON sözlüğünü doldur

# 2. Build et (JSON + HTML)
python build.py 2             # output/gun02-*.json + .html + index.html güncellenir

# 3. Gözden geçir
open output/gun02-slug.html   # tarayıcıda incele

# 4. Deploy et
git add output/ && git commit -m "feat: gün 2 eklendi" && git push
# → Vercel / GitHub Pages otomatik yayınlar
```

## 5. İlerleme Takibi

Checklist kutularının durumu tarayıcının `localStorage`'ında saklanır. Anahtar formatı:
`ccedu:v1:dayN:<item_key>`. Platform dışı sunucu veya hesap gerekmez; veri kullanıcının
cihazında kalır. Cihazlar arası senkron hedef dışındadır (auth yok).

## 6. Dosya Yapısı

```
ccedu/
├── content/
│   ├── gun01.py          ← tek kaynak (LESSON sözlüğü)
│   ├── gun02.py
│   └── ...
├── generators/
│   ├── schema.py         ← blok yardımcıları
│   ├── tokens.css        ← tek stil kaynağı (Anthropic paleti)
│   ├── html_template.py  ← tokens.css'i okur, HTML'e gömer
│   ├── render_html.py
│   ├── render_json.py
│   └── manifest.py
├── output/               ← deploy edilecek klasör (bu klasör host edilir)
│   ├── index.html
│   ├── gun01-claude-code-nedir-kurulum.html
│   ├── gun01-claude-code-nedir-kurulum.json
│   └── ...
└── build.py
```

## 7. Hosting

| Seçenek | Kurulum | Maliyet | Otomatik deploy |
|---------|---------|---------|-----------------|
| **Vercel** (önerilen) | `output/` klasörünü publish dir olarak ayarla | Ücretsiz | GitHub push'ta |
| **GitHub Pages** | `output/` → `gh-pages` branch veya `/docs` klasörü | Ücretsiz | GitHub Actions ile |
| **Netlify** | Drag & drop veya Git bağlantısı | Ücretsiz | GitHub push'ta |

**Vercel kurulumu (tek seferlik):**
1. GitHub'a push et.
2. vercel.com → "Import Project" → repo seç.
3. "Output Directory" → `output` olarak ayarla, build command bırak boş.
4. Deploy. Bundan sonra her push otomatik yayınlar.

## 8. Yol Haritası (opsiyonel iyileştirmeler)

Temel çalışıyorken eklenebilecekler — zorunlu değil:

- Arama (client-side, Fuse.js veya pagefind ile)
- Baskı/PDF görünümü (CSS `@media print`)
- Dark mode toggle
- Okuma süresi tahmini
- Sosyal paylaşım meta etiketleri (OG/Twitter)

---

*Platform budur. Sunucu yok, veritabanı yok, auth yok. Pipeline çalışıyor, host ücretsiz.*
