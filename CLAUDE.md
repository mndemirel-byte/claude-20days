# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Agent skills

### Issue tracker

Issues live as local markdown files under `.scratch/`. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), plus lifecycle labels (`agent-is-working`, `done`) set by implementing agents. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context repo — `CONTEXT.md` at root + `docs/adr/`. See `docs/agents/domain.md`.

---

## Available skills

Skills are invoked by typing `/skill-name` in Claude Code.

### Engineering

| Skill | Ne yapar |
|-------|---------|
| `/diagnose` | Bug teşhis döngüsü — reproduce → minimise → hypothesise → instrument → fix |
| `/tdd` | Test-driven development, red-green-refactor döngüsü |
| `/coverage-check` | Issue/PRD acceptance criteria'larını mevcut test suite'iyle karşılaştırır, eksik testleri bulur |
| `/improve-codebase-architecture` | Mimari iyileştirme fırsatlarını bulur, CONTEXT.md ve ADR'lere dayanır |
| `/design-an-interface` | Bir modül için paralel sub-agent'larla birden fazla farklı interface tasarımı üretir |
| `/prototype` | Tasarımı sabitleme öncesi throwaway prototip oluşturur |
| `/zoom-out` | Kodun büyük resmine ve bağlamına bakar |
| `/to-prd` | Mevcut konuşmayı PRD'ye çevirir ve issue tracker'a yazar |
| `/to-issues` | Plan veya PRD'yi bağımsız issue'lara böler |
| `/triage` | Issue'ları state machine ile triage eder |
| `/review` | Branch veya PR'ı standartlar ve spec ekseninde paralel review yapar |
| `/grill-with-docs` | Planı mevcut domain modeline ve ADR'lere karşı sorgular, CONTEXT.md'yi günceller |
| `/setup-matt-pocock-skills` | Bu skill'lerin ihtiyaç duyduğu repo konfigürasyonunu kurar |
| `/setup-pre-commit` | Husky pre-commit hook'larını kurar (Prettier, tip kontrolü, testler) |
| `/git-guardrails-claude-code` | Tehlikeli git komutlarını engelleyen hook'ları kurar |

### Productivity

| Skill | Ne yapar |
|-------|---------|
| `/grill-me` | Planı veya tasarımı amansızca sorgular, karar ağacını çözer |
| `/handoff` | Konuşmayı başka bir agent'ın devralması için handoff dokümanına sıkıştırır |
| `/teach` | Bu workspace'te yeni bir kavram veya skill öğretir |
| `/caveman` | ~%75 token tasarrufu için ultra-sıkıştırılmış iletişim modu |
| `/write-a-skill` | Yeni agent skill'i oluşturur |

### Writing

| Skill | Ne yapar |
|-------|---------|
| `/writing-fragments` | Ham materyal için fikir madenciliği — yapı dayatmadan önce parçalar toplar |
| `/writing-beats` | Makaleyi beat beat şekillendirir, choose-your-own-adventure tarzı |
| `/writing-shape` | Ham notu yayımlanabilir makaleye dönüştürür |
| `/edit-article` | Makale taslağını yeniden yapılandırır, netleştirir, sıkıştırır |
| `/ubiquitous-language` | Konuşmadan DDD tarzı ubiquitous language glossary çıkarır |

### Misc

| Skill | Ne yapar |
|-------|---------|
| `/scaffold-exercises` | Kurs egzersizi dizin yapısı oluşturur |
| `/migrate-to-shoehorn` | Test dosyalarındaki `as` type assertion'larını shoehorn'a taşır |
| `/obsidian-vault` | Obsidian vault'ta not arar, oluşturur, düzenler |

---

## Project Overview

<!-- TODO: Bu projeye özel proje tanımı, tech stack, mimari ve komutları buraya ekle. -->
