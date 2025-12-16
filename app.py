from browser import document, window, html, local_storage, timer
import random

# -----------------------------
# 1) Harmonogram vydania výziev
# -----------------------------
RELEASES = [
    "2025-12-20",
    "2025-12-22",
    "2025-12-27",
    "2025-12-29",
    "2025-12-30",
    "2026-01-02",
    "2026-01-05",
    "2026-01-08",
]
SERIES_FULL_FROM = "2026-01-09"  # od tohto dátumu ukáž celý archív (kompletnú sériu)

# -----------------------------
# 2) Dáta výziev (Krtko)
# -----------------------------
QUESTS = [
    {
        "title": "Výzva 1: Krtko len v párnych riadkoch",
        "desc": "Priprav logiku, aby sa krtko zobrazoval iba v párnych riadkoch mriežky (0 a 2).",
        "tasks": [
            "Z indexu políčka vypočítaj riadok: row = idx // 4",
            "Povoľ len row % 2 == 0",
        ],
        "warmup": [
            {"q": "Ak idx = 9 v 4×4 mriežke, aký je row = idx//4 ?", "a": ["2"]},
            {"q": "Ak row = 3, platí row%2==0? (áno/nie)", "a": ["nie", "no"]},
        ],
        "solution": r'''# výber cieľa len z povolených indexov
allowed = [i for i in range(16) if (i//4) % 2 == 0]
target = random.choice(allowed)'''
    },
    {
        "title": "Výzva 2: Nikdy nie 2× po sebe rovnaké políčko",
        "desc": "Zabráň tomu, aby sa krtko objavil na rovnakom políčku dva razy po sebe.",
        "tasks": [
            "Pamätaj si last_pos",
            "Pri výbere novej pozície opakuj, kým new != last_pos",
        ],
        "warmup": [
            {"q": "Čo vráti výraz: (5 == 5) ? (True/False)", "a": ["true"]},
            {"q": "Ak last_pos=7 a new_pos=7, máš vybrať znova? (áno/nie)", "a": ["áno", "ano", "yes"]},
        ],
        "solution": r'''# opakovaný výber, kým nie je iné políčko
new_pos = random.randrange(16)
while new_pos == last_pos:
    new_pos = random.randrange(16)
last_pos = new_pos'''
    },
    {
        "title": "Výzva 3: Klik mimo krtka = -1 bod",
        "desc": "Keď žiak klikne na iné políčko než je krtko, odpočítaj 1 bod (minimálne 0).",
        "tasks": [
            "Pri kliku porovnaj clicked_idx s mole_idx",
            "Ak je zle: score = max(0, score-1)",
        ],
        "warmup": [
            {"q": "Čo vráti max(0, -1)?", "a": ["0"]},
            {"q": "Ak score=0 a klik mimo, nové score je?", "a": ["0"]},
        ],
        "solution": r'''def on_click(idx):
    global score
    if idx == mole_idx:
        score += 1
    else:
        score = max(0, score-1)'''
    },
    {
        "title": "Výzva 4: Combo – 3 zásahy po sebe = +2 bonus",
        "desc": "Ak trafíš krtka 3× po sebe bez omylu, pridaj extra +2 body a resetni combo.",
        "tasks": [
            "Maj premennú streak",
            "Pri zásahu streak += 1, pri omyle streak = 0",
            "Ak streak == 3: score += 2 a streak = 0",
        ],
        "warmup": [
            {"q": "Ak streak=2 a trafíš správne, streak bude?", "a": ["3"]},
            {"q": "Po bonuse má byť streak reset na?", "a": ["0"]},
        ],
        "solution": r'''if hit:
    streak += 1
    score += 1
    if streak == 3:
        score += 2
        streak = 0
else:
    streak = 0'''
    },
    {
        "title": "Výzva 5: Zrýchľovanie podľa skóre",
        "desc": "Zrýchľuj interval výskytu krtka: čím vyššie skóre, tým kratší interval (min 300 ms).",
        "tasks": [
            "interval = max(300, 1000 - score*50)",
            "Pri každom presune krtka prepočítaj interval",
        ],
        "warmup": [
            {"q": "Ak score=10, 1000 - score*50 = ?", "a": ["500"]},
            {"q": "Ak vyjde 250ms, po max(300, 250) dostaneš?", "a": ["300"]},
        ],
        "solution": r'''interval = max(300, 1000 - score*50)
timer.set_timeout(move_mole, interval)'''
    },
    {
        "title": "Výzva 6: 30 sekúnd a koniec hry",
        "desc": "Po 30 sekundách hru zastav (žiadne ďalšie presuny), zobraz hlášku s výsledkom.",
        "tasks": [
            "Pri štarte nastav end_time = now + 30s",
            "Pri ticku kontroluj, či už nevypršal čas",
        ],
        "warmup": [
            {"q": "Koľko sekúnd je 0.5 minúty?", "a": ["30"]},
            {"q": "Ak čas vypršal, má sa hra zastaviť? (áno/nie)", "a": ["áno", "ano", "yes"]},
        ],
        "solution": r'''end_ms = window.Date.new().getTime() + 30_000

def tick():
    now = window.Date.new().getTime()
    if now >= end_ms:
        stop_game()
        return
    move_mole()'''
    },
    {
        "title": "Výzva 7: Highscore do localStorage",
        "desc": "Ulož a zobraz najvyššie skóre v localStorage, aktualizuj ho po skončení hry.",
        "tasks": [
            "Načítaj: best = int(local_storage.getItem('best') or '0')",
            "Po hre: ak score > best, ulož nový best",
        ],
        "warmup": [
            {"q": "Ako sa volá úložisko v prehliadači? (localStorage / file)", "a": ["localstorage"]},
            {"q": "Ak best=12 a score=15, uložíš nový best? (áno/nie)", "a": ["áno", "ano", "yes"]},
        ],
        "solution": r'''best = int(local_storage.getItem("best") or "0")
if score > best:
    local_storage.setItem("best", str(score))'''
    },
    {
        "title": "Výzva 8: Difficulty (Easy/Normal/Hard)",
        "desc": "Pridaj voľbu obtiažnosti, ktorá mení interval a penalizáciu za klik mimo.",
        "tasks": [
            "Easy: interval 1200ms, miss -0",
            "Normal: interval 900ms, miss -1",
            "Hard: interval 650ms, miss -2",
        ],
        "warmup": [
            {"q": "Ak miss penalty je -2, pri score=1 po omyle bude max(0, score-2) = ?", "a": ["0"]},
            {"q": "Ktorá obtiažnosť je najrýchlejšia? (easy/normal/hard)", "a": ["hard"]},
        ],
        "solution": r'''difficulty = "hard"
cfg = {"easy": (1200, 0), "normal": (900, 1), "hard": (650, 2)}
base_interval, miss_penalty = cfg[difficulty]'''
    },
]

# -----------------------------
# 3) Helpers: dátum (lokálny)
# -----------------------------
def today_ymd() -> str:
    d = window.Date.new()  # lokálny čas zariadenia
    y = d.getFullYear()
    m = d.getMonth() + 1
    day = d.getDate()
    return f"{y:04d}-{m:02d}-{day:02d}"

def active_index(today: str) -> int:
    idx = -1
    for i, dt in enumerate(RELEASES):
        if dt <= today:
            idx = i
    return idx

# -----------------------------
# 4) Progres: odomykanie riešení
# -----------------------------
LS_KEY = "mqk_unlocked_v1"

def load_unlocked():
    raw = local_storage.getItem(LS_KEY)
    if not raw:
        return set()
    try:
        parts = [p for p in raw.split(",") if p.strip() != ""]
        return set(int(p) for p in parts)
    except Exception:
        return set()

def save_unlocked(s: set):
    local_storage.setItem(LS_KEY, ",".join(str(i) for i in sorted(list(s))))

UNLOCKED = load_unlocked()

def reset_progress(ev=None):
    global UNLOCKED
    UNLOCKED = set()
    local_storage.removeItem(LS_KEY)
    render()

document["btn_reset"].bind("click", reset_progress)

# -----------------------------
# 5) UI render
# -----------------------------
def norm(s: str) -> str:
    return (s or "").strip().lower().replace(" ", "")

def quest_card(i: int, mode: str):
    q = QUESTS[i]
    box = html.DIV(Class="quest")
    box <= html.H3(f"{q['title']}")

    box <= html.DIV(
        html.SPAN(f"Vydanie: {RELEASES[i]}", Class="badge") +
        html.SPAN(("Odomknuté" if i in UNLOCKED else "Zamknuté"), Class="badge"),
        Class="meta"
    )

    box <= html.P(q["desc"], Class="desc")

    ul = html.UL(Class="tasks")
    for t in q["tasks"]:
        ul <= html.LI(t)
    box <= ul

    # Warmup form
    form = html.DIV(Class="qform")
    inputs = []

    for k, item in enumerate(q["warmup"], start=1):
        qi = html.DIV(Class="qitem")
        qi <= html.LABEL(f"{k}. {item['q']}")
        inp = html.INPUT(type="text", placeholder="tvoja odpoveď…")
        qi <= inp
        qi <= html.DIV("Tip: odpoveď píš stručne (napr. 0, true/false, áno/nie).", Class="note")
        form <= qi
        inputs.append((inp, item["a"]))

    msg = html.DIV(Class="row")
    btn = html.BUTTON("Skontrolovať", Class="btn")
    msg <= btn
    status = html.SPAN("", Class="note", **{"aria-live": "polite"})
    msg <= status
    form <= msg

    def check(ev=None):
        ok = True
        for inp, answers in inputs:
            got = norm(inp.value)
            allowed = [norm(a) for a in answers]
            if got in allowed:
                inp.class_name = "input-ok"
            else:
                inp.class_name = "input-err"
                ok = False

        if ok:
            UNLOCKED.add(i)
            save_unlocked(UNLOCKED)
            status.text = "Správne – ukážkové riešenie odomknuté."
            status.class_name = "ok"
            render()
        else:
            status.text = "Niečo nesedí – skús ešte raz."
            status.class_name = "err"

    btn.bind("click", check)
    box <= form

    # Solution
    if i in UNLOCKED:
        sol = html.DIV(Class="solution")
        sol <= html.DIV("Ukážkové riešenie (snippet):", Class="ok")
        sol <= html.PRE(q["solution"])
        box <= sol
    else:
        if mode == "active":
            box <= html.DIV("Riešenie sa odomkne po správnych odpovediach vyššie.", Class="muted")

    return box

def render_banner(today: str, idx: int):
    b = document["banner"]
    b.clear()

    if today < RELEASES[0]:
        b <= html.DIV(f"Séria štartuje {RELEASES[0]}. Dnes je {today}.", Class="muted")
        b <= html.DIV("Tip: v deň štartu sa tu objaví 1. výzva.", Class="muted")
        return

    if today >= SERIES_FULL_FROM:
        b <= html.DIV(f"Dnes je {today}. Séria skončila – zobrazuje sa celý archív 8 výziev.", Class="muted")
        return

    if idx == -1:
        b <= html.DIV(f"Dnes je {today}. Zatiaľ nie je dostupná žiadna výzva.", Class="muted")
        return

    b <= html.DIV(f"Dnes je {today}. Aktuálna je výzva #{idx+1} (od {RELEASES[idx]}).", Class="muted")
    b <= html.DIV("Pravidlo: vidíš aktuálnu výzvu + v archíve predchádzajúcu.", Class="muted")

def render():
    today = today_ymd()
    idx = active_index(today)

    render_banner(today, idx)

    active = document["active_area"]
    arch = document["archive_area"]
    active.clear()
    arch.clear()

    # Aktívna
    if today < RELEASES[0]:
        active <= html.DIV("Ešte nezačalo. 🙂", Class="muted")
    else:
        if idx >= 0:
            active <= quest_card(idx, "active")
        else:
            active <= html.DIV("Zatiaľ nič.", Class="muted")

    # Archív
    if today >= SERIES_FULL_FROM:
        for i in range(len(QUESTS)):
            row = html.DIV(Class="arch-item")
            row <= html.DIV(f"#{i+1} • {QUESTS[i]['title']}", Class="note")
            btn = html.BUTTON("Otvoriť", Class="btn ghost")
            row <= btn

            def make_open(ii):
                def _open(ev=None):
                    active.clear()
                    active <= quest_card(ii, "active")
                    window.scrollTo(0, 0)
                return _open

            btn.bind("click", make_open(i))
            arch <= row
    else:
        prev = idx - 1
        if prev >= 0:
            row = html.DIV(Class="arch-item")
            row <= html.DIV(f"#{prev+1} • {QUESTS[prev]['title']}", Class="note")
            btn = html.BUTTON("Otvoriť", Class="btn ghost")
            row <= btn

            def open_prev(ev=None):
                active.clear()
                active <= quest_card(prev, "active")
                window.scrollTo(0, 0)

            btn.bind("click", open_prev)
            arch <= row
        else:
            arch <= html.DIV("Zatiaľ nič v archíve.", Class="muted")

# -----------------------------
# 6) Baseline Krtko demo
# -----------------------------
GRID = document["grid"]
score_el = document["score"]
time_el = document["time"]

mole_idx = None
score = 0
running = False
tick_id = None
move_id = None
end_ms = None

cells = []

def build_grid():
    GRID.clear()
    cells.clear()
    for i in range(16):
        c = html.DIV(Class="cell")
        c <= html.DIV("", Class="mole")
        def make_click(ii):
            def _click(ev=None):
                on_cell_click(ii)
            return _click
        c.bind("click", make_click(i))
        GRID <= c
        cells.append(c)

def show_mole(idx):
    for c in cells:
        c.children[0].text = ""
    cells[idx].children[0].text = "🦫"  # baseline ikona (vymeníš za obrázok, ak chceš)

def hide_mole():
    for c in cells:
        c.children[0].text = ""

def move_mole():
    global mole_idx, move_id
    if not running:
        return
    mole_idx = random.randrange(16)
    show_mole(mole_idx)
    move_id = timer.set_timeout(move_mole, 900)  # baseline interval

def update_time():
    global tick_id
    if not running:
        return
    now = window.Date.new().getTime()
    left = max(0, int((end_ms - now) / 1000))
    time_el.text = str(left)
    if left <= 0:
        stop_game()
        return
    tick_id = timer.set_timeout(update_time, 250)

def start_game(ev=None):
    global running, score, end_ms
    if running:
        return
    running = True
    score = 0
    score_el.text = "0"
    end_ms = window.Date.new().getTime() + 30_000
    time_el.text = "30"
    move_mole()
    update_time()

def stop_game(ev=None):
    global running, tick_id, move_id
    running = False
    if tick_id is not None:
        try: timer.clear_timeout(tick_id)
        except Exception: pass
    if move_id is not None:
        try: timer.clear_timeout(move_id)
        except Exception: pass
    hide_mole()

def on_cell_click(idx):
    global score
    if not running:
        return
    if idx == mole_idx:
        score += 1
        score_el.text = str(score)

document["btn_start"].bind("click", start_game)
document["btn_stop"].bind("click", stop_game)

build_grid()
render()
