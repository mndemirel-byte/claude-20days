# pipeline.md — İçerik → Build → Deploy Akışı

Bu doküman, bir dersin Claude chat'te üretilmesinden Vercel'de canlıya çıkmasına
kadar geçen tüm adımları açıklar. Kalıcı kurulum bilgisi için `docs/requirements/`
altındaki `product.md` ve `prompt.md`'ye bakabilirsin; bu dosya günlük iş akışına
odaklanır.

## 1. İçeriği content/gunNN.py'ye dönüştür

Claude chat'te üretilen ders içeriği (düz metin/markdown) doğrudan pipeline'a
girmez. `generators/schema.py`'daki `LESSON` sözlüğü şemasına uygun şekilde
`content/gunNN.py` dosyasına dönüştürülmesi gerekir (day, title, tagline,
sections, prompts, challenge, checklist vb. alanlar). Bu adım manuel/agent
destekli bir dönüştürmedir — build.py bu dosyayı olduğu gibi bekler.

## 2. Build et

```bash
python build.py NN             # örn: python build.py 3
```

Üretilenler:
- `output/gunNN-slug.json` — app render kaynağı
- `output/gunNN-slug.html` — standalone/offline kopya
- `output/index.html` güncellenir — ilgili gün artık kilitli değil, tıklanabilir kart

`python build.py all` tüm mevcut günleri + index'i yeniden üretir.
`python build.py index` sadece index.html'i günceller.

## 3. Gözden geçir

`output/gunNN-slug.html` dosyasını tarayıcıda aç ve kontrol et:
- Sidebar'da yeni gün doğru gösteriliyor mu
- Pager (önceki/sonraki) komşu günlere doğru linkleniyor mu
- Checklist kutucukları ve kopyala butonları çalışıyor mu
- localStorage anahtarları (`ccedu:v1:dayN:<item_key>`) doğru namespace'te

## 4. Commit + push

```bash
git add content/gunNN.py output/
git commit -m "feat: gün NN eklendi"
git push
```

## 5. Vercel otomatik deploy

Vercel, repo ile GitHub webhook üzerinden bağlıdır. `master` branch'ine her
push'ta otomatik yeni bir deploy tetiklenir. Build command boş olduğu için
Vercel yalnızca `output/` klasöründeki güncel dosyaları (yeni
`gunNN-slug.html/json` + güncellenmiş `index.html`) olduğu gibi yayınlar.
Push'tan ~10–30 saniye sonra site günceldir — ekstra bir işlem gerekmez.

## Özet akış

```
Claude chat (ham içerik)
   → content/gunNN.py (LESSON sözlüğü)
   → python build.py NN
   → gözden geçir (output/gunNN-slug.html)
   → git add + commit + push
   → Vercel otomatik deploy
```

## Bilinen kısıtlar

- Sadece `json` ve `html` renderer'ları var; `md`/`pdf` üretilmiyor.
- Vercel/GitHub Pages kurulumu tek seferlik, manuel bir dashboard adımıdır —
  pipeline'ın bir parçası değildir (bkz. `docs/requirements/prompt.md` §1-2).
- `build.py`, konsol çıktısı için UTF-8'e zorlanır (`sys.stdout.reconfigure`);
  bu olmadan Windows'ta (cp1252) ✓ karakteri basılırken çöküyordu.
