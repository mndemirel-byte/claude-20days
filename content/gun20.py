# content/gun20.py
# Tek kaynak: LESSON sözlüğü. generators/render_html.py ve generators/render_json.py
# bu sözlükten HTML + JSON üretir.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table


LESSON = {
    "day": 20,
    "total_days": 20,
    "week": 4,
    "slug": "capstone-mikroservis",
    "title": "Capstone: Enterprise Mikro-Servis Projesi",
    "tagline": "Her şeyi bir araya getir — enterprise delivery workflow simülasyonu ve kişisel playbook",
    "tier": "🔴 Kademe 4",
    "date_label": "Temmuz 2026",

    "intro": (
        "Gün 19'da takım ve organizasyon ölçeğinde Claude Code altyapısını kurmuştun — "
        "managed settings, sandbox izolasyonu, maliyet gözlemlenebilirliği ve plugin "
        "marketplace. Bugün programın final günü: öğrendiğin her şeyi tek bir enterprise "
        "capstone'da birleştiriyorsun. Amaç production-grade bir sistem üretmek değil, "
        "Claude Code ile enterprise-style delivery workflow'unu uçtan uca simüle etmek: "
        "spec → architecture → parallel implementation → integration → review → artifact "
        "→ playbook. Conductor workflow ile planlama, Agent Teams (veya fallback olarak "
        "subagent'lar) ile paralel geliştirme, Artifacts ile sonucu paylaşılabilir canlı "
        "sayfaya dönüştürme — ve son adımda kendi Claude Code Playbook'unu yazarak 20 "
        "günlük yolculuğu kişisel bir referansa çevireceksin."
    ),

    "flow": [
        {"phase": "1 · Teorik: Conductor Workflow & Mimari Strateji",
         "dur": "25 dk",
         "desc": "Explore → Plan → Implement → Commit/Review döngüsü, mikro-servis "
                 "planlama, interview-driven spec, plan mode"},
        {"phase": "2 · Teorik: Artifacts & Sürekli İyileştirme",
         "dur": "20 dk",
         "desc": "Artifact oluşturma/güncelleme/paylaşma, page constraints, iteratif "
                 "prompt tuning, ileriye bakış"},
        {"phase": "3 · Pratik: Kademe 4 Proje — Paralel Geliştirme",
         "dur": "50 dk",
         "desc": "Mikro-servis tanımla, Agent Teams veya subagent fallback ile spawn, "
                 "Dynamic Workflow ile fan-out, servisleri birleştir"},
        {"phase": "4 · Pratik: Artifact + Final Review + Playbook",
         "dur": "25 dk",
         "desc": "Projeyi Artifact olarak yayınla, /code-review (lokal veya ultra), "
                 "retrospektif ve Playbook yazımı"},
    ],

    "prerequisites": [
        "Gün 1-19 tamamlanmış — özellikle Agent Teams (Gün 17), Dynamic Workflows "
        "(Gün 17), CI/CD (Gün 18), Enterprise Patterns (Gün 19)",
        "SaaS Dashboard projesi (Kademe 3) çalışır durumda",
        "Team Starter Kit (Gün 19) uygulanmış veya en az kavramsal olarak bilinir",
        "Pro/Max/Team/Enterprise plan + /login ile oturum açık (Artifacts için)",
    ],
    "tools_needed": [
        "Claude Code CLI — v2.1.178+ önerilir; Dynamic Workflows minimum v2.1.154+, "
        "--effort ultracode kullanılacaksa v2.1.203+",
        "Git + GitHub/GitLab",
        "Docker / Docker Compose",
        "Node.js (mikro-servis projesi için)",
        "gh CLI (PR işlemleri için, opsiyonel)",
    ],

    "objectives": [
        "Conductor workflow'un dört fazını (Explore → Plan → Implement → Commit/Review) "
        "büyük bir proje üzerinde uygulayabilmek",

        "Agent Teams ile en az 3 teammate spawn edip plan approval akışını yürütebilmek; "
        "Agent Teams kullanılamıyorsa aynı iş bölümünü subagent'lar ile simüle edebilmek",

        "Dynamic Workflows ile fan-out pattern kullanarak paralel denetim "
        "çalıştırabilmek ve /config üzerinden etkinleştirme adımını bilmek",

        "Minimal skeleton mikro-servis projesini (in-memory data, 2-3 endpoint/servis) "
        "Docker Compose ile çalıştırabilmek",

        "Artifacts özelliğiyle oturum çıktısını canlı, paylaşılabilir bir sayfaya "
        "dönüştürebilmek (oluşturma, güncelleme, tarayıcıda açma)",

        "20 günlük öğrenimleri kişisel bir Claude Code Playbook belgesi olarak "
        "yapılandırabilmek",
    ],

    # =========================================================================
    # SECTIONS — tam 3 bölüm
    # =========================================================================
    "sections": [
        # ─── BÖLÜM 1 ────────────────────────────────────────────────────────
        {
            "num": 1,
            "title": "TEORİK TEMEL — Conductor Workflow, Artifacts & Capstone Stratejisi",
            "blocks": [
                # ── 1.1 Conductor Workflow ─────────────────────────────────
                h("1.1 Conductor Workflow: Büyük Projelerde Strateji"),
                p(
                    "20 gün boyunca Claude Code'u sıralı, tek oturumluk görevlerde "
                    "kullandın: bir dosya yaz, bir test ekle, bir bug düzelt. Ama "
                    "gerçek dünyadaki enterprise projeler tek oturuma sığmaz — on "
                    "binlerce satır kod, birden fazla service, farklı rollerdeki "
                    "insanlar. Bu ölçekte Claude Code'u verimli kullanmak, resmi "
                    "best practice'in önerdiği döngüsel akışı bilinçli uygulamak "
                    "demektir."
                ),
                p(
                    "Resmi best practice dokümanındaki döngü dört fazdan oluşur "
                    "(orijinal adlarıyla Explore → Plan → Code → Commit) ve bu "
                    "eğitimde Conductor Workflow olarak adlandırıyoruz. Aşağıdaki "
                    "tabloda Code fazını, doğrulamayı da kapsadığı için Implement "
                    "olarak genişlettik:"
                ),
                table(
                    ["Faz", "Ne Yapılır", "Araç / Mod"],
                    [
                        [
                            "1 · Explore",
                            "Codebase'i tara, mevcut yapıyı anla, soruları netleştir. "
                            "Henüz hiçbir dosya düzenlenmez.",
                            "Plan mode (Shift+Tab veya /plan), subagent ile araştırma, "
                            "grep/glob/read",
                        ],
                        [
                            "2 · Plan",
                            "Tasarım kararlarını belgele: PRD.md, ARCHITECTURE.md veya "
                            "spec dosyaları yaz. İş bölümünü tanımla.",
                            "Plan mode, interview-driven spec, PRD/ARCHITECTURE "
                            "dosyaları",
                        ],
                        [
                            "3 · Implement",
                            "Kodu yaz, test et, verification loop'la doğrula. "
                            "Bir şey kırıldığında döngüye geri dön.",
                            "Normal mode, Agent Teams / subagent, Dynamic Workflows, "
                            "verification loop (test→build→screenshot)",
                        ],
                        [
                            "4 · Commit / Review",
                            "Değişiklikleri commit et, PR aç, adversarial review yap. "
                            "Resmi akışın son fazı Commit'tir; biz quality gate olarak "
                            "Review'u ekliyoruz.",
                            "/code-review (effort seviyeli lokal veya ultra cloud), custom "
                            "reviewer subagent, git commit/push",
                        ],
                    ],
                ),
                keypoint(
                    "Bu dört fazı ayrı tutmanın asıl nedeni context yönetimidir. "
                    "Explore fazında okunan onlarca dosya, Implement fazında context "
                    "window'u gereksiz yere doldurur. Her faz arasında /clear, "
                    "yeni session veya subagent delegasyonu context'i temiz tutar."
                ),
                tip(
                    "Bazı görevlerde fazları atlaman gerekebilir. Resmi best practice "
                    "dokümanı da keşif amaçlı (exploratory) görevlerde planlama fazının "
                    "atlanabileceğini ve Claude'un kendi yolunu bulmasına izin "
                    "verilebileceğini açıkça belirtir. Conductor workflow katı bir "
                    "kural değil, büyük projelerdeki varsayılan stratejidir."
                ),

                # ── 1.2 Mikro-Servis Stratejisi ───────────────────────────
                h("1.2 Mikro-Servis Mimarisinde Claude Code"),
                p(
                    "Bu capstone'da hedef production-grade bir mikro-servis sistemi "
                    "değil, enterprise delivery workflow'unu simüle eden çalışan bir "
                    "skeleton projedir. Neden mikro-servis? Çünkü service sınırları "
                    "Agent Teams'in doğal iş bölümüyle eşleşir: her teammate bir "
                    "service'i sahiplenir, gateway entegrasyonu lead'in koordinasyonuna "
                    "kalır."
                ),
                p(
                    "Capstone projemizin yapısı: user-service, product-service, "
                    "order-service ve bir api-gateway. Her servis 2-3 endpoint sunar, "
                    "in-memory mock data kullanır, veritabanı zorunlu değildir. "
                    "Docker Compose ile tek komutta ayağa kalkar."
                ),
                table(
                    ["Rol", "Agent / Teammate", "Sorumluluk", "Fallback (Agent Teams Yoksa)"],
                    [
                        [
                            "PM",
                            "pm-analyst",
                            "PRD.md, user story, acceptance criteria",
                            "Doğrudan Claude prompt (plan mode)",
                        ],
                        [
                            "Architect",
                            "architect",
                            "ARCHITECTURE.md, API contract, service sınırları",
                            "Subagent: architect (.claude/agents/)",
                        ],
                        [
                            "Backend Dev × 3",
                            "backend-dev-user / -product / -order",
                            "Her biri kendi service'ini implement eder",
                            "Subagent'lar veya ayrı terminal session'ları",
                        ],
                        [
                            "QA",
                            "qa-tester",
                            "Integration test, endpoint doğrulama",
                            "Subagent: qa-tester",
                        ],
                        [
                            "DevOps",
                            "devops-sre",
                            "Docker Compose, health check, CI konfigürasyonu",
                            "Subagent: devops-sre",
                        ],
                    ],
                ),
                warn(
                    "Agent Teams deneysel ve default kapalıdır. Etkinleştirmek için "
                    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 gerekir (shell env veya "
                    "settings.json). Her teammate bağımsız context window açar; "
                    "token maliyeti teammate sayısıyla doğrusal artar. 3-5 teammate "
                    "ile başla, koordinasyon overhead'i dikkatle izle. Eğer Agent "
                    "Teams kullanılamıyorsa, aynı iş bölümü subagent'lar "
                    "(.claude/agents/) veya ayrı terminal session'ları ile "
                    "simüle edilebilir. Workflow aynıdır; orkestrasyon aracı farklıdır."
                ),

                # ── 1.3 Artifacts ──────────────────────────────────────────
                h("1.3 Artifacts: Çalışmayı Görselleştir ve Paylaş"),
                p(
                    "Terminal satır satır metin üretir — ama bazı çıktılar terminal'de "
                    "okunmak için uygun değildir: mimari diyagram, annotated diff, "
                    "dashboard, karşılaştırma tablosu. Artifacts bu boşluğu kapatır."
                ),
                p(
                    "Bir artifact, Claude Code oturumundan claude.ai üzerindeki özel "
                    "bir URL'ye yayınlanan canlı, etkileşimli bir web sayfasıdır. "
                    "Sayfayı tarayıcıda açarsın; oturum devam ettikçe sayfa yerinde "
                    "güncellenir. Team ve Enterprise planlarında sayfa başlığındaki "
                    "Share kontrolüyle organizasyon içinde paylaşabilirsin."
                ),
                keypoint(
                    "Artifact bir capture of work'tür — bir uygulama değildir. "
                    "Backend yoktur, kalıcı veri saklamaz, view-time API çağrısı "
                    "yapamaz ve çoklu route sunamaz. Geçici client-side etkileşim "
                    "(ör. CSS animasyon, inline JS) olabilir; ama hosted internal "
                    "tool ihtiyacı için kendi altyapına deploy et."
                ),
                p(
                    "Artifact yaşam döngüsü üç adımdır:"
                ),
                bullets([
                    "Oluşturma: Claude'a doğrudan iste veya Claude kendisi önersin. "
                    "İlk yayınlamadan önce izin sorar (ör. 'Deploy failures by "
                    "service (deploy-failures.html) yayınlansın mı?'). Onaylarsan "
                    "URL üretilir, tarayıcın açılır.",
                    "Güncelleme: Aynı oturumda Claude artifact'ı yeniden yayınladığında "
                    "URL değişmez, içerik yerinde güncellenir (version tracking). "
                    "Farklı oturumdan güncellemek için artifact URL'sini Claude'a ver.",
                    "Paylaşma: Pro/Max planlarında artifact kişiseldir. Team/Enterprise "
                    "planlarında sayfa başlığındaki Share kontrolüyle belirli kişilere "
                    "veya tüm organizasyona erişim verebilirsin.",
                ]),
                tip(
                    "Ctrl+] terminalden en son artifact'ı yeniden açar. Otomatik "
                    "tarayıcı açılmasını istemiyorsan CLAUDE_CODE_ARTIFACT_AUTO_OPEN=0 "
                    "environment variable'ını ayarla."
                ),
                p(
                    "Artifact ne zaman kullanılmalı? Terminal metninin yanlış ortam "
                    "olduğu her durumda:"
                ),
                table(
                    ["Pattern", "Örnek", "Neden Artifact"],
                    [
                        [
                            "Walk through a change",
                            "PR diff'ini annotated olarak göster",
                            "Satır satır diff terminalden daha okunur",
                        ],
                        [
                            "Compare alternatives",
                            "3 mimari yaklaşımı yan yana karşılaştır",
                            "Tablo + diyagram inline JS ile etkileşimli olabilir",
                        ],
                        [
                            "Track work in progress",
                            "Investigation timeline: agent çalıştıkça dolar",
                            "Sayfa yerinde güncellenir, terminal scroll'una gerek yok",
                        ],
                        [
                            "Tune with controls",
                            "Parametre slider'ları ile konfigürasyon deneme",
                            "Geçici client-side etkileşim artifact içinde çalışır",
                        ],
                        [
                            "Dashboard",
                            "Service health, endpoint listesi, mimari görsel",
                            "Ekiple paylaşılabilir canlı rapor",
                        ],
                    ],
                ),
                warn(
                    "Artifact kısıtlamaları: harici ağ isteği yapamaz (CSP), tek "
                    "self-contained sayfa (çoklu route yok), .html/.htm/.md formatı, "
                    "maksimum 16 MiB. Token maliyetini düşürmek için inline CSS/JS "
                    "ve SVG/data URI tercih et."
                ),
                warn(
                    "Kullanılabilirlik koşulları — hepsi aynı anda sağlanmalı: "
                    "(1) Pro/Max/Team/Enterprise plan; Team'de varsayılan açık, "
                    "Enterprise'da bir Owner'ın claude.ai admin settings'ten "
                    "etkinleştirmesi gerekir. (2) /login ile claude.ai oturumu — "
                    "API key, gateway token veya cloud-provider credential ile "
                    "publish edilemez. (3) Yalnızca Anthropic API — Bedrock, "
                    "Vertex ve Foundry'de yok. (4) Organizasyonda CMEK, HIPAA veya "
                    "Zero Data Retention etkinse kapalı. Koşullardan biri "
                    "sağlanmıyorsa Claude publish etmek yerine lokal bir HTML "
                    "dosyası yazar — bu dosya senin doğal fallback'indir."
                ),
                tip(
                    "Claude, artifact üretirken projendeki design system'i arar: "
                    "CLAUDE.md'ye (Gün 3) renk/font/spacing token'larını yazarsan "
                    "sayfalar kurum kimliğinle tutarlı çıkar. Bu bölümün akışını "
                    "Bölüm 3.1'de kendi capstone projen üzerinde uçtan uca "
                    "uygulayacaksın."
                ),

            ],
        },

        # ─── BÖLÜM 2 ────────────────────────────────────────────────────────
        {
            "num": 2,
            "title": "PRATİK — ADIM ADIM: Kademe 4 Mikro-Servis Capstone",
            "blocks": [
                h("2.1 Explore Fazı: Proje Tanımı & Interview-Driven Spec"),
                p(
                    "İlk faz: ne inşa edeceğini Claude ile birlikte netleştir. "
                    "Henüz kod yazılmaz — sadece proje kapsamı, service sınırları "
                    "ve teknik kararlar belirlenir."
                ),
                steps([
                    "Proje dizini oluştur ve git init yap:\n"
                    "  mkdir capstone-microservices && cd capstone-microservices && git init",

                    "Claude Code'u plan mode'da başlat (Shift+Tab veya /plan). "
                    "Amacımız codebase keşfi değil (yeni proje), ama plan mode "
                    "dosya düzenlemesini engelleyerek sadece tasarım konuşmasına "
                    "odaklanmamızı sağlar.",

                    "Interview-driven spec prompt'unu çalıştır (aşağıdaki Prompt 1). "
                    "Claude sana sorular soracak: hangi servisler, hangi teknoloji, "
                    "authentication gerekli mi, vb. Cevaplarını ver.",

                    "Claude'un ürettiği PRD.md ve ARCHITECTURE.md dosyalarını incele. "
                    "Eksik veya yanlış bir şey varsa bu aşamada düzelt — kod "
                    "yazıldıktan sonra mimari değişiklik pahalıdır.",

                    "Commit: git add docs/ && git commit -m 'feat: initial spec and architecture'",
                ]),
                tip(
                    "Interview-driven spec, ne istediğini düşünmeden yazdırmak "
                    "yerine kritik kararları kod yazılmadan önce yüzeye çıkarır. "
                    "Ucuz olan aşamada (yazı) pahalı olacak hatayı (kod, sonradan "
                    "değişim) önler. Bu pattern'i Gün 4'te öğrenmiştin."
                ),

                h("2.2 Plan Fazı: Agent Kadrosu & İş Bölümü"),
                p(
                    "Spec hazır. Şimdi iş bölümünü tanımla: hangi agent/teammate "
                    "hangi service'i sahiplenecek, model/effort seçimi ne olacak, "
                    "worktree veya dizin stratejisi nasıl kurulacak."
                ),
                steps([
                    ".claude/agents/ dizini oluştur ve her rol için agent "
                    "tanımla. Minimum 3 agent: backend-dev, qa-tester, devops-sre "
                    "(istersen architect'i de ekle — 1.2'deki rol tablosunun tam "
                    "karşılığı olur). Gün 15'teki rol agent tasarımı pattern'ini kullan.",

                    "Her service için ayrı dizin yapısı kur:\n"
                    "  mkdir -p services/{user-service,product-service,order-service,api-gateway}",

                    "Agent Teams kullanacaksan: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 "
                    "ayarını settings.json veya shell environment'a ekle.",

                    "Agent Teams yoksa fallback stratejini belirle: subagent'lar "
                    "(.claude/agents/) veya ayrı terminal session'ları ile simülasyon.",

                    "İş planını belgele — hangi agent hangi service'i alacak, "
                    "endpoint listesi, tahmini tamamlanma sırası. Bunu CLAUDE.md "
                    "veya docs/PLAN.md'ye yaz.",
                ]),
                code(
                    "# Örnek agent tanımı: .claude/agents/backend-dev.md\n"
                    "---\n"
                    "name: backend-dev\n"
                    "description: >-\n"
                    "  Express.js mikro-servis geliştiricisi.\n"
                    "  Verilen service dizininde endpoint'leri implement eder,\n"
                    "  health check ekler, birim testleri yazar.\n"
                    "tools: Read, Write, Edit, Bash\n"
                    "model: sonnet\n"
                    "---\n"
                    "Sen bir backend developer'sın. Verilen service dizininde:\n"
                    "1. Express.js app scaffold'u oluştur (index.js + routes/)\n"
                    "2. In-memory data store ile endpoint'leri implement et\n"
                    "3. Health check endpoint'i ekle (GET /health)\n"
                    "4. Her endpoint için en az 1 birim test yaz\n"
                    "5. Dockerfile oluştur\n\n"
                    "Dış bağımlılık minimumda tut: express, cors, uuid yeterli.",
                    "markdown",
                ),

                h("2.3 Implement Fazı: Paralel Geliştirme"),
                p(
                    "Plan hazır, agent'lar tanımlı. Şimdi uygulama fazına geç: "
                    "plan mode'dan çık (Shift+Tab) ve paralel geliştirmeyi başlat."
                ),

                h("Yol A: Agent Teams ile"),
                steps([
                    "Lead session'da teammate'leri spawn et. Her teammate bir "
                    "service'i sahiplenir. Plan approval ile başla — teammate "
                    "önce ne yapacağını planlasın, sen onayla:\n"
                    "  'Spawn a backend-dev teammate for user-service. Require "
                    "plan approval before changes. Work in services/user-service/.'",

                    "Aynı pattern ile product-service ve order-service "
                    "teammate'lerini spawn et (toplam en az 3 teammate).",

                    "Ctrl+T ile task list'i izle. Teammate plan gönderdiğinde "
                    "incele ve onayla veya feedback vererek reddet.",

                    "Teammate'ler implement ederken lead olarak api-gateway'i "
                    "kur: service'lere proxy, /health endpoint, CORS ayarı.",

                    "Tüm teammate'ler tamamlandığında entegrasyon testini başlat.",
                ]),

                h("Yol B: Subagent Fallback ile"),
                steps([
                    "Aynı iş bölümünü subagent'larla simüle et. Her subagent "
                    "kendi context'inde çalışır ve sadece sonuç döndürür:\n"
                    "  'Use the backend-dev subagent to implement user-service "
                    "in services/user-service/ with GET /users, GET /users/:id, "
                    "POST /users endpoints. Return a summary of created files.'",

                    "Subagent'ları sırayla veya Dynamic Workflow ile paralel çalıştır.",

                    "Her subagent tamamlandığında dönen summary'yi incele; "
                    "gerekirse düzeltme prompt'u gönder.",

                    "api-gateway'i ana session'da implement et.",
                ]),
                p(
                    "Gateway, pratikte en çok takılınan parça. Minimal bir Express "
                    "proxy için http-proxy-middleware yeterli — Claude'a hedef "
                    "iskeleti şu şekilde gösterebilirsin:"
                ),
                code(
                    "// services/api-gateway/index.js — minimal iskelet\n"
                    "const express = require('express');\n"
                    "const { createProxyMiddleware } = require('http-proxy-middleware');\n"
                    "const app = express();\n\n"
                    "// Docker Compose network'ünde host adı = service adı\n"
                    "app.use('/api/users',    createProxyMiddleware({ target: 'http://user-service:3001',    changeOrigin: true, pathRewrite: {'^/api/users': '/users'} }));\n"
                    "app.use('/api/products', createProxyMiddleware({ target: 'http://product-service:3002', changeOrigin: true, pathRewrite: {'^/api/products': '/products'} }));\n"
                    "app.use('/api/orders',   createProxyMiddleware({ target: 'http://order-service:3003',   changeOrigin: true, pathRewrite: {'^/api/orders': '/orders'} }));\n\n"
                    "app.get('/health', (_, res) => res.json({ status: 'ok' }));\n"
                    "app.listen(3000);",
                    "javascript",
                ),

                h("Dynamic Workflow ile Fan-Out Denetim"),
                p(
                    "Implement fazı tamamlandıktan sonra Dynamic Workflow ile "
                    "tüm servisleri paralel denetle. Bu, bir workflow script'inin "
                    "her service dizinini ayrı bir agent'a vererek denetlemesidir."
                ),
                code(
                    "# Doğal dil ile workflow tetikle:\n"
                    "use a workflow to audit every service under services/ for\n"
                    "missing health checks, missing error handling, and missing\n"
                    "Dockerfiles, and adversarially verify each finding before\n"
                    "reporting it",
                    "text",
                ),
                warn(
                    "Dynamic Workflows v2.1.154+ gerektirir; Max/Team/Enterprise "
                    "planlarında varsayılan açıktır, Pro planda /config üzerinden "
                    "etkinleştirilmelidir. /effort ultracode (v2.1.203+) bir effort "
                    "setting'dir — workflow'un kendisi değildir: modele xhigh effort "
                    "gönderir ve substantive görevlerde otomatik workflow "
                    "orkestrasyonunu açar. Yalnızca xhigh destekleyen modellerde "
                    "/effort menüsünde görünür; desteklemeyen modelde seçenek hiç "
                    "listelenmez."
                ),
                tip(
                    "Session'ın effort seviyesini değiştirmeden tek bir görevi "
                    "workflow olarak çalıştırmak için prompt'a ultracode keyword'ünü "
                    "ekle (v2.1.160 öncesinde keyword 'workflow' idi) — ya da "
                    "yukarıdaki örnekteki gibi doğal dille 'use a workflow' demen "
                    "de aynı opt-in sayılır."
                ),

                h("2.4 Birleştirme & Docker Compose"),
                p(
                    "Hedef iskelet — pitfall listesindeki 'service adı' hatasını "
                    "baştan önlemek için service adlarının gateway'deki proxy "
                    "target host adlarıyla birebir aynı olduğuna dikkat et:"
                ),
                code(
                    "# docker-compose.yml — iskelet\n"
                    "services:\n"
                    "  api-gateway:\n"
                    "    build: ./services/api-gateway\n"
                    "    ports: [\"3000:3000\"]\n"
                    "    depends_on: [user-service, product-service, order-service]\n"
                    "  user-service:\n"
                    "    build: ./services/user-service\n"
                    "    ports: [\"3001:3001\"]\n"
                    "  product-service:\n"
                    "    build: ./services/product-service\n"
                    "    ports: [\"3002:3002\"]\n"
                    "  order-service:\n"
                    "    build: ./services/order-service\n"
                    "    ports: [\"3003:3003\"]",
                    "yaml",
                ),
                steps([
                    "Proje kökünde docker-compose.yml oluştur. Her service "
                    "kendi Dockerfile'ını kullanır, api-gateway diğerlerine "
                    "depends_on ile bağlanır.",

                    "docker compose up --build ile tüm servisleri ayağa kaldır.",

                    "Gateway üzerinden her service için en az 1 endpoint'i test "
                    "et:\n"
                    "  curl http://localhost:3000/api/users\n"
                    "  curl http://localhost:3000/api/products\n"
                    "  curl http://localhost:3000/api/orders",

                    "Hata varsa verification loop: Claude'a hatayı göster, "
                    "düzeltsin, tekrar docker compose up.",

                    "Tüm endpoint'ler çalıştığında commit:\n"
                    "  git add . && git commit -m 'feat: all services running "
                    "with docker compose'",
                ]),
                tip(
                    "In-memory data ile çalışan skeleton servislerin implement "
                    "kısmı genellikle 10-15 dakikada tamamlanır; spec, agent "
                    "kadrosu ve entegrasyonla birlikte fazın tamamı 50 dakikayı "
                    "bulur. Süre yetmezse önceliği daralt: önce 1 servis + gateway "
                    "uçtan uca çalışsın, kalan servisleri challenge aşamasına "
                    "bırak. Production veritabanı, authentication veya message "
                    "queue eklemek zaten kapsam dışıdır — hedef workflow "
                    "simülasyonu, tam uygulama değil."
                ),
            ],
        },

        # ─── BÖLÜM 3 ────────────────────────────────────────────────────────
        {
            "num": 3,
            "title": "PRATİK — DERİNLEŞ: Artifact, Final Review & Playbook",
            "blocks": [
                h("3.1 Projeyi Artifact Olarak Yayınla"),
                p(
                    "Çalışan mikro-servis sisteminiz var. Şimdi bu çalışmayı "
                    "terminal'den çıkar ve paylaşılabilir bir formata dönüştür. "
                    "Artifact, projenin kendisi değil; projenin dashboard'u, "
                    "mimari raporu veya durum özeti olacak."
                ),
                steps([
                    "Claude'a artifact oluşturma prompt'unu ver (aşağıdaki "
                    "Prompt 3). Claude bir HTML dosyası yazacak ve yayınlamak "
                    "için izin isteyecek.",

                    "İzni onayla. Claude URL üretecek ve tarayıcını açacak. "
                    "Sayfayı incele: service listesi, endpoint tablosu, "
                    "mimari diyagram görünüyor mu?",

                    "Eksik bir şey varsa Claude'dan güncelleme iste. "
                    "Aynı URL'de yeni versiyon yayınlanacak.",

                    "Artifact'ı Ctrl+] ile terminalden yeniden aç. "
                    "Team/Enterprise plandaysan Share kontrolünü test et.",
                ]),
                code(
                    "# Artifact oluşturma prompt örneği:\n"
                    "Make an artifact that shows our microservices project\n"
                    "dashboard: list all services with their endpoints,\n"
                    "show a simple architecture diagram (gateway → services),\n"
                    "and include the Docker Compose status summary.\n"
                    "Use a clean, professional layout.",
                    "text",
                ),
                tip(
                    "Artifact'ın güçlü olduğu an, terminal'de scroll edip "
                    "kaybettiğin bilgiyi görsel olarak organize ettiğin andır. "
                    "Özellikle ekiple paylaşıyorsan, 'şu URL'yi aç' demek "
                    "'terminal log'umu oku' demekten çok daha etkili. Bonus "
                    "pattern: sayfaya bir 'Copy as prompt' butonu ekletirsen, "
                    "artifact üzerinde verdiğin kararlar (ör. sürüklenebilir bir "
                    "önceliklendirme board'u) metin olarak session'a geri akar — "
                    "artifact tek yönlü bir çıktı olmak zorunda değildir."
                ),
                warn(
                    "Artifact publish edilemiyorsa (API key auth, Bedrock/Vertex, "
                    "kurumsal kısıt — bkz. 1.3 kullanılabilirlik koşulları) ders "
                    "durmaz: Claude aynı dashboard'u lokal bir HTML dosyası olarak "
                    "yazar. Dosyayı tarayıcıda açıp aynı incelemeyi yap; checklist "
                    "ve challenge için bu geçerli bir fallback'tir. Kurumsal not: "
                    "publish edilen artifact'lar org audit log'unda "
                    "(claude_artifact_* event'leri) izlenir ve Compliance API ile "
                    "yönetilebilir — Gün 19'daki governance katmanının parçasıdır."
                ),

                h("3.2 Final Code Review"),
                p(
                    "Capstone'da adversarial review, ürettiğin kodun son "
                    "kalite kapısıdır. Amaç: spec'e uygunluk, güvenlik "
                    "açıkları, eksik error handling ve mimari tutarsızlıklar."
                ),
                steps([
                    "Önce lokal /code-review ile hızlı bir geçiş yap. Derin bir "
                    "cloud denetimi istiyorsan /code-review ultra (eski adıyla "
                    "/ultrareview) komutunu dene — her bulgu bağımsız doğrulanır.",

                    "Cloud review kullanılamıyorsa fallback: /code-review high "
                    "veya custom reviewer subagent'ı çağır:\n"
                    "  'Use the security-reviewer subagent to audit all "
                    "services for common vulnerabilities: injection, "
                    "missing input validation, hardcoded secrets.'",

                    "Review findings'i incele. Kritik olanları düzelt, "
                    "tekrar review et. Clean bill alana kadar iterate et.",

                    "Final commit:\n"
                    "  git add . && git commit -m 'fix: address review findings'",
                ]),
                warn(
                    "/code-review ultra research preview'dur (v2.1.86+) ve cloud'da "
                    "çalışır. Plan'a değil faturalandırmaya bağlıdır: extra usage "
                    "olarak plan kullanımının DIŞINDA ücretlendirilir — çalıştırmadan "
                    "önce onay ekranındaki maliyet tahminini oku. /login ile claude.ai "
                    "oturumu gerektirir (yalnızca API key ile çalışmaz); Bedrock, "
                    "Vertex, Foundry ve Zero Data Retention org'larında kullanılamaz. "
                    "Review komutları zaman içinde değişebilir; önemli olan "
                    "adversarial review prensibini uygulamak, belirli bir komut "
                    "adına bağlanmak değil."
                ),

                h("3.3 Retrospektif & Claude Code Playbook"),
                p(
                    "Capstone tamamlandı. Son adım: 20 günlük öğrenimleri "
                    "yapılandırılmış, kişisel bir referans belgesine dönüştür. "
                    "Bu belge senin Claude Code Playbook'un — gelecekte her "
                    "yeni projeye başlarken açacağın ilk dosya."
                ),
                p(
                    "Playbook'un önerilen yapısı:"
                ),
                table(
                    ["Bölüm", "İçerik", "Kaynak Gün(ler)"],
                    [
                        [
                            "1. Context Yönetimi",
                            "CLAUDE.md stratejisi, /clear kullanımı, subagent ile "
                            "context izolasyonu, compaction davranışı",
                            "Gün 3, 7, 11",
                        ],
                        [
                            "2. Prompt Stratejileri",
                            "Interview-driven spec, plan mode, verification loop, "
                            "effort level seçimi, ultrathink kullanımı",
                            "Gün 2, 4, 7, 8",
                        ],
                        [
                            "3. Extension Kılavuzu",
                            "Skill vs Subagent vs Agent Teams vs Dynamic Workflow: "
                            "hangi görevi hangi katmana ver",
                            "Gün 6, 11, 13, 16, 17",
                        ],
                        [
                            "4. Maliyet & Model Optimizasyonu",
                            "Model seçim matrisi, effort/maliyet dengesi, /usage "
                            "okuma, spend limits",
                            "Gün 1, 19",
                        ],
                        [
                            "5. Takım Onboarding",
                            "Starter kit, managed settings, rollout checklist, "
                            "ONBOARDING.md şablonu",
                            "Gün 15, 19",
                        ],
                        [
                            "6. Anti-Pattern'ler",
                            "Büyük CLAUDE.md, context şişirme, sandbox'suz bypass, "
                            "tek model herkes için, review'sız commit",
                            "Gün 3, 7, 12, 19",
                        ],
                        [
                            "7. Kişisel Notlar",
                            "Benim iş akışımda en çok işe yarayan pattern'ler, "
                            "karşılaştığım tuzaklar, proje bazında öğrenimler",
                            "Tüm günler",
                        ],
                    ],
                ),
                steps([
                    "Claude'a Playbook yazma prompt'unu ver (aşağıdaki Prompt 5). "
                    "Claude sana sorular sorabilir — 20 günlük deneyiminden örnekler iste.",

                    "Playbook'u docs/PLAYBOOK.md olarak kaydet.",

                    "İstersen Playbook'u da bir Artifact olarak yayınla — "
                    "böylece ekiple paylaşılabilir.",

                    "Final commit:\n"
                    "  git add docs/PLAYBOOK.md && git commit -m "
                    "'docs: personal Claude Code Playbook'",
                ]),
                keypoint(
                    "Playbook canlı bir doküman olmalı. Her yeni projede, "
                    "her yeni Claude Code özelliğinde güncellenmelidir. "
                    "20 günlük eğitimin en kalıcı çıktısı bu belgedir — "
                    "araçlar değişir, senin deneyimin ve prensiplerin kalır."
                ),

                # ── 3.4 Kapanış ───────────────────────────────────────────
                h("3.4 Kapanış: Sürekli İyileştirme & İleriye Bakış"),
                p(
                    "Capstone tek seferlik bir proje değil, iteratif bir döngünün "
                    "başlangıcıdır. Her projede agent prompt'larını, skill'lerini, "
                    "plugin'lerini ve hook'larını rafine edersin. Auto memory etkinse, "
                    "proje bazında öğrenimler otomatik kaydedilir ve sonraki "
                    "oturumları zenginleştirir. İşe yarayan bir workflow çıktıysa "
                    "/workflows panelinden komut olarak kaydedip sonraki projelerde "
                    "yeniden kullanabilirsin."
                ),
                p(
                    "Claude Code ekosistemi hızla genişliyor: yeni modeller (Fable 5 "
                    "gibi), yeni yüzeyler (Desktop, Web, Chrome, Slack), daha derin "
                    "IDE entegrasyonu. Bu eğitimde öğrendiğin araçların adları veya "
                    "arayüzleri değişebilir; ama temel prensipler kalıcıdır."
                ),
                keypoint(
                    "Kalıcı prensipler: (1) Context yönetimi — doğru bilgiyi doğru "
                    "zamanda context'e sok, gerisini temizle. (2) Verification loop "
                    "— her değişikliği test/build/screenshot ile doğrula. (3) İş "
                    "bölümü — büyük görevi küçük, izole parçalara ayır (subagent, "
                    "agent teams, workflow). (4) İteratif iyileştirme — prompt'ları, "
                    "agent'ları ve konfigürasyonu her projede rafine et."
                ),
            ],
        },
    ],

    # =========================================================================
    # PROMPTS
    # =========================================================================
    "prompts": [
        {
            "title": "Interview-Driven Mikro-Servis Spec",
            "prompt": (
                "Bir e-ticaret mikro-servis sistemi tasarlayacağız: user-service, "
                "product-service, order-service ve api-gateway. Bunlar skeleton "
                "servisler olacak — in-memory data, her biri 2-3 endpoint, Docker "
                "Compose ile tek komutta ayağa kalkar. AskUserQuestion tool'unu "
                "kullanarak beni mülakat et. Teknik implementasyon, service "
                "sınırları, API contract'lar ve edge case'ler hakkında sor. "
                "Bariz soruları sorma; düşünmediğim zor kısımlara odaklan. "
                "Her şeyi kapsayana kadar mülakata devam et, sonra tam bir "
                "PRD'yi docs/PRD.md ve mimari kararları docs/ARCHITECTURE.md "
                "olarak yaz."
            ),
        },
        {
            "title": "Agent Teams ile Paralel Geliştirme",
            "prompt": (
                "Mikro-servis capstone projemizde 3 backend-dev teammate spawn et. "
                "Her teammate kendi service'ini sahiplensin:\n"
                "- user-service teammate → services/user-service/\n"
                "- product-service teammate → services/product-service/\n"
                "- order-service teammate → services/order-service/\n\n"
                "Her teammate'den plan approval iste. Plan onaylandıktan sonra "
                "implement etsin. Tamamlanan servislerin health check endpoint'ini "
                "doğrula. Ben lead olarak api-gateway'i kuracağım."
            ),
            "note": (
                "Agent Teams kullanılamıyorsa aynı prompt'u subagent'lar ile "
                "simüle et: her subagent bir service dizininde çalışır ve "
                "sonuç summary'si döndürür."
            ),
        },
        {
            "title": "Artifact: Proje Dashboard'u",
            "prompt": (
                "Make an artifact that shows our microservices capstone project "
                "as an interactive dashboard:\n"
                "- Architecture diagram: api-gateway → user-service, "
                "product-service, order-service\n"
                "- Each service: name, port, endpoints list, health status\n"
                "- Docker Compose command to start everything\n"
                "- Clean, professional layout with a project title\n\n"
                "Use HTML with inline CSS and SVG for the diagram."
            ),
        },
        {
            "title": "Adversarial Review",
            "prompt": (
                "Bu mikro-servis projesinin tüm kodunu adversarial review yap. "
                "Ayrı bir review context'i kullan — daha önce yazdığın kodu "
                "fresh eyes ile denetle. Şunlara bak:\n"
                "1. ARCHITECTURE.md'deki spec ile implementasyon uyumu\n"
                "2. Eksik error handling (input validation, 404/500 yanıtları)\n"
                "3. Hardcoded secret veya güvenlik açığı\n"
                "4. Docker Compose konfigürasyonunda eksik/yanlış ayar\n"
                "5. Endpoint'ler arası tutarsızlık (response format, status code)\n\n"
                "Her finding'i severity (critical/warning/nit) ile raporla."
            ),
        },
        {
            "title": "Claude Code Playbook",
            "prompt": (
                "20 günlük Claude Code eğitiminin sonunda kişisel bir Playbook "
                "yazıyorum. Bana sorular sorarak Playbook'u oluştur:\n"
                "- Hangi context yönetimi pattern'leri en çok işe yaradı?\n"
                "- Hangi prompt stratejilerini sık kullanıyorum?\n"
                "- Extension seçiminde (skill/subagent/agent teams/workflow) "
                "karar kriterlerim ne?\n"
                "- Maliyet optimizasyonunda nelere dikkat ediyorum?\n"
                "- Takım onboarding için ne tür bir kit hazırladım?\n"
                "- Hangi anti-pattern'lerden kaçınmalıyım?\n\n"
                "Cevaplarımı 7 bölümlü bir Playbook'a dönüştür ve "
                "docs/PLAYBOOK.md olarak kaydet."
            ),
        },
    ],

    # =========================================================================
    # CHALLENGE
    # =========================================================================
    "challenge": {
        "title": "Enterprise Delivery Workflow Simülasyonu",
        "task": (
            "Claude Code ile enterprise-style delivery workflow'unu uçtan uca simüle "
            "et: minimal skeleton mikro-servis sistemi (3 service + API gateway, "
            "in-memory data, 2-3 endpoint/servis) tasarla → Agent Teams veya "
            "subagent'larla paralel geliştir → Docker Compose ile ayağa kaldır → "
            "Artifact olarak yayınla → Claude Code Playbook yaz."
        ),
        "requirements": [
            "En az 3 skeleton mikro-servis (user, product, order) + 1 api-gateway",
            "Agent Teams ile en az 3 teammate VEYA subagent fallback ile simülasyon",
            "Docker Compose ile tüm servisler tek komutta ayağa kalkıyor",
            "En az 1 Artifact oluşturulmuş ve claude.ai üzerinde açılmış (veya fallback: lokal HTML dashboard)",
            "Adversarial review yapılmış (/code-review lokal/ultra veya reviewer subagent fallback)",
            "Claude Code Playbook en az 5 bölüm içeriyor (önerilen tam yapı: 3.3'teki 7 bölümlü tablo)",
        ],
        "success": [
            "docker compose up ile gateway + 3 servis ayağa kalkıyor",
            "Gateway üzerinden her servis için en az 1 endpoint yanıt dönüyor "
            "(ör. GET /api/users, GET /api/products, GET /api/orders)",
            "Artifact URL'si claude.ai'de açılıyor ve proje dashboard'unu gösteriyor (fallback: lokal HTML dashboard tarayıcıda açılıyor)",
            "Playbook docs/PLAYBOOK.md olarak kaydedilmiş ve en az 5 bölüm içeriyor",
            "Review findings uygulanmış, final commit yapılmış",
        ],
        "bonus": [
            "Playbook'u da Artifact olarak yayınla ve ekiple paylaş",
            "Dynamic Workflow ile tüm servisleri paralel denetle (fan-out audit)",
            "CI pipeline (GitHub Actions) ekle — push'ta testler otomatik çalışsın",
        ],
        "solution": {
            "intro": (
                "Bu capstone'un amacı production-grade bir e-ticaret sistemi kurmak "
                "değil, Claude Code ile enterprise delivery workflow'unu simüle "
                "etmektir. Aşağıdaki adımlar minimal skeleton servisler üzerinde "
                "conductor workflow'u uygular."
            ),
            "prompts": [
                {
                    "title": "Adım 1 — Explore & Spec",
                    "prompt": (
                        "Bir e-ticaret mikro-servis sistemi tasarlayacağız: "
                        "user-service, product-service, order-service, api-gateway. "
                        "Skeleton servisler: in-memory data, Express.js, her biri 2-3 "
                        "endpoint. AskUserQuestion ile beni mülakat et, sonra "
                        "docs/PRD.md ve docs/ARCHITECTURE.md üret."
                    ),
                },
                {
                    "title": "Adım 2 — Agent Kadrosu & İş Bölümü",
                    "prompt": (
                        ".claude/agents/ altında şu agent'ları oluştur:\n"
                        "- backend-dev.md: Express.js developer, verilen service "
                        "dizininde implement eder\n"
                        "- qa-tester.md: endpoint'leri test eder, edge case kontrol "
                        "eder\n"
                        "- devops-sre.md: Dockerfile ve docker-compose.yml oluşturur\n\n"
                        "Dizin yapısını kur: services/{user-service,product-service,"
                        "order-service,api-gateway}"
                    ),
                },
                {
                    "title": "Adım 3 — Paralel Implement",
                    "prompt": (
                        "Agent Teams varsa: 3 backend-dev teammate spawn et, her biri "
                        "kendi service'ini sahiplensin, plan approval ile başlasın.\n\n"
                        "Agent Teams yoksa: backend-dev subagent'ı sırayla çağır:\n"
                        "1. user-service → GET /users, GET /users/:id, POST /users\n"
                        "2. product-service → GET /products, GET /products/:id\n"
                        "3. order-service → GET /orders, POST /orders\n\n"
                        "Sonra api-gateway'i implement et: her service'e proxy, "
                        "GET /health, CORS."
                    ),
                },
                {
                    "title": "Adım 4 — Docker Compose & Doğrulama",
                    "prompt": (
                        "docker-compose.yml oluştur: gateway port 3000, "
                        "user-service 3001, product-service 3002, order-service 3003. "
                        "docker compose up --build çalıştır, gateway üzerinden:\n"
                        "  curl localhost:3000/api/users\n"
                        "  curl localhost:3000/api/products\n"
                        "  curl localhost:3000/api/orders\n"
                        "Hata varsa düzelt, tekrar test et."
                    ),
                },
                {
                    "title": "Adım 5 — Artifact & Review & Playbook",
                    "prompt": (
                        "1. Proje dashboard'unu Artifact olarak yayınla (mimari "
                        "diyagram + endpoint tablosu + Docker Compose komutu).\n"
                        "2. /code-review (lokal; derin denetim istersen ultra) veya "
                        "reviewer subagent ile adversarial review yap.\n"
                        "3. Findings'i düzelt.\n"
                        "4. 20 günlük öğrenimlerimi 7 bölümlü Playbook'a dönüştür "
                        "ve docs/PLAYBOOK.md olarak kaydet."
                    ),
                },
            ],
            "notes": [
                "Skeleton servisler in-memory data kullanır — database setup gerektirmez",
                "Beklenen dosya yapısı:\n"
                "capstone-microservices/\n"
                "├── CLAUDE.md\n"
                "├── docker-compose.yml\n"
                "├── docs/\n"
                "│   ├── PRD.md\n"
                "│   ├── ARCHITECTURE.md\n"
                "│   └── PLAYBOOK.md\n"
                "├── .claude/\n"
                "│   └── agents/\n"
                "│       ├── backend-dev.md\n"
                "│       ├── qa-tester.md\n"
                "│       └── devops-sre.md\n"
                "└── services/\n"
                "    ├── api-gateway/\n"
                "    │   ├── index.js\n"
                "    │   └── Dockerfile\n"
                "    ├── user-service/\n"
                "    │   ├── index.js\n"
                "    │   ├── routes/\n"
                "    │   └── Dockerfile\n"
                "    ├── product-service/\n"
                "    │   ├── index.js\n"
                "    │   ├── routes/\n"
                "    │   └── Dockerfile\n"
                "    └── order-service/\n"
                "        ├── index.js\n"
                "        ├── routes/\n"
                "        └── Dockerfile",
                "Her servisin endpoint listesi:\n"
                "  user-service:    GET /users, GET /users/:id, POST /users\n"
                "  product-service: GET /products, GET /products/:id\n"
                "  order-service:   GET /orders, POST /orders\n"
                "  api-gateway:     GET /health + /api/* proxy — yukarıdaki tüm "
                "servis endpoint'lerini /api prefix'i ile geçirir "
                "(ör. GET /api/users/:id → user-service GET /users/:id)",
                "Agent Teams experimental flag: CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1",
                "Docker Compose port mapping: gateway 3000, user 3001, "
                "product 3002, order 3003",
            ],
            "pitfalls": [
                "Conductor workflow fazlarını karıştırmak: Explore fazında kod yazmaya "
                "başlamak context'i kirletir — plan mode'da kal",
                "Agent Teams'i kapatmadan session'dan çıkmak — teammate'ler "
                "orphaned tmux session olarak kalabilir. Her zaman shutdown isteği gönder",
                "Artifact'ı 'uygulama' olarak tasarlamak: backend, persistent state "
                "veya API çağrısı olmaz. Dashboard/rapor olarak düşün",
                "Playbook'u jenerik yazmak: 'context yönetimi önemlidir' yerine "
                "'X projede Y pattern işe yaradı çünkü Z' gibi somut örnekler yaz",
                "Docker Compose'da service isimlerini yanlış yazmak: depends_on "
                "ve network referanslarında service name ile container name aynı olmalı",
                "Tüm servisleri tek seferde implement etmeye çalışmak: önce "
                "1 service + gateway çalışsın, sonra diğerlerini ekle",
            ],
        },
    },

    # =========================================================================
    # TAKEAWAYS
    # =========================================================================
    "takeaways": [
        "Conductor workflow (Explore → Plan → Implement → Commit/Review) büyük projelerde "
        "context kirliliğini önler — her faz arasında context temizliği temel prensiptir",

        "Mikro-servis mimarisi + Agent Teams = doğal eşleşme: her teammate bir service'i "
        "sahiplenir. Agent Teams kullanılamıyorsa aynı iş bölümü subagent'larla simüle edilir",

        "Dynamic Workflows fan-out pattern'i codebase-çapında görevlerde (audit, migration, "
        "test) vazgeçilmezdir — birden fazla agent'ı tek workflow script'i koordine eder",

        "Artifacts terminal çıktısını görsel, paylaşılabilir sayfalara dönüştürür — ama "
        "uygulama değildir: backend yoktur, kalıcı state saklamaz, view-time API çağrısı yapamaz",

        "Adversarial review (fresh context'te, tercihen farklı agent) kendi yazdığını "
        "kendi denetlemekten her zaman daha güvenilirdir",

        "Araçlar değişir, prensipler kalır: context yönetimi, verification loop, iş bölümü "
        "ve iteratif iyileştirme araçtan bağımsız kalıcı becerilerdir",

        "Kişisel Playbook yazmak öğrenmeyi kalıcılaştırır, takım onboarding'ini hızlandırır "
        "ve her yeni projede tutarlı bir başlangıç noktası sağlar",
    ],

    # =========================================================================
    # READING
    # =========================================================================
    "reading": {
        "official": [
            {
                "label": "Share session output as artifacts — Artifact oluşturma, "
                         "güncelleme, paylaşma, page constraints ve availability",
                "url": "https://code.claude.com/docs/en/artifacts",
            },
            {
                "label": "Best practices for Claude Code — Conductor workflow, context "
                         "yönetimi, verification loop, subagent review stratejileri",
                "url": "https://code.claude.com/docs/en/best-practices",
            },
            {
                "label": "Orchestrate teams of Claude Code sessions — Agent Teams spawn, "
                         "messaging, plan approval, shutdown ve token maliyeti",
                "url": "https://code.claude.com/docs/en/agent-teams",
            },
            {
                "label": "Orchestrate subagents at scale with dynamic workflows — Workflow "
                         "script, fan-out, resume, /deep-research, ultracode",
                "url": "https://code.claude.com/docs/en/workflows",
            },
        ],
        "community": [
            {
                "label": "Claude Code Best Practices (Anthropic Engineering) — enterprise "
                         "patterns, context yönetimi, subagent delegasyonu",
                "url": "https://www.anthropic.com/engineering/claude-code-best-practices",
            },
        ],
        "extra": [
            {
                "label": "Common workflows — prompt recipes, worktrees, plan mode, "
                         "subagent delegation, pipe Claude into scripts",
                "url": "https://code.claude.com/docs/en/common-workflows",
            },
        ],
    },

    # =========================================================================
    # NEXT PREVIEW — Gün 20 final gün, sonraki gün yok
    # =========================================================================
    "next_preview": None,

    # =========================================================================
    # CHECKLIST
    # =========================================================================
    "checklist": [
        "Conductor workflow'un 4 fazını (Explore → Plan → Implement → Commit/Review) "
        "uygulayarak mikro-servis projesini planladım",

        "Interview-driven spec ile PRD.md ve/veya ARCHITECTURE.md ürettim",

        "Agent Teams ile en az 3 teammate spawn ettim ve plan approval akışını "
        "yürüttüm (veya subagent fallback ile aynı iş bölümünü simüle ettim)",

        "Minimal skeleton mikro-servis projesini (in-memory data) Docker Compose "
        "ile ayağa kaldırıp gateway üzerinden her servis için en az 1 endpoint'ten "
        "yanıt aldım",

        "En az 1 Artifact oluşturup claude.ai üzerinde açabildim (Artifacts kullanılamıyorsa: aynı dashboard'u lokal HTML olarak üretip tarayıcıda açtım)",

        "/code-review (lokal veya ultra) ya da adversarial review subagent ile "
        "final denetim yaptım",

        "Claude Code Playbook'umu en az 5 bölümle (önerilen: 7) yazdım ve docs/PLAYBOOK.md "
        "olarak kaydettim",

        "20 günlük eğitim boyunca öğrendiğim en kritik 3 prensibi kendi cümlelerimle "
        "ifade edebiliyorum",

        "Artifact'ı güncelleyip yeni versiyon yayınlayabildim (veya güncelleme "
        "akışını biliyorum)",

        "Dynamic Workflow ile en az bir fan-out görevi çalıştırdım; Dynamic Workflows "
        "kullanılamıyorsa aynı fan-out denetimini subagent veya ayrı session fallback'i "
        "ile simüle ettim",
    ],
}


# ── Inline assertion check ──────────────────────────────────────────────────
if __name__ == "__main__":
    L = LESSON
    checks = []

    def chk(name, ok):
        checks.append((name, ok))
        status = "✅" if ok else "❌"
        print(f"  {status} {name}")

    print(f"Schema kontrolleri — Gün {L['day']}")
    chk("day == 20", L["day"] == 20)
    chk("total_days == 20", L["total_days"] == 20)
    chk("week == 4", L["week"] == 4)
    chk("slug present", bool(L["slug"]))
    chk("title present", bool(L["title"]))
    chk("tagline present", bool(L["tagline"]))
    chk("tier == 🔴 Kademe 4", L["tier"] == "🔴 Kademe 4")
    chk("intro present", bool(L["intro"]))

    chk("flow == 4 phases", len(L["flow"]) == 4)
    chk("prerequisites present", len(L["prerequisites"]) >= 1)
    chk("tools_needed present", len(L["tools_needed"]) >= 1)

    obj_count = len(L["objectives"])
    chk(f"objectives count ({obj_count}) in 5-7", 5 <= obj_count <= 7)

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

    tw_count = len(L["takeaways"])
    chk(f"takeaways count ({tw_count}) in 6-8", 6 <= tw_count <= 8)

    off_count = len(L["reading"]["official"])
    chk(f"reading.official count ({off_count}) >= 3", off_count >= 3)

    # Gün 20 final gün — next_preview None olmalı
    chk("next_preview is None (final day)", L["next_preview"] is None)

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
