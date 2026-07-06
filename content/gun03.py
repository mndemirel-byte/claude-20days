# -*- coding: utf-8 -*-
"""Gün 3 — CLAUDE.md ve Auto Memory: Projenin Beyni (v2.0, Temmuz 2026)."""
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table

LESSON = {
    "day": 3,
    "total_days": 20,
    "week": 1,
    "slug": "claude-md-auto-memory",
    "title": "CLAUDE.md ve Auto Memory: Projenin Beyni",
    "tagline": "Claude'a projenin kurallarını öğret — ve öğrenmesine izin ver",
    "tier": None,
    "date_label": "Temmuz 2026",

    "intro": (
        "Claude Code her oturumu sıfır hafızayla başlatır — dünkü tercihlerin, projenin "
        "teknoloji stack'i veya \"test her zaman pytest ile çalışsın\" kuralın otomatik olarak "
        "taşınmaz. İşte CLAUDE.md tam burada devreye girer: Claude'a her oturum başında okuması "
        "gereken kalıcı talimatlar verirsin. Bugün hem bu talimat dosyalarını hem de Claude'un "
        "kendi kendine öğrendiği notları (auto memory) uçtan uca öğreneceksin."
    ),

    "flow": [
        {"phase": "1 · Teori",     "dur": "40 dk", "desc": "CLAUDE.md hiyerarşisi, kapsamlar, yazım kuralları, auto memory mekanizması"},
        {"phase": "2 · Uygulama",  "dur": "50 dk", "desc": "Global + proje CLAUDE.md, /init, karşılaştırma, /memory, /context"},
        {"phase": "3 · Derinleş",  "dur": "35 dk", "desc": "Path-scoped rules, CLAUDE.local.md, auto memory gözlem/düzenleme, import"},
        {"phase": "4 · Challenge", "dur": "25 dk", "desc": "CLI not defteri v1'e CLAUDE.md ekosistemi kurma"},
    ],

    "prerequisites": [
        "Gün 1 + 2 tamamlanmış (Claude Code kurulu, temel kullanım ve izinler biliniyor)",
        "CLI not defteri v1 projesi mevcut (Gün 2 challenge çıktısı)",
        "Terminal + metin editörü erişimi",
    ],

    "tools_needed": [
        "Claude Code (terminal veya VS Code)",
        "Metin editörü (CLAUDE.md düzenlemek için)",
        "Git (değişiklikleri izlemek için)",
    ],

    "objectives": [
        "CLAUDE.md dosyasının amacını, yüklenme mantığını ve dört kapsamını (managed policy → user → project → local) açıklayabileceksin",
        "Etkili bir proje CLAUDE.md yazabileceksin (200 satır hedefi, somut talimatlar, yapısal organizasyon)",
        "/init komutuyla otomatik CLAUDE.md üretip iyileştirebileceksin",
        "Auto memory'nin ne olduğunu, nerede saklandığını ve oturum başında nasıl yüklendiğini (ilk 200 satır / 25KB) bileceksin",
        "/memory komutuyla yüklenen talimat dosyalarını listeleyebilecek, auto memory'yi açıp kapayabilecek ve notları düzenleyebileceksin",
        ".claude/rules/ altında path-scoped kurallar oluşturup yalnızca ilgili dosyalar okunduğunda yüklendiğini doğrulayabileceksin",
    ],

    # -------------------------------------------------------------------------
    # BÖLÜM 1 — TEORİK TEMEL
    # -------------------------------------------------------------------------
    "sections": [
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                # 1.1
                h("1.1 CLAUDE.md Nedir ve Neden Kritik?"),
                p(
                    "Claude Code her yeni oturumu boş bir context penceresiyle açar. Dünkü "
                    "konuşmayı, tercihlerini veya proje kurallarını hatırlamaz. **CLAUDE.md** "
                    "bu boşluğu dolduran mekanizmadır: Claude'a her oturum başında okunacak "
                    "kalıcı talimatlar verirsin — build komutları, naming convention'lar, klasör "
                    "yapısı, \"her zaman X yap\" kuralları gibi."
                ),
                p(
                    "CLAUDE.md'yi, yeni gelen bir takım arkadaşına ilk gün verdiğin \"proje "
                    "kuralları\" dokümanı gibi düşün. Yoksa her seferinde aynı şeyleri "
                    "yeniden anlatırsın — ki bu hem yorucu hem de hata riski taşır."
                ),
                keypoint(
                    "CLAUDE.md context'tir, hook değildir. Claude bu talimatları okur ve "
                    "takip etmeye çalışır; ama zorunlu kılmaz. Bir aksiyonun kesinlikle "
                    "çalışması gerekiyorsa (ör. her commit öncesi lint) bunu bir hook olarak "
                    "tanımla — hook'lar Gün 12'de işlenecek."
                ),

                # 1.2
                h("1.2 Dört Kapsam ve Yüklenme Mantığı"),
                p(
                    "CLAUDE.md dosyaları farklı konumlara yerleştirilebilir; her konum farklı "
                    "bir kapsam ifade eder. Claude oturum başında bunların hepsini yükler — "
                    "geniş kapsamdan dar kapsama doğru:"
                ),
                table(
                    ["Kapsam", "Konum", "Amaç", "Kim görür"],
                    [
                        [
                            "Managed Policy",
                            "macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`\n"
                            "Linux: `/etc/claude-code/CLAUDE.md`\n"
                            "Windows: `C:\\Program Files\\ClaudeCode\\CLAUDE.md`",
                            "Organizasyon genelinde zorunlu kurallar (güvenlik politikaları, compliance)",
                            "IT/DevOps tarafından yönetilir; tüm kullanıcılar",
                        ],
                        [
                            "User (Kişisel)",
                            "`~/.claude/CLAUDE.md`",
                            "Tüm projelerde geçerli kişisel tercihler (dil, stil, genel kurallar)",
                            "Sadece sen (tüm projeler)",
                        ],
                        [
                            "Project (Proje)",
                            "`./CLAUDE.md` veya `./.claude/CLAUDE.md`",
                            "Takımla paylaşılan proje kuralları (stack, convention, build komutları)",
                            "Git ile tüm takım",
                        ],
                        [
                            "Local (Yerel)",
                            "`./CLAUDE.local.md`",
                            "Commitlenmemesi gereken kişisel proje notları (sandbox URL, test verisi)",
                            "Sadece sen (bu proje); `.gitignore`'a ekle",
                        ],
                    ],
                ),
                p(
                    "**Yüklenme mantığı:** Claude, çalışma dizininden üst dizinlere doğru yürür "
                    "(walk-up) ve bulduğu tüm CLAUDE.md dosyalarını yükler. Aynı dizinde hem "
                    "`CLAUDE.md` hem `CLAUDE.local.md` varsa ikisi de okunur. Alt dizinlerdeki "
                    "CLAUDE.md dosyaları ise **lazy-load** edilir — yani o dizindeki bir dosya "
                    "okunduğunda devreye girer, oturum başında otomatik yüklenmez."
                ),
                tip(
                    "Çoğu kullanıcı için iki dosya yeterlidir: `~/.claude/CLAUDE.md` (kişisel "
                    "tercihler) ve `./CLAUDE.md` (proje kuralları). Managed policy genellikle "
                    "enterprise ortamlarda IT tarafından yönetilir; local ise ihtiyaç duydukça "
                    "eklersin. Basit başla, karmaşıklaştırma."
                ),

                # 1.3
                h("1.3 Etkili CLAUDE.md Yazma Kuralları"),
                p(
                    "CLAUDE.md'nin etkisi doğrudan içeriğinin kalitesiyle orantılıdır. Belirsiz "
                    "veya çok uzun talimatlar Claude'un uyumunu düşürür. Birkaç temel kural:"
                ),
                bullets([
                    "**Kısa tut:** Dosya başına 200 satırın altını hedefle. Daha kısa = daha tutarlı uyum.",
                    "**Somut ol:** \"Kodu düzgün formatla\" yerine \"2 boşluk indent, trailing comma kullan, satır 100 karakter\" yaz.",
                    "**Markdown formatı kullan:** Başlıklar (`##`) ve madde (`-`) ile yapılandır; Claude bu formatı çok iyi ayrıştırır.",
                    "**Çelişkiden kaçın:** İki CLAUDE.md dosyasında aynı konuda zıt talimatlar varsa Claude rastgele birini seçebilir.",
                    "**Güncel tut:** Stack değişince, convention güncellenince CLAUDE.md'yi de güncelle.",
                ]),
                keypoint(
                    "CLAUDE.md'ye ne koymalı: build/test komutları, naming convention, klasör "
                    "yapısı, kod stili, \"her zaman X yap / asla Y yapma\" kuralları. "
                    "Ne koymamalı: çok adımlı prosedürler (→ skill olarak tanımla), yalnızca "
                    "tek bir modülde geçerli kurallar (→ `.claude/rules/` altında path-scoped rule)."
                ),

                # 1.4
                h("1.4 AGENTS.md İlişkisi"),
                p(
                    "Cursor veya başka araçlardan geliyorsan muhtemelen `AGENTS.md` veya "
                    "`.cursorrules` dosyaların vardır. Claude Code bunları **otomatik okumaz**. "
                    "Ancak CLAUDE.md içinden `@AGENTS.md` ile import edebilir veya symlink "
                    "oluşturabilirsin (`ln -s AGENTS.md CLAUDE.md`)."
                ),
                tip(
                    "`/init` komutu çalıştırıldığında mevcut AGENTS.md, .cursorrules ve "
                    "benzeri dosyaları otomatik algılar ve CLAUDE.md'ye taşıma önerisi sunar. "
                    "Migration için en kolay yol budur."
                ),

                # 1.5
                h("1.5 Auto Memory: Claude'un Kendi Defteri"),
                p(
                    "CLAUDE.md senin yazdığın talimatlardır. **Auto memory** ise Claude'un "
                    "çalışırken kendisi için tuttuğu notlardır — build komutları, debugging "
                    "içgörüleri, mimari kararlar, kod stili tercihleri gibi bilgileri oturumlar "
                    "arasında biriktirmesini sağlar."
                ),
                table(
                    ["", "CLAUDE.md", "Auto Memory"],
                    [
                        ["Kim yazar?", "Sen (developer)", "Claude (otomatik)"],
                        ["Ne içerir?", "Build komutları, naming convention, proje kuralları", "Debugging notları, öğrenilen pattern'ler, tercih gözlemleri"],
                        ["Nerede saklanır?", "Proje dizininde (`./CLAUDE.md`) veya home (`~/.claude/`)", "`~/.claude/projects/<proje>/memory/`"],
                        ["Ne zaman yüklenir?", "Her oturum başında otomatik", "Her oturum başında (MEMORY.md index'i)"],
                        ["Versiyon kontrolü?", "Git ile paylaşılır (local hariç)", "Machine-local; git'e girmez"],
                        ["Düzenleme?", "Elle düzenlersin", "Elle düzenleyebilirsin veya `/memory` ile yönetirsin"],
                    ],
                ),
                keypoint(
                    "Auto memory varsayılan olarak açıktır (Claude Code v2.1.59+ gerektirir). "
                    "Her oturum başında `MEMORY.md` index dosyasının ilk 200 satırı veya 25KB'ı "
                    "(hangisi önce dolarsa) context'e yüklenir."
                ),
                p(
                    "**Depolama yapısı:** Auto memory `~/.claude/projects/<proje>/memory/` "
                    "dizininde tutulur. Bu dizinde bir `MEMORY.md` (index) ve isteğe bağlı "
                    "konu dosyaları (ör. `debugging.md`, `api-conventions.md`) bulunur. "
                    "Claude, MEMORY.md dolmaya başlayınca kendi kendine topic dosyalarına "
                    "ayırabilir."
                ),
                p(
                    "Aynı git repo'sunun tüm worktree'leri aynı memory dizinini paylaşır. "
                    "Ancak memory **makineler arası senkronize olmaz** — ofis bilgisayarındaki "
                    "ve ev bilgisayarındaki memory bağımsız birikir."
                ),
                warn(
                    "Auto memory deterministik değildir. Claude her oturumda not yazmaz; "
                    "gelecekte faydalı olacağına karar verirse yazar. \"3 oturum çalıştırdım "
                    "ama hiç memory yazmadı\" diye endişelenme — bu normal. `/memory` ile "
                    "mevcut durumu her zaman görebilirsin."
                ),
                tip(
                    "Topic dosyaları (debugging.md, api-conventions.md vb.) oturum başında "
                    "otomatik yüklenmez; Claude gerektiğinde okur. Yalnızca MEMORY.md index'i "
                    "her oturumda context'e girer."
                ),

                # 1.6
                h("1.6 Context'e Ne Yüklenir? (Zihinsel Model)"),
                p(
                    "Oturum başında Claude'un görebildiği kalıcı bağlam kabaca şu kaynaklardan "
                    "oluşur:"
                ),
                bullets([
                    "System prompt ve runtime talimatları",
                    "Yüklenen CLAUDE.md / CLAUDE.local.md dosyaları (tüm kapsamlar)",
                    "Koşulsuz `.claude/rules/` dosyaları (path'siz olanlar); path'li kurallar ise eşleşen dosya okunduğunda lazy-load",
                    "Auto memory index'i (MEMORY.md)",
                    "Aktif MCP tool adları, skill açıklamaları ve yapılandırma bilgileri",
                ]),
                p(
                    "Burada önemli nokta kesin iç sıra değil — Anthropic bunu yayımlamıyor — "
                    "**hangi bilginin context bütçesini tükettiğini bilmektir.** Çok uzun "
                    "CLAUDE.md dosyaları, çok sayıda koşulsuz rule ve şişmiş bir MEMORY.md "
                    "context'i daraltır ve Claude'un asıl işe ayırdığı alanı küçültür."
                ),
                warn(
                    "CLAUDE.md 200 satırı aşmaya başladıysa `/context` ile doluluk kontrolü "
                    "yap. Context bütçesinin büyük bölümünü talimat dosyaları yiyorsa: "
                    "split et, path-scoped rules'a taşı veya kısalt."
                ),

                # 1.7
                h("1.7 Hangi Bilgiyi Nereye Koymalıyım? (Karar Tablosu)"),
                p(
                    "Claude Code'da talimat ve otomasyon için birden fazla mekanizma var. "
                    "Hangisini ne zaman kullanacağını bilmek, gereksiz karmaşıklıktan kaçınmanın "
                    "anahtarıdır:"
                ),
                table(
                    ["İhtiyaç", "Doğru mekanizma"],
                    [
                        ["Her projede geçerli kişisel tercih (dil, stil)", "`~/.claude/CLAUDE.md`"],
                        ["Bu repoya ait takım kuralları (stack, convention)", "`./CLAUDE.md`"],
                        ["Commitlenmemesi gereken kişisel not (sandbox URL, test verisi)", "`CLAUDE.local.md`"],
                        ["Sadece test dosyalarında geçerli kural", "`.claude/rules/testing.md` + `paths` frontmatter"],
                        ["Claude'un kendi öğrendiği çalışma notları", "Auto memory (otomatik)"],
                        ["Her edit sonrası zorunlu komut (lint, format)", "Hook (Gün 12)"],
                        ["Uzun, tekrar eden workflow (deploy, review)", "Skill veya custom command (Gün 6)"],
                        ["AGENTS.md / .cursorrules uyumluluğu", "`@AGENTS.md` import veya symlink"],
                    ],
                ),
            ],
        },

        # -----------------------------------------------------------------
        # BÖLÜM 2 — PRATİK: ADIM ADIM
        # -----------------------------------------------------------------
        {
            "num": "BÖLÜM 2",
            "title": "PRATİK — ADIM ADIM",
            "blocks": [
                # 2.1
                h("2.1 Global (User) CLAUDE.md Oluşturma"),
                p(
                    "İlk adım olarak tüm projelerde geçerli olacak kişisel tercihlerini "
                    "tanımlayalım. Bu dosya `~/.claude/CLAUDE.md` konumunda yaşar:"
                ),
                steps([
                    "Terminal'de `~/.claude/` dizininin varlığını kontrol et: `ls ~/.claude/`",
                    "Dosyayı oluştur veya düzenle: `nano ~/.claude/CLAUDE.md` (veya favori editörün)",
                    "Temel tercihlerini yaz (aşağıdaki örneği referans al)",
                    "Kaydet ve Claude Code'u aç — `/memory` ile dosyanın yüklendiğini doğrula",
                ]),
                code(
                    "# Kişisel Tercihlerim\n\n"
                    "## Genel\n"
                    "- Türkçe yanıt ver (teknik terimler İngilizce kalabilir)\n"
                    "- Değişiklik yapmadan önce mevcut kodu oku ve anla\n"
                    "- Her adımda ne yaptığını kısaca açıkla\n\n"
                    "## Kod Stili\n"
                    "- Python tercih et (gerekmedikçe başka dil kullanma)\n"
                    "- Type hints zorunlu\n"
                    "- Docstring her public fonksiyona\n"
                    "- 4 boşluk indent, satır uzunluğu max 100",
                    "markdown",
                ),

                # 2.2
                h("2.2 Proje CLAUDE.md Oluşturma — Manuel Yöntem"),
                p(
                    "Şimdi spesifik bir proje için kuralları tanımlayalım. CLI not defteri v1 "
                    "projeni aç ve kök dizinde bir `CLAUDE.md` oluştur:"
                ),
                steps([
                    "Proje dizinine geç: `cd ~/projects/cli-notes` (kendi dizinin ne ise)",
                    "CLAUDE.md oluştur: `nano CLAUDE.md`",
                    "Proje bilgilerini yaz: stack, klasör yapısı, build/test komutları, kurallar",
                    "Git'e ekle: `git add CLAUDE.md && git commit -m 'feat: add CLAUDE.md'`",
                ]),
                code(
                    "# CLI Not Defteri — Proje Kuralları\n\n"
                    "## Stack\n"
                    "- Python 3.12+\n"
                    "- SQLite (veritabanı)\n"
                    "- click (CLI framework) — henüz eklenmemişse argparse kullan\n\n"
                    "## Build & Test\n"
                    "- Kurulum: `pip install -r requirements.txt`\n"
                    "- Çalıştır: `python main.py`\n"
                    "- Test: `pytest tests/`\n\n"
                    "## Kurallar\n"
                    "- Her fonksiyona type hints ekle\n"
                    "- Her public fonksiyona docstring yaz\n"
                    "- Error handling zorunlu: bare `except:` kullanma, spesifik exception yakala\n"
                    "- Dosya I/O işlemlerinde context manager (`with`) kullan\n"
                    "- Değişken/fonksiyon isimleri snake_case\n"
                    "- Commit mesajları Conventional Commits formatında",
                    "markdown",
                ),
                tip(
                    "CLAUDE.md'yi yazdıktan sonra Claude Code'a şu prompt'u ver: "
                    "\"CLAUDE.md'yi oku ve özetle.\" Claude kuralları doğru anlıyor mu, "
                    "kontrol et."
                ),

                # 2.3
                h("2.3 /init ile Otomatik CLAUDE.md Üretimi"),
                p(
                    "Her projeye elle CLAUDE.md yazmak yerine `/init` komutunu kullanabilirsin. "
                    "Claude projeyi analiz eder ve sana uygun bir CLAUDE.md önerir:"
                ),
                steps([
                    "Proje dizininde Claude Code'u aç",
                    "`/init` yaz ve Enter'a bas",
                    "Claude projeyi tarar: package.json, requirements.txt, Makefile, mevcut AGENTS.md vb.",
                    "Önerdiği CLAUDE.md'yi incele — eksik kuralları ekle, gereksizleri çıkar",
                    "Onaylarsan Claude dosyayı oluşturur",
                ]),
                code(
                    "# /init çıktısı örneği:\n"
                    "> /init\n"
                    "I'll analyze your project to create a CLAUDE.md file.\n"
                    "Found: requirements.txt, pytest.ini, .gitignore\n"
                    "Detected: Python project with pytest\n\n"
                    "Proposed CLAUDE.md:\n"
                    "---\n"
                    "# Project: cli-notes\n"
                    "## Build\n"
                    "- Install: pip install -r requirements.txt\n"
                    "- Test: pytest\n"
                    "...\n"
                    "---\n"
                    "Write this file? (y/n)",
                    "text",
                ),
                tip(
                    "`CLAUDE_CODE_NEW_INIT=1` environment variable'ı ile interaktif multi-phase "
                    "flow aktif olur: Claude sadece CLAUDE.md değil, skill ve hook önerileri de "
                    "sunar. İleri günlerde bunu kullanacağız."
                ),

                # 2.4
                h("2.4 CLAUDE.md'li vs CLAUDE.md'siz Karşılaştırma"),
                p(
                    "CLAUDE.md'nin etkisini en iyi görebileceğin yöntem: aynı prompt'u "
                    "bir kez CLAUDE.md olmadan, bir kez de CLAUDE.md ile çalıştırmak."
                ),
                steps([
                    "CLAUDE.md'yi geçici olarak devre dışı bırak: `mv CLAUDE.md CLAUDE.md.bak`",
                    "Claude Code'u aç ve şu prompt'u ver: `\"Bu projeye bir 'search' komutu ekle: notlar arasında anahtar kelimeyle arama yapsın\"`",
                    "Claude'un ürettiği kodu incele: type hints var mı? Docstring var mı? Naming convention doğru mu?",
                    "Oturumu kapat, CLAUDE.md'yi geri getir: `mv CLAUDE.md.bak CLAUDE.md`",
                    "Aynı prompt'u tekrar ver ve farkı gözlemle",
                ]),
                p(
                    "Alternatif olarak `claude --bare` flag'ini kullanabilirsin — bu, tüm "
                    "özelleştirmeleri (CLAUDE.md, skills, hooks, MCP, auto memory) devre dışı "
                    "bırakarak sorun gidermeye de yarar."
                ),
                keypoint(
                    "CLAUDE.md'nin etkisi kümülatiftir: tek bir kural küçük bir fark yapar, "
                    "ama 10-15 somut kural birlikte ciddi tutarlılık sağlar. \"Kodu düzgün yaz\" "
                    "gibi belirsiz talimatlar yerine \"type hints + docstring + snake_case + "
                    "max 100 karakter\" gibi ölçülebilir kurallar yaz."
                ),

                # 2.5
                h("2.5 /memory ile Yüklenen Dosyaları Görüntüleme"),
                p(
                    "`/memory` komutu, Claude'un bu oturumda hangi talimat dosyalarını "
                    "gördüğünü listelemeni ve auto memory'yi yönetmeni sağlar:"
                ),
                steps([
                    "Claude Code'da `/memory` yaz ve Enter'a bas",
                    "Listelenen dosyaları incele: user CLAUDE.md, project CLAUDE.md, auto memory dosyaları",
                    "Auto memory toggle'ını gör: açık mı kapalı mı",
                    "\"Open memory folder\" seçeneği ile memory dizinini dosya yöneticisinde aç",
                ]),
                code(
                    "> /memory\n\n"
                    "Memory files loaded:\n"
                    "  ~/.claude/CLAUDE.md (user)\n"
                    "  ./CLAUDE.md (project)\n"
                    "  ~/.claude/projects/cli-notes/memory/MEMORY.md (auto memory)\n\n"
                    "Auto memory: enabled\n"
                    "  [Toggle auto memory]  [Open memory folder]",
                    "text",
                ),

                # 2.6
                h("2.6 /context ile Context Doluluk Kontrolü"),
                p(
                    "`/context` komutu context penceresinin ne kadar dolu olduğunu ve "
                    "hangi kaynakların ne kadar yer kapladığını gösterir:"
                ),
                steps([
                    "Claude Code'da `/context` yaz",
                    "CLAUDE.md dosyalarının ve auto memory'nin kapladığı alanı incele",
                    "Toplam doluluk yüzdesine bak — %20'nin altındaysa rahat edersin",
                ]),
                warn(
                    "CLAUDE.md + rules + auto memory toplamı context bütçesinin büyük bölümünü "
                    "kaplıyorsa Claude'un asıl işe (kod okuma, düzenleme) ayırabileceği alan "
                    "daralır. Bu durumda talimatları kısalt, path-scoped rules'a taşı veya "
                    "MEMORY.md'yi elle temizle."
                ),

                # 2.7
                h("2.7 Import Sözdizimi (@path)"),
                p(
                    "CLAUDE.md dosyaları `@path/to/file` sözdizimi ile başka dosyaları import "
                    "edebilir. Bu, organizasyon sağlar — büyük bir CLAUDE.md'yi bölümlere "
                    "ayırabilir veya mevcut dokümanları referans olarak ekleyebilirsin:"
                ),
                code(
                    "# CLAUDE.md içinde import örnekleri\n\n"
                    "## Proje Bilgisi\n"
                    "@README.md\n\n"
                    "## API Standartları\n"
                    "@docs/api-guidelines.md\n\n"
                    "## Paket Bilgisi\n"
                    "@package.json",
                    "markdown",
                ),
                keypoint(
                    "Import dosyaları yalnızca organizasyon içindir; context maliyetini düşürmez. "
                    "Import edilen içerik de oturum başında yüklenir ve context bütçesini tüketir. "
                    "Context azaltmak istiyorsan path-scoped rules veya daha kısa talimatlar kullan."
                ),
                tip(
                    "Backtick içindeki `@path` import edilmez, literal metin olarak kalır. "
                    "Yani CLAUDE.md'de import sözdizimini öğretmek istiyorsan backtick kullan: "
                    "`@README.md`."
                ),
            ],
        },

        # -----------------------------------------------------------------
        # BÖLÜM 3 — PRATİK: DERİNLEŞ / UYGULAMA
        # -----------------------------------------------------------------
        {
            "num": "BÖLÜM 3",
            "title": "PRATİK — DERİNLEŞ / UYGULAMA",
            "blocks": [
                # 3.1
                h("3.1 .claude/rules/ ile Path-Scoped Kurallar"),
                p(
                    "Büyük projelerde her kuralın her dosyada yüklenmesi gereksizdir. Örneğin "
                    "test kuralları yalnızca test dosyaları okunduğunda geçerli olmalı. "
                    "`.claude/rules/` dizini bu ihtiyacı karşılar:"
                ),
                steps([
                    "Proje dizininde `.claude/rules/` klasörünü oluştur: `mkdir -p .claude/rules`",
                    "Bir test kuralı dosyası oluştur: `nano .claude/rules/testing.md`",
                    "YAML frontmatter'a `paths` ekle — hangi dosyalar okunduğunda yüklenmeli",
                    "Kuralları yaz ve kaydet",
                    "Git'e ekle: `git add .claude/rules/ && git commit -m 'feat: add path-scoped test rules'`",
                ]),
                code(
                    "---\n"
                    "paths:\n"
                    "  - tests/**\n"
                    "  - test_*.py\n"
                    "---\n\n"
                    "# Test Kuralları\n\n"
                    "- Framework: pytest kullan (unittest değil)\n"
                    "- Her test fonksiyonuna açıklayıcı docstring yaz\n"
                    "- Test isimleri `test_<ne_test_ediliyor>_<beklenen_sonuç>` formatında\n"
                    "- Fixture'ları `conftest.py`'de topla\n"
                    "- Coverage hedefi: %80+\n"
                    "- Mock kullanırken `unittest.mock.patch` tercih et",
                    "yaml",
                ),
                keypoint(
                    "Path'siz kurallar (YAML frontmatter'da `paths` yok) her oturumda "
                    "koşulsuz yüklenir — tıpkı CLAUDE.md gibi. Path'li kurallar ise yalnızca "
                    "eşleşen bir dosya okunduğunda context'e girer. Bu sayede context bütçesini "
                    "verimli kullanırsın."
                ),
                p(
                    "İkinci bir örnek — API tasarım kuralları:"
                ),
                code(
                    "---\n"
                    "paths:\n"
                    "  - src/api/**\n"
                    "  - routes/**\n"
                    "---\n\n"
                    "# API Tasarım Kuralları\n\n"
                    "- RESTful URL yapısı: `/api/v1/<resource>`\n"
                    "- HTTP status kodlarını doğru kullan (201 create, 404 not found, 422 validation)\n"
                    "- Response format: `{\"data\": ..., \"error\": null}` veya `{\"data\": null, \"error\": {\"message\": ...}}`\n"
                    "- Validation hatalarında detaylı alan bilgisi dön",
                    "yaml",
                ),
                p(
                    "`claudeMdExcludes` ayarı ile belirli CLAUDE.md veya rule dosyalarını "
                    "glob pattern ile hariç tutabilirsin. Bu, monorepo'larda başka takımın "
                    "kurallarını almak istemediğinde faydalıdır:"
                ),
                code(
                    "// .claude/settings.local.json\n"
                    "{\n"
                    "  \"claudeMdExcludes\": [\n"
                    "    \"**/other-team/CLAUDE.md\",\n"
                    "    \"/home/user/monorepo/legacy/.claude/rules/**\"\n"
                    "  ]\n"
                    "}",
                    "json",
                ),

                # 3.2
                h("3.2 CLAUDE.local.md ile Kişisel Tercihler"),
                p(
                    "`CLAUDE.local.md` git'e commitlenmemesi gereken kişisel notlar içindir. "
                    "Sandbox URL'lerin, kişisel test verilerin veya çalışma ortamına özel "
                    "ayarların buraya gider:"
                ),
                steps([
                    "Proje dizininde `CLAUDE.local.md` oluştur",
                    "`.gitignore`'a ekle: `echo 'CLAUDE.local.md' >> .gitignore`",
                    "Kişisel notlarını yaz (sandbox URL, test kullanıcısı vb.)",
                ]),
                code(
                    "# Kişisel Notlarım (commitlenmesin)\n\n"
                    "- Dev sunucu: http://localhost:8000\n"
                    "- Test DB: ~/dev/test-notes.db\n"
                    "- Debug modunda çalıştır: `python main.py --debug`",
                    "markdown",
                ),
                warn(
                    "`CLAUDE.local.md` gitignore'da olsa bile **secret store değildir.** "
                    "API key, production token, müşteri verisi veya şifre yazmayın. Bunlar "
                    "için environment variable (`.env` + `python-dotenv`) veya secret manager "
                    "kullanın. Aynı kural auto memory için de geçerlidir — Claude hassas veriyi "
                    "memory'ye yazmamalı; yanlışlıkla yazarsa `/memory` ile silebilirsiniz."
                ),
                tip(
                    "`/init` çalıştırıldığında \"personal\" seçeneği `CLAUDE.local.md`'yi "
                    "otomatik oluşturur ve `.gitignore`'a ekler — elle yapmana gerek kalmaz."
                ),

                # 3.3
                h("3.3 Auto Memory'yi Gözlemle ve Düzenle"),
                p(
                    "Auto memory zamanla birikir. Birkaç oturum çalıştırdıktan sonra Claude'un "
                    "neler öğrendiğini incelemek ve gerekirse düzeltmek iyi bir pratiktir:"
                ),
                steps([
                    "Birkaç oturum boyunca CLI not defteri üzerinde çalış (not ekle, listele, sil gibi farklı görevler ver)",
                    "Oturumlar sırasında terminal'de \"Writing memory\" mesajını gözle — her oturumda yazması garanti değildir, Claude faydalı olacağına karar verirse yazar",
                    "`/memory` ile auto memory klasörünü aç ve `MEMORY.md`'yi incele",
                    "Yanlış veya istenmeyen bir not varsa elle düzenle (dosya normal bir markdown)",
                ]),
                code(
                    "# Auto memory dizin yapısı örneği\n"
                    "~/.claude/projects/cli-notes/memory/\n"
                    "├── MEMORY.md          # Index — her oturum başında yüklenir\n"
                    "├── debugging.md       # Claude'un debugging notları (lazy-load)\n"
                    "└── code-patterns.md   # Kod pattern'leri (lazy-load)",
                    "text",
                ),
                code(
                    "# MEMORY.md içeriği örneği\n"
                    "- Project uses SQLite via sqlite3 stdlib; no ORM\n"
                    "- Build: python main.py; tests: pytest tests/\n"
                    "- User prefers Turkish variable names for UI strings\n"
                    "- argparse is used for CLI; click migration planned\n"
                    "- See debugging.md for common DB locking issues",
                    "markdown",
                ),
                p(
                    "Auto memory'yi kapatmak veya açmak için iki yol var:"
                ),
                code(
                    "# Yöntem 1: /memory komutu ile toggle\n"
                    "> /memory\n"
                    "  → [Toggle auto memory]\n\n"
                    "# Yöntem 2: settings.json ile\n"
                    "// .claude/settings.json\n"
                    "{\n"
                    "  \"autoMemoryEnabled\": false\n"
                    "}",
                    "text",
                ),
                warn(
                    "Auto memory machine-local'dir. Başka bir makinede çalışırsan oradaki "
                    "memory bağımsız birikir. Kritik proje kurallarını auto memory'ye "
                    "bırakma — onları CLAUDE.md'ye yaz ki tüm takım ve tüm makineler "
                    "aynı kuralları görsün."
                ),

                # 3.4
                h("3.4 Troubleshooting: Talimat Neden Çalışmıyor?"),
                p(
                    "CLAUDE.md yazdın ama Claude kuralları yoksayıyor gibi mi? "
                    "Yaygın sorunlar ve çözümleri:"
                ),
                table(
                    ["Sorun", "Olası sebep", "Çözüm"],
                    [
                        [
                            "CLAUDE.md hiç okunmuyor",
                            "Dosya yanlış konumda veya adı yanlış yazılmış",
                            "`/memory` ile yüklenen dosyaları kontrol et",
                        ],
                        [
                            "Kural bazen uygulanıyor bazen değil",
                            "İki dosyada çelişkili talimat var",
                            "Tüm CLAUDE.md ve rule dosyalarını gözden geçir; çelişkileri gider",
                        ],
                        [
                            "Compaction sonrası kural unutuluyor",
                            "Kural alt dizin CLAUDE.md'sinde; compaction sonrası lazy-load bekliyor",
                            "Kritik kuralları proje kök CLAUDE.md'ye taşı (compaction sonrası yeniden yüklenir)",
                        ],
                        [
                            "Path-scoped rule yüklenmiyor",
                            "Glob pattern dosya yolunu eşlemiyor",
                            "`paths:` frontmatter'daki pattern'i kontrol et (ör. `tests/**` vs `tests/*`)",
                        ],
                        [
                            "Claude talimatı anlıyor ama uygulamıyor",
                            "CLAUDE.md context, hook değil; Claude \"çoğunlukla\" uyar",
                            "Zorunlu aksiyon ise hook yaz (Gün 12); aksi halde talimatı daha somut yap",
                        ],
                    ],
                ),
                tip(
                    "`InstructionsLoaded` hook ile hangi dosyaların ne zaman yüklendiğini "
                    "loglayabilirsin. Bu ileri bir yöntemdir ve hook detaylarını Gün 12'de "
                    "işleyeceğiz; ama troubleshooting ihtiyacın varsa resmi hook dokümantasyonuna "
                    "bakabilirsin."
                ),
            ],
        },
    ],

    # -------------------------------------------------------------------------
    # PROMPT KÜTÜPHANESİ
    # -------------------------------------------------------------------------
    "prompts": [
        {
            "title": "Proje CLAUDE.md Oluştur",
            "prompt": (
                "Bu proje Python 3.12+, FastAPI, SQLite kullanıyor. Type hints zorunlu, "
                "docstring zorunlu. Build: `pip install -r requirements.txt && uvicorn main:app`. "
                "Test: `pytest`. Naming: snake_case. Error handling: spesifik exception "
                "yakala, bare except kullanma. Bu bilgilerle 200 satırı geçmeyen bir "
                "CLAUDE.md oluştur."
            ),
            "note": (
                "Claude'un oluşturduğu CLAUDE.md'yi mutlaka gözden geçir; eksik veya yanlış "
                "kuralları düzelt."
            ),
        },
        {
            "title": "/init Sonrası İyileştirme",
            "prompt": (
                "/init ile üretilen CLAUDE.md'yi oku. Eksik olan naming convention ve "
                "error handling kurallarını ekle. Ayrıca test komutunu `pytest --cov` olarak "
                "güncelle. Dosya 200 satırı geçmesin."
            ),
        },
        {
            "title": "CLAUDE.md'siz vs CLAUDE.md'li Karşılaştırma",
            "prompt": (
                "Bu projeye bir 'search' komutu ekle: notlar arasında anahtar kelimeyle "
                "arama yapsın, eşleşen notları tarih sırasıyla göstersin."
            ),
            "note": (
                "Bu prompt'u önce CLAUDE.md olmadan (mv ile rename et veya --bare flag), "
                "sonra CLAUDE.md ile çalıştır. Type hints, docstring ve naming convention "
                "farkını karşılaştır."
            ),
        },
        {
            "title": "Auto Memory İnceleme",
            "prompt": (
                "/memory ile auto memory'de ne olduğunu göster. Yanlış veya güncel olmayan "
                "bir not varsa sil. Hangi dosyaların yüklendiğini listele."
            ),
        },
        {
            "title": "Path-Scoped Rule Oluştur",
            "prompt": (
                "`.claude/rules/testing.md` oluştur: `tests/` altındaki dosyalar okunduğunda "
                "yüklensin. Kurallar: pytest kullan, her test fonksiyonuna docstring zorunlu, "
                "fixture'lar conftest.py'de olsun, coverage hedefi %80+."
            ),
            "note": (
                "Oluşturulan dosyanın YAML frontmatter'ını kontrol et: `paths:` alanı "
                "doğru glob pattern'leri içermeli."
            ),
        },
    ],

    # -------------------------------------------------------------------------
    # CHALLENGE
    # -------------------------------------------------------------------------
    "challenge": {
        "title": "CHALLENGE: CLI Not Defteri v1'e CLAUDE.md Ekosistemi Kur",
        "task": (
            "Gün 2'de oluşturduğun CLI not defteri v1 projesine tam bir CLAUDE.md ekosistemi kur. "
            "Proje kuralları, path-scoped test kuralları ve Claude yardımıyla refactoring — "
            "hepsini uçtan uca uygula."
        ),
        "requirements": [
            "Proje kök dizininde CLAUDE.md oluştur (en az 5 somut, test edilebilir talimat)",
            ".claude/rules/ altında en az 1 path-scoped rule dosyası oluştur",
            "Claude'dan kodu CLAUDE.md kurallarına göre refactor etmesini iste",
            "Refactor sonrası programın hâlâ çalıştığını doğrula (test veya manuel smoke check)",
            "git diff ile değişiklikleri incele ve hangi kuralın hangi değişikliğe yol açtığını açıkla",
            "/memory ile CLAUDE.md'nin yüklenen dosyalar listesinde göründüğünü doğrula",
        ],
        "success": [
            "`./CLAUDE.md` mevcut ve en az 5 somut, test edilebilir talimat içeriyor",
            "`.claude/rules/` altında en az 1 path-scoped `.md` dosyası var ve `paths` frontmatter'ı doğru",
            "Claude'dan yapılan refactor, CLAUDE.md kurallarından en az 2 tanesini görünür biçimde uyguluyor (ör. type hints eklendi, docstring eklendi)",
            "Test veya manuel smoke check başarılı — program hatasız çalışıyor",
            "`git diff` üzerinden hangi kuralın hangi değişikliğe yol açtığı açıklanabiliyor",
            "`/memory` çalıştırıldığında CLAUDE.md dosyası listede görünüyor",
        ],
        "solution": {
            "intro": (
                "Üç adımda ilerle: önce kuralları tanımla, sonra Claude'a refactor ettir, "
                "son olarak doğrula. Aşağıdaki prompt zinciri tipik akışı gösterir."
            ),
            "prompts": [
                {
                    "title": "1) CLAUDE.md oluştur",
                    "prompt": (
                        "Bu proje Python 3.12+ ve SQLite kullanan bir CLI not defteri. "
                        "Şu kurallarla bir CLAUDE.md oluştur: type hints zorunlu, her public "
                        "fonksiyona docstring yaz, error handling'de spesifik exception kullan, "
                        "dosya I/O'da context manager kullan, değişkenler snake_case olsun, "
                        "commit mesajları Conventional Commits formatında. Build: "
                        "`python main.py`, Test: `pytest tests/`."
                    ),
                },
                {
                    "title": "2) Path-scoped rule oluştur",
                    "prompt": (
                        "`.claude/rules/testing.md` oluştur. `tests/` altındaki dosyalar "
                        "okunduğunda yüklensin. Kurallar: pytest framework, her test "
                        "fonksiyonuna docstring, test ismi `test_<ne>_<beklenti>` formatında, "
                        "fixture'lar conftest.py'de."
                    ),
                },
                {
                    "title": "3) Refactor ettir",
                    "prompt": (
                        "CLAUDE.md'deki kurallara göre tüm projeyi refactor et. Eksik type "
                        "hints ekle, docstring yaz, bare except varsa spesifik exception'a "
                        "çevir, dosya I/O'larda context manager kullan. Her değişikliği "
                        "kısaca açıkla."
                    ),
                },
            ],
            "notes": [
                "Type hints örneği: `def add_note(title: str, content: str) -> int:` — "
                "return type'ı da belirt.",
                "Docstring örneği: Google style veya NumPy style — CLAUDE.md'de hangisini "
                "tercih ettiğini belirtebilirsin.",
                "Auto memory bu challenge sırasında not yazıp yazmayacağını garanti edemezsin — "
                "bu başarı kriteri değil, bonus gözlem.",
            ],
            "pitfalls": [
                "CLAUDE.md'yi çok uzun veya belirsiz yazmak — 200 satırı geçme, somut kurallar yaz.",
                "Çelişkili kurallar — ör. bir yerde 'docstring zorunlu', başka yerde 'kısa ve öz yaz' "
                "gibi zıt talimatlar Claude'u kararsız bırakır.",
                "Path glob hatası — `tests/` yalnızca dizini eşler, dosyaları değil. "
                "Dosyalar için `tests/**` veya `test_*.py` kullan.",
                "CLAUDE.local.md'ye secret yazmak — .gitignore'da olsa bile güvenli değildir, "
                "secret'lar environment variable'da tutulmalı.",
            ],
        },
    },

    # -------------------------------------------------------------------------
    # TAKEAWAYS
    # -------------------------------------------------------------------------
    "takeaways": [
        "CLAUDE.md Claude Code'un kalıcı hafızasıdır: her oturum başında okunur ve davranışı yönlendirir, ama hook gibi zorunlu kılmaz.",
        "Dört kapsam vardır: managed policy (organizasyon), user (kişisel, tüm projeler), project (takım, bu repo), local (kişisel, bu repo, gitignore).",
        "Etkili CLAUDE.md: 200 satır altı, somut kurallar, çelişkisiz. \"Kodu düzgün yaz\" değil, \"type hints + docstring + snake_case\" yaz.",
        "Auto memory Claude'un kendi tuttuğu notlardır; deterministic değildir, her oturumda yazmaz. MEMORY.md index'i oturum başında yüklenir (200 satır / 25KB).",
        ".claude/rules/ ile path-scoped kurallar tanımlarsın: `paths` frontmatter'ı olan kurallar yalnızca eşleşen dosyalar okunduğunda yüklenir — context tasarrufu sağlar.",
        "Import (@path) organizasyon içindir, context maliyetini düşürmez. Import edilen içerik de oturum başında yüklenir.",
        "/memory komutu yüklenen tüm talimat dosyalarını listeler, auto memory toggle'ı sunar. /context ile doluluk kontrolü yapılır.",
        "CLAUDE.local.md ve auto memory secret store değildir — API key, token, şifre yazmayın; environment variable veya secret manager kullanın.",
    ],

    # -------------------------------------------------------------------------
    # READING
    # -------------------------------------------------------------------------
    "reading": {
        "official": [
            {
                "label": "Memory: CLAUDE.md & Auto Memory (Resmi Docs)",
                "url": "https://code.claude.com/docs/en/memory",
            },
            {
                "label": "Explore the .claude Directory",
                "url": "https://code.claude.com/docs/en/claude-directory",
            },
            {
                "label": "Context Window — Ne yüklenir, ne zaman compact olur",
                "url": "https://code.claude.com/docs/en/context-window",
            },
            {
                "label": "Settings — Ayarlar, kapsamlar ve öncelik sırası",
                "url": "https://code.claude.com/docs/en/settings",
            },
        ],
        "community": [
            {
                "label": "Best Practices (Resmi)",
                "url": "https://code.claude.com/docs/en/best-practices",
            },
            {
                "label": "Large Codebases — Monorepo ve büyük proje stratejileri",
                "url": "https://code.claude.com/docs/en/large-codebases",
            },
        ],
        "extra": [
            {
                "label": "ClaudeLog — Topluluk best practices",
                "url": "https://claudelog.com/",
            },
            {
                "label": "Awesome Claude Code (küratörlü liste)",
                "url": "https://github.com/hesreallyhim/awesome-claude-code",
            },
        ],
    },

    # -------------------------------------------------------------------------
    # NEXT PREVIEW
    # -------------------------------------------------------------------------
    "next_preview": (
        "Proje Klasör Yapısı ve Başlangıç Şablonu — Yarın ideal klasör düzenini, "
        ".claude/ dizininin tüm alt bileşenlerini (commands, skills, agents, workflows, rules) "
        "ve Claude'un seni \"mülakat ederek\" PRD.md üretmesini öğreneceksin. "
        "Todo App projesi (Kademe 2) burada başlıyor."
    ),

    # -------------------------------------------------------------------------
    # CHECKLIST
    # -------------------------------------------------------------------------
    "checklist": [
        "CLAUDE.md'nin ne olduğunu ve neden her oturum başında yüklendiğini açıklayabiliyorum",
        "Dört kapsamı (managed → user → project → local) ve yüklenme mantığını biliyorum",
        "~/.claude/CLAUDE.md (user) dosyası oluşturdum",
        "Proje dizininde ./CLAUDE.md oluşturdum (manuel veya /init ile)",
        "CLAUDE.md'li vs CLAUDE.md'siz farkı gözlemledim",
        "Auto memory'nin ne olduğunu, nerede saklandığını ve deterministik olmadığını biliyorum",
        "/memory komutuyla yüklenen dosyaları listeledim",
        ".claude/rules/ altında path-scoped bir kural oluşturdum",
        "\"Hangi bilgiyi nereye koymalı?\" karar tablosunu biliyorum (CLAUDE.md vs rule vs hook vs skill)",
        "Günün challenge'ını tamamladım (CLI not defteri v1'e CLAUDE.md ekosistemi)",
    ],
}
