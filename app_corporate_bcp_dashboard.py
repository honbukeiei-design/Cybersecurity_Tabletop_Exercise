import base64
import json
import os
import random
import time
from datetime import date
from typing import Dict, List, Optional, Set

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh


# ============================================================
# 医療機関サイバーBCP訓練
# Formal tabletop exercise / Feedback flow / Timeout game over
# ============================================================

st.set_page_config(
    page_title="医療機関サイバーBCP訓練",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;800&display=swap');

:root {
    --bg: #f3f6fa;
    --surface: #ffffff;
    --surface-soft: #f8fafd;
    --navy: #173B6C;
    --navy2: #365E95;
    --text: #1f2937;
    --muted: #5f6b7a;
    --line: #d7dee8;
    --line2: #e8edf4;
    --danger: #c62828;
    --warning: #f9a825;
    --success: #2e7d32;
    --info: #1769aa;
    --shadow: 0 10px 24px rgba(23, 59, 108, 0.08);
}

html, body, .stApp, [class*="css"], .stMarkdown, .stButton button,
[data-testid="stWidgetLabel"], [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    padding: 1.0rem 1.2rem 0.8rem 1.2rem !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] {
    width: 340px !important;
    background: #0f223d;
    border-right: 1px solid #0a1a30;
    box-shadow: 6px 0 20px rgba(15,34,61,0.16);
}

section[data-testid="stSidebar"] * {
    color: #eef4fb !important;
}

section[data-testid="stSidebar"] .stSelectbox div,
section[data-testid="stSidebar"] .stSlider div,
section[data-testid="stSidebar"] .stToggle div {
    color: #eef4fb !important;
}

section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] div,
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] span,
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] input {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
}
section[data-testid="stSidebar"] .stSelectbox svg {
    fill: #111827 !important;
}
section[data-testid="stSidebar"] .stTextInput input,
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Sidebar widget readability fixes */
section[data-testid="stSidebar"] [data-baseweb="select"],
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
section[data-testid="stSidebar"] [data-baseweb="popover"] *,
div[data-baseweb="popover"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
section[data-testid="stSidebar"] [role="combobox"] {
    background: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

h1 {
    color: var(--navy) !important;
    font-size: clamp(1.8rem, 3.2vw, 3.2rem) !important;
    line-height: 1.05 !important;
    margin: 0 !important;
    letter-spacing: 0.03em;
    text-align: center;
    font-weight: 800 !important;
}

h2, h3 {
    color: var(--navy) !important;
    margin: 0.35rem 0 !important;
    font-weight: 700 !important;
}

p, div, span {
    color: inherit;
}

hr {
    border: 0;
    border-top: 1px solid var(--line);
    margin: 0.6rem 0 !important;
}

.retro-panel {
    border: 1px solid rgba(215,222,232,0.34);
    background: rgba(255,255,255,0.06);
    box-shadow: none;
    padding: 0.8rem;
    margin-bottom: 0.85rem;
    border-radius: 10px;
}

.retro-panel-cyan {
    border: 1px solid var(--line);
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 1.0rem 1.1rem;
    margin-bottom: 0.9rem;
    border-radius: 12px;
}

.panel-title {
    color: #ffffff;
    font-size: 0.9rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.18);
    margin-bottom: 0.65rem;
    padding-bottom: 0.4rem;
}

.status-row {
    display: grid;
    grid-template-columns: 1fr 52px;
    gap: 8px;
    align-items: center;
    margin: 0.55rem 0;
}

.status-icon { display: none; }
.status-name {
    font-size: 0.92rem;
    font-weight: 600;
    color: #eaf2fb !important;
}
.status-value {
    text-align: right;
    font-size: 0.95rem;
    font-weight: 700;
    color: #ffffff !important;
}

.bar-bg {
    grid-column: 1 / 3;
    height: 8px;
    background: rgba(255,255,255,0.16);
    border: none;
    border-radius: 999px;
    overflow: hidden;
}
.bar-fill { height: 100%; border-radius: 999px; }

.timer-big {
    color: var(--danger);
    font-size: clamp(1.8rem, 3.2vw, 3.0rem);
    text-align: center;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: 0.04em;
}

.timebar {
    width: 100%;
    height: 12px;
    border: none;
    background: #e8edf4;
    margin: 0.55rem 0;
    border-radius: 999px;
    overflow: hidden;
}
.timebar-fill {
    height: 100%;
    background: var(--danger);
    transition: width 0.5s linear;
}

.sidebar-button {
    border: 1px solid rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.08);
    padding: 0.55rem;
    text-align: center;
    margin-top: 0.45rem;
    border-radius: 8px;
    font-size: 0.88rem;
}

.log-box {
    max-height: 170px;
    overflow: hidden;
    font-size: 0.82rem;
    line-height: 1.55;
}

.header-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 4px;
    align-items: center;
    margin-bottom: 0.8rem;
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 6px solid var(--navy);
    border-radius: 12px;
    box-shadow: var(--shadow);
    padding: 1.0rem 1.2rem;
}
.pixel-icon { display:none; }
.subtitle {
    text-align: center;
    color: var(--muted);
    font-size: clamp(0.86rem, 1.1vw, 1.05rem);
    margin-top: 0.25rem;
}
.compact-header h1 { font-size: clamp(1.35rem, 2.3vw, 2.2rem) !important; }
.compact-header .subtitle { font-size: 0.82rem !important; }
.compact-header { margin-bottom: 0.4rem; }

.phase-box {
    display: grid;
    grid-template-columns: 1.5fr 0.65fr;
    gap: 14px;
}
.phase-title {
    color: var(--navy);
    font-size: clamp(1.15rem, 1.6vw, 1.45rem);
    font-weight: 800;
    border-left: 5px solid var(--navy);
    padding-left: 0.7rem;
}
.phase-text {
    color: var(--text);
    font-size: clamp(0.9rem, 1.05vw, 1.0rem);
    line-height: 1.65;
    margin-top: 0.45rem;
}

.event-box {
    border: 1px solid #efc5c5;
    border-left: 6px solid var(--danger);
    background: #fff7f7;
    box-shadow: var(--shadow);
    padding: 1.0rem 1.2rem;
    min-height: auto;
    max-height: none;
    overflow: visible;
    margin: 0.8rem 0;
    display: block;
    border-radius: 12px;
}
.event-phone, .event-virus { display: none; }
.event-main { text-align: left; }
.event-label {
    color: var(--danger);
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.08em;
}
.event-title {
    color: #8f1717;
    font-size: clamp(1.1rem, 1.75vw, 1.55rem);
    line-height: 1.35;
    font-weight: 800;
    margin-top: 0.2rem;
}
.event-desc {
    color: var(--text);
    font-size: clamp(0.88rem, 1.02vw, 1.0rem);
    line-height: 1.7;
    margin-top: 0.6rem;
}

.mini-event {
    border: 1px solid #efc5c5;
    border-left: 5px solid var(--danger);
    background: #fff7f7;
    padding: 0.75rem 1rem;
    margin: 0.55rem 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-radius: 10px;
}

.feedback-best, .feedback-good {
    border: 1px solid #bbd7bd;
    border-left: 6px solid var(--success);
    background: #f5fbf6;
    box-shadow: var(--shadow);
    padding: 1.1rem 1.25rem;
    margin: 0.7rem 0;
    text-align: left;
    border-radius: 12px;
}
.feedback-better {
    border: 1px solid #efd99b;
    border-left: 6px solid var(--warning);
    background: #fffaf0;
    box-shadow: var(--shadow);
    padding: 1.1rem 1.25rem;
    margin: 0.7rem 0;
    text-align: left;
    border-radius: 12px;
}
.feedback-bad {
    border: 1px solid #efc5c5;
    border-left: 6px solid var(--danger);
    background: #fff7f7;
    box-shadow: var(--shadow);
    padding: 1.1rem 1.25rem;
    margin: 0.7rem 0;
    text-align: left;
    border-radius: 12px;
}
.feedback-title {
    font-size: clamp(1.2rem, 1.8vw, 1.55rem);
    font-weight: 800;
}
.feedback-text {
    color: var(--text);
    font-size: clamp(0.92rem, 1.06vw, 1.05rem);
    line-height: 1.75;
    margin-top: 0.7rem;
}

.stButton > button {
    border: 1px solid #12315c !important;
    background: var(--navy) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    min-height: 78px;
    width: 100%;
    white-space: normal;
    font-size: clamp(0.85rem, 1vw, 0.98rem);
    font-weight: 700;
    box-shadow: 0 4px 10px rgba(23,59,108,0.12);
}
.stButton > button:hover {
    background: var(--navy2) !important;
    color: #ffffff !important;
    border-color: var(--navy2) !important;
}

.footer-note {
    border: 1px solid var(--line);
    background: var(--surface-soft);
    color: var(--muted);
    text-align: center;
    padding: 0.55rem;
    margin-top: 0.8rem;
    border-radius: 8px;
}

.training-purpose {
    border: 1px solid var(--line);
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 1rem 1.2rem;
    margin: 0.55rem 0 0.9rem 0;
    border-radius: 12px;
}
.training-purpose-title {
    color: var(--navy);
    font-size: clamp(1rem, 1.4vw, 1.25rem);
    font-weight: 800;
    margin-bottom: 0.45rem;
}
.training-purpose-text {
    color: var(--text);
    font-size: clamp(0.88rem, 1.02vw, 1rem);
    line-height: 1.7;
}
.review-box {
    border: 1px solid var(--line);
    background: var(--surface);
    box-shadow: var(--shadow);
    padding: 1rem 1.2rem;
    margin: 0.75rem 0;
    border-radius: 12px;
}
.review-question {
    color: var(--text);
    font-size: clamp(0.88rem, 1.02vw, 1rem);
    line-height: 1.65;
    margin: 0.35rem 0;
}

[data-testid="stProgress"] > div > div > div > div {
    background-color: var(--navy) !important;
}

@media (max-width: 900px) {
    section[data-testid="stSidebar"] { width: auto !important; }
    .phase-box { grid-template-columns: 1fr; }
    .stButton > button { min-height: 66px; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# Data
# ============================================================

DIFFICULTIES = {
    # event は突発イベントの発生間隔。Noneの場合は発生しない。
    "EASY": {"limit": 55, "event": None, "infection": 10, "panic": 10, "bcp": 100, "trust": 100},
    "NORMAL": {"limit": 45, "event": 22, "infection": 20, "panic": 15, "bcp": 95, "trust": 95},
    "HARD": {"limit": 32, "event": 12, "infection": 35, "panic": 25, "bcp": 85, "trust": 85},
    "NIGHTMARE": {"limit": 24, "event": 6, "infection": 48, "panic": 35, "bcp": 78, "trust": 78},
}

ROLES = ["管理監督者", "SE", "職員"]


# ============================================================
# Team shared simulation settings
# ============================================================
# Streamlit session_state は利用者ごとに独立するため、共有プレイ時は
# チームごとの状態を JSON ファイルへ保存し、別ブラウザから同じチームを選ぶと
# 同じ進行状況を読み込めるようにします。
COLLAB_TEAMS = [f"{i}チーム" for i in range(1, 11)]
COLLAB_STATE_DIR = os.environ.get(
    "MEDICAL_BCP_STATE_DIR",
    os.path.join(os.getcwd(), ".medical_cyber_bcp_state"),
)
SHARED_PHASE_BONUS_SECONDS = 5 * 60

# ============================================================
# Event background image assets
# ============================================================
# GitHub等へ配置する場合は、以下の構成を想定しています。
# app_corporate_bcp_dashboard_v9_jp_revised_with_images.py
# assets/events/event_01_ransomware.png など
EVENT_IMAGE_DIR = os.environ.get(
    "MEDICAL_BCP_EVENT_IMAGE_DIR",
    os.path.join(os.getcwd(), "assets", "events"),
)

EVENT_IMAGE_MAP = {
    # プログラム内の突発イベント
    "bereal": "event_01_ransomware.png",
    "chat_down": "event_03_network_down.png",

    # 選択結果により誘発される突発イベント
    "induced_misinformation": "event_10_crowded_reception.png",
    "induced_reinfection": "event_06_server_down.png",
    "induced_privacy": "event_01_ransomware.png",
}


def event_image_path(event_obj: Optional[dict]) -> Optional[str]:
    """現在の突発イベントに対応する背景画像パスを返す。

    画像が存在しない場合は None を返し、従来の緊急時背景にフォールバックする。
    """
    if not event_obj:
        return None
    filename = EVENT_IMAGE_MAP.get(event_obj.get("id"))
    if not filename:
        return None
    path = os.path.join(EVENT_IMAGE_DIR, filename)
    return path if os.path.exists(path) else None


def image_file_to_data_uri(path: str) -> str:
    """Streamlit Cloud等でも表示しやすいよう、PNGをdata URIへ変換する。"""
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

COLLAB_EXCLUDE_KEYS = {
    "bgm_volume", "se_volume", "bgm_enabled", "se_enabled", "last_se_key", "_choice_processing",
    "_queued_choice", "_skip_shared_sync_once", "_queued_se",
    "collab_mode_input", "collab_team_input",
    "manual_shared_refresh_sidebar", "manual_shared_refresh_main",
}


def is_transient_widget_key(key) -> bool:
    key = str(key)
    return (
        key in COLLAB_EXCLUDE_KEYS
        or key.startswith("FormSubmitter:")
        or key.startswith("choice_")
        or key.startswith("manual_shared_refresh_")
    )


def _json_default(value):
    if isinstance(value, set):
        return {"__type__": "set", "value": list(value)}
    if isinstance(value, date):
        return {"__type__": "date", "value": value.isoformat()}
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def _json_object_hook(obj):
    if obj.get("__type__") == "set":
        return set(obj.get("value", []))
    if obj.get("__type__") == "date":
        return date.fromisoformat(obj["value"])
    return obj


def shared_play_enabled() -> bool:
    return st.session_state.get("collab_mode") == "チームで共有プレイ" and bool(st.session_state.get("collab_team"))


def shared_sync_enabled() -> bool:
    return shared_play_enabled() and bool(st.session_state.get("simulation_started", False))


def shared_state_path(team=None) -> str:
    team = team or st.session_state.get("collab_team", "")
    safe_team = "".join(ch for ch in str(team) if ch.isalnum() or ch in ["_", "-", "チ", "ー", "ム"])
    safe_team = safe_team or "team"
    os.makedirs(COLLAB_STATE_DIR, exist_ok=True)
    return os.path.join(COLLAB_STATE_DIR, f"{safe_team}.json")


def shared_state_exists(team: str) -> bool:
    return os.path.exists(shared_state_path(team))


def export_shared_state() -> dict:
    data = {}
    for key, value in st.session_state.items():
        if is_transient_widget_key(key):
            continue
        try:
            json.dumps(value, ensure_ascii=False, default=_json_default)
        except TypeError:
            continue
        data[key] = value
    data["_shared_saved_at"] = time.time()
    return data


def import_shared_state(data: dict, keep_identity: bool = True):
    current_mode = st.session_state.get("collab_mode")
    current_team = st.session_state.get("collab_team")
    current_bgm = st.session_state.get("bgm_volume", 35)
    current_se = st.session_state.get("se_volume", 70)
    current_bgm_enabled = st.session_state.get("bgm_enabled", True)
    current_se_enabled = st.session_state.get("se_enabled", True)
    current_queued_choice = st.session_state.get("_queued_choice")
    current_choice_processing = st.session_state.get("_choice_processing", False)
    current_queued_se = st.session_state.get("_queued_se")
    for key in list(st.session_state.keys()):
        if key not in ["collab_mode", "collab_team", "collab_mode_input", "collab_team_input", "bgm_volume", "se_volume", "bgm_enabled", "se_enabled", "_queued_choice", "_choice_processing", "_queued_se"]:
            del st.session_state[key]
    for key, value in data.items():
        if key == "_shared_saved_at" or is_transient_widget_key(key):
            continue
        st.session_state[key] = value
    if keep_identity:
        st.session_state["collab_mode"] = current_mode
        st.session_state["collab_team"] = current_team
    st.session_state["bgm_volume"] = current_bgm
    st.session_state["se_volume"] = current_se
    st.session_state["bgm_enabled"] = current_bgm_enabled
    st.session_state["se_enabled"] = current_se_enabled
    if current_queued_choice is not None:
        st.session_state["_queued_choice"] = current_queued_choice
    if current_choice_processing:
        st.session_state["_choice_processing"] = current_choice_processing
    if current_queued_se is not None:
        st.session_state["_queued_se"] = current_queued_se
    st.session_state["_shared_loaded_at"] = float(data.get("_shared_saved_at", time.time()))
    ensure_state_integrity()


def normalize_loaded_feedback_keys(obj):
    """JSON共有後に bool キーが文字列化されてもフィードバック参照できるよう補正する。"""
    if not isinstance(obj, dict):
        return obj
    fb = obj.get("feedback")
    if isinstance(fb, dict):
        fixed = {}
        for k, v in fb.items():
            if k is True or str(k).lower() == "true":
                fixed[True] = v
            elif k is False or str(k).lower() == "false":
                fixed[False] = v
            else:
                fixed[k] = v
        obj["feedback"] = fixed
    return obj


def ensure_state_integrity():
    """共有同期・旧版JSON読込後の欠損キーや型ズレを補正し、一瞬の AttributeError を防ぐ。"""
    if st.session_state.get("difficulty") not in DIFFICULTIES:
        st.session_state["difficulty"] = "NORMAL"
    if st.session_state.get("role") not in ROLES:
        st.session_state["role"] = "職員"
    if st.session_state.get("collab_mode") not in ["個別プレイ", "チームで共有プレイ"]:
        st.session_state["collab_mode"] = "個別プレイ"
    if st.session_state.get("collab_team") not in COLLAB_TEAMS:
        st.session_state["collab_team"] = COLLAB_TEAMS[0]

    defaults = DIFFICULTIES[st.session_state.get("difficulty", "NORMAL")]
    scalar_defaults = {
        "simulation_started": False,
        "completed": False,
        "game_over": False,
        "pending_feedback": None,
        "pending_induced_event": None,
        "phase": 0,
        "infection": defaults["infection"],
        "panic": defaults["panic"],
        "bcp": defaults["bcp"],
        "trust": defaults["trust"],
        "started_at": time.time(),
        "phase_started_at": time.time(),
        "last_event_at": time.time(),
        "current_event": None,
        "event_expanded": False,
        "bgm_volume": 35,
        "se_volume": 70,
        "bgm_enabled": True,
        "se_enabled": True,
        "last_se_key": None,
        "_choice_processing": False,
    }
    for key, value in scalar_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if not isinstance(st.session_state.get("history"), list):
        st.session_state["history"] = []
    if not isinstance(st.session_state.get("log"), list):
        st.session_state["log"] = ["[SYSTEM] セットアップ待機"]
    if not isinstance(st.session_state.get("choice_orders"), dict):
        st.session_state["choice_orders"] = {}

    for set_key in ["seen_event_ids", "seen_induced_event_ids"]:
        value = st.session_state.get(set_key, set())
        if isinstance(value, list):
            st.session_state[set_key] = set(value)
        elif not isinstance(value, set):
            st.session_state[set_key] = set()

    try:
        st.session_state["phase"] = max(0, min(int(st.session_state.get("phase", 0)), len(PHASES) - 1))
    except Exception:
        st.session_state["phase"] = 0

    if st.session_state.get("current_event") is not None:
        st.session_state["current_event"] = normalize_loaded_feedback_keys(st.session_state.get("current_event"))
    if st.session_state.get("pending_induced_event") is not None:
        st.session_state["pending_induced_event"] = normalize_loaded_feedback_keys(st.session_state.get("pending_induced_event"))


def load_shared_state(team=None):
    path = shared_state_path(team)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f, object_hook=_json_object_hook)
    except Exception as exc:
        try:
            st.session_state.setdefault("log", []).append(f"[WARN] 共有状態読込失敗: {exc}")
        except Exception:
            pass
        return None


def save_shared_state():
    if not shared_play_enabled():
        return
    path = shared_state_path()
    tmp_path = path + ".tmp"
    data = export_shared_state()
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=_json_default)
        os.replace(tmp_path, path)
        st.session_state["_shared_loaded_at"] = data["_shared_saved_at"]
    except Exception as exc:
        try:
            st.session_state.setdefault("log", []).append(f"[WARN] 共有状態保存失敗: {exc}")
        except Exception:
            pass


def sync_shared_state_from_file(force: bool = False):
    # 共有同期は、フィードバック画面表示中でも止めない。
    # A端末が「次のフェーズへ」「突発イベント対応完了」を押した際に、
    # B端末がフィードバック画面のままだと同期されない問題を防ぐ。
    if st.session_state.get("_choice_processing", False):
        return
    if not shared_sync_enabled():
        return
    data = load_shared_state()
    if not data:
        return
    saved_at = float(data.get("_shared_saved_at", 0))
    loaded_at = float(st.session_state.get("_shared_loaded_at", 0))
    if force or saved_at > loaded_at:
        import_shared_state(data, keep_identity=True)


def set_shared_query_params():
    if not shared_play_enabled():
        return
    try:
        st.query_params["collab"] = "1"
        st.query_params["team"] = st.session_state.get("collab_team", "")
    except Exception:
        pass


def clear_shared_query_params():
    try:
        if "collab" in st.query_params:
            del st.query_params["collab"]
        if "team" in st.query_params:
            del st.query_params["team"]
    except Exception:
        pass


def restore_shared_state_from_query():
    try:
        if st.query_params.get("collab") != "1":
            return
        team = st.query_params.get("team", "")
    except Exception:
        return
    if team not in COLLAB_TEAMS:
        return
    if st.session_state.get("simulation_started"):
        return
    data = load_shared_state(team)
    st.session_state["collab_mode"] = "チームで共有プレイ"
    st.session_state["collab_team"] = team
    if data and data.get("simulation_started"):
        import_shared_state(data, keep_identity=True)


def manual_refresh_shared_state_button(location="main"):
    # 自動同期へ変更したため、UIボタンは表示しない。
    return


def team_status_label(team: str) -> str:
    data = load_shared_state(team) if shared_state_exists(team) else None
    if data and data.get("simulation_started") and not data.get("completed") and not data.get("game_over"):
        phase_no = int(data.get("phase", 0)) + 1
        return f"{team}（進行中：PHASE {phase_no:02d}）"
    return f"{team}（空き）"


def render_shared_status():
    if st.session_state.get("simulation_started", False):
        return
    if shared_play_enabled():
        bonus = SHARED_PHASE_BONUS_SECONDS // 60
        st.success(f"共有プレイ中：{st.session_state.get('collab_team')}。同じチームを選んだ端末で進行状況を共有します。共有プレイ時は1フェーズあたり+{bonus}分です。")


def current_phase_limit() -> int:
    limit = DIFFICULTIES[st.session_state.get("difficulty", "NORMAL")]["limit"]
    if shared_play_enabled():
        limit += SHARED_PHASE_BONUS_SECONDS
    return limit


# 職員ロールは初動・紙運用・患者対応を重点化
ROLE_PHASE_MAP = {
    "管理監督者": [0,1,2,3,4,6,7,8,9],
    "SE": [0,1,2,3,5,6,7,8,9],
    "職員": [0,0,3,3,4,4,5,5,6],
}

ROLE_EVENT_TARGET = {
    "管理監督者": 15,
    "SE": 15,
    "職員": 15,
}



GUIDELINE_VIEWPOINTS = {
    "PHASE 01：発報": "システム運用編：異常検知時の初動、証跡保全、感染拡大防止。企画管理編：インシデント発生時の連絡・報告手順。",
    "PHASE 02：指揮所設置": "経営管理編：安全管理責任、組織的管理、意思決定体制。企画管理編：運用管理規程・体制整備。",
    "PHASE 03：外部連携": "経営管理編：委託先・関係機関との責任分界。企画管理編：連絡体制、外部委託先管理、報告記録。",
    "PHASE 04：紙運用への切替": "企画管理編：非常時運用・代替運用手順。システム運用編：可用性確保、業務継続、誤入力・誤認防止。",
    "PHASE 05：院内混乱と情報統制": "経営管理編：教育・周知、情報取扱い責任。企画管理編：職員教育、SNS・情報持出し対策。",
    "PHASE 06：バックアップ判断": "システム運用編：バックアップ、復旧、マルウェア対策、アクセス制御、ログ管理。",
    "PHASE 07：医療トリアージ": "経営管理編：医療安全と事業継続の判断。企画管理編：BCP、優先業務、代替手順。",
    "PHASE 08：情報漏えい疑惑": "経営管理編：説明責任、個人情報保護、事故対応。システム運用編：ログ確認、証跡保全、漏えい調査。",
    "PHASE 09：広報・患者説明": "経営管理編：患者・社会への説明責任。企画管理編：インシデント時の広報・問い合わせ対応。",
    "PHASE 10：復旧・再発防止": "経営管理編：継続的改善、監査、再発防止。企画管理編・システム運用編：復旧手順、教育、技術対策の見直し。",
    "職員がSNSに院内の乗っ取り画面を投稿！": "経営管理編・企画管理編：職員教育、情報持出し、SNS利用、個人情報保護。システム運用編：画面・端末・ログの証跡確認。",
    "院内チャット停止": "企画管理編：非常時連絡手段、代替運用、記録管理。システム運用編：コミュニケーション基盤の可用性。",
}


def guideline_viewpoint_for(title: str) -> str:
    return GUIDELINE_VIEWPOINTS.get(
        title,
        "医療情報システム安全管理ガイドライン第6.0版の観点：安全管理責任、運用管理規程、アクセス制御、ログ管理、BCP、教育・周知。"
    )


def feedback_text_for(obj: dict, good: bool) -> str:
    """boolキー/JSON文字列化キーの両方に対応したフィードバック取得。"""
    fb = obj.get("feedback", {}) if isinstance(obj, dict) else {}
    if not isinstance(fb, dict):
        return str(fb) if fb else "判断結果を記録しました。"
    candidates = [good, str(good), str(good).lower(), str(good).upper()]
    for key in candidates:
        if key in fb:
            return fb[key]
    # 品質ラベル形式のフィードバックが将来混在しても落ちないようにする
    if good:
        for key in ["BEST", "BETTER", "GOOD", "true", "True"]:
            if key in fb:
                return fb[key]
    else:
        for key in ["BAD", "NG", "false", "False"]:
            if key in fb:
                return fb[key]
    return "判断結果を記録しました。"



PHASES = [
    {
        "title": "PHASE 01：発報",
        "scene": "外来対応中、医事課端末にランサムウェアによる身代金要求画面が表示された。",
        "objective": "初動対応により感染拡大と院内混乱を防止する。",
        "icon": "🚨",
        "feedback": {
            True: "初動として適切です。感染端末への不用意な操作を避け、指揮系統と報告経路を確保できました。",
            False: "初動対応として不適切です。再起動や様子見は証跡消失・感染拡大・報告遅延につながります。",
        },
        "choices": {
            "管理監督者": [
                ("対策本部を即時招集し、PC操作停止と状況報告を全職員へ指示する", True),
                ("医療安全・情報担当・事務部門から初動班を編成する", True),
                ("現場混乱を避けるため『通常の不具合』として様子を見る", False),
                ("診療制限の可能性を部門長へ伝え、待機を指示する", True),
                ("原因が判明するまで通常診療継続を指示する", False),
                ("患者説明は広報・対策本部に一本化するよう指示する", True),
            ],
            "SE": [
                ("感染端末をネットワークから隔離し、証跡を保全する", True),
                ("基幹ネットワークの遮断範囲を判断し、電子カルテ系を切り離す", True),
                ("まず感染端末を再起動して復旧を試す", False),
                ("EDR・認証ログで感染拡大の兆候を確認する", True),
                ("原因調査を優先し、遮断は後回しにする", False),
                ("サーバー・端末・バックアップの状態を対策本部へ報告する", True),
            ],
            "職員": [
                ("端末を操作せず、上長と情報担当へ即時報告する", True),
                ("画面写真を撮り、端末を操作しないよう周囲へ伝える", True),
                ("再起動すれば直ると思い、端末を再起動する", False),
                ("近くの別PCで同じ業務を続ける", False),
                ("患者には『確認中です』と説明し、推測で話さない", True),
                ("同僚へ状況を共有し、同じ症状がないか確認する", True),
            ],
        },
    },
    {
        "title": "PHASE 02：指揮所設置",
        "scene": "院内からの問い合わせが急増し、指揮命令系統が不明確になっている。",
        "objective": "指揮命令系統を明確にする。",
        "icon": "🏥",
        "feedback": {
            True: "指揮系統を明確化できています。記録係・判断者・広報窓口を置くことで混乱を抑えられます。",
            False: "危険です。部門任せや報告省略は、判断の乱立・責任不明確・現場混乱を招きます。",
        },
        "choices": {
            "管理監督者": [
                ("院長・事務部長・医療安全・情報担当で対策本部を設置する", True),
                ("判断者、記録係、広報窓口、現場連絡係を明確にする", True),
                ("各部門に個別判断での対応を任せる", False),
                ("15分ごとの状況報告体制を整備する", True),
                ("情報担当だけに対応を任せ、経営層報告は後回しにする", False),
                ("院内放送で対策本部の指示に従うよう周知する", True),
            ],
            "SE": [
                ("被害範囲、遮断状況、復旧見込みを短く定時報告する", True),
                ("技術対応の優先順位を対策本部へ提案する", True),
                ("SEだけで復旧作業を進め、意思決定者への報告を省く", False),
                ("管理者権限の利用状況を確認する", True),
                ("現場からの個別依頼をすべて優先して対応する", False),
                ("ネットワーク遮断の影響を部門別に整理する", True),
            ],
            "職員": [
                ("所属長の指示系統を確認し、勝手な判断を避ける", True),
                ("患者からの質問は定型文で対応し、不明点は上長へ回す", True),
                ("患者へ『サイバー攻撃です』と独自説明する", False),
                ("紙運用に備えて必要物品を確認する", True),
                ("SNSや私用チャットで状況を共有する", False),
                ("同じ問い合わせは記録し、対策本部へ集約する", True),
            ],
        },
    },
]

# PHASE 03-10 はテーマ別に自動構成。ただし選択肢はテーマに一致する内容にする。
PHASE_TEMPLATES = [
    ("PHASE 03：外部連携", "ベンダー、警察、監督官庁、自治体、近隣医療機関への連絡判断が必要。", "支援ラインと報告ラインを確立する。", "📞",
     "外部連携として適切です。支援要請と記録化により、技術・法務・地域医療の支援を受けやすくなります。",
     "外部連携として不適切です。報告保留や個人判断の連絡は、支援遅延や説明責任上の問題につながります。"),
    ("PHASE 04：紙運用への切替", "電子カルテ停止が長期化し、受付・診察・検査・薬剤・会計の紙運用が必要。", "医療安全を守りながら業務継続へ移行する。", "📄",
     "紙運用への移行として適切です。様式統一、本人確認、ダブルチェックが医療安全を支えます。",
     "紙運用として危険です。記録後回しや独自様式は、転記ミス・処方ミス・患者誤認につながります。"),
    ("PHASE 05：院内混乱と情報統制", "患者・職員・外部からの問い合わせが増え、未確認情報が拡散し始めている。", "現場混乱と不正確な情報発信を抑える。", "📣",
     "情報統制として適切です。定型文、窓口一本化、SNS注意喚起により、誤情報と不安の拡大を抑えられます。",
     "情報管理上、不適切な対応です。推測発言や個人投稿は、誤情報・炎上・信用低下につながります。"),
    ("PHASE 06：バックアップ判断", "バックアップサーバーは稼働しているように見えるが、安全確認は未完了。", "二次感染を防ぎながら復旧経路を確保する。", "💾",
     "バックアップ対応として適切です。隔離検証と復旧点確認により、二次感染を避けながら復旧できます。",
     "バックアップ対応として危険です。未確認の接続や証跡破壊は、バックアップ暗号化や原因不明化につながります。"),
    ("PHASE 07：医療トリアージ", "予定手術、透析、救急、入院患者の検査結果確認が競合している。", "限られた情報で医療安全を最大化する。", "🚑",
     "医療トリアージとして適切です。受入基準と優先順位を明確にすることで医療安全を守れます。",
     "医療トリアージとして危険です。通常診療維持や独自判断は、確認漏れや重大インシデントにつながります。"),
    ("PHASE 08：情報漏えい疑惑", "攻撃者の脅迫文に『患者情報を取得した』と記載がある。", "個人情報・広報・法務の初動を誤らない。", "🔐",
     "漏えい疑惑対応として適切です。断定せず、証跡保全・事実確認・相談準備を進める姿勢が重要です。",
     "漏えい疑惑対応として危険です。根拠なき断言やログ削除は、信用失墜と説明不能につながります。"),
    ("PHASE 09：広報・患者説明", "報道機関や患者家族から問い合わせが急増している。", "事実、未確定事項、診療制限を正確に伝える。", "🎤",
     "広報対応として適切です。事実と未確定事項を分け、説明窓口を統一することで信頼を維持できます。",
     "広報対応として危険です。過小表現や逃げの姿勢は、炎上・不信・二次被害につながります。"),
    ("PHASE 10：復旧・再発防止", "診療は段階再開。監査ログと改善計画が求められている。", "訓練ログを再発防止策へつなげる。", "🏁",
     "再発防止として適切です。時系列、判断根拠、改善策、次回訓練へつなげることで組織学習になります。",
     "再発防止の観点で課題があります。振り返り省略や責任追及偏重では、次のインシデントに備えられません。"),
]

ROLE_PHASE_CHOICES = {
    "外部連携": {
        "管理監督者": [
            ("ベンダー・警察・監督官庁へ第1報を入れる", True),
            ("地域医療連携へ救急分散や検査代替の相談をする", True),
            ("復旧見込みが出るまで外部報告を保留する", False),
            ("法務・個人情報保護・広報の担当を同時に動かす", True),
            ("問い合わせ対応を各部署に任せる", False),
            ("外部連絡の時刻・内容・担当者を記録する", True),
        ],
        "SE": [
            ("ベンダーへログ、影響範囲、遮断状況を整理して共有する", True),
            ("遠隔接続を許可する前に安全な接続方法を確認する", True),
            ("攻撃者の連絡先へアクセスして復旧可能性を探る", False),
            ("外部支援者に渡す情報を最小限かつ正確に整理する", True),
            ("原因が不明なまま全サーバーを再起動する", False),
            ("証跡保全の方針をベンダーと確認する", True),
        ],
        "職員": [
            ("外部からの問い合わせは広報・対策本部へ一本化する", True),
            ("患者へ代替窓口や待機場所を案内する", True),
            ("知り合いの業者へ個人的に相談する", False),
            ("近隣機関からの連絡内容を記録して上長へ渡す", True),
            ("報道機関に現場感覚で答える", False),
            ("院外へ持ち出す資料がないか確認する", True),
        ],
    },
    "紙運用への切替": {
        "管理監督者": [
            ("紙カルテ・紙処方・紙検査依頼への切替を正式に宣言する", True),
            ("救急・透析・入院患者を優先し、新規外来を制限する", True),
            ("通常どおり全患者を受け入れるよう指示する", False),
            ("受付・診療科・薬剤部の紙運用様式を統一する", True),
            ("部門ごとの独自様式で任せる", False),
            ("患者説明係と誘導係を配置する", True),
        ],
        "SE": [
            ("使用可能端末と使用禁止端末を明確にリスト化する", True),
            ("紙運用中に必要な参照データの安全な取り出し方法を確認する", True),
            ("安全確認前の端末を一時接続して印刷を行う", False),
            ("部門システムごとの停止・稼働状況を掲示用に整理する", True),
            ("復旧を急ぎ、遮断したネットワークを一部戻す", False),
            ("紙運用に必要なプリンタや帳票の利用可否を確認する", True),
        ],
        "職員": [
            ("紙様式に患者ID、氏名、生年月日を必ず記載する", True),
            ("薬剤・アレルギー・禁忌はダブルチェックする", True),
            ("忙しいため記録は後でまとめて書く", False),
            ("検査依頼・処方・会計の控えを所定場所に保管する", True),
            ("自分のメモ帳に患者情報を自由形式で記録する", False),
            ("患者誘導時は診療制限の案内文に沿って説明する", True),
        ],
    },
}

# 残りテーマは汎用選択肢を使いつつ、タイトルに応じたフィードバックで整合させる。
GENERIC_GOOD_BAD = {
    "管理監督者": [
        ("対策本部で優先順位を決定し、全館へ統一指示を出す", True),
        ("患者・職員向けの説明窓口を一本化する", True),
        ("現場裁量を広く認め、各部門に任せる", False),
        ("関係部署の担当者・判断者・記録係を明確にする", True),
        ("問題を小さく見せるため情報共有を制限する", False),
        ("判断内容と根拠を時系列で記録する", True),
    ],
    "SE": [
        ("影響範囲を切り分け、復旧対象を安全な順序に並べる", True),
        ("確認済み事実と未確認事項を分けて対策本部へ報告する", True),
        ("早期復旧を優先し、未確認端末も暫定接続する", False),
        ("証跡保全・ログ確認・認証情報見直しを行う", True),
        ("原因調査前に関係ログを削除する", False),
        ("医療側の優先業務に合わせて技術対応を調整する", True),
    ],
    "職員": [
        ("定型文に沿って患者説明を行い、推測では答えない", True),
        ("記録を残し、後で検証できる状態にする", True),
        ("忙しいため確認や記録を省略する", False),
        ("不明点は独自判断せず、上長へエスカレーションする", True),
        ("未確認情報を同僚や患者へ共有する", False),
        ("患者本人確認とダブルチェックを徹底する", True),
    ],
}

# テンプレートからPHASE 03-10を構成
for title, scene, objective, icon, good_fb, bad_fb in PHASE_TEMPLATES:
    key = title.split("：", 1)[1]
    if key in ROLE_PHASE_CHOICES:
        choices = ROLE_PHASE_CHOICES[key]
    else:
        choices = GENERIC_GOOD_BAD
    PHASES.append({
        "title": title,
        "scene": scene,
        "objective": objective,
        "icon": icon,
        "feedback": {True: good_fb, False: bad_fb},
        "choices": choices,
    })


PHASE_CHOICE_OVERRIDES = {
    "PHASE 05：院内混乱と情報統制": {
        "管理監督者": [
            ("院内向けに統一メッセージと問い合わせ窓口を示す", "BEST"),
            ("職員のSNS投稿禁止と情報取扱い注意を周知する", "BEST"),
            ("患者向け説明文を作成し、受付・外来で同じ説明にする", "BETTER"),
            ("現場の判断で自由に説明するよう任せる", "BAD"),
            ("混乱を避けるため、何も公表しないよう指示する", "BAD"),
            ("広報・医療安全・個人情報担当で想定問答を作る", "BETTER"),
        ],
        "SE": [
            ("院内へ技術状況を簡潔に共有し、操作禁止事項を明示する", "BEST"),
            ("影響範囲図を更新し、対策本部と共有する", "BETTER"),
            ("復旧見込みを不確実性込みで対策本部へ報告する", "BEST"),
            ("安心させるため根拠なく『すぐ復旧する』と伝える", "BAD"),
            ("現場の要望に応じて例外的に端末をつなぐ", "BAD"),
            ("問い合わせの多い技術質問をFAQ化する", "BETTER"),
        ],
        "職員": [
            ("患者には定型文で説明し、推測や私見を言わない", "BEST"),
            ("問い合わせ内容を記録し、繰り返し質問を上長へ共有する", "BEST"),
            ("不安が強い患者を上長や相談窓口へつなぐ", "BETTER"),
            ("患者に聞かれたのでSNSで見た情報も含めて説明する", "BAD"),
            ("不満を個人SNSに投稿する", "BAD"),
            ("院内掲示や最新指示を確認してから回答する", "BETTER"),
        ],
    },
    "PHASE 06：バックアップ判断": {
        "管理監督者": [
            ("安全確認完了までバックアップ接続を許可しない", "BEST"),
            ("復旧判断会議を設け、承認条件を明確にする", "BEST"),
            ("復旧優先順位を診療継続上重要なシステムから決める", "BETTER"),
            ("早期復旧のため未確認バックアップをすぐ戻す", "BAD"),
            ("復旧作業はベンダー任せで院内判断を省く", "BAD"),
            ("復旧遅延時の診療制限継続方針を決める", "BETTER"),
        ],
        "SE": [
            ("バックアップを本番環境から隔離した検証環境で確認する", "BEST"),
            ("バックアップ世代を比較し、感染前の復旧点を探す", "BEST"),
            ("復旧前に認証情報と管理者権限を見直す", "BETTER"),
            ("暗号化されていない領域を本番へ即時書き戻す", "BAD"),
            ("証跡保全前にサーバーを初期化する", "BAD"),
            ("オフライン保管バックアップの有無を確認する", "BETTER"),
        ],
        "職員": [
            ("復旧まで紙運用を継続し、電子入力の再開指示を待つ", "BEST"),
            ("紙記録を後で入力できるよう整理して保管する", "BEST"),
            ("復旧後の二重入力・転記ミスに注意して確認する", "BETTER"),
            ("一部端末が動いたので独自に電子入力を再開する", "BAD"),
            ("紙記録を不要になったらすぐ廃棄する", "BAD"),
            ("復旧状況の問い合わせは対策本部の発表を確認して答える", "BETTER"),
        ],
    },
    "PHASE 07：医療トリアージ": {
        "管理監督者": [
            ("予定手術を延期し、救急受入を一時制限する", "BEST"),
            ("透析・重症・入院患者の安全確認を優先する", "BEST"),
            ("近隣病院へ救急・検査の一部代替を依頼する", "BETTER"),
            ("通常診療を維持し、現場の注意で乗り切る", "BAD"),
            ("診療制限を診療科ごとの判断に任せる", "BAD"),
            ("患者優先順位と受入基準を全館へ明文化する", "BETTER"),
        ],
        "SE": [
            ("診療継続に必要な最小システムを特定する", "BEST"),
            ("検査・薬剤・画像の停止状況を医療安全担当へ共有する", "BEST"),
            ("復旧対象の優先順位を医療側と擦り合わせる", "BETTER"),
            ("便利な部門端末だけ先にネットワークへ戻す", "BAD"),
            ("個別依頼でUSBや私用端末を使う", "BAD"),
            ("医療安全上必要な参照データの安全な取得方法を確認する", "BETTER"),
        ],
        "職員": [
            ("患者の優先度に従い、案内・誘導を行う", "BEST"),
            ("検査結果や処方はダブルチェックして伝達する", "BEST"),
            ("急変リスクのある患者を上長へ早めに共有する", "BETTER"),
            ("混雑しているので確認を省いて口頭で済ませる", "BAD"),
            ("患者から急かされたため順番を独自に変える", "BAD"),
            ("紙記録と患者本人確認をセットで行う", "BETTER"),
        ],
    },
    "PHASE 08：情報漏えい疑惑": {
        "管理監督者": [
            ("流出有無は断定せず、可能性として調査開始を記録する", "BEST"),
            ("個人情報保護・法務・広報の対応チームを組む", "BEST"),
            ("患者問い合わせ窓口と想定問答を準備する", "BETTER"),
            ("確証がないため『流出なし』と断言する", "BAD"),
            ("職員に口外禁止だけ伝え、詳細共有しない", "BAD"),
            ("関係機関への相談・報告要否を確認する", "BETTER"),
        ],
        "SE": [
            ("漏えい可能性のあるログ、通信先、ファイルアクセスを確認する", "BEST"),
            ("患者情報が写った可能性のある画面・端末を特定する", "BEST"),
            ("調査結果を確認済み事実と未確認事項に分ける", "BETTER"),
            ("痕跡を消すためログを削除する", "BAD"),
            ("証跡保全前に端末を初期化する", "BAD"),
            ("ダークウェブ掲載疑惑があれば専門業者と確認する", "BETTER"),
        ],
        "職員": [
            ("患者情報を含む紙記録や画面表示の扱いを厳格にする", "BEST"),
            ("不審な情報の外部掲載を見つけたら拡散せず報告する", "BEST"),
            ("漏えい疑惑について聞かれても定型文で対応する", "BETTER"),
            ("不安から患者情報が表示された画面を同僚チャットへ共有する", "BAD"),
            ("患者に『多分漏れていません』と個人判断で伝える", "BAD"),
            ("記録物の置き忘れや写真撮影がないか周囲を確認する", "BETTER"),
        ],
    },
    "PHASE 09：広報・患者説明": {
        "管理監督者": [
            ("第1報を公表し、診療制限と問い合わせ窓口を示す", "BEST"),
            ("未確定事項は未確定として説明する方針を明確にする", "BEST"),
            ("院長・広報・医療安全で記者会見想定問答を確認する", "BETTER"),
            ("『軽微な障害』として短い告知だけ出す", "BAD"),
            ("報道対応を避け、すべて調査中で押し通す", "BAD"),
            ("患者向け説明文をWeb・院内掲示・受付で統一する", "BETTER"),
        ],
        "SE": [
            ("技術的な確認済み事実と未確認事項を広報へ提供する", "BEST"),
            ("外部公表前にシステム影響範囲の表現を確認する", "BEST"),
            ("復旧見込みは幅を持って説明し、断定を避ける", "BETTER"),
            ("根拠なく『すぐ直る』と広報資料に書く", "BAD"),
            ("専門用語だけで説明し、現場や患者向け表現に直さない", "BAD"),
            ("再発防止策の技術項目を整理して説明材料にする", "BETTER"),
        ],
        "職員": [
            ("患者・家族へ配布用説明文に沿って案内する", "BEST"),
            ("説明した内容と問い合わせを記録する", "BEST"),
            ("苦情や不安の強い患者を相談窓口へつなぐ", "BETTER"),
            ("報道関係者に現場の状況を個人的に話す", "BAD"),
            ("患者へ他職員から聞いた未確認情報を伝える", "BAD"),
            ("院内掲示の内容が古ければ上長へ更新を依頼する", "BETTER"),
        ],
    },
    "PHASE 10：復旧・再発防止": {
        "管理監督者": [
            ("時系列、判断者、根拠、未解決課題を報告書化する", "BEST"),
            ("次回訓練日と改善担当者を設定する", "BEST"),
            ("連絡網、紙運用、広報、訓練計画の見直しを決める", "BETTER"),
            ("復旧したので詳細な振り返りは省略する", "BAD"),
            ("問題のあった職員の責任追及を最優先する", "BAD"),
            ("経営層向けに再発防止投資の優先順位を示す", "BETTER"),
        ],
        "SE": [
            ("侵害経路と復旧手順の技術レポートをまとめる", "BEST"),
            ("復旧後のアカウント棚卸しとパスワードリセットを行う", "BEST"),
            ("EDR、MFA、バックアップ分離、ログ監視の改善案を作る", "BETTER"),
            ("原因が曖昧なまま本番環境を完全再開する", "BAD"),
            ("古い端末をそのまま業務へ戻す", "BAD"),
            ("訓練で出た技術課題を次年度計画に反映する", "BETTER"),
        ],
        "職員": [
            ("紙運用で困った点を振り返りに提出する", "BEST"),
            ("患者説明や誘導で混乱した点を記録する", "BEST"),
            ("SNS・写真撮影・個人情報取扱いの再教育を受ける", "BETTER"),
            ("訓練が終わったのでメモや紙記録を適当に処分する", "BAD"),
            ("ミスを隠して報告しない", "BAD"),
            ("次回訓練に向けて必要物品や様式の改善案を出す", "BETTER"),
        ],
    },
}

for phase in PHASES:
    if phase["title"] in PHASE_CHOICE_OVERRIDES:
        phase["choices"] = PHASE_CHOICE_OVERRIDES[phase["title"]]



RANDOM_EVENTS = [
    {
        "id": "bereal",
        "title": "職員がSNSに院内の乗っ取り画面を投稿！",
        "desc": "電子カルテのランサムウェア画面を、ある職員が深く考えずSNSへ投稿。患者名や端末情報が写り込んだ可能性があり、院外からの問い合わせが急増している。",
        "icon": "📱",
        "effect": {"panic": 20, "bcp": -14, "trust": -34},
        "feedback": {
            True: "SNS拡散対応として適切です。削除依頼、証跡保全、統一コメント、職員への注意喚起を同時に進める必要があります。",
            False: "SNS拡散対応として危険です。スクリーンショット共有や放置は二次拡散を招き、個人情報漏えい疑義を拡大します。",
        },
        "choices": {
            "管理監督者": [
                ("投稿者の特定、削除依頼、事実確認、広報連絡を同時に指示する", True),
                ("SNS投稿を個人の問題として扱い、組織対応は後回しにする", False),
                ("患者情報の写り込み可能性を確認し、個人情報対応チームを動かす", True),
                ("院内へSNS投稿禁止とスクリーンショット拡散禁止を周知する", True),
                ("炎上を避けるため、職員へ投稿の話題を一切しないよう指示する", False),
                ("外部問い合わせ用の統一コメントを広報と作成する", True),
            ],
            "SE": [
                ("投稿画像に患者情報・端末名・ネットワーク情報が写っていないか確認する", True),
                ("投稿端末を初期化し、画像やログを消してしまう", False),
                ("投稿時刻と端末ログを突合し、証跡を保全する", True),
                ("拡散済み画像の範囲確認を広報・法務へ共有する", True),
                ("画像をSE内チャットに貼って全員で確認する", False),
                ("当該端末の感染状態と操作履歴を確認する", True),
            ],
            "職員": [
                ("投稿を拡散せず、上長と対策本部へ即時報告する", True),
                ("スクリーンショットを同僚グループに共有して注意喚起する", False),
                ("投稿者本人へ削除を依頼し、上長にも報告する", True),
                ("患者から聞かれたら定型文で対応し、推測で話さない", True),
                ("自分のSNSで『院内が大変』と投稿する", False),
                ("近くの職員に写真撮影・投稿を控えるよう声をかける", True),
            ],
        },
    },
    {
        "id": "chat_down",
        "title": "院内チャット停止",
        "desc": "業務チャットが停止。連絡手段が内線・紙による連絡が中心となり、現場の混乱が増している。",
        "icon": "💬",
        "effect": {"panic": 18, "bcp": -14, "trust": -8},
        "feedback": {
            True: "代替連絡として適切です。内線、紙掲示、連絡係、記録様式を使って情報の混乱を抑えられます。",
            False: "代替連絡として危険です。私用SNSや口伝え中心の連絡は、患者情報漏えいと誤った情報の拡散につながります。",
        },
        "choices": {
            "管理監督者": [
                ("内線、紙掲示、定時集合の代替連絡ルールを決める", True),
                ("各部署の判断で好きな連絡手段を使わせる", False),
                ("重要連絡は対策本部から一方向に出す仕組みにする", True),
                ("連絡係を部署ごとに指定する", True),
                ("チャット復旧まで指示を止める", False),
                ("問い合わせ内容を紙で集約する様式を配布する", True),
            ],
            "SE": [
                ("チャット停止原因と影響範囲を切り分ける", True),
                ("代替連絡手段の安全性を確認する", True),
                ("私用SNSグループを業務連絡に使うよう案内する", False),
                ("復旧見込みを対策本部へ共有する", True),
                ("停止中のチャットサーバーを未確認のまま再接続する", False),
                ("連絡用端末・内線の利用可否を確認する", True),
            ],
            "職員": [
                ("所属部署の代替連絡ルールを確認する", True),
                ("重要事項は紙や内線で記録を残して伝える", True),
                ("私用LINEで患者情報を共有する", False),
                ("指示が不明な場合は上長へ確認する", True),
                ("聞いた話をそのまま他部署へ流す", False),
                ("掲示板・ホワイトボードの最新指示を確認する", True),
            ],
        },
    },
]


# BETTER / BAD の選択によって誘発される突発イベント
INDUCED_EVENTS = [
    {
        "id": "induced_misinformation",
        "title": "未確認情報が院内外へ拡散",
        "desc": "曖昧な説明や統一されていない案内により、患者・家族・職員の間で未確認情報が広がった。問い合わせが急増している。",
        "icon": "📢",
        "effect": {"panic": 18, "bcp": -10, "trust": -18},
        "trigger": ["BETTER", "BAD"],
        "feedback": {
            True: "情報拡散への対応として適切です。窓口一本化、定型文、記録、誤情報訂正を同時に進める必要があります。",
            False: "情報拡散への対応として危険です。推測説明や放置は混乱と信用低下を加速させます。",
        },
        "choices": {
            "管理監督者": [
                ("広報・対策本部に問い合わせ窓口を一本化し、統一コメントを出す", "BEST"),
                ("各部署に現場判断で説明してもらう", "BAD"),
                ("患者向けFAQを即時更新し、院内掲示にも反映する", "BETTER"),
                ("混乱を避けるため、問い合わせには答えないよう指示する", "BAD"),
                ("誤情報の内容を記録し、訂正すべき情報を整理する", "BEST"),
                ("報道対応は後回しにして現場対応だけを優先する", "BAD"),
            ],
            "SE": [
                ("技術的に確認済みの事実と未確認事項を分けて対策本部へ共有する", "BEST"),
                ("原因不明だが安心させるため『復旧間近』と伝える", "BAD"),
                ("影響範囲図を更新し、広報が使える表現に整理する", "BETTER"),
                ("専門用語だけで状況を説明し、現場判断に任せる", "BAD"),
                ("ログ上確認できた事実のみを記録して共有する", "BEST"),
                ("現場から聞いた噂も参考情報として全体へ流す", "BAD"),
            ],
            "職員": [
                ("患者には定型文で説明し、推測で答えない", "BEST"),
                ("聞いた話を患者へそのまま伝える", "BAD"),
                ("繰り返し問い合わせを記録し、上長へ共有する", "BETTER"),
                ("不安を抑えるため『大丈夫です』と断言する", "BAD"),
                ("不明点は対策本部・上長へ確認してから回答する", "BEST"),
                ("SNSで院内の状況を説明する", "BAD"),
            ],
        },
    },
    {
        "id": "induced_reinfection",
        "title": "未確認端末から再感染の疑い",
        "desc": "安全確認が不十分な端末・ネットワーク操作により、別部門で再び不審な通信が検知された。封じ込め判断が必要。",
        "icon": "🦠",
        "effect": {"infection": 24, "panic": 12, "bcp": -16, "trust": -8},
        "trigger": ["BAD"],
        "feedback": {
            True: "再感染疑いへの対応として適切です。隔離、ログ確認、認証情報見直しを優先する必要があります。",
            False: "再感染疑いへの対応として危険です。未確認端末の継続利用は感染拡大と復旧失敗につながります。",
        },
        "choices": {
            "管理監督者": [
                ("再感染疑い部門の業務を一時制限し、対策本部判断に切り替える", "BEST"),
                ("診療影響を避けるため、当該部門にはそのまま業務継続させる", "BAD"),
                ("ベンダーと情報担当へ緊急調査を指示し、関係部門へ周知する", "BEST"),
                ("原因が判明するまで外部報告は一切しない", "BAD"),
                ("診療継続に必要な代替手順を発動する", "BETTER"),
                ("現場の不安を避けるため詳細を共有しない", "BAD"),
            ],
            "SE": [
                ("疑い端末を即時隔離し、通信ログと認証ログを確認する", "BEST"),
                ("端末を再起動して様子を見る", "BAD"),
                ("同一セグメントの端末を洗い出し、横展開の有無を確認する", "BEST"),
                ("復旧を急ぐため一部通信を例外許可する", "BAD"),
                ("管理者権限と認証情報の悪用有無を確認する", "BETTER"),
                ("ログが多すぎるため重要そうなものだけ削除して整理する", "BAD"),
            ],
            "職員": [
                ("不審端末を操作せず、上長と情報担当へ報告する", "BEST"),
                ("業務が止まるので別端末で同じ作業を続ける", "BAD"),
                ("紙運用に戻し、電子入力再開の指示を待つ", "BETTER"),
                ("端末の画面を撮って同僚チャットへ共有する", "BAD"),
                ("患者対応は定型文に沿って説明する", "BETTER"),
                ("自分でLANケーブルを差し替えて動く端末を探す", "BAD"),
            ],
        },
    },
    {
        "id": "induced_privacy",
        "title": "患者情報の写り込み・持ち出し疑義",
        "desc": "紙記録や画面写真の扱いが不適切だった可能性があり、患者情報の写り込み・持ち出し疑義が発生した。",
        "icon": "🔐",
        "effect": {"panic": 14, "bcp": -8, "trust": -28},
        "trigger": ["BETTER", "BAD"],
        "feedback": {
            True: "個人情報疑義への対応として適切です。事実確認、証跡保全、相談準備、説明窓口の整備が必要です。",
            False: "個人情報疑義への対応として危険です。隠蔽や個人判断の説明は信用失墜を招きます。",
        },
        "choices": {
            "管理監督者": [
                ("個人情報保護・法務・広報担当を集め、事実確認を開始する", "BEST"),
                ("小さな問題として部署内で処理させる", "BAD"),
                ("患者問い合わせ窓口と想定問答を準備する", "BETTER"),
                ("職員へ口外禁止だけ指示し、詳細確認は後回しにする", "BAD"),
                ("写り込み範囲・対象者・外部拡散の有無を記録する", "BEST"),
                ("確証がないため『漏えいなし』と断言する", "BAD"),
            ],
            "SE": [
                ("画像・端末・ログを確認し、患者情報の写り込み有無を調べる", "BEST"),
                ("問題を消すため画像やログを削除する", "BAD"),
                ("投稿・撮影時刻と端末操作履歴を突合する", "BEST"),
                ("関係しそうな職員へ画像を転送して確認してもらう", "BAD"),
                ("調査結果を確認済み事実と未確認事項に分ける", "BETTER"),
                ("端末を初期化してから報告する", "BAD"),
            ],
            "職員": [
                ("写真や紙記録を拡散せず、上長へ即時報告する", "BEST"),
                ("注意喚起のため同僚グループへ画像を共有する", "BAD"),
                ("患者情報が見える資料を所定場所に回収する", "BETTER"),
                ("患者へ『漏れていないと思う』と個人判断で説明する", "BAD"),
                ("画面撮影・SNS投稿を控えるよう周囲に声をかける", "BEST"),
                ("自分のスマホに保存した画像を後で確認する", "BAD"),
            ],
        },
    },
]



# ============================================================
# State
# ============================================================

def init_state():
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "NORMAL"
    if "role" not in st.session_state:
        st.session_state.role = "職員"
    if "collab_mode" not in st.session_state:
        st.session_state.collab_mode = "個別プレイ"
    if "collab_team" not in st.session_state:
        st.session_state.collab_team = COLLAB_TEAMS[0]
    if "simulation_started" not in st.session_state:
        st.session_state.simulation_started = False
    if "completed" not in st.session_state:
        st.session_state.completed = False
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "pending_feedback" not in st.session_state:
        st.session_state.pending_feedback = None
    if "pending_induced_event" not in st.session_state:
        st.session_state.pending_induced_event = None
    if "_choice_processing" not in st.session_state:
        st.session_state._choice_processing = False
    if "history" not in st.session_state:
        st.session_state.history = []
    if "seen_event_ids" not in st.session_state:
        st.session_state.seen_event_ids = set()
    if "last_se_key" not in st.session_state:
        st.session_state.last_se_key = None
    if "seen_induced_event_ids" not in st.session_state:
        st.session_state.seen_induced_event_ids = set()
    if "choice_orders" not in st.session_state:
        st.session_state.choice_orders = {}
    if "bgm_volume" not in st.session_state:
        st.session_state.bgm_volume = 35
    if "se_volume" not in st.session_state:
        st.session_state.se_volume = 70
    if "bgm_enabled" not in st.session_state:
        st.session_state.bgm_enabled = True
    if "se_enabled" not in st.session_state:
        st.session_state.se_enabled = True
    if "phase" not in st.session_state:
        reset_game()


def reset_game():
    clear_shared_query_params()
    d = DIFFICULTIES[st.session_state.get("difficulty", "NORMAL")]
    current_mode = st.session_state.get("collab_mode", "個別プレイ")
    current_team = st.session_state.get("collab_team", COLLAB_TEAMS[0])
    st.session_state.phase = 0
    st.session_state.completed = False
    st.session_state.game_over = False
    st.session_state.simulation_started = False
    st.session_state.pending_feedback = None
    st.session_state.pending_induced_event = None
    st.session_state._choice_processing = False
    st.session_state.history = []
    st.session_state.seen_event_ids = set()
    st.session_state.seen_induced_event_ids = set()
    st.session_state.last_se_key = None
    st.session_state.choice_orders = {}
    st.session_state.infection = d["infection"]
    st.session_state.panic = d["panic"]
    st.session_state.bcp = d["bcp"]
    st.session_state.trust = d["trust"]
    st.session_state.started_at = time.time()
    st.session_state.phase_started_at = time.time()
    st.session_state.last_event_at = time.time()
    st.session_state.current_event = None
    st.session_state.event_expanded = False
    st.session_state.collab_mode = current_mode
    st.session_state.collab_team = current_team
    st.session_state.log = ["[SYSTEM] セットアップ待機"]
    if shared_play_enabled():
        try:
            path = shared_state_path(current_team)
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
    clear_shared_query_params()


def start_simulation():
    d = DIFFICULTIES[st.session_state.difficulty]
    st.session_state.simulation_started = True
    st.session_state.completed = False
    st.session_state.game_over = False
    st.session_state.phase = 0
    st.session_state.pending_feedback = None
    st.session_state.pending_induced_event = None
    st.session_state._choice_processing = False
    st.session_state.history = []
    st.session_state.seen_event_ids = set()
    st.session_state.seen_induced_event_ids = set()
    st.session_state.last_se_key = None
    st.session_state.choice_orders = {}
    st.session_state.infection = d["infection"]
    st.session_state.panic = d["panic"]
    st.session_state.bcp = d["bcp"]
    st.session_state.trust = d["trust"]
    st.session_state.phase_started_at = time.time()
    st.session_state.last_event_at = time.time()
    st.session_state.current_event = None
    st.session_state.event_expanded = False
    shared_label = f" / 共有:{st.session_state.collab_team}" if shared_play_enabled() else ""
    st.session_state.log = [f"[SYSTEM] 開始 / 難易度:{st.session_state.difficulty} / 役割:{st.session_state.role}{shared_label}"]
    save_shared_state()
    set_shared_query_params()


def auto_refresh(interval_seconds: int = 1):
    """Streamlit全体の再描画を必要最小限にする。
    BGM途切れ防止のため、毎秒リロードではなく、イベント発生予定またはタイムアウト予定に合わせる。
    """
    interval_seconds = max(1, int(interval_seconds))
    st_autorefresh(
        interval=interval_seconds * 1000,
        key="medical_cyber_bcp_timer_refresh",
    )


def seconds_to_next_refresh() -> Optional[int]:
    """次にStreamlit側の状態更新が必要になる秒数を返す。"""
    if not st.session_state.get("simulation_started", False):
        return None
    if st.session_state.get("completed", False) or st.session_state.get("game_over", False):
        return None
    if st.session_state.get("pending_feedback") is not None:
        return None
    if st.session_state.current_event is not None and st.session_state.event_expanded:
        return None

    rem = remaining_time()
    if rem <= 0:
        return 1

    event_interval = DIFFICULTIES[st.session_state.get("difficulty", "NORMAL")]["event"]
    if event_interval is None:
        return rem

    # 発生済みイベントがすべて出尽くした場合はタイムアウトだけを見ればよい
    available_events = [
        ev for ev in RANDOM_EVENTS
        if ev["id"] not in st.session_state.seen_event_ids
    ]
    if not available_events:
        return rem

    elapsed_from_event = int(time.time() - st.session_state.last_event_at)
    event_remaining = max(1, event_interval - elapsed_from_event)

    return min(rem, event_remaining)


def clamp(v):
    return max(0, min(120, v))


def apply_effect(effect: Dict[str, int]):
    st.session_state.infection = clamp(st.session_state.infection + effect.get("infection", 0))
    st.session_state.panic = clamp(st.session_state.panic + effect.get("panic", 0))
    st.session_state.bcp = clamp(st.session_state.bcp + effect.get("bcp", 0))
    st.session_state.trust = clamp(st.session_state.trust + effect.get("trust", 0))


def remaining_time():
    limit = current_phase_limit()
    if (
        not st.session_state.get("simulation_started", False)
        or st.session_state.get("completed", False)
        or st.session_state.get("game_over", False)
        or st.session_state.get("pending_feedback") is not None
    ):
        return limit
    return max(0, limit - int(time.time() - st.session_state.phase_started_at))


def time_percent():
    limit = current_phase_limit()
    return int(remaining_time() / limit * 100) if limit else 0


def maybe_random_event():
    if not st.session_state.get("simulation_started", False):
        return
    if st.session_state.get("completed", False) or st.session_state.get("game_over", False):
        return
    if st.session_state.get("pending_feedback") is not None:
        return
    if st.session_state.current_event is not None and st.session_state.event_expanded:
        return

    interval = DIFFICULTIES[st.session_state.get("difficulty", "NORMAL")]["event"]
    if interval is None:
        return

    available_events = [
        ev for ev in RANDOM_EVENTS
        if ev["id"] not in st.session_state.seen_event_ids
    ]

    if not available_events:
        return

    if time.time() - st.session_state.last_event_at > interval:
        ev = random.choice(available_events)
        st.session_state.current_event = ev
        st.session_state.event_expanded = True
        st.session_state.seen_event_ids.add(ev["id"])
        apply_effect(ev["effect"])
        st.session_state.last_event_at = time.time()
        st.session_state.log.append(f"[突発事象] {ev['title']}")
        play_se("event", f"event_{ev['id']}_{len(st.session_state.history)}")
        save_shared_state()


def get_context():
    if st.session_state.current_event is not None and st.session_state.event_expanded:
        return "event", st.session_state.current_event
    return "phase", PHASES[int(st.session_state.get("phase", 0))]


def normalize_choices(raw_choices: List[tuple]) -> List[tuple]:
    """選択肢を必ず6件、かつ BEST / BETTER / BAD の3段階へ変換する。"""
    normalized = []
    good_count = 0

    for idx, item in enumerate(raw_choices[:6]):
        text = item[0]
        raw = item[1]

        if isinstance(raw, str):
            quality = raw.upper()
            if quality not in ["BEST", "BETTER", "BAD"]:
                quality = "BAD"
        elif raw is True:
            good_count += 1
            quality = "BEST" if good_count == 1 else "BETTER"
        else:
            quality = "BAD"

        normalized.append((text, quality))

    fallback = [
        ("対策本部へ報告し、判断を仰ぐ", "BETTER"),
        ("記録を残し、後で検証できる状態にする", "BETTER"),
        ("確認を省略して現場判断で進める", "BAD"),
        ("未確認情報を周囲へ共有する", "BAD"),
        ("患者・家族への説明は定型文に従う", "BETTER"),
        ("安全確認前に作業を再開する", "BAD"),
    ]

    for item in fallback:
        if len(normalized) >= 6:
            break
        normalized.append(item)

    return normalized[:6]


def get_current_choices() -> List[tuple]:
    mode, obj = get_context()
    raw = obj["choices"][st.session_state.role]
    normalized = normalize_choices(raw)

    if mode == "event":
        context_id = f"event_{obj['id']}_{st.session_state.role}"
    else:
        context_id = f"phase_{st.session_state.phase}_{st.session_state.role}"

    if context_id not in st.session_state.choice_orders:
        order = list(range(len(normalized)))
        random.shuffle(order)
        st.session_state.choice_orders[context_id] = order

    order = st.session_state.choice_orders[context_id]
    return [normalized[i] for i in order]


def maybe_induce_event(quality: str):
    """BETTER / BAD 選択後に、その判断が引き金となる突発イベントを発生させる。"""
    if quality == "BEST":
        return False

    candidates = [
        ev for ev in INDUCED_EVENTS
        if quality in ev.get("trigger", [])
        and ev["id"] not in st.session_state.seen_induced_event_ids
    ]

    if not candidates:
        return False

    # BADなら高確率、BETTERなら中確率で誘発
    probability = 0.85 if quality == "BAD" else 0.45

    if random.random() > probability:
        return False

    ev = random.choice(candidates)
    # ここでは current_event を即時差し替えない。
    # 選択ボタン押下中に画面コンテキストが変わると、フィードバック画面へ遷移せず
    # リスク値だけが変わったように見えるため、フィードバック確認後に発生させる。
    st.session_state.pending_induced_event = ev
    st.session_state.seen_induced_event_ids.add(ev["id"])
    return True


def choose(idx: int):
    """選択肢押下時の状態更新。

    突発イベント対応時に、選択処理中のイベント差し替えや二重実行が起きると
    「リスク値だけ変わってフィードバックへ遷移しない」状態に見えるため、
    ここでは必ず 1 回の押下につき pending_feedback を確定してから rerun する。
    """
    if st.session_state.get("_choice_processing", False):
        return
    if st.session_state.get("pending_feedback") is not None:
        return
    if st.session_state.get("completed", False) or st.session_state.get("game_over", False):
        return

    st.session_state._choice_processing = True
    try:
        mode, obj = get_context()
        context_event_id = obj.get("id") if mode == "event" else None
        choices = get_current_choices()
        if idx < 0 or idx >= len(choices):
            st.session_state._choice_processing = False
            st.session_state.log.append("[WARN] 選択肢の取得に失敗")
            return
        text, quality = choices[idx]

        if quality == "BEST":
            recover = random.randint(2, 5)
            st.session_state.phase_started_at += recover
            st.session_state.infection = clamp(st.session_state.infection - random.randint(4, 9))
            st.session_state.panic = clamp(st.session_state.panic - random.randint(5, 12))
            st.session_state.bcp = clamp(st.session_state.bcp + random.randint(5, 12))
            st.session_state.trust = clamp(st.session_state.trust + random.randint(4, 10))
            result = "BEST"
            feedback_prefix = "適切な初動判断です。"
            se_kind = "best"
        elif quality == "BETTER":
            recover = random.randint(1, 3)
            st.session_state.phase_started_at += recover
            st.session_state.infection = clamp(st.session_state.infection + random.randint(0, 4))
            st.session_state.panic = clamp(st.session_state.panic + random.randint(0, 6))
            st.session_state.bcp = clamp(st.session_state.bcp + random.randint(0, 4))
            st.session_state.trust = clamp(st.session_state.trust + random.randint(0, 3))
            result = "BETTER"
            feedback_prefix = "一定の効果はありますが、判断の優先順位としては不十分です。副作用として新たなリスクを誘発する可能性があります。"
            se_kind = "better"
        else:
            recover = 0
            st.session_state.infection = clamp(st.session_state.infection + random.randint(10, 22))
            st.session_state.panic = clamp(st.session_state.panic + random.randint(12, 26))
            st.session_state.bcp = clamp(st.session_state.bcp - random.randint(10, 24))
            st.session_state.trust = clamp(st.session_state.trust - random.randint(12, 28))
            result = "BAD"
            feedback_prefix = "リスクの高い判断です。この対応により追加インシデントを誘発する可能性があります。"
            se_kind = "bad"

        base_feedback = feedback_text_for(obj, quality != "BAD")

        # 通常フェーズの選択だけが、次画面以降の突発イベントを誘発できる。
        # 突発イベント対応中は別イベントを発生させない。
        st.session_state.pending_induced_event = None
        induced = False if mode == "event" else maybe_induce_event(quality)
        pending_ev = st.session_state.get("pending_induced_event") if induced else None

        guideline_text = guideline_viewpoint_for(obj["title"])
        induced_text = ""
        if pending_ev is not None:
            induced_text = f"<br><br><strong>誘発された突発イベント：</strong>{pending_ev['title']}<br>{pending_ev['desc']}"
        feedback_text = f"{feedback_prefix}<br>{base_feedback}{induced_text}<br><br><strong>GL6.0観点：</strong>{guideline_text}"
        title = obj["title"]

        record = {
            "time": time.strftime("%H:%M:%S"),
            "mode": "突発イベント" if mode == "event" else "通常フェーズ",
            "phase": PHASES[st.session_state.phase]["title"],
            "event": obj["title"] if mode == "event" else "",
            "role": st.session_state.role,
            "difficulty": st.session_state.difficulty,
            "training_purpose": "初動判断、報告連絡、紙運用、SNS/個人情報対応、BCP切替判断の確認",
            "choice": text,
            "result": result,
            "feedback": feedback_text.replace("<br>", " "),
            "guideline_viewpoint": guideline_viewpoint_for(obj["title"]),
            "induced_event": pending_ev["title"] if pending_ev is not None else "",
            "infection": st.session_state.infection,
            "panic": st.session_state.panic,
            "bcp": st.session_state.bcp,
            "trust": st.session_state.trust,
        }
        st.session_state.history.append(record)

        st.session_state.pending_feedback = {
            "mode": mode,
            "event_id": context_event_id,
            "title": title,
            "choice": text,
            "quality": quality,
            "good": quality != "BAD",
            "result": result,
            "feedback": feedback_text,
            "induced": induced,
        }

        st.session_state.log.append(f"[{result}] {text[:26]}")
        play_se(se_kind, f"feedback_{len(st.session_state.history)}_{result}")
        check_status_game_over(triggered_by_choice=True)
        st.session_state._choice_processing = False
        st.session_state["_skip_shared_sync_once"] = True
        save_shared_state()
        set_shared_query_params()
    except Exception as exc:
        st.session_state._choice_processing = False
        st.session_state.log.append(f"[ERROR] 選択処理: {type(exc).__name__}: {exc}")
        save_shared_state()

def proceed_after_feedback():
    if st.session_state.pending_feedback is None:
        return
    if st.session_state.game_over:
        st.session_state._choice_processing = False
        save_shared_state()
        set_shared_query_params()
        return

    mode = st.session_state.pending_feedback.get("mode")
    had_induced = bool(st.session_state.pending_feedback.get("induced"))
    pending_ev = st.session_state.get("pending_induced_event")
    st.session_state.pending_feedback = None
    st.session_state._choice_processing = False

    if mode == "event":
        # 対応済みの突発イベントを確実に閉じ、通常フェーズへ戻す。
        st.session_state.event_expanded = False
        st.session_state.current_event = None
        st.session_state.pending_induced_event = None
        st.session_state.phase_started_at = time.time()
    elif had_induced and pending_ev is not None:
        # 通常フェーズ選択の結果として発生した突発イベントは、
        # フィードバック確認後に初めて current_event へ反映する。
        st.session_state.current_event = pending_ev
        st.session_state.event_expanded = True
        apply_effect(pending_ev.get("effect", {}))
        st.session_state.last_event_at = time.time()
        st.session_state.log.append(f"[誘発事象] {pending_ev['title']}")
        st.session_state.pending_induced_event = None
        play_se("event", f"induced_{pending_ev['id']}_{len(st.session_state.history)}")
        st.session_state.phase_started_at = time.time()
    else:
        # 通常フェーズのフィードバック後は次フェーズへ進む。
        st.session_state.pending_induced_event = None
        if st.session_state.phase < len(PHASES) - 1:
            st.session_state.phase += 1
            st.session_state.phase_started_at = time.time()
        else:
            st.session_state.completed = True

    save_shared_state()
    set_shared_query_params()

def check_status_game_over(triggered_by_choice: bool = False):
    """ステータス条件による訓練終了。
    感染拡大度・院内混乱度が100%以上、または診療継続性・対外的信頼が0以下で発生。
    選択後の場合はフィードバック画面に訓練終了理由を統合する。
    """
    if st.session_state.get("game_over", False):
        return

    reasons = []

    if st.session_state.infection >= 100:
        reasons.append("システム感染拡大度が100％に到達しました。院内システム全体への感染拡大を抑制できない状態です。")
    if st.session_state.panic >= 100:
        reasons.append("院内業務混乱度が100％に到達しました。現場統制が困難な状態です。")
    if st.session_state.bcp <= 0:
        reasons.append("診療継続性が0％に到達しました。安全な診療継続ができません。")
    if st.session_state.trust <= 0:
        reasons.append("対外的信頼が0％に到達しました。説明責任と信頼維持に失敗しました。")

    if not reasons:
        return

    st.session_state.game_over = True
    reason_text = "<br>".join(reasons)

    st.session_state.history.append({
        "time": time.strftime("%H:%M:%S"),
        "mode": "訓練終了",
        "phase": PHASES[st.session_state.phase]["title"],
        "event": st.session_state.current_event["title"] if st.session_state.current_event else "",
        "role": st.session_state.role,
        "difficulty": st.session_state.difficulty,
        "choice": "ステータス条件",
        "result": "訓練終了",
        "feedback": reason_text.replace("<br>", " "),
        "infection": st.session_state.infection,
        "panic": st.session_state.panic,
        "bcp": st.session_state.bcp,
        "trust": st.session_state.trust,
    })

    if triggered_by_choice and st.session_state.pending_feedback is not None:
        st.session_state.pending_feedback["feedback"] += f"<br><br><strong>訓練終了：</strong>{reason_text}"
        st.session_state.pending_feedback["result"] = f"{st.session_state.pending_feedback['result']} / 訓練終了"
    else:
        st.session_state.pending_feedback = {
            "mode": "gameover",
            "title": "訓練終了",
            "choice": "ステータス条件",
            "quality": "BAD",
            "good": False,
            "result": "訓練終了",
            "feedback": reason_text,
        }

    st.session_state.log.append("[訓練終了] ステータス条件")
    play_se("gameover", f"gameover_status_{len(st.session_state.history)}")
    save_shared_state()


def check_timeout():
    if not st.session_state.get("simulation_started", False):
        return
    if st.session_state.get("completed", False) or st.session_state.get("game_over", False):
        return
    if st.session_state.get("pending_feedback") is not None:
        return
    if remaining_time() <= 0:
        st.session_state.game_over = True
        st.session_state.log.append("[訓練終了] 時間超過")
        play_se("gameover", f"gameover_timeout_{len(st.session_state.history)}")
        st.session_state.history.append({
            "time": time.strftime("%H:%M:%S"),
            "mode": "訓練終了",
            "phase": PHASES[st.session_state.phase]["title"],
            "event": st.session_state.current_event["title"] if st.session_state.current_event else "",
            "role": st.session_state.role,
            "difficulty": st.session_state.difficulty,
            "choice": "時間超過",
            "result": "制限時間を超過したため訓練終了",
            "feedback": "制限時間を超過したため訓練終了となりました。インシデント対応では、判断遅延そのものが感染拡大・医療安全リスク・信用低下につながります。",
            "infection": st.session_state.infection,
            "panic": st.session_state.panic,
            "bcp": st.session_state.bcp,
            "trust": st.session_state.trust,
        })
        save_shared_state()


# ============================================================
# UI helpers
# ============================================================

def status_row(icon, name, value, color):
    st.sidebar.markdown(
        f"""
<div class="status-row">
  <div class="status-name" style="color:{color};">{name}</div>
  <div class="status-value" style="color:{color};">{value}%</div>
  <div class="bar-bg"><div class="bar-fill" style="width:{value}%;background:{color};"></div></div>
</div>
""",
        unsafe_allow_html=True,
    )


def get_bgm_mode() -> str:
    if st.session_state.get("game_over", False):
        return "gameover"
    if st.session_state.get("completed", False):
        return "clear"
    if st.session_state.get("current_event") is not None and st.session_state.get("event_expanded", False):
        return "event"
    return "normal"


def render_audio():
    # BGMのON/OFFと音量は左コンソール側で制御する。
    bgm_mode = get_bgm_mode()
    bgm_volume = st.session_state.get("bgm_volume", 35) / 100.0
    bgm_enabled = "true" if st.session_state.get("bgm_enabled", True) else "false"

    components.html(
        f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
html, body {{ margin:0; padding:0; width:0; height:0; overflow:hidden; background:transparent; }}
#status {{ display:none; }}
</style>
</head>
<body>
<div id="status"></div>
<script>
(function(){{
  var ctx=null, master=null, timer=null, playing=false;
  var mode = "{bgm_mode}";
  var bgmVolume = {bgm_volume};
  var enabled = {bgm_enabled};

  function init(){{
    var AC = window.AudioContext || window.webkitAudioContext;
    if(!AC){{ document.getElementById("status").innerText="状態：非対応"; return false; }}
    if(!ctx){{
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = bgmVolume * 0.12;
      master.connect(ctx.destination);
    }}
    return true;
  }}

  function beep(f,d,type,gainValue){{
    if(!ctx) return;
    var o=ctx.createOscillator(), g=ctx.createGain();
    o.type=type || "square";
    o.frequency.value=f;
    g.gain.value=(gainValue || 0.05) * Math.max(0.05, bgmVolume);
    o.connect(g);
    g.connect(master);
    o.start();
    o.stop(ctx.currentTime+d);
  }}

  function getPattern(){{
    if(mode === "event") return {{notes:[880,740,880,660,740,620], tempo:170, gain:0.05, type:"square", duration:0.07}};
    if(mode === "gameover") return {{notes:[180,160,140,120,100,80], tempo:260, gain:0.06, type:"sawtooth", duration:0.16}};
    if(mode === "clear") return {{notes:[392,493.88,587.33,783.99,659.25,783.99], tempo:240, gain:0.045, type:"triangle", duration:0.12}};
    return {{notes:[196,196,233.08,207.65,196,174.61,196,246.94,196,174.61,164.81,196], tempo:185, gain:0.048, type:"sawtooth", duration:0.14}};
  }}

  function startBgm(){{
    if(!init()) return;
    if(ctx.state==="suspended") ctx.resume();
    if(playing) return;
    playing=true;
    localStorage.setItem("medical_bcp_bgm", "on");
    localStorage.setItem("medical_bcp_bgm_mode", mode);
    document.getElementById("status").innerText="状態：再生中 ♪";
    var p = getPattern();
    var i=0;
    timer=setInterval(function(){{
      beep(p.notes[i%p.notes.length],p.duration || 0.07,p.type,p.gain);
      i++;
    }}, p.tempo);
  }}

  function stopBgm(){{
    playing=false;
    if(timer) clearInterval(timer);
    timer=null;
    localStorage.setItem("medical_bcp_bgm", "off");
    document.getElementById("status").innerText="状態：停止中";
  }}

  if(enabled){{
    localStorage.setItem("medical_bcp_bgm", "on");
    setTimeout(function(){{
      init();
      if(ctx && ctx.state !== "suspended") startBgm();
      else document.getElementById("status").innerText="状態：再開待ち（ブラウザ制限）";
    }}, 150);
  }} else {{
    localStorage.setItem("medical_bcp_bgm", "off");
    stopBgm();
  }}
}})();
</script>
</body>
</html>
""",
        height=0,
    )


def _se_sequence(kind: str) -> str:
    if kind == "event":
        return "beep(880,0.08,'square',0.08);setTimeout(function(){beep(440,0.12,'sawtooth',0.08);},90);"
    if kind == "gameover":
        return "beep(180,0.22,'sawtooth',0.09);setTimeout(function(){beep(120,0.28,'sawtooth',0.09);},230);"
    if kind == "best":
        return "beep(523.25,0.07,'square',0.07);setTimeout(function(){beep(659.25,0.07,'square',0.07);},80);setTimeout(function(){beep(783.99,0.12,'square',0.07);},160);"
    if kind == "better":
        return "beep(440,0.08,'square',0.06);setTimeout(function(){beep(554.37,0.1,'square',0.06);},90);"
    if kind == "click":
        return "beep(660,0.045,'square',0.055);"
    return "beep(220,0.12,'sawtooth',0.07);setTimeout(function(){beep(160,0.16,'sawtooth',0.07);},130);"


def play_se(kind: str, key: str):
    """SE再生を予約する。

    Streamlit のボタン処理中に components.html() を直接描画すると、
    画面遷移直後に警告や一瞬のエラー表示が出ることがあるため、
    ここでは session_state に予約だけを入れ、通常描画タイミングで再生する。
    """
    if not st.session_state.get("se_enabled", True):
        return
    if st.session_state.get("last_se_key") == key:
        return
    st.session_state.last_se_key = key
    st.session_state["_queued_se"] = {"kind": kind, "key": key}


def render_queued_se():
    """予約済みSEを通常描画タイミングで1回だけ再生する。"""
    item = st.session_state.pop("_queued_se", None)
    if not item:
        return
    if not st.session_state.get("se_enabled", True):
        return

    kind = item.get("kind", "click")
    se_volume = st.session_state.get("se_volume", 70) / 100.0
    seq = _se_sequence(kind)

    components.html(
        f"""
<!DOCTYPE html>
<html>
<body>
<script>
(function(){{
  var AC = window.AudioContext || window.webkitAudioContext;
  if(!AC) return;
  var ctx = new AC();
  var master = ctx.createGain();
  master.gain.value = {se_volume} * 0.18;
  master.connect(ctx.destination);

  function beep(f,d,type,gainValue){{
    var o=ctx.createOscillator(), g=ctx.createGain();
    o.type=type || "square";
    o.frequency.value=f;
    g.gain.value=(gainValue || 0.05) * {se_volume};
    o.connect(g);
    g.connect(master);
    o.start();
    o.stop(ctx.currentTime+d);
  }}

  {seq}
}})();
</script>
</body>
</html>
""",
        height=0,
    )

def render_timer_widget():
    """サイドバー専用タイマー"""
    if st.session_state.game_over:
        label = "終了"
        remaining = 0
        limit = current_phase_limit()
    elif st.session_state.get("pending_feedback") is not None:
        label = "STOP"
        remaining = remaining_time()
        limit = current_phase_limit()
    elif st.session_state.simulation_started:
        label = f"00:{remaining_time():02d}"
        remaining = remaining_time()
        limit = current_phase_limit()
    else:
        limit = current_phase_limit()
        remaining = limit
        label = "READY"

    percent = int((remaining / limit) * 100) if limit else 0

    st.sidebar.markdown(
        f"""
<div class="timer-big">{label}</div>
<div class="timebar">
  <div class="timebar-fill" style="width:{percent}%;"></div>
</div>
<div style="text-align:center;">フェーズ制限時間：{limit}秒</div>
<div class="sidebar-button">制限時間を超過したため訓練終了</div>
""",
        unsafe_allow_html=True,
    )


def render_sidebar():
    if st.session_state.get("simulation_started", False):
        st.sidebar.markdown('<div class="retro-panel"><div class="panel-title">リスク指標</div>', unsafe_allow_html=True)
        status_row("", "システム感染拡大リスク", st.session_state.infection, "#c62828")
        status_row("", "院内業務混乱リスク", st.session_state.panic, "#f9a825")
        status_row("", "診療継続性", st.session_state.bcp, "#1769aa")
        status_row("", "対外的信頼", st.session_state.trust, "#2e7d32")
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown('<div class="retro-panel"><div class="panel-title">訓練設定</div>', unsafe_allow_html=True)
    diff = st.sidebar.selectbox("難易度", list(DIFFICULTIES.keys()), index=list(DIFFICULTIES.keys()).index(st.session_state.difficulty))
    role = st.sidebar.selectbox("役割", ROLES, index=ROLES.index(st.session_state.role))
    collab_mode = st.sidebar.selectbox(
        "プレイ方式",
        ["個別プレイ", "チームで共有プレイ"],
        index=1 if st.session_state.get("collab_mode") == "チームで共有プレイ" else 0,
        key="collab_mode_input",
    )
    collab_team = st.sidebar.selectbox(
        "共有チーム",
        COLLAB_TEAMS,
        index=COLLAB_TEAMS.index(st.session_state.get("collab_team", COLLAB_TEAMS[0])) if st.session_state.get("collab_team", COLLAB_TEAMS[0]) in COLLAB_TEAMS else 0,
        key="collab_team_input",
        format_func=team_status_label,
    )
    if collab_mode != st.session_state.get("collab_mode") or collab_team != st.session_state.get("collab_team"):
        st.session_state.collab_mode = collab_mode
        st.session_state.collab_team = collab_team
        if shared_play_enabled() and shared_state_exists(collab_team):
            data = load_shared_state(collab_team)
            if data and data.get("simulation_started"):
                import_shared_state(data, keep_identity=True)
        else:
            reset_game()
        # ボタン・選択操作による再描画は Streamlit 標準の実行サイクルに任せる
    if diff != st.session_state.difficulty:
        st.session_state.difficulty = diff
        reset_game()
        # 再描画は標準サイクルに任せる
    if role != st.session_state.role:
        st.session_state.role = role
        reset_game()
        # 再描画は標準サイクルに任せる
    if st.sidebar.button("設定変更・初期化"):
        transition_reset_simulation()
        st.rerun()
    if shared_play_enabled() and not st.session_state.get("simulation_started", False):
        st.sidebar.markdown(f'<div class="sidebar-button">共有：{st.session_state.collab_team}<br>自動同期中 / 1フェーズ +5分</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="sidebar-button">GL6.0観点に基づく評価</div>', unsafe_allow_html=True)
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    if not st.session_state.get("simulation_started", False):
        st.sidebar.markdown('<div class="retro-panel"><div class="panel-title">リスク指標</div>', unsafe_allow_html=True)
        status_row("", "システム感染拡大リスク", st.session_state.infection, "#c62828")
        status_row("", "院内業務混乱リスク", st.session_state.panic, "#f9a825")
        status_row("", "診療継続性", st.session_state.bcp, "#1769aa")
        status_row("", "対外的信頼", st.session_state.trust, "#2e7d32")
        st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown('<div class="retro-panel"><div class="panel-title">フェーズ制限時間</div>', unsafe_allow_html=True)
    render_timer_widget()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown('<div class="retro-panel"><div class="panel-title">音声設定</div>', unsafe_allow_html=True)
    st.session_state.bgm_enabled = st.sidebar.toggle("BGM ON / OFF", value=st.session_state.get("bgm_enabled", True))
    st.session_state.bgm_volume = st.sidebar.slider("BGM音量", 0, 100, st.session_state.bgm_volume, 5)
    st.session_state.se_enabled = st.sidebar.toggle("SE ON / OFF", value=st.session_state.get("se_enabled", True))
    st.session_state.se_volume = st.sidebar.slider("SE音量", 0, 100, st.session_state.se_volume, 5)
    render_audio()
    st.sidebar.markdown("</div>", unsafe_allow_html=True)

    st.sidebar.markdown('<div class="retro-panel"><div class="panel-title">監査ログ</div><div class="log-box">', unsafe_allow_html=True)
    for line in st.session_state.log[-7:]:
        st.sidebar.markdown(f"<div>{line}</div>", unsafe_allow_html=True)
    st.sidebar.markdown("</div></div>", unsafe_allow_html=True)


def render_header():
    if st.session_state.get("simulation_started", False):
        return
    compact = st.session_state.get("simulation_started", False)
    wrapper_class = "compact-header" if compact else ""
    st.markdown(
        f"""
<div class="{wrapper_class}">
<div class="header-grid">
  <div>
    <h1>医療機関サイバーBCP訓練</h1>
    <div class="subtitle">医療機関向けサイバー攻撃対応机上訓練</div>
  </div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_training_purpose():
    st.markdown(
        """
<div class="training-purpose">
  <div class="training-purpose-title">訓練目的</div>
  <div class="training-purpose-text">
    本訓練は、医療機関におけるサイバー攻撃発生時の院内机上訓練として、以下を確認することを目的とします。<br>
    ・初動判断：異常検知後の報告、端末操作停止、感染拡大防止の判断<br>
    ・報告連絡：院内対策本部、ベンダー、関係機関、患者・家族への連絡判断<br>
    ・紙運用：電子カルテ停止時の受付、診療、検査、処方、会計の代替運用<br>
    ・SNS・個人情報対応：画面撮影、投稿、患者情報の写り込み、外部拡散への対応<br>
    ・BCP切替判断：診療制限、救急受入、復旧優先順位、再発防止策の検討<br><br>
    本訓練は、医療情報システムの安全管理に関するガイドライン第6.0版の観点を踏まえた訓練です。<br><br>
【ロール別演習構成】<br>
・管理監督者：対策本部運営、広報、意思決定、BCP判断を中心に15前後の演習イベントを実施します。<br>
・SE：感染調査、ログ確認、隔離、バックアップ、復旧判断を中心に15前後の演習イベントを実施します。<br>
・職員：初動報告、紙運用、患者対応、SNS・情報持出し対応を中心に15前後の演習イベントを実施します。<br>
ロールに応じて、重視されるフェーズ・突発イベントの出現内容が変化します。

  </div>
</div>
""",
        unsafe_allow_html=True,
    )



def transition_start_simulation():
    play_se("click", f"click_start_{time.time()}")
    start_simulation()


def transition_reset_simulation():
    play_se("click", f"click_reset_{time.time()}")
    st.session_state._choice_processing = False
    st.session_state.pending_induced_event = None
    reset_game()
    save_shared_state()


def transition_after_feedback():
    play_se("click", f"click_next_{time.time()}")
    proceed_after_feedback()

def render_start_screen():
    render_training_purpose()
    st.markdown(
        """
<div class="event-box">
  <div class="event-main">
    <div class="event-label">訓練設定</div>
    <div class="event-title">難易度と役割を選択してください</div>
    <div class="event-desc">
      左側の訓練設定パネルで、難易度と役割を選択してください。<br>
      設定後に下のボタンを押すと、PHASE 01から訓練を開始します。<br>
      フェーズ制限時間を超過すると、その時点で訓練終了となります。判断結果は医療情報システムの安全管理に関するガイドライン第6.0版の観点を踏まえてフィードバックされます。
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown(
            f"""
<div class="retro-panel-cyan">
  <div class="phase-title">現在の設定</div>
  <div style="font-size:1rem;line-height:1.9;color:#1f2937;">
    難易度：<strong>{st.session_state.difficulty}</strong><br>
    役割：<strong>{st.session_state.role}</strong><br>
    プレイ方式：<strong>{st.session_state.get("collab_mode", "個別プレイ")}</strong><br>
    共有チーム：<strong>{st.session_state.get("collab_team", "-") if shared_play_enabled() else "-"}</strong>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
        if st.button("訓練を開始する"):
            transition_start_simulation()
            st.rerun()


def render_phase():
    phase = PHASES[st.session_state.phase]
    rem = remaining_time()
    st.markdown(
        f"""
<div class="phase-box">
  <div class="retro-panel-cyan">
    <div class="phase-title">{phase["title"]}</div>
    <div class="phase-text">シーン：{phase["scene"]}</div>
    <div class="phase-text">目的：{phase["objective"]}</div>
    <div class="phase-text" style="color:#5f6b7a;margin-top:0.45rem;font-weight:700;">このフェーズで最も適切と考えられる対応方針を選択してください。</div>
  </div>
  <div class="retro-panel-cyan">
    <div style="color:var(--navy);font-size:1.0rem;font-weight:700;text-align:center;">残り時間</div>
    <div class="timer-big">00:{rem:02d}</div>
    <div class="timebar"><div class="timebar-fill" style="width:{time_percent()}%;"></div></div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_event():
    ev = st.session_state.current_event
    if ev is None:
        return

    if st.session_state.event_expanded:
        st.markdown(
            f"""
<div class="event-box">
  <div class="event-main">
    <div class="event-label">追加対応課題</div>
    <div class="event-title">{ev["title"]}</div>
    <div class="event-desc">{ev["desc"]}</div>
    <div class="event-label" style="font-size:0.9rem;margin-top:0.65rem;">
      この突発事象に対する対応方針を選択してください
    </div>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
<div class="mini-event">
  <div>
    <div style="color:#8f1717;font-size:0.85rem;font-weight:700;">突発事象への対応済み</div>
    <div style="color:#1f2937;font-size:1rem;font-weight:700;">{ev["title"]}</div>
  </div>
  <div style="color:#5f6b7a;font-size:0.85rem;">完了</div>
</div>
""",
            unsafe_allow_html=True,
        )



def current_choice_context_signature() -> dict:
    """選択肢表示時点の文脈を識別するための署名。"""
    mode, obj = get_context()
    return {
        "mode": mode,
        "phase": st.session_state.get("phase"),
        "role": st.session_state.get("role"),
        "event_id": obj.get("id") if mode == "event" else None,
        "event_expanded": bool(st.session_state.get("event_expanded", False)),
    }


def queue_choice(idx: int):
    """ボタン押下時は選択内容だけを記録し、実処理は次の通常実行の先頭で行う。

    Streamlit のボタン callback 内でゲーム状態を大きく変更すると、
    自動更新・共有同期・イベント発生処理と競合して「リスク値だけ更新され、
    フィードバック画面へ入らない」表示になり得るため、ここでは処理しない。
    """
    if st.session_state.get("_choice_processing", False):
        return
    if st.session_state.get("pending_feedback") is not None:
        return
    if not st.session_state.get("simulation_started", False):
        return
    if st.session_state.get("completed", False) or st.session_state.get("game_over", False):
        return
    sig = current_choice_context_signature()
    sig["idx"] = int(idx)
    sig["queued_at"] = time.time()
    st.session_state["_queued_choice"] = sig
    st.session_state["_choice_processing"] = True


def process_queued_choice():
    """予約された選択を、画面分岐より前に1回だけ確定処理する。"""
    queued = st.session_state.pop("_queued_choice", None)
    if not queued:
        return

    # ここからは通常実行コンテキストなので、choose() が状態更新しても
    # この同じ実行内で pending_feedback 分岐へ進める。
    st.session_state["_choice_processing"] = False

    if st.session_state.get("pending_feedback") is not None:
        return
    if not st.session_state.get("simulation_started", False):
        return
    if st.session_state.get("completed", False) or st.session_state.get("game_over", False):
        return

    current = current_choice_context_signature()
    expected = {k: queued.get(k) for k in ["mode", "phase", "role", "event_id", "event_expanded"]}
    actual = {k: current.get(k) for k in ["mode", "phase", "role", "event_id", "event_expanded"]}
    if expected != actual:
        st.session_state.setdefault("log", []).append("[WARN] 選択時点と現在の画面状態が異なるため選択を破棄")
        save_shared_state()
        return

    choose(int(queued.get("idx", -1)))

def render_choices():
    """選択肢タイルを描画する。

    on_click callback は使わず、ボタン押下を通常の実行コンテキストで処理する。
    これにより `Calling st.rerun() within a callback is a no-op.` を避けつつ、
    選択後は必ず評価画面へ即時遷移させる。
    """
    choices = get_current_choices()
    processing = bool(st.session_state.get("_choice_processing", False))

    cols = st.columns(3)
    for i, (text, quality) in enumerate(choices):
        with cols[i % 3]:
            key_event = st.session_state.get("current_event", {}).get("id", "phase") if st.session_state.get("current_event") else "phase"
            clicked = st.button(
                f"{i+1}. {text}",
                key=f"choice_{st.session_state.phase}_{st.session_state.role}_{i}_{key_event}",
                disabled=processing,
            )
            if clicked:
                # 即時に二重押下を抑止し、状態更新後に通常の rerun を行う。
                # callback 内ではないため Streamlit の no-op 警告は出ない。
                st.session_state["_choice_processing"] = False
                choose(i)
                save_shared_state()
                st.rerun()

def render_feedback():
    fb = st.session_state.pending_feedback
    if fb is None:
        return

    quality = fb.get("quality", "BAD")
    if quality == "BEST":
        css = "feedback-best"
        icon = ""
        color = "#2e7d32"
    elif quality == "BETTER":
        css = "feedback-better"
        icon = ""
        color = "#f9a825"
    else:
        css = "feedback-bad"
        icon = ""
        color = "#c62828"

    if st.session_state.game_over:
        icon = ""
        color = "#c62828"

    st.markdown(
        f"""
<div class="{css}">
  <div class="feedback-title" style="color:{color};">評価：{fb["result"]}</div>
  <div class="feedback-text">
    <strong>選択：</strong>{fb["choice"]}<br><br>
    <strong>フィードバック：</strong>{fb["feedback"]}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    if st.session_state.game_over:
        render_history_download()
        if st.button("もう一度訓練を実施する"):
            transition_reset_simulation()
            st.rerun()
        return

    if fb["mode"] == "event":
        button_label = "突発イベントへの対応を完了し、フェーズへ戻る"
    else:
        button_label = "次のフェーズに進む"

    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        if st.button(button_label):
            transition_after_feedback()
            save_shared_state()
            st.rerun()

def render_game_over():
    play_se("gameover", f"gameover_screen_{len(st.session_state.history)}")
    st.markdown(
        """
<div class="feedback-bad">
  <div class="feedback-title" style="color:#c62828;">訓練終了</div>
  <div class="feedback-text">
    制限時間を超過したため訓練終了となりました。<br>
    インシデント対応では、判断遅延そのものが感染拡大・医療安全リスク・信用低下につながります。
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    render_history_download()
    render_review_questions()
    if st.button("もう一度訓練を実施する"):
        transition_reset_simulation()
        st.rerun()


def render_history_download():
    if not st.session_state.history:
        return
    df = pd.DataFrame(st.session_state.history)
    st.download_button(
        "訓練結果をCSV形式でダウンロード",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="medical_cyber_bcp_choices_feedback.csv",
        mime="text/csv",
    )
    st.dataframe(df, use_container_width=True, height=260)


def render_review_questions():
    questions = [
        "1. 初動判断で迷った点は何でしたか。端末操作停止、報告、隔離判断は適切でしたか。",
        "2. 判断や報告が遅れた場面があった場合、その理由は何でしたか。",
        "3. 院内対策本部、情報担当、ベンダー、警察、自治体、監督官庁などの連絡先に不足はありませんでしたか。",
        "4. 電子カルテ停止時の紙運用で、実際に不足しそうな様式・帳票・物品は何でしたか。",
        "5. 紙運用中の本人確認、処方、検査、会計、転記ミス防止の手順は十分でしたか。",
        "6. SNS投稿、画面撮影、患者情報の写り込みに対する職員教育・周知は十分でしたか。",
        "7. 患者・家族・報道機関への説明文や問い合わせ窓口は、実際に運用できる内容でしたか。",
        "8. バックアップ確認、復旧優先順位、再感染防止の判断に不足はありませんでしたか。",
        "9. 今回の訓練結果を踏まえ、院内BCP、情報セキュリティ手順、教育研修で見直すべき点は何ですか。",
        "10. 次回訓練までに、誰が、いつまでに、何を改善する必要がありますか。",
    ]

    st.markdown(
        """
<div class="review-box">
  <div class="phase-title">講評・振り返り設問</div>
  <div class="training-purpose-text">
    以下の設問をもとに、訓練後の講評・振り返りを行ってください。
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    for q in questions:
        st.markdown(f'<div class="review-question">{q}</div>', unsafe_allow_html=True)

    review_df = pd.DataFrame({
        "no": list(range(1, len(questions) + 1)),
        "review_question": questions,
        "comment": ["" for _ in questions],
        "responsible_department": ["" for _ in questions],
        "due_date": ["" for _ in questions],
    })

    st.download_button(
        "振り返りシートをCSV形式でダウンロード",
        data=review_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="medical_cyber_bcp_review_questions.csv",
        mime="text/csv",
    )


def render_clear():
    play_se("best", f"clear_{len(st.session_state.history)}")
    score = st.session_state.bcp + st.session_state.trust - st.session_state.infection - st.session_state.panic
    max_score = 200
    st.markdown(
        f"""
<div class="event-box" style="border-left-color:#2e7d32;background:#f5fbf6;border-color:#bbd7bd;">
  <div class="event-main">
    <div class="event-label" style="color:#2e7d32;">訓練完了</div>
    <div class="event-title" style="color:#1b5e20;">総合防御スコア：{score} / {max_score}</div>
    <div class="event-desc">訓練結果とフィードバックをCSVで保存し、院内BCP訓練の振り返りに活用してください。</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    render_history_download()
    render_review_questions()
    if st.button("もう一度訓練を実施する"):
        transition_reset_simulation()
        st.rerun()



def apply_runtime_background():
    if not (
        st.session_state.get("simulation_started", False)
        and st.session_state.get("current_event") is not None
        and st.session_state.get("event_expanded", False)
        and st.session_state.get("pending_feedback") is None
        and not st.session_state.get("game_over", False)
    ):
        return

    current_event = st.session_state.get("current_event")
    image_path = event_image_path(current_event)

    if image_path:
        image_uri = image_file_to_data_uri(image_path)
        st.markdown(
            f"""
<style>
.stApp {{
    background-image:
        linear-gradient(90deg, rgba(255,241,241,0.98) 0%, rgba(255,241,241,0.93) 42%, rgba(255,241,241,0.72) 100%),
        url('{image_uri}') !important;
    background-position: center center, right 3vw center !important;
    background-size: cover, min(44vw, 680px) auto !important;
    background-repeat: no-repeat, no-repeat !important;
    background-attachment: fixed, fixed !important;
}}
.block-container {{
    background: linear-gradient(180deg, rgba(255,241,241,0.90), rgba(243,246,250,0.88));
    border-radius: 16px;
}}
.event-box {{
    background: rgba(255,232,232,0.94) !important;
    border-color: #d32f2f !important;
    border-left-color: #b71c1c !important;
    box-shadow: 0 12px 28px rgba(198,40,40,0.18) !important;
}}
.retro-panel-cyan, .feedback-best, .feedback-better, .feedback-bad, .training-purpose, .review-box {{
    background-color: rgba(255,255,255,0.94) !important;
}}
@media (max-width: 900px) {{
    .stApp {{
        background-position: center center, center bottom !important;
        background-size: cover, 78vw auto !important;
    }}
}}
</style>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
<style>
.stApp { background: #fff1f1 !important; }
.block-container { background: linear-gradient(180deg, rgba(255,241,241,0.96), rgba(243,246,250,0.96)); }
.event-box {
    background: #ffe8e8 !important;
    border-color: #d32f2f !important;
    border-left-color: #b71c1c !important;
    box-shadow: 0 12px 28px rgba(198,40,40,0.14) !important;
}
</style>
""",
            unsafe_allow_html=True,
        )

# ============================================================
# Main
# ============================================================

init_state()
ensure_state_integrity()
restore_shared_state_from_query()
ensure_state_integrity()
# キュー方式は使わない。ボタン押下時に通常コンテキストで直接処理する。

if st.session_state.pop("_skip_shared_sync_once", False):
    pass
elif not st.session_state.get("_choice_processing", False):
    sync_shared_state_from_file()
ensure_state_integrity()

if (
    st.session_state.get("simulation_started", False)
    and not st.session_state.get("completed", False)
    and not st.session_state.get("game_over", False)
    and not st.session_state.get("_choice_processing", False)
):
    # 共有プレイではフィードバック画面中も自動更新し、他端末の遷移を強制同期する。
    # 個別プレイでは従来どおりフィードバック中はタイマー更新しない。
    if st.session_state.pending_feedback is None or shared_play_enabled():
        auto_refresh(1)

if not st.session_state.get("_choice_processing", False):
    maybe_random_event()
check_timeout()
check_status_game_over()
apply_runtime_background()
render_sidebar()
render_queued_se()
render_header()
render_shared_status()

if not st.session_state.get("simulation_started", False):
    render_start_screen()
elif st.session_state.get("pending_feedback") is not None:
    phase_now = st.session_state.phase + 1
    total = len(PHASES)
    st.progress(phase_now / total)
    render_feedback()
elif st.session_state.get("game_over", False):
    render_game_over()
elif st.session_state.get("completed", False):
    render_clear()
else:
    phase_now = st.session_state.phase + 1
    total = len(PHASES)
    st.markdown('<div style="margin-top:-0.2rem;"></div>', unsafe_allow_html=True)
    st.progress(phase_now / total)
    st.markdown(
        f'<div style="color:#1f2937;margin:0.25rem 0;font-weight:700;">PHASE {phase_now:02d} / {total:02d}　役割：{st.session_state.role}　難易度：{st.session_state.difficulty}</div>',
        unsafe_allow_html=True,
    )
    render_phase()
    render_event()
    render_choices()
