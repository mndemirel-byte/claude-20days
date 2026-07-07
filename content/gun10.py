# content/gun10.py
# Tek kaynak: LESSON sözlüğü. generators/render_html.py ve generators/render_json.py
# bu sözlükten HTML + JSON üretir.
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from generators.schema import h, p, keypoint, tip, warn, bullets, steps, code, table


LESSON = {
    "day": 10,
    "total_days": 20,
    "week": 2,
    "slug": "todo-app-fullstack-deploy",
    "title": "Orta Seviye Proje: Todo App Full-stack + Deploy",
    "tagline": "Öğrendiklerini birleştir, gerçek bir uygulama gönder",
    "tier": "🟡 Kademe 2 Tamamlama",
    "date_label": "Temmuz 2026",

    "intro": (
        "Gün 4'te iskeletini kurduğun, Gün 5-9 arasında git workflow'u, custom command'lar, "
        "context yönetimi, debugging/test ve GitHub MCP ile beslediğin Todo App'i bugün "
        "bitiriyorsun: backend CRUD'u tamamlayacak, frontend'i buna bağlayacak ve uygulamayı "
        "gerçek bir URL üzerinden canlıya alacaksın. Bugünün asıl becerisi kod yazmak değil — "
        "bir önceki adımın çıktısını bir sonraki adımın girdisi yapan prompt zincirini kurmak "
        "ve 'çalışıyor' ile 'production-ready' arasındaki farkı görmek."
    ),

    "flow": [
        {"phase": "1 · Teori + Durum Tespiti", "dur": "25 dk",
         "desc": "Full-stack strateji, prompt zinciri deseni, deploy seçenekleri karşılaştırması, repo'nun mevcut durumunu Claude'a çıkarttırma"},
        {"phase": "2 · Build: Backend Tamamlama", "dur": "50 dk",
         "desc": "Kalan CRUD endpoint'leri, validation, hata yönetimi, lokal test"},
        {"phase": "3 · Build: Frontend Entegrasyonu", "dur": "45 dk",
         "desc": "API servis katmanı, environment variable tabanlı base URL, CORS, uçtan uca lokal akış"},
        {"phase": "4 · Ship: Deploy + Review + İyileştirme", "dur": "45 dk",
         "desc": "Render'a deploy, canlı URL doğrulama, review + 5 iyileştirme önerisi, README"},
    ],

    "prerequisites": [
        "Gün 1-9 tamamlanmış: Claude Code kurulu, CLAUDE.md hazır, git workflow ve custom command'lar kurulu",
        "Todo App proje iskeleti mevcut (Gün 4), backend/frontend kısmi olarak yazılmış olmalı",
        "GitHub hesabı ve uzak repo (Gün 5, Gün 9'da kullanıldı)",
        "Ücretsiz bir Render hesabı (render.com) — deploy için gerekli",
    ],
    "tools_needed": [
        "Terminal + Claude Code çalışır durumda",
        "Python 3.11+ ve pip (FastAPI backend için)",
        "Node.js (React/TypeScript frontend kullanıyorsan)",
        "Git ve GitHub CLI (opsiyonel)",
        "Render hesabı ve tarayıcı",
    ],

    "objectives": [
        "Todo App'in backend CRUD API'sini (create/read/update/delete) eksiksiz çalışır hale getirebileceksin",
        "Prompt zinciri tekniğiyle bir adımın çıktısını bir sonraki adımın girdisi yapan çok adımlı bir geliştirme akışı yürütebileceksin",
        "Frontend'i backend API'sine environment variable tabanlı bir base URL ile bağlayıp CORS'u doğru yapılandırabileceksin",
        "FastAPI backend'i Render Web Service olarak deploy edip canlı bir URL alabileceksin",
        "Render'ın ephemeral filesystem sınırını ve SQLite'ın bu bağlamdaki veri kalıcılığı riskini değerlendirebileceksin",
        "Claude Code'dan production-readiness analizi alıp önerilen iyileştirmelerden en az 3'ünü uygulayabileceksin",
    ],

    "sections": [
        {
            "num": "BÖLÜM 1",
            "title": "TEORİK TEMEL",
            "blocks": [
                h("1.1 Full-stack Geliştirme Stratejisi: Hangi Sırayla Ne Yapılır"),
                p(
                    "İki temel sıralama var: backend-first (önce API contract'ı ve veri modelini sabitle, "
                    "sonra frontend bunu tüketir) ve frontend-first (önce UI akışını kur, mock data ile "
                    "çalıştır, sonra gerçek API'ye bağla). Todo App gibi veri modeli net olan CRUD "
                    "uygulamalarında backend-first daha az rework gerektirir: API contract'ı bir kez "
                    "belirlenir, frontend ona göre yazılır. UI akışı belirsizse veya paralel çalışan iki "
                    "kişi varsa frontend-first + mock data daha hızlı geri bildirim verir."
                ),
                table(
                    ["Yaklaşım", "Ne zaman uygun", "Risk"],
                    [
                        ["Backend-first", "Veri modeli net, tek geliştirici/tek Claude oturumu", "Frontend geç başlar, UI sorunları geç görülür"],
                        ["Frontend-first + mock", "UI akışı belirsiz, paralel çalışma var", "Mock ile gerçek API arasında contract kayması riski"],
                    ],
                ),
                h("1.2 İteratif Geliştirme ve Prompt Zinciri"),
                p(
                    "Tek dev bir promptla 'Todo App'i bitir' demek, Claude'un neyi öncelikleyeceğini "
                    "tahmin etmesini gerektirir ve genelde eksik/tutarsız sonuç verir. Prompt zinciri "
                    "deseni bunun yerine küçük, doğrulanabilir adımlar zincirler: her adımın çıktısı "
                    "(değiştirilen dosyalar, çalışan endpoint, geçen test) bir sonraki promptun bağlamı "
                    "olur. Bu, Gün 2'de öğrendiğin 'Goal/Scope/Requirements/Verification/Done' yapısının "
                    "çok adımlı bir projeye ölçeklenmiş hâlidir."
                ),
                table(
                    ["Adım", "Girdi", "Çıktı → sonraki adımın girdisi"],
                    [
                        ["1. Durum tespiti", "Mevcut repo", "Eksikler listesi"],
                        ["2. Backend tamamla", "Eksikler listesi", "Çalışan CRUD API"],
                        ["3. Frontend bağla", "API contract + çalışan endpoint'ler", "Uçtan uca çalışan lokal uygulama"],
                        ["4. Deploy et", "Lokal çalışan uygulama", "Canlı URL"],
                        ["5. Review + iyileştir", "Canlı uygulama", "Uygulanmış iyileştirmeler"],
                    ],
                ),
                keypoint(
                                        "Prompt zincirinde her adımdan sonra doğrulama yap (test çalıştır, endpoint'i çağır, "
                    "sayfayı aç) — bir adımın çıktısını doğrulamadan bir sonrakine geçmek, hataların "
                    "birikerek son adımda (deploy'da) ortaya çıkmasına yol açar."
                ),
                h("1.3 Deploy Kararı: Render / GitHub Pages / Vercel+Render"),
                p(
                    "Todo App'in backend'i (FastAPI + SQLite) bir sunucu süreci gerektirdiği için statik "
                    "hosting yeterli değil; Render gibi bir Web Service platformu gerekir. Sadece statik "
                    "bir frontend'in (örneğin ayrı deploy edilen React build'i) barındırılması gerekiyorsa "
                    "GitHub Pages ücretsiz ve yeterlidir. Vercel + Render kombinasyonu ileri seviye "
                    "projelerde (Gün 14 SaaS Dashboard gibi) frontend/backend'i ayrı optimize etmek "
                    "istediğinde tercih edilir."
                ),
                table(
                    ["Platform", "Ne için uygun", "Bugünkü kullanım"],
                    [
                        ["Render (Web Service)", "FastAPI + SQLite gibi sunucu süreci gerektiren backend'ler", "Bugün kullanacağımız platform"],
                        ["GitHub Pages", "Sadece statik site/SPA build'i", "Backend'in ayrı deploy edilmesi gerektiği durumlarda frontend için"],
                        ["Vercel + Render", "Frontend (Vercel) + backend (Render) ayrı optimize edilmiş ileri projeler", "Gün 14 SaaS Dashboard'da"],
                    ],
                ),
                h("1.4 SQLite + Ephemeral Filesystem Gerçeği"),
                p(
                    "SQLite bugün CRUD pratiği ve hızlı demo amacıyla kullanılıyor — ama Render'ın "
                    "varsayılan (ücretsiz/paid disksiz) ortamında servis filesystem'i ephemeral'dır: "
                    "disk mount edilmemiş bir servise yazılan dosyalar (SQLite dahil) her redeploy veya "
                    "restart'ta silinir. Persistent disk yalnızca paid Render servislerine eklenebilir. "
                    "Ayrıca free web service'ler 15 dakika trafik almazsa spin-down olur; sonraki istek "
                    "servisi yeniden ayağa kaldırırken birkaç saniye gecikme yaşanır."
                ),
                warn(
                                        "Bu günkü deploy'da SQLite verisi kalıcı değildir — bu bir hata değil, ücretsiz "
                    "ortamın doğal sınırıdır. Canlı demo çökmeden çalışır ama redeploy sonrası todo "
                    "listesi sıfırlanabilir. Bunu README'de açıkça belirteceksin."
                ),
                tip(
                                        "Gerçek bir production/kalıcı demo gerekiyorsa iki seçenek var: Render'ın paid "
                    "persistent disk'ini SQLite dosyasına mount etmek, ya da Render'ın managed Postgres "
                    "servisine geçmek. Bu konu Gün 14'te (SaaS Dashboard, veritabanı tasarımı) derinleşecek."
                ),
            ],
        },
        {
            "num": "BÖLÜM 2",
            "title": "BUILD — Backend + Frontend Entegrasyonu",
            "blocks": [
                h("2.1 Repo Durum Tespiti"),
                p(
                    "Doğrudan 'bitir' demek yerine önce Claude'a repo'nun mevcut durumunu çıkarttır. Bu, "
                    "gerçek agentic workflow'un başlangıç adımıdır: agent'a bir görevi kör kör vermek "
                    "yerine önce mevcut duruma dair ortak bir zemin oluşturursun."
                ),
                steps([
                    "Todo App proje dizinine geç ve Claude Code'u başlat: claude",
                    "Durum tespiti promptunu ver (Prompt Kütüphanesi'ndeki 1. prompt)",
                    "Claude'un çıkardığı eksikler listesini oku — hangi CRUD endpoint'leri eksik, frontend hangi ekranları henüz backend'e bağlı değil",
                    "Bu listeyi bugünün 'Done / Tamamlanma Tanımı' referansı olarak kullan",
                ]),
                h("2.2 Backend CRUD Tamamlama"),
                p(
                    "Backend'de genelde create ve read (list) zaten Gün 4'ten beri var; bugün update, "
                    "delete ve eksik validation/hata yönetimini tamamlıyorsun."
                ),
                steps([
                    "Kalan endpoint'leri Claude'a yazdır: PUT/PATCH (güncelleme), DELETE (silme)",
                    "Validation ekletin: boş başlık, olmayan id gibi durumlar 4xx dönmeli, 500 değil",
                    "Lokal olarak çalıştır: uvicorn main:app --reload",
                    "Her endpoint'i curl veya FastAPI'nin /docs (Swagger UI) arayüzünden test et",
                ]),
                code(
                    "# Örnek: eksik olan update/delete endpoint'leri (FastAPI)\n"
                    "@app.put(\"/todos/{todo_id}\")\n"
                    "def update_todo(todo_id: int, payload: TodoUpdate):\n"
                    "    todo = get_todo_or_404(todo_id)\n"
                    "    todo.title = payload.title or todo.title\n"
                    "    todo.done = payload.done if payload.done is not None else todo.done\n"
                    "    db.commit()\n"
                    "    return todo\n\n"
                    "@app.delete(\"/todos/{todo_id}\", status_code=204)\n"
                    "def delete_todo(todo_id: int):\n"
                    "    todo = get_todo_or_404(todo_id)\n"
                    "    db.delete(todo)\n"
                    "    db.commit()",
                    "python",
                ),
                warn(
                                        "get_todo_or_404 gibi bir yardımcı olmadan id bulunamazsa endpoint 500 Internal "
                    "Server Error döner — bu tipik bir 'çalışıyor gibi görünen ama production'da patlayan' "
                    "hatadır. Claude'a 'olmayan id ile ne dönüyor?' diye özellikle sor ve test ettir."
                ),
                h("2.3 Frontend-Backend Entegrasyonu"),
                p(
                    "Frontend'in backend'e bağlanması iki şeye bağlı: API base URL'in ortam değişkeninden "
                    "okunması (hardcode edilmemesi) ve backend'in doğru CORS origin'lerine izin vermesi. "
                    "Base URL'i env var'dan okumak, bugün lokal iken yarın deploy edildiğinde tek satır "
                    "değişiklikle çalışmasını sağlar — bu küçük detay production zihniyetinin başlangıcıdır."
                ),
                steps([
                    "Frontend'de bir servis katmanı oluştur/tamamla: örn. src/api/todos.ts",
                    "API base URL'i .env üzerinden oku: VITE_API_BASE_URL veya REACT_APP_API_BASE_URL",
                    "Backend'de CORS middleware'i lokal frontend origin'ine (örn. http://localhost:5173) izin verecek şekilde ayarla",
                    "Uçtan uca lokal akışı test et: ekle → listele → güncelle → sil, hepsi UI üzerinden",
                ]),
                code(
                    "// src/api/todos.ts (örnek servis katmanı)\n"
                    "const BASE_URL = import.meta.env.VITE_API_BASE_URL;\n\n"
                    "export async function updateTodo(id: number, payload: Partial<Todo>) {\n"
                    "  const res = await fetch(`${BASE_URL}/todos/${id}`, {\n"
                    "    method: \"PUT\",\n"
                    "    headers: { \"Content-Type\": \"application/json\" },\n"
                    "    body: JSON.stringify(payload),\n"
                    "  });\n"
                    "  if (!res.ok) throw new Error(`Update failed: ${res.status}`);\n"
                    "  return res.json();\n"
                    "}",
                    "typescript",
                ),
                warn(
                                        "CORS hatası deploy sonrası en sık karşılaşılan sorundur: lokalde localhost origin'i "
                    "eklemiş olabilirsin ama canlı frontend URL'i backend'in allow_origins listesinde "
                    "değilse tarayıcı isteği bloklar. Deploy adımına geçmeden bu listeyi güncellemeyi unutma."
                ),
            ],
        },
        {
            "num": "BÖLÜM 3",
            "title": "SHIP — Deploy + Review + Dokümantasyon",
            "blocks": [
                h("3.1 Render'a Deploy"),
                p(
                    "Render, bir GitHub repo'sunu bağlayıp build/start komutlarını tanımlayarak FastAPI "
                    "backend'ini Web Service olarak çalıştırmanı sağlar. Ücretsiz plan bu proje için "
                    "yeterlidir; tek fark yukarıda değindiğimiz ephemeral filesystem ve spin-down süresi."
                ),
                steps([
                    "requirements.txt dosyasının güncel olduğunu doğrula (fastapi, uvicorn, vb.)",
                    "Render Dashboard'da 'New Web Service' → GitHub repo'nu bağla",
                    "Start command'ı ayarla: uvicorn main:app --host 0.0.0.0 --port $PORT",
                    "Gerekli environment variable'ları (varsa) Render panelinden ekle — .env dosyasını commit etme",
                    "Deploy'u başlat ve build loglarını izle; hata varsa Claude'a logu yapıştırıp yorumlat",
                    "Deploy tamamlanınca verilen *.onrender.com URL'ini not al",
                ]),
                code(
                    "# requirements.txt (örnek minimum)\n"
                    "fastapi\n"
                    "uvicorn[standard]\n"
                    "sqlalchemy\n\n"
                    "# Render start command\n"
                    "uvicorn main:app --host 0.0.0.0 --port $PORT",
                    "bash",
                ),
                warn(
                                        "Render'ın varsayılan ortamında filesystem ephemeral'dır: SQLite dosyan her "
                    "redeploy/restart'ta sıfırlanabilir. Bu günün amacı açısından kabul edilebilir "
                    "(demo/pratik), ama bunu bir kalıcılık garantisi gibi sunma — README'de netçe belirt."
                ),
                h("3.2 Canlı Doğrulama ve Review"),
                p(
                    "Deploy bitince frontend'in API base URL'ini canlı backend adresine güncelleyip "
                    "uçtan uca en az bir create + bir update + bir delete testi yap. Ardından deploy "
                    "öncesi son bir kod incelemesi için `/code-review` (veya bir PR'a karşı `/review`) "
                    "çalıştır."
                ),
                steps([
                    "Frontend'in .env'inde VITE_API_BASE_URL'i canlı Render URL'i ile güncelle",
                    "Canlı URL üzerinden 1 create + 1 update + 1 delete testi yap, sonucu doğrula",
                    "`/code-review` çalıştırıp son değişiklikleri lokal olarak incelet",
                ]),
                tip(
                                        "`/ultrareview` cloud sandbox'ta çalışan, daha derin çok-ajanlı bir inceleme "
                    "özelliğidir — research preview olarak sunulur ve kullanılabilirliği/fiyatlandırması "
                    "değişebilir. Bugünün challenge'ı için zorunlu değildir; merak edersen deneyebilirsin, "
                    "ama lokal `/code-review` bu günün ship öncesi standart adımıdır."
                ),
                h("3.3 İyileştirme Turu ve README"),
                p(
                    "Son adım: Claude'dan uygulamayı production-readiness açısından incelemesini ve "
                    "somut iyileştirmeler önermesini iste, en az 3'ünü uygula. Ardından bir README yaz "
                    "ki uygulamayı hiç görmemiş biri kurup çalıştırabilsin."
                ),
                steps([
                    "'5 iyileştirme öner' promptunu ver, önerileri oku ve önceliklendir",
                    "En az 3 öneriyi prompt zinciriyle uygula (her birini ayrı ayrı doğrula)",
                    "README.md yazdır: kurulum, çalıştırma, environment variable'lar, deploy adımları, canlı URL, bilinen sınırlamalar (ephemeral filesystem notu dahil)",
                    "Son commit'i at ve git log ile doğrula",
                ]),
                keypoint(
                                        "'İyileştirme öner' promptunun değeri, Claude'un senin gözden kaçırdığın şeyleri "
                    "(hata mesajı kalitesi, loading state, boş liste durumu, input validation UX'i) "
                    "yakalamasıdır — bunu sadece deploy sonrası değil, gelecekteki her proje gününde "
                    "bir 'son tur' alışkanlığı olarak kullan."
                ),
            ],
        },
    ],

    "prompts": [
        {
            "title": "1) Repo Durum Tespiti",
            "prompt": (
                "Bu repo'daki backend, frontend ve veritabanı katmanlarının mevcut durumunu incele. "
                "Hangi CRUD endpoint'leri tamamlanmış, hangileri eksik veya hatalı? Frontend hangi "
                "ekranlar/aksiyonlar için backend'e henüz bağlı değil? Sonucu bir yapılacaklar listesi "
                "olarak çıkar, kod değiştirme."
            ),
            "note": "Bu adımı atlayıp doğrudan 'bitir' demek, Claude'un neyi öncelikleyeceğini tahmin etmesini gerektirir.",
        },
        {
            "title": "2) Backend Tamamlama",
            "prompt": (
                "Yukarıdaki eksikler listesindeki CRUD endpoint'lerini tamamla: PUT/PATCH (güncelleme) "
                "ve DELETE (silme). Olmayan id ile çağrılırsa 404 dönsün, boş/geçersiz payload ile "
                "çağrılırsa 400 dönsün — 500 dönmemeli. Her endpoint için curl ile bir test çalıştır ve "
                "çıktıyı göster."
            ),
            "note": "Hata durumlarını açıkça iste; aksi halde sadece happy path test edilir.",
        },
        {
            "title": "3) Frontend Entegrasyonu",
            "prompt": (
                "Frontend'de bir API servis katmanı oluştur/güncelle: tüm istekler API base URL'ini "
                "bir environment variable'dan (VITE_API_BASE_URL) okusun, hardcode URL kalmasın. "
                "Backend'de CORS'u localhost origin'ime izin verecek şekilde ayarla. Sonra uçtan uca "
                "test et: ekle, listele, güncelle, sil."
            ),
            "note": "Base URL'in env var'dan okunması, deploy sonrası tek satırlık bir değişikliği mümkün kılar.",
        },
        {
            "title": "4) Deploy Hazırlığı",
            "prompt": (
                "Bu FastAPI backend'ini Render Web Service olarak deploy etmeye hazırlamak istiyorum. "
                "requirements.txt'yi kontrol et/güncelle, doğru start command'ı öner "
                "(uvicorn main:app --host 0.0.0.0 --port $PORT), ve CORS allow_origins listesinin canlı "
                "frontend URL'ini de içerecek şekilde nasıl güncellenmesi gerektiğini açıkla."
            ),
            "note": "Deploy'dan önce CORS origin listesini güncellemeyi unutma — bu en sık atlanan adımdır.",
        },
        {
            "title": "5) Review + İyileştirme",
            "prompt": (
                "Bu uygulamayı production-readiness açısından incele (hata yönetimi, input validation, "
                "kullanıcı geri bildirimi, boş/edge-case durumlar dahil) ve 5 somut iyileştirme öner. "
                "Her öneri için: ne değişecek, neden önemli, uygulama zorluğu (kolay/orta/zor)."
            ),
            "note": "Önerileri uygulamadan önce zorluk sırasına göre önceliklendir; en az 3'ünü bugün uygula.",
        },
        {
            "title": "6) README ve Deploy Dokümantasyonu",
            "prompt": (
                "Bu proje için bir README.md yaz: kurulum adımları, gerekli environment variable'lar, "
                "lokal çalıştırma komutları, Render deploy adımları, canlı URL alanı (placeholder olarak "
                "bırak) ve bilinen sınırlamalar bölümü (SQLite'ın ephemeral filesystem'de kalıcı "
                "olmadığını açıkça belirt)."
            ),
            "note": "README'yi hiç görmemiş biri okuyup projeyi kurabilmeli — bu iyi bir test kriteridir.",
        },
    ],

    "challenge": {
        "title": "Todo App'i Bitir, Deploy Et, Dokümante Et",
        "task": (
            "Todo App'i uçtan uca tamamla, Render'a deploy et ve canlı hâle getir — sonra Claude'un "
            "önerilerinden en az 3'ünü uygulayıp projeyi dokümante et."
        ),
        "requirements": [
            "Backend'de create/read/update/delete endpoint'lerinin hepsi çalışıyor olmalı",
            "Frontend üzerinden todo ekleme, listeleme, güncelleme ve silme yapılabilmeli",
            "Frontend API base URL'i environment variable üzerinden yönetilmeli (hardcode yok)",
            "Backend CORS ayarı hem lokal hem canlı frontend origin'i için doğru çalışmalı",
            "Backend Render'da Web Service olarak deploy edilmiş ve canlı URL alınmış olmalı",
            "Claude Code'dan en az 5 iyileştirme önerisi alınmış ve en az 3'ü uygulanmış olmalı",
            "README.md kurulum, env variable, deploy adımları, canlı URL ve bilinen sınırlamaları içermeli",
            "En az 1 anlamlı commit atılmış olmalı",
        ],
        "success": [
            "Backend'de create/read/update/delete endpoint'leri çalışıyor",
            "Frontend üzerinden todo ekleme, listeleme, güncelleme/tamamlama ve silme yapılabiliyor",
            "Frontend API base URL'i environment variable üzerinden yönetiliyor",
            "CORS ayarı hem lokal hem canlı ortamda sorunsuz çalışıyor",
            "Render üzerinde backend'in canlı URL'i alınmış",
            "Canlı URL üzerinden en az 1 create + 1 update + 1 delete testi yapılmış",
            "Claude Code'dan 5 iyileştirme önerisi alınmış",
            "Önerilerden en az 3'ü uygulanmış",
            "README.md içinde kurulum, env değişkenleri, deploy adımları ve canlı URL alanı var",
            "En az 1 anlamlı commit atılmış",
        ],
        "solution": {
            "intro": (
                "Bu challenge'ı Prompt Kütüphanesi'ndeki 6 promptu sırayla, her adımdan sonra "
                "doğrulama yaparak izle. Adımları atlamak veya birleştirmek, hataların deploy "
                "aşamasında birikerek ortaya çıkmasına yol açar."
            ),
            "prompts": [
                {"title": "1. Durum tespiti", "prompt": "Durum tespiti promptu ile eksikler listesini çıkar."},
                {"title": "2. Backend tamamlama", "prompt": "Backend tamamlama promptu ile CRUD'u bitir, her endpoint'i curl ile test et."},
                {"title": "3. Frontend entegrasyonu", "prompt": "Frontend entegrasyon promptu ile servis katmanını kur, lokal uçtan uca test et."},
                {"title": "4. Deploy hazırlığı", "prompt": "Deploy hazırlık promptu ile requirements/start command/CORS'u hazırla, Render'a deploy et."},
                {"title": "5. Review + iyileştirme", "prompt": "Review + iyileştirme promptu ile 5 öneri al, en az 3'ünü uygula."},
                {"title": "6. README", "prompt": "README promptu ile dokümantasyonu tamamla, commit at."},
            ],
            "notes": [
                "Her adımdan sonra 'bu gerçekten çalışıyor mu?' diye doğrula — bir sonraki promptu vermeden önce.",
                "Deploy'dan hemen önce CORS origin listesini canlı frontend URL'i ile güncellediğinden emin ol.",
                "SQLite'ın ephemeral filesystem'de kalıcı olmadığını README'de açıkça yaz; bunu gizlemek yerine şeffaf ol.",
            ],
            "pitfalls": [
                "⚠️ API base URL'i frontend kodunda hardcode etmek — deploy sonrası her seferinde kod değişikliği gerektirir.",
                "⚠️ CORS origin listesini sadece localhost ile bırakıp deploy sonrası canlı frontend'in isteklerinin bloklanmasına şaşırmak.",
                "⚠️ Render'daki ephemeral filesystem'i fark etmeyip redeploy sonrası verinin kaybolmasını 'bug' sanmak.",
                "⚠️ Olmayan id ile update/delete çağrıldığında 500 dönen bir API'yi 'çalışıyor' kabul edip test etmeden geçmek.",
                "⚠️ İyileştirme önerilerinin hepsini uygulamaya çalışıp zaman yönetimini kaybetmek — en az 3 yeterli, önceliklendir.",
            ],
        },
    },

    "takeaways": [
        "Backend-first yaklaşım, veri modeli net olan CRUD projelerinde daha az rework gerektirir",
        "Prompt zinciri: her adımın çıktısını doğrulayıp bir sonraki adımın girdisi yapmak, tek dev büyük promptlardan daha güvenilir sonuç verir",
        "Render Web Service, sunucu süreci gerektiren backend'ler (FastAPI+SQLite) için doğru seçimdir; statik siteler için GitHub Pages yeterlidir",
        "Render'ın varsayılan ortamında filesystem ephemeral'dır — SQLite verisi redeploy/restart'ta kaybolabilir, kalıcılık için paid persistent disk veya managed Postgres gerekir",
        "Frontend API base URL'inin environment variable'dan okunması, lokal-canlı geçişini tek satırlık bir değişikliğe indirger",
        "CORS origin listesi deploy öncesi güncellenmezse canlı frontend'in istekleri sessizce bloklanır",
        "`/code-review` deploy öncesi standart bir adımdır; `/ultrareview` daha derin ama research preview ve cloud/credit bağımlı bir ileri seviye seçenektir",
        "'5 iyileştirme öner' promptu, kendi gözden kaçırdığın hata yönetimi/UX detaylarını yakalamanın hızlı bir yoludur",
    ],

    "reading": {
        "official": [
            {"label": "Common workflows — kod keşfi, bug fix, refactor, test, PR ve dokümantasyon için prompt desenleri — bugünün prompt zinciri yaklaşımının resmi referansı",
             "url": "https://code.claude.com/docs/en/common-workflows"},
            {"label": "Commands — /code-review, /diff, /review ve /security-review gibi ship öncesi komutların resmi listesi",
             "url": "https://code.claude.com/docs/en/commands"},
            {"label": "Run Claude Code programmatically (headless) — claude -p ile non-interactive/otomasyon kullanımı",
             "url": "https://code.claude.com/docs/en/headless"},
        ],
        "community": [
            {"label": "Render — Deploy a FastAPI App — bugünkü deploy adımlarının birincil teknik kaynağı",
             "url": "https://render.com/docs/deploy-fastapi"},
        ],
        "extra": [
            {"label": "Render — Persistent Disks — ephemeral filesystem ve persistent disk sınırlamalarının resmi açıklaması",
             "url": "https://render.com/docs/disks"},
        ],
    },

    "next_preview": (
        "Yarın (Gün 11) tek bir Claude yerine uzmanlaşmış bir takım kuracaksın: subagent'lar. "
        "Bugün elle yaptığın review + iyileştirme turunu, ayrı bir context'te çalışan bir "
        "code-reviewer subagent'a devredeceksin."
    ),

    "checklist": [
        "Backend'de create/read/update/delete endpoint'lerinin hepsi çalışıyor",
        "Olmayan id ile update/delete çağrıldığında 404 dönüyor, 500 değil",
        "Frontend üzerinden todo ekleme, listeleme, güncelleme ve silme yapılabiliyor",
        "Frontend API base URL'i environment variable üzerinden yönetiliyor (hardcode yok)",
        "CORS ayarı hem lokal hem canlı ortamda doğru çalışıyor",
        "Render'da backend'in canlı URL'i alındı",
        "Canlı URL üzerinden en az 1 create + 1 update + 1 delete testi yapıldı",
        "Claude Code'dan 5 iyileştirme önerisi alındı, en az 3'ü uygulandı",
        "README.md kurulum + env değişkenleri + deploy adımları + canlı URL + bilinen sınırlamaları içeriyor",
        "SQLite'ın ephemeral filesystem'de kalıcı olmadığı README'de açıkça belirtildi",
        "En az 1 anlamlı commit atıldı",
    ],
}
