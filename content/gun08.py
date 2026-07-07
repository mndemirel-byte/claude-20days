# -*- coding: utf-8 -*-
"""Gün 8 — Debugging, Test Yazma ve Kod İncelemesi (v2.0, Temmuz 2026)."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table

LESSON = {
    # ── Meta ──────────────────────────────────────────────────────────────
    "day": 8,
    "total_days": 20,
    "week": 2,
    "slug": "debugging-test-yazma-kod-incelemesi",
    "title": "Debugging, Test Yazma ve Kod İncelemesi",
    "tagline": "Claude'u QA mühendisi olarak çalıştır",
    "tier": None,
    "date_label": "Temmuz 2026",

    # ── Giriş ─────────────────────────────────────────────────────────────
    "intro": (
        "Bugüne kadar Claude Code ile kod yazdın, yapılandırdın ve context'ini "
        "yönettin. Artık sıra kalite kontrolünde: hataları sistematik olarak "
        "bulmak, testle kanıtlamak, fix sonrası review ettirmek ve mühendis "
        "olarak bulguları değerlendirmek. Gün sonunda 'debug → test → review → "
        "karar → postmortem' döngüsünü Claude Code ile çalıştırmış olacaksın."
    ),

    # ── Akış ──────────────────────────────────────────────────────────────
    "flow": [
        {"phase": "1 · Teorik Temel",       "dur": "25 dk",
         "desc": "Debugging mental modeli + bağlam paketi, TDD ile Claude, "
                 "kod incelemesi katmanları, review bulgusu karar tablosu"},
        {"phase": "2 · Adım-Adım Pratik",   "dur": "55 dk",
         "desc": "Stack trace debugging, TDD döngüsü, /code-review + --fix + "
                 "effort farkı + karar tablosu, /security-review mini karşılaştırma, "
                 "lint kısa destek"},
        {"phase": "3 · Derinleş",           "dur": "25 dk",
         "desc": "Ultrareview 'ne zaman kullanılır?' karar çerçevesi, "
                 "security-guidance plugin bonus pratik, Chrome teaser"},
        {"phase": "4 · Challenge",           "dur": "35 dk",
         "desc": "Todo App auth modülü: 6 test + 1 bug + 1 review + "
                 "postmortem + bonus güvenlik senaryosu"},
    ],

    # ── Ön koşullar ──────────────────────────────────────────────────────
    "prerequisites": [
        "Gün 1–7 tamamlanmış (Claude Code kurulu, CLAUDE.md hazır, context yönetimi biliniyor)",
        "Terminal ve kod editörü açık",
        "Todo App projesi çalışır durumda (Gün 4'te oluşturulan yapı)",
        "Git repository initialized ve en az birkaç commit mevcut",
    ],
    "tools_needed": [
        "Terminal (Claude Code çalışır durumda)",
        "VS Code veya tercih edilen editör",
        "Git (commit, diff, branch işlemleri için)",
        "Node.js / Python (Todo App'in kullandığı dile göre test framework'ü)",
    ],

    # ── Hedefler ──────────────────────────────────────────────────────────
    "objectives": [
        "Claude Code'a hata mesajı / stack trace vererek sistematik debugging yapabileceksin",
        "TDD döngüsünü (Red → Green → Refactor) Claude Code ile uygulayabileceksin",
        "/code-review komutunu effort seviyeleri ve --fix ile kullanarak lokal kod incelemesi yapabileceksin",
        "/security-review ile güvenlik odaklı diff incelemesini çalıştırıp /code-review ile farkını karşılaştırabileceksin",
        "/code-review ultra (ultrareview) ile bulut tabanlı çok-ajanlı derin incelemenin ne zaman gerektiğini bileceksin",
        "security-guidance plugin'ini tanıyacak ve ne yaptığını açıklayabileceksin",
    ],

    # ── BÖLÜM 1: TEORİK TEMEL ────────────────────────────────────────────
    "sections": [
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                h("1.1 Claude Code ile Debugging: Zihinsel Model"),
                p(
                    "Claude Code sıradan bir hata düzeltme aracı değil — doğru "
                    "bağlamla beslersen kök neden analizi yapan, fix öneren ve "
                    "düzeltmeyi testle kanıtlayan bir debugging partneri. Ama "
                    "kritik kelime 'doğru bağlam'. Hata mesajını yapıştırıp "
                    "'düzelt' demek çoğu zaman yüzeysel sonuç verir. Etkili "
                    "debugging sistematik bir döngüdür:"
                ),
                table(
                    ["Adım", "Ne yaparsın?", "Claude'a ne verirsin?"],
                    [
                        ["1. Tanımla", "Hatayı tekrarlanabilir hale getir",
                         "Hata mesajı + stack trace + repro koşulları"],
                        ["2. İzole et", "Hangi modül/fonksiyon sorunlu?",
                         "İlgili dosyalar + son değişiklik diff'i"],
                        ["3. Düzelt", "Minimal fix uygula",
                         "Beklenen vs gerçek davranış + test çıktısı"],
                        ["4. Doğrula", "Fix'in doğruluğunu kanıtla",
                         "Test sonucu + regresyon kontrolü"],
                    ],
                ),

                h("1.2 Minimum Bağlam Paketi"),
                p(
                    "Claude'a etkili debugging yaptırmak için verilecek minimum "
                    "bağlam paketi şu 7 maddeden oluşur. Bu listeyi bir kontrol "
                    "listesi gibi kullan — ne kadar çok maddeyi verirsen, "
                    "Claude'un çözüm kalitesi o kadar yükselir:"
                ),
                bullets([
                    "**Hata mesajı / stack trace** — tam olarak kopyala, kısaltma",
                    "**Hatanın ne zaman oluştuğu** — hangi işlem sırasında, hangi input ile?",
                    "**Beklenen davranış** — ne olmasını bekliyordun?",
                    "**Gerçek davranış** — ne oldu?",
                    "**İlgili dosyalar** — hata hangi modülde, hangi fonksiyonda?",
                    "**Test çıktısı** — varsa, failing test sonucu",
                    "**Son değişiklik diff'i** — hatadan önce ne değişti?",
                ]),
                keypoint(
                    "Bağlam paketi ne kadar eksiksizse, Claude o kadar az "
                    "varsayım yapar ve o kadar isabetli fix önerir. 'Bu hatayı "
                    "düzelt' yerine 'Bu stack trace X işlemi sırasında oluşuyor, "
                    "Y input ile tekrarlanıyor, beklenen davranış Z' çok daha "
                    "etkili bir prompt."
                ),

                h("1.3 TDD ile Claude Code"),
                p(
                    "Test-Driven Development (TDD) Claude Code ile doğal bir "
                    "iş akışıdır. Döngü basit: önce testi yaz (Red — test fail "
                    "eder), sonra minimal implementasyonu yaz (Green — test geçer), "
                    "son olarak kodu temizle (Refactor — testler hâlâ geçer). "
                    "Claude'a bu sırayı açıkça söylemek kritik — aksi halde "
                    "Claude doğrudan implementasyona atlayabilir."
                ),
                table(
                    ["Aşama", "Claude'a söylediğin", "Beklenen sonuç"],
                    [
                        ["Red", "'Auth modülü için 6 test yaz — henüz implementasyon yok'",
                         "Testler yazılır, hepsi fail eder"],
                        ["Green", "'Bu testleri geçirecek minimal implementasyonu yaz'",
                         "İmplementasyon yazılır, testler geçer"],
                        ["Refactor", "'Kodu refactor et, testler hâlâ geçmeli'",
                         "Kod temizlenir, testler hâlâ geçer"],
                    ],
                ),
                tip(
                    "Claude bazen testleri geçirecek şekilde implementasyonu "
                    "şişirir veya gereksiz mock'lar ekler. 'YAGNI: sadece "
                    "testlerin gerektirdiği kadar yaz, fazlasını ekleme' "
                    "talimatı bunu önler."
                ),

                h("1.4 Kod İncelemesi Katmanları — Savunma Derinliği"),
                p(
                    "Claude Code tek bir review komutu değil, birden fazla "
                    "katmanda kod incelemesi sunar. Her katman farklı aşamada "
                    "farklı türde hataları yakalar:"
                ),
                table(
                    ["Katman", "Komut / Araç", "Nerede çalışır?",
                     "Ne bulur?", "Ne zaman kullan?"],
                    [
                        ["1 — Lokal Review",
                         "/code-review", "Terminalinde, anlık",
                         "Correctness bug, temizlik fırsatı",
                         "Her iterasyonda, her commit öncesi"],
                        ["2 — Security Review",
                         "/security-review", "Terminalinde, anlık",
                         "Güvenlik açıkları (injection, XSS vb.)",
                         "Güvenlik-kritik değişikliklerden sonra"],
                        ["3 — Ultrareview",
                         "/code-review ultra", "Bulutta, 5-10 dk",
                         "Derin bug, regresyon, mantık hatası",
                         "Büyük PR, riskli refactor, release öncesi"],
                        ["4 — Security Plugin",
                         "security-guidance", "Session boyunca otomatik",
                         "Yaygın güvenlik açıkları (per-edit + commit)",
                         "Her zaman (kuruluysa)"],
                        ["5 — Code Review (CI)",
                         "GitHub App / Actions", "PR açıldığında otomatik",
                         "Codebase bağlamında bug, regresyon",
                         "Her PR'da (Team/Enterprise, Gün 18)"],
                    ],
                ),
                keypoint(
                    "Savunma derinliği: tek bir katmana güvenme. Lokal "
                    "/code-review günlük sürüş, /security-review güvenlik "
                    "kontrolü, ultrareview büyük merge öncesi derin kontrol, "
                    "security-guidance session boyunca otomatik gözcü. "
                    "Her katman farklı aşamada farklı türde hataları yakalar."
                ),

                h("1.5 Review Bulgusu Karar Tablosu"),
                p(
                    "Claude Code'un review çıktısı bir öneri listesidir — "
                    "hakikat değil. Her bulguyu mühendis olarak "
                    "değerlendirmelisin:"
                ),
                table(
                    ["Bulgu Türü", "Karar", "Gerekçe"],
                    [
                        ["Gerçek bug", "✅ Uygula",
                         "Test veya kod akışıyla doğrulandı"],
                        ["Stil önerisi", "⏸️ Opsiyonel",
                         "Dersin/sprint'in hedefi correctness ise bekletilebilir"],
                        ["Belirsiz öneri", "🔍 İncele",
                         "Ek test veya manuel kontrol gerekir"],
                        ["False positive", "❌ Reddet",
                         "Mevcut davranış kasıtlı (intentional)"],
                        ["Security riski", "🚨 Önceliklendir",
                         "Exploit ihtimali ve etki alanı değerlendirilmeli"],
                    ],
                ),
                keypoint(
                    "Claude reviewer'dır ama karar verici engineer'dır. "
                    "Review bulgusunu körü körüne uygulama — her bulgu için "
                    "'gerçek bug mu, stil mi, false positive mı?' sorusunu sor."
                ),

                h("1.6 Sürüm ve Platform Bağımlılıkları"),
                warn(
                    "Bu derste anlatılan komutlar, plugin davranışları ve "
                    "plan limitleri Claude Code sürümüne, platforma ve "
                    "abonelik tipine göre değişebilir. Özellikle "
                    "/code-review ultra (cloud, credit bağımlı), "
                    "security-guidance plugin (sürüm bağımlı) ve Chrome "
                    "entegrasyonu (platform bağımlı, WSL desteklenmiyor) "
                    "için geçerlidir. Ders sırasında `claude --version`, "
                    "`/status` ve resmi dokümanlarla doğrulama yap."
                ),

                h("1.7 Chrome Entegrasyonu ile Canlı Debug (Teaser)"),
                p(
                    "Claude Code, Chrome extension ile canlı web "
                    "uygulamalarında console log okuma, DOM state inceleme ve "
                    "form validasyonu test etme gibi frontend debugging "
                    "işlemleri yapabilir. `--chrome` flag'i veya `/chrome` "
                    "komutuyla etkinleştirilir. Bu derste sadece kavramsal "
                    "tanıtım yapıyoruz — Chrome entegrasyonunun derinlemesine "
                    "pratiği Gün 18'de işlenecek."
                ),
                tip(
                    "Chrome entegrasyonu macOS ve Windows (PowerShell) "
                    "üzerinde çalışır; WSL desteklenmez. Ayrıca Bedrock, "
                    "Vertex veya Foundry üzerinden değil, doğrudan Anthropic "
                    "hesabı ile çalışır. Platform kısıtlamalarını kontrol et."
                ),
            ],
        },

        # ── BÖLÜM 2: PRATİK — ADIM ADIM ─────────────────────────────────
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                h("2.1 Stack Trace ile Debugging"),
                p(
                    "İlk pratik: kasıtlı bug'lı bir dosya oluştur ve Claude'un "
                    "sistematik debugging döngüsünü gözlemle. Burada amaç "
                    "'Claude düzeltsin' değil, 'Claude nasıl debug eder' "
                    "sürecini anlamak."
                ),
                steps([
                    "Todo App projesinde kasıtlı bir bug ekle. Örneğin: auth "
                    "modülünde `null` kontrolü eksik bir fonksiyon, bir async "
                    "işlemde hatalı `await` kullanımı veya yanlış bir array index.",

                    "Kodu çalıştır ve hata mesajını / stack trace'i kopyala.",

                    "Claude'a bağlam paketini ver: 'Bu hata POST /login "
                    "isteğinde oluşuyor, boş email ile tekrarlanıyor. "
                    "Beklenen: 400 Bad Request. Gerçek: 500 Internal Server "
                    "Error. Stack trace: [yapıştır]. İlgili dosya: "
                    "src/auth/login.js'",

                    "Claude'un dosya okuma → kök neden analizi → fix önerisi → "
                    "test yazma adımlarını gözlemle.",

                    "`git diff` ile Claude'un yaptığı değişiklikleri kontrol et. "
                    "Değişiklik minimal mi? Başka şeyleri bozmuş mu?",

                    "Testi çalıştır: fix doğru mu? Regresyon var mı?",
                ]),
                tip(
                    "'Düzelt' yerine 'kök nedeni bul, varsayımlarını söyle, "
                    "minimal fix öner, testle kanıtla' dersen Claude çok daha "
                    "sistematik çalışır. Debugging'de precision önemli — Claude'u "
                    "hızlı fix yerine analitik debugging'e yönlendir."
                ),
                warn(
                    "Claude'un fix'i her zaman doğru olmayabilir. Her "
                    "düzeltmeden sonra test çalıştır ve `git diff` ile "
                    "değişikliğin kapsamını doğrula. Fix sırasında başka "
                    "fonksiyonları bozmak yaygın bir risktir."
                ),

                h("2.2 TDD Döngüsü — Önce Test, Sonra Kod"),
                p(
                    "Şimdi TDD döngüsünü uygula. Amaç Claude'a 'kod yaz' "
                    "değil, 'kanıtlı geliştirme yap' demek."
                ),
                steps([
                    "Todo App'in auth modülü için test spec tanımla: "
                    "'Auth modülü için 6 test yaz: 2 happy path (başarılı "
                    "login, başarılı register), 2 edge case (çok uzun "
                    "email, boş password), 2 error case (yanlış password, "
                    "olmayan kullanıcı). Henüz implementasyon yok, sadece "
                    "testler.'",

                    "Testleri çalıştır — hepsi fail etmeli (Red). Fail etmiyorsa "
                    "testlerin gerçekten bir şeyi test ettiğinden emin ol.",

                    "'Bu testleri geçirecek minimal implementasyonu yaz. "
                    "YAGNI: sadece testlerin gerektirdiği kadar yaz, fazlasını "
                    "ekleme.' (Green)",

                    "Testleri tekrar çalıştır — hepsi geçmeli.",

                    "'Kodu refactor et: okunabilirliği artır, tekrarları azalt. "
                    "Testler hâlâ geçmeli.' (Refactor)",

                    "Son bir test çalıştırması yap — hâlâ hepsi geçiyor mu?",
                ]),
                keypoint(
                    "TDD'nin gücü 'test geçti' değil, 'test fail ettiğinde ne "
                    "olduğunu gördüm' noktasından gelir. Red aşamasını "
                    "atlamak TDD'nin değerini sıfırlar."
                ),

                h("2.3 /code-review ile Lokal İnceleme"),
                p(
                    "TDD döngüsünden sonra biriken değişiklikleri Claude'un "
                    "review etmesini sağla. `/code-review` branch'inin upstream'e "
                    "göre diff'ini ve uncommitted değişiklikleri inceler."
                ),
                steps([
                    "`/code-review` çalıştır — default effort ile bulgularını incele.",

                    "`/code-review --fix` çalıştır — Claude bulguları working "
                    "tree'ye otomatik uygular. Diff'i kontrol et.",

                    "Effort farkını gözlemle: `/code-review low` vs "
                    "`/code-review high`. Düşük effort → az ama yüksek güvenli "
                    "bulgular; yüksek effort → geniş kapsam, belirsiz bulgular "
                    "da dahil.",

                    "Review bulgularını karar tablosuyla değerlendir: hangi "
                    "bulgu gerçek bug? Hangisi stil önerisi? Hangisi false "
                    "positive? Her bulgu için 'uygula / reddet / sonraya bırak' "
                    "kararı ver.",
                ]),
                code(
                    "# /code-review kullanım örnekleri\n"
                    "/code-review              # default effort, mevcut diff\n"
                    "/code-review high         # geniş kapsamlı inceleme\n"
                    "/code-review --fix        # bulguları otomatik uygula\n"
                    "/code-review --comment    # PR'a inline yorum gönder\n"
                    "/code-review src/auth/    # sadece belirli path'i incele",
                    lang="bash",
                ),

                h("2.4 /security-review ile Mini Karşılaştırma"),
                p(
                    "`/security-review` pending değişikliklerdeki güvenlik "
                    "açıklarını inceler. `/code-review` ile farkını karşılaştırmak "
                    "review türlerinin odak farkını anlamana yardımcı olur."
                ),
                steps([
                    "`/security-review` çalıştır — güvenlik odaklı bulguları incele.",

                    "İki çıktıyı karşılaştır: `/code-review` correctness, "
                    "maintainability ve bug risk'e odaklanır; `/security-review` "
                    "injection, XSS, hardcoded secret gibi güvenlik risklerine odaklanır.",

                    "Her iki çıktıdan birer bulguyu karar tablosuyla değerlendir.",
                ]),
                tip(
                    "Bu karşılaştırmanın amacı güvenlik öğretmek değil, "
                    "review türleri arasındaki odak farkını göstermek. "
                    "Güvenliğin derinlemesine pratiği Gün 12 (hook'lar), "
                    "Gün 13 (plugin'ler) ve Gün 19'da (enterprise patterns) "
                    "işlenecek."
                ),

                h("2.5 Lint / Format — Kısa Destek Adımı"),
                p(
                    "Lint ve format, bu dersin ana konusu değil. Burada "
                    "sadece Claude'un fix'inden sonra otomatik kalite "
                    "kontrol komutu olarak kullanacağız. Hook ile "
                    "otomatikleştirme Gün 12'de işlenecek."
                ),
                steps([
                    "Projenin linter'ını çalıştır: Claude'a 'Tüm lint "
                    "hatalarını düzelt' de.",
                    "Formatter'ı çalıştır: Claude'a 'Kodu formatla' de.",
                    "Sonucu kontrol et: lint/format sonrası testler hâlâ geçiyor mu?",
                ]),
            ],
        },

        # ── BÖLÜM 3: DERİNLEŞ ────────────────────────────────────────────
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 /code-review ultra (Ultrareview) — Ne Zaman Kullanılır?"),
                p(
                    "Ultrareview bulutta çalışan, çok-ajanlı bir derin kod "
                    "incelemesidir. Reviewer fleet bağımsız olarak her bulguyu "
                    "doğrular — stil önerisi değil, gerçek bug'lara odaklanır. "
                    "Lokal kaynak kullanmaz, 5-10 dakika sürer ve background'da "
                    "çalışır. Ancak her zaman kullanılacak bir araç değil — "
                    "doğru senaryoda değerlidir."
                ),
                table(
                    ["Soru", "Cevap"],
                    [
                        ["Ne zaman?",
                         "Büyük PR, riskli refactor, release öncesi, "
                         "auth/data migration gibi kritik değişiklikler"],
                        ["Ne zaman değil?",
                         "Küçük lokal değişiklik, eğitim challenge'ı, basit "
                         "lint/test hataları, hızlı iterasyon sırasında"],
                        ["Neden dikkat?",
                         "Cloud tabanlı, credit bağımlı (Pro/Max: 3 ücretsiz "
                         "run, sonra $5-$20/review), plan/sürüm gereksinimi var"],
                        ["Alternatif?",
                         "Lokal `/code-review high` veya `/security-review` "
                         "— ücretsiz, anlık, iterasyon sırasında kullan"],
                    ],
                ),
                p(
                    "Aşağıdaki tablo üç review komutunu karşılaştırır:"
                ),
                table(
                    ["Özellik", "/code-review", "/review <pr>",
                     "/code-review ultra"],
                    [
                        ["Nerede çalışır?", "Lokal terminal", "Lokal terminal",
                         "Bulut (remote sandbox)"],
                        ["Ne inceler?", "Mevcut diff + uncommitted",
                         "GitHub PR diff'i", "Branch veya PR diff'i"],
                        ["Derinlik", "Effort seviyesine göre",
                         "Read-only özet", "Çok-ajanlı, doğrulanmış bulgular"],
                        ["Süre", "Saniyeler", "Saniyeler", "5-10 dakika"],
                        ["Maliyet", "Plan kullanımı", "Plan kullanımı",
                         "Usage credits ($5-$20)"],
                        ["En iyi kullanım", "Günlük iterasyon",
                         "Başkasının PR'ını inceleme", "Merge öncesi derin kontrol"],
                    ],
                ),
                keypoint(
                    "Lokal `/code-review` günlük sürüş; ultrareview büyük merge "
                    "öncesi derin kontrol. İkisi birbirinin yerine değil, "
                    "birbirini tamamlar."
                ),
                warn(
                    "Ultrareview'u bugün çalıştırmak zorunda değilsin. Pro/Max "
                    "hesaplarda 3 ücretsiz run var ve bunlar hesap başına tek "
                    "seferlik tahsis — yenilenmez. Eğitimde lokal `/code-review` "
                    "ile pratik yap, ultrareview'u gerçek projelerde sakla."
                ),
                tip(
                    "Non-interaktif kullanım: `claude ultrareview` komutu CI "
                    "script'lerinde çalışır. `--json` ile parseable çıktı verir. "
                    "Detay Gün 18'de (CI/CD entegrasyonu)."
                ),

                h("3.2 security-guidance Plugin (Bonus Pratik)"),
                p(
                    "security-guidance plugin, Claude'un kendi yazdığı kodu "
                    "güvenlik açıkları için otomatik olarak inceleyen bir "
                    "araçtır. Kurulduktan sonra ayrı komut gerektirmez — "
                    "otomatik çalışır. Üç katmanlı inceleme yapar:"
                ),
                table(
                    ["Katman", "Ne zaman?", "Nasıl?", "Maliyet"],
                    [
                        ["Per-edit pattern match", "Her dosya düzenlemesinde",
                         "Deterministik string match (model çağrısı yok)",
                         "Sıfır"],
                        ["End-of-turn review", "Her Claude turn sonunda",
                         "Ayrı model çağrısı, güvenlik odaklı prompt",
                         "1 ek model kullanımı"],
                        ["Commit review", "Commit veya push'ta",
                         "Agentic çok turlu inceleme (maks 20/saat)",
                         "Birden fazla model turu"],
                    ],
                ),
                p(
                    "Plugin'in en önemli özelliği: kodu yazan Claude instance "
                    "ile reviewer instance ayrıdır. Per-edit katmanı "
                    "deterministik string match ile çalışır (model çağrısı yok). "
                    "End-of-turn ve commit katmanları ayrı bir Claude çağrısı "
                    "ile, güvenlik odaklı prompt ve temiz context ile çalışır. "
                    "Yani 'kendi kendini değerlendirme' değil, bağımsız inceleme."
                ),
                steps([
                    "Plugin'i kur: `/plugin install security-guidance@claude-plugins-official` "
                    "(scope: user önerilir).",

                    "`/reload-plugins` ile mevcut session'da aktifleştir.",

                    "Kasıtlı güvenlik açıklı kod yaz. Örneğin: SQL query'de "
                    "string concatenation (injection riski), HTML template'te "
                    "escape edilmemiş kullanıcı girdisi (XSS), veya hardcoded "
                    "API key.",

                    "Claude'un per-edit pattern check → end-of-turn review → "
                    "commit review adımlarını gözlemle. Plugin bulguları "
                    "Claude'a talimat olarak döner ve Claude aynı session'da "
                    "düzeltir.",

                    "İsteğe bağlı: Proje kökünde `claude-security-guidance.md` "
                    "dosyası oluştur ve proje-spesifik güvenlik kuralları ekle.",
                ]),
                code(
                    "# claude-security-guidance.md örneği\n"
                    "# Proje kökünde: .claude/claude-security-guidance.md\n\n"
                    "# Güvenlik kuralları — bu repo için\n"
                    "- customer_id veya account_number'ı INFO loglamayın.\n"
                    "- SQL query'lerde string concatenation kullanmayın;\n"
                    "  parameterized query zorunlu.\n"
                    "- Tüm kullanıcı girdisi HTML encode edilmelidir.\n"
                    "- API key'ler environment variable'dan okunmalıdır;\n"
                    "  hardcoded secret commit edilmemelidir.",
                    lang="markdown",
                ),
                warn(
                    "AI code review — ister /code-review, ister security-guidance, "
                    "ister ultrareview olsun — güvenlik garantisi vermez. Bu "
                    "araçlar riskleri görünür kılar; son karar, tehdit modeli, "
                    "manuel inceleme, testler ve CI/CD güvenlik kontrolleriyle "
                    "birlikte verilmelidir."
                ),
                tip(
                    "Plugin bulunamazsa: `/plugin marketplace add "
                    "anthropics/claude-plugins-official` çalıştır, sonra "
                    "kurulumu tekrar dene. Plugin sürüm, ortam ve ağ erişimi "
                    "gereksinimleri için resmi dokümanı kontrol et."
                ),

                h("3.3 Chrome Entegrasyonu — Gün 18'e Yönlendirme"),
                p(
                    "Chrome entegrasyonu canlı web uygulamasında console log → "
                    "kaynak dosya → fix döngüsünü kapatır. Kullanım senaryoları: "
                    "frontend bug debug, form validasyonu doğrulama, visual "
                    "regression tespiti, web app'te data extraction. Bugün "
                    "sadece tanıtıyoruz — derinlemesine pratik Gün 18'de "
                    "(CI/CD ve Entegrasyonlar bölümünde)."
                ),
            ],
        },
    ],

    # ── PROMPT'LAR ────────────────────────────────────────────────────────
    "prompts": [
        {
            "title": "Hata Avcısı",
            "prompt": (
                "Bu hata mesajını analiz et: [stack trace yapıştır]. "
                "Hatanın kök nedenini bul, varsayımlarını söyle, "
                "minimal fix öner ve düzeltmenin doğru olduğunu bir test "
                "yazarak kanıtla."
            ),
            "note": (
                "Bağlam paketinin mümkün olduğunca çok maddesini ekle: "
                "repro koşulları, beklenen davranış, ilgili dosyalar."
            ),
        },
        {
            "title": "TDD Mühendisi",
            "prompt": (
                "Auth modülü için önce test suite'ini yaz: 2 happy path "
                "(başarılı login, başarılı register), 2 edge case (çok uzun "
                "email, boş password), 2 error case (yanlış password, olmayan "
                "kullanıcı). Testleri çalıştır — hepsi fail etmeli. Sonra "
                "testleri geçirecek minimal implementasyonu yaz. Son olarak "
                "kodu refactor et, testler hâlâ geçmeli."
            ),
            "note": (
                "Red → Green → Refactor sırasını açıkça belirt. "
                "'YAGNI: sadece testlerin gerektirdiği kadar yaz' talimatını ekle."
            ),
        },
        {
            "title": "Güvenlik Tarayıcısı",
            "prompt": (
                "Bu dosyada potansiyel güvenlik açıkları var mı? OWASP Top 10'a "
                "göre kontrol et. Bulduklarını severity ile birlikte listele "
                "ve her biri için fix öner."
            ),
            "note": (
                "Manuel güvenlik taraması. Plugin kurulu değilken veya "
                "spesifik bir dosyayı derinlemesine incelemek istediğinde kullan."
            ),
        },
        {
            "title": "Review & Fix",
            "prompt": (
                "/code-review --fix ile son değişiklikleri incele. Bulguları "
                "otomatik uygula. Sonra `/security-review` çalıştır ve "
                "güvenlik bulgularını listele."
            ),
            "note": (
                "/code-review correctness'a, /security-review güvenlik "
                "risklerine odaklanır. İkisini ardışık çalıştırmak "
                "kapsamlı bir review sağlar."
            ),
        },
        {
            "title": "Kapsamlı Test Yazıcı",
            "prompt": (
                "Bu modülün test coverage'ını artır. Mevcut testleri analiz et, "
                "eksik senaryoları belirle (boundary, null/undefined, async "
                "error, concurrent access) ve yeni testler ekle. Testleri "
                "çalıştır ve sonucu raporla."
            ),
            "note": (
                "Coverage sayısını değil, senaryo çeşitliliğini hedef al. "
                "%100 coverage anlamlı değilse değersizdir."
            ),
        },
        {
            "title": "Review Bulgusu Değerlendirici",
            "prompt": (
                "Bu review bulgularını karar tablosuna göre değerlendir. "
                "Her bulgu için: Gerçek bug mı? Stil önerisi mi? Security "
                "riski mi? False positive olabilir mi? Kararın: uygula / "
                "reddet / sonraya bırak. Gerekçe."
            ),
            "note": (
                "Claude'un review çıktısını körü körüne uygulamak yerine, "
                "mühendis olarak değerlendirmeyi pratik ettirir."
            ),
        },
    ],

    # ── CHALLENGE ─────────────────────────────────────────────────────────
    "challenge": {
        "title": "Auth Modülü: Debug, Test ve Review Döngüsü",
        "task": (
            "Todo App auth modülünde bir bug'ı testle yakala, düzelt ve "
            "Claude Code review ile doğrula."
        ),
        "requirements": [
            "En az 6 test yaz: 2 happy path, 2 edge case, 2 error case",
            "En az 1 test başlangıçta fail etmeli ve bug'ı görünür yapmalı",
            "Claude'a bağlam paketi ver (stack trace + test çıktısı + dosya bağlamı)",
            "Fix sonrası tüm testleri çalıştır",
            "/code-review veya /security-review ile son diff'i incelet",
            "Review bulgularını karar tablosuna göre değerlendir",
            "Debugging postmortem tamamla",
        ],
        "success": [
            "En az 6 test yazıldı: 2 happy path, 2 edge case, 2 error case",
            "En az 1 test başlangıçta fail etti ve bug'ı görünür yaptı",
            "Claude'a stack trace / test çıktısı / dosya bağlamı verildi",
            "Fix sonrası tüm testler geçti",
            "/code-review veya /security-review çalıştırıldı",
            "Review bulguları karar tablosuna göre değerlendirildi",
            "En az 1 bulgu için 'uygula / reddet / sonraya bırak' kararı verildi",
            "Debugging postmortem tamamlandı",
        ],
        "bonus": [
            "security-guidance plugin kuruldu ve aktif",
            "Kasıtlı güvenlik açığı eklendi (SQL injection veya XSS)",
            "Plugin veya /security-review ile risk yakalandı",
            "Güvenlik fix'i sonrası testler tekrar çalıştırıldı",
        ],
        "solution": {
            "intro": (
                "Bu challenge'ı adım adım çözmek için aşağıdaki prompt "
                "dizisini izle. Her adımda bir öncekinin çıktısını kontrol et."
            ),
            "prompts": [
                {"title": "1. Bug + testler", "prompt": (
                    "Auth modülünde kasıtlı bir bug oluştur. Örneğin: login fonksiyonunda "
                    "email validation'ı atla — boş string'le login olunabilsin. Sonra "
                    "6 test yaz: 2 happy path, 2 edge case (boş email, çok uzun password), "
                    "2 error case (yanlış password, olmayan kullanıcı). Testleri çalıştır."
                )},
                {"title": "2. Debug", "prompt": (
                    "Fail eden testi bul. Stack trace'i, test çıktısını ve ilgili "
                    "dosya bağlamını Claude'a ver: 'Bu test fail ediyor: [test çıktısı]. "
                    "Kök nedeni bul, minimal fix öner ve testle kanıtla.'"
                )},
                {"title": "3. Review", "prompt": (
                    "Fix sonrası tüm testleri çalıştır. Hepsi geçiyorsa "
                    "`/code-review` çalıştır. Bulguları karar tablosuna göre "
                    "değerlendir."
                )},
                {"title": "4. Postmortem", "prompt": (
                    "Debugging postmortem yaz: Bug neydi? Nasıl reproduce edildi? "
                    "Hangi test yakaladı? Root cause neydi? Fix ne yaptı? "
                    "Review'da ne kabul/reddedildi? Bir daha olmaması için "
                    "hangi guard eklendi?"
                )},
            ],
            "notes": [
                "/code-review effort seviyesi: ilk denemede default kullan; güvenlik konusunda endişen varsa `/security-review` ile tamamla.",
                "Coverage sayısı yerine senaryo çeşitliliğine odaklan.",
                "Postmortem, challenge'ın en değerli parçasıdır — atlamayın.",
            ],
            "pitfalls": [
                "Claude testleri geçirecek şekilde mock'ları şişirebilir — "
                "'gerçek davranışı test et, mock'u sadece dış bağımlılıklar "
                "için kullan' talimatı ver.",
                "Claude fix sırasında başka fonksiyonları bozabilir — her "
                "fix sonrası tüm testleri çalıştır, sadece fail eden testi değil.",
                "Review çıktısını körü körüne uygulama: 'stil önerisi' ve "
                "'gerçek bug' ayrımını yap. False positive'leri not et.",
                "security-guidance plugin kurulumda marketplace bulunamazsa: "
                "`/plugin marketplace add anthropics/claude-plugins-official` "
                "çalıştır, sonra tekrar dene.",
            ],
        },
        "postmortem_template": (
            "## Debugging Postmortem\n\n"
            "- **Bug neydi?**\n"
            "- **Nasıl reproduce edildi?**\n"
            "- **Hangi test bug'ı yakaladı?**\n"
            "- **Root cause neydi?**\n"
            "- **Fix ne yaptı?**\n"
            "- **Hangi review bulguları kabul edildi?**\n"
            "- **Hangi review bulguları reddedildi ve neden?**\n"
            "- **Bir daha olmaması için hangi test/guard eklendi?**"
        ),
    },

    # ── TAKEAWAYS ─────────────────────────────────────────────────────────
    "takeaways": [
        "Claude Code'a ne kadar bağlam (stack trace + repro koşulları + "
        "ilgili dosyalar + test çıktısı) verirsen, debugging o kadar isabetli olur",

        "TDD döngüsü (Red → Green → Refactor) Claude ile doğal bir iş "
        "akışıdır — 'önce test' talimatı kritik; Red aşamasını atlamak "
        "TDD'nin değerini sıfırlar",

        "/code-review hızlı iterasyon geri bildirimi, /security-review "
        "güvenlik kontrolü, /code-review ultra merge öncesi derin kontrol, "
        "security-guidance session boyunca otomatik gözcü — her katman "
        "farklı aşamada farklı türde hataları yakalar",

        "Ultrareview bulutta çok-ajanlı çalışır — her bulgu bağımsız olarak "
        "doğrulanır, style değil gerçek bug'lara odaklanır. Günlük iterasyon "
        "için değil, büyük merge öncesi için kullan",

        "security-guidance plugin'inin reviewer'ı, kodu yazan Claude "
        "instance'dan bağımsız ayrı bir çağrıdır — 'kendi kendini "
        "değerlendirme' değil, bağımsız inceleme",

        "Review bulgusunu körü körüne uygulama — karar tablosuyla "
        "değerlendir: gerçek bug mu, stil önerisi mi, false positive mı? "
        "Claude reviewer'dır ama karar verici engineer'dır",

        "AI code review — ister lokal, ister cloud, ister plugin — güvenlik "
        "garantisi vermez. Riskleri görünür kılar; son karar, tehdit modeli, "
        "testler ve CI/CD kontrolleriyle birlikte verilmelidir",

        "Debugging postmortem alışkanlığı bug'ı çözmekten önemli — çünkü "
        "tekrarını önler. 'Bug neydi? → Root cause → Guard' zincirini her "
        "debug oturumundan sonra yaz",
    ],

    # ── KAYNAKLAR ─────────────────────────────────────────────────────────
    "reading": {
        "official": [
            {
                "label": "Find bugs with ultrareview — /code-review ultra komutu, fiyatlandırma, non-interaktif kullanım",
                "url": "https://code.claude.com/docs/en/ultrareview",
            },
            {
                "label": "Catch security issues as Claude writes code — security-guidance plugin kurulum, 3 katmanlı inceleme, proje-spesifik kurallar",
                "url": "https://code.claude.com/docs/en/security-guidance",
            },
            {
                "label": "Commands reference — /code-review, /security-review, /review ve tüm komutların tam referansı",
                "url": "https://code.claude.com/docs/en/commands",
            },
            {
                "label": "Use Claude Code with Chrome — Chrome entegrasyonu, debugging workflow'ları, kurulum ve kısıtlamalar",
                "url": "https://code.claude.com/docs/en/chrome",
            },
        ],
        "community": [
            {
                "label": "Claude Code Best Practices (Anthropic Engineering) — debugging, test yazma, review stratejileri ve workflow organizasyonu",
                "url": "https://www.anthropic.com/engineering/claude-code-best-practices",
            },
        ],
        "extra": [
            {
                "label": "Code Review (CI) — GitHub PR Reviews — GitHub PR'larında otomatik kod incelemesi (Team/Enterprise, Gün 18'de detay)",
                "url": "https://code.claude.com/docs/en/code-review",
            },
        ],
    },

    # ── SONRAKİ GÜN ÖNİZLEME ─────────────────────────────────────────────
    "next_preview": (
        "Yarın (Gün 9) Claude Code'a yeni yetenekler kazandıracaksın: MCP "
        "(Model Context Protocol) ile GitHub, veritabanı ve web search gibi "
        "dış araçları bağlamayı, `claude mcp login` ile kimlik doğrulamayı "
        "ve kendi MCP server konfigürasyonunu yazmayı öğreneceksin."
    ),

    # ── KONTROL LİSTESİ ──────────────────────────────────────────────────
    "checklist": [
        "Bir stack trace'i Claude'a verip kök neden analizi + fix + test döngüsü uyguladım",
        "TDD döngüsünü (Red → Green → Refactor) Claude Code ile en az bir modül için çalıştırdım",
        "/code-review ile lokal kod incelemesi yaptım ve bulgularını inceledim",
        "/code-review --fix ile bulguların otomatik uygulanmasını denedim",
        "/code-review effort seviyelerinin (low vs high) çıktı farkını gözlemledim",
        "/security-review çalıştırdım ve /code-review ile farkını karşılaştırdım",
        "Review bulgularını karar tablosuyla değerlendirdim (uygula / reddet / sonraya bırak)",
        "/code-review ultra (ultrareview) kavramını ve ne zaman kullanılacağını biliyorum",
        "security-guidance plugin'inin ne yaptığını ve nasıl kurulacağını açıklayabiliyorum",
        "Günün challenge'ını tamamladım (6+ test + bug fix + review + postmortem)",
    ],
}


# ── Quick sanity check ───────────────────────────────────────────────────
if __name__ == "__main__":
    L = LESSON
    checks = []

    def chk(name, ok):
        checks.append((name, ok))
        print(f"  {'✅' if ok else '❌'} {name}")

    print("Schema validation – Gün 8")
    chk("day == 8", L["day"] == 8)
    chk("total_days == 20", L["total_days"] == 20)
    chk("week == 2", L["week"] == 2)
    chk("slug present", bool(L["slug"]))
    chk("title present", bool(L["title"]))
    chk("tagline present", bool(L["tagline"]))
    chk("intro present", bool(L["intro"]))

    chk("flow == 4 phases", len(L["flow"]) == 4)
    chk("prerequisites present", len(L["prerequisites"]) >= 1)
    chk("tools_needed present", len(L["tools_needed"]) >= 1)

    obj_count = len(L["objectives"])
    chk(f"objectives count ({obj_count}) in 5-6", 5 <= obj_count <= 6)

    sec_count = len(L["sections"])
    chk(f"sections count ({sec_count}) == 3", sec_count == 3)

    prompt_count = len(L["prompts"])
    chk(f"prompts count ({prompt_count}) >= 4", prompt_count >= 4)

    chk("challenge.task present", bool(L["challenge"]["task"]))
    chk("challenge.requirements present", len(L["challenge"]["requirements"]) >= 1)
    succ_count = len(L["challenge"]["success"])
    chk(f"challenge.success count ({succ_count}) >= 1", succ_count >= 1)
    chk("challenge.bonus present", len(L["challenge"].get("bonus", [])) >= 1)
    chk("challenge.solution.intro present", bool(L["challenge"]["solution"]["intro"]))
    chk("challenge.solution.prompts present", len(L["challenge"]["solution"]["prompts"]) >= 1)
    chk("challenge.solution.notes present", bool(L["challenge"]["solution"]["notes"]))
    chk("challenge.solution.pitfalls present", len(L["challenge"]["solution"]["pitfalls"]) >= 1)
    chk("challenge.postmortem_template present", bool(L["challenge"].get("postmortem_template")))

    tw_count = len(L["takeaways"])
    chk(f"takeaways count ({tw_count}) in 6-8", 6 <= tw_count <= 8)

    off_count = len(L["reading"]["official"])
    chk(f"reading.official count ({off_count}) >= 3", off_count >= 3)

    chk("next_preview present", bool(L["next_preview"]))

    cl_count = len(L["checklist"])
    chk(f"checklist count ({cl_count}) >= 8", cl_count >= 8)

    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    print(f"\nSonuç: {passed}/{total}")
    if passed == total:
        print("✅ TÜM SCHEMA KONTROLLERİ GEÇTİ")
    else:
        failed = [n for n, ok in checks if not ok]
        print(f"❌ Başarısız: {failed}")
