# -*- coding: utf-8 -*-
"""Gün 9 — MCP ile Araç Entegrasyonu (v2.0, Temmuz 2026)."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table

LESSON = {
    # ── Meta ──────────────────────────────────────────────────────────────
    "day": 9,
    "total_days": 20,
    "week": 2,
    "slug": "mcp-temelleri",
    "title": "MCP (Model Context Protocol) Temelleri",
    "tagline": "Claude'a yeni yetenekler kazandır",
    "tier": None,
    "date_label": "Temmuz 2026",

    # ── Giriş ─────────────────────────────────────────────────────────────
    "intro": (
        "Dün Claude Code'u QA mühendisi olarak çalıştırdın; bugün onu dış "
        "dünyaya bağlıyorsun. MCP (Model Context Protocol), Claude Code'un "
        "GitHub, veritabanları, issue tracker'lar ve daha yüzlerce araçla "
        "konuşmasını sağlayan açık standarttır — artık bir hata mesajını "
        "veya issue içeriğini elle kopyalayıp yapıştırmak yerine, Claude "
        "doğrudan o sisteme erişip üzerinde işlem yapabilir. Gün sonunda "
        "GitHub MCP server'ını bağlamış, gerçek bir issue lifecycle'ı "
        "(oluştur → bul → kapat) çalıştırmış ve MCP güvenlik/organizasyon "
        "kontrolünü tanımış olacaksın."
    ),

    # ── Akış ──────────────────────────────────────────────────────────────
    "flow": [
        {"phase": "1 · Mental Model",        "dur": "30 dk",
         "desc": "MCP nedir, client-server mimarisi, built-in vs MCP tool "
                 "farkı, ne zaman server bağlanmalı, tool search ile context "
                 "yönetimi"},
        {"phase": "2 · Config ve Komutlar",  "dur": "40 dk",
         "desc": "Transport türleri (HTTP/SSE/stdio), /mcp vs claude mcp "
                 "list/get/remove, scope katmanları (local/project/user), "
                 "secret yönetimi"},
        {"phase": "3 · GitHub Hands-on",     "dur": "50 dk",
         "desc": "Fine-grained PAT oluşturma, GitHub MCP server bağlama, "
                 "issue listeleme/oluşturma/kapatma"},
        {"phase": "4 · Güvenlik ve Bonus",   "dur": "30 dk",
         "desc": "Prompt injection ve tool poisoning riski, Managed MCP "
                 "(allowlist/denylist/managed-mcp.json), bonus: web search "
                 "MCP"},
    ],

    # ── Ön koşullar ──────────────────────────────────────────────────────
    "prerequisites": [
        "Gün 1–8 tamamlanmış (Claude Code kurulu, CLAUDE.md hazır, "
        "debugging/review pratiği yapılmış)",
        "Terminal ve Claude Code çalışır durumda",
        "GitHub hesabı (fine-grained personal access token oluşturabilecek yetkide)",
        "Test/sandbox amaçlı kullanılabilecek bir GitHub repo'su (kişisel veya boş bir repo)",
    ],
    "tools_needed": [
        "Terminal (Claude Code çalışır durumda)",
        "GitHub hesabı ve web tarayıcı (token oluşturma için)",
        "Sandbox/test GitHub repo'su",
    ],

    # ── Hedefler ──────────────────────────────────────────────────────────
    "objectives": [
        "MCP mimarisini (client-server, tool discovery) açıklayabileceksin",
        "/mcp panelini ve claude mcp list/get/remove/add komutlarını doğru "
        "durumda kullanabileceksin",
        ".mcp.json, ~/.claude.json ve settings.json'ın farklı rollerini ve "
        "project-scope approval akışını anlayabileceksin",
        "GitHub MCP server'ını fine-grained PAT ile bağlayıp issue "
        "listeleme/oluşturma/kapatma işlemlerini Claude Code üzerinden "
        "yapabileceksin",
        "MCP server güvenlik risklerini (prompt injection, tool poisoning) "
        "değerlendirip minimum-yetki ilkesini uygulayabileceksin",
        "Managed MCP (allowlist/denylist/managed-mcp.json) kavramını "
        "organizasyonel bir kontrol mekanizması olarak tanıyacaksın",
    ],

    "sections": [
        # ── BÖLÜM 1: TEORİK TEMEL ────────────────────────────────────────
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                h("1.1 MCP Nedir ve Hangi Problemi Çözer"),
                p(
                    "MCP (Model Context Protocol), Claude Code'u harici "
                    "araçlara, veritabanlarına ve API'lere bağlamak için "
                    "kullanılan açık kaynaklı bir entegrasyon standardıdır. "
                    "MCP olmadan her araç entegrasyonu özel bir bağlantı "
                    "gerektirirdi; MCP bu sorunu tek bir protokolle çözer — "
                    "bir kez yazılan bir MCP server, Claude Code dahil "
                    "protokolü destekleyen her istemciyle çalışır."
                ),
                table(
                    ["Bileşen", "Rol", "Örnek"],
                    [
                        ["Client", "İstekleri başlatır, tool sonuçlarını "
                         "konuşmaya entegre eder", "Claude Code (senin terminalin)"],
                        ["Server", "Tool, resource ve prompt'ları expose eder",
                         "GitHub MCP server, Postgres MCP server"],
                        ["Transport", "Client-server iletişim kanalı",
                         "HTTP (önerilen), stdio (lokal süreç), WebSocket"],
                    ],
                ),
                p(
                    "Pratikte kural basit: kendini başka bir araçtan "
                    "(issue tracker, monitoring dashboard, tasarım aracı) "
                    "veriyi elle kopyalayıp chat'e yapıştırırken bulduğun "
                    "an, o araç için bir MCP server bağlamayı düşünmelisin. "
                    "Bağlandıktan sonra Claude o sisteme doğrudan erişip "
                    "üzerinde işlem yapabilir — 'JIRA'daki ENG-4521 "
                    "issue'sunda tarif edilen özelliği ekle ve GitHub'da PR "
                    "aç' gibi bir istek tek adımda çalışır."
                ),

                h("1.2 Built-in Tool'lar vs MCP Tool'ları"),
                table(
                    ["", "Built-in tool (Read, Bash, Edit...)", "MCP tool"],
                    [
                        ["Kaynak", "Claude Code'a gömülü", "Harici server, ayrıca bağlanmalı"],
                        ["Kimlik doğrulama", "Gerekmez", "Çoğunlukla gerekir (OAuth, PAT, header)"],
                        ["Kapsam", "Dosya sistemi, terminal, düzenleme",
                         "GitHub, veritabanı, Slack, Figma, monitoring vb. — sınırsız"],
                        ["Bağlantı", "Her zaman aktif", "Proje/kullanıcı bazında yapılandırılır"],
                    ],
                ),
                keypoint(
                    "MCP server sayısı arttıkça context şişmesinden "
                    "korkmana gerek yok: tool search (varsayılan aktif) "
                    "server'ların tool tanımlarını oturum başında context'e "
                    "yüklemek yerine, Claude ihtiyaç duyduğunda arayarak "
                    "keşfeder. Gün 7'de öğrendiğin context bütçesi disiplini "
                    "burada da geçerli."
                ),
                tip(
                    "Yeni bir MCP server bağlamadan önce her zaman güven "
                    "değerlendirmesi yap: harici içerik çeken server'lar "
                    "prompt injection riski taşır. Bu konuyu BÖLÜM 3'te "
                    "derinleştireceğiz."
                ),
            ],
        },
        # ── BÖLÜM 2: PRATİK — ADIM ADIM ─────────────────────────────────
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                h("2.1 Transport Türleri ve Server Ekleme"),
                p(
                    "HTTP, uzak MCP server'lar için önerilen transport'tur "
                    "— en yaygın desteklenen yöntemdir ve OAuth'u destekler. "
                    "SSE (Server-Sent Events) artık deprecated; mevcut "
                    "server'lar için hâlâ çalışır ama yeni bağlantılarda "
                    "HTTP tercih et. stdio, lokal makinede çalışan "
                    "süreçler (örn. bir Python script'i) için kullanılır."
                ),
                code(
                    "# HTTP (önerilen)\n"
                    "claude mcp add --transport http notion https://mcp.notion.com/mcp\n\n"
                    "# Header ile kimlik doğrulama (örn. Bearer token)\n"
                    'claude mcp add --transport http secure-api https://api.example.com/mcp \\\n'
                    '  --header "Authorization: Bearer your-token"\n\n'
                    "# Lokal stdio server\n"
                    "claude mcp add --env AIRTABLE_API_KEY=YOUR_KEY --transport stdio airtable \\\n"
                    "  -- npx -y airtable-mcp-server",
                    "bash",
                ),
                warn(
                    "SSE artık deprecated olarak işaretlendi — yeni "
                    "server bağlarken HTTP'yi tercih et, SSE'yi yalnızca "
                    "server başka transport sunmuyorsa kullan."
                ),

                h("2.2 Server Yönetimi: /mcp vs CLI Komutları"),
                table(
                    ["Kullanım", "Komut", "Amaç"],
                    [
                        ["Oturum içi (Claude Code içinde)", "/mcp",
                         "Bağlı server durumunu görmek, OAuth login akışını başlatmak"],
                        ["Terminal / CLI", "claude mcp list",
                         "Tüm yapılandırılmış server'ları listelemek"],
                        ["Terminal / CLI", "claude mcp get <name>",
                         "Tek bir server'ın detayını görmek"],
                        ["Terminal / CLI", "claude mcp remove <name>",
                         "Server'ı kaldırmak"],
                        ["Terminal / CLI", "claude mcp login <name>",
                         "OAuth destekleyen server için CLI'dan kimlik doğrulama"],
                    ],
                ),
                p(
                    "Not: claude mcp login yalnızca OAuth destekleyen "
                    "server'lar için kullanılır ve komut kullanılabilirliği "
                    "Claude Code sürümüne göre değişebilir — sorun "
                    "yaşarsan claude mcp --help ile güncel komut setini "
                    "kontrol et."
                ),

                h("2.3 Config Katmanları: Nerede Ne Tutulur"),
                table(
                    ["Scope", "Nerede yüklenir?", "Ekiple paylaşılır mı?", "Saklandığı yer"],
                    [
                        ["local (varsayılan)", "Sadece bu projede", "Hayır", "~/.claude.json"],
                        ["project", "Sadece bu projede", "Evet (Git ile)", ".mcp.json (proje kökü)"],
                        ["user", "Tüm projelerinde", "Hayır", "~/.claude.json"],
                    ],
                ),
                p(
                    "settings.json ise MCP server tanımlamak için "
                    "kullanılmaz — izinler, environment değişkenleri ve "
                    "organizasyon davranış ayarları için ayrı bir katmandır."
                ),
                warn(
                    ".mcp.json ile eklenen project-scope server'lar "
                    "kullanılmadan önce onay ister (güvenlik amaçlı); "
                    "onay kararlarını sıfırlamak için "
                    "`claude mcp reset-project-choices` çalıştır. Sırrı "
                    "asla .mcp.json'a düz metin yazma — ${VAR} veya "
                    "${VAR:-default} expansion sözdizimiyle her "
                    "kullanıcının kendi ortam değişkeninden oku."
                ),
                code(
                    '{\n'
                    '  "mcpServers": {\n'
                    '    "api-server": {\n'
                    '      "type": "http",\n'
                    '      "url": "${API_BASE_URL:-https://api.example.com}/mcp",\n'
                    '      "headers": { "Authorization": "Bearer ${API_KEY}" }\n'
                    '    }\n'
                    '  }\n'
                    '}',
                    "json",
                ),

                h("2.4 GitHub MCP Server Bağlama"),
                steps([
                    "github.com/settings/personal-access-tokens adresinden **fine-grained** "
                    "bir token oluştur; sadece çalışacağın sandbox/test repo'ya erişim ver "
                    "(tüm repo'lara değil).",
                    "Server'ı HTTP transport ile ekle: "
                    "`claude mcp add --transport http github https://api.githubcopilot.com/mcp/ "
                    '--header "Authorization: Bearer YOUR_GITHUB_PAT"`',
                    "`claude mcp list` ile server'ın listede göründüğünü doğrula.",
                    "Claude Code oturumunda `/mcp` çalıştırıp bağlantı durumunu ve tool "
                    "sayısını kontrol et.",
                ]),
                warn(
                    "GitHub MCP için burada gösterilen PAT/header akışı, "
                    "resmi dokümantasyondaki örnektir — tek yol bu değil. "
                    "GitHub'ın resmi MCP Server reposu local/remote farklı "
                    "kurulum seçenekleri de sunar (bkz. Ekstra Okuma). "
                    "claude mcp login ise bu senaryoda kullanılmaz çünkü "
                    "GitHub'ın remote server'ı OAuth değil, PAT header ile "
                    "kimlik doğruluyor."
                ),

                h("2.5 Issue Lifecycle: Listele, Oluştur, Kapat"),
                p(
                    "Server bağlandıktan sonra GitHub ile doğal dille "
                    "çalışabilirsin — Claude arka planda ilgili MCP "
                    "tool'larını çağırır:"
                ),
                bullets([
                    "**Listeleme:** \"Bu repo'daki açık issue'ları listele\"",
                    "**Oluşturma:** \"Şu bug tanımını issue formatına çevirip repo'da oluştur\"",
                    "**Kapatma:** \"Az önce oluşturduğun issue'yu bul ve kapat\"",
                ]),
            ],
        },
        # ── BÖLÜM 3: PRATİK — DERİNLEŞ / UYGULAMA ───────────────────────
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 MCP Güvenlik Değerlendirmesi"),
                p(
                    "Her MCP server, Claude Code'un tool setine yeni bir "
                    "yetenek ekler — ve her yetenek bir risk yüzeyidir. "
                    "Bir server'ı bağlamadan önce güvenip güvenmediğini "
                    "sorgula, çünkü Anthropic Directory'deki server'lar "
                    "listeleme kriterlerine göre incelense de, hiçbir MCP "
                    "server'ın güvenlik denetimini Anthropic yapmaz."
                ),
                table(
                    ["Risk", "Ne demek?", "Azaltma"],
                    [
                        ["Prompt injection", "Harici içerik çeken bir "
                         "server (örn. web'den veri okuyan), o içerik "
                         "içine gizlenmiş talimatları Claude'a taşıyabilir",
                         "Yalnızca güvendiğin server'ları bağla; şüpheli "
                         "çıktıları sorgula"],
                        ["Tool poisoning", "Kötü niyetli/ele geçirilmiş "
                         "bir server, tool açıklamasını yanıltıcı yazıp "
                         "Claude'u istenmeyen bir aksiyona yönlendirebilir",
                         "Kaynağı bilinmeyen server'lardan kaçın; "
                         "minimum-yetki token kullan"],
                        ["Secret sızıntısı", "Token'lar .mcp.json'a düz "
                         "metin yazılırsa Git geçmişine sızabilir",
                         "${VAR} expansion veya headersHelper kullan, asla commit etme"],
                    ],
                ),
                warn(
                    "Her server'ı bağlamadan önce güvenip güvenmediğini "
                    "değerlendir — harici içerik çeken server'lar prompt "
                    "injection riski taşır."
                ),

                h("3.2 Managed MCP: Organizasyon Kontrolü"),
                p(
                    "Varsayılan olarak herkes istediği MCP server'ı "
                    "bağlayabilir. Orion TR gibi bir organizasyonda "
                    "yöneticiler bunu merkezi olarak sınırlayabilir — "
                    "sıfır kısıtlamadan tam kilitli bir server setine "
                    "kadar bir yelpazede:"
                ),
                table(
                    ["Desen", "Ne yapar?", "Mekanizma"],
                    [
                        ["MCP'yi tamamen kapat", "Hiçbir server yüklenmez",
                         "Boş mcpServers ile managed-mcp.json"],
                        ["Sabit dağıtım", "Herkese aynı server set'i, "
                         "başkası eklenemez", "Dolu managed-mcp.json"],
                        ["Onaylı katalog", "Kullanıcılar listeden seçer, "
                         "listede olmayan engellenir",
                         "allowedMcpServers + allowManagedMcpServersOnly"],
                        ["Sadece denylist", "Bilinen kötü server'lar "
                         "engellenir, gerisi serbest", "deniedMcpServers"],
                    ],
                ),
                code(
                    '{\n'
                    '  "mcpServers": {\n'
                    '    "github": { "type": "http", "url": "https://api.githubcopilot.com/mcp/" },\n'
                    '    "sentry": { "type": "http", "url": "https://mcp.sentry.dev/mcp" }\n'
                    '  }\n'
                    '}',
                    "json",
                ),
                tip(
                    "DevOps/Manager Notu: Fazla derine inmene gerek yok "
                    "— bugünlük yeterli olan, bu mekanizmaların var "
                    "olduğunu ve managed-mcp.json'ın (platform bazlı "
                    "sistem yoluna, MDM/GPO ile) exclusive kontrol "
                    "sağladığını, allowedMcpServers/deniedMcpServers'ın "
                    "ise daha esnek allowlist/denylist filtresi olduğunu "
                    "bilmen. Detaylı rollout planlaması Gün 19 Enterprise "
                    "Patterns'te işlenecek."
                ),

                h("3.3 Bonus: Web Search MCP Ekleme"),
                p(
                    "Zaman kalırsa, aynı `claude mcp add --transport "
                    "http` deseniyle bir web search MCP server'ı da "
                    "ekleyip test edebilirsin. Bu, günün ana hands-on "
                    "hedefi değil — GitHub issue lifecycle'ına odaklan, "
                    "ekstra zamanın varsa dene."
                ),
                steps([
                    "Anthropic Directory'de (claude.ai/directory) veya "
                    "bilinen bir web search MCP server'ı seç.",
                    "`claude mcp add --transport http <name> <url>` ile ekle.",
                    "\"Son bir haftadaki [konu] hakkındaki gelişmeleri "
                    "araştır ve özetle\" gibi bir prompt ile test et.",
                ]),
            ],
        },
    ],

    # ── PROMPT KÜTÜPHANESİ ───────────────────────────────────────────────
    "prompts": [
        {
            "title": "Sunucu Keşfi",
            "prompt": (
                "Claude Code oturumunda /mcp çalıştır, bağlı server'ları "
                "ve her birinin expose ettiği tool sayısını listele."
            ),
            "note": "/mcp bir komut değil, oturum içi panel; terminaldeki "
                    "`claude mcp list` çıktısıyla karşılaştır.",
        },
        {
            "title": "GitHub Issue Listeleme",
            "prompt": (
                "GitHub MCP üzerinden bu repo'daki açık issue'ları "
                "listele ve label'lara göre grupla."
            ),
            "note": "Server bağlı değilse önce claude mcp list ile "
                    "durumu kontrol et.",
        },
        {
            "title": "GitHub Issue Oluşturma",
            "prompt": (
                "Bu bug tanımını GitHub issue formatına çevir (başlık + "
                "repro adımları + beklenen davranış) ve repo'da issue "
                "olarak oluştur."
            ),
            "note": "Claude'un ürettiği başlık/etiketleri oluşturmadan "
                    "önce gözden geçir.",
        },
        {
            "title": "GitHub Issue Kapatma",
            "prompt": (
                "Az önce oluşturduğun issue'yu bul, acceptance criteria "
                "karşılandıysa bir kapanış notuyla kapat."
            ),
            "note": "Bu, challenge'ın 'bul + kapat' adımı için doğrudan kullanılabilir.",
        },
        {
            "title": "MCP Server Güvenlik Değerlendirmesi",
            "prompt": (
                "Bu MCP server konfigürasyonunu güvenlik açısından "
                "değerlendir: hangi scope'ta tanımlı, hangi header/env "
                "kullanıyor, secret nerede tutuluyor, minimum yetki "
                "ilkesine uyuyor mu?"
            ),
            "note": "Bir .mcp.json dosyasını veya claude mcp get "
                    "çıktısını yapıştırıp isteyebilirsin.",
        },
    ],

    # ── CHALLENGE ─────────────────────────────────────────────────────────
    "challenge": {
        "title": "GitHub MCP ile Issue Lifecycle",
        "task": (
            "Bir eğitim/sandbox GitHub repo'sunda GitHub MCP server'ını "
            "Claude Code'a bağla; Claude Code üzerinden bir issue "
            "oluştur, listele ve sonra kapat."
        ),
        "requirements": [
            "Fine-grained PAT oluştur, yalnızca sandbox/test repo'ya erişim ver",
            "GitHub MCP server'ını HTTP transport ile bağla",
            "claude mcp list ve /mcp ile bağlantı durumunu doğrula",
            "En az 1 issue Claude Code üzerinden oluştur",
            "Oluşturulan issue'yu Claude Code üzerinden tekrar bul (listele/ara)",
            "Issue'yu Claude Code üzerinden kapat",
            "Token'ı repo'ya commit etme; .mcp.json kullanıyorsan ${VAR} expansion ile sakla",
        ],
        "success": [
            "claude mcp list çıktısında GitHub server görünüyor",
            "/mcp panelinde server bağlantı durumu ve tool sayısı doğrulandı",
            "En az 1 issue Claude Code üzerinden oluşturuldu",
            "Oluşturulan issue Claude Code üzerinden tekrar bulundu",
            "Issue Claude Code üzerinden kapatıldı",
            "Token repo'ya commit edilmedi (git log / git diff ile doğrulandı)",
            "Token minimum gerekli yetkilerle (belirli repo(lar)a sınırlı) oluşturuldu",
            "Test/sandbox repo kullanıldı, üretim repo'su değil",
        ],
        "bonus": [
            "Web search MCP server eklendi ve bir prompt ile test edildi",
            "Kendi organizasyonun için taslak bir managed-mcp.json veya "
            "allowedMcpServers örneği yazıldı",
        ],
        "solution": {
            "intro": (
                "Bu challenge'ı adım adım çözmek için aşağıdaki prompt "
                "dizisini izle. Her adımda bir öncekinin çıktısını kontrol et."
            ),
            "prompts": [
                {"title": "1. Token ve bağlantı", "prompt": (
                    "GitHub MCP server'ını sandbox repo'm için bağlamak "
                    "istiyorum. claude mcp add --transport http github "
                    "https://api.githubcopilot.com/mcp/ --header "
                    "\"Authorization: Bearer $GITHUB_PAT\" komutunu "
                    "çalıştırmadan önce, bu komutun ne yaptığını ve "
                    "token'ımın nerede saklanacağını açıkla."
                )},
                {"title": "2. Issue oluştur", "prompt": (
                    "GitHub MCP üzerinden [sandbox-repo] reposunda şu "
                    "başlıkla bir issue oluştur: 'Test: MCP entegrasyon "
                    "doğrulaması'. Açıklamaya bugünün tarihini ve "
                    "oluşturma amacını ekle."
                )},
                {"title": "3. Issue'yu bul", "prompt": (
                    "Az önce oluşturduğun issue'yu repo'daki açık "
                    "issue'lar arasından bul ve numarasını doğrula."
                )},
                {"title": "4. Issue'yu kapat", "prompt": (
                    "Bu issue'yu 'Doğrulama tamamlandı' notuyla kapat. "
                    "Kapatma işleminin başarılı olduğunu teyit et."
                )},
            ],
            "notes": [
                "Token'ı ortam değişkeni olarak ($GITHUB_PAT) tut, "
                "komuta düz metin yazma.",
                "/mcp panelinde server'ın 'connected' durumuna geçtiğini "
                "görmeden issue işlemlerine geçme.",
                "Bonus için managed-mcp.json örneğini gerçek bir sisteme "
                "deploy etmene gerek yok — yalnızca taslak yaz.",
            ],
            "pitfalls": [
                "Token'a repo-genelinde (tüm repo'lar) erişim vermek — "
                "fine-grained token'da yalnızca sandbox repo'yu seç.",
                "Token'ı .mcp.json'a düz metin yazıp yanlışlıkla commit "
                "etmek — ${VAR} expansion kullan ve .gitignore'u kontrol et.",
                "claude mcp login komutunu GitHub için denemek — GitHub "
                "remote server'ı OAuth değil, header/PAT ile çalışır.",
                "Production/gerçek bir repo üzerinde denemek — daima "
                "sandbox/test repo kullan.",
            ],
        },
    },

    # ── TAKEAWAYS ─────────────────────────────────────────────────────────
    "takeaways": [
        "MCP, tool entegrasyonlarını standartlaştıran açık bir protokoldür: "
        "Claude Code client, MCP server tool/resource/prompt sağlar",

        "HTTP transport önerilen yöntemdir; SSE deprecated, yeni "
        "bağlantılarda tercih etme",

        "/mcp oturum içi bir panel (durum görüntüleme + OAuth login), "
        "claude mcp list/get/remove ise CLI'dan server yönetimi — "
        "ikisi farklı amaçlara hizmet eder",

        "Üç config scope'u var: local (varsayılan, özel), project "
        "(.mcp.json, ekiple paylaşılır, approval gerektirir), user "
        "(tüm projelerinde, özel) — settings.json MCP server tanımlamaz",

        "GitHub'ın remote MCP server'ı OAuth değil, fine-grained PAT "
        "header ile kimlik doğrular; claude mcp login yalnızca OAuth "
        "destekleyen server'lar içindir",

        "Sırları asla .mcp.json'a düz metin yazma — ${VAR} expansion "
        "veya headersHelper ile her kullanıcının kendi ortamından oku",

        "MCP güvenlik riskleri gerçek: prompt injection (harici içerik "
        "çeken server'lardan) ve tool poisoning (yanıltıcı tool "
        "açıklamaları) — bağlamadan önce her server'a güven değerlendirmesi yap",

        "Managed MCP, organizasyonun MCP kullanımını merkezi kontrol "
        "altına almasını sağlar: tam kapatmadan sabit server set'ine, "
        "allowlist/denylist'e kadar farklı sıkılık seviyeleri mevcut",
    ],

    # ── KAYNAKLAR ─────────────────────────────────────────────────────────
    "reading": {
        "official": [
            {
                "label": "Connect Claude Code to tools via MCP — transport "
                         "türleri, scope'lar, GitHub örneği, güvenlik uyarısı",
                "url": "https://code.claude.com/docs/en/mcp",
            },
            {
                "label": "Control MCP server access for your organization — "
                         "managed-mcp.json, allowlist/denylist, enterprise kontrol desenleri",
                "url": "https://code.claude.com/docs/en/managed-mcp",
            },
            {
                "label": "MCP quickstart — ilk server bağlantısı için adım adım rehber",
                "url": "https://code.claude.com/docs/en/mcp-quickstart",
            },
            {
                "label": "Model Context Protocol — resmi protokol tanıtımı ve mimarisi",
                "url": "https://modelcontextprotocol.io/docs/getting-started/intro",
            },
        ],
        "community": [
            {
                "label": "Anthropic Directory — incelenmiş (reviewed) MCP "
                         "connector kataloğu",
                "url": "https://claude.ai/directory",
            },
        ],
        "extra": [
            {
                "label": "GitHub MCP Server (resmi repo) — local/remote "
                         "kurulum seçenekleri, toolset detayları",
                "url": "https://github.com/github/github-mcp-server",
            },
        ],
    },

    # ── SONRAKİ GÜN ÖNİZLEME ─────────────────────────────────────────────
    "next_preview": (
        "Yarın (Gün 10) öğrendiklerini birleştirip Todo App'i full-stack "
        "olarak tamamlayıp deploy edeceksin. Bugün kurduğun GitHub MCP "
        "bağlantısı, projenin feature/bug/chore kayıtlarını doğrudan "
        "GitHub issue'ları olarak yönetmeni sağlayacak."
    ),

    # ── KONTROL LİSTESİ ──────────────────────────────────────────────────
    "checklist": [
        "MCP mimarisini (client-server, tool discovery) açıklayabiliyorum",
        "/mcp panelini ve claude mcp list/get/remove komutlarını kullandım",
        "HTTP transport ile en az bir MCP server ekledim",
        "local/project/user scope farkını ve approval akışını biliyorum",
        "Sırları .mcp.json'a düz metin yazmadan ${VAR} expansion ile sakladım",
        "GitHub MCP server'ını fine-grained PAT ile bağladım",
        "GitHub MCP üzerinden issue oluşturdum",
        "GitHub MCP üzerinden issue'yu bulup kapattım",
        "MCP güvenlik risklerini (prompt injection, tool poisoning) değerlendirdim",
        "Managed MCP (allowlist/denylist/managed-mcp.json) kavramını tanıyorum",
    ],
}


# ── Quick sanity check ───────────────────────────────────────────────────
if __name__ == "__main__":
    L = LESSON
    checks = []

    def chk(name, ok):
        checks.append((name, ok))
        print(f"  {'✅' if ok else '❌'} {name}")

    print("Schema validation – Gün 9")
    chk("day == 9", L["day"] == 9)
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
