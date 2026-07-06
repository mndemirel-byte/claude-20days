# PROMPT.md — Statik Site Kurulum ve Deploy Kılavuzu

Pipeline zaten çalışıyor. Bu doküman **tek seferlik hosting kurulumu** ve
**ders ekleme → deploy** döngüsünü açıklar.

---

## 1. Vercel'e Deploy (önerilen, tek seferlik)

```bash
# 1. GitHub repo oluştur ve mevcut projeyi push et
git init && git add . && git commit -m "chore: initial commit"
git remote add origin https://github.com/<kullanici>/cc-egitim.git
git push -u origin master

# 2. vercel.com → "Add New Project" → GitHub repoyu seç
#    Settings:
#      Framework Preset  : Other
#      Root Directory    : ./          (proje kökü)
#      Output Directory  : output      ← kritik
#      Build Command     : (boş bırak)
#
# 3. Deploy → site yayında.
```

Bundan sonra her `git push` otomatik olarak yeniden yayınlar.

---

## 2. GitHub Pages (alternatif, ücretsiz)

```bash
# output/ klasörünü gh-pages branch'ine gönder
pip install ghp-import --break-system-packages
python build.py all
ghp-import -n -p -f output    # output/ → gh-pages branch → otomatik yayın

# Site adresi: https://<kullanici>.github.io/<repo>/
```

---

## 3. Yeni Ders Ekleme → Deploy Döngüsü

Her gün aynı üç adım:

```bash
# Adım 1: İçeriği yaz (ders-hazirlama-yonergesi.md'yi izle)
# content/gun02.py → LESSON sözlüğü

# Adım 2: Build et
python build.py 2             # output/gun02-*.html + .json üretir, index.html güncellenir

# Adım 3: Gözden geçir
open output/gun02-slug.html   # macOS; Linux'ta: xdg-open ...

# Adım 4: Deploy
git add output/
git commit -m "feat: gün 2 eklendi — temel kullanım ve izinler"
git push                      # → Vercel / GitHub Pages otomatik yayınlar
```

---

## 4. Opsiyonel: Otomatik Build (GitHub Actions)

Elle `python build.py` çalıştırmak istemiyorsan, `content/` değişince
pipeline'ı CI'da otomatik çalıştırıp `output/`'u commit eden bir Action yazılabilir.

```yaml
# .github/workflows/build.yml
name: Build lessons
on:
  push:
    paths: ['content/**']
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: python build.py all
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'chore: auto-build lessons'
          file_pattern: 'output/'
```

---

## 5. Kontrol (deploy sonrası)

```
[ ] Site URL'i açılıyor ve index.html görünüyor
[ ] Yeni ders kartı index'te listelenmiş
[ ] Ders sayfası doğru açılıyor (sidebar, checklist, kopyala)
[ ] Mobilde görünüm düzgün (responsive test)
[ ] localStorage ile checklist durumu kaydediliyor
```

---

*Özet: pipeline çalışıyor, host ücretsiz, deploy tek komut. Karmaşık bir şey yok.*
