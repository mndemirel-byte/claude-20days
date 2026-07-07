# Claude Code Master Eğitim Programı

20 günlük Claude Code eğitimini, ders eklendikçe büyüyen statik bir web sitesi olarak
yayınlayan içerik pipeline'ı. Sunucu, veritabanı veya kimlik doğrulama yok — ilerleme
takibi tamamen tarayıcının `localStorage`'ında tutulur.

## Nasıl çalışır

```
content/gunNN.py  →  python build.py  →  output/*.json + *.html  →  git push  →  Vercel otomatik deploy
```

Her gün için `content/gunNN.py` dosyasında tek bir `LESSON` sözlüğü tanımlanır
(`generators/schema.py`'daki şemaya göre). `build.py` bu sözlükten hem JSON (app render
kaynağı) hem de standalone HTML üretir; `index.html` de aynı anda güncellenir.

## Kullanım

```bash
# Tek bir günü build et
python build.py 3

# Mevcut tüm günleri + index'i yeniden üret
python build.py all

# Sadece index.html'i güncelle
python build.py index
```

Üretilen dosyalar `output/` klasörüne yazılır ve doğrudan statik olarak servis edilir.

## Proje yapısı

```
claude-20days/
├── build.py                 ← build script (CLI giriş noktası)
├── content/
│   ├── gun01.py              ← her gün için LESSON sözlüğü (tek kaynak)
│   ├── gun02.py
│   └── ...
├── generators/
│   ├── schema.py             ← LESSON şeması + blok yapıcılar (h, p, tip, code, ...)
│   ├── manifest.py           ← 20 günlük program planı (day/week/slug/title/tier)
│   ├── render_json.py        ← LESSON → JSON
│   ├── render_html.py        ← LESSON → standalone HTML
│   ├── html_template.py       ← ortak HTML kabuğu (topbar, sidebar, JS)
│   └── tokens.css            ← tek stil kaynağı
├── output/                   ← build çıktısı (json + html), deploy edilen klasör
└── docs/
    ├── requirements/          ← ürün spesifikasyonu ve deploy komutları
    └── pipeline.md            ← içerik → build → deploy iş akışı detayları
```

## Yeni ders ekleme

1. `content/gunNN.py` dosyasını `generators/schema.py`'daki `LESSON` şemasına göre yaz.
2. `python build.py NN` ile build et.
3. `output/gunNN-slug.html` dosyasını tarayıcıda gözden geçir.
4. `git add content/gunNN.py output/ && git commit -m "feat: gün NN eklendi" && git push`
5. Vercel, `master` branch'ine push algılayınca otomatik yeniden deploy eder.

Detaylı akış için bkz. [`docs/pipeline.md`](docs/pipeline.md).

## İlerleme takibi

Checklist durumu tarayıcıda `localStorage` anahtarlarıyla saklanır:
`ccedu:v1:day<N>:<item_key>` (madde bazlı) ve `ccedu:v1:dayDone:<N>` (gün tamamlandı mı).
Hesap veya sunucu yok; veri kullanıcının cihazında kalır.

## Renderer'lar

Sadece **json** ve **html** üretilir; `md`/`pdf` yok.
