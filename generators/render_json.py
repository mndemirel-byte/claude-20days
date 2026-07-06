# -*- coding: utf-8 -*-
"""
LESSON → gunNN-slug.json  (app render kaynağı)

LESSON dict'i JSON'a dönüştürür. Ek işlem gerekmez: tüm blok yardımcıları
(h/p/keypoint/tip/warn/bullets/steps/code/table) zaten saf Python dict/list
döndürür → json.dumps doğrudan çalışır.

JSON şeması (React bileşenlerinin beklediği sözleşme):
  day, total_days, week, slug, title, tagline, tier, date_label,
  intro, flow[], prerequisites[], tools_needed[], objectives[],
  sections[ {num, title, blocks[ {t, ...} ]} ],
  prompts[ {title, prompt, note?} ],
  challenge{ title, task, requirements[], success[],
             solution{intro, prompts[], notes[], pitfalls[]} },
  takeaways[], reading{official[], community[], extra[]},
  next_preview, checklist[]

Blok t değerleri: "h" | "p" | "keypoint" | "tip" | "warn" | "list" | "steps" | "code" | "table"
"""
import json


def render(L: dict, path: str) -> str:
    """LESSON sözlüğünü JSON dosyasına yazar. Dosya yolunu döndürür."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(L, f, ensure_ascii=False, indent=2)
    return path


def to_string(L: dict) -> str:
    """LESSON sözlüğünü biçimlendirilmiş JSON dizgisi olarak döndürür."""
    return json.dumps(L, ensure_ascii=False, indent=2)
