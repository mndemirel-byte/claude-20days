Status: ready-for-agent

## Parent

Gün 18/19/20 içerik ekleme çalışması (bkz. konuşma bağlamı — content/gun18.py, gun19.py, gun20.py ve docs/tool/render_html.py eklendi).

## What to build

`content/gun18.py`, `content/gun19.py`, `content/gun20.py` zaten `generators/manifest.py`'de kayıtlı, `generators/schema.py` şema kontrollerinden geçiyor ve `python build.py all` ile hatasız derleniyor. Tek gerçek sorun render katmanında:

`docs/tool/render_html.py`, `generators/render_html.py`'nin bire bir kopyası olarak eklenmiş, ancak içinde `generators/render_html.py`'de bulunmayan bir düzeltme var: `challenge.solution.notes` içinde `\n` geçen (çok satırlı) bir not varsa, ilk satırı etiket olarak, kalanını `<pre><code>` bloğu olarak render eden `_note()` yardımcı fonksiyonu (satır 156-163). Bu düzeltme `generators/render_html.py`'ye hiç taşınmamış — `docs/tool/` dizini `generators`'ın `manifest`/`html_template` modüllerine bağımlı olduğu için (`from . import manifest`, `from .html_template import ...`) zaten kendi başına çalışan bağımsız bir paket değil, sadece elle yama yapılmış bir taslak.

`content/gun20.py`'deki `challenge.solution.notes` alanında tam olarak bu durum var: "Beklenen dosya yapısı:\ncapstone-microservices/\n├── CLAUDE.md\n..." şeklinde çok satırlı bir dosya ağacı notu. `python build.py all` çalıştırıldığında bu not düz metin olarak `<li>` içine basılıyor (satır sonları HTML'de görünmüyor, ağaç yapısı tek satıra karışıyor) — pre-format kayboluyor. Bu regresyon `output/gun20-capstone-mikroservis.html` dosyasında doğrulandı.

Yapılacaklar:
1. `generators/render_html.py` içindeki `_note()` mantığını `docs/tool/render_html.py`'den taşı (satır ~156-163 civarı, `sol.get("notes")` bloğu).
2. `docs/tool/render_html.py` dosyasını ve boş kalacak `docs/tool/` dizinini sil — artık `generators/` tek kaynak.
3. `python build.py all` çalıştırarak gün 1-20 + index'i yeniden üret.
4. `output/gun20-capstone-mikroservis.html` içinde "Beklenen dosya yapısı" notunun `<pre><code>` bloğu içinde doğru render edildiğini doğrula.
5. Değişen tüm `output/*.html` ve `output/*.json` dosyalarını (gun18/19/20 yeni + gun01-17/index nav güncellemeleri) ve `content/gun18.py`, `content/gun19.py`, `content/gun20.py` dosyalarını commit'e ekle.

## Acceptance criteria

- [ ] `generators/render_html.py` çok satırlı `challenge.solution.notes` girdilerini `<pre><code>` bloğu olarak render ediyor (docs/tool/render_html.py'deki `_note()` mantığı taşındı)
- [ ] `docs/tool/` dizini repodan kaldırıldı
- [ ] `python build.py all` hatasız çalışıyor ve gün 1-20 + index.html üretiliyor
- [ ] `output/gun20-capstone-mikroservis.html` içinde dosya ağacı notu `<pre><code>` içinde, satır sonları korunmuş şekilde görünüyor
- [ ] `python content/gun18.py`, `python content/gun19.py`, `python content/gun20.py` şema kontrolleri hatasız geçiyor (mevcut durumda zaten geçiyor, regresyon olmadığını doğrula)
- [ ] Yeni/değişen `content/`, `output/` dosyaları commit'e eklendi

## Blocked by

None - can start immediately
