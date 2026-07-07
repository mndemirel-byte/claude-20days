# -*- coding: utf-8 -*-
"""Gün 6 — Slash Commands & Skills: Tekrarlayan İşleri Otomatize Et (v2.0, Temmuz 2026)."""
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table

LESSON = {
    "day": 6,
    "total_days": 20,
    "week": 2,
    "slug": "slash-commands-skills",
    "title": "Slash Commands & Skills: Tekrarlayan İşleri Otomatize Et",
    "tagline": "Günde 10 kez yaptığın şeyi bir kez tanımla",
    "tier": None,
    "date_label": "Temmuz 2026",

    # ------------------------------------------------------------------ intro
    "intro": (
        "Bugüne kadar Claude Code'a her seferinde aynı talimatları tekrar tekrar yazdın: "
        "'testleri çalıştır', 'commit at', 'şu formatta review yap'. Bu tekrarlayan "
        "rutinleri bir kez tanımlayıp tek komutla çağırmanın yolu skill'ler. Gün sonunda "
        "Todo App için çalışan bir workflow skill pack yazmış olacaksın."
    ),

    # ------------------------------------------------------------------ flow
    "flow": [
        {"phase": "1 · Mental Model",    "dur": "35 dk", "desc": "Slash command, built-in command, bundled skill, custom skill farkı; commands→skills evrimi; ne zaman skill yazılır?"},
        {"phase": "2 · İlk Çalışan Skill", "dur": "50 dk", "desc": "commit skill, SKILL.md frontmatter, /skills, /reload-skills, $ARGUMENTS ile parametre alan skill"},
        {"phase": "3 · Derinleş",          "dur": "40 dk", "desc": "Dinamik context injection, tool izinleri, scope/paylaşım, troubleshooting ve ileri seviye teaser'lar"},
        {"phase": "4 · Challenge",         "dur": "25 dk", "desc": "Todo App Developer Workflow Skill Pack (3 zorunlu + 2 bonus skill)"},
    ],

    # ------------------------------------------------------------------ prerequisites
    "prerequisites": [
        "Gün 1–5 tamamlanmış (Claude Code kurulu, CLAUDE.md hazır, Git workflow biliniyor)",
        "Terminal ve kod editörü açık",
        "Todo App projesi çalışır durumda (Gün 4'te oluşturulan yapı)",
    ],
    "tools_needed": [
        "Terminal (Claude Code çalışır durumda)",
        "VS Code veya tercih edilen editör",
        "Git (skill'leri commitlemek için)",
    ],

    # ------------------------------------------------------------------ objectives
    "objectives": [
        "Slash command, built-in command, bundled skill ve custom skill arasındaki mimari farkı açıklayabileceksin",
        "`.claude/skills/<name>/SKILL.md` formatında çalışan bir skill yazabileceksin",
        "`/skills` ve `/reload-skills` ile skill'leri keşfedip test edebileceksin",
        "`$ARGUMENTS`, `$0` ve named arguments ile parametre alan skill yazabileceksin",
        "`` !`command` `` ile dinamik context injection kullanabileceksin",
        "`disable-model-invocation` ve `allowed-tools`/`disallowed-tools` alanlarının davranış farkını açıklayabileceksin",
        "Tekrarlayan bir developer workflow'unu Git'e commitlenebilir takım standardına çevirebileceksin",
    ],

    # ================================================================== SECTIONS
    "sections": [
        # ─────────────────────── BÖLÜM 1: TEORİK TEMEL ───────────────────────
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                h("1.1 Neden Skill? — Prompt Tekrarından Workflow Standardına"),
                p(
                    "Bir projede düzinelerce kez aynı talimatı yapıştırdığını düşün: "
                    "'testleri çalıştır, başarısız olanları analiz et, düzelt'; "
                    "'conventional commit mesajı yaz'; 'PR açıklaması oluştur'. "
                    "Her seferinde aynı metni yazmak zaman kaybıdır ve tutarsızlık riski taşır. "
                    "Skill'ler bu tekrarı ortadan kaldırır: talimatı bir kez yazarsın, "
                    "sonra `/skill-name` ile çağırırsın. Claude bu talimatı her seferinde "
                    "aynı kalitede uygular."
                ),
                p(
                    "Peki skill ile CLAUDE.md arasındaki fark ne? CLAUDE.md kalıcı proje bilgisidir: "
                    "teknoloji stack'i, naming convention, klasör yapısı — her oturumda yüklenir. "
                    "Skill ise bir workflow paketidir: belirli bir görevi baştan sona yürüten talimat seti. "
                    "CLAUDE.md'ye 'testleri her zaman pytest ile çalıştır' yaz; ama 'testleri çalıştır, "
                    "başarısız olanları analiz et, düzelt ve tekrar çalıştır' gibi çok adımlı bir "
                    "workflow'u skill olarak paketle."
                ),
                keypoint(
                    "CLAUDE.md = kalıcı proje bilgisi (her oturumda yüklenir). "
                    "Skill = workflow paketi (sadece çağrıldığında veya tetiklendiğinde yüklenir). "
                    "İkisi birbirini tamamlar, yerine geçmez."
                ),

                h("1.2 Claude Code'da Komut Tipleri"),
                p(
                    "Claude Code'da `/` ile başlayan her şey bir komuttur ama her komut aynı "
                    "mekanizmayı kullanmaz. Dört temel tip vardır:"
                ),
                table(
                    ["Tip", "Mekanizma", "Tetikleme", "Örnek"],
                    [
                        ["Built-in command", "Sabit logic (Claude Code'un kendi kodu)", "Sadece manuel `/komut`", "/clear, /compact, /config, /model"],
                        ["Bundled skill", "Claude Code ile gelen prompt tabanlı skill", "Manuel `/skill` veya Claude otomatik", "/code-review, /debug, /init"],
                        ["Custom skill", "Kullanıcının yazdığı SKILL.md", "Manuel `/skill` veya Claude otomatik", "/commit, /test-runner, /fix-issue"],
                        ["MCP prompt", "MCP server'dan gelen komut", "Manuel `/mcp__server__prompt`", "Server bağlantısına göre dinamik"],
                    ],
                ),
                warn(
                    "Komut listesi Claude Code sürümüne, plana ve ortama göre değişir. "
                    "Sabit bir liste ezberlemek yerine `/` menüsünü ve resmi Commands referansını "
                    "kaynak kabul et. Aşağıdaki tablo temsili bir seçkidir — tamamı değildir."
                ),

                h("1.3 Kategori Bazlı Komut Seçkisi"),
                p(
                    "Built-in komutları ve bundled skill'leri kategori bazında tanımak, "
                    "günlük çalışmada doğru komutu hızla bulmana yardımcı olur. "
                    "Tam listeye `/` menüsünden veya resmi docs'tan ulaşabilirsin."
                ),
                table(
                    ["Kategori", "Komutlar (seçki)", "Açıklama"],
                    [
                        ["Oturum Yönetimi", "/clear, /compact, /resume, /rewind", "Context temizleme, sıkıştırma, oturum devam ettirme, geri sarma"],
                        ["Context & Teşhis", "/context, /skills, /doctor, /usage, /cost", "Context analizi, skill listesi, teşhis, kullanım/maliyet bilgisi"],
                        ["Geliştirme Workflow", "/code-review, /debug, /init, /loop, /batch", "Kod inceleme, hata ayıklama, proje başlatma, tekrar eden görevler"],
                        ["Yapılandırma", "/config, /model, /effort, /fast, /permissions", "Ayarlar, model seçimi, effort seviyesi, hız modu, izin yönetimi"],
                    ],
                ),
                tip(
                    "Gün 6'nın merkezi komutları `/skills` (mevcut skill'leri listele) ve "
                    "`/reload-skills` (değişiklik sonrası yeniden yükle). "
                    "Bu ikisini sık kullanacaksın."
                ),

                h("1.4 Custom Commands'dan Skills'e Genişleyen Model"),
                p(
                    "Claude Code'un eski custom command sistemi `.claude/commands/` dizininde "
                    "Markdown dosyaları kullanıyordu. Bu format hâlâ destekleniyor ve çalışıyor — "
                    "`.claude/commands/deploy.md` yazdığında `/deploy` komutu oluşuyor. "
                    "Ancak skills sistemi (`.claude/skills/`) daha zengin bir model sunuyor:"
                ),
                table(
                    ["Özellik", "Commands (.claude/commands/)", "Skills (.claude/skills/)"],
                    [
                        ["Slash ile çağırma", "✅ /komut-adı", "✅ /skill-adı"],
                        ["Claude otomatik tetikleme", "❌", "✅ (description + when_to_use eşleşirse)"],
                        ["YAML frontmatter", "Opsiyonel (sadece description, argument-hint)", "Tam destek (model, effort, tools, context, agent vb.)"],
                        ["Destek dosyaları", "❌ Sadece tek .md", "✅ Klasör yapısı (template, script, example)"],
                        ["Tool izin kontrolü", "❌", "✅ allowed-tools, disallowed-tools"],
                        ["Forked context", "❌", "✅ context: fork + agent seçimi"],
                    ],
                ),
                keypoint(
                    "`.claude/commands/` hâlâ desteklenen eski command formatıdır. "
                    "`.claude/skills/` ise daha zengin metadata, destek dosyaları ve davranış kontrolü sunar. "
                    "İkisi aynı isimde varsa skill kazanır. Yeni workflow'lar için `.claude/skills/` tercih et."
                ),

                h("1.5 SKILL.md Anatomisi: Frontmatter + Markdown"),
                p(
                    "Her skill iki parçadan oluşur: YAML frontmatter (--- ile ayrılan bölüm) "
                    "ve Markdown içerik. Frontmatter Claude'a skill'in ne olduğunu, ne zaman "
                    "tetikleneceğini ve hangi kısıtlamaların geçerli olduğunu söyler. "
                    "Markdown içerik ise Claude'un çalıştıracağı talimatları içerir."
                ),
                code(
                    "# .claude/skills/commit/SKILL.md\n"
                    "---\n"
                    "name: commit\n"
                    "description: Staged değişiklikleri analiz edip conventional commit mesajı önerir\n"
                    "argument-hint: [mesaj-notu]\n"
                    "disable-model-invocation: true\n"
                    "---\n\n"
                    "## Commit Workflow\n\n"
                    "1. `git status` ve `git diff --cached` çalıştır\n"
                    "2. Değişiklikleri analiz et\n"
                    "3. Conventional commit mesajı öner: type(scope): description\n"
                    "4. Kullanıcı onaylarsa commit et\n"
                    "5. $ARGUMENTS varsa commit mesajına not olarak ekle",
                    "markdown",
                ),
                p(
                    "Tüm frontmatter alanlarını bir anda öğrenmeye çalışma. "
                    "Bugün temel alanları öğreneceksin; ileri alanlarla sonraki günlerde tanışacaksın."
                ),
                table(
                    ["Katman", "Alanlar", "Ne yapar?"],
                    [
                        [
                            "Temel (bugün)",
                            "name, description, argument-hint, arguments, disable-model-invocation, allowed-tools, disallowed-tools",
                            "Skill'in kimliği, parametreleri, tetikleme kontrolü ve tool izinleri",
                        ],
                        [
                            "İleri (sonraki günler)",
                            "context, agent (Gün 11), model, effort, paths, shell, hooks (Gün 12), user-invocable, when_to_use",
                            "Forked context, subagent, model/effort override, path filtreleme, hook bağlama",
                        ],
                    ],
                ),

                h("1.6 Ne Zaman Skill Yazılır, Ne Zaman Yazılmaz?"),
                p(
                    "Her şeyi skill yapmak da kötü pratiktir. Skill bir mühendislik kararıdır; "
                    "doğru aracı doğru yerde kullanmak gerekir."
                ),
                table(
                    ["Skill yaz ✅", "Skill yazma ❌"],
                    [
                        ["Aynı talimatı tekrar tekrar yapıştırıyorsan", "Tek seferlik bir işse → doğrudan prompt yaz"],
                        ["Workflow 3+ adımdan oluşuyorsa", "Kalıcı proje bilgisi ise → CLAUDE.md'ye ekle"],
                        ["Takımda aynı rutin paylaşılacaksa", "Deterministik bir script yeterliyse → shell script yaz"],
                        ["Destek dosyası/template gerekiyorsa", "Basit bir alias yeterliyse → shell alias tanımla"],
                        ["Claude'un otomatik tetiklemesini istiyorsan", "İş mantığı her seferinde farklıysa → prompt'u o an yaz"],
                    ],
                ),
                tip(
                    "Challenge'a başlamadan önce her skill fikrin için şu soruyu sor: "
                    "'Bu gerçekten skill olmalı mı, yoksa CLAUDE.md, script veya "
                    "tek seferlik prompt yeterli mi?'"
                ),
            ],
        },

        # ─────────────────────── BÖLÜM 2: PRATİK — ADIM ADIM ─────────────────
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                h("2.1 İlk Custom Skill: commit"),
                p(
                    "İlk skill'ini yazacaksın: değişiklikleri analiz edip conventional commit "
                    "mesajı öneren bir workflow. Bu skill otomatik tetiklenmemeli — commit kararı "
                    "bilinçli olmalı. Bu yüzden `disable-model-invocation: true` ayarlayacağız."
                ),
                steps([
                    "Skill dizinini oluştur: `mkdir -p .claude/skills/commit`",
                    (
                        "SKILL.md dosyasını yaz (editörde veya Claude'a yazdır):\n"
                        "```\n"
                        "---\n"
                        "name: commit\n"
                        "description: Staged değişiklikleri analiz edip conventional commit mesajı önerir\n"
                        "argument-hint: [mesaj-notu]\n"
                        "disable-model-invocation: true\n"
                        "---\n\n"
                        "## Commit Workflow\n\n"
                        "1. `git status` ve `git diff --cached` çalıştır\n"
                        "2. Değişiklikleri mantıksal gruplara ayır\n"
                        "3. Her grup için conventional commit mesajı öner: type(scope): description\n"
                        "4. Commit planını kullanıcıya göster ve onay bekle\n"
                        "5. Kullanıcı onaylarsa commit et, onaylamazsa revize et\n"
                        "6. $ARGUMENTS varsa commit mesajına ek not olarak ekle\n"
                        "```"
                    ),
                    "`/skills` yaz — commit skill'inin listede göründüğünü doğrula",
                    "`/commit` yaz — skill'i çalıştır ve sonucu gözlemle",
                    "Commit mesajını incele: conventional commit formatına uyuyor mu?",
                ]),
                warn(
                    "Commit skill'i otomatik commit atmamalı — önce mesaj önersin, "
                    "kullanıcı onayladıktan sonra commit yapsın. Bu 'güvenlik kapısı' "
                    "yaklaşımı state-changing işlemler için iyi pratiktir."
                ),
                tip(
                    "SKILL.md'yi değiştirdikten sonra `/reload-skills` çalıştır. "
                    "Bu komut skill'leri yeniden yükler ve değişikliklerin etkisini "
                    "hemen görmeni sağlar."
                ),

                h("2.2 Parametre Alan Skill: fix-issue"),
                p(
                    "Bazı skill'ler her çağrıda farklı girdi almalıdır. Örneğin "
                    "`/fix-issue 42` dediğinde Claude 42 numaralı issue'yu çözmeli. "
                    "Bunu `$ARGUMENTS` veya indexed parametreler (`$0`, `$1`) ile yaparsın."
                ),
                code(
                    "# .claude/skills/fix-issue/SKILL.md\n"
                    "---\n"
                    "name: fix-issue\n"
                    "description: Verilen issue numarasını okuyup çözer\n"
                    "argument-hint: [issue-number]\n"
                    "---\n\n"
                    "## Issue Çözme Workflow'u\n\n"
                    "Issue numarası: $ARGUMENTS\n\n"
                    "1. Issue açıklamasını oku ve anla\n"
                    "2. İlgili dosyaları bul ve analiz et\n"
                    "3. Çözüm planı oluştur ve kullanıcıya sun\n"
                    "4. Onay alınca implementasyonu yap\n"
                    "5. İlgili testleri çalıştır\n"
                    "6. Değişiklik özetini hazırla",
                    "markdown",
                ),
                p(
                    "`$ARGUMENTS` skill'e verilen tüm metni içerir. "
                    "Eğer birden fazla parametreye ihtiyaç varsa indexed form kullanabilirsin: "
                    "`$0` birinci, `$1` ikinci argüman olur. Ancak çoğu durumda `$ARGUMENTS` yeterlidir."
                ),
                keypoint(
                    "Skill'e argüman verirsen (`/fix-issue 123`) `$ARGUMENTS` = '123' olur. "
                    "Argüman vermezsen Claude Code `$ARGUMENTS` yerine boş bırakmaz; "
                    "skill içeriğinin sonuna `ARGUMENTS: <input>` ekler. "
                    "Skill'ini her iki durumu da karşılayacak şekilde yaz."
                ),

                h("2.3 test-runner Skill'i: Tool İzinleri"),
                p(
                    "Bazı skill'ler belirli tool'ları onay istemeden kullanmalıdır. "
                    "Örneğin test çalıştıran bir skill her seferinde 'Bash çalıştırayım mı?' "
                    "diye sormamalı. `allowed-tools` bunu sağlar."
                ),
                code(
                    "# .claude/skills/test-runner/SKILL.md\n"
                    "---\n"
                    "name: test-runner\n"
                    "description: Testleri çalıştırır, başarısız olanları analiz edip düzeltir\n"
                    "argument-hint: [test-path]\n"
                    "allowed-tools:\n"
                    "  - Bash\n"
                    "---\n\n"
                    "## Test Workflow\n\n"
                    "1. $ARGUMENTS verilmişse sadece o path'teki testleri çalıştır\n"
                    "2. $ARGUMENTS boşsa tüm testleri çalıştır\n"
                    "3. Başarısız testleri listele ve her birinin hata nedenini analiz et\n"
                    "4. Düzeltilebilecek hataları düzelt\n"
                    "5. Testleri tekrar çalıştır ve sonucu raporla",
                    "markdown",
                ),
                keypoint(
                    "allowed-tools ve disallowed-tools birbirinden farklı şeyler yapar:\n\n"
                    "• allowed-tools: Bu skill aktifken listelenen tool'ları approval istemeden "
                    "kullanma izni verir. Diğer tool'lar hâlâ kullanılabilir ama onay gerektirir.\n\n"
                    "• disallowed-tools: Bu skill aktifken listelenen tool'ları tamamen engeller. "
                    "Claude o tool'ları çağıramaz.\n\n"
                    "Kısaca: allowed-tools onay atlar, disallowed-tools tool'u kaldırır."
                ),
                warn(
                    "allowed-tools: [\"Bash\"] eğitimde basitlik için kullanılır. "
                    "Production ve takım ortamında mümkünse daha dar tool izinleri, "
                    "hook'lar (Gün 12) veya explicit approval tercih edilmelidir. "
                    "'Bash'i allow et, rahat et' güvenli bir alışkanlık değildir."
                ),

                h("2.4 Dinamik Context Injection"),
                p(
                    "Bazı skill'lerin çalışma anında güncel bilgiye ihtiyacı vardır. "
                    "Örneğin PR özeti yazan bir skill, o andaki diff'i bilmeli. "
                    "`` !`command` `` söz dizimi bunu sağlar: SKILL.md yüklenirken "
                    "komut çalıştırılır ve çıktısı prompt'a enjekte edilir."
                ),
                code(
                    "# .claude/skills/pr-summary/SKILL.md\n"
                    "---\n"
                    "name: pr-summary\n"
                    "description: Mevcut branch'in diff'ini analiz edip PR açıklaması üretir\n"
                    "---\n\n"
                    "## Mevcut Değişiklikler\n\n"
                    "!`git diff main...HEAD --stat`\n\n"
                    "## Detaylı Diff\n\n"
                    "```!\n"
                    "git diff main...HEAD\n"
                    "```\n\n"
                    "## Görev\n\n"
                    "Yukarıdaki değişiklikleri analiz et ve bir PR açıklaması yaz:\n"
                    "- Ne değişti (özet)\n"
                    "- Neden değişti (motivasyon)\n"
                    "- Nasıl test edilir\n"
                    "- Breaking change var mı",
                    "markdown",
                ),
                p(
                    "İki farklı söz dizimi var: satır içi `` !`command` `` tek satırlık komutlar için; "
                    "` ```! ` ile açılan fenced block çok satırlı komutlar için. "
                    "Her ikisi de preprocessing aşamasında çalışır — Claude sonucu değil, "
                    "komutu değil, yalnızca çıktıyı görür."
                ),
                tip(
                    "Dinamik context injection güçlüdür ama güvenlik sorumluluğu sende. "
                    "Shell çıktısı doğrudan Claude'un prompt'una girer. Hassas bilgi "
                    "döndüren komutlar kullanma. Gerekirse settings'ten "
                    "`disableSkillShellExecution: true` ile bu özelliği kapatabilirsin."
                ),

                h("2.5 Destek Dosyaları ve ${CLAUDE_SKILL_DIR}"),
                p(
                    "Skill tek bir SKILL.md olmak zorunda değil — template, example, "
                    "script gibi destek dosyaları ekleyebilirsin. Skill klasörü içindeki "
                    "dosyalara `${CLAUDE_SKILL_DIR}` ile referans verirsin."
                ),
                code(
                    "# Skill klasör yapısı:\n"
                    ".claude/skills/api-design/\n"
                    "├── SKILL.md          # Ana talimatlar\n"
                    "├── template.md       # API endpoint şablonu\n"
                    "├── examples/\n"
                    "│   ├── rest-crud.md  # Örnek CRUD endpoint\n"
                    "│   └── error-codes.md\n"
                    "└── scripts/\n"
                    "    └── validate.sh   # OpenAPI doğrulama scripti",
                    "bash",
                ),
                p(
                    "SKILL.md içinde destek dosyalarına şöyle referans verirsin:\n"
                    "`${CLAUDE_SKILL_DIR}/template.md` dosyasını oku ve bu şablona göre endpoint yaz. "
                    "Bu sayede skill self-contained bir paket olur — başka projeye taşıdığında "
                    "tüm destek dosyaları birlikte gelir."
                ),

                h("2.6 Skill Stacking (Bonus)"),
                p(
                    "v2.1.199 itibarıyla birden fazla skill'i tek komutta zincirleyebilirsin: "
                    "`/code-review /fix-issue 123` yazarsan her iki skill de yüklenir ve "
                    "trailing text ('123') her birine `$ARGUMENTS` olarak aktarılır. "
                    "En fazla 6 skill zincirlenebilir."
                ),
                tip(
                    "Skill stacking ileri bir tekniktir. Önce tek skill'in nasıl "
                    "çalıştığını net anla, sonra stacking'e geç."
                ),
            ],
        },

        # ─────────────────────── BÖLÜM 3: DERİNLEŞ / UYGULAMA ───────────────
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 Skill Scope ve Paylaşım Stratejisi"),
                p(
                    "Skill'ler iki ana scope'ta yaşar: personal ve project. "
                    "Doğru scope seçimi takım çalışmasında kritiktir."
                ),
                table(
                    ["Scope", "Konum", "Kim görür?", "Ne zaman kullan?"],
                    [
                        ["Personal", "~/.claude/skills/", "Sadece sen, tüm projelerinde", "Kişisel workflow'lar: commit tarzı, editor tercihleri"],
                        ["Project", ".claude/skills/", "Projeyi klonlayan herkes", "Takım standardları: test, review, deploy workflow'ları"],
                    ],
                ),
                p(
                    "Project skill'lerini Git'e commitleyerek takımla paylaşırsın. "
                    "Bu sayede yeni takım üyesi projeyi klonladığında tüm skill'ler hazır olur. "
                    "`.claude/skills/` dizinini `.gitignore`'a ekleme — paylaşılması amaçlanmıştır."
                ),
                keypoint(
                    "Enterprise ortamlarda skill öncelik sırası: "
                    "Enterprise (managed settings) > Personal (~/.claude/) > Project (.claude/) > Plugin. "
                    "Aynı isimde skill varsa üst scope kazanır."
                ),

                h("3.2 Rol Bazlı Skill Tasarımı"),
                p(
                    "Farklı SDLC rolleri farklı skill'lerden faydalanır. "
                    "Takım genelinde bir 'workflow skill pack' standardı oluşturmak, "
                    "herkesin aynı kalitede çalışmasını sağlar."
                ),
                table(
                    ["Rol", "Örnek Skill Fikirleri", "Odak"],
                    [
                        ["Developer", "commit, fix-issue, refactor, api-scaffold", "Kod üretim ve bakım workflow'ları"],
                        ["QA / Tester", "test-runner, edge-case-finder, regression-check", "Test kapsamı ve kalite kontrol"],
                        ["DevOps / SRE", "deploy-check, health-monitor, incident-report", "Deployment güvenliği ve izleme"],
                        ["Tech Lead", "code-review, pr-summary, architecture-check", "Kod kalitesi ve mimari tutarlılık"],
                    ],
                ),
                tip(
                    "Takımda herkes kendi skill'ini yazmasın — birkaç temel skill üzerinde "
                    "uzlaşın ve bunları project scope'ta yayınlayın. Kişisel tercihler "
                    "personal scope'ta kalsın."
                ),

                h("3.3 Skill Teşhis ve Troubleshooting"),
                p(
                    "Skill'ler beklendiği gibi çalışmadığında teşhis araçları devreye girer."
                ),
                table(
                    ["Sorun", "Komut / Çözüm"],
                    [
                        ["Skill'im listede görünmüyor", "`/reload-skills` çalıştır; dosya yolunu ve frontmatter söz dizimini kontrol et"],
                        ["Claude skill'imi otomatik tetiklemiyor", "description alanının kullanıcının doğal dildeki isteğiyle eşleştiğini doğrula"],
                        ["Çok fazla skill var, bazıları kısaltılıyor", "`/doctor` çalıştır — listing budget uyarısı varsa önceliği düşük skill'lere skillOverrides ile 'name-only' ata"],
                        ["Skill istemediğim zaman tetikleniyor", "description'ı daralt veya `disable-model-invocation: true` ekle"],
                    ],
                ),
                warn(
                    "İleri teşhis notu: Çok fazla skill varsa `/doctor` listing budget uyarısı "
                    "verebilir. Skill listeleme bütçesi context window'un yaklaşık %1'i kadardır. "
                    "`skillListingBudgetFraction` ayarı veya `skillOverrides` ile görünürlük "
                    "kontrol edilebilir. Bu konu Gün 13'te plugin/skill yönetimi bağlamında derinleşecek."
                ),

                h("3.4 İleri Seviye Teaser'lar"),
                p(
                    "Aşağıdaki özellikler bugün sadece tanıtılıyor — tam derinlikleri "
                    "ilgili günlerde işlenecek."
                ),
                table(
                    ["Özellik", "Ne yapar?", "Hangi gün?"],
                    [
                        ["`context: fork` + `agent: Explore`", "Skill'i izole subagent context'inde çalıştırır; ana konuşmayı kirletmez", "Gün 11 (Subagent'lar)"],
                        ["Plugin olarak paketleme", "Skill + agent + hook + MCP server'ı tek pakette birleştirip dağıtır", "Gün 13 (Skills & Plugins)"],
                        ["Skill stacking (v2.1.199+)", "6'ya kadar skill'i tek komutta zincirleme", "Gün 13 (ileri workflow'lar)"],
                    ],
                ),
            ],
        },
    ],

    # ================================================================== PROMPTS
    "prompts": [
        {
            "title": "Skill Keşfedici",
            "prompt": (
                "Projemde hangi slash komutlarını ve skill'leri kullanabilirim? "
                "/skills çalıştır ve sonuçları kategorize et: built-in komutlar, "
                "bundled skill'ler ve custom skill'ler ayrı ayrı listele."
            ),
            "note": "Gün 6'nın ilk adımı: mevcut durumu keşfet.",
        },
        {
            "title": "Commit Skill Oluşturucu",
            "prompt": (
                "`.claude/skills/commit/SKILL.md` oluştur: staged değişiklikleri analiz et, "
                "conventional commit mesajı öner, kullanıcı onaylarsa commit et. "
                "disable-model-invocation: true olsun. Format: type(scope): description. "
                "$ARGUMENTS varsa commit mesajına ek not olarak ekle."
            ),
            "note": "İlk custom skill. Otomatik tetiklenmez, sadece /commit ile çağrılır.",
        },
        {
            "title": "Test Runner Skill Oluşturucu",
            "prompt": (
                "`.claude/skills/test-runner/SKILL.md` oluştur: $ARGUMENTS ile spesifik "
                "test path alabilsin, varsayılan olarak tüm testleri çalıştırsın, "
                "başarısız olanları analiz edip düzeltsin. allowed-tools: [\"Bash\"] ekle."
            ),
            "note": "allowed-tools ile onaysız test çalıştırma.",
        },
        {
            "title": "Fix-Issue Skill Oluşturucu",
            "prompt": (
                "`.claude/skills/fix-issue/SKILL.md` oluştur: $ARGUMENTS ile issue numarası "
                "alsın. Workflow: issue'yu oku → plan yap → implement et → test et → özet ver."
            ),
            "note": "Parametre alan skill örneği. /fix-issue 42 şeklinde çağrılır.",
        },
        {
            "title": "PR Summary Skill (Dinamik Context)",
            "prompt": (
                "`.claude/skills/pr-summary/SKILL.md` oluştur: !`git diff main...HEAD --stat` "
                "ile değişiklikleri dinamik olarak inject etsin. PR açıklaması üretsin: "
                "ne değişti, neden değişti, nasıl test edilir, breaking change var mı."
            ),
            "note": "Dinamik context injection (!`command`) ile çalışma anında güncel bilgi.",
        },
    ],

    # ================================================================== CHALLENGE
    "challenge": {
        "title": "Todo App Developer Workflow Skill Pack",
        "task": (
            "Todo App projesi için bir 'Developer Workflow Skill Pack' oluştur. "
            "Tekrarlayan developer rutinlerini custom skill'lere dönüştür ve "
            "Git'e commitleyerek takımla paylaşılabilir hale getir."
        ),
        "requirements": [
            "3 zorunlu skill `.claude/skills/<name>/SKILL.md` formatında yazılmış olsun",
            "Zorunlu: commit — conventional commit mesajı öneren, disable-model-invocation: true, !`git diff --cached` ile dinamik context",
            "Zorunlu: test-runner — $ARGUMENTS ile spesifik test path alan, allowed-tools: [\"Bash\"]",
            "Zorunlu: fix-issue — $ARGUMENTS ile issue numarası alan, plan → implement → test → summary akışı",
            "Bonus: pr-summary — !`git diff main...HEAD` ile dinamik context injection",
            "Bonus: deploy-check — release öncesi checklist, disallowed-tools ile push/publish engelleme",
            "Tüm skill'ler Git'e commitlenmiş olsun",
        ],
        "success": [
            "3 zorunlu SKILL.md dosyası `.claude/skills/` altında mevcut",
            "`/skills` çıktısında 3 skill de görünüyor",
            "`/commit` staged değişikliklerden conventional commit mesajı öneriyor (otomatik commit atmıyor)",
            "`/test-runner src/tests/` sadece belirtilen path için test çalıştırıyor",
            "`/fix-issue 42` issue numarasını doğru alıp plan → implement → test → summary akışını başlatıyor",
            "Skill dosyaları Git'e commitlenmiş durumda",
        ],
        "solution": {
            "intro": (
                "Bu challenge'ı adım adım çözmek için aşağıdaki akışı izle. "
                "Her skill için önce dizin oluştur, SKILL.md yaz, `/reload-skills` ile yükle "
                "ve `/skill-name` ile test et. Challenge'a başlamadan önce her skill için "
                "sor: 'Bu gerçekten skill olmalı mı?' — commit, test, fix-issue rutinleri "
                "tekrarlayan, çok adımlı ve takımla paylaşılabilir: evet, skill olmalı."
            ),
            "prompts": [
                {
                    "title": "1) commit skill'ini oluştur",
                    "prompt": (
                        "mkdir -p .claude/skills/commit && Claude'a: "
                        "'.claude/skills/commit/SKILL.md oluştur. Staged değişiklikleri analiz et, "
                        "conventional commit mesajı öner, onay al, commit et. "
                        "disable-model-invocation: true. Dynamic context: !`git diff --cached`'"
                    ),
                },
                {
                    "title": "2) test-runner skill'ini oluştur",
                    "prompt": (
                        "'.claude/skills/test-runner/SKILL.md oluştur. $ARGUMENTS ile test path alsın, "
                        "varsayılan tüm testleri çalıştırsın, başarısız olanları analiz edip düzeltsin. "
                        "allowed-tools: [\"Bash\"]'"
                    ),
                },
                {
                    "title": "3) fix-issue skill'ini oluştur",
                    "prompt": (
                        "'.claude/skills/fix-issue/SKILL.md oluştur. $ARGUMENTS ile issue numarası alsın. "
                        "Workflow: issue oku → plan yap → implement et → test et → değişiklik özeti yaz.'"
                    ),
                },
                {
                    "title": "4) Skill'leri doğrula",
                    "prompt": (
                        "'/skills çalıştır — 3 skill de görünüyor mu? "
                        "Sonra /commit ile staged bir değişiklik üzerinde test et. "
                        "/test-runner src/tests/ ile spesifik path testi dene. "
                        "/fix-issue 1 ile bir örnek issue çöz.'"
                    ),
                },
                {
                    "title": "5) Git'e commitle",
                    "prompt": (
                        "'Skill dosyalarını Git'e commitle: "
                        "git add .claude/skills/ && git commit -m \"feat(skills): add developer workflow skill pack\"'"
                    ),
                },
            ],
            "notes": (
                "Temel frontmatter alanları: name (skill adı, /name ile çağrılır), "
                "description (Claude'un otomatik tetikleme kararında kullandığı metin), "
                "argument-hint (kullanıcıya gösterilen parametre ipucu), "
                "disable-model-invocation (true ise Claude otomatik tetiklemez), "
                "allowed-tools (onaysız kullanım izni — tool'u kaldırmaz), "
                "disallowed-tools (tool'u tamamen engeller — onay atlamaz, kaldırır). "
                "commit skill'inde disable-model-invocation: true önemli çünkü commit "
                "state-changing bir işlem — Claude'un 'yardımcı olmak için' otomatik commit "
                "atmasını istemezsin."
            ),
            "pitfalls": [
                "⚠️ SKILL.md'yi değiştirip /reload-skills çalıştırmayı unutma — eski versiyon yüklenmiş kalır.",
                "⚠️ allowed-tools: [\"Bash\"] çok geniş bir izindir. Production'da daha dar izinler kullan.",
                "⚠️ $ARGUMENTS boş geldiğinde skill'in ne yapacağını planla — argümansız çağrıda fallback davranışı tanımla.",
                "⚠️ Dinamik context injection (!`command`) preprocessing'dir — komut başarısız olursa hata mesajı prompt'a enjekte edilir.",
                "⚠️ disallowed-tools ile deploy-check skill'i tasarlarken hangi tool'ları engellediğini somutlaştır: örneğin Bash(git push*), Bash(npm publish*), Bash(kubectl apply*) gibi pattern'ler kullanılabilir.",
                "⚠️ Personal ve project scope skill'ler aynı isimde olursa personal kazanır — isim çakışmalarına dikkat et.",
            ],
        },
    },

    # ================================================================== TAKEAWAYS
    "takeaways": [
        "Skill, tekrar eden çok adımlı workflow'ları bir kez tanımlayıp `/skill-name` ile çağırmanın yoludur — CLAUDE.md ile karıştırma: biri kalıcı bilgi, diğeri workflow paketi.",
        "`.claude/commands/` hâlâ desteklenen eski command formatıdır; `.claude/skills/` daha zengin metadata, destek dosyaları ve davranış kontrolü sunar. Aynı isimde varsa skill kazanır.",
        "Temel frontmatter alanları (name, description, argument-hint, disable-model-invocation, allowed-tools, disallowed-tools) çoğu skill için yeterlidir; ileri alanlar (context, agent, model) sonraki günlerde.",
        "allowed-tools onay atlar ama tool'u kaldırmaz; disallowed-tools tool'u tamamen engeller — bu fark güvenlik açısından kritiktir.",
        "Dinamik context injection (`` !`command` ``) skill'e çalışma anında güncel bilgi kazandırır: git diff, test sonuçları, API yanıtları.",
        "Her şeyi skill yapma — 'Bu gerçekten skill olmalı mı?' sorusu mühendislik kararıdır. Tek seferlik iş → prompt, kalıcı bilgi → CLAUDE.md, tekrarlayan workflow → skill.",
        "Skill'leri `.claude/skills/` dizininde Git'e commitle — takımda herkes projeyi klonladığında aynı workflow standardını kullanır.",
        "Skill'in çalışmadığında: `/reload-skills` ile yeniden yükle, `/skills` ile görünürlüğü kontrol et, `/doctor` ile bütçe teşhisi yap.",
    ],

    # ================================================================== READING
    "reading": {
        "official": [
            {
                "label": "Extend Claude with skills — SKILL.md yapısı, frontmatter alanları, substitution, context fork, destek dosyaları",
                "url": "https://code.claude.com/docs/en/skills",
            },
            {
                "label": "Commands Reference — tüm built-in komutlar ve bundled skill'lerin tam referansı",
                "url": "https://code.claude.com/docs/en/commands",
            },
            {
                "label": "Interactive Mode — / menüsü, Tab autocomplete, shell mode, skill çağırma",
                "url": "https://code.claude.com/docs/en/interactive-mode",
            },
        ],
        "community": [
            {
                "label": "Claude Code Best Practices (Anthropic Engineering) — skill, CLAUDE.md ve workflow organizasyonu için resmi öneriler",
                "url": "https://www.anthropic.com/engineering/claude-code-best-practices",
            },
        ],
        "extra": [
            {
                "label": "Conventional Commits — commit skill'inde referans alınan commit mesajı formatı standardı",
                "url": "https://www.conventionalcommits.org/",
            },
        ],
    },

    # ------------------------------------------------------------------ next_preview
    "next_preview": (
        "Yarın (Gün 7) Claude Code'un context window'unu yönetmeyi öğreneceksin: "
        "200K → 1M token aralığında verimli çalışma, /compact stratejileri, "
        "/context ile kullanım analizi ve büyük projelerde context taşmasını önleme teknikleri."
    ),

    # ================================================================== CHECKLIST
    "checklist": [
        "Slash command, built-in command, bundled skill ve custom skill arasındaki farkı açıklayabiliyorum",
        "`.claude/commands/` (eski format) ile `.claude/skills/` (güncel) ilişkisini ve öncelik kuralını biliyorum",
        "`.claude/skills/<name>/SKILL.md` formatında çalışan bir skill yazabiliyorum",
        "`/skills` ile mevcut skill'leri listeleyip `/reload-skills` ile yeniden yükleyebiliyorum",
        "`$ARGUMENTS`, `$0` ve `argument-hint` ile parametre alan skill yazabiliyorum",
        "`` !`command` `` ve ``` ! ile dinamik context injection yapabiliyorum",
        "`disable-model-invocation` (otomatik tetikleme kontrolü) ile `allowed-tools` / `disallowed-tools` (tool izin/engelleme) farkını açıklayabiliyorum",
        "'Ne zaman skill yazılır, ne zaman CLAUDE.md yeter?' kararını verebiliyorum",
        "Skill'leri Git'e commitleyerek takımla paylaşabiliyorum",
        "Todo App için en az 3 custom skill yazıp çalıştığını doğruladım",
    ],
}
