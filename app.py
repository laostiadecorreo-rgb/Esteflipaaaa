"""
OS v2.0 — Poker Operating System  |  Streamlit App
v2.05-fix2: Plotly 6 fix + M4 Coach + SunChat + Progresión + Drill Guiado + Hole Cards
"""

import streamlit as st
import tempfile, os, sys, io, json, math
from pathlib import Path

st.set_page_config(page_title="OS v2.0 — Poker OS", page_icon="♠",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.os-header{background:linear-gradient(135deg,#0a0a0a 0%,#1a1a2e 100%);border:1px solid #2d2d4e;border-radius:12px;padding:24px 32px;margin-bottom:24px;display:flex;align-items:center;gap:16px;}
.os-header h1{font-family:'JetBrains Mono',monospace;font-size:1.8rem;font-weight:700;color:#e8e8f0;margin:0;letter-spacing:-0.5px;}
.os-header .subtitle{font-size:0.85rem;color:#6b6b8a;margin:4px 0 0 0;}
.os-badge{background:#1e3a5f;color:#60a5fa;font-family:'JetBrains Mono',monospace;font-size:0.75rem;padding:4px 10px;border-radius:20px;border:1px solid #2d5a8e;white-space:nowrap;}
.metric-card{background:#0f0f1a;border:1px solid #1e1e3a;border-radius:10px;padding:16px 20px;transition:border-color .2s;}
.metric-card:hover{border-color:#3d3d6e;}
.metric-label{font-size:.75rem;font-weight:500;color:#6b6b8a;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px;}
.metric-value{font-family:'JetBrains Mono',monospace;font-size:1.6rem;font-weight:700;line-height:1;}
.metric-value.green{color:#22c55e;}.metric-value.red{color:#ef4444;}.metric-value.yellow{color:#f59e0b;}.metric-value.neutral{color:#e8e8f0;}
.metric-sub{font-size:.78rem;color:#4b4b6a;margin-top:4px;}
.section-title{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:600;color:#4b4b8a;text-transform:uppercase;letter-spacing:.12em;border-bottom:1px solid #1e1e3a;padding-bottom:8px;margin:24px 0 16px 0;}
.leak-row{background:#0f0f1a;border-left:3px solid #ef4444;border-radius:0 8px 8px 0;padding:12px 16px;margin-bottom:8px;font-family:'JetBrains Mono',monospace;font-size:.82rem;}
.opp-row{background:#0f1a0f;border-left:3px solid #22c55e;border-radius:0 8px 8px 0;padding:12px 16px;margin-bottom:8px;font-family:'JetBrains Mono',monospace;font-size:.82rem;}
.leak-spot{color:#a78bfa;font-weight:600;}.leak-ev{color:#ef4444;float:right;}.opp-ev{color:#22c55e;float:right;}.leak-meta{color:#4b4b6a;font-size:.75rem;margin-top:4px;}
.drill-card{background:linear-gradient(135deg,#0f1629 0%,#0a0f1e 100%);border:1px solid #1e3a5f;border-radius:12px;padding:20px 24px;}
.drill-title{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#60a5fa;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px;}
.drill-spot{font-family:'JetBrains Mono',monospace;font-size:1rem;color:#e8e8f0;font-weight:600;margin-bottom:12px;}
.drill-trigger{font-size:.85rem;color:#94a3b8;margin-bottom:6px;}.drill-action{font-size:.85rem;color:#22c55e;font-weight:500;}
.progress-container{background:#1e1e3a;border-radius:4px;height:6px;margin:8px 0;overflow:hidden;}
.progress-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,#3b82f6,#8b5cf6);}
.exploit-row{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-radius:6px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;font-size:.8rem;}
.exploit-red{background:#1a0f0f;border-left:2px solid #ef4444;}.exploit-yellow{background:#1a160a;border-left:2px solid #f59e0b;}.exploit-green{background:#0a1a0f;border-left:2px solid #22c55e;}
.session-row{display:flex;gap:8px;align-items:center;padding:6px 10px;border-radius:6px;margin-bottom:3px;font-family:'JetBrains Mono',monospace;font-size:.78rem;background:#0a0a14;border:1px solid #15152a;}
.coach-box{background:#0a0f1e;border:1px solid #1e3a5f;border-radius:10px;padding:16px 20px;font-size:.85rem;color:#94a3b8;line-height:1.6;}
.coach-box b{color:#60a5fa;}
section[data-testid="stSidebar"]{background:#05050f;border-right:1px solid #1e1e3a;}
.main .block-container{padding-top:1rem;}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# CARGA LIBRERÍA
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="Cargando OS v2.0...")
def load_os_library():
    import unittest.mock as mock
    import pandas as pd, numpy as np, random, sqlite3
    from datetime import datetime, timedelta
    g = {'pd':pd,'np':np,'random':random,'datetime':datetime,'timedelta':timedelta,
         'sqlite3':sqlite3,'__builtins__':__builtins__}
    sys.modules['google']       = mock.MagicMock()
    sys.modules['google.colab'] = mock.MagicMock()
    lib_path = Path(__file__).parent / 'os_library.py'
    if not lib_path.exists():
        return None, "❌ os_library.py no encontrado."
    try:
        exec(open(lib_path, encoding='utf-8').read(), g)
        return g, None
    except Exception as e:
        return None, f"❌ Error cargando librería: {e}"


# ══════════════════════════════════════════════════════════════════════════════
# PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
def run_pipeline(hh_path, friccion_r, friccion_a, friccion_v, num_tables, hero_name, g):
    import pandas as pd

    parse_fn = g.get('parse_real_hand_history_file')
    if not parse_fn:
        return None, "❌ Parser no disponible."

    df = parse_fn(hh_path, hero=hero_name)
    if df.empty:
        return None, "❌ No se encontraron manos cash."

    for fn_name in ['enrich_df_with_board_texture', 'build_spot_identifier']:
        if fn_name in g:
            df = g[fn_name](df)

    current_session_id = df['session_id'].iloc[-1] if 'session_id' in df.columns else 'session_001'
    mask = df['session_id'] == current_session_id
    for col, val in [('friccion_r', friccion_r), ('friccion_a', friccion_a), ('friccion_v', friccion_v)]:
        df.loc[mask, col] = val
    df['num_tables'] = num_tables

    if 'classify_opponent_pool' in g:
        try: _, df = g['classify_opponent_pool'](df, hero=hero_name)
        except: df['opp_class'] = 'unknown'

    overall_metrics, spot_results = {}, pd.DataFrame()
    if 'calculate_ev_metrics' in g:
        overall_metrics, spot_results = g['calculate_ev_metrics'](df, current_session_id=current_session_id)

    hand_count = len(df)

    friccion_avg = round((friccion_r + friccion_a + friccion_v) / 3, 2)
    if 'calculate_friccion_avg' in g:
        try:
            fa = g['calculate_friccion_avg'](df)
            if fa is not None and not math.isnan(float(fa)):
                friccion_avg = float(fa)
        except: pass

    current_mode = 'M1'
    if 'determine_operating_mode' in g:
        current_mode = g['determine_operating_mode'](overall_metrics, friccion_avg, hand_count)

    roi_ranking = {}
    if 'build_roi_ranking' in g and not spot_results.empty:
        roi_ranking = g['build_roi_ranking'](spot_results, top_n=10)

    m5_result = {}
    if 'run_m5_pool_detector' in g:
        try: m5_result = g['run_m5_pool_detector'](df, hand_count=hand_count)
        except: pass

    tilt_result = {}
    if 'detect_tilt_sessions' in g:
        try: tilt_result = g['detect_tilt_sessions'](df)
        except: pass

    speed_result = {}
    if 'estimate_preflop_speed' in g:
        try: speed_result = g['estimate_preflop_speed'](df, num_tables=num_tables)
        except: pass

    # Progression metrics
    progression = []
    if 'calculate_progression_metrics' in g:
        try: progression = g['calculate_progression_metrics'](df)
        except: pass

    # Build leak object for M4/SunChat
    leak_object = None
    if 'build_leak_object_from_roi' in g and roi_ranking:
        try: leak_object = g['build_leak_object_from_roi'](roi_ranking, df, top_n=1)
        except: pass

    # ── drill activo para bridge (top leak del ROI ranking) ──────────────────
    leaks_pipeline = []
    if roi_ranking and isinstance(roi_ranking, dict) and 'ranking' in roi_ranking:
        leaks_pipeline = roi_ranking['ranking']
    elif roi_ranking and isinstance(roi_ranking, list):
        leaks_pipeline = roi_ranking
    drill_activo_pipeline = leaks_pipeline[0]['spot_identifier'] if leaks_pipeline else None

    # ── execution rate del drill activo ──────────────────────────────────────
    execution_rate_result = {}
    if 'calculate_execution_rate' in g and drill_activo_pipeline:
        try:
            execution_rate_result = g['calculate_execution_rate'](
                df, drill_activo_pipeline,
                drill_start_session=current_session_id
            ) or {}
        except Exception as _er:
            execution_rate_result = {}

    # ── after_session_bridge: detecta errores de ejecución del drill ─────────
    bridge_result = {}
    if 'after_session_bridge' in g and drill_activo_pipeline:
        try:
            import io as _io, sys as _sys
            _buf = _io.StringIO()
            _old_stdout = _sys.stdout
            _old_stdin  = _sys.stdin
            _sys.stdout = _buf
            # Redirect stdin so input() calls devuelven '' sin bloquear
            import unittest.mock as _mock
            with _mock.patch('builtins.input', return_value=''):
                bridge_result = g['after_session_bridge'](
                    df, drill_activo=drill_activo_pipeline,
                    session_id=current_session_id,
                    interactive=False   # v2.20: suppress prompts in Streamlit
                ) or {}
            _sys.stdout = _old_stdout
        except Exception as _be:
            bridge_result = {'error': str(_be)[:200]}

    sess_df = df[df['session_id'] == current_session_id]

    # ── v2.14: EV por acción ──────────────────────────────────────────────────
    ev_by_action = {}
    action_leak_rank = []
    if 'calculate_ev_by_action' in g:
        try: ev_by_action = g['calculate_ev_by_action'](df) or {}
        except Exception: pass
    if ev_by_action and 'build_action_leak_ranking' in g:
        try: action_leak_rank = g['build_action_leak_ranking'](ev_by_action) or []
        except Exception: pass

    # ── MDF analysis (v2.14) ──────────────────────────────────────────────────
    mdf_result = {}
    if 'calculate_mdf_analysis' in g:
        try: mdf_result = g['calculate_mdf_analysis'](df) or {}
        except Exception: pass

    # ── v2.14: M0 basic triggers ──────────────────────────────────────────────
    m0_triggers = {}
    if 'implement_m0_basic_triggers' in g and overall_metrics:
        try:
            _hist_ev = g['generate_historical_ev_h_per_week'](df) if 'generate_historical_ev_h_per_week' in g else []
            m0_triggers = g['implement_m0_basic_triggers'](overall_metrics, friccion_avg, _hist_ev) or {}
        except Exception: pass

    return {
        'df': df, 'overall_metrics': overall_metrics,
        'spot_results': spot_results, 'roi_ranking': roi_ranking,
        'm5_result': m5_result, 'tilt_result': tilt_result,
        'current_mode': current_mode, 'current_session_id': current_session_id,
        'session_net': sess_df['net_won'].sum() if 'net_won' in sess_df.columns else 0,
        'session_hands': len(sess_df),
        'hand_count': hand_count, 'friccion_avg': friccion_avg,
        'speed_result': speed_result, 'progression': progression,
        'leak_object': leak_object, 'bridge_result': bridge_result,
        'execution_rate_result': execution_rate_result,
        'ev_by_action': ev_by_action, 'action_leak_rank': action_leak_rank,
        'mdf_result': mdf_result, 'm0_triggers': m0_triggers, 'g': g,
    }, None


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def cc(val, pos=True):
    try:
        v = float(val)
        if pos: return 'green' if v>0 else ('red' if v<0 else 'neutral')
        else:   return 'red'   if v>0 else ('green' if v<0 else 'neutral')
    except: return 'neutral'

def fbb(v):
    try: v=float(v); return f"{'+' if v>0 else ''}{v:.1f}"
    except: return 'N/A'

def fevh(v):
    try: v=float(v); return f"{'+' if v>0 else ''}{v:.2f}€/h"
    except: return 'N/A'

def card(label, value, sub, color_cls, extra_style=""):
    return f"""<div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color_cls}" {extra_style}>{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>"""

def _df_to_rows(df_or_none):
    """FIX: DataFrames from build_roi_ranking — never eval as bool. Normalize cols."""
    import pandas as pd
    if df_or_none is None or not isinstance(df_or_none, pd.DataFrame) or df_or_none.empty:
        return []
    rows = []
    for _, r in df_or_none.iterrows():
        rows.append({
            'spot_identifier': r.get('spot_identifier', '?'),
            'ev_shrunk':       float(r.get('impacto_ev_total_eur_shrunk', 0)),
            'n':               int(r.get('spot_hands_count', 0)),
            'ip_oop':          r.get('ip_oop', ''),
            'pot_type':        r.get('pot_type', ''),
            'stack_depth':     r.get('stack_depth', ''),
            'decision_street': r.get('decision_street', ''),
            'tipo':            r.get('tipo', ''),
            'prioridad':       int(r.get('prioridad', 99)),
        })
    return rows

def _fam_to_rows(fd):
    if not fd or not isinstance(fd, dict): return []
    rows = [{'family':k,'ev_total':float(v.get('ev_combined',0)),
             'n_hands':int(v.get('n_combined',0)),'description':v.get('descripcion',''),
             'icon':v.get('icon','⚪'),'n_spots':int(v.get('n_spots',0))}
            for k,v in fd.items()]
    rows.sort(key=lambda x: x['ev_total'])
    return rows

def _safe_capture(fn, *args, **kwargs):
    """Run OS display function capturing stdout → return as string."""
    buf = io.StringIO()
    try:
        old = sys.stdout; sys.stdout = buf
        fn(*args, **kwargs)
        sys.stdout = old
    except Exception as e:
        sys.stdout = old
        return f"⚠️ {e}"
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# HEADER + SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""<div class="os-header">
    <div><h1>♠ OS v2.0</h1>
    <p class="subtitle">Poker Operating System · LaRuinaDeMago · NL2</p></div>
    <span class="os-badge">v2.05</span>
</div>""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Sesión")
    hero_name = st.text_input("Nick PokerStars", value="LaRuinaDeMago")
    st.markdown("---")
    st.markdown("**🎚️ Fricción** *(1=nada · 5=mucho)*")
    friccion_r = st.slider("🔴 Rabia",    1, 5, 2)
    friccion_a = st.slider("🟠 Ansiedad", 1, 5, 1)
    friccion_v = st.slider("🟡 Varianza", 1, 5, 2)
    fa = round((friccion_r+friccion_a+friccion_v)/3, 2)
    fc = "#22c55e" if fa<=2 else ("#f59e0b" if fa<=3 else "#ef4444")
    fl = "🟢 VERDE" if fa<=2 else ("🟡 AMARILLO" if fa<=3 else "🔴 STOP")
    st.markdown(f"""<div style="background:#0f0f1a;border-radius:8px;padding:10px 14px;margin-top:8px;
        border:1px solid #1e1e3a;font-family:'JetBrains Mono',monospace;font-size:.85rem;">
        Promedio: <span style="color:{fc};font-weight:700;">{fa:.2f}</span>
        <span style="color:#4b4b6a;margin-left:8px;">{fl}</span></div>""", unsafe_allow_html=True)
    st.markdown("---")
    num_tables = st.selectbox("🎮 Mesas", [1, 2, 3, 4], index=1)
    st.markdown("---")

    # M4 / SunChat API keys
    with st.expander("🤖 IA Coach (opcional)"):
        gemini_key = st.text_input("GEMINI_API_KEY", type="password",
                                    help="Gemini 2.0 Flash — gratuito")
        groq_key   = st.text_input("GROQ_API_KEY",   type="password",
                                    help="Groq Llama-3.3-70B — gratuito")
        m4_enabled = st.checkbox("Activar M4.4 Coach", value=bool(gemini_key))
        sc_enabled = st.checkbox("Activar SunChat", value=bool(groq_key))

    st.markdown("---")
    st.markdown("**📂 Hand History**")
    uploaded_file = st.file_uploader("Sube tu .txt de PokerStars", type=['txt'])
    run_btn = st.button("▶ Ejecutar análisis", type="primary",
                        use_container_width=True, disabled=uploaded_file is None)

for k in ['results','error','m4_output','sunchat_msgs']:
    if k not in st.session_state:
        st.session_state[k] = None if k != 'sunchat_msgs' else []

# ── SM-2 / Estudio session state ─────────────────────────────────────────────
# sm2_levels  : {drill_id: 'level_1'|'level_2'|'level_3'}
# sm2_q_state : estado de la pregunta activa durante run_reasoning_session
#               {'drill','level','questions',[idx],'phase':'question'|'answer'|'done'}
# sm2_lu_state: estado del level-up test activo
#               {'drill','level_key','questions','answers':{},'phase':'q'|'result'}
for k, default in [('sm2_levels', {}), ('sm2_q_state', None), ('sm2_lu_state', None)]:
    if k not in st.session_state:
        st.session_state[k] = default

g, lib_error = load_os_library()
if lib_error: st.error(lib_error); st.stop()

if run_btn and uploaded_file:
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='wb') as tmp:
        tmp.write(uploaded_file.read()); tmp_path = tmp.name
    with st.spinner("Analizando manos..."):
        results, err = run_pipeline(tmp_path, friccion_r, friccion_a, friccion_v,
                                    num_tables, hero_name, g)
    os.unlink(tmp_path)
    if err:
        st.session_state.error = err; st.session_state.results = None
    else:
        st.session_state.results = results
        st.session_state.error   = None
        st.session_state.m4_output    = None
        st.session_state.sunchat_msgs = []

if st.session_state.error: st.error(st.session_state.error)

if st.session_state.results is None:
    st.markdown("""<div style="text-align:center;padding:60px 20px;color:#3d3d6e;">
        <div style="font-size:3rem;margin-bottom:16px;">♠</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:1rem;color:#4b4b8a;">
            Sube tu .txt de PokerStars y pulsa Ejecutar análisis</div>
        <div style="font-size:.8rem;color:#2d2d4e;margin-top:8px;">
            PokerStars → Historial de manos → Exportar</div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ──────────────────────────────────────────────────────────────────────────────
R = st.session_state.results
om, df, roi, m5 = R['overall_metrics'], R['df'], R['roi_ranking'], R['m5_result']
hand_count = R['hand_count']

leaks_list    = _df_to_rows(roi.get('leaks')         if roi else None)
opps_list     = _df_to_rows(roi.get('oportunidades') if roi else None)
families_list = _fam_to_rows(roi.get('families', {}) if roi else {})

# ══════════════════════════════════════════════════════════════════════════════
# KPIs PRINCIPALES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Métricas globales</div>', unsafe_allow_html=True)

bb100     = om.get('bb_per_100_net', 0)
evh       = om.get('ev_euro_per_hour', 0)   # FIX: clave correcta
total_net = df['net_won'].sum() if 'net_won' in df.columns else 0
sess_net  = R['session_net']
n_sess    = df['session_id'].nunique() if 'session_id' in df.columns else 1
speed     = R['speed_result'].get('hands_per_hour', 0)
mode      = R['current_mode']

c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: st.markdown(card("BB/100 global",  fbb(bb100),              f"{hand_count:,} manos",   cc(bb100)), unsafe_allow_html=True)
with c2: st.markdown(card("EV €/hora",      fevh(evh),               f"{n_sess} sesiones",       cc(evh)),  unsafe_allow_html=True)
with c3: st.markdown(card("Net total",      f"{'+' if total_net>=0 else ''}{total_net:.2f}€", "acumulado", cc(total_net)), unsafe_allow_html=True)
with c4: st.markdown(card("Sesión actual",  f"{'+' if sess_net>=0 else ''}{sess_net:.2f}€",   f"{R['session_hands']} manos", cc(sess_net)), unsafe_allow_html=True)
with c5:
    sp_c = 'green' if 70<=speed<=110 else ('yellow' if speed>0 else 'neutral')
    st.markdown(card("Velocidad", f"{speed:.0f}", "manos/hora", sp_c), unsafe_allow_html=True)
with c6:
    mc = {'M1':'#60a5fa','M2':'#a78bfa','M3':'#22c55e'}.get(mode,'#6b6b8a')
    st.markdown(card("Modo OS", mode, f"fricción {R['friccion_avg']:.2f}", "neutral",
                     f'style="color:{mc};"'), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

pct_m2 = min(hand_count/30000*100, 100)
st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;border-radius:10px;
    padding:14px 18px;margin-bottom:20px;">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#4b4b8a;
            text-transform:uppercase;letter-spacing:.1em;">Progreso → M2</span>
        <span style="font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#60a5fa;">
            {hand_count:,} / 30,000 — {pct_m2:.1f}%</span>
    </div>
    <div class="progress-container"><div class="progress-fill" style="width:{pct_m2}%;"></div></div>
    <div style="font-size:.75rem;color:#3d3d6e;margin-top:4px;">Gate M2: ≥30k manos + BB/100 > 0 + EV/h > 0 + fricción ≤ 2</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9 = st.tabs([
    "🎯 Drill", "📉 Leaks & ROI", "🌊 Pool M5",
    "📈 Sesiones", "📊 Progresión", "🔢 Stats",
    "🤖 M4 Coach", "💬 SunChat", "🧠 Estudio SM-2",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DRILL ACTIVO
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    drill_activo = leaks_list[0]['spot_identifier'] if leaks_list else None

    # ── Dashboard dinámico (v2.14) — resumen M0/M1/M2/M3 con study tasks ─────
    if 'display_dynamic_dashboard' in g and not R['spot_results'].empty:
        try:
            _study_tasks_dyn = []
            if 'develop_canalized_study_module_logic' in g:
                _tr = g['develop_canalized_study_module_logic'](
                    R['spot_results'], mode, roi_ranking=roi)
                if _tr and 'tasks' in _tr: _study_tasks_dyn = _tr['tasks']
            out = _safe_capture(
                g['display_dynamic_dashboard'],
                R['overall_metrics'], R['spot_results'], mode,
                _study_tasks_dyn, R.get('m0_triggers', {}), roi=roi,
            )
            if out.strip():
                with st.expander("📊 Dashboard dinámico", expanded=False):
                    st.code(out.strip(), language=None)
        except Exception: pass

    # ── Study brief del spot activo (v2.14) ───────────────────────────────────
    if drill_activo and 'generate_study_brief' in g:
        try:
            out = _safe_capture(g['generate_study_brief'],
                                df, drill_activo, R['overall_metrics'])
            if out.strip():
                with st.expander("📖 Study brief del spot"):
                    st.code(out.strip(), language=None)
        except Exception: pass

    # ── Briefing pre-sesión (v2.14) ───────────────────────────────────────────
    if 'display_briefing_clean' in g:
        try:
            drill_plan_brief = None
            if 'recommend_drill_plan' in g and not R['spot_results'].empty:
                try:
                    drill_plan_brief = g['recommend_drill_plan'](
                        df, R['spot_results'], R['overall_metrics'],
                        R['roi_ranking'], drill_activo=drill_activo
                    )
                except Exception: pass
            out = _safe_capture(
                g['display_briefing_clean'],
                overall_metrics=R['overall_metrics'],
                drill_activo=drill_activo,
                drill_plan=drill_plan_brief,
                hand_count=hand_count,
                mode=mode,
            )
            if out.strip():
                with st.expander("📋 Briefing pre-sesión", expanded=True):
                    st.code(out.strip(), language=None)
        except Exception as _e:
            pass  # briefing silently skipped if error

    # ── Session commitment (v2.14) ────────────────────────────────────────────
    if 'display_session_commitment' in g:
        out = _safe_capture(g['display_session_commitment'], df,
                            session_id=current_session_id)
        if out.strip():
            with st.expander("🎯 Compromiso de sesión"):
                st.code(out.strip(), language=None)

    col_d1, col_d2 = st.columns([3,2])

    with col_d1:
        st.markdown('<div class="section-title">🎯 Drill activo</div>', unsafe_allow_html=True)
        if drill_activo:
            registry   = g.get('DRILL_REGISTRY', {})
            drill_data = (registry or {}).get(drill_activo, {})
            trigger = drill_data.get('trigger','Detectado por ROI ranking')
            action  = drill_data.get('action', 'Ver leaks para instrucción')
            level   = drill_data.get('level',  'level_1')
            st.markdown(f"""<div class="drill-card">
                <div class="drill-title">🎯 Drill primario — {level}</div>
                <div class="drill-spot">{drill_activo}</div>
                <div class="drill-trigger"><b>Trigger:</b> {trigger}</div>
                <div class="drill-action"><b>Acción:</b> {action}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Sin drill activo — acumula más manos para señal.")

        # Drill guiado — manos representativas
        if drill_activo and 'get_representative_hands' in g:
            st.markdown('<div class="section-title">📋 Manos representativas del spot</div>', unsafe_allow_html=True)
            try:
                rep_df = g['get_representative_hands'](df, drill_activo, top_n=5)
                if not rep_df.empty:
                    for _, hrow in rep_df.head(5).iterrows():
                        date_s  = str(hrow.get('date',''))[:10]
                        hole    = hrow.get('hole_cards','??')
                        flop    = hrow.get('board_cards_flop','') or '—'
                        pf_act  = hrow.get('preflop_action','?')
                        net_h   = float(hrow.get('net_won',0))
                        ev_h    = float(hrow.get('ev_won',0))
                        nc      = '#22c55e' if net_h>=0 else '#ef4444'
                        st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;
                            border-radius:8px;padding:8px 12px;margin-bottom:4px;
                            font-family:'JetBrains Mono',monospace;font-size:.78rem;">
                            <span style="color:#a78bfa;">{hole}</span>
                            <span style="color:#6b6b8a;margin-left:8px;">Flop: {flop}</span>
                            <span style="color:#94a3b8;margin-left:8px;">PF: {pf_act}</span>
                            <span style="color:{nc};float:right;">
                                {'+' if net_h>=0 else ''}{net_h:.3f}€ (EV {'+' if ev_h>=0 else ''}{ev_h:.3f}€)
                            </span>
                            <div style="color:#3d3d5e;font-size:.72rem;">{date_s}</div>
                        </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.caption(f"Drill hands: {e}")

        # Drill con rangos visuales (v2.14)
        if drill_activo and 'display_drill_with_ranges' in g:
            st.markdown('<div class="section-title">🎯 Drill con rangos</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_drill_with_ranges'], df, drill_activo)
            if out.strip(): st.code(out.strip(), language=None)

        # EV por calle del drill activo (v2.14)
        if 'display_ev_by_street' in g:
            st.markdown('<div class="section-title">📊 EV por calle</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_ev_by_street'], df,
                                position=drill_activo.split('_')[0] if drill_activo else None)
            if out.strip(): st.code(out.strip(), language=None)

        # Drill SB con rangos (v2.14) — solo si drill activo es SB
        if drill_activo and 'SB' in drill_activo and 'display_drill_sb_ranges' in g:
            st.markdown('<div class="section-title">📐 SB Rangos</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_drill_sb_ranges'], df)
            if out.strip(): st.code(out.strip(), language=None)

        st.markdown('<div class="section-title">📌 Reglas paralelas</div>', unsafe_allow_html=True)
        sb_df = df[df['player_position']=='SB'] if 'player_position' in df.columns else None
        bb_df = df[df['player_position']=='BB'] if 'player_position' in df.columns else None
        sb_vpip = sb_df['flg_vpip'].mean()*100 if sb_df is not None and 'flg_vpip' in sb_df.columns and len(sb_df)>0 else 0
        sb_limp = sb_df['flg_p_limp'].mean()*100 if sb_df is not None and 'flg_p_limp' in sb_df.columns and len(sb_df)>0 else 0
        bb_vpip = bb_df['flg_vpip'].mean()*100 if bb_df is not None and 'flg_vpip' in bb_df.columns and len(bb_df)>0 else 0
        for regla, stat, ok in [
            ("SB: NUNCA limp. Solo raise o fold.", f"VPIP {sb_vpip:.1f}% · Limp {sb_limp:.1f}%", sb_vpip<=40 and sb_limp<5),
            ("BB: Defender amplio. Suited → call.", f"VPIP {bb_vpip:.1f}% (ref ≥55%)", bb_vpip>=45),
        ]:
            st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;border-radius:8px;
                padding:10px 14px;margin-bottom:8px;font-size:.85rem;">
                {'🟢' if ok else '🔴'} <b style="color:#e8e8f0;">{regla}</b><br>
                <span style="color:#4b4b6a;font-family:'JetBrains Mono',monospace;font-size:.78rem;">{stat}</span>
            </div>""", unsafe_allow_html=True)

        # ── Execution Rate del drill activo ──────────────────────────────
        er = R.get('execution_rate_result', {})
        if er and isinstance(er, dict) and er.get('total_opportunities', 0) > 0:
            er_rate  = er.get('execution_rate_pct', 0)
            er_total = er.get('total_opportunities', 0)
            er_ok    = er.get('executed_correctly', 0)
            er_color = '#22c55e' if er_rate >= 75 else '#f59e0b' if er_rate >= 50 else '#ef4444'
            st.markdown(
                f"""<div style="background:#0a0f1e;border:1px solid {er_color};
                    border-radius:10px;padding:12px 18px;margin-bottom:8px;
                    display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;
                            color:#60a5fa;text-transform:uppercase;margin-bottom:4px;">
                            📊 Tasa de ejecución drill</div>
                        <div style="color:#94a3b8;font-size:.82rem;">
                            {er_ok}/{er_total} oportunidades aplicadas correctamente</div>
                    </div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;
                        font-weight:700;color:{er_color};">{er_rate:.0f}%</div>
                </div>""",
                unsafe_allow_html=True
            )

        # ── Puente Teoría → Mesa (after_session_bridge) ───────────────────
        bridge = R.get('bridge_result', {})
        if bridge and not bridge.get('error'):
            exec_rate = bridge.get('execution_rate', 0)
            applied   = bridge.get('applied', 0)
            missed    = bridge.get('missed', [])
            total_opp = applied + len(missed)
            if total_opp > 0:
                rate_color = '#22c55e' if exec_rate >= 80 else '#f59e0b' if exec_rate >= 50 else '#ef4444'
                st.markdown('<div class="section-title">🔗 Puente Teoría → Mesa</div>',
                            unsafe_allow_html=True)
                st.markdown(
                    f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;
                        border-radius:10px;padding:14px 18px;margin-bottom:10px;">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:.85rem;color:#94a3b8;">
                                Oportunidades drill: <b style="color:#e8e8f0;">{total_opp}</b>
                                · Correctas: <b style="color:#22c55e;">{applied}</b>
                                · Errores: <b style="color:#ef4444;">{len(missed)}</b>
                            </span>
                            <span style="font-family:'JetBrains Mono',monospace;font-size:1.1rem;
                                font-weight:700;color:{rate_color};">{exec_rate:.0f}%</span>
                        </div>
                    </div>""",
                    unsafe_allow_html=True
                )
                if missed:
                    with st.expander(f"❌ Ver {len(missed)} error(es) detectado(s)"):
                        for m in missed[:8]:
                            net_c = '#ef4444' if float(m.get('net',0)) < 0 else '#94a3b8'
                            st.markdown(
                                f"""<div style="background:#1a0a0a;border:1px solid #3d1515;
                                    border-radius:8px;padding:10px 14px;margin-bottom:6px;
                                    font-family:'JetBrains Mono',monospace;font-size:.8rem;">
                                    <span style="color:#a78bfa;">{m.get('hole','??')}</span>
                                    <span style="color:#4b4b6a;margin:0 8px;">
                                        {m.get('pos','?')} · {str(m.get('date',''))[:10]}</span>
                                    <span style="color:{net_c};float:right;">
                                        {m.get('net',0):+.3f}€</span><br>
                                    <span style="color:#ef4444;font-size:.75rem;">{m.get('error','')}</span>
                                </div>""",
                                unsafe_allow_html=True
                            )
                        if len(missed) > 8:
                            st.caption(f"... y {len(missed)-8} más")

    with col_d2:
        st.markdown('<div class="section-title">📚 Plan de estudio M1</div>', unsafe_allow_html=True)
        study_tasks = []
        if 'develop_canalized_study_module_logic' in g and not R['spot_results'].empty:
            try:
                tr = g['develop_canalized_study_module_logic'](R['spot_results'], mode, roi_ranking=roi)
                if tr and 'tasks' in tr: study_tasks = tr['tasks']
            except: pass

        for i, task in enumerate((study_tasks or [
            "Rangos preflop: aperturas por posición BTN/CO/MP/UTG. Foco SRP. (10 min)",
            "2-3 situaciones de tu sesión: calcula equity vs rango estimado. (10 min)",
            "Clasifica últimos 10 flops: favorable/neutro/peligroso. (10 min)",
        ])[:3], 1):
            desc = task if isinstance(task,str) else task.get('description',str(task))
            st.markdown(f"""<div style="background:#0f0f1a;border:1px solid #1e1e3a;border-radius:8px;
                padding:10px 14px;margin-bottom:8px;">
                <span style="color:#60a5fa;font-family:'JetBrains Mono',monospace;
                    font-size:.75rem;font-weight:600;">DRILL #{i}</span><br>
                <span style="color:#94a3b8;font-size:.82rem;">{desc[:200]}</span>
            </div>""", unsafe_allow_html=True)

        # Recursos de estudio
        if 'display_study_resources' in g and drill_activo:
            st.markdown('<div class="section-title">📖 Recursos</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_study_resources'], drill_activo)
            if out.strip():
                st.code(out.strip(), language=None)

        # Transfer Drill — aplica tu fortaleza donde fallas
        if 'display_transfer_drill' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">🔄 Transfer Drill</div>',
                        unsafe_allow_html=True)
            try:
                out = _safe_capture(g['display_transfer_drill'],
                                    R['spot_results'], df)
                if out.strip():
                    st.code(out.strip(), language=None)
                else:
                    st.caption("Sin pares estructurales detectados aún (necesitas más spots con ≥10 manos).")
            except Exception as _e:
                st.caption(f"Transfer drill: {_e}")

        st.markdown('<div class="section-title">🧠 Tilt</div>', unsafe_allow_html=True)
        tilt = R['tilt_result']
        n_tilt   = tilt.get('n_tilt', 0) if tilt else 0
        n_sess_t = tilt.get('n_sessions', n_sess) if tilt else n_sess
        if n_tilt == 0:
            st.markdown(f"""<div style="background:#0a1a0a;border:1px solid #15381a;border-radius:8px;
                padding:10px 14px;font-size:.85rem;color:#4ade80;">
                🟢 Sin sesiones tilt ({n_sess_t} analizadas)</div>""", unsafe_allow_html=True)
        else:
            cost = tilt.get('tilt_cost_bb100', 0) if tilt else 0
            st.markdown(f"""<div style="background:#1a0a0a;border:1px solid #381515;border-radius:8px;
                padding:10px 14px;font-size:.85rem;color:#f87171;">
                🔴 {n_tilt} sesión(es) tilt · coste {cost:+.1f} BB/100</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — LEAKS & ROI
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col_l1, col_l2 = st.columns([3,2])

    with col_l1:
        # Análisis completo de top leaks (v2.14)
        if 'display_leak_analysis' in g and not R['spot_results'].empty:
            out = _safe_capture(g['display_leak_analysis'],
                                R['spot_results'], df, top_n=3)
            if out.strip():
                with st.expander("🔍 Análisis completo de leaks", expanded=True):
                    st.code(out.strip(), language=None)

        st.markdown('<div class="section-title">🔴 Top leaks</div>', unsafe_allow_html=True)
        if leaks_list:
            for i, lk in enumerate(leaks_list[:10], 1):
                ip   = lk['ip_oop'][:3] if lk['ip_oop'] else ''
                pt   = lk['pot_type'][:3] if lk['pot_type'] else ''
                tag  = f" · {ip} {pt}".strip() if ip or pt else ''
                st.markdown(f"""<div class="leak-row">
                    <span style="color:#4b4b6a;font-size:.72rem;">#{i}</span>
                    <span class="leak-spot"> {lk['spot_identifier']}</span>
                    <span class="leak-ev">{lk['ev_shrunk']:.3f}€</span>
                    <div class="leak-meta">{lk['n']} manos{tag}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Sin leaks — acumula más manos.")

        if families_list:
            st.markdown('<div class="section-title">📦 Familias</div>', unsafe_allow_html=True)
            for fam in families_list:
                ev  = fam['ev_total']
                dot = '🔴' if ev<-0.2 else ('🟡' if ev<0 else '⚪')
                st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;border-radius:8px;
                    padding:10px 14px;margin-bottom:6px;font-family:'JetBrains Mono',monospace;font-size:.8rem;">
                    {dot} {fam['icon']} <b style="color:#e8e8f0;">{fam['family']}</b>
                    <span style="float:right;color:#ef4444;">{ev:.3f}€</span>
                    <div style="color:#4b4b6a;font-size:.75rem;margin-top:3px;">
                        {fam['n_hands']} manos · {fam['description']}</div>
                </div>""", unsafe_allow_html=True)

        # Error pattern analysis
        if 'display_error_pattern_analysis' in g:
            st.markdown('<div class="section-title">🔍 Patrones de error</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_error_pattern_analysis'])
            if out.strip():
                st.code(out.strip(), language=None)

        # Top spots con manos reales representativas
        if 'display_top_spots_with_hands' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">🃏 Manos reales de los top leaks</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_top_spots_with_hands'],
                                df, R['spot_results'], top_n_spots=2, hands_per_spot=3)
            if out.strip():
                st.code(out.strip(), language=None)

        # Action leak dashboard (v2.14) — EV por raise/call/fold
        if 'display_action_leak_dashboard' in g and R.get('ev_by_action'):
            st.markdown('<div class="section-title">⚡ Leaks por acción</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_action_leak_dashboard'],
                                R['ev_by_action'],
                                R.get('action_leak_rank', []),
                                current_mode=mode)
            if out.strip(): st.code(out.strip(), language=None)

        # False strength audit (v2.14)
        if 'display_false_strength_audit' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">⚠️ Fortalezas falsas</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_false_strength_audit'],
                                df, R['spot_results'])
            if out.strip(): st.code(out.strip(), language=None)

    with col_l2:
        st.markdown('<div class="section-title">🟢 Oportunidades</div>', unsafe_allow_html=True)
        if opps_list:
            for opp in opps_list[:5]:
                st.markdown(f"""<div class="opp-row">
                    <span class="leak-spot" style="color:#4ade80;">{opp['spot_identifier']}</span>
                    <span class="opp-ev">+{opp['ev_shrunk']:.3f}€</span>
                    <div class="leak-meta">{opp['n']} manos</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Sin oportunidades con señal.")

        st.markdown('<div class="section-title">📐 Hero vs referencia NL2</div>', unsafe_allow_html=True)
        ref_vpip = {'BTN':45,'CO':35,'HJ':28,'UTG':20,'SB':40,'BB':55}
        for pos in ['BTN','CO','HJ','UTG','SB','BB']:
            pos_df = df[df['player_position']==pos] if 'player_position' in df.columns else None
            if pos_df is None or len(pos_df)<20 or 'flg_vpip' not in pos_df.columns: continue
            vpip = pos_df['flg_vpip'].mean()*100
            ref  = ref_vpip.get(pos,30); gap = vpip-ref
            dot  = '✅' if abs(gap)<=7 else ('⬆️' if gap>0 else '⬇️')
            col_g= '#22c55e' if abs(gap)<=7 else '#ef4444'
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
                padding:5px 10px;border-radius:5px;margin-bottom:3px;
                background:#0a0a14;font-family:'JetBrains Mono',monospace;font-size:.78rem;">
                <span style="color:#94a3b8;width:40px;">{pos}</span>
                <span style="color:#e8e8f0;">{vpip:.1f}%</span>
                <span style="color:#4b4b6a;">ref {ref}%</span>
                <span style="color:{col_g};">{'+' if gap>=0 else ''}{gap:.1f}pp {dot}</span>
            </div>""", unsafe_allow_html=True)

        # Velocity forecast
        if 'display_velocity_forecast' in g:
            st.markdown('<div class="section-title">⏱ Proyección</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_velocity_forecast'], df)
            if out.strip():
                st.code(out.strip()[:600], language=None)

        # GTO button — parámetros de consulta solver (v2.14)
        if 'display_gto_button' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">🔬 Consulta GTO</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_gto_button'], R['spot_results'], df)
            if out.strip(): st.code(out.strip(), language=None)

        # Comparación hero vs rangos referencia (v2.14)
        if 'display_range_comparison' in g:
            st.markdown('<div class="section-title">📐 Hero vs rangos GTO</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_range_comparison'], df)
            if out.strip(): st.code(out.strip(), language=None)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — POOL M5
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🌊 Pool fingerprint NL2</div>', unsafe_allow_html=True)
    m5_exploits = (m5 or {}).get('exploits', [])

    if not m5_exploits:
        st.info(f"M5 activo · {hand_count:,} manos")
        for opp_col, did_col, ref, label, tip in [
            ('flg_f_cbet_def_opp','flg_f_cbet_def', 40,"Fold vs cbet flop","CALL más — pool llama mucho"),
            ('flg_f_cbet_opp','flg_f_cbet', 62,"CBet flop IP","Expandir — pool over-folds"),
        ]:
            if opp_col in df.columns and did_col in df.columns:
                on = df[opp_col].sum()
                if on > 50:
                    pct = (on - df[did_col].sum())/on*100 if 'def' in opp_col else df[did_col].sum()/on*100
                    diff= pct-ref; cls='exploit-red' if abs(diff)>10 else 'exploit-yellow'
                    st.markdown(f"""<div class="exploit-row {cls}">
                        <span style="color:#94a3b8;">{'🔴' if abs(diff)>10 else '🟡'} {label}</span>
                        <span style="color:#e8e8f0;font-weight:600;">{pct:.1f}%</span>
                        <span style="color:#4b4b6a;">ref {ref}%</span>
                    </div>
                    <div style="font-size:.75rem;color:#3d5a6e;margin:-2px 0 6px 12px;">→ {tip}</div>""",
                    unsafe_allow_html=True)
    else:
        for item in m5_exploits[:20]:
            obs=item.get('observed_pct',0); base=item.get('baseline_pct',0)
            diff=obs-base; n=item.get('n',0); tip=item.get('exploit_tip','')
            dot='🔴' if abs(diff)>10 else('🟡' if abs(diff)>5 else '✅')
            cls='exploit-red' if abs(diff)>10 else('exploit-yellow' if abs(diff)>5 else 'exploit-green')
            st.markdown(f"""<div class="exploit-row {cls}">
                <span style="color:#94a3b8;">{dot} {item.get('spot','?')}</span>
                <div><span style="color:#e8e8f0;">{obs:.1f}%</span>
                <span style="color:#4b4b6a;margin-left:8px;">base {base:.0f}%</span>
                <span style="color:#3d5a6e;margin-left:8px;">n={n}</span></div>
            </div>""", unsafe_allow_html=True)
            if tip:
                st.markdown(f"<div style='font-size:.75rem;color:#3d5a6e;margin:-2px 0 6px 12px;'>→ {tip}</div>",
                            unsafe_allow_html=True)

    st.markdown('<div class="section-title">👥 Pool</div>', unsafe_allow_html=True)
    if 'opp_class' in df.columns:
        counts = df['opp_class'].value_counts(); tot=counts.sum()
        icons  = {'fish':'🐟','maniac':'🤪','reg':'🎯','unknown':'❓'}
        cols_p = st.columns(len(counts))
        for i,(cls,cnt) in enumerate(counts.items()):
            with cols_p[i]:
                st.markdown(f"""<div class="metric-card" style="text-align:center;">
                    <div style="font-size:1.5rem;">{icons.get(cls,'❓')}</div>
                    <div class="metric-label">{cls}</div>
                    <div class="metric-value neutral" style="font-size:1.2rem;">{cnt/tot*100:.0f}%</div>
                    <div class="metric-sub">{cnt} opp</div>
                </div>""", unsafe_allow_html=True)

    # Pool fingerprint pending
    if 'display_pool_fingerprint_pending' in g:
        st.markdown('<div class="section-title">📍 Pool fingerprint detalle</div>', unsafe_allow_html=True)
        out = _safe_capture(g['display_pool_fingerprint_pending'], m5)
        if out.strip():
            st.code(out.strip(), language=None)

    # Board texture summary
    if 'display_board_texture_summary' in g:
        st.markdown('<div class="section-title">🌊 Texturas de tablero</div>',
                    unsafe_allow_html=True)
        out = _safe_capture(g['display_board_texture_summary'], df)
        if out.strip():
            st.code(out.strip(), language=None)
        else:
            st.caption("Disponible tras enriquecimiento de tableros.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SESIONES
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">📈 Sesiones</div>', unsafe_allow_html=True)

    # Manos de alto impacto — v2.52: con consulta solver integrada
    st.markdown('<div class="section-title">💥 Manos de alto impacto</div>',
                unsafe_allow_html=True)
    if 'display_high_impact_with_solver' in g:
        out = _safe_capture(g['display_high_impact_with_solver'], df,
                            session_id=current_session_id)
        if out.strip():
            st.code(out.strip(), language=None)
        else:
            st.caption("Sin manos de alto impacto (umbral: >4BB).")
    elif 'display_high_impact_hands' in g:
        out = _safe_capture(g['display_high_impact_hands'], df,
                            session_id=current_session_id)
        if out.strip():
            st.code(out.strip(), language=None)
        else:
            st.caption("Sin manos de alto impacto en esta sesión (umbral: >5BB).")

    if 'session_id' in df.columns and 'net_won' in df.columns:
        import pandas as pd
        sess = df.groupby('session_id',sort=True).agg(
            date=('date','first'),hands=('hand_id','count'),net=('net_won','sum')
        ).reset_index()
        sess['cumulative'] = sess['net'].cumsum()

        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Bar(x=sess['session_id'], y=sess['net'],
            marker_color=['#22c55e' if x>=0 else '#ef4444' for x in sess['net']],
            name='Net sesión', opacity=0.8))
        fig.add_trace(go.Scatter(x=sess['session_id'], y=sess['cumulative'],
            line=dict(color='#60a5fa',width=2), name='Acumulado', yaxis='y2'))
        fig.update_layout(
            plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
            font=dict(family='JetBrains Mono',color='#6b6b8a',size=11),
            xaxis=dict(gridcolor='#1e1e3a',tickangle=45),
            yaxis=dict(gridcolor='#1e1e3a',title='Net €'),
            yaxis2=dict(overlaying='y',side='right',title='Acumulado €',
                        gridcolor='rgba(0,0,0,0)'),
            legend=dict(bgcolor='#0f0f1a',bordercolor='#1e1e3a'),
            margin=dict(l=40,r=40,t=20,b=60), height=300)
        st.plotly_chart(fig, use_container_width=True)

        # Luck/skill analysis
        if 'display_luck_skill_analysis' in g and hand_count >= 5000:
            st.markdown('<div class="section-title">🎲 Luck vs Skill</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_luck_skill_analysis'], df)
            if out.strip():
                st.code(out.strip(), language=None)
        elif hand_count < 5000:
            st.caption(f"🔒 Luck/Skill analysis se activa a 5.000 manos ({hand_count:,}/{5000})")

        st.markdown('<div class="section-title">📋 Detalle sesiones</div>', unsafe_allow_html=True)
        for _, row in sess.iterrows():
            nv=row['net']; cv=row['cumulative']
            nc='#22c55e' if nv>=0 else '#ef4444'; cc2='#22c55e' if cv>=0 else '#ef4444'
            ds=row['date'].strftime('%Y-%m-%d') if hasattr(row['date'],'strftime') else str(row['date'])[:10]
            st.markdown(f"""<div class="session-row">
                <span style="color:#4b4b6a;width:100px;">{row['session_id']}</span>
                <span style="color:#94a3b8;width:90px;">{ds}</span>
                <span style="color:#6b6b8a;width:70px;">{row['hands']}m</span>
                <span style="color:{nc};width:80px;font-weight:600;">{'+' if nv>=0 else ''}{nv:.2f}€</span>
                <span style="color:{cc2};width:80px;">cum: {'+' if cv>=0 else ''}{cv:.2f}€</span>
            </div>""", unsafe_allow_html=True)

        # Duración óptima de sesión
        if 'display_optimal_session_length' in g:
            st.markdown('<div class="section-title">⏱ Duración óptima de sesión</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_optimal_session_length'], df)
            if out.strip():
                st.code(out.strip(), language=None)
            else:
                st.caption("Disponible con ≥3 sesiones y ≥50 manos/sesión.")

        # Stop-loss inteligente
        if 'display_session_stoploss' in g:
            st.markdown('<div class="section-title">🛑 Stop-loss de sesión</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_session_stoploss'], df,
                                current_session_id)
            if out.strip():
                st.code(out.strip(), language=None)

        # Tilt analysis detallado
        if 'display_tilt_analysis' in g and R.get('tilt_result'):
            st.markdown('<div class="section-title">🌡 Análisis de tilt</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_tilt_analysis'], R['tilt_result'])
            if out.strip():
                st.code(out.strip(), language=None)

        # Performance by hour
        if 'display_performance_by_hour' in g:
            st.markdown('<div class="section-title">🕐 Rendimiento por hora del día</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_performance_by_hour'], df)
            if out.strip():
                st.code(out.strip(), language=None)
            else:
                st.caption("Disponible con ≥50 manos por franja horaria.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROGRESIÓN
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown('<div class="section-title">📊 Progresión sesión a sesión</div>', unsafe_allow_html=True)
        progression = R.get('progression', [])
        if progression:
            for sess_data in progression[-10:]:
                sid      = sess_data.get('session_id','?')
                bb_vpip  = sess_data.get('bb_vpip', None)
                btn_vpip = sess_data.get('btn_vpip', None)
                cbet_ip  = sess_data.get('cbet_ip', None)
                net_s    = sess_data.get('net', 0)
                nc       = '#22c55e' if net_s>=0 else '#ef4444'
                parts = []
                if bb_vpip  is not None: parts.append(f"BB VPIP {bb_vpip:.0f}%")
                if btn_vpip is not None: parts.append(f"BTN {btn_vpip:.0f}%")
                if cbet_ip  is not None: parts.append(f"CBet IP {cbet_ip:.0f}%")
                st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;border-radius:8px;
                    padding:8px 12px;margin-bottom:4px;font-family:'JetBrains Mono',monospace;font-size:.78rem;">
                    <span style="color:#a78bfa;">{sid}</span>
                    <span style="color:{nc};float:right;">{'+' if net_s>=0 else ''}{net_s:.2f}€</span>
                    <div style="color:#4b4b6a;font-size:.72rem;margin-top:2px;">{' · '.join(parts)}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Progresión disponible con ≥2 sesiones.")

        # Features status
        if 'display_features_status' in g:
            st.markdown('<div class="section-title">🔓 Features activas</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_features_status'], hand_count)
            if out.strip():
                st.code(out.strip(), language=None)

        # Velocidad de corrección de KPIs (v2.14)
        if 'display_learning_velocity' in g:
            st.markdown('<div class="section-title">⚡ Velocidad de aprendizaje</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_learning_velocity'], df)
            if out.strip():
                st.code(out.strip(), language=None)
            else:
                st.caption("Disponible con ≥3 sesiones.")

        # Tabla de progresión detallada con semáforos (v2.14)
        if 'display_progression_table' in g:
            st.markdown('<div class="section-title">📋 Tabla de progresión</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_progression_table'], df, m5_result=m5)
            if out.strip():
                st.code(out.strip(), language=None)

    with col_p2:
        st.markdown('<div class="section-title">📐 KPI gaps</div>', unsafe_allow_html=True)
        if 'display_kpi_gaps' in g and not R['spot_results'].empty:
            out = _safe_capture(g['display_kpi_gaps'], df)
            if out.strip():
                st.code(out.strip(), language=None)

        # Hole card analysis
        if 'display_hole_card_analysis' in g:
            st.markdown('<div class="section-title">🃏 Hole cards analysis</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_hole_card_analysis'], df)
            if out.strip():
                st.code(out.strip()[:800], language=None)

        # Strengths
        if 'build_strength_ranking' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">💪 Fortalezas</div>', unsafe_allow_html=True)
            try:
                str_ranking = g['build_strength_ranking'](R['spot_results'])
                if str_ranking is not None and hasattr(str_ranking,'head'):
                    for _, sr in str_ranking.head(3).iterrows():
                        spot = sr.get('spot_identifier','?')
                        ev   = float(sr.get('impacto_ev_total_eur_shrunk',0))
                        n    = int(sr.get('spot_hands_count',0))
                        st.markdown(f"""<div class="opp-row">
                            <span class="leak-spot" style="color:#4ade80;">{spot}</span>
                            <span class="opp-ev">+{ev:.3f}€</span>
                            <div class="leak-meta">{n} manos</div>
                        </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.caption(f"Strengths: {e}")

        # Strength analysis detallado (v2.14)
        if 'display_strength_analysis' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">💎 Análisis de fortalezas</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_strength_analysis'],
                                df, R['spot_results'], R['overall_metrics'])
            if out.strip(): st.code(out.strip(), language=None)

        # Evolución del leak en el tiempo (v2.14)
        if 'track_leak_evolution' in g and drill_activo and not R['spot_results'].empty:
            st.markdown('<div class="section-title">📉 Evolución del leak</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['track_leak_evolution'],
                                R['spot_results'], drill_activo)
            if out.strip(): st.code(out.strip(), language=None)
            else: st.caption("Disponible con ≥3 sesiones con datos del leak.")

        # Evaluación transición de stake (v2.14)
        if 'evaluate_stake_transition' in g and 'calculate_ev_metrics_by_stake' in g:
            st.markdown('<div class="section-title">⬆ Transición de stake</div>',
                        unsafe_allow_html=True)
            try:
                metrics_by_stake = g['calculate_ev_metrics_by_stake'](df)
                if metrics_by_stake:
                    out = _safe_capture(g['evaluate_stake_transition'],
                                        metrics_by_stake, 'NL2', 'NL5',
                                        friccion_avg=R['friccion_avg'])
                    if out.strip(): st.code(out.strip(), language=None)
            except Exception as _e:
                st.caption(f"Transición stake: {_e}")

        # Plan de drills recomendado (v2.14)
        if 'recommend_drill_plan' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">📋 Plan de drills</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['recommend_drill_plan'],
                                df, R['spot_results'], R['overall_metrics'],
                                R['roi_ranking'], drill_activo=drill_activo)
            if out.strip(): st.code(out.strip(), language=None)

        # Progreso de fortalezas M7 (v2.14)
        if 'display_strength_progress' in g:
            st.markdown('<div class="section-title">🌟 Progreso de fortalezas</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_strength_progress'])
            if out.strip():
                st.code(out.strip(), language=None)
            else:
                st.caption("Disponible tras registrar fortalezas en M7.")

        # TW Ranking — comparación time-weighted vs ranking simple (v2.52)
        if 'display_tw_ranking_comparison' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">⚖️ Ranking TW vs Simple</div>',
                        unsafe_allow_html=True)
            try:
                tw_spots = None
                if 'build_time_weighted_spot_results' in g:
                    tw_spots = g['build_time_weighted_spot_results'](
                        None, R['spot_results'])
                if tw_spots is not None:
                    out = _safe_capture(g['display_tw_ranking_comparison'],
                                        tw_spots, R['spot_results'])
                    if out.strip(): st.code(out.strip(), language=None)
            except Exception as _e:
                st.caption(f"TW ranking: {_e}")

        # Perfil cognitivo del jugador (v2.52)
        if 'build_cognitive_profile_context' in g and not R['spot_results'].empty:
            st.markdown('<div class="section-title">🧬 Perfil cognitivo</div>',
                        unsafe_allow_html=True)
            try:
                cp_ctx = g['build_cognitive_profile_context'](
                    df, R['spot_results'], R['overall_metrics'])
                if cp_ctx:
                    # Display summary
                    if '_display_cognitive_profile_summary' in g:
                        out = _safe_capture(g['_display_cognitive_profile_summary'], cp_ctx)
                        if out.strip(): st.code(out.strip(), language=None)
                    else:
                        # Fallback: show raw key metrics
                        for k in ['dominant_leak_type','learning_style','exec_rate_trend']:
                            if k in cp_ctx:
                                st.caption(f"{k}: {cp_ctx[k]}")
            except Exception as _e:
                st.caption(f"Perfil cognitivo disponible con ≥200 manos.")



# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — STATS DETALLE
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown('<div class="section-title">🔢 Stats por posición</div>', unsafe_allow_html=True)
        for pos in ['BTN','CO','HJ','UTG','SB','BB']:
            pos_df = df[df['player_position']==pos] if 'player_position' in df.columns else None
            if pos_df is None or len(pos_df)<5: continue
            vpip = pos_df['flg_vpip'].mean()*100 if 'flg_vpip' in pos_df.columns else 0
            pfr  = pos_df['flg_p_first_raise'].mean()*100 if 'flg_p_first_raise' in pos_df.columns else 0
            net  = pos_df['net_won'].sum() if 'net_won' in pos_df.columns else 0
            n    = len(pos_df); c='#22c55e' if net>0 else '#ef4444'
            st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;border-radius:8px;
                padding:10px 14px;margin-bottom:6px;font-family:'JetBrains Mono',monospace;font-size:.8rem;">
                <span style="color:#a78bfa;font-weight:600;width:40px;display:inline-block;">{pos}</span>
                <span style="color:#94a3b8;">VPIP {vpip:.1f}%</span>
                <span style="color:#6b6b8a;margin-left:12px;">PFR {pfr:.1f}%</span>
                <span style="color:{c};float:right;">{'+' if net>=0 else ''}{net:.2f}€ ({n}m)</span>
            </div>""", unsafe_allow_html=True)

        # Session degradation
        if 'display_session_degradation' in g:
            st.markdown('<div class="section-title">⏳ Degradación de sesión</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_session_degradation'], df)
            if out.strip(): st.code(out.strip(), language=None)

    with col_s2:
        st.markdown('<div class="section-title">📊 KPIs globales</div>', unsafe_allow_html=True)
        kpis = [
            ("VPIP global",  df['flg_vpip'].mean()*100 if 'flg_vpip' in df.columns else None,"%",(20,35)),
            ("PFR global",   df['flg_p_first_raise'].mean()*100 if 'flg_p_first_raise' in df.columns else None,"%",(15,28)),
            ("3-bet %",      df['flg_p_3bet'].sum()/max(df['flg_p_3bet_opp'].sum(),1)*100 if 'flg_p_3bet' in df.columns else None,"%",(5,12)),
            ("CBet flop IP", df['flg_f_cbet'].sum()/max(df['flg_f_cbet_opp'].sum(),1)*100 if 'flg_f_cbet' in df.columns else None,"%",(55,70)),
            ("Fold to CBet", (df['flg_f_cbet_def_opp'].sum()-df['flg_f_cbet_def'].sum())/max(df['flg_f_cbet_def_opp'].sum(),1)*100 if 'flg_f_cbet_def_opp' in df.columns else None,"%",(27,45)),
            ("WTSD%",        df['flg_showdown'].sum()/max(df['flg_f_saw'].sum(),1)*100 if 'flg_showdown' in df.columns else None,"%",(25,32)),
            ("W$SD%",        df[df['flg_showdown']==True]['flg_won_hand'].mean()*100 if 'flg_showdown' in df.columns and df['flg_showdown'].sum()>0 else None,"%",(48,56)),
        ]
        for label, val, unit, (lo,hi) in kpis:
            if val is None: continue
            in_r = lo<=val<=hi; dot='✅' if in_r else ('⬆️' if val<lo else '⬇️')
            c='#22c55e' if in_r else '#f59e0b'
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;
                padding:7px 12px;border-radius:6px;margin-bottom:4px;
                background:#0a0a14;border:1px solid #15152a;
                font-family:'JetBrains Mono',monospace;font-size:.8rem;">
                <span style="color:#94a3b8;">{label}</span>
                <span style="color:{c};font-weight:600;">{val:.1f}{unit} {dot}</span>
                <span style="color:#3d3d5e;">ref {lo}-{hi}{unit}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-title">📉 Red / Blue line</div>', unsafe_allow_html=True)
        if 'display_red_blue_line' in g:
            out = _safe_capture(g['display_red_blue_line'], df,
                                by_position=True, by_session=True)
            if out.strip():
                st.code(out.strip(), language=None)
        elif 'flg_showdown' in df.columns and 'net_won' in df.columns:
            # Fallback inline si la función no está disponible
            sd=df[df['flg_showdown']==True]; nsd=df[df['flg_showdown']==False]; nt=len(df)
            for line, vn, color in [("🔵 Blue (showdown)",sd['net_won'].sum(),'#60a5fa'),
                                     ("🔴 Red (no-SD)",   nsd['net_won'].sum(),'#f87171')]:
                vb=vn/nt*100/0.02 if nt>0 else 0; s='+' if vb>=0 else ''
                st.markdown(f"""<div style="background:#0a0a14;border:1px solid #1e1e3a;border-radius:8px;
                    padding:10px 14px;margin-bottom:6px;font-family:'JetBrains Mono',monospace;font-size:.82rem;">
                    <span style="color:{color};">{line}</span>
                    <span style="float:right;color:{color};font-weight:600;">
                        {s}{vb:.1f} BB/100 ({s}{vn:.2f}€)</span>
                </div>""", unsafe_allow_html=True)

        # Stack depth performance
        if 'display_stack_depth_performance' in g:
            st.markdown('<div class="section-title">📏 Stack depth</div>', unsafe_allow_html=True)
            out = _safe_capture(g['display_stack_depth_performance'], df)
            if out.strip(): st.code(out.strip(), language=None)

        # EV sin iniciativa preflop (v2.14)
        if 'display_no_initiative_ev' in g:
            st.markdown('<div class="section-title">⚠️ EV sin iniciativa</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_no_initiative_ev'], df)
            if out.strip(): st.code(out.strip(), language=None)

        # MDF dashboard — Minimum Defense Frequency (v2.14)
        if 'display_mdf_dashboard' in g:
            st.markdown('<div class="section-title">🛡 MDF — Defensa mínima</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_mdf_dashboard'], df)
            if out.strip(): st.code(out.strip(), language=None)
            else: st.caption("MDF disponible con ≥15 manos por posición/calle.")

        # Drill transfer analysis completo (v2.14)
        if 'display_drill_transfer_analysis' in g and drill_activo:
            st.markdown('<div class="section-title">🔄 Transfer drill completo</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_drill_transfer_analysis'],
                                df, drill_activo=drill_activo)
            if out.strip(): st.code(out.strip(), language=None)
            else: st.caption("Transfer analysis disponible con ≥4 sesiones post-drill.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — M4 COACH (GEMINI)
# ══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown('<div class="section-title">🤖 M4.4 Coach Analítico</div>', unsafe_allow_html=True)

    if not gemini_key:
        st.info("Introduce tu GEMINI_API_KEY en la barra lateral para activar el coach. Es gratuito: https://aistudio.google.com/apikey")
    elif not m4_enabled:
        st.info("Activa M4.4 Coach en la barra lateral.")
    else:
        col_m1, col_m2 = st.columns([2,1])
        with col_m1:
            if st.session_state.m4_output:
                out = st.session_state.m4_output
                try:
                    d = json.loads(out) if isinstance(out, str) else out
                    st.markdown(f"""<div class="coach-box">
                        <b>Acción concreta:</b> {d.get('accion_concreta','—')}<br><br>
                        <b>Concepto teórico:</b> {d.get('concepto_teorico','—')}<br><br>
                        <b>Contexto:</b> {d.get('contexto_spot',d.get('contexto_pool','—'))}<br><br>
                        <b>Impacto estimado:</b> {d.get('impacto_estimado','—')}<br><br>
                        <b>Patrón:</b> {d.get('patron_detectado','—')} ·
                        <b>Confianza:</b> {d.get('confianza','—')}<br><br>
                        <b>❓ Pregunta:</b> {d.get('pregunta_implementacion',d.get('pregunta_reflexion','—'))}
                    </div>""", unsafe_allow_html=True)
                except:
                    st.code(str(out), language=None)
            else:
                st.markdown("""<div class="coach-box" style="color:#3d3d6e;">
                    Pulsa "Consultar coach" para obtener análisis del top leak con el contexto de tu sesión actual.
                </div>""", unsafe_allow_html=True)

        with col_m2:
            if st.button("🤖 Consultar M4 Coach", type="primary", use_container_width=True):
                if 'run_m44_coach' in g:
                    import os as _os
                    _os.environ['GEMINI_API_KEY'] = gemini_key
                    with st.spinner("Consultando Gemini..."):
                        buf = io.StringIO()
                        try:
                            old = sys.stdout; sys.stdout = buf
                            result = g['run_m44_coach'](
                                R['overall_metrics'], R['spot_results'], mode,
                                full_df=df, m5_result=m5,
                                speed_result=R['speed_result'],
                                roi_ranking=roi, m4_enabled=True,
                                api_key=gemini_key
                            )
                            sys.stdout = old
                            st.session_state.m4_output = result if result else buf.getvalue()
                        except Exception as e:
                            sys.stdout = old
                            st.session_state.m4_output = f"Error: {e}"
                    st.rerun()

            if 'run_m4_gemini_diagnosis' in g:
                st.markdown("---")
                if st.button("🔬 Diagnóstico Gemini", use_container_width=True):
                    import os as _os; _os.environ['GEMINI_API_KEY'] = gemini_key
                    with st.spinner("Diagnosticando..."):
                        out = _safe_capture(g['run_m4_gemini_diagnosis'],
                                           R['leak_object'] or {}, mode, api_key=gemini_key)
                    st.code(out[:1000] if out.strip() else "Sin output", language=None)

    # Coach history
    if 'display_study_progress' in g:
        st.markdown('<div class="section-title">📚 Progreso de estudio</div>', unsafe_allow_html=True)
        out = _safe_capture(g['display_study_progress'])
        if out.strip(): st.code(out.strip(), language=None)

    # Followup effectiveness
    if 'display_followup_effectiveness' in g:
        st.markdown('<div class="section-title">📈 Efectividad followup</div>', unsafe_allow_html=True)
        out = _safe_capture(g['display_followup_effectiveness'])
        if out.strip(): st.code(out.strip(), language=None)

    # Error timing analysis (GAP 4: errores por momento de sesión T1/T2/T3)
    if 'display_error_timing_analysis' in g:
        st.markdown('<div class="section-title">⏱ Errores por momento de sesión</div>',
                    unsafe_allow_html=True)
        out = _safe_capture(g['display_error_timing_analysis'], df)
        if out.strip():
            st.code(out.strip(), language=None)
        else:
            st.caption("Disponible tras ≥5 errores clasificados en sesiones de estudio.")

    # Auditoría de uso del sistema (v2.14)
    if 'display_system_usage_audit' in g:
        st.markdown('<div class="section-title">🔍 Auditoría del sistema</div>',
                    unsafe_allow_html=True)
        out = _safe_capture(g['display_system_usage_audit'], df)
        if out.strip(): st.code(out.strip(), language=None)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — SUNCHAT
# ══════════════════════════════════════════════════════════════════════════════
with tab8:
    st.markdown('<div class="section-title">💬 SunChat — Entrenamiento conversacional</div>', unsafe_allow_html=True)

    # ── run_sunchat_0c — modo rápido sin HH (v2.52) ───────────────────────────
    if groq_key and 'run_sunchat_0c' in g:
        with st.expander("⚡ SunChat 0c — sesión rápida (sin HH)", expanded=False):
            st.caption("Sesión cognitiva sin necesidad de hand history. Solo con las API keys configuradas.")
            if st.button("▶ Iniciar SunChat 0c", key='sc0c_start'):
                import os as _os0c; _os0c.environ['GROQ_API_KEY'] = groq_key
                if gemini_key: _os0c.environ['GEMINI_API_KEY'] = gemini_key
                with st.spinner("Iniciando sesión SunChat 0c..."):
                    _buf0c = __import__('io').StringIO()
                    _sys0c = __import__('sys')
                    _old0c = _sys0c.stdout; _sys0c.stdout = _buf0c
                    try:
                        import unittest.mock as _mk0c
                        with _mk0c.patch('builtins.input', return_value=''):
                            g['run_sunchat_0c']()
                    except Exception as _e0c:
                        print(f"Error: {_e0c}")
                    finally:
                        _sys0c.stdout = _old0c
                out0c = _buf0c.getvalue()
                if out0c.strip():
                    st.code(out0c.strip(), language=None)
                else:
                    st.info("run_sunchat_0c requiere HH cargada o API key activa. Carga una HH primero.")

    if not groq_key:
        st.info("Introduce tu GROQ_API_KEY en la barra lateral. Gratuito: https://console.groq.com/keys")
    elif not sc_enabled:
        st.info("Activa SunChat en la barra lateral.")
    else:
        leak_obj = R.get('leak_object')
        if leak_obj:
            col_sc1, col_sc2 = st.columns([3,1])
            with col_sc1:
                st.markdown(f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;border-radius:10px;
                    padding:14px 18px;margin-bottom:16px;font-family:'JetBrains Mono',monospace;font-size:.82rem;">
                    <b style="color:#60a5fa;">Leak activo:</b>
                    <span style="color:#a78bfa;"> {leak_obj.get('leak_id','?')}</span><br>
                    <span style="color:#4b4b6a;">
                        EV loss: {leak_obj.get('ev_loss_bb100',0):.0f} BB/100 ·
                        {leak_obj.get('sample',0)} manos ·
                        {leak_obj.get('pattern','—')[:80]}
                    </span>
                </div>""", unsafe_allow_html=True)
            with col_sc2:
                if st.button("🆕 Reset chat", use_container_width=True):
                    st.session_state.sunchat_msgs = []
                    st.rerun()

        # Chat history
        msgs = st.session_state.sunchat_msgs or []
        for msg in msgs:
            role = msg.get('role','user')
            txt  = msg.get('content','')
            bg   = '#0f1629' if role=='assistant' else '#0a0a14'
            bc   = '#1e3a5f' if role=='assistant' else '#1e1e3a'
            icon = '🤖' if role=='assistant' else '👤'
            st.markdown(f"""<div style="background:{bg};border:1px solid {bc};border-radius:8px;
                padding:10px 14px;margin-bottom:8px;font-size:.85rem;color:#94a3b8;">
                {icon} {txt}</div>""", unsafe_allow_html=True)

        # Input
        user_input = st.chat_input("Escribe tu respuesta o pregunta...")
        if user_input:
            msgs.append({'role':'user','content':user_input})
            if 'run_sunchat_session' in g and '_groq_call' in g:
                import os as _os; _os.environ['GROQ_API_KEY'] = groq_key
                try:
                    # Build conversation for groq
                    system_fn = g.get('_build_sunchat_system_prompt')
                    _m4_ctx   = {'error_concreto': '', 'concepto_clave': '', 'drill_focus': ''}
                    system_p  = system_fn(leak_obj or {}, _m4_ctx, mode) if system_fn else \
                                f"Eres SunChat, coach de poker. Leak: {(leak_obj or {}).get('leak_id','?')}. Modo: {mode}."
                    history_for_api = [{'role':m['role'],'content':m['content']} for m in msgs]
                    reply, err_sc = g['_groq_call'](history_for_api, system=system_p, api_key=groq_key)
                    if err_sc:
                        reply = f"⚠️ {err_sc}"
                    msgs.append({'role':'assistant','content':reply or '...'})
                except Exception as e:
                    msgs.append({'role':'assistant','content':f"⚠️ Error: {e}"})
            else:
                msgs.append({'role':'assistant','content':"⚠️ SunChat no disponible en esta versión de os_library."})
            st.session_state.sunchat_msgs = msgs
            st.rerun()

        if not msgs and leak_obj:
            if st.button("▶ Iniciar sesión SunChat", type="primary"):
                import os as _os; _os.environ['GROQ_API_KEY'] = groq_key
                try:
                    system_fn = g.get('_build_sunchat_system_prompt')
                    _m4_ctx   = {'error_concreto': '', 'concepto_clave': '', 'drill_focus': ''}
                    system_p  = system_fn(leak_obj, _m4_ctx, mode) if system_fn else \
                                f"Eres SunChat, coach de poker. Modo {mode}. Leak: {leak_obj.get('leak_id','?')}."
                    history_for_api = [{'role':'user','content':f"Empezamos. Mi leak activo es: {leak_obj.get('leak_id','?')}. Patrón: {leak_obj.get('pattern','')}. EV loss: {leak_obj.get('ev_loss_bb100',0):.0f} BB/100."}]
                    reply, _ = g['_groq_call'](history_for_api, system=system_p, api_key=groq_key)
                    st.session_state.sunchat_msgs = [
                        history_for_api[0],
                        {'role':'assistant','content': reply or 'Hola, empecemos.'}
                    ]
                except Exception as e:
                    st.error(f"Error iniciando SunChat: {e}")
                st.rerun()



# ══════════════════════════════════════════════════════════════════════════════
# TAB 9 — ESTUDIO SM-2
# ══════════════════════════════════════════════════════════════════════════════
with tab9:
    st.markdown('<div class="section-title">🧠 Estudio SM-2 — Razonamiento & Level-Up</div>',
                unsafe_allow_html=True)

    # ── helpers locales ───────────────────────────────────────────────────────
    DRILL_LABELS = {
        'BB_OOP_SRP_deep_preflop_unknown_F': 'BB Defense',
        'SB_open_or_fold':                   'SB Open/Fold',
        'BTN_IP_open_postflop':              'BTN Postflop',
        'ccall_PF':                          'Cold-Call PF',
    }
    LEVEL_ORDER  = ['level_1', 'level_2', 'level_3']
    LEVEL_LABELS = {'level_1': 'Nivel 1 — Iniciando',
                    'level_2': 'Nivel 2 — Reconociendo',
                    'level_3': 'Nivel 3 — Aplicando'}

    rq = g.get('REASONING_QUESTIONS', {})
    lu = g.get('LEVEL_UP_TESTS',      {})

    def _get_level(drill):
        return st.session_state.sm2_levels.get(drill, 'level_1')

    def _set_level(drill, level):
        st.session_state.sm2_levels[drill] = level

    # ── selector de drill ─────────────────────────────────────────────────────
    available_drills = [d for d in DRILL_LABELS if d in rq]

    col_sel, col_info = st.columns([2, 3])
    with col_sel:
        st.markdown('<div class="section-title">📋 Selecciona drill</div>',
                    unsafe_allow_html=True)
        selected_drill = st.selectbox(
            "Drill",
            options=available_drills,
            format_func=lambda d: DRILL_LABELS.get(d, d),
            key='sm2_drill_select',
            label_visibility='collapsed',
        )

    with col_info:
        # Panel de estado de todos los drills
        st.markdown('<div class="section-title">📊 Estado de niveles</div>',
                    unsafe_allow_html=True)
        cols_info = st.columns(len(available_drills))
        for ci, dd in enumerate(available_drills):
            lv = _get_level(dd)
            lv_num = LEVEL_ORDER.index(lv) + 1 if lv in LEVEL_ORDER else 1
            q_count = len(rq.get(dd, {}).get(lv, []))
            lu_key  = f"{lv}_to_{LEVEL_ORDER[min(lv_num, len(LEVEL_ORDER)-1)]}"
            has_lu  = lu_key in lu.get(dd, {})
            with cols_info[ci]:
                st.markdown(
                    f"""<div style="background:#0a0f1e;border:1px solid {'#a78bfa' if dd==selected_drill else '#1e3a5f'};
                        border-radius:8px;padding:8px 10px;text-align:center;">
                        <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;
                            color:#60a5fa;text-transform:uppercase;">{DRILL_LABELS[dd]}</div>
                        <div style="font-size:1.1rem;color:#e8e8f0;font-weight:700;">Nv.{lv_num}</div>
                        <div style="font-size:.7rem;color:#4b4b6a;">{q_count} preguntas</div>
                        {'<div style="font-size:.65rem;color:#a78bfa;">⬆ LevelUp disponible</div>' if has_lu else ''}
                    </div>""",
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # ── tabs internos del drill seleccionado ──────────────────────────────────
    itab_rq, itab_lu, itab_hist, itab_cog, itab_sess = st.tabs(
        ["💭 Razonamiento", "⬆ Level-Up Test", "📜 Progreso",
         "💬 Cognitivo", "🎓 Sesión completa"])

    # ──────────────────────────────────────────────────────────────────────────
    # INNER TAB A — RAZONAMIENTO SM-2
    # ──────────────────────────────────────────────────────────────────────────
    with itab_rq:
        current_level = _get_level(selected_drill)
        questions_for_level = rq.get(selected_drill, {}).get(current_level, [])

        st.markdown(
            f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;border-radius:10px;
                padding:12px 18px;margin-bottom:16px;display:flex;justify-content:space-between;
                align-items:center;">
                <div>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:.75rem;
                        color:#60a5fa;text-transform:uppercase;">Drill activo</span><br>
                    <span style="color:#e8e8f0;font-size:.95rem;font-weight:600;">
                        {DRILL_LABELS.get(selected_drill, selected_drill)}</span>
                </div>
                <div style="text-align:right;">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:.75rem;
                        color:#a78bfa;">{LEVEL_LABELS.get(current_level,'—')}</span><br>
                    <span style="font-size:.72rem;color:#4b4b6a;">
                        {len(questions_for_level)} preguntas disponibles</span>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

        if not questions_for_level:
            st.warning(f"Sin preguntas para {selected_drill} / {current_level}.")
        else:
            qs = st.session_state.sm2_q_state

            # ── arranque / navegación ──────────────────────────────────────
            col_rq1, col_rq2, col_rq3 = st.columns([1, 1, 1])
            with col_rq1:
                n_sel = st.selectbox("Nº preguntas", [1, 2, 3, 4, 5],
                                     index=2, key='sm2_n_questions')
            with col_rq2:
                if st.button("▶ Nueva sesión", type="primary",
                              use_container_width=True, key='sm2_start'):
                    import random as _rnd
                    pool = list(questions_for_level)
                    _rnd.shuffle(pool)
                    st.session_state.sm2_q_state = {
                        'drill':     selected_drill,
                        'level':     current_level,
                        'questions': pool[:n_sel],
                        'idx':       0,
                        'phase':     'question',   # 'question' | 'answer' | 'done'
                        'n_correct': 0,
                    }
                    st.rerun()
            with col_rq3:
                if st.button("✖ Limpiar", use_container_width=True, key='sm2_clear'):
                    st.session_state.sm2_q_state = None
                    st.rerun()

            qs = st.session_state.sm2_q_state

            if qs and qs.get('drill') == selected_drill and qs.get('level') == current_level:
                questions = qs['questions']
                idx       = qs['idx']
                phase     = qs['phase']
                total     = len(questions)

                if phase == 'done':
                    # ── sesión completada ──────────────────────────────────
                    score = qs.get('n_correct', 0)
                    st.markdown(
                        f"""<div style="background:linear-gradient(135deg,#0a1a0a,#0a0f1e);
                            border:1px solid #22c55e;border-radius:12px;padding:24px;text-align:center;">
                            <div style="font-size:2rem;">{'🏆' if score==total else '✅'}</div>
                            <div style="color:#22c55e;font-size:1.1rem;font-weight:700;margin:8px 0;">
                                Sesión completada — {score}/{total} correctas</div>
                            <div style="color:#4b4b6a;font-size:.82rem;">
                                Drill: {DRILL_LABELS.get(selected_drill,selected_drill)} ·
                                {LEVEL_LABELS.get(current_level,'')}</div>
                        </div>""",
                        unsafe_allow_html=True
                    )
                    if score == total and total >= 2:
                        lv_idx = LEVEL_ORDER.index(current_level) if current_level in LEVEL_ORDER else 0
                        lu_key_chk = f"{current_level}_to_{LEVEL_ORDER[min(lv_idx+1,len(LEVEL_ORDER)-1)]}"
                        if lu_key_chk in lu.get(selected_drill, {}):
                            st.info("🎯 Puntuación perfecta — puedes intentar el Level-Up Test en la pestaña ⬆")

                elif 0 <= idx < total:
                    q = questions[idx]
                    progress = (idx) / total
                    st.progress(progress,
                                text=f"Pregunta {idx+1} de {total}")

                    # ── tarjeta de pregunta ────────────────────────────────
                    st.markdown(
                        f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;
                            border-radius:12px;padding:20px 24px;margin:12px 0;">
                            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;
                                color:#60a5fa;text-transform:uppercase;margin-bottom:10px;">
                                {'🔢 Cálculo' if q.get('tipo')=='calculo' else '💡 Conceptual'}
                                · {DRILL_LABELS.get(selected_drill,selected_drill)}
                            </div>
                            <div style="color:#e8e8f0;font-size:.92rem;line-height:1.6;">
                                {q['pregunta']}
                            </div>
                            {f'<div style="background:#0f1629;border-left:3px solid #a78bfa;border-radius:0 6px 6px 0;padding:10px 14px;margin-top:14px;font-family:JetBrains Mono,monospace;font-size:.8rem;color:#a78bfa;">💡 Hay un cálculo concreto — trabájalo antes de revelar.</div>' if q.get('calculo') else ''}
                        </div>""",
                        unsafe_allow_html=True
                    )

                    if phase == 'question':
                        col_a, col_b = st.columns([3, 1])
                        with col_b:
                            if st.button("👁 Revelar respuesta", type="primary",
                                          use_container_width=True, key=f'sm2_reveal_{idx}'):
                                st.session_state.sm2_q_state['phase'] = 'answer'
                                st.rerun()

                    elif phase == 'answer':
                        # ── cálculo ───────────────────────────────────────
                        if q.get('calculo'):
                            st.markdown(
                                f"""<div style="background:#0f1629;border-left:3px solid #a78bfa;
                                    border-radius:0 8px 8px 0;padding:14px 18px;margin:10px 0;
                                    font-family:'JetBrains Mono',monospace;font-size:.82rem;
                                    color:#c4b5fd;line-height:1.6;">
                                    📐 <b>Cálculo:</b><br>{q['calculo']}
                                </div>""",
                                unsafe_allow_html=True
                            )
                        # ── respuesta ─────────────────────────────────────
                        st.markdown(
                            f"""<div style="background:#0a1a0a;border:1px solid #22c55e;
                                border-radius:10px;padding:16px 20px;margin:10px 0;">
                                <div style="color:#22c55e;font-weight:700;font-size:.8rem;
                                    text-transform:uppercase;margin-bottom:8px;">✅ Respuesta</div>
                                <div style="color:#e8e8f0;font-size:.9rem;line-height:1.6;">
                                    {q['respuesta']}
                                </div>
                            </div>""",
                            unsafe_allow_html=True
                        )
                        # ── aplicación ────────────────────────────────────
                        if q.get('aplicacion'):
                            st.markdown(
                                f"""<div style="background:#0f0a1a;border:1px solid #4c1d95;
                                    border-radius:10px;padding:14px 18px;margin:6px 0;">
                                    <div style="color:#a78bfa;font-size:.75rem;
                                        text-transform:uppercase;margin-bottom:6px;">
                                        🎯 Aplicación a tus datos</div>
                                    <div style="color:#94a3b8;font-size:.86rem;line-height:1.55;">
                                        {q['aplicacion']}
                                    </div>
                                </div>""",
                                unsafe_allow_html=True
                            )
                        if q.get('followup'):
                            with st.expander("🔍 Profundizar"):
                                st.markdown(
                                    f'<div style="color:#6b6b8a;font-size:.83rem;line-height:1.55;">'
                                    f'{q["followup"]}</div>',
                                    unsafe_allow_html=True
                                )

                        # ── autoevaluación ────────────────────────────────
                        st.markdown(
                            '<div style="color:#4b4b6a;font-size:.78rem;margin-top:14px;">'
                            '¿Lo tenías claro?</div>',
                            unsafe_allow_html=True
                        )
                        col_ev1, col_ev2, col_ev3 = st.columns(3)
                        def _advance(correct):
                            qs = st.session_state.sm2_q_state
                            if correct:
                                qs['n_correct'] = qs.get('n_correct', 0) + 1
                            next_idx = qs['idx'] + 1
                            if next_idx >= len(qs['questions']):
                                qs['phase'] = 'done'
                            else:
                                qs['idx']   = next_idx
                                qs['phase'] = 'question'
                            st.rerun()

                        with col_ev1:
                            if st.button("✅ Sí, claro", use_container_width=True,
                                          key=f'sm2_yes_{idx}'):
                                _advance(True)
                        with col_ev2:
                            if st.button("⚠️ Parcial", use_container_width=True,
                                          key=f'sm2_partial_{idx}'):
                                _advance(False)
                        with col_ev3:
                            if st.button("❌ No", use_container_width=True,
                                          key=f'sm2_no_{idx}'):
                                _advance(False)

    # ──────────────────────────────────────────────────────────────────────────
    # INNER TAB B — LEVEL-UP TEST
    # ──────────────────────────────────────────────────────────────────────────
    with itab_lu:
        current_level_lu = _get_level(selected_drill)
        lv_idx_lu = LEVEL_ORDER.index(current_level_lu) if current_level_lu in LEVEL_ORDER else 0
        next_level = LEVEL_ORDER[min(lv_idx_lu + 1, len(LEVEL_ORDER) - 1)]
        lu_key_active = f"{current_level_lu}_to_{next_level}"
        lu_questions  = lu.get(selected_drill, {}).get(lu_key_active, [])

        st.markdown(
            f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;border-radius:10px;
                padding:14px 18px;margin-bottom:16px;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:.75rem;
                    color:#60a5fa;text-transform:uppercase;">Level-Up Test</span><br>
                <span style="color:#e8e8f0;font-size:.92rem;font-weight:600;">
                    {DRILL_LABELS.get(selected_drill,selected_drill)}</span>
                <span style="color:#4b4b6a;font-size:.82rem;margin-left:12px;">
                    {LEVEL_LABELS.get(current_level_lu,'')} → {LEVEL_LABELS.get(next_level,'')}</span><br>
                <span style="color:#94a3b8;font-size:.78rem;">
                    Necesitas 2/{len(lu_questions) if lu_questions else 3} correctas para subir de nivel.</span>
            </div>""",
            unsafe_allow_html=True
        )

        if not lu_questions:
            if current_level_lu == LEVEL_ORDER[-1]:
                st.success("🏆 Nivel máximo alcanzado en este drill.")
            else:
                st.info("Sin test de level-up para este drill/nivel.")
        else:
            lu_s = st.session_state.sm2_lu_state

            col_lu1, col_lu2 = st.columns([1, 2])
            with col_lu1:
                if st.button("▶ Iniciar Level-Up Test", type="primary",
                              use_container_width=True, key='lu_start'):
                    st.session_state.sm2_lu_state = {
                        'drill':     selected_drill,
                        'level_key': lu_key_active,
                        'next_level': next_level,
                        'questions': lu_questions,
                        'idx':       0,
                        'answers':   {},
                        'phase':     'q',    # 'q' | 'feedback' | 'result'
                        'current_choice': None,
                    }
                    st.rerun()
            with col_lu2:
                if st.button("✖ Resetear test", use_container_width=True, key='lu_reset'):
                    st.session_state.sm2_lu_state = None
                    st.rerun()

            lu_s = st.session_state.sm2_lu_state

            if (lu_s and lu_s.get('drill') == selected_drill
                    and lu_s.get('level_key') == lu_key_active):

                lu_qs    = lu_s['questions']
                lu_idx   = lu_s['idx']
                lu_phase = lu_s['phase']
                answers  = lu_s['answers']

                if lu_phase == 'result':
                    # ── resultado final ────────────────────────────────────
                    n_correct = sum(1 for i, q in enumerate(lu_qs)
                                    if answers.get(i) == q['correcta'])
                    needed  = max(2, (len(lu_qs) * 2) // 3)
                    passed  = n_correct >= needed
                    color   = '#22c55e' if passed else '#ef4444'
                    icon    = '🏆' if passed else '📚'
                    msg     = 'APROBADO — ¡Nivel desbloqueado!' if passed else f'No aprobado — necesitabas {needed}/{len(lu_qs)}'

                    st.markdown(
                        f"""<div style="background:#0a0f1e;border:2px solid {color};
                            border-radius:12px;padding:24px;text-align:center;margin-bottom:16px;">
                            <div style="font-size:2.5rem;">{icon}</div>
                            <div style="color:{color};font-size:1.1rem;font-weight:700;margin:10px 0;">
                                {n_correct}/{len(lu_qs)} correctas — {msg}</div>
                        </div>""",
                        unsafe_allow_html=True
                    )

                    if passed:
                        if st.button("⬆ Confirmar subida de nivel", type="primary",
                                      use_container_width=True, key='lu_levelup_confirm'):
                            _set_level(selected_drill, lu_s['next_level'])
                            st.session_state.sm2_lu_state = None
                            st.success(f"✅ Nivel actualizado → {LEVEL_LABELS.get(lu_s['next_level'],'')}")
                            st.rerun()
                    else:
                        st.info("Repasa las preguntas de Razonamiento y vuelve a intentarlo.")

                    # ── revisión de respuestas ─────────────────────────────
                    st.markdown('<div class="section-title">📋 Revisión</div>',
                                unsafe_allow_html=True)
                    for ri, rq_item in enumerate(lu_qs):
                        chosen  = answers.get(ri, '?')
                        correct = rq_item['correcta']
                        ok      = chosen == correct
                        border  = '#22c55e' if ok else '#ef4444'
                        st.markdown(
                            f"""<div style="background:#0a0f1e;border:1px solid {border};
                                border-radius:8px;padding:12px 16px;margin-bottom:8px;">
                                <div style="color:#e8e8f0;font-size:.88rem;margin-bottom:8px;">
                                    {'✅' if ok else '❌'} <b>P{ri+1}:</b> {rq_item['pregunta']}</div>
                                <div style="font-size:.82rem;color:#94a3b8;">
                                    Tu respuesta: <b style="color:{'#22c55e' if ok else '#ef4444'};">{chosen}</b>
                                    {'· ' if not ok else ''}
                                    {'Correcta: <b style="color:#22c55e;">'+correct+'</b>' if not ok else ''}
                                </div>
                                <div style="font-size:.8rem;color:#6b6b8a;margin-top:6px;
                                    border-top:1px solid #1e1e3a;padding-top:6px;">
                                    {rq_item['explicacion']}
                                </div>
                            </div>""",
                            unsafe_allow_html=True
                        )

                elif lu_phase in ('q', 'feedback') and 0 <= lu_idx < len(lu_qs):
                    q_lu = lu_qs[lu_idx]
                    st.progress(lu_idx / len(lu_qs),
                                text=f"Pregunta {lu_idx+1} de {len(lu_qs)}")

                    st.markdown(
                        f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;
                            border-radius:12px;padding:20px 24px;margin:12px 0;">
                            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;
                                color:#60a5fa;text-transform:uppercase;margin-bottom:10px;">
                                Pregunta {lu_idx+1}</div>
                            <div style="color:#e8e8f0;font-size:.92rem;line-height:1.6;
                                margin-bottom:16px;">{q_lu['pregunta']}</div>
                            <div style="display:flex;flex-direction:column;gap:6px;">
                        """,
                        unsafe_allow_html=True
                    )

                    if lu_phase == 'q':
                        # Mostrar opciones como botones
                        for opt in q_lu['opciones']:
                            opt_letter = opt[0]
                            if st.button(opt, use_container_width=True,
                                          key=f'lu_opt_{lu_idx}_{opt_letter}'):
                                lu_s['answers'][lu_idx]     = opt_letter
                                lu_s['current_choice']       = opt_letter
                                lu_s['phase']                = 'feedback'
                                st.rerun()

                    elif lu_phase == 'feedback':
                        chosen  = lu_s.get('current_choice', '?')
                        correct = q_lu['correcta']
                        ok      = chosen == correct
                        color   = '#22c55e' if ok else '#ef4444'

                        # Mostrar opciones con colores
                        for opt in q_lu['opciones']:
                            opt_letter = opt[0]
                            if opt_letter == correct:
                                bg_c = '#0a1a0a'; border_c = '#22c55e'; tc = '#22c55e'
                            elif opt_letter == chosen and not ok:
                                bg_c = '#1a0a0a'; border_c = '#ef4444'; tc = '#ef4444'
                            else:
                                bg_c = '#0a0a14'; border_c = '#1e1e3a'; tc = '#4b4b6a'
                            st.markdown(
                                f"""<div style="background:{bg_c};border:1px solid {border_c};
                                    border-radius:6px;padding:8px 14px;margin-bottom:4px;
                                    font-size:.86rem;color:{tc};">{opt}</div>""",
                                unsafe_allow_html=True
                            )

                        st.markdown(
                            f"""<div style="background:{'#0a1a0a' if ok else '#1a0a0a'};
                                border-left:3px solid {color};border-radius:0 8px 8px 0;
                                padding:12px 16px;margin-top:12px;font-size:.84rem;color:{color};">
                                {'✅ Correcto' if ok else '❌ Incorrecto'} — {q_lu['explicacion']}
                            </div>""",
                            unsafe_allow_html=True
                        )

                        next_btn_label = ("Ver resultado" if lu_idx == len(lu_qs) - 1
                                          else "Siguiente →")
                        if st.button(next_btn_label, type="primary",
                                      use_container_width=True, key=f'lu_next_{lu_idx}'):
                            if lu_idx + 1 >= len(lu_qs):
                                lu_s['phase'] = 'result'
                            else:
                                lu_s['idx']   = lu_idx + 1
                                lu_s['phase'] = 'q'
                                lu_s['current_choice'] = None
                            st.rerun()

    # ──────────────────────────────────────────────────────────────────────────
    # INNER TAB C — PROGRESO
    # ──────────────────────────────────────────────────────────────────────────
    with itab_hist:
        st.markdown('<div class="section-title">📜 Estado de progreso por drill</div>',
                    unsafe_allow_html=True)

        for dd in available_drills:
            lv      = _get_level(dd)
            lv_idx2 = LEVEL_ORDER.index(lv) if lv in LEVEL_ORDER else 0
            lv_num2 = lv_idx2 + 1
            fill    = (lv_idx2 / max(len(LEVEL_ORDER)-1, 1)) * 100
            color_p = '#22c55e' if lv_num2 == 3 else '#60a5fa' if lv_num2 == 2 else '#4b4b6a'

            # Level-up disponible?
            lu_key_p = f"{lv}_to_{LEVEL_ORDER[min(lv_idx2+1, len(LEVEL_ORDER)-1)]}"
            has_lu_p = lu_key_p in lu.get(dd, {}) and lv_num2 < len(LEVEL_ORDER)

            st.markdown(
                f"""<div style="background:#0a0f1e;border:1px solid #1e3a5f;border-radius:10px;
                    padding:14px 18px;margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;
                        margin-bottom:10px;">
                        <div>
                            <span style="font-family:'JetBrains Mono',monospace;font-size:.75rem;
                                color:#60a5fa;text-transform:uppercase;">{DRILL_LABELS[dd]}</span><br>
                            <span style="color:#e8e8f0;font-size:.85rem;">{LEVEL_LABELS.get(lv,'')}</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:1.3rem;color:{color_p};font-weight:700;">
                                {'🏆' if lv_num2==3 else f'Nv.{lv_num2}'}</span>
                            {'<span style="font-size:.72rem;color:#a78bfa;display:block;">⬆ Level-Up disponible</span>' if has_lu_p else ''}
                        </div>
                    </div>
                    <div style="background:#1e1e3a;border-radius:4px;height:6px;">
                        <div style="background:{color_p};width:{fill:.0f}%;height:6px;
                            border-radius:4px;transition:width .3s;"></div>
                    </div>
                </div>""",
                unsafe_allow_html=True
            )

        # Botón reset niveles
        st.markdown("---")
        col_reset1, col_reset2 = st.columns([1, 3])
        with col_reset1:
            if st.button("🔄 Reset todos los niveles", key='sm2_reset_all'):
                st.session_state.sm2_levels     = {}
                st.session_state.sm2_q_state    = None
                st.session_state.sm2_lu_state   = None
                st.rerun()
        with col_reset2:
            st.markdown(
                '<span style="color:#3d3d6e;font-size:.78rem;">'
                'Resetea el progreso de niveles de todos los drills. '
                'No afecta a las manos ni al análisis.</span>',
                unsafe_allow_html=True
            )

        # Display study progress if available
        if 'display_study_progress' in g:
            st.markdown('<div class="section-title">📈 Historial de estudio (M7)</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_study_progress'])
            if out.strip():
                st.code(out.strip(), language=None)

        # M7 status por drill activo
        if 'display_m7_status' in g and drill_activo:
            st.markdown('<div class="section-title">🗂 Estado M7 del drill activo</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_m7_status'], drill_activo)
            if out.strip():
                st.code(out.strip(), language=None)
            else:
                st.caption(f"Sin historial M7 para {drill_activo} aún.")

    # ──────────────────────────────────────────────────────────────────────────
    # INNER TAB D — REVISIÓN COGNITIVA + CHAT
    # ──────────────────────────────────────────────────────────────────────────
    with itab_cog:
        st.markdown('<div class="section-title">💬 Revisión cognitiva de manos</div>',
                    unsafe_allow_html=True)

        # Revisión cognitiva estructurada (display_cognitive_review)
        if 'display_cognitive_review' in g and selected_drill:
            st.markdown('<div class="section-title">🔍 Revisión del spot</div>',
                        unsafe_allow_html=True)
            out = _safe_capture(g['display_cognitive_review'],
                                df, selected_drill, n_hands=5)
            if out.strip():
                st.code(out.strip(), language=None)
            else:
                st.caption("Disponible con manos del spot activo en el HH cargado.")

        # Chat cognitivo sobre mano concreta (run_cognitive_chat via Groq)
        st.markdown('<div class="section-title">💬 Chat cognitivo sobre una mano</div>',
                    unsafe_allow_html=True)
        if not groq_key:
            st.info("Introduce tu GROQ_API_KEY en la barra lateral para activar el chat cognitivo.")
        elif 'run_cognitive_chat' in g:
            # Selector de mano de alto impacto
            if 'get_high_impact_hands' in g:
                try:
                    hi_hands = g['get_high_impact_hands'](df, session_id=current_session_id)
                    if hi_hands is not None and len(hi_hands) > 0:
                        hand_options = [str(h) for h in hi_hands.get('hand_id', hi_hands.index)[:6]] \
                                       if hasattr(hi_hands, 'get') else []
                        if not hand_options and hasattr(hi_hands, '__len__'):
                            hand_options = [str(h) for h in list(hi_hands)[:6]]
                    else:
                        hand_options = []
                except Exception:
                    hand_options = []
            else:
                hand_options = []

            cog_hand = st.text_input(
                "Hand ID o descripción de la mano (ej: AKo BTN vs BB, misseé cbet flop K72)",
                key='cog_hand_input'
            )
            cog_razon = st.text_area(
                "Tu razonamiento en la mano (¿qué pensaste? ¿por qué tomaste esa decisión?)",
                height=100, key='cog_razon_input'
            )

            if st.button("🧠 Analizar con coach", type="primary", key='cog_submit'):
                if cog_hand and cog_razon:
                    import os as _os; _os.environ['GROQ_API_KEY'] = groq_key
                    with st.spinner("Analizando..."):
                        buf_cog = __import__('io').StringIO()
                        old_cog = __import__('sys').stdout
                        __import__('sys').stdout = buf_cog
                        try:
                            g['run_cognitive_chat'](
                                hand_context=cog_hand,
                                razonamiento_jugador=cog_razon,
                                overall_metrics=R['overall_metrics'],
                                spot_identifier=selected_drill,
                                drill_activo=selected_drill,
                                mode=mode,
                                api_key=groq_key,
                                use_groq=True,
                            )
                        except Exception as _ce:
                            print(f"Error: {_ce}")
                        finally:
                            __import__('sys').stdout = old_cog
                    out_cog = buf_cog.getvalue()
                    if out_cog.strip():
                        st.code(out_cog.strip(), language=None)
                    else:
                        st.warning("Sin respuesta del coach. Verifica la GROQ_API_KEY.")
                else:
                    st.warning("Completa la mano y el razonamiento antes de analizar.")

    # ──────────────────────────────────────────────────────────────────────────
    # INNER TAB E — SESIÓN COMPLETA (run_study_session)
    # ──────────────────────────────────────────────────────────────────────────
    with itab_sess:
        st.markdown('<div class="section-title">🎓 Sesión de estudio completa</div>',
                    unsafe_allow_html=True)
        st.markdown(
            """<div style="background:#0a0f1e;border:1px solid #1e3a5f;border-radius:10px;
                padding:14px 18px;margin-bottom:16px;font-size:.85rem;color:#94a3b8;">
                <b style="color:#60a5fa;">run_study_session</b> — orquestador completo de aprendizaje.<br>
                Decide automáticamente qué estudiar: bridge de errores, SM-2 pendiente,
                preguntas de razonamiento o sesión postflop. Integra M4+M7+SunChat.
            </div>""",
            unsafe_allow_html=True
        )

        col_ss1, col_ss2 = st.columns([1, 1])
        with col_ss1:
            ss_modo_rapido = st.checkbox("⚡ Modo rápido (10 min)", value=True, key='ss_rapido')
        with col_ss2:
            ss_level = st.selectbox("Nivel actual", ['level_1','level_2','level_3'],
                                    index=['level_1','level_2','level_3'].index(
                                        st.session_state.sm2_levels.get(selected_drill,'level_1')),
                                    key='ss_level')

        if 'run_study_session' in g:
            if st.button("▶ Iniciar sesión de estudio", type="primary",
                          use_container_width=True, key='ss_start'):
                with st.spinner("Preparando sesión de estudio..."):
                    import io as _io2, sys as _sys2, unittest.mock as _mock2
                    _buf_ss = _io2.StringIO()
                    _old_ss = _sys2.stdout; _sys2.stdout = _buf_ss
                    try:
                        with _mock2.patch('builtins.input', return_value=''):
                            g['run_study_session'](
                                df=df,
                                session_id=current_session_id,
                                drill_activo=selected_drill,
                                current_level=ss_level,
                                modo_rapido=ss_modo_rapido,
                            )
                    except Exception as _sse:
                        print(f"Error en run_study_session: {_sse}")
                    finally:
                        _sys2.stdout = _old_ss
                out_ss = _buf_ss.getvalue()
                if out_ss.strip():
                    st.code(out_ss.strip(), language=None)
                else:
                    st.info("Sesión completada. Revisa el progreso en la pestaña 📜 Progreso.")
        else:
            st.warning("run_study_session no disponible en esta versión de os_library.")


# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""<div style="text-align:center;font-family:'JetBrains Mono',monospace;
    font-size:.72rem;color:#2d2d4e;padding:8px;">
    OS v2.0 · LaRuinaDeMago · NL2 → NL25+ · El sistema mide, tú decides.
</div>""", unsafe_allow_html=True)
