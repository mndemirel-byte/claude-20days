# content/gun16.py
# Tek kaynak: LESSON sözlüğü. generators/render_html.py ve generators/render_json.py
# bu sözlükten HTML + JSON üretir.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table


LESSON = {
    "day": 16,
    "total_days": 20,
    "week": 4,
    "slug": "paralel-calisma-agent-view-worktrees",
    "title": "Paralel Çalışma, Agent View ve Worktrees",
    "tagline": "Birden fazla Claude'u aynı anda çalıştır ve tek ekrandan yönet",
    "tier": "🟠 Kademe 3",
    "date_label": "Temmuz 2026",

    "intro": (
        "Gün 15'te her yazılım rolü için uzmanlaşmış agent'lar tanımladın. Bugün bu agent'ları "
        "ve Claude Code oturumlarını aynı anda çalıştırmayı öğreniyorsun. Tek bir terminal "
        "sekmesinde sırayla iş yapmak yerine, birden fazla worktree'de izole oturumlar açıp "
        "agent view ile hepsini tek ekrandan yöneteceksin. Günün sonunda SaaS Dashboard'a "
        "paralel olarak backend ve frontend feature ekleyip, contract-first bir workflow ile "
        "merge edeceksin — üstelik çakışma riski olmadan."
    ),

    "flow": [
        {"phase": "1 · Teorik: Paralellik Zihinsel Modeli", "dur": "35 dk",
         "desc": "Neden paralel çalışılır, worktree vs agent view, task partitioning kuralları, karar matrisi"},
        {"phase": "2 · Pratik: Worktrees ile İzolasyon", "dur": "40 dk",
         "desc": "--worktree / -w, .worktreeinclude, subagent worktree izolasyonu, cleanup"},
        {"phase": "3 · Pratik: Agent View", "dur": "45 dk",
         "desc": "claude agents, dispatch/peek/attach, claude --bg, /background, state okuma, pattern'ler"},
        {"phase": "4 · Mini Challenge", "dur": "30 dk",
         "desc": "SaaS Dashboard'a Usage Metrics feature'ı: backend + frontend + integration, paralel worktree'ler"},
    ],

    "prerequisites": [
        "Gün 1-15 tamamlanmış: Claude Code kurulu, subagent'lar (Gün 11), hooks (Gün 12), "
        "skill/plugin (Gün 13), SaaS Dashboard projesi başlatılmış (Gün 14), rol agent'ları (Gün 15)",
        "SaaS Dashboard projesi Git repository'si olarak init edilmiş (en az bir commit)",
        "Terminal ve Claude Code çalışır durumda (v2.1.139+ önerilir, agent view için)",
    ],
    "tools_needed": [
        "Terminal (Claude Code çalışır durumda)",
        "İkinci bir terminal sekmesi/penceresi (tmux, iterm2 split, VS Code terminal vb.)",
        "Git (worktree desteği için zorunlu)",
        "VS Code veya tercih edilen editör",
    ],

    "objectives": [
        "Worktrees, agent view, agent teams ve dynamic workflows arasındaki farkı — 'kim "
        "koordine ediyor, işçiler birbirine konuşuyor mu, aynı dosyaya mı yazıyorlar' "
        "eksenlerinde — açıklayabileceksin",
        "`--worktree` / `-w` flag'i ile izole git worktree'lerde oturum başlatabilecek; "
        "`.worktreeinclude` ile gitignored dosyaları otomatik taşıyabileceksin",
        "`claude agents` (agent view) ile arka plan oturumları dispatch edip tek ekrandan "
        "izleyebilecek; `claude --bg` ile shell'den, `/background` ile mevcut session'dan "
        "arka plan oturumu başlatabileceksin",
        "Writer/Reviewer ve Test-first paralel çalışma pattern'lerini uygulayabileceksin",
        "Paralel task partitioning kurallarını (contract-first, dosya ayrımı, scope sınırlama, "
        "integration pass) uygulayabileceksin",
        "Ne zaman paralel, ne zaman sıralı çalışmanın daha verimli olduğuna — bağımlılık, "
        "rate limit ve maliyet çarpanı farkındalığıyla — karar verebileceksin",
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
                h("1.1 Neden Paralel Çalışma?"),
                p(
                    "Claude Code oturumları hızlandıkça asıl darboğaz AI'ın kodu yazması değil, "
                    "senin bekleme ve context-switch süren oluyor. Tek terminal sekmesinde "
                    "sırayla bir feature geliştirip, bir bug düzeltip, bir de review yapmak "
                    "yüzlerce dakika demek. Paralel çalışma bu sırayı kırar: bir oturum "
                    "feature yazarken, ikincisi bug düzeltir, üçüncüsünü sadece hazır olduğunda "
                    "kontrol edersin."
                ),
                p(
                    "Ancak paralellik bedava değil. Her oturum senin abonelik kotanı bağımsız "
                    "tüketir — üç paralel oturum, üç kat token harcar. Yanlış bölünmüş görevler "
                    "aynı dosyaya iki oturumun yazmasına, dolayısıyla merge conflict'e yol açar. "
                    "Bu yüzden bugün iki şey öğreneceğiz: paralelliğin mekanikleri (worktree + "
                    "agent view) ve paralelliğin tasarımı (task partitioning)."
                ),

                h("1.2 Karar Matrisi: Bugün Worktrees + Agent View, Yarın Agent Teams + Dynamic Workflows"),
                p(
                    "Claude Code'da paralel çalışmanın dört yaklaşımı var. Bunlar farklı "
                    "soruları çözer; üst üste biner değil, yan yana durur:"
                ),
                table(
                    ["Yaklaşım", "Kim koordine eder?", "İşçiler konuşur mu?", "Dosya izolasyonu", "Ne zaman?"],
                    [
                        ["Worktrees", "Sen (veya otomatik)", "Hayır", "Her oturum ayrı git checkout", "Her zaman — dosya çakışmasını önler"],
                        ["Agent View", "Sen (dispatch/peek/attach)", "Hayır", "Dispatch edilen her session otomatik worktree alır", "Bağımsız görevleri paralel yürütmek istediğinde"],
                        ["Agent Teams", "Claude (team lead)", "Evet (mesajlaşma + task claim)", "Git tabanlı", "Birbiriyle koordineli çalışması gereken görevler — Gün 17"],
                        ["Dynamic Workflows", "Script (sen yazarsın)", "Hayır (script yönlendirir)", "Worktree", "Büyük migrasyon/denetim; tekrarlanabilir plan — Gün 17"],
                    ]
                ),
                keypoint(
                    "Bugünün odağı ilk iki satır: Worktrees dosya çakışmasını çözer, Agent View senin "
                    "dikkatini yönetir. İkisi farklı problemi çözer ama birlikte kullanılır — agent "
                    "view zaten dispatch ettiği her oturumu otomatik worktree'ye taşır."
                ),
                p(
                    "Agent teams ve dynamic workflows'u yarın (Gün 17) derinlemesine göreceğiz. "
                    "Aradaki temel fark: bugün koordinasyonu sen yapıyorsun (dispatch, peek, "
                    "attach); yarın koordinasyonu Claude veya bir script yapacak."
                ),

                h("1.3 Git Worktree Temelleri ve Claude Code'un Native Desteği"),
                p(
                    "Git worktree, aynı repository'ye bağlı ama dosya sistemi üzerinde ayrı "
                    "bir dizinde yaşayan ikinci (üçüncü, dördüncü…) bir çalışma kopyadır. Her "
                    "worktree kendi branch'ine sahiptir; ancak tümü aynı git history ve remote'u "
                    "paylaşır. Bu sayede bir worktree'deki değişiklik diğerini etkilemez."
                ),
                p(
                    "Claude Code, git worktree desteğini `--worktree` (kısa: `-w`) flag'i ile "
                    "native olarak sunar. Bu flag'i kullandığında Claude Code:"
                ),
                bullets([
                    "Projenin kök dizininde `.claude/worktrees/<isim>/` altında yeni bir worktree oluşturur.",
                    "`worktree-<isim>` adında yeni bir branch açar (varsayılan olarak remote'un default branch'inden dallanır).",
                    "Claude Code oturumunu doğrudan bu izole dizinde başlatır.",
                    "Oturum bittiğinde (değişiklik yoksa) worktree ve branch'i otomatik temizler.",
                ]),
                code(
                    "# Terminal 1: feature-auth worktree'sinde oturum başlat\n"
                    "claude --worktree feature-auth\n"
                    "# veya kısa form:\n"
                    "claude -w feature-auth\n\n"
                    "# Terminal 2: aynı repo, farklı worktree\n"
                    "claude -w bugfix-sidebar\n\n"
                    "# İsimsiz worktree (Claude otomatik isim üretir, ör. bright-running-fox)\n"
                    "claude -w",
                    "bash"
                ),
                tip(
                    "`.claude/worktrees/` dizinini `.gitignore` dosyana ekle; worktree içerikleri "
                    "ana checkout'ta untracked dosya olarak görünmesin: `echo '.claude/worktrees/' "
                    ">> .gitignore`."
                ),

                h("1.4 Agent View: Tüm Oturumları Tek Ekrandan Yönet"),
                p(
                    "Agent view, `claude agents` komutu ile açılan terminal tabanlı bir dashboard'dur. "
                    "Makine üzerinde çalışan tüm arka plan Claude Code oturumlarını tek bir listede "
                    "gösterir. Her satır bir tam Claude Code konuşmasıdır — terminale bağlı olmadan "
                    "çalışmaya devam eder."
                ),
                p("Agent view'daki temel session state'leri:"),
                table(
                    ["State", "İkon", "Anlamı"],
                    [
                        ["Working", "✽ / ✻", "Claude aktif olarak yanıt üretiyor veya bir araç çalıştırıyor"],
                        ["Needs input", "Sarı nokta", "Claude senden bir karar bekliyor — müdahale et"],
                        ["Idle", "—", "Bekliyor ama spesifik bir bloklayıcı soru yok"],
                        ["Completed", "Yeşil ✢", "Görev başarıyla tamamlandı"],
                        ["Failed", "Kırmızı", "Terminal bir hata ile durdu"],
                        ["Stopped", "Gri", "Oturum durduruldu"],
                    ]
                ),
                p(
                    "Bunlara ek olarak, liste görünümünde PR açılmış işler 'Ready for review' grubu "
                    "altında toplanabilir. Bu ayrı bir state değil, bir sunum gruplamasıdır."
                ),
                p(
                    "Agent view'a girmek ve arka plan oturumu başlatmak için iki farklı yol var. "
                    "Ayrımı bilmek önemli:"
                ),
                table(
                    ["Kullanım", "Komut", "Bağlam"],
                    [
                        ["Dashboard'u aç", "claude agents", "Terminal'den; tüm session'ları listeler"],
                        ["Shell'den yeni arka plan oturumu başlat", 'claude --bg "görev açıklaması"', "Scriptable; session ID döner"],
                        ["Mevcut oturumu arka plana gönder", "/background veya /bg", "Aktif konuşmanın içinden; konuşma arka planda devam eder"],
                        ["Arka plan oturumuna bağlan", "claude attach <session-id>", "Tam konuşma transcript'ine dönersin"],
                    ]
                ),
                warn(
                    "Agent view Temmuz 2026 itibarıyla Research Preview aşamasında (v2.1.139+). "
                    "Arayüz ve kısayol tuşları değişebilir. Oturumlar local'dir — laptop uykuya geçerse "
                    "oturumlar durur; `claude respawn --all` ile yeniden başlatılır. Her paralel oturum "
                    "kotanı bağımsız tüketir."
                ),

                h("1.5 Desktop App'te Paralel Oturumlar"),
                p(
                    "Claude Code Desktop App'in Code tab'inde, local Git repository üzerinde açılan "
                    "paralel session'lar varsayılan olarak ayrı git worktree içinde çalışır. Bu sayede "
                    "split pane'lerde birden fazla oturumu görsel olarak yan yana izleyebilir, görsel "
                    "diff inceleyebilir ve PR durumlarını takip edebilirsin."
                ),
                warn(
                    "Bu davranış local Git repository session'ları için geçerlidir. Git repository'si "
                    "olmayan bir dizinde veya farklı environment'larda (cloud, cowork) aynı izolasyon "
                    "davranışı garanti edilmez."
                ),
                tip(
                    "Desktop App'i CLI ile birlikte kullanabilirsin: CLI'dan `claude --bg` ile "
                    "dispatch ettiğin oturumlar Desktop App'in agent view panelinde de görünür. "
                    "İkisi aynı supervisor process'i paylaşır."
                ),

                h("1.6 Paralel Task Partitioning Kuralları"),
                p(
                    "Paralel çalışmanın başarısı komutları bilmekten çok, işi doğru bölmeye "
                    "bağlıdır. Yanlış bölünmüş görevler conflict, tekrar ve zaman kaybı yaratır. "
                    "Beş temel kural:"
                ),
                table(
                    ["Kural", "Açıklama", "Kötü örnek → İyi örnek"],
                    [
                        [
                            "Aynı dosyaya iki agent yazmasın",
                            "Conflict riskini doğrudan azaltır",
                            "'Dashboard'u geliştir' → 'Backend: /api/metrics endpoint'i ekle / Frontend: MetricsCard component'i yaz'"
                        ],
                        [
                            "Contract önce yazılsın",
                            "Backend ve frontend paralel çalışacaksa API contract veya mock schema önceden sabitlenmeli",
                            "İkisi birden 'bir şeyler yapsın' → Önce UsageSummary type tanımla, sonra paralel başlat"
                        ],
                        [
                            "Her agent'ın scope'u küçük olsun",
                            "Tek sorumluluk ilkesi: bir oturum bir iş",
                            "'Dashboard'u tamamla' → '/api/usage/summary endpoint'i ekle'"
                        ],
                        [
                            "Her session kendi commit'ini atsın",
                            "Merge ve rollback kolaylaşır; her branch izlenebilir",
                            "Commit'siz çalışıp sonra toplu → Her oturum kendi branch'inde commit"
                        ],
                        [
                            "Integration agent ayrı olsun",
                            "Son bir oturum tüm branch'leri entegre edip test çalıştırsın",
                            "Herkes merge etsin → Bir integration pass tüm branch'leri birleştirir"
                        ],
                    ]
                ),
                keypoint(
                    "İyi partitioning conflict'i azaltır. Eğer paralel çalışırken sürekli conflict "
                    "çıkıyorsa, sorun araçta değil görev bölümünde. Bugünkü challenge'da bunu "
                    "bizzat deneyimleyeceksin."
                ),

                h("1.7 Ne Zaman Paralel, Ne Zaman Sıralı?"),
                p("Her iş paralele uygun değildir. Karar verirken şu soruları sor:"),
                bullets([
                    "**Görevler birbirinden bağımsız mı?** Bağımsızsa paralel; Feature B, Feature A'nın çıktısına bağlıysa sıralı.",
                    "**Aynı dosyalara dokunacaklar mı?** Dokunacaklarsa scope'u daralt veya sıralı çalış.",
                    "**Kotam yeterli mi?** 3 paralel oturum = 3× token tüketimi. Pro plan'da 5+ eşzamanlı oturum rate limit'e takılabilir.",
                    "**Görev kısa mı?** 10 dakikada biten bir düzeltme için worktree kurulumu overhead yaratır; doğrudan ana session'da yap.",
                    "**Sonuçları bütünleştirmem gerekecek mi?** Integration pass planlıyorsan zaman ayır.",
                ]),
            ],
        },

        # ── BÖLÜM 2: PRATİK — ADIM ADIM ─────────────────────────────────
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                h("2.1 İlk Worktree Oturumunu Başlat"),
                p(
                    "SaaS Dashboard proje dizinine git. Bu proje Gün 14'te oluşturuldu ve en az "
                    "bir commit içeriyor olmalı (worktree, git repository gerektirir)."
                ),
                steps([
                    "SaaS Dashboard proje dizinine gir: `cd ~/projects/saas-dashboard` (veya senin dizinin).",
                    "İlk worktree oturumunu başlat: `claude --worktree feature-metrics-api`",
                    "Claude Code'un `.claude/worktrees/feature-metrics-api/` dizinini oluşturduğunu gözlemle.",
                    "Worktree'nin hangi branch'te olduğunu kontrol et: `git branch` (worktree-feature-metrics-api branch'i görünecek).",
                    "Bu oturumda küçük bir değişiklik yap (ör. bir yorum satırı ekle) ve commit et.",
                ]),
                code(
                    "# Worktree başlatıldıktan sonra Claude oturumunda:\n"
                    "# Claude otomatik olarak .claude/worktrees/feature-metrics-api/ dizininde çalışır\n\n"
                    "# Aktif worktree'leri listele (ayrı bir terminal'den):\n"
                    "git worktree list\n"
                    "# Çıktı:\n"
                    "# /home/user/projects/saas-dashboard                        abc1234 [main]\n"
                    "# /home/user/projects/saas-dashboard/.claude/worktrees/feature-metrics-api  def5678 [worktree-feature-metrics-api]",
                    "bash"
                ),

                h("2.2 İkinci Worktree ile Paralel Çalışma"),
                steps([
                    "Yeni bir terminal sekmesi/penceresi aç (ana proje dizininde ol).",
                    "İkinci bir worktree oturumu başlat: `claude -w feature-metrics-widget`",
                    "Şimdi iki ayrı Claude Code oturumun var: biri API, diğeri frontend widget üzerinde çalışabilir.",
                    "`git worktree list` ile iki worktree'yi doğrula.",
                    "Her iki oturumda da bağımsız değişiklikler yap ve commit et.",
                ]),
                tip(
                    "tmux kullanıyorsan `Ctrl+B %` ile terminal'i dikey böl; sol panelde bir "
                    "worktree, sağda diğeri. VS Code'da Terminal → Split Terminal ile aynı "
                    "sonucu alırsın."
                ),

                h("2.3 .worktreeinclude ile Gitignored Dosyaları Taşıma"),
                p(
                    "Worktree yeni bir git checkout olduğu için `.env`, `.env.local` gibi "
                    "gitignored dosyalar otomatik gelmez. `.worktreeinclude` dosyası bu sorunu çözer."
                ),
                steps([
                    "Proje kök dizininde `.worktreeinclude` dosyası oluştur:",
                    "İçine taşınmasını istediğin gitignored dosya pattern'lerini yaz (`.gitignore` sözdizimi).",
                    "Yeni bir worktree başlattığında bu dosyalar otomatik kopyalanır.",
                ]),
                code(
                    "# .worktreeinclude dosyası (proje kök dizini)\n"
                    ".env\n"
                    ".env.local\n"
                    "config/secrets.yaml",
                    ""
                ),
                p(
                    "Kural: Yalnızca bir pattern'e uyan ve aynı zamanda gitignored olan dosyalar "
                    "kopyalanır — tracked dosyalar asla çoğaltılmaz. Bu mekanizma `--worktree`, "
                    "subagent worktree'leri ve Desktop App paralel session'ları için geçerlidir."
                ),

                h("2.4 Subagent Worktree İzolasyonu"),
                p(
                    "Gün 11'de öğrendiğin subagent'lar da kendi worktree'lerinde çalışabilir. "
                    "Bu özellikle birden fazla subagent'ın paralel dosya düzenlemesi gereken "
                    "durumlarda (ör. her modülü ayrı bir subagent migrate etsin) kritiktir."
                ),
                code(
                    "# .claude/agents/migration-worker.md\n"
                    "---\n"
                    "name: migration-worker\n"
                    "description: Kod migration uzmanı\n"
                    "tools: Read, Write, Edit, Bash, Grep, Glob\n"
                    "model: sonnet\n"
                    "effort: high\n"
                    "isolation: worktree\n"
                    "---\n"
                    "Sen bir kod migration uzmanısın. Verilen modülü migrate et,\n"
                    "build'ın geçtiğini doğrula.",
                    "yaml"
                ),
                p(
                    "Subagent worktree'leri geçicidir: subagent değişiklik yapmadan biterse "
                    "worktree ve branch otomatik silinir. Değişiklik varsa commit'lenmiş olarak "
                    "kalır ve ana oturumdan merge edilebilir."
                ),
                tip(
                    "Prompt'ta da isteyebilirsin: 'Subagent'larını worktree izolasyonuyla çalıştır' "
                    "— Claude bunu anlayıp her subagent'a ayrı worktree verir."
                ),

                h("2.5 Worktree Cleanup ve Yaşam Döngüsü"),
                p("Bir worktree oturumundan çıktığında temizlik davranışı şöyle çalışır:"),
                table(
                    ["Durum", "Davranış"],
                    [
                        ["Uncommitted değişiklik yok, yeni commit yok, untracked dosya yok", "Worktree ve branch otomatik silinir"],
                        ["Oturumun bir ismi var (--worktree ile verdiysen)", "Claude sorar: sakla mı sil mi?"],
                        ["Commit'lenmiş değişiklikler var", "Worktree kalır; merge veya push yapman beklenir"],
                        ["-p (non-interactive) ile oluşturulmuş worktree", "Otomatik temizlenmez; manuel `git worktree remove` gerekir"],
                    ]
                ),
                warn(
                    "Worktree'yi kapatmadan/silmeden önce mutlaka `git status` çalıştır. "
                    "Commit edilmemiş veya push edilmemiş değişikliklerin kaybolmaması için "
                    "merge veya push yap. `git worktree remove --force` ile zorla silersen "
                    "commit'lenmemiş değişiklikler gider."
                ),
                code(
                    "# Aktif worktree'leri listele:\n"
                    "git worktree list\n\n"
                    "# Belirli bir worktree'yi kaldır (değişiklik yoksa):\n"
                    "git worktree remove .claude/worktrees/feature-metrics-api\n\n"
                    "# Zorla kaldır (dikkatli!):\n"
                    "git worktree remove --force .claude/worktrees/eski-deneme",
                    "bash"
                ),
            ],
        },

        # ── BÖLÜM 3: PRATİK — DERİNLEŞ / UYGULAMA ────────────────────────
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                h("3.1 Agent View ile Çoklu Oturumları Yönetme"),
                steps([
                    "Ana proje dizininde `claude agents` komutunu çalıştır. Agent view dashboard'u açılır.",
                    "Alt kısımdaki input alanına bir görev yaz ve Enter'a bas. Yeni bir arka plan oturumu başlar ve tabloda bir satır olarak görünür.",
                    "İkinci bir görev daha dispatch et (her prompt ayrı bir oturum başlatır).",
                    "Space tuşu ile bir satıra peek yap — son çıktıyı göreceksin, konuşmaya girmeden.",
                    "Enter ile bir oturuma attach ol — tam konuşma transcript'ine dönersin.",
                    "Boş prompt'ta ← (sol ok) ile agent view'a geri dön; oturum arka planda çalışmaya devam eder.",
                    "Esc ile agent view'dan çık — oturumlar çalışmaya devam eder.",
                ]),
                code(
                    "# Agent view'ı aç:\n"
                    "claude agents\n\n"
                    "# Tek projeye filtrele:\n"
                    "claude agents --cwd ~/projects/saas-dashboard\n\n"
                    "# Shell'den doğrudan arka plan oturumu başlat (agent view açmadan):\n"
                    'claude --bg "SaaS Dashboard\'daki flaky test\'i bul, düzelt ve PR aç"\n\n'
                    "# Belirli bir agent ile arka plan oturumu:\n"
                    'claude --agent code-reviewer --bg "PR #42\'deki review yorumlarını çöz"',
                    "bash"
                ),
                tip(
                    "Agent view'da Ctrl+S ile gruplalamayı dizine göre / duruma göre geçiş "
                    "yapabilirsin. Ctrl+R ile bir oturumu yeniden adlandırabilirsin — satırlar "
                    "bir task board gibi okunabilir olsun."
                ),

                h("3.2 Mevcut Oturumdan Arka Plana Geçiş"),
                p(
                    "Shell'den `claude --bg` ile yeni oturum başlatmak dışında, aktif bir Claude "
                    "Code konuşmasını da arka plana gönderebilirsin. Bu iki farklı mekanizmayı "
                    "karıştırmamak önemli:"
                ),
                table(
                    ["Durum", "Kullanım", "Ne olur"],
                    [
                        ["Yeni arka plan oturumu başlat (shell'den)", 'claude --bg "görev"', "Yeni session ID alırsın; agent view'da satır olarak görünür"],
                        ["Mevcut konuşmayı arka plana gönder", "/background veya /bg", "Aktif konuşma arka planda çalışmaya devam eder; agent view'da görünür olur"],
                        ["Arka plan oturumuna bağlan", "claude attach <id>", "Tam transcript ile oturuma dönersin"],
                        ["Arka plan oturumunu durdur", "/stop (içinden) veya claude stop <id>", "Oturum sonlanır, worktree kalır"],
                    ]
                ),
                warn(
                    "← (sol ok), Ctrl+C, Ctrl+D, Ctrl+Z ve /exit ile oturumdan ayrılsan "
                    "bile arka plan oturumu çalışmaya devam eder. Oturumu tamamen durdurmak "
                    "için /stop kullan."
                ),

                h("3.3 Writer/Reviewer Pattern"),
                p(
                    "Paralel çalışmanın en yaygın pattern'i: bir oturum yazar, diğeri inceler. "
                    "Bu pattern kod kalitesini artırır çünkü reviewer farklı bir context'te, "
                    "yazarın varsayımlarından bağımsız bakabilir."
                ),
                steps([
                    "Birinci worktree'de (writer): `claude -w feature-new-endpoint` — 'SaaS Dashboard'a /api/usage/summary endpoint'i ekle, testini yaz.'",
                    "İkinci worktree'de (reviewer): `claude -w review-endpoint` — writer branch'teki değişiklikleri review etmek için bekle.",
                    "Writer commit edince, reviewer worktree'sinde: 'worktree-feature-new-endpoint branch'indeki son commit'leri incele, potansiyel sorunları listele.'",
                    "Reviewer'ın bulduğu sorunları writer oturumuna geri bildir ve düzeltilmesini iste.",
                ]),
                tip(
                    "Agent view ile bu pattern daha verimli olur: writer'ı `claude --bg` ile "
                    "dispatch et, reviewer'ı ayrı bir `--bg` ile başlat, agent view'dan "
                    "ikisini birden izle."
                ),

                h("3.4 Test-First Pattern"),
                p(
                    "Bir diğer güçlü pattern: önce testleri yazan bir oturum, sonra testleri "
                    "geçecek implementasyonu yazan ikinci oturum."
                ),
                steps([
                    "Birinci oturum (test writer): 'UsageSummary API endpoint'i için pytest testleri yaz. Endpoint henüz yok, mock kullanma, gerçek HTTP istekleri yap. Beklenen response shape'i şu: {activeUsers, requestsToday, errorRate, costEstimateUsd}.'",
                    "İkinci oturum (implementer): 'Bu branch'teki testleri çalıştır, fail edenleri geçecek şekilde endpoint'i implement et.'",
                    "İkinci oturumun testleri geçirip geçirmediğini agent view'dan izle.",
                ]),

                h("3.5 Desktop App Paralel Panelleri (İsteğe Bağlı)"),
                p(
                    "Claude Code Desktop App kullanıyorsan, Code tab'de birden fazla session "
                    "panelini yan yana açabilirsin. Her panel kendi worktree'sinde çalışır. "
                    "Görsel diff inceleme ve PR durumu takibi için Desktop App özellikle kullanışlı. "
                    "CLI'dan dispatch ettiğin arka plan oturumları burada da görünür."
                ),
            ],
        },
    ],

    # =========================================================================
    # PROMPTS
    # =========================================================================
    "prompts": [
        {
            "title": "Worktree Başlatma + Göreve Bağlama",
            "prompt": (
                "SaaS Dashboard projesinde yeni bir worktree aç ve /api/usage/summary "
                "endpoint'ini implement et. Endpoint şu alanları dönsün: activeUsers "
                "(number), requestsToday (number), errorRate (number), costEstimateUsd "
                "(number). SQLite'tan mock veri çek. Testini yaz ve çalıştır."
            ),
            "note": "claude -w feature-usage-api komutuyla başlattıktan sonra bu prompt'u gir.",
        },
        {
            "title": "Agent View'dan Dispatch: Kapsamlı Arka Plan Görevi",
            "prompt": (
                "SaaS Dashboard'daki flaky test'i bul: testlerin rastgele fail ettiği "
                "senaryoyu izole et, root cause'u belirle ve minimal bir fix yaz. "
                "Fix'i commit et ve PR aç. PR açıklamasında root cause'u açıkla."
            ),
            "note": "claude agents dashboard'unda veya claude --bg ile dispatch et.",
        },
        {
            "title": "Writer → Reviewer Devri",
            "prompt": (
                "worktree-feature-usage-api branch'indeki son commit'leri incele. "
                "API response shape'inin contracts/usage-summary.contract.ts ile uyumunu "
                "kontrol et. Güvenlik, performans ve hata yönetimi açısından potansiyel "
                "sorunları listele. Her sorun için önerilen düzeltmeyi tek cümleyle yaz."
            ),
            "note": "Reviewer worktree'sinde veya ayrı bir agent view oturumunda kullan.",
        },
        {
            "title": "Merge Conflict Çözüm Rehberliği",
            "prompt": (
                "feature-usage-api ve feature-usage-widget branch'lerini main'e merge "
                "etmem gerekiyor. Önce merge sırası öner (hangisi önce merge edilmeli?), "
                "sonra merge et. Conflict çıkarsa nedenini açıkla ve minimal çözüm öner. "
                "Merge sonrası testleri çalıştır."
            ),
        },
        {
            "title": "Task Partitioning: Paralel İş Paketleri Oluşturma",
            "prompt": (
                "Bu feature'ı paralel çalışmaya uygun küçük iş paketlerine böl. Her iş "
                "paketinin hangi dosyalara dokunacağını, hangi branch/worktree'de "
                "çalışacağını, bağımlılıklarını ve acceptance criteria'larını listele. "
                "Aynı dosyaya iki agent'ın yazmasını engelle. Her paket için scope "
                "sınırını açıkça belirt."
            ),
            "note": "Paralel çalışmaya başlamadan önce bu prompt'u çalıştır — plan yapmadan dispatch etme.",
        },
        {
            "title": "Integration Agent: Branch Birleştirme ve Test",
            "prompt": (
                "Aşağıdaki worktree branch'lerindeki değişiklikleri incele: "
                "worktree-feature-usage-api, worktree-feature-usage-widget. "
                "Önce API contract uyumunu kontrol et (contracts/ dizinindeki type "
                "tanımlarına bak), sonra merge sırası öner, ardından merge et ve "
                "test komutlarını çalıştır. Conflict çıkarsa nedenini açıkla ve "
                "minimal çözüm öner."
            ),
            "note": "Integration worktree'sinde (claude -w usage-integration) çalıştır.",
        },
    ],

    # =========================================================================
    # CHALLENGE
    # =========================================================================
    "challenge": {
        "title": "CHALLENGE: SaaS Dashboard'a Usage Metrics Feature'ı — Paralel Worktree Workflow",
        "task": (
            "SaaS Dashboard'a 'Usage Metrics' feature'ı ekleyeceksin. Backend API ve frontend "
            "widget'ı paralel olarak ayrı worktree'lerde geliştir, bir integration pass ile "
            "birleştir. Amaç feature'ı tamamlamak kadar, contract-first paralel workflow'u "
            "deneyimlemek."
        ),
        "requirements": [
            "Önce bir API contract tanımla (ör. UsageSummary type: activeUsers, requestsToday, "
            "errorRate, costEstimateUsd alanları)",
            "Backend oturumu ayrı bir worktree'de çalışsın (claude -w usage-api)",
            "Frontend oturumu ayrı bir worktree'de çalışsın (claude -w usage-widget)",
            "Her oturum kendi branch'inde commit atsın",
            "Bir integration pass ile branch'ler birleştirilsin ve testler çalıştırılsın",
            "Agent view'dan en az iki arka plan oturumu izlensin (peek veya attach)",
        ],
        "success": [
            "Her oturum ayrı worktree'de izole çalıştı — `git worktree list` ile doğrulandı",
            "Backend ve frontend scope'u önceden API contract ile ayrıldı",
            "Her oturum kendi branch'inde en az bir commit attı",
            "Integration pass sonunda testler çalıştırıldı ve feature entegre çalışıyor",
            "Conflict çıkarsa Claude ile çözüldü; çıkmazsa iyi partitioning'in sonucu olduğu açıklandı",
            "Agent view'dan en az iki oturum izlenip birine peek veya attach yapıldı",
        ],
        "bonus": [
            "Bilinçli bir conflict senaryosu simüle et: iki worktree'den aynı config dosyasına "
            "bir satır ekle, merge et, conflict'i Claude ile çöz.",
            "Writer/Reviewer veya Test-first pattern'lerinden birini uygula.",
            "Üçüncü bir worktree ile integration agent pattern'ini kullan.",
        ],
        "solution": {
            "intro": (
                "Bu challenge contract-first paralel geliştirme yaklaşımını adım adım uygular. "
                "Önce paylaşılan sözleşmeyi yaz, sonra bağımsız worktree'lerde paralel çalış, "
                "son olarak bir integration pass ile birleştir."
            ),
            "prompts": [
                {
                    "title": "0) Contract Tanımla (ana branch'te, paralel başlamadan önce)",
                    "prompt": (
                        "SaaS Dashboard projesinde contracts/ dizini oluştur. İçine "
                        "usage-summary.contract.ts dosyası ekle. UsageSummary type'ını tanımla: "
                        "activeUsers (number), requestsToday (number), errorRate (number, 0-1 "
                        "aralığında), costEstimateUsd (number). Bu dosyayı commit et."
                    ),
                },
                {
                    "title": "1) Backend Worktree Başlat",
                    "prompt": (
                        "claude -w usage-api komutuyla worktree aç. Ardından: "
                        "'/api/usage/summary endpoint'ini implement et. Response shape'i "
                        "contracts/usage-summary.contract.ts ile birebir uyumlu olsun. "
                        "SQLite'tan örnek veri çek veya mock data kullan. Endpoint'in "
                        "testini yaz ve çalıştır. Commit et.'"
                    ),
                },
                {
                    "title": "2) Frontend Worktree Başlat (paralel)",
                    "prompt": (
                        "İkinci bir terminal'de: claude -w usage-widget komutuyla worktree aç. "
                        "Ardından: 'Dashboard'a UsageMetrics card component'i ekle. "
                        "contracts/usage-summary.contract.ts type'ını kullan. Şimdilik mock "
                        "data ile çalışsın (API henüz main'de yok). Component'in testini yaz. "
                        "Commit et.'"
                    ),
                },
                {
                    "title": "3) Integration Pass",
                    "prompt": (
                        "İki worktree branch'ini main'e merge et (sıra: önce backend, sonra "
                        "frontend). Frontend'deki mock data'yı gerçek API endpoint'e bağla. "
                        "Tüm testleri çalıştır. Çalışıyorsa commit et."
                    ),
                },
            ],
            "notes": [
                "Contract'ı ana branch'e commit ettikten sonra worktree'ler bu commit'i görecektir "
                "(aynı repository history'yi paylaşırlar).",
                "Backend ve frontend birbirinden bağımsız çalışır; bağlantı noktası contract type'ıdır.",
                "Integration pass'te frontend'in mock data'sını gerçek fetch'e çevirmek en yaygın adımdır.",
                "`git worktree list` ile worktree durumlarını, `claude agents` ile session durumlarını kontrol et.",
                "Agent view'dan dispatch ettiğin oturumlar otomatik worktree alır — ekstra `-w` flag'ine gerek yok.",
            ],
            "pitfalls": [
                "Contract tanımlamadan paralel başlamak → Backend ve frontend uyumsuz response shape'leri üretir.",
                "Worktree'yi commit etmeden silmek → Değişiklikler kaybolur. Silmeden önce `git status` çalıştır.",
                "İki worktree'de aynı dosyayı düzenlemek → Merge conflict kaçınılmaz. Scope'u dosya bazında ayır.",
                "Merge sırasını düşünmemek → Backend önce merge edilmeli ki frontend gerçek API'ye bağlanabilsin.",
                "Agent view'daki oturumları unutmak → Laptop uykuya geçerse oturumlar durur; `claude respawn --all`.",
                "Rate limit'i hesaplamamak → Üç paralel oturum üç kat kota tüketir; Pro plan'da dikkatli ol.",
            ],
        },
    },

    # =========================================================================
    # TAKEAWAYS
    # =========================================================================
    "takeaways": [
        "Worktrees dosya izolasyonunu, agent view dikkat yönetimini çözer — ikisi farklı "
        "problemi çözer ama birlikte kullanılır.",
        "`claude --worktree <isim>` veya `claude -w` ile bir komutta izole oturum açarsın; "
        "`.worktreeinclude` ile `.env` gibi gitignored dosyaları otomatik taşırsın.",
        "`claude agents` tek ekrandan tüm arka plan oturumlarını listeler; `claude --bg` shell'den, "
        "`/background` aktif konuşmadan arka plan oturumu başlatır.",
        "İyi paralel çalışmanın anahtarı task partitioning: aynı dosyaya iki agent yazmaz, "
        "contract önce yazılır, scope küçük tutulur, integration pass ayrıdır.",
        "Her paralel oturum kotanı bağımsız tüketir; ne zaman paralel ne zaman sıralı "
        "çalışılacağı bilinçli bir mühendislik kararıdır.",
        "Writer/Reviewer ve Test-first pattern'leri kod kalitesini artırır — paralel çalışma "
        "sadece hız değil, kalite aracı da olabilir.",
        "Agent view Research Preview aşamasında; oturumlar local'dir, laptop uykuya geçince "
        "durur (`claude respawn --all`), arayüz değişebilir.",
        "Worktree cleanup otomatiktir (değişiklik yoksa); commit etmeden worktree silmek en "
        "sık yapılan hata — `git status` alışkanlığı edin.",
    ],

    # =========================================================================
    # READING
    # =========================================================================
    "reading": {
        "official": [
            {
                "label": "Run parallel sessions with worktrees — --worktree, .worktreeinclude, subagent izolasyonu, cleanup",
                "url": "https://code.claude.com/docs/en/worktrees",
            },
            {
                "label": "Manage multiple agents with agent view — claude agents, dispatch, peek, attach, background sessions",
                "url": "https://code.claude.com/docs/en/agent-view",
            },
            {
                "label": "Run agents in parallel — Worktrees, agent view, agent teams, dynamic workflows karşılaştırması",
                "url": "https://code.claude.com/docs/en/agents",
            },
            {
                "label": "Desktop application — Paralel session'lar, görsel diff, PR izleme",
                "url": "https://code.claude.com/docs/en/desktop",
            },
        ],
        "community": [
            {
                "label": "Parallel Vibe Coding: Using Git Worktrees with Claude Code (Dan Does Code)",
                "url": "https://www.dandoescode.com/blog/parallel-vibe-coding-with-git-worktrees",
            },
            {
                "label": "How to Run Claude Code Agents in Parallel (Towards Data Science)",
                "url": "https://towardsdatascience.com/how-to-run-claude-code-agents-in-parallel/",
            },
        ],
        "extra": [
            {
                "label": "Git Worktree resmi dokümantasyonu",
                "url": "https://git-scm.com/docs/git-worktree",
            },
        ],
    },

    # =========================================================================
    # NEXT PREVIEW
    # =========================================================================
    "next_preview": (
        "Yarın (Gün 17) koordinasyonu sen değil, Claude yapacak: Agent Teams ile team lead + "
        "worker mimarisi kuracak, dynamic workflows ile script tabanlı çoklu-agent orkestrasyonu "
        "deneyecek ve SaaS Dashboard'a paralel 3 bağımsız feature ekleyeceksin."
    ),

    # =========================================================================
    # CHECKLIST
    # =========================================================================
    "checklist": [
        "Worktrees, agent view, agent teams ve dynamic workflows arasındaki farkı (kim koordine eder, "
        "işçiler konuşur mu, dosya izolasyonu) açıklayabiliyorum",
        "`claude --worktree <isim>` veya `claude -w` ile izole worktree oturumu başlatabildim",
        "`.worktreeinclude` dosyası oluşturup gitignored dosyaları (ör. .env) yeni worktree'ye "
        "otomatik taşıyabildim",
        "`git worktree list` ile aktif worktree'leri listeledim ve cleanup davranışını gözlemledim",
        "Worktree kapatmadan/silmeden önce `git status` ile commit durumunu kontrol etme "
        "alışkanlığını edindim",
        "`claude agents` ile agent view dashboard'unu açtım, en az bir görev dispatch ettim",
        "`claude --bg` (shell'den) ve `/background` (aktif oturumdan) arasındaki farkı biliyorum "
        "ve en az birini denedim",
        "Agent view'da bir oturuma peek (Space) ve attach (Enter) yaptım",
        "Writer/Reviewer veya Test-first pattern'lerinden en az birini uyguladım",
        "Task partitioning kurallarını (contract-first, dosya ayrımı, scope sınırlama) en az bir "
        "kez uyguladım",
        "Challenge'ı tamamladım: backend + frontend paralel worktree'lerde geliştirildi, "
        "integration pass ile birleştirildi",
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
    chk("day == 16", L["day"] == 16)
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
