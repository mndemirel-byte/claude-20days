# content/gun17.py
# Tek kaynak: LESSON sözlüğü. generators/render_html.py ve generators/render_json.py
# bu sözlükten HTML + JSON üretir.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table


LESSON = {
    "day": 17,
    "total_days": 20,
    "week": 4,
    "slug": "agent-teams-dynamic-workflows",
    "title": "Agent Teams & Dynamic Workflows",
    "tagline": "Claude'ların takımını kur, team lead'i de Claude olsun",
    "tier": None,
    "date_label": "Temmuz 2026",

    "intro": (
        "Gün 16'da paralelliğin koordinasyonunu sen yapıyordun: worktree açtın, agent view'dan "
        "dispatch/peek/attach ettin. Bugün koordinasyonu Claude'a devrediyorsun. İki farklı "
        "yaklaşımı derinlemesine göreceksin: Agent Teams'te bir 'team lead' Claude, birbiriyle "
        "konuşan teammate'lere görev dağıtır; Dynamic Workflows'ta ise Claude'un yazdığı bir "
        "script, onlarca-yüzlerce subagent'ı arka planda orkestre eder. İkisinin de cevapladığı "
        "soru aynı değil: 'planı kim tutuyor?' Bugünün sonunda SaaS Dashboard'da bir takıma "
        "review yaptırmış, bir workflow ile codebase denetimi çalıştırmış ve hangi görevi hangi "
        "katmana vereceğine bilinçli karar verebilir olacaksın."
    ),

    "flow": [
        {"phase": "1 · Teorik: İki Orkestrasyon Katmanı", "dur": "30 dk",
         "desc": "Agent Teams mimarisi, Dynamic Workflows mimarisi, ultracode'un iki mekanizması, 5 katmanlı karar tablosu"},
        {"phase": "2 · Pratik: Agent Teams", "dur": "40 dk",
         "desc": "Takımı etkinleştir, dosya sahipliğiyle 3 teammate spawn et, task list + mailbox'ı gözlemle, shutdown akışı"},
        {"phase": "3 · Pratik: Dynamic Workflows", "dur": "45 dk",
         "desc": "ultracode ile bir audit workflow'u tetikle, /workflows ile izle, script'i incele, komut olarak kaydet"},
        {"phase": "4 · Mini Challenge", "dur": "35 dk",
         "desc": "SaaS Dashboard'a 3 bağımsız feature: biri worktree+subagent, biri Agent Teams, biri Dynamic Workflow ile"},
    ],

    "prerequisites": [
        "Gün 1-16 tamamlanmış: worktrees ve agent view (Gün 16), subagent'lar (Gün 11), rol "
        "agent'ları (Gün 15), SaaS Dashboard projesi git repository'si olarak init edilmiş",
        "Claude Code güncel sürümde (Agent Teams için v2.1.178+, Dynamic Workflows için "
        "v2.1.154+ önerilir — `claude --version` ile kontrol et)",
        "Pro, Max, Team veya Enterprise plan / Console hesabı — Dynamic Workflows'un "
        "kullanılabilirliği plana göre değişir, `/config`'ten kontrol edilmeli",
    ],
    "tools_needed": [
        "Terminal (Claude Code çalışır durumda)",
        "tmux veya iTerm2 (opsiyonel — Agent Teams'te split-pane görünüm için)",
        "Git (worktree ve branch tabanlı koordinasyon için)",
        "VS Code veya tercih edilen editör",
    ],

    "objectives": [
        "Agent Teams mimarisini (team lead + teammate, shared task list, mailbox) ve deneysel "
        "durumunu (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`, varsayılan kapalı) açıklayabileceksin",
        "Doğal dille bir takım isteyip, dosya sahipliği net ayrılmış teammate'ler spawn "
        "edebilecek; task list ve doğrudan mesajlaşmayı takip edebileceksin",
        "Dynamic Workflow'un 'planı script'in tuttuğu' bir orkestrasyon katmanı olduğunu, "
        "Claude'un yazdığı script'teki `agent()`/`pipeline()` çağrılarını okuyup "
        "yorumlayabileceksin",
        "`ultracode` anahtar kelimesi (tek görev) ile `/effort ultracode` (oturum geneli) "
        "arasındaki farkı ayırt edip doğru olanı seçebileceksin",
        "`/workflows` ile bir run'ı izleyip 'Large workflow' uyarısını (25 agent / 1.5M token "
        "eşiği) yorumlayabileceksin",
        "Skill / Subagent / Agent View+Worktree / Agent Teams / Dynamic Workflow katmanları "
        "arasında 'planı kim tutuyor, işçiler birbirine konuşuyor mu' eksenlerinde doğru "
        "katmanı seçebileceksin",
        "SaaS Dashboard'da bir review görevini Agent Teams'e, bir denetim görevini Dynamic "
        "Workflow'a verip sonuçları değerlendirebileceksin",
    ],

    # =========================================================================
    # SECTIONS
    # =========================================================================
    "sections": [
        # ── BÖLÜM 1: TEORİK TEMEL ──────────────────────────────────────────
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                h("1.1 Agent Teams: Team Lead + Teammate Mimarisi"),
                p(
                    "Agent Teams, birden fazla Claude Code oturumunun bir arada, birbirleriyle "
                    "konuşarak çalışmasını sağlar. İlk teammate spawn edildiğinde bir takım "
                    "oluşur; o anki oturum otomatik olarak 'team lead' rolünü üstlenir. Lead "
                    "işi parçalara böler, görev atar ve sonuçları senteze dönüştürür. "
                    "Teammate'ler ise bağımsız çalışır: her biri kendi context window'una "
                    "sahiptir ve doğrudan birbirleriyle mesajlaşabilir."
                ),
                p(
                    "Her teammate, tam ve bağımsız bir Claude Code session'ıdır. Spawn "
                    "edildiğinde proje context'ini (CLAUDE.md, MCP server'lar, skill'ler) "
                    "otomatik yükler — ama lead'in konuşma geçmişini **almaz**. Sadece spawn "
                    "prompt'uyla işe başlar. Bu yüzden teammate'e verdiğin görev talimatı "
                    "kendi başına yeterli olmalı: dosya yolları, teknoloji yığını, ne aranacağı, "
                    "beklenen çıktı formatı."
                ),
                keypoint(
                    "Teammate spawn iki şekilde olur: sen açıkça istersin ('3 teammate ile "
                    "şunu incele') veya Claude görevin paralel çalışmadan fayda göreceğini "
                    "düşünüp önerir. Her iki durumda da senin onayınla gerçekleşir."
                ),

                h("1.2 Etkinleştirme ve Deneysel Durum"),
                p(
                    "Agent Teams Temmuz 2026 itibarıyla hâlâ **deneysel** bir özellik ve "
                    "varsayılan olarak **kapalıdır**. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` "
                    "değişkeni set edilmeden hiçbir takım kurulmaz, takım dizini yazılmaz, "
                    "Claude teammate spawn etmez veya önermez. İki yerden açabilirsin:"
                ),
                table(
                    ["Yöntem", "Nasıl", "Ne zaman tercih edilir"],
                    [
                        ["Shell environment", "`export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`", "Tek oturumluk / geçici deneme"],
                        ["settings.json", "`{\"env\": {\"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS\": \"1\"}}`", "Proje genelinde kalıcı, takım arkadaşlarıyla paylaşılabilir"],
                    ]
                ),
                warn(
                    "Resmi dokümanda spesifik bir model şartı belirtilmiyor — ama Agent Teams "
                    "deneysel bir özellik olduğu için bilinen sınırlamaları var: in-process "
                    "teammate'ler `/resume` veya `/rewind` ile geri gelmez; task status bazen "
                    "gecikir (tamamlanan görev 'completed' işaretlenmeyebilir); shutdown yavaş "
                    "olabilir; bir session'da tek takım kurulabilir; teammate'ler kendi "
                    "teammate'lerini doğuramaz (nested team yok)."
                ),

                h("1.3 Task List, Mailbox ve Plan Onayı"),
                p(
                    "Takımın koordinasyonu iki mekanizmaya dayanır: paylaşılan **task list** "
                    "(bağımlılıklı görevler, her teammate kendi görevini claim eder) ve "
                    "**mailbox** (doğrudan mesaj veya tüm takıma broadcast). Broadcast'i "
                    "tutumlu kullan — maliyet takım büyüklüğüyle orantılı artar."
                ),
                p(
                    "Bir teammate 'plan' modunda spawn edilirse salt-okunur çalışır: kod "
                    "tabanını inceler, bir yaklaşım tasarlar ama hiçbir değişiklik yapmadan "
                    "planını lead'e onaya sunar. Lead planı onaylar veya gerekçeli reddeder; "
                    "reddedilirse teammate planı revize edip yeniden sunar. Onaydan sonra "
                    "teammate implementasyona geçer."
                ),
                tip(
                    "Lead'in onay kararını yönlendirmek istiyorsan prompt'una kriter ekle: "
                    "'sadece test kapsamı içeren planları onayla' veya 'veritabanı şemasını "
                    "değiştiren planları reddet' gibi."
                ),

                h("1.4 Subagent'lardan Farkı"),
                p(
                    "Gün 11'deki subagent'lar ile Agent Teams'i karıştırmamak önemli. İkisi de "
                    "paralelliği sağlar ama koordinasyon şekli tamamen farklıdır:"
                ),
                table(
                    ["Özellik", "Subagent", "Agent Teams"],
                    [
                        ["Çalıştığı yer", "Ana konuşmanın içinde, izole context", "Bağımsız, tam Claude Code session'ları"],
                        ["Birbirleriyle konuşurlar mı?", "Hayır — sadece ana agent'a rapor eder", "Evet — doğrudan mesajlaşır, task claim eder"],
                        ["Ne zaman tercih edilir", "Hızlı, odaklı, rapor eden işçi yeterliyse", "Bulgular paylaşılmalı, birbirini sorgulamalıysa"],
                        ["Maliyet", "Görece düşük", "Her teammate tam context window — yüksek"],
                    ]
                ),

                h("1.5 Dynamic Workflows: Planı Script Tutar"),
                p(
                    "Subagent, Agent View ve Agent Teams'te koordinasyonu hep Claude (veya sen) "
                    "turn-by-turn yapar: her adımda ne spawn edileceğine karar verilir ve her "
                    "sonuç bir context window'a düşer. Dynamic Workflow bu modeli tersine "
                    "çevirir: Claude, görev için bir **JavaScript script** yazar; bu script "
                    "planı, döngüyü, dallanmayı ve ara sonuçları kendi içinde tutar. Senin "
                    "context'ine sadece final rapor düşer."
                ),
                p(
                    "Script içinde iki temel çağrı kullanılır: `agent()` tek bir subagent "
                    "çalıştırır, `pipeline()` bir listedeki her öğe için bir agent çalıştırıp "
                    "sonuçları toplar. Bu bölümde script'i **sen yazmayacaksın** — Claude yazar, "
                    "sen okuyup hangi dosya kümesine hangi agent'ın gittiğini izleyecek, "
                    "beğendiğin bir run'ı komut olarak kaydedeceksin."
                ),
                keypoint(
                    "Planı koda taşımanın faydası sadece daha fazla agent çalıştırmak değil: "
                    "bir workflow, bağımsız agent'ları birbirinin bulgusunu çapraz kontrol "
                    "ettirebilir (adversarial review) veya aynı planı birkaç farklı açıdan "
                    "taslaklatıp karşılaştırabilir — tek context window'da elde edilmesi zor "
                    "bir güvenilirlik."
                ),

                h("1.6 İki `ultracode` Mekanizması"),
                p("`ultracode` kelimesi iki farklı, birbirinden bağımsız şeyi tetikler — ayrımı netleştirmek maliyet kontrolü için kritik:"),
                table(
                    ["Mekanizma", "Nasıl tetiklenir", "Kapsam"],
                    [
                        ["Prompt keyword", "Prompt'un içine `ultracode` kelimesini yazmak (veya 'bir workflow kullan' demek)", "Sadece o tek görevi workflow'a çevirir"],
                        ["`/effort ultracode`", "Oturum ayarını değiştirmek", "Oturumdaki **her** önemli görev için Claude otomatik workflow planlar (xhigh reasoning + otomatik orkestrasyon); session-only"],
                    ]
                ),
                warn(
                    "`/effort ultracode`'u açık unutmak, rutin küçük görevlerin bile workflow'a "
                    "dönüşmesine yol açar — bu token maliyetini gereksiz yere şişirir. Rutin işe "
                    "dönünce `/effort high`'a geri dön."
                ),

                h("1.7 Kullanılabilirlik ve Limitler"),
                p(
                    "Dynamic Workflows artık dokümante edilmiş, ana orkestrasyon katmanlarından "
                    "biri — ama kullanılabilirliği plan ve sürüme bağlı: Claude Code v2.1.154+ "
                    "gerekiyor, tüm paid plan'larda ve Anthropic API/Bedrock/Vertex/Foundry "
                    "üzerinde destekleniyor. Kendi ortamında açık olup olmadığını `/config`'ten "
                    "kontrol et — bazı planlarda ayarı sen açman gerekebilir."
                ),
                p("Somut limitler:"),
                bullets([
                    "Bir run'da en fazla **16 eşzamanlı agent** (makine kapasitesine göre daha az olabilir).",
                    "Run başına toplam **1000 agent** üst sınırı.",
                    "Bir workflow **25 agent**'ı aşarsa veya öngörülen token toplamı **1.5 milyonu** "
                    "geçerse, task panelindeki ilerleme satırında 'Large workflow' uyarısı çıkar "
                    "(v2.1.203+). Bu uyarı bilgilendirmedir — run'ı durdurmaz; seni `/workflows`'a yönlendirir.",
                    "`/config`'te bir size guideline (small/medium/large/unrestricted) belirlersen, "
                    "o kılavuzun agent sayısı 25'lik eşiğin yerine geçer.",
                ]),
                tip(
                    "`/workflows` her zaman çalışan ve tamamlanmış run'ları listeler; birini "
                    "seçip faz, agent sayısı ve token toplamını görebilir, gerekirse run'ı "
                    "oradan durdurabilirsin."
                ),

                h("1.8 Beş Katmanlı Karar Tablosu"),
                p(
                    "Gün 16'da worktree ve agent view'ı gördün. Bugün ekledğin iki katmanla "
                    "birlikte, Claude Code'daki tüm paralellik/orkestrasyon yüzeyi şöyle özetlenir:"
                ),
                table(
                    ["Katman", "Ne işe yarar?", "Planı kim tutar?", "Worker iletişimi"],
                    [
                        ["Skill", "Bir davranışı/uzmanlığı paketler — agent çalıştırma katmanı değildir", "Ana Claude", "Yok"],
                        ["Subagent (Gün 11)", "Tek oturum içinden uzman worker çağırır", "Ana Claude", "Parent'a rapor eder, birbirine konuşmaz"],
                        ["Agent View + Worktree (Gün 16)", "Kullanıcı bağımsız session'ları yönetir", "Kullanıcı (dispatch/peek/attach)", "Ayrı session'lar, birbirinden habersiz"],
                        ["Agent Teams", "Lead Claude görev dağıtır, teammate'ler koordine olur", "Lead Claude + shared task list", "Teammate'ler doğrudan mesajlaşır"],
                        ["Dynamic Workflow", "Script çok sayıda subagent'ı orkestre eder", "Workflow script", "Script üzerinden sonuç toplama/çapraz kontrol"],
                    ]
                ),
                keypoint(
                    "Skill'i bu tabloya 'agent çalıştıran' bir katman gibi değil, 'davranış "
                    "paketleyen' bir katman gibi oku — Gün 13'teki skill/subagent ayrımıyla "
                    "çelişmez, sadece spektrumun neresinde durduğunu netleştirir."
                ),
            ],
        },

        # ── BÖLÜM 2: PRATİK — ADIM ADIM ─────────────────────────────────
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                h("2.1 Agent Teams'i Etkinleştir"),
                steps([
                    "SaaS Dashboard proje dizinine gir.",
                    "Kalıcı olması için `.claude/settings.json` içine "
                    "`{\"env\": {\"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS\": \"1\"}}` ekle "
                    "(veya geçici denemek için shell'de `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`).",
                    "Oturumu yeniden başlat — takım araçları sadece başlangıçta yüklenir: `claude`.",
                    "Etkinleştirmeyi doğrula: teammate spawn isteyip Claude'un kabul ettiğini gözlemle "
                    "(reddederse env değişkeni okunmamış demektir).",
                ]),

                h("2.2 Dosya Sahipliğiyle İlk Takımı Spawn Et"),
                p(
                    "Rastgele 'birkaç agent aç' demek yerine, her teammate'in hangi dosyalara "
                    "dokunacağını baştan belirt. Bu, Gün 16'daki task partitioning kurallarının "
                    "Agent Teams'e uyarlanmış hâlidir."
                ),
                steps([
                    "SaaS Dashboard'da doğal dille bir takım iste: 'Auth modülünü 3 açıdan incele — "
                    "bir teammate güvenlik (src/auth/), bir teammate performans (API/query katmanı), "
                    "bir teammate test kapsamı (tests/) — sadece kendi alanına dokunsun, bulguları "
                    "birbirine bildirsin.'",
                    "Claude'un üç teammate spawn ettiğini agent panelinden gözlemle.",
                    "Lead'den beklenen çıktıyı netleştir: bulgu matrisi + risk sırası + merge önerisi.",
                ]),
                tip(
                    "Performans teammate'inin test-coverage teammate'ine 'şu endpoint'i yük "
                    "testine al' diye doğrudan mesaj göndermesi — Agent Teams'in subagent'tan "
                    "farkını en net gösteren andır: bulgu ana konuşmaya dönmeden teammate'ler "
                    "arasında akar."
                ),

                h("2.3 Task List ve Mesajlaşmayı Takip Et"),
                steps([
                    "Agent panelinde yukarı/aşağı ok tuşlarıyla bir teammate seç, Enter ile session'ını görüntüle.",
                    "`Ctrl+T` ile task list'i aç; hangi görevlerin kimde, hangi durumda (pending/in-progress/completed) olduğunu incele.",
                    "Bir teammate'e doğrudan mesaj gönder — örn. bulgusunu netleştirmesini iste.",
                    "Delegate mode'u (Shift+Tab) aç: lead'in kendi kodu yazmaya başlamasını değil, "
                    "sadece koordinasyona odaklanmasını sağlar.",
                ]),
                warn(
                    "Task status bazen gecikir — bir teammate işini bitirdiği hâlde görev "
                    "'completed' işaretlenmeyebilir, bu da ona bağımlı görevleri bloklar. Görev "
                    "takılı görünüyorsa işin gerçekten bitip bitmediğini kontrol et ve gerekirse "
                    "lead'den teammate'i dürtmesini iste."
                ),

                h("2.4 Takımı Kapat"),
                p(
                    "Agent Teams'te ayrı bir 'temizlik' komutu yoktur. Lead teammate'lere bir "
                    "shutdown isteği gönderir; teammate mevcut işini bitirip onaylar (ya da "
                    "gerekçeyle reddeder). Session sona erdiğinde takımın paylaşılan dizinleri "
                    "**otomatik** temizlenir — ayrı bir cleanup adımı gerekmez."
                ),
                steps([
                    "Lead'den takımı kapatmasını iste: 'İşiniz bittiyse teammate'leri kapat.'",
                    "Shutdown'ın hemen değil, her teammate mevcut tool call'unu bitirdikten sonra "
                    "gerçekleştiğini gözlemle (yavaş olabilir, sabırlı ol).",
                    "Oturumu normal şekilde `/exit` ile kapat — paylaşılan dizinler otomatik silinir.",
                ]),
                tip(
                    "Terminal çöker veya bağlantı koparsa arkada bir tmux session'ı kalabilir. "
                    "`tmux ls` ile listele, `tmux kill-session -t <isim>` ile temizle — bu, "
                    "normal shutdown akışının dışında kalan tek troubleshooting adımıdır."
                ),

                h("2.5 İlk Dynamic Workflow'u Tetikle"),
                p(
                    "İlk workflow denemesini bilinçli olarak güvenli bir görevle başlat: dosya "
                    "değiştirmeyen, sadece **denetim yapan (audit)** bir görev. Migration gibi "
                    "yazma-ağırlıklı görevleri daha sonraya bırak."
                ),
                steps([
                    "SaaS Dashboard'da şu prompt'u çalıştır: 'ultracode: SaaS Dashboard'daki tüm "
                    "route'larda auth kontrolünün tutarlı uygulandığını denetle — hangi "
                    "endpoint'lerde middleware eksik, hangilerinde farklı bir pattern kullanılmış, listele.'",
                    "Claude'un görevi bir workflow'a çevirdiğini onay kartından (Desktop) veya "
                    "session mesajından gözlemle.",
                    "`/workflows` komutunu çalıştır, run'ı seç ve ilerleme görünümünü aç.",
                ]),

                h("2.6 Run'ı İzle ve Script'i Oku"),
                steps([
                    "İlerleme görünümünde her fazın agent sayısını, token toplamını ve geçen "
                    "süreyi incele.",
                    "Bir faza gir (drill down) ve o fazdaki agent'lardan birinin ne bulduğunu oku.",
                    "Claude'un yazdığı script dosyasını aç; `agent()` ve `pipeline()` çağrılarının "
                    "hangi dosya kümesine hangi görevi verdiğini takip et — script'i **değiştirmeyeceksin**, "
                    "sadece orkestrasyonun mantığını anlayacaksın.",
                    "Run tamamlandığında session'a düşen final raporu oku: her bulgu hangi "
                    "kaynaktan geldi, hangi iddialar çapraz kontrolü geçemedi.",
                ]),

                h("2.7 Sonucu Küçük Bir Patch'e Dönüştür ve Kaydet"),
                steps([
                    "Raporda öncelikli bulunan 1-2 endpoint için Claude'dan düzeltme patch'i iste "
                    "(bu artık workflow değil, normal bir oturum adımıdır).",
                    "Patch'i test et, commit et.",
                    "Beğendiğin workflow'u tekrar kullanmak için kaydet: `/workflows` → çalışan/biten "
                    "run'ı seç → `s` tuşu → `.claude/workflows/` (proje geneli, takımla paylaşılır) "
                    "veya `~/.claude/workflows/` (kişisel).",
                    "Kaydedilen workflow artık `/` otomatik tamamlamasında bir komut olarak görünür "
                    "— bir dahaki denetimde yeniden yazmana gerek kalmaz.",
                ]),
            ],
        },

        # ── BÖLÜM 3: PRATİK DERİNLEŞ ──────────────────────────────────────
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK DERİNLEŞ",
            "blocks": [
                h("3.1 Üç Katmanı Yan Yana Kullanmak"),
                p(
                    "Şimdiye kadar üç farklı paralellik katmanını gördün: worktree+subagent "
                    "(Gün 16), Agent Teams ve Dynamic Workflows. Bu bölümde SaaS Dashboard'a "
                    "3 bağımsız feature ekleyerek üçünü aynı projede, bilinçli bir seçimle "
                    "kullanacaksın — challenge'ın kendisi budur."
                ),
                table(
                    ["Görev tipi", "Önerilen katman", "Neden"],
                    [
                        ["Tek, net sınırlı bir dosya değişikliği", "Worktree + subagent (Gün 16)", "Koordinasyon overhead'i gereksiz; hızlı ve ucuz"],
                        ["Birbirini sorgulaması gereken çok açılı bir inceleme (güvenlik+performans+test)", "Agent Teams", "Bulguların birbirine akması gerekiyor"],
                        ["Onlarca dosyada tekrarlanan bir denetim/tutarlılık kontrolü", "Dynamic Workflow", "Tek context window'a sığmayan ölçek; tekrarlanabilir script"],
                    ]
                ),
                keypoint(
                    "Karar kriteri hep aynı iki soru: (1) İşçiler birbirine konuşmalı mı? "
                    "(2) İş, tek context window'un rahatça tutabileceği ölçekte mi? Hayır/Evet "
                    "→ worktree+subagent; Evet/Evet → Agent Teams; Hayır/Hayır → Dynamic Workflow."
                ),

                h("3.2 Maliyet Farkındalığı"),
                p(
                    "Her katman farklı bir maliyet profiline sahiptir. Agent Teams'te her "
                    "teammate tam bir context window'dur — üç teammate, kabaca tek session'ın "
                    "birkaç katı token tüketebilir. Dynamic Workflows'ta agent sayısı "
                    "onlara-yüzlere çıkabildiği için toplam token daha da büyüyebilir; bu yüzden "
                    "25 agent/1.5M token eşiği bir uyarı olarak var."
                ),
                warn(
                    "Aynı dosyaya iki teammate'in (veya iki workflow agent'ının) yazması en "
                    "sık rastlanan hata sınıfıdır. Önlem Gün 16'dan tanıdık: net dosya "
                    "sahipliği + contract-first + küçük scope."
                ),
                warn(
                    "Büyük bir migration'ı hiç test etmeden doğrudan Dynamic Workflow'a vermek "
                    "riskli ve pahalıdır. Önce küçük bir slice ile (tek modül, tek dosya kümesi) "
                    "dene, sonucu doğrula, sonra ölçeği büyüt."
                ),
                warn(
                    "`/effort ultracode`'u kapatmayı unutup rutin işe dönmek, her küçük görevi "
                    "gereksiz yere workflow'a çevirir. Session bitmeden `/effort high`'a dön."
                ),
            ],
        },
    ],

    # =========================================================================
    # PROMPTS
    # =========================================================================
    "prompts": [
        {
            "title": "Agent Team Spawn: Çok Açılı Code Review",
            "prompt": (
                "Auth modülünü (src/auth/) 3 açıdan incele. Üç teammate spawn et: "
                "1) security-reviewer — token handling, session yönetimi, input validation, "
                "sadece src/auth/ dosyalarına bakar. 2) performance-reviewer — query ve API "
                "katmanındaki gecikme kaynaklarını arar, sadece backend/api/ dosyalarına bakar. "
                "3) test-coverage-reviewer — eksik test senaryolarını listeler, sadece tests/ "
                "dizinine bakar. Her teammate sadece kendi alanına dokunsun, bulgularını "
                "birbirine bildirsin. Sonunda bana bulgu matrisi + risk sırası + merge önerisi getir."
            ),
            "note": "Agent Teams etkinleştirildikten sonra çalıştır. Dosya sahipliğini prompt'ta açıkça belirtmek conflict riskini azaltır.",
        },
        {
            "title": "Task Partitioning: Takım İçi Bağımlılıklar",
            "prompt": (
                "Bu görevi takım içinde bağımlılıklı görevlere böl. Her görev için: hangi "
                "teammate sorumlu, hangi dosyalara dokunacak, hangi görev tamamlanmadan "
                "başlayamaz, kabul kriteri ne. Aynı dosyaya iki teammate'in yazmasını engelle."
            ),
            "note": "Takımı spawn etmeden önce bu prompt'la planı netleştir.",
        },
        {
            "title": "Dynamic Workflow: Codebase Denetimi (Audit)",
            "prompt": (
                "ultracode: SaaS Dashboard'daki tüm route'larda auth kontrolünün tutarlı "
                "uygulandığını denetle. Her endpoint için middleware'in var olup olmadığını, "
                "varsa hangi pattern'i kullandığını kontrol et. Eksik veya tutarsız olanları "
                "önem sırasına göre listele. Hiçbir dosyayı değiştirme, sadece rapor üret."
            ),
            "note": "İlk workflow denemesi için yazma yapmayan bir audit görevi seç — migration gibi riskli işleri daha sonraya bırak.",
        },
        {
            "title": "Workflow Sonucunu Komuta Dönüştürme",
            "prompt": (
                "Az önce çalışan auth-tutarlılık denetim workflow'unu tekrar kullanılabilir "
                "bir komut olarak kaydetmek istiyorum. `.claude/workflows/` altına, proje "
                "genelinde paylaşılacak şekilde kaydet ve kısa bir kullanım notu ekle."
            ),
            "note": "`/workflows` üzerinden `s` tuşuyla da yapılabilir; bu prompt Claude'a doğrudan istekle aynı işi yaptırır.",
        },
    ],

    # =========================================================================
    # CHALLENGE
    # =========================================================================
    "challenge": {
        "title": "CHALLENGE: SaaS Dashboard'a 3 Bağımsız Feature — Üç Farklı Orkestrasyon Katmanı",
        "task": (
            "SaaS Dashboard'a birbirinden bağımsız 3 küçük iyileştirme ekleyeceksin. Her "
            "birini farklı bir katmanla geliştir: biri worktree+subagent (Gün 16), biri Agent "
            "Teams, biri Dynamic Workflow ile. Amaç sadece feature'ları tamamlamak değil, hangi "
            "katmanı ne zaman seçeceğine dair gerekçeli bir karar vermek."
        ),
        "requirements": [
            "Feature 1 (worktree+subagent): küçük, net sınırlı bir iyileştirme — örn. bir "
            "endpoint'e input validation eklemek. `claude -w` ile izole worktree'de geliştir.",
            "Feature 2 (Agent Teams): birden fazla açıdan bakılması gereken bir görev — örn. "
            "yeni bir 'export data' endpoint'ini güvenlik + performans açısından incelettirip "
            "geliştirt. En az 2 teammate spawn et, dosya sahipliğini ayır.",
            "Feature 3 (Dynamic Workflow): tekrarlanan bir denetim/tutarlılık kontrolü — örn. "
            "tüm API response'larının hata formatının tutarlı olup olmadığını denetle, bulunan "
            "1-2 sorunu küçük bir patch ile düzelt.",
            "Her feature için hangi katmanı neden seçtiğini bir cümleyle not et.",
            "Agent Teams'te takımı düzgün kapat (shutdown isteği); Dynamic Workflow'u "
            "`/workflows`'tan izle.",
        ],
        "success": [
            "Üç feature de tamamlandı ve doğru katmanla geliştirildi",
            "Worktree feature'ı ayrı branch'te, temiz bir commit ile bitti",
            "Agent Teams feature'ında en az 2 teammate net dosya sahipliğiyle çalıştı, bulgular "
            "birbirine iletildi",
            "Dynamic Workflow feature'ında `/workflows` ile run izlendi, sonuç küçük bir "
            "patch'e dönüştürüldü",
            "Her feature için katman seçim gerekçesi yazılı olarak belirtildi",
            "Agent Teams session'ı temiz şekilde kapatıldı (orphaned tmux session kalmadı)",
        ],
        "bonus": [
            "Dynamic Workflow'u `.claude/workflows/` altına komut olarak kaydet ve ikinci bir "
            "denetimde yeniden kullan.",
            "Agent Teams'te bir teammate'i 'plan' modunda spawn edip lead'in onay/red akışını dene.",
            "Aynı görevi bilerek yanlış katmanla dene (ör. tek dosyalık bir düzeltmeyi Agent "
            "Teams'e ver) ve maliyet/hız farkını gözlemleyip not al.",
        ],
        "solution": {
            "intro": (
                "Bu challenge üç katmanı aynı projede, art arda kullanmanı sağlar. Sıra "
                "önemlidir: önce en ucuz katmandan (worktree+subagent) başla, sonra "
                "koordinasyon gerektiren işe (Agent Teams) geç, en sona ölçek gerektiren "
                "denetimi (Dynamic Workflow) bırak."
            ),
            "prompts": [
                {
                    "title": "1) Worktree + Subagent Feature",
                    "prompt": (
                        "claude -w input-validation komutuyla worktree aç. Ardından: "
                        "'/api/reports endpoint'ine input validation ekle — tarih aralığı ve "
                        "sayfa numarası parametrelerini doğrula, hatalı girişte 400 ve açık "
                        "hata mesajı dön. Testini yaz ve çalıştır. Commit et.'"
                    ),
                },
                {
                    "title": "2) Agent Teams Feature",
                    "prompt": (
                        "'export data' endpoint'ini ekleyeceğim. Bir güvenlik teammate (rate "
                        "limiting ve yetkilendirme kontrolü, sadece backend/export/ dosyalarına "
                        "dokunur) ve bir performans teammate (büyük veri setlerinde streaming "
                        "response, sadece aynı dizine dokunur) spawn et. İkisi bulgularını "
                        "paylaşıp ortak bir implementasyon planında anlaşsın, sonra "
                        "uygulasınlar."
                    ),
                },
                {
                    "title": "3) Dynamic Workflow Feature",
                    "prompt": (
                        "ultracode: Tüm API endpoint'lerinin hata response formatını denetle "
                        "— aynı { error, code, message } şemasını kullanıyorlar mı? Tutarsız "
                        "olanları listele, hiçbir dosyayı değiştirme."
                    ),
                },
                {
                    "title": "4) Workflow Sonucunu Patch'e Dönüştürme",
                    "prompt": (
                        "Denetim raporundaki en öncelikli 2 tutarsızlığı düzelt: response "
                        "formatlarını ortak şemaya çevir, testleri çalıştır, commit et."
                    ),
                },
            ],
            "notes": [
                "Worktree feature'ı en ucuz ve en hızlı olduğu için önce bitirmek, sonraki iki "
                "katmanın maliyetini daha rahat gözlemlemeni sağlar.",
                "Agent Teams'te teammate'lerin 'ortak bir planda anlaşması' istendiğinde, lead "
                "bulguları senteze dönüştürüp tek bir implementasyon kararına varır.",
                "Dynamic Workflow'un raporu değişiklik yapmadan geldiği için, patch'i ayrı bir "
                "adımda (workflow dışında) uygulaman gerekir — bu bilinçli bir güvenlik sınırıdır.",
                "`/workflows` ve agent panelini (Agent Teams için) yan yana açık tutmak, hangi "
                "katmanın ne kadar sürdüğünü karşılaştırmanı kolaylaştırır.",
            ],
            "pitfalls": [
                "Agent Teams'te dosya sahipliğini belirtmemek → İki teammate aynı dosyaya "
                "yazar, merge conflict kaçınılmaz olur.",
                "Dynamic Workflow'dan doğrudan dosya değişikliği beklemek → Workflow rapor "
                "üretir; patch ayrı bir adımdır.",
                "İlk workflow denemesini büyük bir migration ile yapmak → Token maliyeti "
                "sürpriz olur; küçük audit ile başla.",
                "Agent Teams session'ını `/exit` yerine terminali kapatarak bitirmek → Orphaned "
                "tmux session kalabilir; `tmux ls` ile kontrol et.",
                "`/effort ultracode`'u açık unutmak → Rutin görevler bile workflow'a döner, "
                "maliyet artar.",
                "Worktree feature'ı için Agent Teams kurmak → Tek dosyalık iş için gereksiz "
                "koordinasyon overhead'i; katman seçimi göreve göre yapılmalı.",
            ],
        },
    },

    # =========================================================================
    # TAKEAWAYS
    # =========================================================================
    "takeaways": [
        "Agent Teams'te koordinasyonu Claude (team lead) yapar; Dynamic Workflows'ta "
        "koordinasyonu Claude'un yazdığı bir script yapar — 'planı kim tutuyor' sorusu iki "
        "katmanı ayıran temel eksendir.",
        "Agent Teams hâlâ deneysel ve varsayılan kapalı: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` "
        "ile açılır; teammate'ler tam context window'lu bağımsız session'lardır ve lead'in "
        "konuşma geçmişini almazlar.",
        "Subagent'lar sadece ana agent'a rapor eder; Agent Teams'te teammate'ler doğrudan "
        "birbirine mesaj atar ve paylaşılan task list'ten görev claim eder.",
        "Dynamic Workflow script'i `agent()`/`pipeline()` çağrılarıyla onlarca-yüzlerce "
        "subagent'ı orkestre eder; sen script'i yazmazsın, okur ve beğendiğini komut olarak "
        "kaydedersin.",
        "`ultracode` iki ayrı mekanizmadır: prompt içindeki kelime tek görevi workflow'a "
        "çevirir, `/effort ultracode` oturum geneli her önemli görevi otomatik workflow'a çevirir.",
        "Dynamic Workflows'ta somut limitler var: 16 eşzamanlı agent, run başına 1000 agent üst "
        "sınırı, 25 agent/1.5M token eşiğinde bilgilendirici 'Large workflow' uyarısı.",
        "Agent Teams'te ayrı bir cleanup adımı yoktur — session çıkışında paylaşılan dizinler "
        "otomatik temizlenir; orphaned tmux session'lar tek manuel troubleshooting durumudur.",
        "Katman seçimi iki soruya indirgenir: işçiler birbirine konuşmalı mı, iş tek context "
        "window'a sığar mı — cevaba göre worktree+subagent / Agent Teams / Dynamic Workflow "
        "arasında seçim yapılır.",
    ],

    # =========================================================================
    # READING
    # =========================================================================
    "reading": {
        "official": [
            {
                "label": "Orchestrate teams of Claude Code sessions — Agent Teams mimarisi, "
                         "etkinleştirme, task list, mailbox, shutdown ve known limitations",
                "url": "https://code.claude.com/docs/en/agent-teams",
            },
            {
                "label": "Orchestrate subagents at scale with dynamic workflows — script yapısı, "
                         "ultracode tetikleyicileri, limitler, /workflows kullanımı",
                "url": "https://code.claude.com/docs/en/workflows",
            },
            {
                "label": "Run agents in parallel — subagent, agent view, agent teams ve dynamic "
                         "workflows'u karşılaştıran resmi köprü sayfa",
                "url": "https://code.claude.com/docs/en/agents",
            },
            {
                "label": "Create custom subagents — teammate spawn prompt'larını tasarlarken "
                         "referans alınacak subagent tanımı",
                "url": "https://code.claude.com/docs/en/sub-agents",
            },
        ],
        "community": [],
        "extra": [],
    },

    # =========================================================================
    # NEXT PREVIEW
    # =========================================================================
    "next_preview": (
        "Yarın (Gün 18) Claude Code'u pipeline'ına ve takvimine sokuyorsun: headless mode "
        "(Agent SDK), GitHub Actions/GitLab CI entegrasyonu, otomatik PR review ve zamanlanmış "
        "Routines ile Claude'un bilgisayarın kapalıyken bile çalışmasını sağlayacaksın."
    ),

    # =========================================================================
    # CHECKLIST
    # =========================================================================
    "checklist": [
        "Agent Teams'i `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` ile (shell env veya "
        "settings.json) etkinleştirdim",
        "Dosya sahipliği net ayrılmış en az 2 teammate spawn ettim",
        "Task list'i `Ctrl+T` ile görüntüledim, en az bir teammate'e doğrudan mesaj gönderdim",
        "Agent Teams session'ını düzgün kapattım (shutdown isteği) ve orphaned tmux session "
        "kontrolü yaptım",
        "`ultracode` anahtar kelimesiyle veya doğal dille bir görevi Dynamic Workflow'a çevirdim",
        "`/workflows` ile run'ı izledim, en az bir fazın agent sayısı ve token toplamını inceledim",
        "Claude'un yazdığı workflow script'ini açıp `agent()`/`pipeline()` çağrılarını "
        "yorumladım (değiştirmedim)",
        "Workflow sonucunu küçük bir patch'e dönüştürüp commit ettim",
        "`ultracode` keyword ile `/effort ultracode` arasındaki farkı açıklayabiliyorum",
        "Skill / Subagent / Agent View+Worktree / Agent Teams / Dynamic Workflow arasında hangi "
        "görevi hangi katmana vereceğime karar verebiliyorum",
        "Challenge'ı tamamladım: 3 feature, 3 farklı katman, her biri için seçim gerekçesi yazılı",
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
    chk("day == 17", L["day"] == 17)
    chk("total_days == 20", L["total_days"] == 20)
    chk("week == 4", L["week"] == 4)
    chk("slug present", bool(L["slug"]))
    chk("title present", bool(L["title"]))
    chk("tagline present", bool(L["tagline"]))
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
