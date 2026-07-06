"""20 günün manifestosu: sidebar, index ve gün-arası navigasyon için tek liste."""

# tier: gün başlığının yanında gösterilecek proje kademesi rozeti (ya da None)
DAYS = [
    {"day": 1,  "week": 1, "slug": "claude-code-nedir-kurulum",
     "title": "Claude Code Nedir ve Kurulum", "tier": None},
    {"day": 2,  "week": 1, "slug": "temel-kullanim-izinler-auto-mode",
     "title": "Temel Kullanım, İzinler ve Auto Mode", "tier": "🟢 Kademe 1"},
    {"day": 3,  "week": 1, "slug": "claude-md-auto-memory",
     "title": "CLAUDE.md ve Auto Memory", "tier": None},
    {"day": 4,  "week": 1, "slug": "proje-klasor-yapisi",
     "title": "Proje Klasör Yapısı ve Başlangıç Şablonu", "tier": "🟡 Kademe 2"},
    {"day": 5,  "week": 1, "slug": "git-checkpointing-workflow",
     "title": "Git Entegrasyonu, Checkpointing ve Workflow", "tier": None},
    {"day": 6,  "week": 2, "slug": "slash-commands-skills",
     "title": "Slash Commands & Bundled Skills", "tier": None},
    {"day": 7,  "week": 2, "slug": "context-window-auto-mode",
     "title": "Context Window Yönetimi ve Verimli Çalışma", "tier": None},
    {"day": 8,  "week": 2, "slug": "debugging-test-kod-inceleme",
     "title": "Debugging, Test Yazma ve Kod İncelemesi", "tier": None},
    {"day": 9,  "week": 2, "slug": "mcp-temelleri",
     "title": "MCP (Model Context Protocol) Temelleri", "tier": None},
    {"day": 10, "week": 2, "slug": "todo-app-fullstack-deploy",
     "title": "Todo App Full-stack + Deploy", "tier": "🟡 Kademe 2"},
    {"day": 11, "week": 3, "slug": "subagentlar",
     "title": "Subagent'lar: Uzmanlaşmış AI Takım Arkadaşları", "tier": None},
    {"day": 12, "week": 3, "slug": "hooks-sandboxing",
     "title": "Hooks ve Sandboxing", "tier": None},
    {"day": 13, "week": 3, "slug": "skills-plugins",
     "title": "Skills & Plugins", "tier": None},
    {"day": 14, "week": 3, "slug": "saas-dashboard",
     "title": "İleri Seviye Proje: SaaS Dashboard", "tier": "🟠 Kademe 3"},
    {"day": 15, "week": 3, "slug": "rol-agent-tasarimi",
     "title": "Yazılım Rolleri İçin Agent Tasarımı", "tier": None},
    {"day": 16, "week": 4, "slug": "paralel-agent-view-worktrees",
     "title": "Paralel Çalışma, Agent View ve Worktrees", "tier": None},
    {"day": 17, "week": 4, "slug": "agent-teams-dynamic-workflows",
     "title": "Agent Teams & Dynamic Workflows", "tier": None},
    {"day": 18, "week": 4, "slug": "cicd-routines-otomasyon",
     "title": "CI/CD, Routines ve Otomasyon", "tier": None},
    {"day": 19, "week": 4, "slug": "enterprise-patterns",
     "title": "Enterprise Patterns ve Best Practices", "tier": None},
    {"day": 20, "week": 4, "slug": "capstone-mikroservis",
     "title": "Capstone: Enterprise Mikro-Servis Projesi", "tier": "🔴 Kademe 4"},
]

WEEK_TITLES = {
    1: "HAFTA 1 — Temel",
    2: "HAFTA 2 — Orta",
    3: "HAFTA 3 — İleri",
    4: "HAFTA 4 — Master",
}


def filename(day):
    d = DAYS[day - 1]
    return f"gun{day:02d}-{d['slug']}"
