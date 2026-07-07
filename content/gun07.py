# -*- coding: utf-8 -*-
"""Gün 7 — Context Window Yönetimi ve Verimli Çalışma (v2.0, Temmuz 2026)."""
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table

LESSON = {
    "day": 7,
    "total_days": 20,
    "week": 2,
    "slug": "context-window-verimli-calisma",
    "title": "Context Window Yönetimi ve Verimli Çalışma",
    "tagline": "Claude'un hafızasını yönetmek senin görevin",
    "tier": None,
    "date_label": "Temmuz 2026",

    # ------------------------------------------------------------------ intro
    "intro": (
        "Dün tekrarlayan işleri skill'lere devrettin. Bugünün amacı daha fazla context "
        "kullanmak değil — aynı işi daha az context, daha az maliyet ve daha az state "
        "kaybıyla yapmayı öğrenmek. Context window Claude'un çalışma belleğidir ve "
        "en kıt kaynağındır; onu nasıl yönettiğin, uzun oturumlarda aldığın sonucun "
        "kalitesini doğrudan etkiler."
    ),

    # ------------------------------------------------------------------ flow
    "flow": [
        {"phase": "1 · Context Anatomisi",  "dur": "30 dk",
         "desc": "Context window nedir, neyi tutar; başlangıçta otomatik yüklenenler; 200K → 1M geçişi; doluluk seviyeleri ve stratejiler"},
        {"phase": "2 · Adım Adım Pratik",   "dur": "45 dk",
         "desc": "/context ile analiz, /compact stratejileri, compaction sonrası ne korunur, /cost ve /usage, session yönetimi"},
        {"phase": "3 · Derinleş: /goal ve İleri Teknikler", "dur": "40 dk",
         "desc": "/goal ile tamamlanma koşulu, subagent delegasyonu, context budgeting karar ağacı, anti-pattern'ler"},
        {"phase": "4 · Challenge",          "dur": "35 dk",
         "desc": "Todo App — context-bilinçli geliştirme: 2 endpoint, context log, compact ve goal uygulaması"},
    ],

    "prerequisites": [
        "Gün 1-6 tamamlanmış (kurulum, temel kullanım, CLAUDE.md, proje yapısı, Git/checkpointing, skill'ler)",
        "Todo App proje iskeleti mevcut (Gün 4'ten)",
    ],
    "tools_needed": [
        "Claude Code (terminal veya IDE eklentisi)",
        "Todo App proje dizini",
    ],

    # ------------------------------------------------------------------ objectives
    "objectives": [
        "Context window'un neleri içerdiğini (system prompt, CLAUDE.md, auto memory, skill açıklamaları, MCP araç adları, dosya okumaları, komut çıktıları, konuşma geçmişi) sayabilir",
        "/context çıktısını okuyup hangi kategorinin en çok yer kapladığını tespit edip buna göre optimizasyon kararı verebilir",
        "/compact, /compact <focus>, /clear ve auto-compact arasındaki farkı açıklayabilir; her birini doğru senaryoda kullanabilir",
        "Compaction sonrası hangi bilginin diskten yeniden yüklendiğini, hangisinin yeniden okunana kadar kaybolduğunu bilir ve buna göre bilgiyi doğru yere (CLAUDE.md vs. path-scoped rule vs. skill) yerleştirebilir",
        "/goal ile bir tamamlanma koşulu tanımlayıp Claude'un koşul sağlanana kadar çok turlu çalışmasını başlatıp izleyebilir",
        "/cost ile hızlı, /usage ile detaylı maliyet takibi yapabilir ve uzun oturumları session bölme veya subagent delegasyonuyla optimize edebilir",
    ],

    # ================================================================== SECTIONS
    "sections": [
        # ---------------------------------------------------------- BÖLÜM 1
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                h("1.1 Context Window Nedir ve Neden En Kıt Kaynaktır"),
                p(
                    "Context window, Claude'un bir oturumda \"gördüğü\" her şeyi tutar: "
                    "konuşma geçmişi, okuduğu dosyalar, çalıştırdığı komutların çıktıları, "
                    "CLAUDE.md, auto memory, yüklü skill'ler ve sistem talimatları. Bu pencere "
                    "sabit değil — çalıştıkça dolar."
                ),
                p(
                    "Context büyüdükçe üç şey olur: token maliyeti artar (her istek tüm context'i "
                    "yeniden gönderir), önemli bilginin sinyal/gürültü oranı düşebilir ve oturumun "
                    "başında verdiğin talimatların pratikte daha az takip edilme riski artar. Bu "
                    "kesin bir doğrusal kural değil, ama pratikte gözlemlenen bir eğilimdir — bu "
                    "yüzden kalıcı kuralları konuşma geçmişine değil CLAUDE.md'ye yazmak daha güvenlidir."
                ),
                keypoint(
                    "Context, Claude'un hafızası değil; senin yönettiğin kıt bir kaynak. "
                    "Bugünün hedefi daha fazla context doldurmak değil, aynı işi daha az "
                    "context ve daha az state kaybıyla bitirmek."
                ),

                h("1.2 Oturum Başlarken Otomatik Yüklenen Bileşenler"),
                p(
                    "İlk prompt'unu yazmadan önce bile context'in bir kısmı dolar. Resmi "
                    "dokümantasyona göre şu kategoriler oturum başında (veya ilgili dosya "
                    "okunduğunda) yüklenir. Aşağıdaki token değerleri gerçek bir örnek "
                    "oturumdan alınmış temsili rakamlardır — kurulumuna, CLAUDE.md uzunluğuna "
                    "ve yüklü skill sayısına göre değişir; kesin sayı olarak ezberleme."
                ),
                table(
                    ["Bileşen", "Yaklaşık Token (örnek)", "Açıklama"],
                    [
                        ["System prompt", "~birkaç bin", "Davranış, araç kullanımı, format talimatları — görünmez"],
                        ["Auto memory", "~yüzlerce", "Claude'un öğrendiklerini biriktirdiği dosya — görünmez"],
                        ["Ortam bilgisi", "~yüzlerce", "Çalışma dizini, platform, Git branch/status"],
                        ["MCP araç adları", "~yüzlerce", "Sadece isimler; tam şemalar talep üzerine (tool search) yüklenir"],
                        ["Skill açıklamaları", "~yüzlerce", "Tek satırlık açıklamalar; disable-model-invocation olanlar hariç"],
                        ["~/.claude/CLAUDE.md", "~yüzlerce", "Global (kullanıcı seviyesi) tercihler"],
                        ["Proje kökündeki CLAUDE.md", "~1000+", "Proje kuralları — genelde en büyük tekil kalem"],
                    ],
                ),
                tip(
                    "Kesin sayıları merak ediyorsan kendi oturumunda /context çalıştır — o "
                    "an geçerli, güncel ve doğru rakamları sana gösterir. Proje kökündeki "
                    "CLAUDE.md'yi 200 satırın altında tutmak en etkili tek önlemdir; uzun "
                    "referans içeriğini skill'lere veya path-scoped rule'lara taşı."
                ),

                h("1.3 Çalışma Sırasında Context'i Dolduran Şeyler"),
                bullets([
                    "Her dosya okuma — büyük dosyalar orantısız yer kaplar",
                    "Path-scoped rule'lar — eşleşen dosya okunduğunda mesaj geçmişine otomatik yüklenir",
                    "Komut çıktıları (test, build, grep vb.) — özellikle uzun loglar",
                    "Hook çıktıları — additionalContext JSON ile context'e girer",
                    "Claude'un kendi yanıtları ve ara analiz metni",
                ]),
                tip(
                    "Dosya okumaları context'in en büyük tüketicisidir. Prompt'unu spesifik "
                    "tut (\"auth.ts'deki login bug'ını düzelt\") ki Claude gereksiz dosya "
                    "okumasın. Geniş kapsamlı araştırma görevlerinde subagent'a devret — "
                    "bkz. Bölüm 3.2."
                ),

                h("1.4 Model Bazında Context Kapasitesi"),
                p(
                    "Claude Code'da desteklenen context boyutu modele, plana ve sağlayıcıya "
                    "göre değişir. Ders yazıldığı tarihte (Temmuz 2026) resmi dokümantasyona "
                    "göre durum aşağıdaki gibidir; bu tablo dersin hazırlandığı tarihteki "
                    "resmi dokümantasyona göre hazırlanmıştır. Claude model adları, context "
                    "limitleri ve plan bazlı erişim koşulları değişebileceği için eğitim "
                    "gününde code.claude.com/docs üzerinden tekrar kontrol edilmelidir."
                ),
                table(
                    ["Model", "1M Context Desteği", "Not"],
                    [
                        ["Sonnet 5", "Evet — native", "API'de her zaman 1M; [1m] suffix'e gerek yok"],
                        ["Opus 4.8 / 4.7 / 4.6", "Evet", "API'de her zaman 1M; Max/Team/Enterprise'da otomatik upgrade"],
                        ["Fable 5", "Evet", "Uzun/otonom görevler için tasarlanmış en yetenekli model"],
                        ["Sonnet 4.6", "Evet, ama usage credit gerekir", "1M için her planda ek kullanım kredisi şart"],
                        ["Haiku 4.5", "Hayır (200K)", "Subagent ve hızlı görevler için tercih edilir"],
                    ],
                ),
                warn(
                    "CLAUDE_CODE_DISABLE_1M_CONTEXT=1 ayarı 1M seçeneklerini model picker'dan "
                    "kaldırır. LLM gateway kullanıyorsan (ANTHROPIC_BASE_URL üzerinden), Claude "
                    "Code 1M desteğini otomatik doğrulayamaz — model picker'da açıkça 1M "
                    "seçeneğini seçmen gerekir."
                ),

                h("1.5 Context Doluluk Seviyeleri ve Genel Strateji"),
                table(
                    ["Seviye", "Durum", "Önerilen Aksiyon"],
                    [
                        ["%0-30", "Serbest alan", "Normal çalış"],
                        ["%30-50", "Rahat", "Büyük araştırma varsa subagent'ı düşün"],
                        ["%50-70", "Dikkatli", "/compact <focus> ile odaklı sıkıştırma; görev değişiminde /clear"],
                        ["%70-90", "Kritik", "/compact zorunlu; yeni görev başlatma"],
                        ["%90+", "Otomatik devreye girer", "Auto-compact tetiklenir; gerekirse /clear + /resume"],
                    ],
                ),
            ],
        },

        # ---------------------------------------------------------- BÖLÜM 2
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                h("2.1 /context ile Oturumunu Analiz Et"),
                steps([
                    "/context çalıştır → kategori bazlı token dağılımını gör",
                    "En çok yer kaplayan 2-3 kategoriyi not al",
                    "/memory ile hangi CLAUDE.md ve auto memory dosyalarının aktif olduğunu kontrol et",
                    "/mcp ile bağlı MCP server'ların token maliyetini incele",
                ]),

                h("2.2 /compact Stratejileri"),
                steps([
                    "Basit compact: /compact — Claude en önemli gördüğünü kendi belirler",
                    "Odaklı compact: /compact Focus on the API changes and test results — sen önceliği belirlersin",
                    "Kısmi compact: Esc Esc ile mesaj listesini aç → bir checkpoint seç → \"Summarize from here\" (o noktadan sonrasını özetler) veya \"Summarize up to here\" (o noktaya kadarını özetler, sonrasını tam tutar)",
                    "CLAUDE.md'ye kalıcı compact talimatı ekle: # Compact Instructions başlığı altında \"test çıktılarını ve değiştirilen dosya listesini her zaman koru\" gibi bir not",
                ]),
                code(
                    "# Compact Instructions\n"
                    "When compacting, always preserve the full list of\n"
                    "modified files and the exact test commands used."
                ),
                tip(
                    "/compact <focus> auto-compact'tan üstündür çünkü neyin korunacağına "
                    "sen karar verirsin — otomatik geçiş Claude'un tahminine bırakır."
                ),

                h("2.3 Compaction Sonrası Ne Olur"),
                p(
                    "Bu bölümdeki bilgiler resmi dokümantasyonda yer aldığı için korunuyor "
                    "— ancak Claude Code'un iç davranışı sürüm ve plana göre değişebileceğinden "
                    "tabloyu kesin garanti değil, gözlemlenen genel davranış olarak oku."
                ),
                table(
                    ["Mekanizma", "Compaction Sonrası Davranış"],
                    [
                        ["System prompt + output style", "Değişmez — mesaj geçmişinin parçası değil"],
                        ["Proje kökündeki CLAUDE.md", "Diskten yeniden yüklenir"],
                        ["Auto memory", "Diskten yeniden yüklenir"],
                        ["paths: frontmatter'lı path-scoped rule'lar", "Kaybolur — eşleşen dosya tekrar okunduğunda yeniden yüklenir"],
                        ["Alt dizin CLAUDE.md'leri", "Kaybolur — o dizindeki dosya tekrar okunduğunda yeniden yüklenir"],
                        ["Çağrılan skill body'leri", "Yeniden enjekte edilir; resmi dokümana göre skill başına ~5.000, toplamda ~25.000 token sınırı var; sınır aşılırsa en eski çağrılan skill önce düşer"],
                        ["Skill açıklamaları listesi (başlangıç)", "Yeniden yüklenmez — sadece fiilen çağrılmış skill'ler korunur"],
                    ],
                ),
                keypoint(
                    "Bir kuralın compaction'dan sağ çıkmasını istiyorsan paths: frontmatter'ı "
                    "kaldır veya kuralı proje kökündeki CLAUDE.md'ye taşı."
                ),

                h("2.4 Maliyet Farkındalığı: Hızlı Kontrol için /cost, Analiz için /usage"),
                p(
                    "İki komutun rolü farklıdır. /cost, o anki oturumun tahmini maliyetine "
                    "hızlı bir bakış sağlar — anlık farkındalık için. /usage ise çok daha "
                    "kapsamlıdır: session token kullanımı, tahmini yerel maliyet, plan "
                    "kullanım çubukları, aktivite istatistikleri, skill/subagent/plugin/MCP "
                    "bazlı kırılım ve 24 saat / 7 gün görünüm arasında geçiş sunar."
                ),
                warn(
                    "Pro/Max gibi abonelik planlarında /cost ve /usage'ın gösterdiği dolar "
                    "tahmini, gerçek faturanla birebir örtüşmeyebilir. API billing için "
                    "otoriter kaynak Anthropic Console'daki Usage ekranıdır."
                ),

                h("2.5 Session Yönetimi ile Context Kontrolü"),
                bullets([
                    "/clear — görev değişiminde context'i tamamen sıfırlar; eski konuşma /resume ile geri getirilebilir",
                    "/rename — oturuma isim ver, sonradan bulması kolay olsun",
                    "--continue — son oturuma kaldığın yerden devam et",
                    "--resume — oturum listesinden seçerek devam et",
                    "/btw — context'i büyütmeden hızlı bir soru sor; yanıt kapatılabilir bir overlay'de görünür, konuşma geçmişine girmez",
                ]),
            ],
        },

        # ---------------------------------------------------------- BÖLÜM 3
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 /goal ile Tamamlanma Koşulu Tanımlama"),
                p(
                    "/goal, bir tamamlanma koşulu belirlemeni sağlar; Claude o koşul "
                    "sağlanana kadar art arda turlar boyunca çalışmaya devam eder — sen her "
                    "adımda yeni prompt yazmak zorunda kalmazsın. Bugün /goal'u tanıyıp "
                    "kontrollü bir ilk uygulama yapacaksın; ileri seviye kullanım (büyük "
                    "migration'lar, backlog temizliği gibi çok adımlı işler) ilerleyen "
                    "günlerde pratikle derinleşecek."
                ),
                steps([
                    "/goal all tests in test/auth pass and the lint step is clean gibi bir koşulla başlat — komut hemen bir tur başlatır, ayrı prompt yazmana gerek yok",
                    "Aktifken ◎ /goal active göstergesi ne kadar süredir çalıştığını gösterir",
                    "Her tur sonunda küçük/hızlı bir model (varsayılan: Haiku) koşulu değerlendirir ve kısa bir gerekçeyle yes/no döner; bu gerekçe transcript'te görünür",
                    "/goal (argümansız) → o ana kadar harcanan tur ve token miktarını gösterir",
                    "/goal clear → hedefi iptal eder",
                ]),
                p(
                    "Evaluator dosya okumaz veya komut çalıştırmaz — sadece Claude'un "
                    "konuşmada üretmiş olduğu çıktıyı değerlendirir. Bu yüzden koşulu, "
                    "Claude'un kendi çıktısıyla kanıtlayabileceği şekilde yazmalısın."
                ),
                keypoint(
                    "İyi bir /goal koşulunun üç özelliği vardır: tek ölçülebilir son durum "
                    "(\"npm test exits 0\"), Claude'un nasıl kanıtlayacağı (test sonucu "
                    "transcript'te görünür) ve varsa sınır (\"or stop after 15 turns\"). "
                    "Koşul en fazla 4.000 karakter olabilir."
                ),
                warn(
                    "/goal, güvendiğin (trust dialog onaylanmış) çalışma alanlarında "
                    "çalışır çünkü evaluator hooks sisteminin bir parçasıdır. "
                    "disableAllHooks ayarlıysa veya yönetilen ayarlarda "
                    "allowManagedHooksOnly açıksa /goal devre dışı kalır ve neden "
                    "çalışmadığını sana bildirir."
                ),

                h("3.2 Subagent ile Context Delegasyonu"),
                p(
                    "\"Use subagents to investigate X\" dediğinde, araştırma ayrı bir "
                    "context penceresinde yapılır — dosya okumaları oraya gider, sadece "
                    "özet ana konuşmana döner. Bu, büyük kod tabanı taramalarında context "
                    "tasarrufunun en etkili yollarından biridir."
                ),
                tip(
                    "Kural: kod yazmadan önce geniş araştırma gerekiyorsa subagent kullan. "
                    "Doğrudan bir dosyayı düzenlemek gibi dar kapsamlı işlerde subagent "
                    "gereksiz — ekstra context penceresi açmanın maliyeti fayda getirmez."
                ),

                h("3.3 Token Tasarrufu Teknikleri Karşılaştırması"),
                table(
                    ["Teknik", "Ne Zaman Kullanılır"],
                    [
                        ["Subagent delegasyonu", "Geniş araştırma / çok dosyalı tarama görevleri"],
                        ["/compact <focus>", "Görev geçişlerinde, öncelik senin elinde kalsın istiyorsan"],
                        ["/clear + /resume", "Alakasız görevler arasında tam sıfırlama gerektiğinde"],
                        ["/btw", "Context'i büyütmeden hızlı bir soru sorarken"],
                        ["Effort level düşürme (/effort low)", "Basit, derin muhakeme gerektirmeyen görevlerde"],
                        ["CLAUDE.md'den skill'e taşıma", "Uzun, sadece belirli görevlerde gereken referans talimatları için"],
                    ],
                ),

                h("3.4 Context Budgeting Karar Ağacı"),
                p(
                    "Her yeni adımda şu soruları sırayla sor — komutları ezberlemek yerine "
                    "karar vermeyi öğrenmek asıl amaç:"
                ),
                code(
                    "Yeni görev mi?\n"
                    "  Evet -> /clear veya yeni session\n"
                    "  Hayir -> devam\n\n"
                    "Repo arastirmasi mi gerekiyor?\n"
                    "  Evet -> subagent kullan\n"
                    "  Hayir -> hedef dosyalari sinirli oku\n\n"
                    "Context %50+ mi?\n"
                    "  Evet -> /compact <focus>\n"
                    "  Hayir -> devam\n\n"
                    "Gorev cok turlu ve olculebilir mi?\n"
                    "  Evet -> /goal\n"
                    "  Hayir -> manuel ilerle\n\n"
                    "Sadece kucuk bir soru mu?\n"
                    "  Evet -> /btw",
                ),

                h("3.5 Anti-Pattern'ler ve Kaçınılacak Hatalar"),
                bullets([
                    "\"Kitchen sink session\": Bir görevden alakasız başka bir konuya atlayıp sonra geri dönmek — context'i gereksiz kirletir",
                    "Yanlış giden bir turu düzeltmek için /compact kullanmak: Doğru araç /rewind'dir — hatalı turu tamamen geriye sarar, yanlış çıktı context'te kalıp sonraki yanıtları çarpıtmaz",
                    "Büyük bir dosyayı doğrudan mesaja yapıştırmak: Path referansı ver, Claude'un kendi okumasına izin ver — hem daha kontrollü olur hem 30MB istek boyutu limitine takılmazsın",
                ]),
            ],
        },
    ],

    # ------------------------------------------------------------------ prompts
    "prompts": [
        {
            "title": "Context Analizi",
            "prompt": "Context doluluk durumumu analiz et. /context çalıştır ve hangi kategorinin en çok yer kapladığını söyle. Optimizasyon önerileri ver.",
            "note": "Oturuma her başladığında ve büyük bir görev öncesi çalıştırmaya alışkanlık haline getir.",
        },
        {
            "title": "Odaklı Compact",
            "prompt": "/compact Todo App'in API endpoint'leri, test sonuçları ve mevcut hata durumlarına odaklan. UI ile ilgili eski konuşmaları özetle.",
            "note": "Odak cümlesi ne kadar spesifikse özet o kadar isabetli olur.",
        },
        {
            "title": "Goal ile Kontrollü Çalışma",
            "prompt": "/goal POST /todos ve GET /todos endpoint'leri için birer test var ve npm test exits 0 — or stop after 10 turns",
            "note": "Tur sınırı koymak, koşul yanlış yazıldığında sonsuz döngüye girmeyi engeller.",
        },
        {
            "title": "Subagent ile Araştırma",
            "prompt": "Todo App'teki mevcut route yapısını ve hata yönetim pattern'ini araştırmak için subagent kullan. Hangi dosyalarda hangi konvansiyonların kullanıldığını özetle.",
            "note": "Ana context'ini kirletmeden geniş bir kod tabanı taramasının nasıl yapılacağını gösterir.",
        },
        {
            "title": "Session Bölme Planı",
            "prompt": "Bu feature'ı session'lara nasıl bölebileceğimi planla. Her session'ın scope'unu, girdi bağımlılıklarını ve çıktı beklentisini belirle.",
            "note": "Uzun bir feature'ı tek session'da bitirmeye çalışmak yerine önceden bölmek, context thrashing riskini azaltır.",
        },
    ],

    # ------------------------------------------------------------------ challenge
    "challenge": {
        "title": "Context-Bilinçli API Geliştirme",
        "task": (
            "Todo App backend'inde POST /todos ve GET /todos endpoint'lerini "
            "context-bilinçli şekilde geliştir: context yönetimini pasif değil, "
            "aktif bir karar süreci olarak uygula."
        ),
        "requirements": [
            "Session'ı başlatmadan önce ve geliştirme sırasında en az 2 kez /context çalıştır",
            "Context %50'ye yaklaştığında /compact <focus> uygula (odak cümlesini kendin yaz)",
            "Compact sonrası devam et; aynı görev üzerinde çıktı kalitesinin korunduğunu doğrula",
            "/goal ile POST ve GET endpoint'lerinin testlerinin geçmesini koşul olarak belirle (tur sınırı ekle)",
            "Aşağıdaki Context Log şablonunu doldurarak süreci kaydet",
        ],
        "success": [
            "/context çıktısında en çok yer kaplayan kategoriyi doğru tespit ettin ve not aldın",
            "/compact öncesi ve sonrası aynı görevi test edip çıktı kalitesini karşılaştırdın",
            "/goal ile bir koşul belirledin; Claude en az 2 tur çalıştı ve evaluator'ın gerekçesi transcript'te göründü",
            "POST /todos ve GET /todos çalışır durumda ve her ikisinin en az bir testi var",
            "Context Log şablonu eksiksiz dolduruldu",
        ],
        "solution": {
            "intro": (
                "Session'ı plan mode ile başlat, CRUD kapsamını POST+GET ile sınırlı "
                "tut, sonra normal veya acceptEdits moduna geç."
            ),
            "prompts": [
                {"title": "1. Endpoint'leri oluştur", "prompt": "POST /todos ve GET /todos endpoint'lerini oluştur (proje route konvansiyonuna uygun)"},
                {"title": "2. Context analizi", "prompt": "/context"},
                {"title": "3. Odaklı compact", "prompt": "/compact Focus on API implementation and test results"},
                {"title": "4. Tamamlanma koşulu", "prompt": "/goal POST /todos ve GET /todos icin birer test var ve npm test exits 0 — or stop after 10 turns"},
            ],
            "notes": [
                "Compact öncesi CLAUDE.md'ye kısa bir '# Compact Instructions' bölümü eklemeyi dene — hangi bilginin (örneğin test komutları, değişen dosya listesi) her zaman korunmasını istediğini yaz.",
                "Context Log Şablonu: Başlangıç /context özeti, en çok yer kaplayan kategori, compact öncesi karar, compact focus metni, compact sonrası doğrulama, /goal koşulu, test sonucu.",
            ],
            "pitfalls": [
                "Context thrashing: aynı büyük dosyanın tekrar tekrar okunması — bunun yerine dosyayı bir kez oku, sonucu kendi notlarında tut.",
                "Belirsiz /goal koşulu: 'endpoint'ler iyi çalışsın' yerine 'npm test exits 0' gibi Claude'un transcript'te kanıtlayabileceği somut bir koşul yaz.",
                "Tur sınırı koymamak: koşul yanlış yazılırsa Claude gereksiz yere çok tur harcayabilir — 'or stop after N turns' ekle.",
            ],
        },
    },

    # ------------------------------------------------------------------ takeaways
    "takeaways": [
        "Context window Claude'un en kıt kaynağıdır; doluluk arttıkça maliyet artar ve erken talimatların etkisi zayıflayabilir",
        "İlk prompt'u yazmadan önce context'in bir kısmı zaten dolar — CLAUDE.md'yi kısa tut, uzun referansı skill'lere taşı",
        "Dosya okumaları context'in en büyük tüketicisidir — spesifik prompt'lar ve subagent delegasyonu ile kontrol et",
        "/compact <focus>, otomatik compaction'dan üstündür çünkü neyin korunacağına sen karar verirsin",
        "Compaction sonrası proje kökündeki CLAUDE.md ve auto memory yeniden yüklenir; path-scoped rule'lar eşleşen dosya tekrar okunana kadar kaybolur",
        "/goal, Claude'u ölçülebilir bir koşul etrafında çok turlu otonom çalışmaya geçirir — etkili koşul yazımı (tek ölçülebilir son durum + kanıtlama yöntemi + sınır) anahtardır",
        "/cost hızlı farkındalık, /usage detaylı analiz için; abonelik planlarında gösterilen dolar tahmini gerçek faturayla birebir örtüşmeyebilir",
        "Her görev geçişinde /clear alışkanlığı, uzun bir session'ı sonradan temizlemeye çalışmaktan çok daha verimlidir",
    ],

    # ------------------------------------------------------------------ reading
    "reading": {
        "official": [
            {"label": "Explore the context window — başlangıçtan compaction'a context'i dolduran her şeyin interaktif dökümü",
             "url": "https://code.claude.com/docs/en/context-window"},
            {"label": "How Claude Code works — auto-compact mekanizması ve context doluluğunun genel işleyişi",
             "url": "https://code.claude.com/docs/en/how-claude-code-works"},
            {"label": "Keep Claude working toward a goal — /goal komutu, koşul yazımı ve evaluator mekanizması",
             "url": "https://code.claude.com/docs/en/goal"},
            {"label": "Manage costs effectively — /cost, /usage ve token azaltma stratejileri",
             "url": "https://code.claude.com/docs/en/costs"},
        ],
        "community": [
            {"label": "Claude Code Best Practices (Anthropic Engineering) — context yönetimi, subagent delegasyonu ve session stratejileri için resmi öneriler",
             "url": "https://www.anthropic.com/engineering/claude-code-best-practices"},
        ],
        "extra": [
            {"label": "Model configuration — 1M context, effort level ve auto-compact eşiği ayarları",
             "url": "https://code.claude.com/docs/en/model-config"},
        ],
    },

    "next_preview": (
        "Gün 8'de Claude Code'u QA mühendisi gibi çalıştıracaksın: debugging "
        "workflow'ları, TDD ile test yazdırma, /code-review ve /code-review ultra "
        "ile çok-ajanlı kod incelemesi, ve security-guidance plugin'ini öğreneceksin."
    ),

    # ------------------------------------------------------------------ checklist
    "checklist": [
        "Context window'un ne içerdiğini (system prompt, CLAUDE.md, memory, skill'ler, dosya okumaları, konuşma) sayabiliyorum",
        "/context çıktısını okuyup en çok yer kaplayan kategoriyi tespit edebiliyorum",
        "/compact, /compact <focus> ve /clear arasındaki farkı biliyorum ve doğru senaryoda kullanıyorum",
        "Compaction sonrası neyin korunup neyin kaybolduğunu biliyorum (proje kökü CLAUDE.md ✓, path-scoped ✗, çağrılan skill body kısmi ✓)",
        "Model bazında context kapasitesinin değişebileceğini ve /context ile güncel durumu her zaman doğrulayabileceğimi biliyorum",
        "/goal ile bir tamamlanma koşulu belirleyip Claude'un çok turlu çalışmasını izledim",
        "/cost ile hızlı, /usage ile detaylı maliyet/kullanım takibi yaptım",
        "Subagent delegasyonu ile context tasarrufu tekniğini uyguladım veya ne zaman kullanacağımı biliyorum",
        "/btw ile context büyütmeden soru sorabileceğimi biliyorum",
        "Günün challenge'ını tamamladım (POST+GET endpoint + Context Log + compact + /goal)",
    ],
}
