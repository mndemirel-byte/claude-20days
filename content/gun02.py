# -*- coding: utf-8 -*-
"""Gün 2 — Temel Kullanım, İzinler ve Auto Mode (v2.0, Temmuz 2026)."""
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table

LESSON = {
    "day": 2, "total_days": 20, "week": 1,
    "slug": "temel-kullanim-izinler-auto-mode",
    "title": "Temel Kullanım, İzinler ve Auto Mode",
    "tagline": "Doğru soru sormayı öğren, doğru kod al — ve izinleri yönet",
    "tier": "🟢 Kademe 1",
    "date_label": "Temmuz 2026",

    "intro": (
        "Bu derste Claude Code'un araçlarını, izin sistemini ve auto mode'u öğreneceksin. "
        "İyi ve kötü prompt farkını bizzat deneyerek görecek, context window kavramıyla "
        "tanışacak ve ilk gerçek uygulamanı — CLI not defterini — Claude Code ile "
        "baştan sona oluşturacaksın."
    ),

    "flow": [
        {"phase": "1 · Teori",
         "dur": "40 dk",
         "desc": "Araçlar, izin sistemi, auto mode, context window, prompt kalitesi"},
        {"phase": "2 · Pratik — Adım Adım",
         "dur": "45 dk",
         "desc": "Araç gözlemi, izin modları geçişi, prompt denemeleri, debugging"},
        {"phase": "3 · Derinleş",
         "dur": "35 dk",
         "desc": "Prompt pattern'leri, done definition, git diff alışkanlığı, context farkındalığı"},
        {"phase": "4 · Challenge",
         "dur": "40 dk",
         "desc": "CLI Not Defteri v1 + çözüm rehberi"},
    ],

    "prerequisites": [
        "Gün 1 tamamlanmış (Claude Code kurulu, kimlik doğrulama yapılmış)",
        "Temel terminal komutları (cd, ls, mkdir)",
        "Aktif internet bağlantısı",
    ],
    "tools_needed": [
        "Terminal (Claude Code kurulu)",
        "VS Code (isteğe bağlı)",
        "Web tarayıcı (docs için)",
    ],

    "objectives": [
        "Claude Code'un temel araçlarını (Read, Write, Edit, Bash, Grep, Glob, WebSearch/WebFetch) "
        "ve agentic loop içindeki rollerini açıklayabileceksin.",
        "İzin modlarını (Manual/default, acceptEdits, plan, auto) anlayacak, Shift+Tab ile "
        "aralarında geçiş yapabilecek ve her modun hangi risk seviyesinde uygun olduğunu ayırt edebileceksin.",
        "Auto mode'un izin yorgunluğunu nasıl azalttığını, risk sınıflandırma modelini (classifier) "
        "ve neden review'un yerini almadığını açıklayabileceksin.",
        "Context window kavramını (doluluk, /context, /compact, /clear) ve bilinçli context "
        "yönetiminin neden önemli olduğunu kavrayacaksın.",
        "Aynı görevi kötü, orta ve iyi prompt ile ifade ederek çıktı kalitesi farkını gözlemleyecek; "
        "scope, requirement ve verification içeren prompt yapısını uygulayabileceksin.",
        "İlk gerçek uygulamanı (CLI not defteri) Claude Code ile baştan sona yazdırıp, çalıştırıp, "
        "hatasını düzelttirip, git diff ile doğrulayacaksın.",
    ],

    # =========================================================================
    # BÖLÜM 1: TEORİK TEMEL
    # =========================================================================
    "sections": [
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                # --- 1.1 Araç Kutusu ---
                h("1.1 Claude Code'un Araç Kutusu (Tools)"),

                p(
                    "Gün 1'de Claude Code'un agentic loop içinde çalıştığını gördün: "
                    "Anla → Planla → Araç Kullan → Doğrula → Düzelt. Bugün bu döngüdeki "
                    "'Araç Kullan' adımını derinlemesine inceliyoruz. Claude Code her adımda "
                    "bir veya birden fazla araç çağırır ve hangi aracı kullanacağına kendisi "
                    "karar verir. Senin görevin outcome'u tarif etmek; araç seçimini ona bırakmak."
                ),

                p("Claude Code'un araçlarını iki katmanda tanıyalım:"),

                h("Temel Araçlar (Gün 2'de gözlemleyeceksin)"),

                table(
                    ["Araç", "Ne yapar", "Ne zaman görünür", "Başlangıç riski"],
                    [
                        ["Read", "Dosya içeriğini okur",
                         "Kod incelerken, proje taranırken", "Düşük"],
                        ["Write", "Yeni dosya oluşturur",
                         "Sıfırdan dosya yazarken", "Orta"],
                        ["Edit", "Mevcut dosyayı değiştirir",
                         "Refactor, fix, iyileştirme sırasında", "Orta"],
                        ["Bash", "Terminal komutu çalıştırır",
                         "Test, build, run, pip install sırasında", "Değişken"],
                        ["Grep", "Metin/pattern arar",
                         "Projede anahtar kelime/pattern ararken", "Düşük"],
                        ["Glob", "Dosya deseni bulur",
                         "Dosya keşfinde (*.py, *.json)", "Düşük"],
                        ["WebFetch / WebSearch", "Web'den bilgi çeker/arar",
                         "Dokümantasyon, güncel API bilgisi gerektiğinde", "Orta"],
                    ]
                ),

                h("İleri Seviye Araçlar (sonraki derslere köprü)"),

                table(
                    ["Araç", "Ne yapar", "Hangi gün"],
                    [
                        ["Agent (subagent)",
                         "İzole context'te uzman görev çalıştırır", "Gün 11"],
                        ["MCP tools",
                         "Harici servislerle entegrasyon (GitHub, Slack vb.)", "Gün 9"],
                    ]
                ),

                keypoint(
                    "Claude hangi aracı kullanacağına kendisi karar verir; sen outcome'u tarif et, "
                    "araç seçimini ona bırak. Ancak büyük repo veya riskli alanda çalışırken arama "
                    "kapsamını ve dokunulmayacak dosyaları açıkça belirtmek hem hızı hem güvenliği artırır."
                ),

                tip(
                    "Claude'un her adımda hangi aracı kullandığını terminalde gözlemle. Araç adı "
                    "(Read, Write, Edit, Bash...) ve hedefi (dosya adı, komut) terminalde görünür. "
                    "Bu farkındalık, ileride daha verimli prompt yazmana yardımcı olacak."
                ),

                # --- 1.2 İzin Sistemi ---
                h("1.2 İzin Sistemi ve İzin Modları"),

                p(
                    "Claude Code her araç çağrısında bir karar verir: bu aksiyonu otomatik mi "
                    "yapsın, yoksa senden izin mi istesin? Bu kararı belirleyen şey izin modudur. "
                    "Shift+Tab ile mevcut izin modları arasında geçiş yaparsın. Hangi modların "
                    "cycle'da göründüğü ortamına, Claude Code sürümüne ve hesap ayarlarına "
                    "bağlıdır — her mod her zaman listede olmayabilir."
                ),

                p(
                    "Temel cycle: default (Manual) → acceptEdits → plan. Auto mode, hesap "
                    "gereksinimleri karşılanırsa cycle'a eklenir. bypassPermissions ise yalnızca "
                    "başlangıçta özel bir flag ile etkinleştirilmişse görünür."
                ),

                table(
                    ["Mod", "Davranış", "Ne zaman kullanılır", "Risk seviyesi"],
                    [
                        ["Manual / default",
                         "Claude okur; dosya değiştirme, komut çalıştırma ve network "
                         "aksiyonlarında izin ister",
                         "İlk hafta, hassas işler, tanımadığın repo",
                         "Düşük (her şey kontrollü)"],
                        ["acceptEdits",
                         "Dosya editlerini ve güvenli filesystem Bash komutlarını "
                         "(mkdir, touch, rm, rmdir, mv, cp, sed) otomatik kabul eder; "
                         "diğer Bash komutları ve kapsam dışı path'ler hâlâ izin ister",
                         "Küçük iterasyonlar, refactor döngüleri",
                         "Orta"],
                        ["plan",
                         "Önce dosyaları okur, araştırır ve plan sunar; onay almadan "
                         "edit yapmaz. Planı onaylayınca istediğin moda geçer",
                         "Büyük değişiklik öncesi, mimari kararlar",
                         "Düşük (düşünme alanı)"],
                        ["auto",
                         "Rutin izinlerin bir kısmını azaltır; ayrı bir risk sınıflandırma "
                         "modeli (classifier) aksiyonları çalışmadan önce değerlendirir",
                         "Güvenilen repo, uzun otonom görev",
                         "Orta-yüksek"],
                        ["bypassPermissions",
                         "Tüm izin kontrollerini atlar",
                         "Yalnızca izole container, VM veya sandbox",
                         "Yüksek"],
                    ]
                ),

                keypoint(
                    "acceptEdits, 'her şeyi otomatik onayla' demek değildir. Dosya editleri ve "
                    "güvenli filesystem komutları (mkdir, touch, rm, rmdir, mv, cp, sed) çalışma "
                    "dizininde otomatik kabul edilir; ama diğer Bash komutları, kapsam dışı path'ler "
                    "ve korumalı dosyalar (protected paths) hâlâ onay ister."
                ),

                keypoint(
                    "Plan mode, başlangıç seviyesi için en değerli moddur. 'Önce ne yapılacağını "
                    "anla, sonra diske dokun' disiplinini öğretir. Planı onayladığında istediğin "
                    "izin modunda (auto, acceptEdits veya manual) çalışmaya geçersin."
                ),

                warn(
                    "bypassPermissions modunu yalnızca tamamen izole ortamlarda (container, VM, "
                    "sandbox) kullan. Kendi makinende, gerçek projende asla kullanma. Bu eğitimde "
                    "pratikte denenmeyecektir; bilgi amaçlı tanıyorsun."
                ),

                # --- 1.3 Auto Mode ---
                h("1.3 Auto Mode"),

                p(
                    "Auto mode, Claude'dan ayrı çalışan bir risk sınıflandırma modeli (classifier) "
                    "kullanır. Bu classifier, her aksiyonu çalışmadan önce değerlendirir ve risk "
                    "kategorisine göre otomatik onaylar veya sana sorar. Sonuç: rutin izin "
                    "onaylarının bir kısmı ortadan kalkar, akış hızlanır."
                ),

                bullets([
                    "Neden cazip: Uzun görevlerde sürekli onay vermek yerine Claude'un akışını "
                    "bozmadan çalışmasını sağlar.",
                    "Neden kör güvenilmez: Auto mode bir güvenlik garantisi değil, ek koruma "
                    "katmanıdır. Production deploy, migration, secret içeren dosyalar, destructive "
                    "operasyonlar ve force push gibi riskli işlemlerde manuel review zorunlu "
                    "kabul edilmelidir.",
                    "Ne zaman kullanılmaz: Tanımadığın repo, production ortam, hassas veri "
                    "içeren dosyalar.",
                    "Kullanılabilirlik: Claude Code sürümü, model, provider ve organizasyon "
                    "ayarlarına bağlıdır. Derste kendi ortamında Shift+Tab ile görünüp "
                    "görünmediğini kontrol edeceğiz.",
                ]),

                warn(
                    "Auto mode bir research preview'dur. İzin yorgunluğunu azaltır ama review'un "
                    "yerini almaz. Auto mode'da bile git diff ve test sonucu okumadan işi bitmiş "
                    "sayma. Yapılandırma detaylarını (güvenilen repo/domain tanımlama, izin "
                    "kuralları) Gün 7 ve Gün 12'de derinlemesine işleyeceğiz."
                ),

                tip(
                    "Auto mode'u ilk kez güvenli bir deneme repo'sunda dene; kendi projende "
                    "kullanmadan önce davranışına aşina ol."
                ),

                # --- 1.4 Context Window ---
                h("1.4 Context Window: Claude'un Kısa Süreli Hafızası"),

                p(
                    "Context window, Claude'un mevcut oturumda bildiği her şeydir: konuşma "
                    "geçmişi, okunan dosyalar, CLAUDE.md, auto memory, tool sonuçları ve bazı "
                    "sistem içerikleri. Her dosya okuma, her yanıt, her araç çıktısı context'e "
                    "eklenir. Büyük context mümkün ama sınırsız değil."
                ),

                p(
                    "Bazı güncel modeller 1M (bir milyon) token context destekler — örneğin Sonnet 5 "
                    "native 1M ile çalışır; diğer modellerde [1m] varyantı seçilebilir. "
                    "Kullanılabilirlik model, provider ve plan ayarına bağlıdır."
                ),

                table(
                    ["Komut", "Ne yapar", "Ne zaman kullanılır"],
                    [
                        ["/context",
                         "Context doluluk görselleştirmesi (kategorilere göre dağılım)",
                         "Context'in ne kadar dolduğunu görmek istediğinde"],
                        ["/compact",
                         "Konuşma geçmişini yapısal bir özete dönüştürüp yer açar",
                         "Context dolmaya başladığında veya yeni göreve geçerken"],
                        ["/clear",
                         "Tüm konuşmayı siler, taze oturum başlatır",
                         "Tamamen alakasız bir işe geçerken"],
                    ]
                ),

                keypoint(
                    "Context = Claude'un kısa süreli hafızası. Bilinçli yönetmek bir beceridir "
                    "ve Gün 7'de derinlemesine işleyeceğiz. Bugün sadece /context ile durumu "
                    "görebilmeyi öğren."
                ),

                # --- 1.5 Prompt Kalitesi ---
                h("1.5 Prompt Kalitesi = Çıktı Kalitesi"),

                p(
                    "Claude Code'a verdiğin prompt'un kalitesi, aldığın çıktının kalitesini "
                    "doğrudan belirler. İyi bir prompt sadece 'ne yap' demez; scope, requirement, "
                    "constraint ve verification içerir."
                ),

                p("İyi bir Claude Code prompt'unun 5 bileşeni:"),

                table(
                    ["Bileşen", "Ne anlama gelir", "Örnek"],
                    [
                        ["Goal (Hedef)",
                         "Ne yapılmasını istiyorsun",
                         "CLI not defteri uygulaması yaz"],
                        ["Scope (Kapsam)",
                         "Hangi dosyalarda çalışsın, hangi dizinde",
                         "Sadece app.py ve notes.json oluştur"],
                        ["Requirements (Gereksinimler)",
                         "Ne üretsin, hangi özellikler olsun",
                         "Ekle, listele, sil, ara komutları olsun"],
                        ["Verification (Doğrulama)",
                         "Nasıl test edilsin",
                         "Çalıştır, örnek not ekle, sonucu özetle"],
                        ["Done / Tamamlanma Tanımı",
                         "Ne zaman 'bitti' sayılacak",
                         "Program hatasız çalışıyor, git diff kontrol edildi"],
                    ]
                ),

                p("Structured prompt formatı — bugünden itibaren bu yapıyı kullan:"),

                code(
                    "Goal: Python ile CLI not uygulaması yaz.\n\n"
                    "Scope: Sadece app.py ve notes.json oluştur.\n\n"
                    "Requirements:\n"
                    "- Not ekle, listele, sil, ara komutları olsun\n"
                    "- JSON dosyasında sakla\n"
                    "- Türkçe karakterleri bozma\n\n"
                    "Verification: Uygulamayı çalıştır, örnek not ekle, listele ve sil.\n\n"
                    "Done / Tamamlanma Tanımı:\n"
                    "- Program hatasız çalışıyor\n"
                    "- JSON dosyasında veri persist ediyor\n"
                    "- git diff kontrol edildi"
                ),

                keypoint(
                    "Done / Tamamlanma Tanımı alanı, Claude'a 'ne zaman durması gerektiğini' söyler "
                    "ve seni de 'gerçekten bitti mi?' diye düşünmeye zorlar. Bu alışkanlığı "
                    "şimdiden edin — ileride auto mode ve agent teams kullandığında, done definition "
                    "olmadan 'bitmiş gibi görünen ama aslında eksik' iş riskiyle karşılaşırsın."
                ),

                p("Aynı görevin kötü, orta ve iyi prompt ile ifadesi:"),

                table(
                    ["Kalite", "Prompt", "Beklenen sonuç"],
                    [
                        ["Kötü",
                         "Not defteri yap",
                         "Belirsiz: hangi dil? Ne tür not? Nasıl saklansın?"],
                        ["Orta",
                         "Python ile CLI not defteri yaz",
                         "Daha iyi ama scope, test ve done yok"],
                        ["İyi",
                         "Python ile CLI not defteri yaz. Ekle, listele, sil ve ara olsun. "
                         "notes.json'da sakla. Türkçe bozulmasın. Çalıştır ve test et.",
                         "Net scope, gereksinimler, doğrulama adımı var"],
                    ]
                ),

                tip(
                    "Prompt'a beklenen dosya adı, test kriteri veya çıktı formatı eklemek "
                    "sonucu dramatik iyileştirir. 'Ne istediğini tanımla, nasıl yapacağını bırak' "
                    "— ama büyük/riskli işte scope ve constraint ver."
                ),
            ],
        },

        # =====================================================================
        # BÖLÜM 2: PRATİK — ADIM ADIM
        # =====================================================================
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                # --- 2.1 Araçları Gözlemleme ---
                h("2.1 Araçları Gözlemleme"),

                p(
                    "İlk pratik adımımız Claude Code'un araçlarını canlı gözlemlemek. "
                    "Aşağıdaki prompt'u Claude Code'a ver ve terminalde hangi araçların "
                    "kullanıldığını izle:"
                ),

                code(
                    "Python ile hello_notes.py oluştur.\n"
                    "Program notes.txt dosyasına 3 satır örnek not yazsın.\n"
                    "Sonra dosyayı okuyup satır sayısını ekrana bassın.\n"
                    "Programı çalıştır ve sonucu doğrula.",
                    "prompt"
                ),

                steps([
                    "Claude Code'un terminaldeki çıktısını izle: Write (dosya oluşturma), "
                    "Bash (python komutu çalıştırma), Read (dosya okuma) araçlarını göreceksin.",
                    "Her araç kullanımında Claude'un ne söylediğini oku: hangi dosyaya ne "
                    "yazıyor, hangi komutu çalıştırıyor.",
                    "Manual/default modda olduğun için her adımda izin isteyecek — diff'leri "
                    "ve komutları bilinçli incele.",
                    "Sonuç başarılıysa /context çalıştır ve context doluluk durumunu gör.",
                ]),

                tip(
                    "Claude'un kullandığı her aracın adı terminalde açıkça görünür: "
                    "'Read file', 'Write file', 'Execute bash' gibi. Bu çıktıları okumak, "
                    "Claude'un ne yaptığını anlamanın en hızlı yolu."
                ),

                # --- 2.2 İzin Modları Arasında Geçiş ---
                h("2.2 İzin Modları Arasında Geçiş"),

                p(
                    "Şimdi aynı küçük görev üzerinde farklı izin modlarını deneyeceğiz. "
                    "Tek bir dosya (counter.py) üzerinde çalışarak her modun farkını gözlemle:"
                ),

                steps([
                    "Manual/default mod: 'Bir counter.py oluştur, 1'den 10'a say' de. "
                    "Dosya oluşturma ve çalıştırma iznini gör.",
                    "Shift+Tab → acceptEdits mod: 'counter.py'ye geri sayım özelliği ekle' de. "
                    "Dosya editinin otomatik kabul edildiğini, ama python counter.py "
                    "komutunun hâlâ izin isteyebildiğini gözlemle.",
                    "Shift+Tab → plan mod: 'counter.py'ye dosyaya yazma özelliği ekle' de. "
                    "Claude'un önce plan sunduğunu ve onay bekleyip edit yapmadığını gör. "
                    "Planı onayladığında hangi moda geçeceğini seç.",
                    "Eğer auto mode ortamında mevcutsa (Shift+Tab ile görünüyorsa): "
                    "güvenli bir deneme klasöründe kısa bir görev dene. Görev: "
                    "'counter.py'ye toplam sonucu hesaplayan bir özellik ekle ve test et.' "
                    "Claude'un izin sormadan çalışmasını gözlemle.",
                ]),

                warn(
                    "Auto mode'da çalışırken terminali dikkatle izle; beklenmedik bir şey "
                    "görürsen Escape ile durdurabilirsin. Her zaman git diff ile "
                    "sonuçları kontrol et."
                ),

                # --- 2.3 Prompt Denemeleri ---
                h("2.3 Prompt Denemeleri (Aynı Görev, 3 Kalite)"),

                p(
                    "Şimdi prompt kalitesinin çıktıyı nasıl etkilediğini bizzat deneyeceksin. "
                    "Aynı uygulama (CLI not defteri) için 3 farklı kalitede prompt ver ve "
                    "sonuçları karşılaştır. Her denemeden önce /clear ile temiz oturum başlat:"
                ),

                steps([
                    "Kötü prompt: 'Not defteri yap' — Claude'un ne üreteceğini gözlemle. "
                    "Muhtemelen çok basit veya yanlış dilde bir şey çıkacak.",
                    "Orta prompt: 'Python ile CLI not defteri yaz' — Daha iyi ama scope, "
                    "test ve dosya formatı belirsiz.",
                    "İyi prompt: 'Python ile CLI not defteri yaz. Ekle, listele, sil ve "
                    "ara komutları olsun. Notları notes.json dosyasında sakla. Hatalı "
                    "girişlerde kullanıcıyı uyar. Programı çalıştır ve test et.' — "
                    "Sonuçtaki farkı gör: dosya sayısı, hata yönetimi, test durumu.",
                ]),

                p(
                    "Üç sonucu karşılaştır: hangi prompt daha eksiksiz kod üretti? Hangisi "
                    "test etti? Hangisi hata yönetimi ekledi? Bu fark, eğitimin geri kalanında "
                    "sürekli karşına çıkacak."
                ),

                # --- 2.4 Debugging ---
                h("2.4 Hata Mesajıyla Debugging"),

                p(
                    "Gerçek hayatta Claude Code'u en çok kullanacağın senaryolardan biri: "
                    "bir hata mesajını yapıştırıp düzeltmesini istemek. Ama burada da "
                    "prompt kalitesi kritik."
                ),

                p("İki debugging prompt'unu karşılaştır:"),

                code(
                    "# Zayıf debugging prompt:\n"
                    "Bu hatayı düzelt:\n"
                    "Traceback (most recent call last):\n"
                    "  File \"app.py\", line 12, in delete_note\n"
                    "    notes.pop(note_id)\n"
                    "IndexError: pop index out of range",
                    "prompt"
                ),

                code(
                    "# Güçlü debugging prompt:\n"
                    "Bu CLI not uygulamasında not silme sırasında\n"
                    "aşağıdaki hata oluşuyor.\n\n"
                    "Beklenen davranış: ID verilince ilgili not silinsin,\n"
                    "yoksa kullanıcıya uyarı versin.\n\n"
                    "Stack trace:\n"
                    "Traceback (most recent call last):\n"
                    "  File \"app.py\", line 12, in delete_note\n"
                    "    notes.pop(note_id)\n"
                    "IndexError: pop index out of range\n\n"
                    "Kodu incele, minimal düzeltme yap,\n"
                    "sonra aynı senaryoyu çalıştırarak doğrula.",
                    "prompt"
                ),

                steps([
                    "Zayıf prompt'u ver ve Claude'un adımlarını izle.",
                    "Aynı hatayı güçlü prompt ile ver — farkı gör: Claude bağlamı "
                    "anlıyor, minimal fix yapıyor ve doğruluyor.",
                    "Claude'un debugging adımlarını gözlemle: Read → analiz → Edit → "
                    "Bash (test çalıştırma).",
                ]),

                keypoint(
                    "Claude'a sadece hatayı değil, çalışma niyetini ve beklenen davranışı da "
                    "ver. Bu, düzeltme kalitesini dramatik artırır."
                ),

                # --- 2.5 Git Diff Alışkanlığı ---
                h("2.5 Git Diff Alışkanlığı"),

                p(
                    "Claude Code her değişiklik yaptığında, sonuçları kontrol etme alışkanlığını "
                    "bugünden başlatıyoruz. acceptEdits ve auto mode kullanırken 'sonradan review' "
                    "becerisi şart."
                ),

                code("git status    # hangi dosyalar değişti?\ngit diff      # ne değişti?"),

                tip(
                    "Claude'un yaptığı her değişiklikten sonra git diff oku. Bu, ileride "
                    "auto mode'a geçtiğinde güvenlik ağın olacak. Aynı alışkanlığı challenge'da "
                    "da uygulayacaksın."
                ),
            ],
        },

        # =====================================================================
        # BÖLÜM 3: PRATİK — DERİNLEŞ / UYGULAMA
        # =====================================================================
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 Prompt Pattern'leri"),

                p(
                    "Farklı görevler farklı prompt yapıları gerektirir. İşte başlangıç için "
                    "4 temel pattern — her birini ne zaman kullanacağını öğren:"
                ),

                table(
                    ["Pattern", "Kullanım", "Örnek prompt"],
                    [
                        ["Yap ve test et",
                         "Basit, tek adımlı görevler",
                         "Bir fibonacci fonksiyonu yaz, 10. terimi hesaplat ve doğrula."],
                        ["Analiz et ve öner",
                         "Mevcut kodu değerlendirmek",
                         "CLI not defterini incele ve 3 iyileştirme öner, henüz uygulama."],
                        ["Planla, onay al, uygula",
                         "Büyük değişiklik, mimari karar",
                         "Not defterine kategori özelliği eklemek istiyorum. Önce plan yap."],
                        ["Kısıtlı görev",
                         "Hassas, büyük repo, belirli scope",
                         "Sadece app.py içindeki delete_note fonksiyonunu düzelt, "
                         "başka dosyaya dokunma."],
                    ]
                ),

                tip(
                    "'Planla, onay al, uygula' pattern'i ile plan mode doğal bir uyum sağlar. "
                    "Bu pattern'i büyük değişikliklerden önce kullanmayı alışkanlık haline getir."
                ),

                # --- 3.2 Done Definition ---
                h("3.2 Done Definition Disiplini"),

                p(
                    "Her görevde 'tamamlandı' ne demek? Bu soruyu sormak, hem Claude'un doğru "
                    "noktada durmasını hem de senin sonucu bilinçli doğrulamanı sağlar."
                ),

                code(
                    "Done / Tamamlanma Tanımı:\n"
                    "Bu görev ancak şu durumda tamamlanmış sayılır:\n"
                    "- Program hatasız çalıştı\n"
                    "- En az 3 senaryo manuel denendi\n"
                    "- git diff ile değişiklikler kontrol edildi\n"
                    "- Claude hangi dosyaları değiştirdiğini özetledi"
                ),

                p(
                    "Bu format, Claude Code eğitimini gerçek development disiplinine bağlar. "
                    "Bu alışkanlığı şimdiden edin — ileride auto mode ve agent teams "
                    "kullandığında, done definition olmadan 'bitmiş gibi görünen ama aslında "
                    "eksik' iş riskiyle karşılaşırsın."
                ),

                # --- 3.3 Context Farkındalığı ---
                h("3.3 Context Farkındalığı (Gün 7'ye Hazırlık)"),

                p(
                    "Context yönetimini Gün 7'de derinlemesine işleyeceğiz. Bugün sadece "
                    "temel farkındalığı oluşturuyoruz:"
                ),

                steps([
                    "/context komutuyla context doluluk durumunu gör. Kategorilere göre "
                    "dağılımı (system prompt, CLAUDE.md, dosyalar, konuşma) incele.",
                    "Birkaç dosya okutup /context'i tekrar çalıştır — doluluk değişimini gözlemle.",
                    "/compact ile konuşma geçmişini özetlemeyi dene; öncesi ve sonrasındaki "
                    "doluluk farkını gör.",
                    "/clear ile taze oturum başlat — ne zaman /compact ne zaman /clear "
                    "kullanman gerektiğini anla.",
                ]),

                tip(
                    "Büyük araştırma görevlerinde context'i korumak için subagent'a delege "
                    "etmek etkilidir — subagent kendi izole context'inde çalışır, sadece "
                    "sonuç senin context'ine döner. Bunu Gün 11'de pratikte uygulayacağız."
                ),
            ],
        },
    ],

    # =========================================================================
    # PROMPT KÜTÜPHANESİ
    # =========================================================================
    "prompts": [
        {
            "title": "Araç gözlem",
            "prompt": (
                "Python ile hello_notes.py oluştur. Program notes.txt dosyasına "
                "3 satır örnek not yazsın. Sonra dosyayı okuyup satır sayısını ekrana "
                "bassın. Programı çalıştır ve sonucu doğrula. Her adımda hangi aracı "
                "kullandığını görmek istiyorum."
            ),
        },
        {
            "title": "İzin modu karşılaştırma",
            "prompt": (
                "Bir fibonacci fonksiyonu yaz, test et ve çalıştır. Şu an Manual/default "
                "moddayım; her adımda ne izin istediğini görmek istiyorum."
            ),
            "note": (
                "Aynı görevi acceptEdits modunda tekrar dene ve izin davranışı farkını "
                "gözlemle."
            ),
        },
        {
            "title": "Structured prompt (iyi örnek)",
            "prompt": (
                "Goal: Python ile CLI not uygulaması yaz.\n"
                "Scope: Sadece app.py ve notes.json oluştur.\n"
                "Requirements:\n"
                "- Not ekle, listele, sil, ara komutları olsun\n"
                "- Notları JSON dosyasında sakla\n"
                "- Türkçe karakterleri bozma (ensure_ascii=False)\n"
                "Verification: Programı çalıştır, not ekle, listele, ara ve sil.\n"
                "Done / Tamamlanma Tanımı:\n"
                "- Program hatasız çalışıyor\n"
                "- JSON dosyasında veri persist ediyor\n"
                "- git diff kontrol edildi"
            ),
        },
        {
            "title": "Debugging (bağlamlı)",
            "prompt": (
                "Bu CLI not uygulamasında not silme sırasında aşağıdaki hata oluşuyor.\n"
                "Beklenen davranış: ID verilince ilgili not silinsin, yoksa kullanıcıya "
                "uyarı versin.\n"
                "Stack trace:\n"
                "Traceback (most recent call last):\n"
                "  File \"app.py\", line 12, in delete_note\n"
                "    notes.pop(note_id)\n"
                "IndexError: pop index out of range\n\n"
                "Kodu incele, minimal düzeltme yap, sonra aynı senaryoyu çalıştırarak doğrula."
            ),
            "note": (
                "Gerçek stack trace'ler ne kadar tam olursa Claude o kadar iyi düzeltir. "
                "Beklenen davranışı belirtmek düzeltme kalitesini artırır."
            ),
        },
        {
            "title": "Plan modu denemesi",
            "prompt": (
                "Plan moduna geç (Shift+Tab). Sonra:\n"
                "CLI not defterine kategori özelliği eklemek istiyorum. Her nota bir "
                "kategori atanabilsin ve kategoriye göre filtreleme yapılabilsin.\n"
                "Önce plan yap, onay bekle."
            ),
            "note": (
                "Claude'un planı sunmasını gözlemle: edit yapmayacak, onay bekleyecek. "
                "Planı onaylayınca hangi modda devam edeceğini seçeceksin."
            ),
        },
    ],

    # =========================================================================
    # CHALLENGE
    # =========================================================================
    "challenge": {
        "title": "CHALLENGE: CLI Not Defteri v1 — İlk Vibe Coding Projen (🟢 Kademe 1)",
        "task": (
            "Claude Code ile komut satırından çalışan bir not defteri uygulaması oluştur. "
            "Amaç sadece kod yazmak değil; Claude'un araçlarını, izin modlarını ve prompt "
            "kalitesinin etkisini bizzat gözlemlemek."
        ),
        "requirements": [
            "Python ile yazılsın",
            "Not ekleme, listeleme, silme ve arama",
            "Notlar notes.json dosyasında saklansın (kapat-aç sonrası veri korunsun)",
            "İlk çalıştırmada notes.json dosyası yokken program çökmemeli (dosyayı "
            "otomatik oluşturmalı)",
            "Türkçe karakterler bozulmadan saklanmalı ve gösterilmeli (ş, ç, ğ, ü, ö, ı)",
            "Basit hata yönetimi (geçersiz komut, olmayan not ID'si)",
            "Claude çalıştırıp test etsin",
        ],
        "success": [
            "Uygulama hatasız çalışıyor",
            "4 temel işlem çalışıyor (ekle, listele, sil, ara)",
            "Notlar JSON dosyasında persist ediyor (kapat-aç sonrası kaybolmuyor)",
            "İlk çalıştırmada notes.json yokken program çökmüyor (dosyayı otomatik oluşturuyor)",
            "Türkçe karakterler bozulmadan saklanıyor ve gösteriliyor",
            "Hatalı girişlerde program çökmüyor, uyarı veriyor",
            "git diff ile değişiklikler kontrol edildi",
        ],
        "solution": {
            "intro": (
                "Tek structured prompt ile temel versiyonu oluştur, sonra iterasyonla "
                "iyileştir. Aynı görevi önce Manual/default modda, sonra acceptEdits "
                "modunda yaptırarak farkı gözlemle."
            ),
            "prompts": [
                {
                    "title": "1) İlk üretim (structured prompt)",
                    "prompt": (
                        "Goal: Python ile CLI not defteri uygulaması yaz.\n"
                        "Scope: Sadece app.py ve notes.json oluştur.\n"
                        "Requirements:\n"
                        "- Komutlar: ekle, listele, sil, ara\n"
                        "- Notları notes.json dosyasında sakla\n"
                        "- İlk çalıştırmada dosya yoksa boş liste ile oluştur\n"
                        "- Türkçe karakterleri koru (ensure_ascii=False)\n"
                        "- Hatalı girişlerde uyarı ver, çökme\n"
                        "Verification: Programı çalıştır, not ekle, listele, ara ve sil.\n"
                        "Done / Tamamlanma Tanımı:\n"
                        "- Program hatasız çalışıyor\n"
                        "- 3 kez çalıştırıp farklı senaryolar denendi\n"
                        "- git diff kontrol edildi"
                    ),
                },
                {
                    "title": "2) İyileştirme (gözlemden sonra)",
                    "prompt": (
                        "CLI not defterini incele ve şu iyileştirmeleri yap:\n"
                        "- Her nota otomatik zaman damgası ekle\n"
                        "- Notları ID ile silmeyi destekle\n"
                        "- --help komutu ekle\n"
                        "Sadece app.py dosyasını değiştir. Çalıştır ve test et."
                    ),
                },
                {
                    "title": "3) Doğrulama",
                    "prompt": (
                        "Uygulamayı 3 kez çalıştır, her seferinde farklı senaryo dene:\n"
                        "1) Not ekle ve listele\n"
                        "2) Olmayan bir ID ile silmeyi dene (hata yönetimi)\n"
                        "3) Türkçe karakterli not ekle ve ara\n"
                        "Sonuçları özetle."
                    ),
                },
            ],
            "notes": [
                "Claude'un hangi araçları kullandığını izle: Write (dosya oluşturma), "
                "Edit (düzenleme), Bash (çalıştırma/test).",
                "İzin isteme anlarını gözlemle: dosya oluşturmadan ve python komutunu "
                "çalıştırmadan önce (Manual/default modda).",
                "Her adımda git diff ile değişiklikleri kontrol et.",
                "Aynı görevi bir kez Manual/default modda, bir kez acceptEdits modunda "
                "yaptır; akış farkını gözlemle.",
            ],
            "pitfalls": [
                "Çok belirsiz prompt ('not defteri yap') — scope + requirement + "
                "verification + done definition ver.",
                "İlk çalıştırmada notes.json yokken FileNotFoundError — dosya yoksa "
                "boş liste ile oluşturma kontrolü gerekli.",
                "Türkçe karakterlerin JSON'da bozulması (\\u015f gibi escape) — "
                "json.dump(..., ensure_ascii=False) kontrolü şart.",
                "Dosya yolu hardcoding — çalışma dizinine göreceli path kullan.",
                "İzinleri okumadan hızlıca onaylamak — ilk günlerde her diff'i ve "
                "komutu bilinçli incele.",
            ],
        },
    },

    # =========================================================================
    # TAKEAWAYS
    # =========================================================================
    "takeaways": [
        "Claude Code 7 temel araç kullanır (Read, Write, Edit, Bash, Grep, Glob, "
        "WebFetch/WebSearch); hangi aracı kullanacağına kendisi karar verir.",
        "İzin modları (Manual/default → acceptEdits → plan → auto) farklı güvenlik-verimlilik "
        "denge noktaları sunar; Shift+Tab ile geçiş yaparsın.",
        "acceptEdits dosya editlerini ve güvenli filesystem komutlarını otomatik kabul eder; "
        "ama her şeyi sınırsız çalıştırmaz.",
        "Auto mode izin yorgunluğunu azaltır ama bir research preview'dur; review'un yerini "
        "almaz — git diff ve test sonucu kontrol etmeye devam et.",
        "Context window, Claude'un kısa süreli hafızasıdır; /context ile izle, /compact ile "
        "yer aç, /clear ile taze başla.",
        "İyi prompt = Goal + Scope + Requirements + Verification + Done / Tamamlanma Tanımı. "
        "Bu 5 bileşen çıktı kalitesini dramatik artırır.",
        "Debugging'de Claude'a sadece hatayı değil, beklenen davranışı ve bağlamı da ver.",
        "git diff alışkanlığını bugünden başlat — ileride auto mode ve agent teams için "
        "güvenlik ağın olacak.",
    ],

    # =========================================================================
    # READING
    # =========================================================================
    "reading": {
        "official": [
            {"label": "⭐ Claude Code Tools & Capabilities (araçlar)",
             "url": "https://code.claude.com/docs/en/overview"},
            {"label": "⭐ Permission Modes (izin modları, auto mode)",
             "url": "https://code.claude.com/docs/en/permission-modes"},
            {"label": "⭐ Best Practices — Prompt Techniques",
             "url": "https://code.claude.com/docs/en/best-practices"},
            {"label": "⭐ Context Window",
             "url": "https://code.claude.com/docs/en/context-window"},
        ],
        "community": [
            {"label": "Prompt Library (resmi prompt örnekleri)",
             "url": "https://code.claude.com/docs/en/prompt-library"},
            {"label": "ClaudeLog — Community Best Practices",
             "url": "https://claudelog.com/"},
        ],
        "extra": [
            {"label": "What's New (haftalık yeni özellikler)",
             "url": "https://code.claude.com/docs/en/whats-new"},
        ],
    },

    # =========================================================================
    # NEXT PREVIEW
    # =========================================================================
    "next_preview": (
        "CLAUDE.md ve Auto Memory — Claude'a projenin kurallarını öğretecek, "
        "CLAUDE.md hiyerarşisini anlayacak, auto memory'nin nasıl çalıştığını görecek "
        "ve CLI Not Defteri'ne bir CLAUDE.md ekleyerek kod kalitesindeki farkı "
        "gözlemleyeceksin."
    ),

    # =========================================================================
    # CHECKLIST
    # =========================================================================
    "checklist": [
        "Claude Code'un temel araçlarını sayabiliyorum: Read, Write, Edit, Bash, "
        "Grep, Glob, WebFetch/WebSearch.",
        "Manual/default modda Claude'un ne zaman izin istediğini gözlemledim.",
        "acceptEdits modunun dosya editlerini otomatik kabul ettiğini ama her Bash "
        "komutunu sınırsız çalıştırmadığını biliyorum.",
        "Plan mode'da Claude'un önce araştırıp plan sunduğunu, onay almadan edit "
        "yapmadığını gördüm.",
        "Auto mode'un izin yorgunluğunu azalttığını ama review'un yerini almadığını "
        "açıklayabiliyorum.",
        "Shift+Tab ile mevcut izin modları arasında geçiş yapabiliyorum.",
        "Aynı görevi kötü, orta ve iyi prompt ile denedim; farkı gözlemledim.",
        "Structured prompt formatını (Goal / Scope / Requirements / Verification / "
        "Done) uyguladım.",
        "Bir stack trace'i bağlamıyla birlikte Claude'a verip minimal fix + test "
        "döngüsü yaptım.",
        "CLI Not Defteri v1 challenge'ını tamamladım.",
        "git status ve git diff ile Claude'un yaptığı değişiklikleri kontrol ettim.",
        "/context ile context kullanımını gördüm; /compact ve /clear farkını temel "
        "düzeyde açıklayabiliyorum.",
    ],
}
