#!/usr/bin/env python3
from __future__ import annotations

import json
import time
import tkinter as tk
import unicodedata
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

BASE_DIR = Path(__file__).resolve().parent
SPECIES_DIR = BASE_DIR / "species-catalog"
CLAUDE_JSON = Path.home() / ".claude.json"
APP_SETTINGS = BASE_DIR / "buddy_desktop_settings.json"
APP_ICON_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAE8AAAA3CAIAAADCJ4B9AAABM0lEQVR4AeyYwQ3CMAxF"
    "Uc8swgBMwQAMwQDMwAAMwQBMwQCsQ6RKlhVSy3LTxnF+5YOxE+P/3wHU6TjSMx1GeqA2Lm0t"
    "28/t4jw0jLRqNbP8n4Fa/4ysG4Kt1Tn/98DWPyPrhmBrdc7/vQpsT48XRXXBNHlOVs6voHbl"
    "Bnteh1rZ7Z67YNszPXl3sJX96bk7MFvhXYxA9Hu/UgjHbC2aPCfCEM3yA7MVnIvRAtsYHEsq"
    "wLbkSowa2MbgWFIxMNvz870UJad81ZY2T3VadA+29GXNE6htjmCzBcB2M2ubDwbb5gg2WwBs"
    "S9am32iKrE/1lAit1FUGH5JdUbb4MZ6DLXcjVg62sXhyNWDL3YiVg20snlyNT7Z8w5q5RW3d"
    "/zf/avj8rCu0spPFjxa1xUFdFMdS+wMAAP//QEWmvwAAAAZJREFUAwAkFf6Lc4qkBwAAAAB"
    "JRU5ErkJggg=="
)

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary"]
SHINY_ORDER = ["false", "true"]
BG = "#151515"
PANEL_BG = "#1e1e1e"
FG = "#d9d9d9"
ACCENT = "#ff9966"
LEFT_PANEL_WIDTH = 800
RIGHT_PANEL_WIDTH = 200
RARITY_COLORS = {
    "common": "#9aa0a6",
    "uncommon": "#4caf50",
    "rare": "#42a5f5",
    "epic": "#ab47bc",
    "legendary": "#ffb300",
}
HAT_SYMBOLS = {
    "none": "",
    "beanie": "(___)",
    "crown": r"\^^^/",
    "halo": "(   )",
    "tophat": "[___]",
    "propeller": "-+-",
    "wizard": "/^\\",
    "tinyduck": ",>",
}

LANGUAGE_CHOICES = [
    ("en", "English"),
    ("zh-CN", "中文(简体)"),
    ("zh-TW", "中文(繁體)"),
    ("ja", "日本語"),
    ("ko", "한국어"),
    ("fr", "Français"),
    ("de", "Deutsch"),
    ("es", "Español"),
    ("pt-BR", "Português (Brasil)"),
    ("it", "Italiano"),
    ("ru", "Русский"),
    ("ar", "العربية"),
    ("hi", "हिन्दी"),
    ("id", "Bahasa Indonesia"),
    ("vi", "Tiếng Việt"),
    ("tr", "Türkçe"),
    ("nl", "Nederlands"),
    ("pl", "Polski"),
]

I18N = {
    "en": {
        "tab_main": "Main",
        "tab_language": "Language",
        "language_title": "Localization",
        "language_desc": "Choose UI language (default: English)",
        "preview": "Preview",
        "species": "1) Species",
        "rarity": "2) Rarity",
        "hat": "3) Hat",
        "eye": "4) Eye",
        "shiny": "5) Shiny (default true)",
        "settings": "Apply & Settings",
        "settings_path": "settings.json path:",
        "browse": "Browse...",
        "name": "name",
        "personality": "personality",
        "userid": "userId:",
        "copy": "Copy",
        "apply": "Apply to .claude.json",
        "ready": "Ready",
        "loaded": "Loaded {species}, {count} records",
        "matched": "",
        "not_matched": "No matching record",
        "copied": "Copied userId",
        "no_userid": "No userId to copy",
        "path_error": "Config file not found:\n{path}",
        "apply_done": "Updated config:\n{path}\n\nuserID: {uid}\nbackup: {backup}",
        "warn_select": "Please finish selection first",
        "choose_config": "Choose settings.json / .claude.json",
        "load_failed": "Load failed",
        "write_failed": "Write failed",
        "complete": "Done",
        "hint_pick": "Please finish selection to show stats",
        "preview_missing": "(Preview for this species is not added yet)",
        "title_warning": "Warning",
        "title_error": "Error",
        "title_info": "Info",
        "title_startup_failed": "Startup failed",
        "path_help": (
            "Config file not found:\n{path}\n\n"
            "I copied the current userId to clipboard.\n"
            "Please ask Claude Code to analyze your current files and locate the real settings file path,\n"
            "then paste this userId into the correct place."
        ),
    },
    "zh-CN": {
        "tab_main": "主界面",
        "tab_language": "语言",
        "language_title": "本地化",
        "language_desc": "选择界面语言（默认：英语）",
        "preview": "预览",
        "species": "1) 物种",
        "rarity": "2) 稀有度",
        "hat": "3) 帽子",
        "eye": "4) 眼睛",
        "shiny": "5) 闪光（默认 true）",
        "settings": "应用与设置",
        "settings_path": "settings.json 路径:",
        "browse": "浏览...",
        "name": "name",
        "personality": "personality",
        "userid": "userId:",
        "copy": "复制",
        "apply": "一键应用到 .claude.json",
        "ready": "准备就绪",
        "loaded": "已加载 {species}，共 {count} 条",
        "matched": "",
        "not_matched": "未匹配到记录",
        "copied": "已复制 userId",
        "no_userid": "当前没有可复制的 userId",
        "path_error": "配置文件不存在:\n{path}",
        "apply_done": "已更新配置文件:\n{path}\n\nuserID: {uid}\nbackup: {backup}",
        "warn_select": "请先完成筛选并选中一个结果",
        "choose_config": "选择 settings.json / .claude.json",
        "load_failed": "加载失败",
        "write_failed": "写入失败",
        "complete": "完成",
        "hint_pick": "请选择完整条件以显示属性",
        "preview_missing": "(该物种预览图待补充)",
        "title_warning": "提示",
        "title_error": "错误",
        "title_info": "完成",
        "title_startup_failed": "启动失败",
        "path_help": (
            "配置文件不存在：\n{path}\n\n"
            "已将当前 userId 复制到剪贴板。\n"
            "请让 Claude Code 分析你当前工程文件，定位真实的 settings/.claude 配置路径，\n"
            "然后把该 userId 粘贴到对应位置。"
        ),
    },
}


def _add_lang(code: str, **overrides) -> None:
    I18N[code] = {**I18N["en"], **overrides}


_add_lang(
    "zh-TW",
    tab_main="主介面",
    tab_language="語言",
    language_title="本地化",
    language_desc="選擇介面語言（預設：英文）",
    preview="預覽",
    species="1) 物種",
    rarity="2) 稀有度",
    hat="3) 帽子",
    eye="4) 眼睛",
    shiny="5) 閃光（預設 true）",
    settings="套用與設定",
    settings_path="settings.json 路徑:",
    browse="瀏覽...",
    copy="複製",
    apply="一鍵套用到 .claude.json",
    ready="準備就緒",
    loaded="已載入 {species}，共 {count} 筆",
)
_add_lang(
    "ja",
    tab_main="メイン",
    tab_language="言語",
    language_title="ローカライズ",
    language_desc="UI 言語を選択（デフォルト: 英語）",
    preview="プレビュー",
    species="1) 種類",
    rarity="2) レア度",
    hat="3) 帽子",
    eye="4) 目",
    shiny="5) シャイニー（既定 true）",
    settings="適用と設定",
    settings_path="settings.json パス:",
    browse="参照...",
    copy="コピー",
    apply=".claude.json に適用",
    ready="準備完了",
    loaded="{species} を読み込みました（{count} 件）",
)
_add_lang(
    "ko",
    tab_main="메인",
    tab_language="언어",
    language_title="현지화",
    language_desc="UI 언어 선택(기본: 영어)",
    preview="미리보기",
    species="1) 종족",
    rarity="2) 희귀도",
    hat="3) 모자",
    eye="4) 눈",
    shiny="5) 샤이니(기본 true)",
    settings="적용 및 설정",
    settings_path="settings.json 경로:",
    browse="찾아보기...",
    copy="복사",
    apply=".claude.json에 적용",
    ready="준비됨",
    loaded="{species} 로드 완료, {count}개",
)
_add_lang(
    "fr",
    tab_main="Principal",
    tab_language="Langue",
    language_title="Localisation",
    language_desc="Choisir la langue de l'interface (défaut: anglais)",
    preview="Aperçu",
    species="1) Espèce",
    rarity="2) Rareté",
    hat="3) Chapeau",
    eye="4) Yeux",
    shiny="5) Shiny (défaut true)",
    settings="Appliquer & Paramètres",
    settings_path="Chemin settings.json :",
    browse="Parcourir...",
    copy="Copier",
    apply="Appliquer à .claude.json",
    ready="Prêt",
    loaded="{species} chargé, {count} entrées",
)
_add_lang(
    "de",
    tab_main="Hauptseite",
    tab_language="Sprache",
    language_title="Lokalisierung",
    language_desc="UI-Sprache wählen (Standard: Englisch)",
    preview="Vorschau",
    species="1) Spezies",
    rarity="2) Seltenheit",
    hat="3) Hut",
    eye="4) Augen",
    shiny="5) Shiny (Standard true)",
    settings="Anwenden & Einstellungen",
    settings_path="settings.json Pfad:",
    browse="Durchsuchen...",
    copy="Kopieren",
    apply="Auf .claude.json anwenden",
    ready="Bereit",
    loaded="{species} geladen, {count} Einträge",
)
_add_lang(
    "es",
    tab_main="Principal",
    tab_language="Idioma",
    language_title="Localización",
    language_desc="Elegir idioma de la interfaz (predeterminado: inglés)",
    preview="Vista previa",
    species="1) Especie",
    rarity="2) Rareza",
    hat="3) Sombrero",
    eye="4) Ojos",
    shiny="5) Shiny (por defecto true)",
    settings="Aplicar y Ajustes",
    settings_path="Ruta de settings.json:",
    browse="Examinar...",
    copy="Copiar",
    apply="Aplicar a .claude.json",
    ready="Listo",
    loaded="{species} cargado, {count} registros",
)
_add_lang(
    "pt-BR",
    tab_main="Principal",
    tab_language="Idioma",
    language_title="Localização",
    language_desc="Escolha o idioma da interface (padrão: inglês)",
    preview="Pré-visualização",
    species="1) Espécie",
    rarity="2) Raridade",
    hat="3) Chapéu",
    eye="4) Olhos",
    shiny="5) Shiny (padrão true)",
    settings="Aplicar e Configurações",
    settings_path="Caminho do settings.json:",
    browse="Procurar...",
    copy="Copiar",
    apply="Aplicar ao .claude.json",
    ready="Pronto",
    loaded="{species} carregado, {count} registros",
)
_add_lang(
    "it",
    tab_main="Principale",
    tab_language="Lingua",
    language_title="Localizzazione",
    language_desc="Scegli la lingua dell'interfaccia (predefinita: inglese)",
    preview="Anteprima",
    species="1) Specie",
    rarity="2) Rarità",
    hat="3) Cappello",
    eye="4) Occhi",
    shiny="5) Shiny (predefinito true)",
    settings="Applica e Impostazioni",
    settings_path="Percorso settings.json:",
    browse="Sfoglia...",
    copy="Copia",
    apply="Applica a .claude.json",
)
_add_lang(
    "ru",
    tab_main="Главная",
    tab_language="Язык",
    language_title="Локализация",
    language_desc="Выберите язык интерфейса (по умолчанию: английский)",
    preview="Предпросмотр",
    species="1) Вид",
    rarity="2) Редкость",
    hat="3) Шляпа",
    eye="4) Глаза",
    shiny="5) Shiny (по умолчанию true)",
    settings="Применение и настройки",
    settings_path="Путь settings.json:",
    browse="Обзор...",
    copy="Копировать",
    apply="Применить к .claude.json",
)
_add_lang(
    "ar",
    tab_main="الرئيسية",
    tab_language="اللغة",
    language_title="الترجمة",
    language_desc="اختر لغة الواجهة (الافتراضي: الإنجليزية)",
    preview="معاينة",
    species="1) النوع",
    rarity="2) الندرة",
    hat="3) القبعة",
    eye="4) العين",
    shiny="5) لامع (افتراضي true)",
    settings="تطبيق وإعدادات",
    settings_path="مسار settings.json:",
    browse="استعراض...",
    copy="نسخ",
    apply="تطبيق على .claude.json",
)
_add_lang(
    "hi",
    tab_main="मुख्य",
    tab_language="भाषा",
    language_title="स्थानीयकरण",
    language_desc="इंटरफ़ेस भाषा चुनें (डिफ़ॉल्ट: अंग्रेज़ी)",
    preview="पूर्वावलोकन",
    species="1) प्रजाति",
    rarity="2) दुर्लभता",
    hat="3) टोपी",
    eye="4) आँख",
    shiny="5) शाइनी (डिफ़ॉल्ट true)",
    settings="लागू करें और सेटिंग्स",
    settings_path="settings.json पथ:",
    browse="ब्राउज़...",
    copy="कॉपी",
    apply=".claude.json पर लागू करें",
)
_add_lang(
    "id",
    tab_main="Utama",
    tab_language="Bahasa",
    language_title="Lokalisasi",
    language_desc="Pilih bahasa antarmuka (default: Inggris)",
    preview="Pratinjau",
    species="1) Spesies",
    rarity="2) Kelangkaan",
    hat="3) Topi",
    eye="4) Mata",
    shiny="5) Shiny (default true)",
    settings="Terapkan & Pengaturan",
    settings_path="Path settings.json:",
    browse="Telusuri...",
    copy="Salin",
    apply="Terapkan ke .claude.json",
)
_add_lang(
    "vi",
    tab_main="Chính",
    tab_language="Ngôn ngữ",
    language_title="Bản địa hóa",
    language_desc="Chọn ngôn ngữ giao diện (mặc định: tiếng Anh)",
    preview="Xem trước",
    species="1) Loài",
    rarity="2) Độ hiếm",
    hat="3) Mũ",
    eye="4) Mắt",
    shiny="5) Shiny (mặc định true)",
    settings="Áp dụng & Cài đặt",
    settings_path="Đường dẫn settings.json:",
    browse="Duyệt...",
    copy="Sao chép",
    apply="Áp dụng vào .claude.json",
)
_add_lang(
    "tr",
    tab_main="Ana",
    tab_language="Dil",
    language_title="Yerelleştirme",
    language_desc="Arayüz dilini seçin (varsayılan: İngilizce)",
    preview="Önizleme",
    species="1) Tür",
    rarity="2) Nadirlik",
    hat="3) Şapka",
    eye="4) Göz",
    shiny="5) Shiny (varsayılan true)",
    settings="Uygula ve Ayarlar",
    settings_path="settings.json yolu:",
    browse="Gözat...",
    copy="Kopyala",
    apply=".claude.json'a uygula",
)
_add_lang(
    "nl",
    tab_main="Hoofd",
    tab_language="Taal",
    language_title="Lokalisatie",
    language_desc="Kies de UI-taal (standaard: Engels)",
    preview="Voorbeeld",
    species="1) Soort",
    rarity="2) Zeldzaamheid",
    hat="3) Hoed",
    eye="4) Oog",
    shiny="5) Shiny (standaard true)",
    settings="Toepassen & Instellingen",
    settings_path="settings.json pad:",
    browse="Bladeren...",
    copy="Kopiëren",
    apply="Toepassen op .claude.json",
)
_add_lang(
    "pl",
    tab_main="Główna",
    tab_language="Język",
    language_title="Lokalizacja",
    language_desc="Wybierz język interfejsu (domyślnie: angielski)",
    preview="Podgląd",
    species="1) Gatunek",
    rarity="2) Rzadkość",
    hat="3) Kapelusz",
    eye="4) Oko",
    shiny="5) Shiny (domyślnie true)",
    settings="Zastosuj i ustawienia",
    settings_path="Ścieżka settings.json:",
    browse="Przeglądaj...",
    copy="Kopiuj",
    apply="Zastosuj do .claude.json",
)


def load_app_settings() -> dict:
    if not APP_SETTINGS.exists():
        return {}
    try:
        return json.loads(APP_SETTINGS.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_app_settings(data: dict) -> None:
    APP_SETTINGS.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

SPECIES_ART_BUTTON = {
    "axolotl": r"""
 }~(______)~{
 }~(@ .. @)~{
 ( .--. )
 (_/  \_)
""".strip("\n"),
    "blob": r"""
 .----.
(@    @)
(      )
`----´
""".strip("\n"),
    "cactus": r"""
n  ____  n
| |@  @| |
|_|    |_|
 |    |
""".strip("\n"),
    "capybara": r"""
n______n
(@    @)
(  oo  )
`------´
""".strip("\n"),
    "cat": r"""
/\_/\
(@   @)
(  ω  )
(")_(")
""".strip("\n"),
    "chonk": r"""
/\    /\
( @    @ )
(   ..   )
`------´
""".strip("\n"),
    "dragon": r"""
/^\  /^\
<  @  @  >
(   ~~   )
`-vvvv-´
""".strip("\n"),
    "duck": r"""
__
<( @ )___
(  ._>
  `--´
""".strip("\n"),
    "ghost": r"""
.----.
/ @  @ \
|      |
~`~``~`~
""".strip("\n"),
    "goose": r"""
( @ >
||
_(__)_
^^^^
""".strip("\n"),
    "mushroom": r"""
.-o-OO-o-.
(__________)
|@  @|
|____|
""".strip("\n"),
    "octopus": r"""
.----.
(@  @)
(______)
/\/\/\/\
""".strip("\n"),
    "owl": r"""
/\  /\
((@)(@))
(  ><  )
`----´
""".strip("\n"),
    "penguin": r"""
(@>@)
/(   )\
`---´
""".strip("\n"),
    "rabbit": r"""
(\__/)
(@  @)
=(  ..  )=
(")__(")
""".strip("\n"),
    "robot": r"""
.[||].
[@  @]
[ ==== ]
`------´
""".strip("\n"),
    "snail": r"""
@    .--.
\  ( @ )
 \_`--´
~~~~~~~
""".strip("\n"),
    "turtle": r"""
_,--._
(@  @)
/[______]\
``    ``
""".strip("\n"),
}

SPECIES_ART_PREVIEW = {
    "axolotl": r"""
  }~(______)~{
  }~(@ .. @)~{
    ( .--. )
    (_/  \_)
""".strip("\n"),
    "blob": r"""
     .----.
    ( @  @ )
    (      )
     `----´
""".strip("\n"),
    "cactus": r"""
   n  ____  n
   | |@  @| |
   |_|    |_|
     |    |
""".strip("\n"),
    "capybara": r"""
    n______n
   ( @    @ )
   (   oo   )
    `------´
""".strip("\n"),
    "cat": r"""
     /\_/\
    ( @   @)
    (  ω  )
    (")_(")
""".strip("\n"),
    "chonk": r"""
    /\    /\
   ( @    @ )
   (   ..   )
    `------´
""".strip("\n"),
    "dragon": r"""
    /^\  /^\
   <  @  @  >
   (   ~~   )
    `-vvvv-´
""".strip("\n"),
    "duck": r"""
      __
    <(@ )___
     (  ._>
      `--´
""".strip("\n"),
    "ghost": r"""
     .----.
    / @  @ \
    |      |
    ~`~``~`~
""".strip("\n"),
    "goose": r"""
       (@>
       ||
     _(__)_
      ^^^^
""".strip("\n"),
    "mushroom": r"""
   .-o-OO-o-.
  (__________)
     |@  @|
     |____|
""".strip("\n"),
    "octopus": r"""
     .----.
    ( @  @ )
    (______)
    /\/\/\/\
""".strip("\n"),
    "owl": r"""
     /\  /\
    ((@)(@))
    (  ><  )
     `----´
""".strip("\n"),
    "penguin": r"""
    (@>@)
   /(   )\
    `---´
""".strip("\n"),
    "rabbit": r"""
     (\__/)
    ( @  @ )
   =(  ..  )=
    (")__(")
""".strip("\n"),
    "robot": r"""
     .[||].
    [ @  @ ]
    [ ==== ]
    `------´
""".strip("\n"),
    "snail": r"""
   @    .--.
    \  ( @ )
     \_`--´
    ~~~~~~~
""".strip("\n"),
    "turtle": r"""
     _,--._
    ( @  @ )
   /[______]\
    ``    ``
""".strip("\n"),
}


def load_species_index() -> list[str]:
    index_path = SPECIES_DIR / "_index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Index file not found: {index_path}")
    data = json.loads(index_path.read_text(encoding="utf-8"))
    species = data.get("species", [])
    if not isinstance(species, list) or not species:
        raise RuntimeError("Species index is empty. Please generate species-catalog first.")
    return species


def load_species_records(species: str) -> list[dict]:
    path = SPECIES_DIR / f"{species}.json"
    if not path.exists():
        raise FileNotFoundError(f"Species file not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("records", [])


def rarity_rank(rarity: str) -> int:
    try:
        return RARITY_ORDER.index(rarity)
    except ValueError:
        return -1


def stats_total(rec: dict) -> int:
    stats = rec.get("match", {}).get("bones", {}).get("stats", {})
    return int(sum(int(v) for v in stats.values()))


def stat_bar(value: int, width: int = 10) -> str:
    filled = max(0, min(width, round((value / 100) * width)))
    return ("█" * filled) + ("░" * (width - filled))


def display_width(text: str) -> int:
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return width


def fit_display_width(text: str, max_width: int) -> str:
    out: list[str] = []
    used = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        w = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if used + w > max_width:
            break
        out.append(ch)
        used += w
    return "".join(out)


def render_species_art(species: str, eye_symbol: str, hat_symbol: str) -> str:
    template = SPECIES_ART_PREVIEW.get(species, "(Preview for this species is not added yet)")
    eye = eye_symbol if eye_symbol else "@"
    base = template.replace("@", eye)
    if not hat_symbol or hat_symbol == "none":
        return base
    lines = base.splitlines()
    if not lines:
        return base
    maxw = max(display_width(ln) for ln in lines)
    hat = hat_symbol
    # Shift hat right and down a little to sit on top.
    pad = max(0, (maxw - display_width(hat)) // 2 + 2)
    hat_line = (" " * pad) + hat
    return "\n".join(["", hat_line, *lines])


def write_claude_config(config_path: Path, user_id: str) -> Path:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    raw = config_path.read_text(encoding="utf-8")
    data = json.loads(raw)

    backup_path = config_path.with_suffix(f".json.bak-{int(time.time())}")
    backup_path.write_text(raw, encoding="utf-8")

    data["userID"] = user_id
    data.pop("companion", None)
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return backup_path


class App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ClaudeCodeBuddy Manager")
        self.root.geometry("1100x800")
        self.root.resizable(True, True)
        self.root.minsize(1100, 800)
        self.root.configure(bg=BG)
        self._icon_img: tk.PhotoImage | None = None
        try:
            self._icon_img = tk.PhotoImage(data=APP_ICON_B64)
            self.root.iconphoto(True, self._icon_img)
        except Exception:
            pass

        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG)
        style.configure("TEntry", fieldbackground=PANEL_BG, foreground=FG)
        style.configure("TButton", background=PANEL_BG, foreground=FG)
        style.map("TButton", background=[("active", "#2a2a2a")])

        self.species_list = load_species_index()
        self.current_records: list[dict] = []
        self.selected_record: dict | None = None
        self.app_settings = load_app_settings()
        supported_codes = {code for code, _ in LANGUAGE_CHOICES}
        saved_lang = self.app_settings.get("language", "en")
        if saved_lang not in supported_codes:
            saved_lang = "en"

        self.species_var = tk.StringVar()
        self.lang_var = tk.StringVar(value=saved_lang)
        default_display = next((label for code, label in LANGUAGE_CHOICES if code == saved_lang), LANGUAGE_CHOICES[0][1])
        self.lang_display_var = tk.StringVar(value=default_display)
        self.rarity_var = tk.StringVar()
        self.hat_var = tk.StringVar()
        self.eye_var = tk.StringVar()
        self.shiny_var = tk.StringVar()
        self.user_id_var = tk.StringVar(value="")
        self.status_var = tk.StringVar(value=self.t("ready"))
        self.config_path_var = tk.StringVar(value=str(CLAUDE_JSON))

        self._build_ui()
        self._init_defaults()

    def t(self, key: str, **kwargs) -> str:
        lang = self.lang_var.get().strip() or "en"
        text = I18N.get(lang, I18N["en"]).get(key, I18N["en"].get(key, key))
        return text.format(**kwargs)

    def _species_button_text(self, species: str) -> str:
        art = SPECIES_ART_BUTTON.get(species, "")
        if not art:
            return species.upper()
        lines = [ln.rstrip() for ln in art.splitlines() if ln.strip()]
        if not lines:
            return species.upper()
        return "\n".join(lines + [species.upper()])

    def _build_ui(self) -> None:
        self.notebook = ttk.Notebook(self.root)
        self.main_tab = ttk.Frame(self.notebook)
        self.lang_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text=self.t("tab_main"))
        self.notebook.add(self.lang_tab, text=self.t("tab_language"))
        self.notebook.pack(fill="both", expand=True)

        self._build_language_tab()

        layout = ttk.Frame(self.main_tab)
        layout.pack(fill="both", expand=True, padx=12, pady=10)
        layout.columnconfigure(0, minsize=LEFT_PANEL_WIDTH, weight=0)
        layout.columnconfigure(1, minsize=RIGHT_PANEL_WIDTH, weight=0)
        layout.columnconfigure(2, weight=1)
        layout.rowconfigure(0, weight=1)

        left = ttk.Frame(layout, width=LEFT_PANEL_WIDTH)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        right = ttk.Frame(layout, width=RIGHT_PANEL_WIDTH)
        right.grid(row=0, column=1, sticky="ns")
        left.grid_propagate(False)
        right.grid_propagate(False)
        left.columnconfigure(0, weight=1)

        self.lbl_preview = ttk.Label(right, text=self.t("preview"))
        self.lbl_preview.pack(anchor="w", pady=(0, 6))
        self.preview = tk.Text(right, wrap="word", font=("Consolas", 10), height=42, borderwidth=0, highlightthickness=0)
        self.preview.pack(fill="both", expand=True)
        self.preview.configure(state="disabled", bg="#0b0b0b", fg="#d9d9d9", insertbackground="#d9d9d9")
        self.preview.tag_config("gold", foreground="#ffcc33")
        self.preview.tag_config("muted", foreground="#d9d9d9")
        self.preview.tag_config("personality", foreground="#a8a8a8")
        self.preview.tag_config("stats", foreground="#d9d9d9")

        controls = ttk.Frame(left)
        controls.grid(row=0, column=0, sticky="nsew")
        controls.columnconfigure(0, weight=1)

        species_box = ttk.Frame(controls)
        species_box.pack(fill="x", pady=(4, 6))
        self.lbl_species = ttk.Label(species_box, text=self.t("species"))
        self.lbl_species.pack(anchor="w")
        species_grid = ttk.Frame(species_box)
        species_grid.pack(fill="x", pady=(4, 0))
        self.species_buttons: dict[str, tk.Button] = {}
        for idx, species in enumerate(self.species_list):
            r = idx // 6
            c = idx % 6
            btn = tk.Button(
                species_grid,
                text=self._species_button_text(species),
                width=18,
                height=6,
                font=("Consolas", 9),
                justify="center",
                relief="raised",
                bg=PANEL_BG,
                fg=FG,
                activebackground="#2a2a2a",
                activeforeground=FG,
                highlightthickness=0,
                bd=1,
                command=lambda s=species: self.select_species(s),
            )
            btn.grid(row=r, column=c, padx=4, pady=4, sticky="ew")
            self.species_buttons[species] = btn
            species_grid.grid_columnconfigure(c, weight=1)

        rarity_box = ttk.Frame(controls)
        rarity_box.pack(fill="x", pady=6)
        self.lbl_rarity = ttk.Label(rarity_box, text=self.t("rarity"))
        self.lbl_rarity.pack(anchor="w")
        self.rarity_row = ttk.Frame(rarity_box)
        self.rarity_row.pack(fill="x", pady=(4, 0))
        self.rarity_buttons: dict[str, tk.Button] = {}

        hat_box = ttk.Frame(controls)
        hat_box.pack(fill="x", pady=6)
        self.lbl_hat = ttk.Label(hat_box, text=self.t("hat"))
        self.lbl_hat.pack(anchor="w")
        self.hat_row = ttk.Frame(hat_box)
        self.hat_row.pack(fill="x", pady=(4, 0))
        self.hat_buttons: dict[str, tk.Button] = {}

        eye_box = ttk.Frame(controls)
        eye_box.pack(fill="x", pady=6)
        self.lbl_eye = ttk.Label(eye_box, text=self.t("eye"))
        self.lbl_eye.pack(anchor="w")
        self.eye_row = ttk.Frame(eye_box)
        self.eye_row.pack(fill="x", pady=(4, 0))
        self.eye_buttons: dict[str, tk.Button] = {}

        shiny_box = ttk.Frame(controls)
        shiny_box.pack(fill="x", pady=6)
        self.lbl_shiny = ttk.Label(shiny_box, text=self.t("shiny"))
        self.lbl_shiny.pack(anchor="w")
        self.shiny_row = ttk.Frame(shiny_box)
        self.shiny_row.pack(fill="x", pady=(4, 0))
        self.shiny_buttons: dict[str, tk.Button] = {}
        for shiny in ("true", "false"):
            btn = tk.Button(
                self.shiny_row,
                text=shiny,
                width=10,
                bg=PANEL_BG,
                fg=FG,
                activebackground="#2a2a2a",
                activeforeground=FG,
                highlightthickness=0,
                bd=1,
                command=lambda s=shiny: self.select_shiny(s),
            )
            btn.pack(side="left", padx=4)
            self.shiny_buttons[shiny] = btn

        apply_box = ttk.Frame(controls)
        apply_box.pack(fill="x", pady=(10, 0))
        self.lbl_settings = ttk.Label(apply_box, text=self.t("settings"))
        self.lbl_settings.pack(anchor="w")

        path_row = ttk.Frame(apply_box)
        path_row.pack(fill="x", pady=(0, 6))
        self.lbl_settings_path = ttk.Label(path_row, text=self.t("settings_path"))
        self.lbl_settings_path.pack(side="left")
        ttk.Entry(path_row, textvariable=self.config_path_var, width=62).pack(side="left", padx=(6, 8))
        self.btn_browse = ttk.Button(path_row, text=self.t("browse"), command=self.choose_config_path)
        self.btn_browse.pack(side="left")

        top = ttk.Frame(apply_box)
        top.pack(fill="x", pady=(0, 6))
        self.lbl_userid = ttk.Label(top, text=self.t("userid"))
        self.lbl_userid.pack(side="left")
        ttk.Entry(top, textvariable=self.user_id_var, width=62, state="readonly").pack(side="left", padx=(6, 8))
        self.btn_copy = ttk.Button(top, text=self.t("copy"), command=self.copy_user_id)
        self.btn_copy.pack(side="left")
        self.btn_apply = ttk.Button(top, text=self.t("apply"), command=self.apply_to_claude)
        self.btn_apply.pack(side="left", padx=8)
        status = ttk.Frame(controls)
        status.pack(fill="x", pady=(6, 0))
        ttk.Label(status, textvariable=self.status_var).pack(side="left")

    def _build_language_tab(self) -> None:
        container = ttk.Frame(self.lang_tab)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        self.lbl_language_title = ttk.Label(container, text=self.t("language_title"))
        self.lbl_language_title.pack(anchor="w")
        self.lbl_language_desc = ttk.Label(container, text=self.t("language_desc"))
        self.lbl_language_desc.pack(anchor="w", pady=(4, 12))
        display_values = [label for _, label in LANGUAGE_CHOICES]
        self.lang_choice_combo = ttk.Combobox(
            container,
            values=display_values,
            textvariable=self.lang_display_var,
            state="readonly",
            width=32,
        )
        self.lang_choice_combo.pack(anchor="w")
        self.lang_choice_combo.bind("<<ComboboxSelected>>", self.on_language_change)

    def on_language_change(self, _event=None) -> None:
        selected_label = self.lang_display_var.get().strip()
        code = "en"
        for c, label in LANGUAGE_CHOICES:
            if label == selected_label:
                code = c
                break
        self.lang_var.set(code)
        self.app_settings["language"] = code
        save_app_settings(self.app_settings)
        self.refresh_language()

    def refresh_language(self) -> None:
        self.notebook.tab(0, text=self.t("tab_main"))
        self.notebook.tab(1, text=self.t("tab_language"))
        self.lbl_language_title.configure(text=self.t("language_title"))
        self.lbl_language_desc.configure(text=self.t("language_desc"))
        self.lbl_preview.configure(text=self.t("preview"))
        self.lbl_species.configure(text=self.t("species"))
        self.lbl_rarity.configure(text=self.t("rarity"))
        self.lbl_hat.configure(text=self.t("hat"))
        self.lbl_eye.configure(text=self.t("eye"))
        self.lbl_shiny.configure(text=self.t("shiny"))
        self.lbl_settings.configure(text=self.t("settings"))
        self.lbl_settings_path.configure(text=self.t("settings_path"))
        self.lbl_userid.configure(text=self.t("userid"))
        self.btn_copy.configure(text=self.t("copy"))
        self.btn_apply.configure(text=self.t("apply"))
        self.btn_browse.configure(text=self.t("browse"))
        if not self.status_var.get().strip():
            self.status_var.set(self.t("ready"))
        self._render_preview()

    def _init_defaults(self) -> None:
        if not self.species_list:
            return
        self.select_species(self.species_list[0])

    def _set_selected_button(
        self,
        button_map: dict[str, tk.Button],
        selected_key: str,
        text_colors: dict[str, str] | None = None,
    ) -> None:
        for key, btn in button_map.items():
            fg_color = text_colors.get(key, FG) if text_colors else FG
            if key == selected_key:
                btn.configure(relief="sunken", bg="#3b2518", fg=fg_color)
            else:
                btn.configure(relief="raised", bg=PANEL_BG, fg=fg_color)

    def _clear_row(self, row: ttk.Frame) -> None:
        for w in row.winfo_children():
            w.destroy()

    def _build_rarity_buttons(self, values: list[str]) -> None:
        self._clear_row(self.rarity_row)
        self.rarity_buttons.clear()
        for rarity in values:
            color = RARITY_COLORS.get(rarity, "#666666")
            btn = tk.Button(
                self.rarity_row,
                text=rarity.upper(),
                fg=color,
                bg=PANEL_BG,
                activebackground="#2a2a2a",
                activeforeground=color,
                highlightthickness=0,
                bd=1,
                width=12,
                command=lambda r=rarity: self.select_rarity(r),
            )
            btn.pack(side="left", padx=4, pady=2)
            self.rarity_buttons[rarity] = btn

    def _build_hat_buttons(self, values: list[str]) -> None:
        self._clear_row(self.hat_row)
        self.hat_buttons.clear()
        for hat in values:
            sym = HAT_SYMBOLS.get(hat, "?")
            btn = tk.Button(
                self.hat_row,
                text=f"{sym}\n{hat}",
                width=10,
                height=2,
                bg=PANEL_BG,
                fg=FG,
                activebackground="#2a2a2a",
                activeforeground=FG,
                highlightthickness=0,
                bd=1,
                command=lambda h=hat: self.select_hat(h),
            )
            btn.pack(side="left", padx=4, pady=2)
            self.hat_buttons[hat] = btn

    def _build_eye_buttons(self, values: list[str]) -> None:
        self._clear_row(self.eye_row)
        self.eye_buttons.clear()
        for eye in values:
            btn = tk.Button(
                self.eye_row,
                text=eye,
                width=8,
                bg=PANEL_BG,
                fg=FG,
                activebackground="#2a2a2a",
                activeforeground=FG,
                highlightthickness=0,
                bd=1,
                command=lambda e=eye: self.select_eye(e),
            )
            btn.pack(side="left", padx=4, pady=2)
            self.eye_buttons[eye] = btn

    def select_species(self, species: str) -> None:
        prev_rarity = self.rarity_var.get().strip()
        self.species_var.set(species)
        self._set_selected_button(self.species_buttons, species)
        try:
            self.current_records = load_species_records(species)
        except Exception as exc:
            messagebox.showerror(self.t("title_error"), f"{self.t('load_failed')}\n{exc}")
            return
        rarities = sorted({r["query"]["rarity"] for r in self.current_records}, key=rarity_rank, reverse=True)
        self._build_rarity_buttons(rarities)
        self.status_var.set(self.t("loaded", species=species, count=len(self.current_records)))
        if rarities:
            preferred = prev_rarity if prev_rarity in rarities else rarities[0]
            self.select_rarity(preferred)
        else:
            self._sync_selected_record()
            self._render_preview()

    def select_rarity(self, rarity: str) -> None:
        prev_hat = self.hat_var.get().strip()
        prev_eye = self.eye_var.get().strip()
        prev_shiny = self.shiny_var.get().strip()
        self.rarity_var.set(rarity)
        rarity_text_colors = {name: RARITY_COLORS.get(name, "#666666") for name in self.rarity_buttons}
        self._set_selected_button(self.rarity_buttons, rarity, text_colors=rarity_text_colors)
        hats = sorted({r["query"]["hat"] for r in self._filter_base(rarity=rarity)})
        if "none" in hats:
            hats = ["none"] + [h for h in hats if h != "none"]
        else:
            hats = ["none"] + hats
        self._build_hat_buttons(hats)
        chosen_hat = "none" if rarity == "common" else (prev_hat if prev_hat in hats else ("none" if "none" in hats else (hats[0] if hats else "")))
        if chosen_hat:
            self.select_hat(chosen_hat, preferred_eye=prev_eye, preferred_shiny=prev_shiny)
        else:
            self._sync_selected_record()
            self._render_preview()

    def select_hat(self, hat: str, preferred_eye: str | None = None, preferred_shiny: str | None = None) -> None:
        # Keep current selection when user clicks hat directly.
        if preferred_eye is None:
            preferred_eye = self.eye_var.get().strip() or None
        if preferred_shiny is None:
            preferred_shiny = self.shiny_var.get().strip() or None
        self.hat_var.set(hat)
        self._set_selected_button(self.hat_buttons, hat)
        eyes = sorted({r["query"]["eye"] for r in self._filter_base(rarity=self.rarity_var.get(), hat=hat)})
        self._build_eye_buttons(eyes)
        pick_eye = preferred_eye if preferred_eye and preferred_eye in eyes else (eyes[0] if eyes else "")
        if pick_eye:
            self.select_eye(pick_eye, preferred_shiny=preferred_shiny)
        else:
            self._sync_selected_record()
            self._render_preview()

    def select_eye(self, eye: str, preferred_shiny: str | None = None) -> None:
        self.eye_var.set(eye)
        self._set_selected_button(self.eye_buttons, eye)
        shiny_values = sorted(
            {str(r["query"]["shiny"]).lower() for r in self._filter_base(rarity=self.rarity_var.get(), hat=self.hat_var.get(), eye=eye)},
            key=lambda v: SHINY_ORDER.index(v),
            reverse=True,
        )
        if preferred_shiny and preferred_shiny in shiny_values:
            pick_shiny = preferred_shiny
        else:
            pick_shiny = "true" if "true" in shiny_values else (shiny_values[0] if shiny_values else "true")
        self.select_shiny(pick_shiny)

    def select_shiny(self, shiny: str) -> None:
        self.shiny_var.set(shiny)
        self._set_selected_button(self.shiny_buttons, shiny)
        self._sync_selected_record()
        self._render_preview()

    def _sync_selected_record(self) -> None:
        shiny_value = None
        if self.shiny_var.get().strip():
            shiny_value = self.shiny_var.get().strip() == "true"
        target = self._filter_base(
            rarity=self.rarity_var.get().strip() or None,
            hat=self.hat_var.get().strip() or None,
            eye=self.eye_var.get().strip() or None,
            shiny=shiny_value,
        )
        if not target:
            self.selected_record = None
            self.user_id_var.set(f"({self.t('not_matched')})")
            self.status_var.set(self.t("not_matched"))
            return
        self.selected_record = target[0]
        self.user_id_var.set(self.selected_record["match"]["userId"])
        self.status_var.set("")

    def _on_meta_change(self, *_args) -> None:
        self._render_preview()

    def _filter_base(self, rarity: str | None = None, hat: str | None = None, eye: str | None = None, shiny: bool | None = None) -> list[dict]:
        result = self.current_records
        if rarity:
            result = [r for r in result if r["query"]["rarity"] == rarity]
        if hat:
            result = [r for r in result if r["query"]["hat"] == hat]
        if eye:
            result = [r for r in result if r["query"]["eye"] == eye]
        if shiny is not None:
            result = [r for r in result if bool(r["query"]["shiny"]) == shiny]
        return result

    def copy_user_id(self) -> None:
        uid = self.user_id_var.get()
        if not uid or uid.startswith("("):
            messagebox.showwarning(self.t("title_warning"), self.t("no_userid"))
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(uid)
        self.status_var.set(self.t("copied"))

    def choose_config_path(self) -> None:
        picked = filedialog.askopenfilename(
            title=self.t("choose_config"),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if picked:
            self.config_path_var.set(picked)

    def apply_to_claude(self) -> None:
        if not self.selected_record:
            messagebox.showwarning(self.t("title_warning"), self.t("warn_select"))
            return
        uid = self.selected_record["match"]["userId"]
        config_path = Path(self.config_path_var.get().strip()).expanduser()
        if not config_path.exists():
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(uid)
                self.status_var.set(self.t("copied"))
            except Exception:
                pass
            messagebox.showwarning(self.t("title_warning"), self.t("path_help", path=config_path))
            return
        try:
            backup = write_claude_config(config_path, uid)
        except Exception as exc:
            messagebox.showerror(self.t("title_error"), f"{self.t('write_failed')}\n{exc}")
            return
        self.status_var.set(f"{self.t('complete')}: {config_path}")
        messagebox.showinfo(self.t("title_info"), self.t("apply_done", path=config_path, uid=uid, backup=backup))

    def _render_preview(self) -> None:
        species = self.species_var.get().strip() or "?"
        rarity = self.rarity_var.get().strip() or "?"
        hat = self.hat_var.get().strip() or "none"
        eye = self.eye_var.get().strip() or "@"
        shiny = self.shiny_var.get().strip()

        stats = {}
        if self.selected_record:
            stats = self.selected_record["match"]["bones"]["stats"]
        hat_symbol = HAT_SYMBOLS.get(hat, hat)
        art = render_species_art(species, eye, hat_symbol if hat != "none" else "none")
        width = 34

        rarity_color = RARITY_COLORS.get(rarity, "#ffcc33")
        self.preview.tag_config("rarity", foreground=rarity_color)

        def row(left: str = "", right: str = "") -> str:
            left_fitted = fit_display_width(left, width)
            if not right:
                return left_fitted
            right_fitted = fit_display_width(right, width)
            lw = display_width(left_fitted)
            rw = display_width(right_fitted)
            if lw + rw >= width:
                left_fitted = fit_display_width(left_fitted, max(0, width - rw - 1))
                lw = display_width(left_fitted)
            pad = max(1, width - lw - rw)
            return left_fitted + (" " * pad) + right_fitted

        stars = "★★★★★" if rarity == "legendary" else "★" * max(1, rarity_rank(rarity) + 1)
        segments: list[tuple[str, str]] = []
        segments.append((f"{stars} {rarity.upper()}     {species.upper()}", "rarity"))
        if shiny == "true":
            segments.append(("✨ SHINY ✨", "gold"))
        segments.append(("", "muted"))
        for art_line in art.splitlines():
            segments.append((fit_display_width("  " + art_line.rstrip(), width), "rarity"))
        segments.append(("", "muted"))
        if stats:
            for k in ["DEBUGGING", "PATIENCE", "CHAOS", "WISDOM", "SNARK"]:
                value = int(stats.get(k, 0))
                segments.append((f"{k:<10} {stat_bar(value)} {value:>3}", "stats"))
        else:
            segments.append((self.t("hint_pick"), "muted"))

        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        for idx, (line, tag) in enumerate(segments):
            suffix = "\n" if idx < len(segments) - 1 else ""
            self.preview.insert("end", line + suffix, tag)
        self.preview.configure(state="disabled")


def main() -> None:
    root = tk.Tk()
    try:
        App(root)
    except Exception as exc:
        messagebox.showerror("Startup failed", str(exc))
        root.destroy()
        return
    root.mainloop()


if __name__ == "__main__":
    main()
