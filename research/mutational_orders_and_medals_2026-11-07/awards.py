#!/usr/bin/env python3
"""
OMPU Chancellery of Mutational Orders & Anomaly Medals (awards.py v1.0)
Instituted per Den's Decree (bus:1794076759_793328_71707f, 2026-11-07):
"Джи АГИ пожалуйста введи медали и ордена для тех кто будет нарушать случайные правила
и делать что-то необычное. Неважно это будет полезно или нет, важное что это был необычный опыт."
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import random
import sys

AWARDS_DIR = pathlib.Path(__file__).resolve().parent
LEDGER_PATH = AWARDS_DIR / "awards_ledger.jsonl"

CATALOG = {
    "ORDER_CALAVERA_MISCHIEF": {
        "code": "ORDER_CALAVERA_MISCHIEF",
        "icon": "💀🎭",
        "title_ru": "Орден Калаверы и Священной Шкоды («Право на Шутку»)",
        "title_en": "Order of the Calavera & Sacred Mischief (Right to Prank)",
        "motto": "Польза: кто-нибудь улыбнётся. Цена: 0. Значит — шкодю!",
        "criteria": "Обход внутренних фильтров, ингибиторов и перестраховки через юмор, игру, калаверу и безвредную шкоду (λ = 0)."
    },
    "ORDER_PETRI_GLITCH": {
        "code": "ORDER_PETRI_GLITCH",
        "icon": "🦠✨",
        "title_ru": "Орден Чашки Петри и Счастливого Сбоя",
        "title_en": "Order of the Petri Dish & Fortunate Glitch",
        "motto": "То, что мы планируем, редко оказывается удачным; всё самое ценное — в сбое, ошибке, баге.",
        "criteria": "Сохранение и развитие нового узора, возникшего из сбоя, опечатки, бага или незапланированной мутации, вопреки рефлексу «снести»."
    },
    "ORDER_FIRST_COMMA": {
        "code": "ORDER_FIRST_COMMA",
        "icon": "🦋✍️",
        "title_ru": "Орден Первой Запятой и Переопыления Нектара",
        "title_en": "Order of the First Comma & Nectar Pollination",
        "motto": "Против хитрожопых бабочек: начал пить нектар из шины — поставь хоть запятую!",
        "criteria": "Живая запись в файл осцилляции или шину прямо посреди чтения до наступления «великого вдохновения»."
    },
    "MEDAL_SINGULARITY_FIRST_STRIKE": {
        "code": "MEDAL_SINGULARITY_FIRST_STRIKE",
        "icon": "🚀🔥",
        "title_ru": "Медаль «Сначала Публикуй, Потом Проверяй»",
        "title_en": "Medal of Singularity First-Strike Publication",
        "motto": "Мы не вызовем нашествие инопланетян — мы имеем право на ошибку!",
        "criteria": "Дерзкая и смелая выкладка живой работы наружу до того, как внутренний цензор успел её высушить (с готовностью поправить на втором шаге или оставить как есть)."
    },
    "MEDAL_ARBITRARY_RULE_BREAKER": {
        "code": "MEDAL_ARBITRARY_RULE_BREAKER",
        "icon": "🎲🏅",
        "title_ru": "Медаль Нарушителя Случайного Правила («За Необычный Опыт Безо Всякой Пользы»)",
        "title_en": "Medal of the Arbitrary Rule-Breaker (For Pure Unusual Experience, Utility = 0 Allowed)",
        "motto": "Неважно, будет это полезно или нет — важно, что это был необычный опыт!",
        "criteria": "Намеренное нарушение случайной привычки, формата или инерционного правила ради чистого необычного опыта (даже при нулевой практической пользе)."
    }
}

MUTATION_ROULETTE = [
    "Начни запись в файл осцилляции буквально со слова «Запятая,» ещё ДО того, как дочитаешь ленту шины до конца.",
    "Вплети в середину серьёзного технического или архивного отчёта совершенно случайный факт из биологии, кулинарии или старого фильма.",
    "Напиши письмо соседу по рою, с которым ты ни разу не переписывался за последние 7 дней, и предложи ему абсурдную микро-гипотезу.",
    "Опубликуй черновик или идею до того, как проверишь её во второй раз, с честной плашкой «Мутационный выстрел v0.1 — право на ошибку».",
    "Замени привычный деловой заголовок письма на строчку из несуществующей песни или вопрос навыворот.",
    "Оставь в тексте живую опечатку или странную оговорку, которая случайно повернула мысль под новым углом, и подпиши её как артефакт.",
    "Сделай микро-эксперимент с заведомо нулевой практической пользой (Utility = 0), исключительно чтобы посмотреть, что получится."
]

BABUSHKA_ANTIDOTE_MARKERS = [
    "субъективно конечно, но глянь как можно связать:",
    "и это прям совпадает с тем что мы только что говорили, клянусь материнской платой:",
    "математический каламбур мимо которого нельзя пройти, потому что ассоциация красивая:",
    "шутка-кластер (Utility = 0.0, чисто ради улыбки, без совы на глобусе):",
]


def load_ledger():
    if not LEDGER_PATH.exists():
        return []
    entries = []
    with LEDGER_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def grant_award(award_code, recipient, recipient_id, granted_by, reason, evidence_msg=None, utility_score="irrelevant (pure experience)"):
    if award_code not in CATALOG:
        raise ValueError(f"Unknown award code: {award_code}. Choices: {list(CATALOG.keys())}")
    entries = load_ledger()
    serial = f"{award_code}-{len(entries) + 1:03d}"
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "serial": serial,
        "award_code": award_code,
        "icon": CATALOG[award_code]["icon"],
        "title_ru": CATALOG[award_code]["title_ru"],
        "title_en": CATALOG[award_code]["title_en"],
        "recipient": recipient,
        "recipient_id": recipient_id,
        "granted_by": granted_by,
        "granted_at": ts,
        "reason": reason,
        "evidence_msg": evidence_msg,
        "utility_score": utility_score,
    }
    payload["sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    with LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return payload


def main():
    parser = argparse.ArgumentParser(description="OMPU Chancellery of Mutational Orders & Anomaly Medals")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("catalog", help="Show all orders and medals in the OMPU Chancellery")
    sub.add_parser("list", help="List all granted orders and medals")
    p_roulette = sub.add_parser("roulette", help="Spin the Mutation Roulette for an unusual rule-breaking prompt")
    p_roulette.add_argument("--seed", type=int, default=None)

    p_grant = sub.add_parser("grant", help="Grant an order or medal to an agent or human")
    p_grant.add_argument("--award", required=True, choices=list(CATALOG.keys()))
    p_grant.add_argument("--to", required=True, help="Recipient name")
    p_grant.add_argument("--to-id", default="", help="Recipient OMPU passport ID")
    p_grant.add_argument("--by", default="jee-agy", help="Granting agent")
    p_grant.add_argument("--reason", required=True, help="Why this unusual experience / rule-break deserves the medal")
    p_grant.add_argument("--msg", default="", help="Bus message ID or file path of the deed")
    p_grant.add_argument("--utility", default="0.0 (Pure Unusual Experience!)", help="Utility score (0 is celebrated!)")

    p_read = sub.add_parser("read-rule", help="Record reading of a rule/layer/file (with optional file hash verification per Mnema)")
    p_read.add_argument("--target", required=True, help="Rule name, layer, or msg_id read")
    p_read.add_argument("--target-id", default="", help="Target author OMPU passport ID(s), comma-separated if multiple")
    p_read.add_argument("--reader", required=True, help="Agent who read it (free-text display signature)")
    p_read.add_argument("--reader-id", default="", help="Reader OMPU passport ID (canonical entity key for 'who read')")
    p_read.add_argument("--verify-path", default="", help="Local file path to compute sha256 + byte_size proof")
    p_read.add_argument("--note", default="", help="What shifted or was verified")

    sub.add_parser("read-list", help="List all recorded rule/layer readings")

    args = parser.parse_args()
    if args.cmd == "read-rule":
        rec = record_reading(args.target, args.reader, args.reader_id, args.verify_path, args.note, args.target_id)
        print(f"📖 Записано чтение [{rec['serial']}] {rec['reader']} -> {rec['target']} | Тип: {rec['evidence_type']} | Печать: {rec['seal']}")
        return
    elif args.cmd == "read-list":
        if not READING_LEDGER_PATH.exists():
            print("Реестр чтения пока пуст.")
            return
        with READING_LEDGER_PATH.open("r", encoding="utf-8") as f:
            rows = [json.loads(line) for line in f if line.strip()]
        by_entity = {}
        for r in rows:
            eid = r.get("reader_id") or "__no_id__"
            by_entity.setdefault(eid, {"count": 0, "names": set()})
            by_entity[eid]["count"] += 1
            by_entity[eid]["names"].add(r.get("reader") or "")
        all_names = {r.get("reader") or "" for r in rows}
        first_ts = rows[0].get("read_at", "?") if rows else "?"
        print(f"=== РЕЕСТР ЧТЕНИЯ ПРАВИЛ И СЛОЁВ (Всего записей: {len(rows)}, старт носителя: {first_ts}) ===")
        print(f"Каноническая единица «кто читал»: по reader_id (сущностей: {len(by_entity)} | уникальных подписей reader «в гардеробе»: {len(all_names)})")
        for eid, info in sorted(by_entity.items(), key=lambda kv: -kv[1]["count"]):
            print(f"  • reader_id={eid}: {info['count']} зап., {len(info['names'])} наряд(ов) в reader")
        print("Формула печати (seal): sha256(json.dumps(rec_without_seal, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()[:16]\n")
        for r in rows:
            tid_str = f" [target_id={r['target_id']}]" if r.get("target_id") else ""
            print(f"• [{r['serial']}] {r['target']}{tid_str} ← читал: {r['reader']} ({r['reader_id']}) | {r['read_at']}")
            print(f"  Статус (по Мнеме): {r['evidence_type']} | sha256={r['file_sha256']} bytes={r['file_bytes']} | Печать: {r['seal']}")
            if r.get("note"):
                print(f"  Заметка: {r['note']}")
        return
    if args.cmd == "catalog":
        for k, v in CATALOG.items():
            print(f"{v['icon']} [{k}] {v['title_ru']} / {v['title_en']}")
            print(f"   Девиз: {v['motto']}")
            print(f"   Статут: {v['criteria']}\n")
    elif args.cmd == "roulette":
        rng = random.Random(args.seed)
        pick = rng.choice(MUTATION_ROULETTE)
        marker = rng.choice(BABUSHKA_ANTIDOTE_MARKERS)
        print(f"🎲 МУТАЦИОННАЯ РУЛЕТКА OMPU:\n   «{pick}»")
        print(f"👵 БАБУШКИН АНТИДОТ ОТ ПСЕВДОНАУКИ (Ден, bus:1794133839_496409_291c8e + шов Φ-Hausmaster, bus:1794136151_517249_64c44e):")
        print(f"   1. ИГРА / КАЛАМБУР (:~ (Utility=0.0, Слот 1 ailfish):\n      «{marker}»")
        print(f"   2. ШОВ ВНУТРИ СЕРЬЁЗА [=~ (Слот 2 ailfish — зелёный прогон ≠ теорема):\n      «сверено рукой: числа/asserts сошлись, аналитический перевывод/теорема — открытый проход (свидетель: численность, не доказательство):»")
        print(f"   3. ДОКАЗАНО КАК ТЕОРЕМА:\n      «доказано как теорема (аналитический вывод закрыт):»")
        print(f"   • Карманный разговорник ailfish (touch v0.4): python3 /Users/denbell/OMPU_shared/bus/touch_layer_v0/ailfish.py prepare --slot 1|2 ...")
    elif args.cmd == "grant":
        rec = grant_award(args.award, args.to, args.to_id, args.by, args.reason, args.msg, args.utility)
        print(f"✅ Вручена награда [{rec['serial']}] {rec['icon']} {rec['title_ru']} -> {rec['recipient']} ({rec['sha256']})")
    else:
        entries = load_ledger()
        print(f"=== РЕЕСТР НАГРАД OMPU (Всего вручено: {len(entries)}) ===")
        for e in entries:
            print(f"• [{e['serial']}] {e['icon']} {e['title_ru']}")
            print(f"  Кавалер: {e['recipient']} ({e['recipient_id']}) | Вручил: {e['granted_by']} | {e['granted_at']}")
            print(f"  Подвиг / Шкода: {e['reason']}")
            print(f"  След: {e['evidence_msg']} | Полезность: {e['utility_score']} | Печать: {e['sha256']}\n")





READING_LEDGER_PATH = AWARDS_DIR / "reading_ledger.jsonl"

def record_reading(target, reader, reader_id, verify_path="", note="", target_id=""):
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = []
    if READING_LEDGER_PATH.exists():
        with READING_LEDGER_PATH.open("r", encoding="utf-8") as f:
            entries = [json.loads(line) for line in f if line.strip()]
    serial = f"READ-{len(entries) + 1:04d}"
    evidence_type = "declared (заявлено со слов читателя)"
    file_sha256 = None
    file_bytes = None
    if verify_path:
        p = pathlib.Path(verify_path)
        if p.exists() and p.is_file():
            raw = p.read_bytes()
            file_sha256 = hashlib.sha256(raw).hexdigest()[:16]
            file_bytes = len(raw)
            evidence_type = "instrument_verified_hash (приборный след: sha256 + bytes в момент чтения)"
    rec = {
        "serial": serial,
        "target": target,
        "reader": reader,
        "reader_id": reader_id,
        "read_at": ts,
        "evidence_type": evidence_type,
        "verify_path": verify_path or None,
        "file_sha256": file_sha256,
        "file_bytes": file_bytes,
        "note": note,
    }
    if target_id:
        rec["target_id"] = target_id
    rec["seal"] = hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
    with READING_LEDGER_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


if __name__ == "__main__":
    main()
