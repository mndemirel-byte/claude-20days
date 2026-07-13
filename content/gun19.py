# content/gun19.py
# Tek kaynak: LESSON sözlüğü. generators/render_html.py ve generators/render_json.py
# bu sözlükten HTML + JSON üretir.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table


LESSON = {
    "day": 19,
    "total_days": 20,
    "week": 4,
    "slug": "enterprise-patterns",
    "title": "Enterprise Patterns ve Best Practices",
    "tagline": "Takımın için ölçeklenebilir bir Claude Code altyapısı kur",
    "tier": None,
    "date_label": "Temmuz 2026",

    "intro": (
        "Gün 18'de Claude Code'u CI/CD pipeline'ına ve takvime soktun — headless mode, "
        "GitHub Actions entegrasyonu, Routines ile zamanlanmış görevler. Bugün bakış açısını "
        "bireysel geliştirici'den takım ve organizasyona genişletiyorsun. Enterprise "
        "ortamında Claude Code kullanmak sadece 'herkese hesap aç' demek değil: merkezi "
        "politika dağıtımı, model governance, sandbox izolasyonu, maliyet gözlemlenebilirliği "
        "ve standartlaştırılmış onboarding gerektirir. Günün sonunda bir 'Team Starter Kit' "
        "— CLAUDE.md şablonu, agent'lar, skill'ler, hook'lar ve bunları bir plugin "
        "marketplace olarak paketleyen yapıyı — üretmiş, managed settings ve sandbox "
        "stratejisini kavramış, maliyet raporlama katmanlarını birbirinden ayırt edebilir "
        "hale gelmiş olacaksın."
    ),

    "flow": [
        {"phase": "1 · Teorik: Enterprise Büyük Resim", "dur": "15 dk",
         "desc": "Bireysel → takım geçişi, admin karar haritası, erişim tiering (Local Sim / Team-Enterprise / Ops-Admin)"},
        {"phase": "2 · Teorik: Governance + Güvenlik", "dur": "20 dk",
         "desc": "Managed settings, model governance, sandbox spectrum, managed MCP, veri gizliliği"},
        {"phase": "3 · Teorik: Maliyet + Anti-Pattern", "dur": "20 dk",
         "desc": "/usage, billing ayrımı, OTel, analytics dashboard, anti-pattern'ler ve olgunluk merdiveni"},
        {"phase": "4 · Pratik: Team Starter Kit", "dur": "30 dk",
         "desc": "CLAUDE.md template + 3 agent + 2 skill + 2 hook + managed settings simülasyonu"},
        {"phase": "5 · Pratik: Plugin Marketplace + Maliyet", "dur": "25 dk",
         "desc": "Kit'i marketplace olarak paketle, /usage okuma, model/effort strateji kararı"},
        {"phase": "6 · Mini Challenge", "dur": "10 dk",
         "desc": "Kit'i lokal marketplace'te yayınla, yeni projede kur, rollout checklist ile doğrula"},
    ],

    "prerequisites": [
        "Gün 1-18 tamamlanmış: subagent'lar (Gün 11), hooks (Gün 12), plugins (Gün 13), "
        "rol agent'ları (Gün 15), CI/CD ve Routines (Gün 18)",
        "SaaS Dashboard projesi (Gün 14-17'den) çalışır durumda",
        "Terminal ve Claude Code güncel sürümde çalışır durumda",
    ],
    "tools_needed": [
        "Terminal (Claude Code çalışır durumda)",
        "SaaS Dashboard proje dizini (Gün 14-17'den)",
        "VS Code veya tercih edilen editör",
    ],

    "objectives": [
        "Managed settings precedence sırasını (Managed > CLI args > local > project > user) ve "
        "server-managed delivery mekanizmasını açıklayabileceksin; bunun client-side control "
        "olduğunu ve hard security boundary olmadığını bileceksin",
        "`availableModels` ve `enforceAvailableModels` ile merkezi model governance "
        "tanımlayabileceksin; `availableModels` managed source tarafından set edildiğinde "
        "kullanıcı/proje scope'undan genişletilemeyeceğini bileceksin",
        "Sandbox isolation spectrum'unu (sandboxed Bash → sandbox runtime → dev container → "
        "Docker → VM) tehdit modeline göre seçebileceksin; built-in sandbox'ın yalnızca "
        "Bash komutlarını sınırladığını, Read/Edit/WebFetch/MCP/hooks'un aynı sınırda "
        "olmadığını bileceksin",
        "`managed-mcp.json` (fixed server set, server-managed settings ile dağıtılamaz) ile "
        "`allowedMcpServers`/`deniedMcpServers` (policy filtering) farkını uygulayabileceksin",
        "`/usage` (local estimate) ile Console billing (authoritative), OpenTelemetry (org-wide "
        "telemetry) ve Analytics dashboard (adoption/contribution) katmanlarını birbirinden "
        "ayırt edebileceksin",
        "Team starter kit'i plugin marketplace formatında paketleyip lokal olarak "
        "dağıtabileceksin",
        "Yeni takım üyesi için onboarding rehberi ve rollout checklist yazabileceksin",
    ],

    # =========================================================================
    # SECTIONS
    # =========================================================================
    "sections": [
        # ── BÖLÜM 1: TEORİK TEMEL ────────────────────────────────────────
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL — Enterprise'da Claude Code",
            "blocks": [
                # ── 1.1 Büyük Resim ──────────────────────────────────────
                h("1.1 Enterprise Büyük Resim: Bireysel'den Organizasyona"),
                p(
                    "Bir geliştirici Claude Code'u kendi terminalinde kullandığında "
                    "sorumluluk kendindedir: hangi modeli seçer, hangi MCP server'ı bağlar, "
                    "hangi komutu onaylar — hepsine kendisi karar verir. 10 kişilik bir "
                    "takımda bu serbestlik hızla kargaşaya dönüşür: herkesin farklı model "
                    "seçimi maliyet tahminini anlamsızlaştırır, denetimsiz MCP server'lar "
                    "güvenlik riski oluşturur, ortak standart olmaması code review "
                    "kalitesini düşürür."
                ),
                p(
                    "Enterprise'da Claude Code yönetişimi dört eksen etrafında döner: "
                    "(1) Politika — merkezi ayar dağıtımı ve izin kontrolü, "
                    "(2) Güvenlik — sandbox izolasyonu, MCP kısıtlaması ve veri gizliliği, "
                    "(3) Maliyet — model/effort stratejisi, spend limitleri ve gözlemlenebilirlik, "
                    "(4) Onboarding — standart kit ve rollout süreci. Bu dört eksen bugünün "
                    "yapısını belirliyor."
                ),
                p(
                    "Ancak bu günde anlatılan her özellik herkese açık değil. Aşağıdaki "
                    "tiering tablosu, her başlık için minimum erişim seviyesini gösteriyor. "
                    "Pratik adımlarda hangi tier'a düştüğünüzü parantez içinde belirteceğiz."
                ),
                table(
                    ["Erişim Seviyesi", "Kimin İçin", "Özellik Örnekleri"],
                    [
                        [
                            "Local Simulation",
                            "Herkes (Pro, Max, API dahil)",
                            ".claude/settings.json, .claude/agents/, .claude/skills/, "
                            "lokal plugin marketplace, /usage, /sandbox, hook'lar",
                        ],
                        [
                            "Team / Enterprise",
                            "Claude for Teams veya Enterprise planı",
                            "Server-managed settings, org model restrictions, org effort "
                            "limits, analytics dashboard (claude.ai/analytics), Code Review",
                        ],
                        [
                            "Ops / Admin",
                            "Organizasyon admin + MDM/altyapı yetkisi",
                            "managed-mcp.json (sistem path'e deploy), endpoint-managed "
                            "settings (plist/registry), OTel collector, Claude apps gateway",
                        ],
                    ],
                ),
                keypoint(
                    "Bu gün boyunca 'Local Simulation' etiketli her adımı doğrudan "
                    "uygulayabilirsin. 'Team/Enterprise' ve 'Ops/Admin' etiketli "
                    "başlıklarda kavramı öğrenir, sample konfigürasyon yazarsın — ama "
                    "gerçek enforcement için ilgili plan ve altyapı yetkisi gerekir."
                ),

                # ── 1.2 Managed Settings ─────────────────────────────────
                h("1.2 Managed Settings: Merkezi Politika Dağıtımı"),
                p(
                    "Claude Code settings beş katmanlı bir öncelik sırasıyla çalışır. "
                    "Üstteki katman alttakini override eder — merge etmez (array-valued "
                    "settings gibi istisnalar aşağıda):"
                ),
                table(
                    ["Öncelik", "Katman", "Kaynak", "Kimin Kontrolünde"],
                    [
                        ["1 (en yüksek)", "Managed", "Server-managed / endpoint-managed / policyHelper", "Organizasyon admin"],
                        ["2", "Command-line", "--model, --allowedTools vb. CLI argümanları", "Geliştirici (session bazlı)"],
                        ["3", "Local", ".claude/settings.local.json (gitignore'da)", "Geliştirici (kişisel)"],
                        ["4", "Project", ".claude/settings.json (repo'da commit'li)", "Takım (paylaşımlı)"],
                        ["5 (en düşük)", "User", "~/.claude/settings.json", "Geliştirici (global)"],
                    ],
                ),
                p(
                    "Managed tier kendi içinde de alt katmanlara ayrılır: "
                    "policyHelper > server-managed (remote / Claude apps gateway) > "
                    "endpoint-managed (MDM plist / HKLM registry / managed-settings.json dosyası) > "
                    "HKCU (Windows kullanıcı registry — bu katman admin-controlled sayılmaz). "
                    "Managed kaynaklardan herhangi biri non-empty bir payload döndürdüğünde, "
                    "diğer endpoint-managed kaynaklar yok sayılır. İstisna: sandbox allowlist "
                    "lock'ları gibi küçük bir 'cross-source lock' key seti her admin-controlled "
                    "kaynaktan uygulanır."
                ),
                warn(
                    "Server-managed settings client-side bir kontroldür, hard security "
                    "boundary değildir. Yönetilmeyen (unmanaged) bir cihazda kullanıcı "
                    "modified bir client veya eski sürümle bu kontrolleri atlayabilir. "
                    "Güvenlik garantisi istiyorsan managed settings'i sandbox izolasyonu "
                    "ve/veya managed MCP ile birleştirmelisin."
                ),
                p(
                    "Server-managed settings, claude.ai admin console üzerinden "
                    "dağıtılır — MDM altyapısı veya cihaz yönetimi gerektirmez. "
                    "Claude Code başlangıçta settings'i fetch eder, oturum boyunca "
                    "saatlik poll yapar ve `~/.claude/remote-settings.json`'a cache'ler. "
                    "Tolerant parsing uygulanır: bir key schema validation'ı geçemezse "
                    "o key strip edilir ama diğer geçerli key'ler uygulanır."
                ),
                tip(
                    "Managed settings'in aktif olduğunu doğrulamak için oturum içinde "
                    "/status çalıştır. Status tab'ında 'Setting sources' satırı "
                    "'Enterprise managed settings (remote)' gibi aktif kaynağı gösterir."
                ),

                # ── 1.3 Model Governance ─────────────────────────────────
                h("1.3 Model Governance ve Maliyet Stratejisi"),
                p(
                    "Enterprise'da model seçimi bireysel tercihe bırakılamaz: Fable 5 "
                    "en yetenekli ama en pahalı model, Haiku en ucuz ama basit görevler "
                    "için. Merkezi model governance üç mekanizma ile sağlanır:"
                ),
                table(
                    ["Mekanizma", "Nasıl Çalışır", "Gereksinim"],
                    [
                        [
                            "availableModels (managed settings)",
                            "Kullanıcının seçebileceği modelleri sınırlar. Ana session, subagent, "
                            "skill ve advisor seçimlerini etkiler. enforceAvailableModels: true "
                            "eklenirse Default model de allowlist'e zorlanır.",
                            "Managed settings (herhangi bir tier)",
                        ],
                        [
                            "Organization model restrictions",
                            "Claude.ai admin console'dan modelleri disable eder. Server-side "
                            "enforcement — client'tan bağımsız.",
                            "Claude Enterprise planı",
                        ],
                        [
                            "Organization effort limits",
                            "Effort level'i rol bazında sınırlar (ör. max effort yalnızca "
                            "senior developer rolüne açık).",
                            "Claude Enterprise planı",
                        ],
                    ],
                ),
                warn(
                    "`availableModels` managed source tarafından tanımlandığında "
                    "kullanıcı veya proje scope'u bu listeyi genişletemez. Çoğu "
                    "scalar setting managed tarafından override edilir, çoğu "
                    "array-valued setting merge edilir — ama `availableModels` "
                    "istisnai olarak managed listeyi as-is uygular. Bu, 'project "
                    "settings'e model ekleyerek kısıtlamayı bypass ederim' "
                    "yanılgısını önler."
                ),
                code(
                    '// managed-settings.json — model governance örneği\n'
                    '{\n'
                    '  "availableModels": ["sonnet", "opus", "haiku"],\n'
                    '  "enforceAvailableModels": true,\n'
                    '  "model": "sonnet"\n'
                    '}',
                    lang="json",
                ),
                tip(
                    'Bu örnekte Fable 5 allowlist\'te yok → hiçbir geliştirici '
                    '/model fable ile geçiş yapamaz. "model": "sonnet" başlangıç '
                    "default'unu Sonnet 5 yapar ama kullanıcı session içinde "
                    "opus veya haiku'ya geçebilir."
                ),
                p(
                    "Model seçim stratejisi takım maliyetini doğrudan etkiler. "
                    "Aşağıdaki matris, görev türüne göre önerilen model/effort "
                    "kombinasyonlarını gösterir:"
                ),
                table(
                    ["Görev Türü", "Önerilen Model", "Effort", "Gerekçe"],
                    [
                        ["Uzun otonom görev, 1M context", "Fable 5", "high-max",
                         "En yetenekli; ama varsayılan değil, açıkça seçilmeli"],
                        ["Karmaşık akıl yürütme, mimari karar", "Opus 4.8", "high",
                         "Güçlü reasoning; fast mode ile hız/maliyet dengesi"],
                        ["Günlük kodlama, review, test", "Sonnet 5", "high",
                         "Maliyet/yetenek sweet spot; çoğu takım için default"],
                        ["Basit format, lint, açıklama", "Haiku 4.5", "medium-low",
                         "En düşük maliyet; basit görevlerde yeterli"],
                        ["Plan Opus, uygulama Sonnet", "opusplan alias", "high",
                         "Planlama kalitesi + uygulama maliyeti dengesi"],
                    ],
                ),
                tip(
                    "Version pinning stratejisi: Claude Code sürümlerini güncel "
                    "tutmak önemlidir; eski sürümler yeni managed settings key'lerini "
                    "tanımayabilir. Managed settings'e spesifik bir 'minimum version' "
                    "key'i yerine, rollout sürecinde /status ve claude --version ile "
                    "sürüm kontrolü yapın ve güncelleme politikası belirleyin."
                ),

                # ── 1.4 Güvenlik Katmanları ──────────────────────────────
                h("1.4 Güvenlik Katmanları: İzin, Sandbox ve MCP"),
                p(
                    "Enterprise güvenliği üç katmanda ele alınır: (1) Permission modes — "
                    "eylemin çalışıp çalışmayacağına ve onay gerekip gerekmediğine karar "
                    "verir, (2) Sandbox — çalışan komutun neye erişebileceğini sınırlar, "
                    "(3) Managed MCP — hangi dış araçların bağlanabileceğini kontrol eder. "
                    "Bu üçü birbirini tamamlar; tek başına hiçbiri yeterli değildir."
                ),
                p(
                    "Sandbox isolation bir spectrum üzerinde konumlanır. Her katman farklı "
                    "bir tehdit modeline yanıt verir:"
                ),
                table(
                    ["Katman", "Ne İzole Eder", "Ne İzole Etmez", "Kurulum"],
                    [
                        [
                            "Sandboxed Bash (built-in)",
                            "Bash komutlarının filesystem ve network erişimi (macOS Seatbelt, "
                            "Linux bubblewrap ile)",
                            "Read/Edit/Write file tools, WebFetch, MCP server'lar, hooks — "
                            "bunlar sandbox sınırı dışında çalışır",
                            "/sandbox ile etkinleştir; zero-install (macOS), "
                            "bubblewrap+iptables (Linux)",
                        ],
                        [
                            "Sandbox Runtime",
                            "Tüm Claude Code sürecini containerd ile izole eder",
                            "Host kernel paylaşılır (VM düzeyinde değil)",
                            "claude sandbox init; Docker Desktop sandbox desteği",
                        ],
                        [
                            "Dev Container",
                            "Proje bazlı izole ortam; filesystem, network, kimlik ayrı",
                            "Container escape riski (kernel paylaşımlı)",
                            "devcontainer.json + VS Code / CLI",
                        ],
                        [
                            "Docker Container",
                            "Namespace izolasyonu, resource limits, network=none mümkün",
                            "Kernel paylaşımlı; gVisor ile güçlendirilebilir",
                            "docker run --cap-drop ALL --network none ...",
                        ],
                        [
                            "VM / Firecracker",
                            "Kernel düzeyinde tam izolasyon",
                            "En yüksek overhead; cold-start süresi",
                            "Cloud instance, Firecracker microVM",
                        ],
                    ],
                ),
                warn(
                    "Built-in sandboxed Bash sadece Bash komutlarını sınırlar. "
                    "Read, Edit, Write gibi file tool'lar, WebFetch, MCP server'lar "
                    "ve hook'lar aynı izolasyon sınırı içinde değildir — host "
                    "üzerinde çalışmaya devam eder. 'Sandbox açtım, artık her şey "
                    "izole' varsayımı yanlıştır. Tüm Claude Code sürecini izole "
                    "etmek gerekiyorsa sandbox runtime, dev container, Docker veya "
                    "VM kullanılmalıdır."
                ),
                p(
                    "Sandbox admin entegrasyonu: Managed settings ile sandbox "
                    "politikasını tüm geliştiricilere zorunlu kılabilirsin. "
                    "sandbox.credentials ile belirli env variable'ları sandboxed "
                    "komutlardan gizleyebilir, CLAUDE_CODE_SUBPROCESS_ENV_SCRUB ile "
                    "Anthropic ve cloud provider credential'larını tüm alt "
                    "süreçlerden strip edebilirsin."
                ),

                # ── 1.4b Managed MCP ─────────────────────────────────────
                h("1.4b Managed MCP: Dış Araç Erişimini Kontrol Etme"),
                p(
                    "MCP server'lar Claude Code'a güçlü dış yetenekler ekler — ama "
                    "enterprise'da 'herkes istediği server'ı bağlasın' kabul edilemez. "
                    "İki farklı kontrol mekanizması var ve bunları karıştırmamak önemli:"
                ),
                table(
                    ["Mekanizma", "Ne Yapar", "Nasıl Dağıtılır", "Etki"],
                    [
                        [
                            "managed-mcp.json",
                            "Fixed server set tanımlar. Kullanıcı başka server ekleyemez; "
                            "claude mcp add enterprise policy hatası verir.",
                            "Sistem path'e admin yetkisiyle deploy (Jamf, GPO, Intune vb.). "
                            "Server-managed settings ile dağıtılamaz.",
                            "Exclusive: yalnızca bu dosyadaki server'lar yüklenir. "
                            "Plugin-provided server'lar suppress edilir "
                            "(allowAllClaudeAiMcps: true ile claude.ai connector'ları hariç).",
                        ],
                        [
                            "allowedMcpServers / deniedMcpServers",
                            "Kullanıcının veya managed set'in eklediği server'ları "
                            "allowlist/denylist ile filtreler.",
                            "Herhangi bir settings katmanında tanımlanabilir (managed dahil). "
                            "Kullanıcı kendi deniedMcpServers'ını ekleyerek managed bir "
                            "server'ı kendisi için engelleyebilir.",
                            "Additive filtering: managed-mcp.json ile birlikte de çalışır — "
                            "managed set'teki server bile allowlist'e uymuyorsa yüklenmez.",
                        ],
                    ],
                ),
                keypoint(
                    "managed-mcp.json exclusive bir deploy aracıdır ve admin yetkisi "
                    "gerektirir. allowedMcpServers/deniedMcpServers ise policy filtering "
                    "yapan, settings katmanlarına yerleştirilebilen kurallar setidir. "
                    "İkisi birlikte kullanıldığında en güçlü kontrolü sağlar."
                ),
                p(
                    "Hook güvenliği de benzer şekilde merkezi kontrol altına alınabilir. "
                    "allowManagedHooksOnly: true ayarı, yalnızca managed settings "
                    "ve managed settings'teki enabledPlugins tarafından sağlanan hook'ları "
                    "yükler; kullanıcı ve proje hook'ları engellenir."
                ),

                # ── 1.5 Veri Gizliliği ──────────────────────────────────
                h("1.5 Veri Gizliliği ve Uyumluluk"),
                p(
                    "Claude Code'un veri akışı hesap türüne göre farklı "
                    "retention politikalarına tabidir:"
                ),
                table(
                    ["Hesap Türü", "Retention", "Model Eğitimine Katkı"],
                    [
                        ["Consumer (Free/Pro/Max) — feedback izni var",
                         "Standart retention", "Katkı sağlayabilir (privacy ayarlarına bağlı)"],
                        ["Consumer — feedback izni yok",
                         "30 gün retention", "Hayır"],
                        ["Commercial (Team/Enterprise/API)",
                         "Standart commercial retention", "Hayır — kod ve prompt'lar model "
                         "eğitiminde kullanılmaz"],
                        ["Enterprise + ZDR (Zero Data Retention)",
                         "Zero data retention", "Hayır"],
                    ],
                ),
                warn(
                    "ZDR (Zero Data Retention) standart Enterprise planında "
                    "otomatik olarak dahil değildir. Qualified Claude for Enterprise "
                    "hesapları için Anthropic account team tarafından per-organization "
                    "bazında etkinleştirilir. 'Enterprise aldık, ZDR'mız var' varsayımı "
                    "doğru olmayabilir — account team ile doğrulanmalıdır."
                ),
                p(
                    "Yerel veri: Claude Code oturum transcript'lerini "
                    "~/.claude/projects/ altında düz metin olarak saklar; "
                    "varsayılan 30 gün sonra temizlenir. cleanupPeriodDays "
                    "ayarıyla bu süre değiştirilebilir. Telemetry "
                    "(operasyonel metrikler — kod veya dosya yolu içermez) "
                    "varsayılan olarak açıktır; DISABLE_TELEMETRY=1 ile "
                    "kapatılabilir."
                ),

                # ── 1.6 Maliyet Gözlemlenebilirliği ─────────────────────
                h("1.6 Maliyet Gözlemlenebilirliği"),
                p(
                    "Claude Code maliyet takibinde beş farklı katman var. "
                    "Her birinin kapsamı ve güvenilirlik seviyesi farklı:"
                ),
                table(
                    ["Katman", "Kapsam", "Erişim", "Not"],
                    [
                        [
                            "/usage (ana komut; /cost ve /stats alias)",
                            "Mevcut oturum maliyeti + plan limit kullanımı. "
                            "Skill, subagent, plugin, MCP bazlı breakdown (d/w toggle).",
                            "Herkes (Local Sim)",
                            "Lokal tahmindir; authoritative billing değildir. "
                            "Yalnızca bu cihazdaki kullanımı gösterir.",
                        ],
                        [
                            "Console Usage (platform.claude.com)",
                            "Workspace bazlı token kullanımı ve spend.",
                            "API / Console kullanıcıları",
                            "Authoritative billing kaynağı.",
                        ],
                        [
                            "Analytics Dashboard (claude.ai/analytics/claude-code)",
                            "Lines of code accepted, suggestion accept rate, daily active "
                            "users, spend chart, GitHub contribution metrics (beta).",
                            "Team / Enterprise (admin/owner)",
                            "Adoption ve productivity metrikleri için; billing için değil.",
                        ],
                        [
                            "OpenTelemetry (OTel) Export",
                            "Per-session token/cost/tool metrics; skill.name, plugin.name, "
                            "agent.name ile attribution. Grafana, Datadog vb.'ye aktar.",
                            "Ops/Admin (OTel collector kurulumu gerekir)",
                            "Org-wide, real-time observability; cost metric'ler tahminidir.",
                        ],
                        [
                            "Claude Apps Gateway",
                            "Per-user audit log, OTLP metrics, per-user spend limits. "
                            "Third-party provider routing (Bedrock, Vertex, Foundry).",
                            "Ops/Admin (self-hosted gateway)",
                            "En kapsamlı enterprise kontrol; gateway kurulumu ve IdP "
                            "entegrasyonu gerektirir.",
                        ],
                    ],
                ),
                keypoint(
                    "/usage oturum içinde hızlı farkındalık için idealdir ama "
                    "gösterdiği dolar değeri bir tahmindir — fatura için Console "
                    "Usage veya cloud provider billing dashboard'una bakılmalıdır. "
                    "Takım genelinde maliyet optimizasyonu yapacaksan Analytics + "
                    "OTel birlikte kullanılmalıdır."
                ),
                p(
                    "Maliyet azaltma stratejileri: Claude Code otomatik prompt "
                    "caching uygular (tekrar eden system prompt ve CLAUDE.md içeriği "
                    "cache'lenir). /clear ile görev geçişlerinde context temizliği, "
                    "/compact ile bilinçli özetleme, subagent delegasyonu ile context "
                    "izolasyonu — bunlar Gün 7'de öğrendiğin context stratejilerinin "
                    "enterprise ölçeğindeki karşılığıdır."
                ),
                p(
                    "Takım büyüklüğüne göre TPM (Token Per Minute) önerisi: "
                    "küçük takım (~10 kişi) için kişi başı ~80K TPM, orta takım "
                    "(~50 kişi) için ~40K, büyük takım (200+ kişi) için ~20K. "
                    "Rate limit'ler organizasyon seviyesinde uygulanır; bireysel "
                    "kullanıcı geçici olarak payından fazlasını tüketebilir."
                ),

                # ── 1.7 Anti-Pattern'ler ─────────────────────────────────
                h("1.7 Anti-Pattern'ler ve Olgunluk Merdiveni"),
                p(
                    "Enterprise Claude Code kullanımında sık karşılaşılan "
                    "anti-pattern'ler:"
                ),
                table(
                    ["Anti-Pattern", "Sonuç", "Çözüm"],
                    [
                        [
                            "Dev CLAUDE.md (10K+ karakter)",
                            "Her mesajda context bütçesinin büyük kısmı "
                            "CLAUDE.md'ye harcanır; maliyet artar, erken talimatların "
                            "etkisi zayıflar.",
                            "CLAUDE.md'yi 2-3K karakterle sınırla; detayları "
                            "skill'lere ve rules/ dosyalarına taşı.",
                        ],
                        [
                            "Her şey için agent kullanma",
                            "Gereksiz context fork'u; basit görevlerde overhead.",
                            "Agent yalnızca ayrı context ve uzman prompt "
                            "gerektiğinde kullan; basit görevleri ana session'da yap.",
                        ],
                        [
                            "Sandbox'suz --dangerously-skip-permissions",
                            "Claude'un tüm dosya sistemi ve ağa sınırsız erişimi; "
                            "güvenlik riski maksimum.",
                            "Bypass mode yalnızca container, VM veya sandbox "
                            "runtime içinde kullan.",
                        ],
                        [
                            "Tek model herkes için",
                            "Ya pahalı model israf, ya ucuz model yetersiz.",
                            "Görev türüne göre model/effort matrisini uygula "
                            "(bkz. Bölüm 1.3 tablosu).",
                        ],
                        [
                            "MCP server denetimi yok",
                            "Potansiyel veri sızıntısı, güvenilmeyen araç riski.",
                            "allowedMcpServers veya managed-mcp.json ile kontrol.",
                        ],
                    ],
                ),
                p(
                    "Enterprise olgunluk merdiveni — takımın nerede olduğunu "
                    "değerlendirmek için:"
                ),
                table(
                    ["Seviye", "Özellik", "Gösterge"],
                    [
                        ["1 · Ad-hoc", "Bireysel kullanım, standart yok",
                         "Herkes kendi ayarlarıyla çalışır; maliyet takibi yok"],
                        ["2 · Standardized", "Ortak CLAUDE.md ve agent seti",
                         "Team starter kit repo'da; yeni üye kit ile başlar"],
                        ["3 · Governed", "Managed settings + sandbox + MCP kontrolü",
                         "Model allowlist, sandbox policy, analytics dashboard aktif"],
                        ["4 · Optimized", "OTel + gateway + continuous improvement",
                         "Per-skill/agent maliyet attribution; effort tuning; "
                         "plugin marketplace ile güncel kit dağıtımı"],
                    ],
                ),
            ],
        },

        # ── BÖLÜM 2: PRATİK ADIM ADIM ────────────────────────────────────
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM: Team Starter Kit",
            "blocks": [
                h("2.1 CLAUDE.md Şablonu [Local Sim]"),
                p(
                    "Enterprise-grade bir CLAUDE.md şablonu oluşturarak başlıyoruz. "
                    "Amaç: yeni bir projede bu template'i kopyala-yapıştır yapıp "
                    "birkaç satır değiştirerek takım standardına uygun bir CLAUDE.md "
                    "elde etmek."
                ),
                steps([
                    "Bir çalışma dizini oluştur: mkdir -p team-claude-code-starter-kit",
                    "Claude Code'a şu prompt'u ver:",
                ]),
                code(
                    "Bu proje için enterprise-grade bir CLAUDE.md şablonu oluştur.\n"
                    "Şablonda şunlar olsun:\n"
                    "- Proje metadatası (ad, açıklama, teknoloji stack'i — placeholder)\n"
                    "- Coding standards (naming convention, test gereksinimleri)\n"
                    "- Security policy (secret yok, güvenli dependency kullanımı)\n"
                    "- Model/effort guidance (default: sonnet, high; review: opus)\n"
                    "- Yasaklı eylemler (production DB'ye doğrudan erişim yok vb.)\n"
                    "Toplam 2000-2500 karakter arasında tut — gereğinden uzun CLAUDE.md\n"
                    "context bütçesini yer.",
                    lang="text",
                ),
                tip(
                    "CLAUDE.md'yi 2-3K karakterle sınırlamak bilinçli bir tasarım kararı. "
                    "Detaylı kurallar .claude/rules/ altına path-scoped rule olarak, "
                    "domain bilgisi skill'lere taşınmalı. Bu yaklaşım Gün 3 ve Gün 7'de "
                    "öğrendiğin context yönetimi prensiplerinin enterprise uygulaması."
                ),

                # ── 2.2 Agent'lar ve Skills ──────────────────────────────
                h("2.2 Kit: Agent'lar ve Skills [Local Sim]"),
                p(
                    "Starter kit'e 3 agent ve 2 skill ekleyeceğiz. Bunlar Gün 11 ve "
                    "Gün 13'te öğrendiğin subagent ve skill mekanizmalarının "
                    "standartlaştırılmış, takım genelinde paylaşıma hazır versiyonları."
                ),
                steps([
                    "Dizin yapısını oluştur:\n"
                    "mkdir -p plugins/team-starter-kit/.claude-plugin\n"
                    "mkdir -p plugins/team-starter-kit/agents\n"
                    "mkdir -p plugins/team-starter-kit/skills/project-setup\n"
                    "mkdir -p plugins/team-starter-kit/skills/deployment-checklist\n"
                    "mkdir -p plugins/team-starter-kit/commands\n"
                    "mkdir -p plugins/team-starter-kit/hooks",

                    "Claude Code'a 3 agent markdown dosyası yazdır:\n"
                    "- security-reviewer.md (model: opus, effort: high, tools: Read/Grep/Glob/Bash)\n"
                    "- test-writer.md (model: sonnet, effort: high, tools: Read/Write/Bash)\n"
                    "- documenter.md (model: sonnet, effort: medium, tools: Read/Write/Glob)",

                    "2 skill için SKILL.md dosyaları yazdır:\n"
                    "- project-setup: yeni proje başlatma rehberi (dizin yapısı, CLAUDE.md, git init)\n"
                    "- deployment-checklist: deploy öncesi kontrol listesi (testler, lint, env vars, secrets)",

                    "3 command markdown dosyası yazdır:\n"
                    "- security-review.md: güvenlik taraması başlatan komut\n"
                    "- cost-check.md: /usage çıktısını yorumlayan komut\n"
                    "- onboarding.md: yeni takım üyesine rehber gösteren komut",
                ]),
                keypoint(
                    "Agent frontmatter'ında model ve effort seçimi bilinçli olmalı. "
                    "Security reviewer için Opus + high (kritik akıl yürütme), "
                    "documenter için Sonnet + medium (metin üretimi, düşük maliyet). "
                    "Bu seçimler Gün 15'teki rol-model eşlemesinin standardizasyonu."
                ),

                # ── 2.3 Hook'lar ─────────────────────────────────────────
                h("2.3 Kit: Hook'lar [Local Sim]"),
                p(
                    "Kit'e 2 hook ekliyoruz — biri güvenlik, biri denetim için:"
                ),
                steps([
                    "block-dangerous-bash.sh: PreToolUse Bash hook'u. rm -rf /, "
                    "güvenlik açısından riskli komutları (DROP TABLE, chmod 777 vb.) "
                    "yakalar ve engeller.",

                    "audit-edit.sh: PostToolUse Write/Edit hook'u. Yapılan her dosya "
                    "değişikliğini tarih damgasıyla bir log dosyasına yazar "
                    "(basit denetim izi).",
                ]),
                code(
                    '# plugins/team-starter-kit/hooks/block-dangerous-bash.sh\n'
                    '#!/usr/bin/env bash\n'
                    '# PreToolUse Bash hook: tehlikeli komutları engeller\n'
                    'INPUT=$(cat)\n'
                    'COMMAND=$(echo "$INPUT" | jq -r \'.tool_input.command // empty\')\n'
                    '\n'
                    '# Tehlikeli pattern\'ler\n'
                    'DANGEROUS_PATTERNS=(\n'
                    '  "rm -rf /"\n'
                    '  "rm -rf ~"\n'
                    '  "DROP TABLE"\n'
                    '  "DROP DATABASE"\n'
                    '  "chmod 777"\n'
                    '  "> /dev/sda"\n'
                    ')\n'
                    '\n'
                    'for PATTERN in "${DANGEROUS_PATTERNS[@]}"; do\n'
                    '  if echo "$COMMAND" | grep -qi "$PATTERN"; then\n'
                    '    echo "BLOCKED: Dangerous command detected: $PATTERN" >&2\n'
                    '    exit 2  # exit 2 = block the tool call\n'
                    '  fi\n'
                    'done\n'
                    '\n'
                    'exit 0  # exit 0 = allow',
                    lang="bash",
                ),
                tip(
                    "Hook exit code'ları: 0 = izin ver, 2 = engelle (hata mesajıyla). "
                    "Enterprise ortamda allowManagedHooksOnly: true ile yalnızca "
                    "managed/plugin hook'larının çalışmasını zorunlu kılabilirsin."
                ),

                # ── 2.4 Plugin Marketplace ───────────────────────────────
                h("2.4 Kit'i Plugin Marketplace Olarak Paketleme [Local Sim]"),
                p(
                    "Şimdi tüm bu bileşenleri bir plugin marketplace yapısına "
                    "dönüştürüyoruz. Bu yapı sayesinde kit başka projelere ve "
                    "takım üyelerine dağıtılabilir."
                ),
                steps([
                    "Marketplace root'unda .claude-plugin/ dizinini oluştur:\n"
                    "mkdir -p .claude-plugin",

                    "marketplace.json dosyasını oluştur (aşağıdaki örneği kullan)",

                    "Plugin manifest'ini oluştur:\n"
                    "plugins/team-starter-kit/.claude-plugin/plugin.json",

                    "Claude Code oturumunda validate et:\n"
                    "/plugin validate .",

                    "Marketplace'i ekle ve plugin'i kur:\n"
                    "/plugin marketplace add ./\n"
                    "/plugin install team-starter-kit@team-tools",
                ]),
                code(
                    '// .claude-plugin/marketplace.json\n'
                    '{\n'
                    '  "name": "team-tools",\n'
                    '  "owner": {\n'
                    '    "name": "Orion TR Engineering"\n'
                    '  },\n'
                    '  "description": "Enterprise team starter kit — agents, skills, hooks",\n'
                    '  "plugins": [\n'
                    '    {\n'
                    '      "name": "team-starter-kit",\n'
                    '      "source": "./plugins/team-starter-kit",\n'
                    '      "description": "Standard agents, skills, hooks and commands for team projects",\n'
                    '      "version": "1.0.0"\n'
                    '    }\n'
                    '  ]\n'
                    '}',
                    lang="json",
                ),
                code(
                    '// plugins/team-starter-kit/.claude-plugin/plugin.json\n'
                    '{\n'
                    '  "name": "team-starter-kit",\n'
                    '  "description": "Enterprise starter kit: security-reviewer, test-writer, '
                    'documenter agents + project-setup, deployment-checklist skills + hooks",\n'
                    '  "version": "1.0.0"\n'
                    '}',
                    lang="json",
                ),
                warn(
                    "plugin.json dosyası plugins/team-starter-kit/.claude-plugin/plugin.json "
                    "path'inde olmalıdır — doğrudan plugin kökünde değil. Bu, resmi docs "
                    "walkthrough'undaki standart yapıdır. Yanlış path plugin'in "
                    "tanınmamasına neden olur."
                ),
                tip(
                    "CLI tarafında claude plugin marketplace add ve claude plugin install "
                    "komutları da kullanılabilir (otomasyon ve CI senaryoları için). "
                    "Eğitim pratiklerinde session-içi /plugin ... slash komutları "
                    "daha doğal ve interaktiftir."
                ),

                # ── 2.5 Managed Settings Simülasyonu ────────────────────
                h("2.5 Managed Settings Simülasyonu [Local Sim]"),
                p(
                    "Gerçek server-managed settings Team/Enterprise gerektirir. "
                    "Ama lokal olarak aynı JSON yapısını .claude/settings.json veya "
                    "settings.local.json'a yazarak policy kararlarını simüle edebilirsin. "
                    "Ayrıca examples/ dizinine enterprise-ready sample'lar ekleyeceğiz."
                ),
                steps([
                    "examples/ dizini oluştur ve 3 sample dosya yaz:\n"
                    "- managed-settings.sample.json (model allowlist + sandbox policy)\n"
                    "- managed-mcp.sample.json (fixed MCP server set)\n"
                    "- sandbox-policy.sample.json (sandboxed bash config)",

                    ".claude/settings.json'a model ve sandbox ayarı ekle:\n"
                    '{ "model": "sonnet", "sandbox": { "autoApprove": true } }',

                    "/status ile hangi settings source'ların aktif olduğunu doğrula.",

                    "/sandbox ile sandbox durumunu kontrol et — Dependencies, "
                    "Overrides ve Config panellerini incele.",
                ]),
                code(
                    '// examples/managed-settings.sample.json\n'
                    '// NOT: Bu örnek gerçek deploy için managed settings altyapısı gerektirir.\n'
                    '// Lokal simülasyonda .claude/settings.json\'a yazabilirsiniz.\n'
                    '{\n'
                    '  "availableModels": ["sonnet", "opus", "haiku"],\n'
                    '  "enforceAvailableModels": true,\n'
                    '  "model": "sonnet",\n'
                    '  "sandbox": {\n'
                    '    "autoApprove": true,\n'
                    '    "allow": {\n'
                    '      "allowedDomains": ["github.com", "registry.npmjs.org"]\n'
                    '    }\n'
                    '  },\n'
                    '  "allowManagedHooksOnly": true\n'
                    '}',
                    lang="json",
                ),
                code(
                    '// examples/managed-mcp.sample.json\n'
                    '// NOT: Bu dosya gerçek ortamda sistem path\'ine admin yetkisiyle deploy edilir.\n'
                    '// Server-managed settings ile dağıtılamaz. Burada yalnızca yapıyı gösteriyoruz.\n'
                    '{\n'
                    '  "mcpServers": {\n'
                    '    "approved-github": {\n'
                    '      "command": "npx",\n'
                    '      "args": ["-y", "@anthropic/mcp-github"]\n'
                    '    },\n'
                    '    "company-jira": {\n'
                    '      "command": "npx",\n'
                    '      "args": ["-y", "@company/mcp-jira"]\n'
                    '    }\n'
                    '  }\n'
                    '}',
                    lang="json",
                ),
                keypoint(
                    "managed-mcp.sample.json bir Ops/Admin artifact'idir — öğrenciden "
                    "bunu gerçekten deploy etmesi beklenmez. Amacı yapıyı öğrenmek ve "
                    "managed-mcp.json ile allowedMcpServers farkını anlamaktır."
                ),

                # ── 2.6 Maliyet Raporu ───────────────────────────────────
                h("2.6 Maliyet Raporu: /usage Okuma ve Strateji [Local Sim]"),
                p(
                    "Günün pratik bölümünü maliyet farkındalığı ile kapatıyoruz."
                ),
                steps([
                    "/usage çalıştır — oturum maliyetini, API süresini, "
                    "kod değişiklik satırlarını gör.",

                    "d (day) ve w (week) ile dönem değiştir — son 24 saat ve "
                    "son 7 günlük breakdown'ı karşılaştır.",

                    "Breakdown bölümünde hangi skill, subagent, plugin veya "
                    "MCP server'ın en çok token tükettiğini belirle.",

                    "Takımın için bir model/effort strateji kararı yaz:\n"
                    "- Default model ne olmalı?\n"
                    "- Hangi görevlerde Opus/Fable gerekli?\n"
                    "- Effort level policy ne olmalı?\n"
                    "- Estimated monthly cost per developer?",
                ]),
                warn(
                    "/usage içindeki dolar değeri bu cihazdaki lokal tahmindir. "
                    "Farklı cihazlardaki veya claude.ai web kullanımı dahil değildir. "
                    "Authoritative billing için Console Usage (API) veya cloud "
                    "provider billing dashboard'una bakılmalıdır."
                ),
            ],
        },

        # ── BÖLÜM 3: DERİNLEŞ ────────────────────────────────────────────
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 Onboarding Guide ve Rollout Checklist [Local Sim]"),
                p(
                    "Enterprise rollout'un en kritik noktalarından biri: yeni takım "
                    "üyesi ilk gününde ne yapacak? Aşağıdaki adımlarla bir "
                    "ONBOARDING.md ve ROLLOUT-CHECKLIST.md yazacaksın."
                ),
                steps([
                    "Claude Code'a şu prompt'u ver:\n"
                    "'Yeni bir takım üyesi için Claude Code onboarding rehberi yaz. "
                    "Adımlar: (1) Kurulum, (2) Kimlik doğrulama, (3) Team starter kit "
                    "kurulumu, (4) İlk session — kit'teki security-reviewer ile bir "
                    "kod taraması, (5) /usage ile maliyet farkındalığı. Format: "
                    "ONBOARDING.md'",

                    "Ardından bir ROLLOUT-CHECKLIST.md yazdır — admin perspektifinden:\n"
                    "□ Managed settings hazırlandı mı?\n"
                    "□ Model allowlist tanımlandı mı?\n"
                    "□ Sandbox policy belirlendi mi?\n"
                    "□ MCP server set onaylandı mı?\n"
                    "□ Starter kit marketplace'e publish edildi mi?\n"
                    "□ Analytics dashboard erişimi açıldı mı?\n"
                    "□ Onboarding guide hazır mı?",

                    "Her iki dosyayı starter kit repo'sunun kök dizinine koy.",
                ]),

                h("3.2 Sandbox Stratejisi Karar Ağacı"),
                p(
                    "Farklı senaryolar farklı izolasyon katmanları gerektirir. "
                    "Aşağıdaki karar ağacını kullanarak kendi ortamın için "
                    "doğru sandbox stratejisini belirle:"
                ),
                table(
                    ["Senaryo", "Önerilen İzolasyon", "Neden"],
                    [
                        [
                            "Bireysel geliştirici, güvenilir codebase",
                            "Sandboxed Bash (built-in) + auto mode",
                            "Düşük overhead, yeterli Bash izolasyonu, "
                            "auto mode classifier ile akıllı onay",
                        ],
                        [
                            "Takım, standart projeler",
                            "Sandboxed Bash + permission allowlists",
                            "Ortak ground; ekstra MCP/file tool izolasyonu gerekmez",
                        ],
                        [
                            "CI/CD pipeline, otonom agent",
                            "Sandbox runtime veya Docker (--network none)",
                            "Unattended çalışma; tüm sürecin izole olması şart",
                        ],
                        [
                            "Untrusted code evaluation",
                            "VM veya Firecracker microVM",
                            "Kernel-level izolasyon; container escape riskini sıfırlar",
                        ],
                        [
                            "Regulated industry (finans, sağlık)",
                            "VM + gateway + ZDR + audit logging",
                            "Compliance gereksinimleri; her katmanda kontrol",
                        ],
                    ],
                ),
                steps([
                    "SaaS Dashboard projesinde /sandbox çalıştır ve mevcut "
                    "sandbox durumunu incele.",

                    "Sandboxed Bash'i etkinleştir (eğer aktif değilse): "
                    "/sandbox panelinde 'Enable' seç.",

                    "Basit bir test: sandbox aktifken 'curl https://example.com' "
                    "komutunu dene — allowedDomains listesine göre geçer veya "
                    "engellenir.",

                    "Kendi projen için yukarıdaki karar tablosundan uygun "
                    "izolasyon katmanını seç ve gerekçesini not et.",
                ]),

                h("3.3 Enterprise Challenge: Kit'i Yayınla ve Doğrula"),
                p(
                    "Günün final challenge'ı: ürettiğin tüm deliverable'ları "
                    "bir arada test et."
                ),
                steps([
                    "README.md yaz: kit'in ne içerdiği, nasıl kurulacağı, "
                    "hangi bileşenlerin ne yaptığı. Claude Code'a yazdır.",

                    "Kit'i lokal marketplace olarak doğrula:\n"
                    "/plugin validate .\n"
                    "Hata varsa düzelt.",

                    "Starter kit marketplace'i ekle:\n"
                    "/plugin marketplace add ./team-claude-code-starter-kit",

                    "Plugin'i kur:\n"
                    "/plugin install team-starter-kit@team-tools",

                    "Yeni bir test projesi oluştur (mkdir test-project && cd test-project "
                    "&& git init) ve kit'in agent'larını, skill'lerini ve hook'larını "
                    "bu projede test et.",

                    "ROLLOUT-CHECKLIST.md'yi aç ve her maddeyi (lokal simülasyon "
                    "kapsamında) kontrol et.",
                ]),
            ],
        },
    ],

    # =========================================================================
    # PROMPTS
    # =========================================================================
    "prompts": [
        {
            "title": "Enterprise CLAUDE.md Şablonu",
            "prompt": (
                "Bu proje için enterprise-grade bir CLAUDE.md şablonu oluştur. "
                "Şablonda şunlar olsun: proje metadatası (placeholder), coding standards, "
                "security policy, model/effort guidance (default: sonnet, high; review: opus), "
                "yasaklı eylemler. Toplam 2000-2500 karakter."
            ),
        },
        {
            "title": "Security Reviewer Agent",
            "prompt": (
                ".claude/agents/security-reviewer.md oluştur. Frontmatter: name: "
                "security-reviewer, description: Güvenlik açıkları için kod inceler, "
                "tools: Read Grep Glob Bash, model: opus, effort: high. System prompt: "
                "Kıdemli güvenlik mühendisi — injection, auth, secrets, data handling."
            ),
        },
        {
            "title": "Deployment Checklist Skill",
            "prompt": (
                ".claude/skills/deployment-checklist/SKILL.md oluştur. Frontmatter: "
                "description: Deploy öncesi kontrol listesi. İçerik: test suite geçiyor mu, "
                "lint temiz mi, env variables tanımlı mı, secrets güvende mi, migration "
                "çalıştırıldı mı, rollback planı var mı."
            ),
        },
        {
            "title": "Maliyet Strateji Raporu",
            "prompt": (
                "/usage çıktımı analiz et. Şu soruları yanıtla: (1) En çok token "
                "tüketen bileşen hangisi? (2) Model/effort kombinasyonu optimal mi? "
                "(3) Takımım için aylık tahmini maliyet ne olur? (4) Hangi "
                "optimizasyonları önerirsin?"
            ),
        },
        {
            "title": "Plugin Marketplace Oluştur",
            "prompt": (
                "team-claude-code-starter-kit/ dizinindeki bileşenleri bir plugin "
                "marketplace olarak paketle. marketplace.json ve plugin.json oluştur. "
                "/plugin validate ile doğrula. Hata varsa düzelt."
            ),
        },
        {
            "title": "Onboarding Rehberi",
            "prompt": (
                "Yeni bir takım üyesi için Claude Code onboarding rehberi yaz "
                "(ONBOARDING.md). Adımlar: kurulum, auth, starter kit kurulumu, "
                "ilk session (security-reviewer ile kod taraması), /usage ile "
                "maliyet farkındalığı."
            ),
        },
    ],

    # =========================================================================
    # CHALLENGE
    # =========================================================================
    "challenge": {
        "title": "Enterprise Team Starter Kit — Paketleme ve Doğrulama",
        "task": (
            "Bugün oluşturduğun tüm bileşenleri (CLAUDE.md şablonu, 3 agent, "
            "2 skill, 3 command, 2 hook) bir plugin marketplace olarak paketle, "
            "lokal olarak yayınla, yeni bir projede kur ve çalıştığını doğrula."
        ),
        "requirements": [
            "marketplace.json ve plugin.json doğru path'lerde ve /plugin validate ile hatasız",
            "/plugin marketplace add ve /plugin install ile başarıyla kurulabilir",
            "Yeni bir projede en az 1 agent çağrılabiliyor, 1 skill tetiklenebiliyor, "
            "1 hook çalışıyor",
            "README.md kurulum talimatlarını içeriyor",
            "ONBOARDING.md yeni üye rehberi olarak hazır",
            "ROLLOUT-CHECKLIST.md admin perspektifinden doldurulmuş",
        ],
        "success": [
            "Plugin validate hatasız geçiyor",
            "Başka projede kit kuruldu ve agent/skill/hook çalıştı",
            "README, ONBOARDING ve ROLLOUT-CHECKLIST tamamlandı",
        ],
        "bonus": [
            "examples/ dizininde managed-settings, managed-mcp ve sandbox-policy "
            "sample dosyaları da var ve her birinin 'gerçek deploy' vs 'lokal sim' "
            "ayrımı README'de açıklanmış",
            "Kit'i bir Git repo'suna push et ve /plugin marketplace add owner/repo "
            "ile remote marketplace olarak test et",
        ],
        "solution": {
            "intro": (
                "Challenge tek seferde değil, adım adım çözülmelidir. "
                "Deliverable yapısı bu gün boyunca Bölüm 2'de oluşturulmuştur; "
                "şimdi son doğrulamayı yapıyoruz."
            ),
            "prompts": [
                {
                    "title": "Yapıyı Kontrol Et",
                    "prompt": (
                        "team-claude-code-starter-kit/ dizininin yapısını göster. "
                        "Şu dosyaların var olduğunu doğrula: "
                        ".claude-plugin/marketplace.json, "
                        "plugins/team-starter-kit/.claude-plugin/plugin.json, "
                        "plugins/team-starter-kit/agents/ (3 dosya), "
                        "plugins/team-starter-kit/skills/ (2 dizin), "
                        "plugins/team-starter-kit/hooks/ (2 dosya), "
                        "plugins/team-starter-kit/commands/ (3 dosya), "
                        "README.md, ONBOARDING.md, ROLLOUT-CHECKLIST.md"
                    ),
                },
                {
                    "title": "Validate ve Kur",
                    "prompt": (
                        "/plugin validate . çalıştır. Hata varsa düzelt. "
                        "Sonra /plugin marketplace add ./ ve "
                        "/plugin install team-starter-kit@team-tools ile kur."
                    ),
                },
                {
                    "title": "Yeni Projede Test",
                    "prompt": (
                        "Yeni bir dizin oluştur (test-enterprise-project), git init yap, "
                        "kit'in security-reviewer agent'ını çağır, "
                        "deployment-checklist skill'ini tetikle, "
                        "bir Bash komutu ile hook'un çalışıp çalışmadığını test et."
                    ),
                },
            ],
            "notes": [
                "plugin.json path'i plugins/team-starter-kit/.claude-plugin/plugin.json "
                "olmalıdır — doğrudan plugin kökünde değil",
                "marketplace.json'daki plugin name ile plugin.json'daki name aynı olmalı",
                "Hook'ları test ederken kasıtlı olarak 'rm -rf /' gibi bir komut "
                "yazmayı dene — hook engellerse başarılı",
                "/plugin validate hata veriyorsa JSON syntax'ını ve path'leri kontrol et",
            ],
            "pitfalls": [
                "plugin.json'ı yanlış path'e koymak (plugin kökü vs .claude-plugin/ altı) — "
                "en sık yapılan hata",
                "marketplace.json'daki version ile plugin.json'daki version'ı farklı yazmak — "
                "plugin.json her zaman önceliklidir",
                "Hook exit code'unu yanlış kullanmak: 0 = izin ver, 2 = engelle. "
                "1 veya başka kod = hook hatası ama komut engellenmez",
                "Managed-mcp.json'ı .claude/settings.json'a yazmaya çalışmak — "
                "bu dosya ayrı bir mekanizmadır ve sistem path'ine deploy edilir",
            ],
        },
    },

    # =========================================================================
    # TAKEAWAYS
    # =========================================================================
    "takeaways": [
        "Enterprise Claude Code yönetişimi dört eksende döner: politika (managed settings), "
        "güvenlik (sandbox + MCP), maliyet (model/effort + observability) ve onboarding "
        "(kit + rehber)",

        "Settings precedence: Managed > CLI args > local > project > user. Server-managed "
        "settings client-side kontroldür; hard security boundary için sandbox ve managed MCP "
        "ile birleştirilmelidir",

        "Built-in sandboxed Bash yalnızca Bash komutlarını izole eder — file tools, MCP "
        "server'lar ve hooks aynı sınırda değildir. Tam süreç izolasyonu için container "
        "veya VM gerekir",

        "managed-mcp.json exclusive bir deploy aracıdır (admin yetkisi gerektirir, "
        "server-managed settings ile dağıtılamaz); allowedMcpServers/deniedMcpServers "
        "ise settings katmanlarında tanımlanabilen policy filtering kurallarıdır",

        "/usage lokal tahmindir, authoritative billing değildir. Maliyet gözlemlenebilirliği "
        "katmanlıdır: /usage → Console → Analytics → OTel → Gateway",

        "`availableModels` managed source tarafından set edildiğinde kullanıcı/proje scope'u "
        "genişletemez — 'settings'e model ekleyerek kısıtlamayı bypass ederim' yanılgısından "
        "kaçın",

        "ZDR standart Enterprise'da otomatik değildir; per-org etkinleştirme gerektirir. "
        "Team/Enterprise/API planlarında kod ve prompt'lar model eğitiminde kullanılmaz",

        "Team starter kit (CLAUDE.md + agents + skills + hooks → plugin marketplace) "
        "enterprise standardizasyonun temel deliverable'ıdır; olgunluk seviyesi arttıkça "
        "managed settings, OTel ve gateway katmanları eklenir",
    ],

    # =========================================================================
    # READING
    # =========================================================================
    "reading": {
        "official": [
            {
                "label": "Set up Claude Code for your organization — admin karar haritası, "
                         "managed settings, policy enforcement, monitoring seçenekleri",
                "url": "https://code.claude.com/docs/en/admin-setup",
            },
            {
                "label": "Configure server-managed settings — remote delivery, hourly poll, "
                         "tolerant parsing, cache mekanizması",
                "url": "https://code.claude.com/docs/en/server-managed-settings",
            },
            {
                "label": "Choose a sandbox environment — isolation spectrum karşılaştırması: "
                         "built-in sandbox, sandbox runtime, dev container, Docker, VM",
                "url": "https://code.claude.com/docs/en/sandbox-environments",
            },
            {
                "label": "Configure the sandboxed Bash tool — filesystem/network izolasyon, "
                         "allowWrite, allowedDomains, admin enforcement",
                "url": "https://code.claude.com/docs/en/sandboxing",
            },
            {
                "label": "Control MCP server access — managed-mcp.json, allowedMcpServers, "
                         "deniedMcpServers ve enterprise MCP stratejisi",
                "url": "https://code.claude.com/docs/en/managed-mcp",
            },
            {
                "label": "Manage costs effectively — /usage, spend limits, token azaltma "
                         "stratejileri, takım TPM önerileri",
                "url": "https://code.claude.com/docs/en/costs",
            },
            {
                "label": "Track team usage with analytics — dashboard, GitHub contribution "
                         "metrics, data export",
                "url": "https://code.claude.com/docs/en/analytics",
            },
            {
                "label": "Data usage — retention politikaları, ZDR, telemetry opt-out, "
                         "Claude Code on Web veri akışı",
                "url": "https://code.claude.com/docs/en/data-usage",
            },
            {
                "label": "Monitoring — OpenTelemetry export, per-skill/agent/plugin cost "
                         "attribution, OTEL_LOG_TOOL_CONTENT",
                "url": "https://code.claude.com/docs/en/monitoring-usage",
            },
            {
                "label": "Create and distribute a plugin marketplace — marketplace.json, "
                         "plugin.json, validate, host ve distribute akışı",
                "url": "https://code.claude.com/docs/en/plugin-marketplaces",
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
                "label": "Securely deploying AI agents — isolation, credential management, "
                         "network controls için derinlemesine güvenlik rehberi",
                "url": "https://code.claude.com/docs/en/agent-sdk/secure-deployment",
            },
        ],
    },

    # =========================================================================
    # NEXT PREVIEW
    # =========================================================================
    "next_preview": (
        "Yarın (Gün 20) eğitimin final projesi: Mikro-servis mimarisinde enterprise "
        "capstone. Agent Teams ve Dynamic Workflows ile paralel geliştirme, tüm "
        "kit/plugin/hook'ları canlı projede uygulama, Artifacts ile sonucu paylaşma "
        "ve kendi Claude Code Playbook'unu yazma."
    ),

    # =========================================================================
    # CHECKLIST
    # =========================================================================
    "checklist": [
        "Settings precedence sırasını (Managed > CLI > local > project > user) "
        "açıklayabiliyorum ve server-managed settings'in client-side control "
        "olduğunu, hard security boundary olmadığını biliyorum",

        "`availableModels` ve `enforceAvailableModels` farkını açıklayabilirim; "
        "managed source'un bu listeyi kullanıcı/proje scope'undan genişletmeye "
        "izin vermediğini biliyorum",

        "Sandbox spectrum'undaki 5 katmanı (sandboxed Bash → sandbox runtime → "
        "dev container → Docker → VM) ve her birinin neyi izole ettiğini / "
        "etmediğini biliyorum",

        "Built-in sandbox'ın sadece Bash komutlarını sınırladığını; file tools, "
        "MCP ve hooks'un izole olmadığını biliyorum",

        "`managed-mcp.json` (fixed set, admin deploy) ile `allowedMcpServers` / "
        "`deniedMcpServers` (policy filtering, settings katmanları) farkını "
        "açıklayabilirim",

        "ZDR'ın standart Enterprise'da otomatik olmadığını, per-org account team "
        "tarafından etkinleştirildiğini biliyorum",

        "/usage ana komutunu çalıştırdım, breakdown'ı okudum; /cost ve /stats'ın "
        "alias olduğunu biliyorum; estimate vs authoritative billing ayrımını "
        "yapabiliyorum",

        "Team starter kit oluşturdum: CLAUDE.md şablonu + 3 agent + 2 skill + "
        "3 command + 2 hook",

        "Kit'i plugin marketplace formatında paketledim (.claude-plugin/marketplace.json "
        "+ plugins/.../\\.claude-plugin/plugin.json) ve /plugin validate ile doğruladım",

        "Kit'i /plugin marketplace add ve /plugin install ile kurdum; başka bir "
        "projede agent/skill/hook çalıştığını test ettim",

        "ONBOARDING.md ve ROLLOUT-CHECKLIST.md yazdım",

        "Enterprise anti-pattern'leri (büyük CLAUDE.md, sandbox'suz bypass, tek "
        "model herkes için, denetimsiz MCP) listeleyebilir ve çözüm önerebilirim",
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
    chk("day == 19", L["day"] == 19)
    chk("total_days == 20", L["total_days"] == 20)
    chk("week == 4", L["week"] == 4)
    chk("slug present", bool(L["slug"]))
    chk("title present", bool(L["title"]))
    chk("tagline present", bool(L["tagline"]))
    chk("intro present", bool(L["intro"]))

    chk("flow >= 4 phases", len(L["flow"]) >= 4)
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
