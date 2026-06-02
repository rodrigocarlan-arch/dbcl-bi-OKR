import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io, requests
from datetime import date

st.set_page_config(page_title="DBCL — OKR 2026", page_icon="🎯", layout="wide",
                   initial_sidebar_state="expanded")

OKR_ID = "1WI7ogJK_s0gcDbMVFBtb0BuxzCWyyzmO"

# ── Brand CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Tomorrow:wght@400;600;700;900&display=swap');

@keyframes fadeUp { from { opacity:0; transform:translateY(7px) } to { opacity:1; transform:translateY(0) } }
@keyframes pulse  { 0%,100% { opacity:1 } 50% { opacity:.2 } }
@keyframes prog   { from { width:0 } }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
.main, section.main, .block-container,
[data-testid="block-container"] {
    background-color: #FAF7EC !important;
    color: #23282E !important;
    font-family: 'Lora', Georgia, serif !important;
}
* { box-sizing: border-box; }

[data-testid="stSidebar"] {
    background: #003C28 !important;
    border-right: 1px solid rgba(0,255,0,.12) !important;
}
[data-testid="stSidebar"] * { color: #FAF7EC !important; font-family: 'Tomorrow', sans-serif !important; }
[data-testid="stSidebar"] hr { border-color: rgba(0,255,0,.15) !important; margin: 12px 0 !important; }
[data-testid="stSidebar"] label {
    color: rgba(250,247,236,.5) !important;
    font-size: 9px !important;
    text-transform: uppercase !important;
    letter-spacing: 2.5px !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"] label span {
    font-size: 11px !important;
    letter-spacing: .3px !important;
    text-transform: none !important;
    white-space: nowrap !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(0,255,0,.12) !important;
    border: 1px solid rgba(0,255,0,.3) !important;
    border-radius: 2px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #FAF7EC !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] [role="button"],
[data-testid="stSidebar"] [data-baseweb="tag"] button { color: rgba(0,255,0,.7) !important; }
[data-testid="stSidebar"] input {
    background: rgba(250,247,236,.07) !important;
    border: 1px solid rgba(0,255,0,.25) !important;
    border-radius: 2px !important;
    color: #FAF7EC !important;
    font-size: 12px !important;
}

/* Header */
.hdr {
    background: #003C28;
    border-radius: 2px;
    border: 1px solid rgba(0,255,0,.15);
    padding: 20px 28px 18px;
    margin-bottom: 22px;
    display: flex; align-items: center; gap: 20px;
    animation: fadeUp .3s ease;
}
.hdr-logo { display:flex; flex-direction:column; gap:2px; padding-right:20px; border-right:1px solid rgba(250,247,236,.18); flex-shrink:0; }
.hdr-logo .dbcl { font-family:'Tomorrow',sans-serif; font-size:20px; font-weight:700; color:#FAF7EC; line-height:1; letter-spacing:1px; }
.hdr-logo .adv  { font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:400; color:rgba(250,247,236,.5); letter-spacing:4px; text-transform:uppercase; }
.hdr-ctx { display:flex; flex-direction:column; gap:3px; padding-left:4px; }
.hdr-ctx .pg  { font-family:'Tomorrow',sans-serif; font-size:13px; font-weight:600; color:#FAF7EC; }
.hdr-ctx .sub { font-family:'Tomorrow',sans-serif; font-size:9px; color:rgba(250,247,236,.5); letter-spacing:1.5px; text-transform:uppercase; }
.hdr-right { margin-left:auto; display:flex; align-items:center; gap:6px; font-family:'Tomorrow',sans-serif; font-size:9px; color:rgba(0,255,0,.7); letter-spacing:2px; text-transform:uppercase; }
.hdr-dot { width:6px; height:6px; border-radius:50%; background:#00FF00; animation:pulse 2s infinite; }

/* KPI */
.kpi { background:#003C28; border-radius:2px; padding:16px 18px 14px; border-left:3px solid #00FF00; margin-bottom:6px; animation:fadeUp .25s ease; }
.kpi.dim   { border-left-color:rgba(0,255,0,.35); }
.kpi.warn  { border-left-color:#F0E8C8; }
.kpi.alert { border-left-color:#C0392B; }
.kpi .lbl  { font-family:'Tomorrow',sans-serif; font-size:9px; font-weight:700; color:rgba(250,247,236,.5); text-transform:uppercase; letter-spacing:2.5px; margin-bottom:8px; }
.kpi .val  { font-family:'Tomorrow',sans-serif; font-size:20px; font-weight:700; color:#FAF7EC; line-height:1; letter-spacing:-.3px; }
.kpi .sub  { font-family:'Tomorrow',sans-serif; font-size:10px; color:rgba(250,247,236,.45); margin-top:6px; letter-spacing:.5px; }

/* Section */
.sec {
    font-family:'Tomorrow',sans-serif; font-size:10px; font-weight:700;
    color:rgba(0,60,40,.75); text-transform:uppercase; letter-spacing:2.5px;
    border-left:1.5px solid #00FF00; padding:6px 12px;
    background:rgba(0,255,0,.05); border-radius:0 2px 2px 0;
    margin:20px 0 10px; animation:fadeUp .25s ease;
}

/* OKR cards */
.obj-card {
    background:#003C28; border-radius:2px; border:1px solid rgba(0,255,0,.15);
    padding:20px 24px; margin-bottom:12px; animation:fadeUp .25s ease;
}
.obj-card .obj-label { font-family:'Tomorrow',sans-serif; font-size:9px; font-weight:700; color:rgba(0,255,0,.6); text-transform:uppercase; letter-spacing:2.5px; margin-bottom:4px; }
.obj-card .obj-title { font-family:'Lora',serif; font-size:16px; font-weight:700; color:#FAF7EC; line-height:1.4; margin-bottom:14px; }
.obj-card .obj-bar-bg { background:rgba(0,255,0,.12); border-radius:1px; height:4px; width:100%; }
.obj-card .obj-bar-fg { background:#00FF00; border-radius:1px; height:4px; animation:prog .8s ease; }
.obj-card .obj-stats  { font-family:'Tomorrow',sans-serif; font-size:9px; color:rgba(250,247,236,.5); margin-top:6px; letter-spacing:1px; }

.kr-card {
    background:rgba(0,255,0,.04); border-radius:2px;
    border:1px solid rgba(0,255,0,.15); border-left:3px solid rgba(0,255,0,.5);
    padding:14px 18px; margin:8px 0;
}
.kr-card .kr-label { font-family:'Tomorrow',sans-serif; font-size:9px; color:rgba(0,255,0,.6); text-transform:uppercase; letter-spacing:2px; margin-bottom:3px; }
.kr-card .kr-title  { font-family:'Lora',serif; font-size:14px; font-weight:600; color:#23282E; line-height:1.4; }
.kr-card .kr-meta   { font-family:'Tomorrow',sans-serif; font-size:9px; color:#8FB89A; margin-top:8px; letter-spacing:.5px; }

.ini-card {
    background:#FFFFFF; border-radius:2px;
    border-left:3px solid #D4C9A8;
    padding:12px 16px; margin:6px 0 4px 16px;
    border-bottom:1px solid rgba(0,60,40,.06);
}
.ini-card .ini-title { font-family:'Lora',serif; font-size:13px; color:#003C28; font-weight:600; line-height:1.4; }
.ini-card .ini-meta  { font-family:'Tomorrow',sans-serif; font-size:9px; color:#8FB89A; margin-top:5px; letter-spacing:.5px; }

.acao-row {
    padding:8px 16px 8px 32px; border-bottom:1px solid rgba(0,60,40,.05);
    background: rgba(250,247,236,.5);
}
.acao-row .acao-text { font-family:'Lora',serif; font-size:12px; color:#23282E; line-height:1.5; }
.acao-row .acao-meta { font-family:'Tomorrow',sans-serif; font-size:9px; color:#8FB89A; margin-top:3px; letter-spacing:.5px; }

/* Status badges */
.badge {
    display:inline-block; font-family:'Tomorrow',sans-serif;
    font-size:8px; font-weight:700; text-transform:uppercase;
    letter-spacing:2px; padding:2px 8px; border-radius:2px;
}
.badge-andamento { background:rgba(0,255,0,.12); color:#1A6B45; border:1px solid rgba(0,255,0,.3); }
.badge-iniciar   { background:rgba(212,201,168,.3); color:#5A4A28; border:1px solid rgba(212,201,168,.5); }
.badge-concluido { background:rgba(26,107,69,.15); color:#003C28; border:1px solid rgba(26,107,69,.3); }
.badge-atrasado  { background:rgba(192,57,43,.12); color:#7B1A0E; border:1px solid rgba(192,57,43,.25); }

/* Priority */
.p1 { display:inline-block; font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:900; color:#00FF00; border:1px solid rgba(0,255,0,.4); padding:1px 6px; border-radius:2px; letter-spacing:1px; margin-left:6px; }
.p2 { display:inline-block; font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:700; color:#D4C9A8; border:1px solid rgba(212,201,168,.4); padding:1px 6px; border-radius:2px; letter-spacing:1px; margin-left:6px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background:rgba(0,60,40,.06); border-radius:2px; padding:3px; gap:2px; border:1px solid rgba(0,255,0,.1); }
.stTabs [data-baseweb="tab"] { border-radius:2px; padding:7px 18px; font-family:'Tomorrow',sans-serif !important; font-size:10px !important; font-weight:600 !important; text-transform:uppercase !important; letter-spacing:1.5px !important; color:rgba(0,60,40,.5) !important; transition:all .14s; }
.stTabs [aria-selected="true"] { background:#003C28 !important; color:#FAF7EC !important; border:1px solid rgba(0,255,0,.25) !important; }

hr { border:none; border-top:1px solid rgba(0,255,0,.1); margin:18px 0; }
[data-testid="stDataFrame"] { border-radius:2px; overflow:hidden; border:1px solid rgba(0,60,40,.1); }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def hdr(page, sub):
    st.markdown(f"""<div class="hdr">
        <div class="hdr-logo"><div class="dbcl">dbcl</div><div class="adv">Advogados</div></div>
        <div class="hdr-ctx"><div class="pg">{page}</div><div class="sub">{sub}</div></div>
        <div class="hdr-right"><div class="hdr-dot"></div>2026</div>
    </div>""", unsafe_allow_html=True)

def kpi_card(col, label, value, sub='', variant=''):
    with col:
        st.markdown(f"""<div class="kpi {variant}">
            <div class="lbl">{label}</div><div class="val">{value}</div>
            {'<div class="sub">'+sub+'</div>' if sub else ''}
        </div>""", unsafe_allow_html=True)

def sec(title):
    st.markdown(f'<div class="sec">{title}</div>', unsafe_allow_html=True)

def status_badge(s):
    if not isinstance(s, str): return ''
    s_lower = s.lower()
    if 'andamento' in s_lower: return f'<span class="badge badge-andamento">{s}</span>'
    if 'iniciar'   in s_lower: return f'<span class="badge badge-iniciar">{s}</span>'
    if 'concluí'   in s_lower or 'concluido' in s_lower: return f'<span class="badge badge-concluido">{s}</span>'
    if 'atrasad'   in s_lower: return f'<span class="badge badge-atrasado">{s}</span>'
    return f'<span class="badge badge-iniciar">{s}</span>'

def priority_badge(p):
    try:
        v = int(float(p))
        if v == 1: return '<span class="p1">P1</span>'
        if v == 2: return '<span class="p2">P2</span>'
    except: pass
    return ''

def fmt_date(d):
    if pd.isna(d): return '—'
    try:
        dt = pd.to_datetime(d)
        return dt.strftime('%d/%m/%y')
    except: return str(d)[:10]

def is_late(d, status):
    if pd.isna(d): return False
    try:
        dt = pd.to_datetime(d).date()
        s = str(status).lower() if isinstance(status, str) else ''
        return dt < date.today() and 'concluí' not in s
    except: return False

# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch():
    try:
        r = requests.get(
            f"https://docs.google.com/spreadsheets/d/{OKR_ID}/export?format=xlsx",
            timeout=30)
        return r.content if r.status_code == 200 else None
    except: return None

@st.cache_data(show_spinner=False)
def load(b):
    raw = pd.read_excel(io.BytesIO(b), sheet_name=0, header=0)
    raw.columns = [str(c).strip() for c in raw.columns]

    # Rename columns
    cols = list(raw.columns)
    raw = raw.rename(columns={
        cols[0]: 'tipo',
        cols[1]: 'descricao',
        cols[7]: 'dono',
        cols[8]: 'socio',
        cols[9]: 'prazo',
        cols[10]: 'status_mai',
        cols[11]: 'status_jun',
        cols[12]: 'prioridade',
    })

    # Merge description from cols 2-6 if needed (some rows use other cols)
    for c in [cols[2], cols[3], cols[4], cols[5], cols[6]]:
        if c in raw.columns:
            mask = raw['descricao'].isna() & raw[c].notna()
            raw.loc[mask, 'descricao'] = raw.loc[mask, c]

    raw = raw[raw['tipo'].notna()].copy()
    # Filter out repeated header rows
    raw = raw[~raw['tipo'].str.strip().eq('OKR - PLANEJAMENTO ESTRATÉGICO')]

    # Derive level
    def get_level(t):
        t = str(t).strip()
        if t.startswith('Objetivo'): return 'objetivo'
        if t.startswith('KR'):       return 'kr'
        if t.startswith('Inicia'):   return 'iniciativa'
        if t.startswith('Ação'):     return 'acao'
        return 'outro'

    raw['nivel'] = raw['tipo'].apply(get_level)

    # Assign objective and KR context to each row
    curr_obj = curr_kr = curr_obj_desc = curr_kr_desc = None
    ctx_obj = []; ctx_kr = []; ctx_obj_desc = []; ctx_kr_desc = []
    for _, row in raw.iterrows():
        if row['nivel'] == 'objetivo':
            curr_obj = row['tipo']; curr_obj_desc = str(row['descricao']).strip()
            curr_kr = None; curr_kr_desc = None
        elif row['nivel'] == 'kr':
            curr_kr = row['tipo']; curr_kr_desc = str(row['descricao']).strip()
        ctx_obj.append(curr_obj); ctx_kr.append(curr_kr)
        ctx_obj_desc.append(curr_obj_desc); ctx_kr_desc.append(curr_kr_desc)

    raw['ctx_obj']      = ctx_obj
    raw['ctx_kr']       = ctx_kr
    raw['ctx_obj_desc'] = ctx_obj_desc
    raw['ctx_kr_desc']  = ctx_kr_desc

    # Current status = status_mai (most recent filled)
    raw['status'] = raw['status_jun'].where(
        raw['status_jun'].notna() & raw['status_jun'].apply(lambda x: isinstance(x, str)),
        raw['status_mai']
    )
    raw['status'] = raw['status'].apply(
        lambda x: x if isinstance(x, str) else ('A iniciar' if pd.notna(x) else 'A iniciar')
    )

    return raw

# ── Upload fallback ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="padding:20px 4px 14px">
        <div style="font-family:'Tomorrow',sans-serif;font-size:20px;font-weight:700;color:#FAF7EC;letter-spacing:1px">dbcl</div>
        <div style="font-family:'Tomorrow',sans-serif;font-size:8px;color:rgba(250,247,236,.45);letter-spacing:4px;text-transform:uppercase;margin-top:2px">Advogados</div>
        <div style="margin-top:12px;display:flex;align-items:center;gap:6px">
          <div style="width:5px;height:5px;border-radius:50%;background:#00FF00;animation:pulse 2s infinite"></div>
          <span style="font-family:'Tomorrow',sans-serif;font-size:8px;color:rgba(0,255,0,.6);letter-spacing:2px;text-transform:uppercase">OKR 2026</span>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")

    page = st.radio("", [
        "🎯  Visão Geral",
        "📌  Por Objetivo",
        "👤  Por Responsável",
        "🔥  Prioridades",
    ], label_visibility="collapsed")

    st.markdown("---")
    up = st.file_uploader("Atualizar planilha", type=['xlsx'], key='okr',
                           help="Substitui o Drive temporariamente")

# ── Load ──────────────────────────────────────────────────────────────────────
raw_bytes = up.getvalue() if up else fetch()
if not raw_bytes:
    hdr("OKR 2026", "Carregando…")
    st.warning("Não foi possível conectar ao Google Drive. Faça upload manual.")
    st.stop()

with st.spinner(""):
    df = load(raw_bytes)

# ── Filters sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    donos_disp = sorted(df[df['dono'].notna() & ~df['dono'].eq('Dono')]['dono'].unique())
    dono_sel   = st.multiselect("Responsável", donos_disp, default=[])
    status_disp = ['A iniciar','Em andamento','Concluído','Atrasado']
    status_sel  = st.multiselect("Status", status_disp, default=[])

df_f = df.copy()
if dono_sel:  df_f = df_f[df_f['dono'].isin(dono_sel)]
if status_sel:
    for s in status_sel:
        if s == 'Atrasado':
            df_f = df_f[df_f.apply(lambda r: is_late(r['prazo'], r['status']), axis=1)]
        else:
            df_f = df_f[df_f['status'].str.contains(s.split()[0], na=False, case=False)]

acoes = df_f[df_f['nivel']=='acao']
tots  = len(acoes)
andamento  = acoes['status'].str.contains('andamento', case=False, na=False).sum()
concluidos = acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
a_iniciar  = tots - andamento - concluidos
atrasadas  = acoes[acoes.apply(lambda r: is_late(r['prazo'], r['status']), axis=1)]

pct = int(concluidos / tots * 100) if tots else 0

# ═══════════════════════════════════════════════════════════════════════════════
# VISÃO GERAL
# ═══════════════════════════════════════════════════════════════════════════════
if page == "🎯  Visão Geral":
    hdr("OKR 2026 — Visão Geral", "Planejamento estratégico DBCL")

    k1,k2,k3,k4,k5 = st.columns(5)
    kpi_card(k1, "Progresso Geral", f"{pct}%", f"{concluidos}/{tots} ações")
    kpi_card(k2, "Em Andamento", str(andamento), "ações ativas", "dim")
    kpi_card(k3, "A Iniciar", str(a_iniciar), "ainda não iniciadas", "warn")
    kpi_card(k4, "Atrasadas", str(len(atrasadas)), "prazo vencido", "alert")
    kpi_card(k5, "Objetivos", "2", "KRs: 5 · Iniciativas: 22", "dim")

    st.markdown("---")
    c1, c2 = st.columns([1,1])

    with c1:
        sec("Progresso por Objetivo")
        for obj_key in df['ctx_obj'].dropna().unique():
            obj_row = df[df['tipo']==obj_key]
            if obj_row.empty: continue
            obj_desc = obj_row.iloc[0]['descricao']
            obj_acoes = acoes[acoes['ctx_obj']==obj_key]
            tot_o = len(obj_acoes)
            conc_o = obj_acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
            pct_o = int(conc_o/tot_o*100) if tot_o else 0
            and_o = obj_acoes['status'].str.contains('andamento', case=False, na=False).sum()
            st.markdown(f"""<div class="obj-card">
                <div class="obj-label">{obj_key}</div>
                <div class="obj-title">{obj_desc}</div>
                <div class="obj-bar-bg"><div class="obj-bar-fg" style="width:{pct_o}%"></div></div>
                <div class="obj-stats">{pct_o}% concluído · {and_o} em andamento · {tot_o} ações totais</div>
            </div>""", unsafe_allow_html=True)

    with c2:
        sec("Progresso por KR")
        krs = df[df['nivel']=='kr']
        kr_data = []
        for _, kr in krs.iterrows():
            kr_acoes = acoes[acoes['ctx_kr']==kr['tipo']]
            tot_k = len(kr_acoes)
            conc_k = kr_acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
            and_k  = kr_acoes['status'].str.contains('andamento', case=False, na=False).sum()
            pct_k  = int(conc_k/tot_k*100) if tot_k else 0
            kr_data.append({'kr': kr['tipo'], 'desc': kr['descricao'][:50]+'…' if len(str(kr['descricao']))>50 else kr['descricao'],
                            'pct': pct_k, 'tot': tot_k, 'and': and_k, 'conc': conc_k,
                            'obj': kr['ctx_obj'], 'dono': kr['dono']})

        fig = go.Figure()
        for kr in kr_data:
            label = f"{kr['kr']}: {kr['desc'][:35]}…" if len(str(kr['desc']))>35 else f"{kr['kr']}: {kr['desc']}"
            fig.add_trace(go.Bar(
                x=[kr['pct']], y=[label], orientation='h',
                marker_color='#1A6B45' if kr['pct']>50 else '#00FF00' if kr['pct']>0 else 'rgba(0,255,0,.15)',
                marker_line_width=0,
                text=f" {kr['pct']}%", textposition='outside',
                textfont=dict(size=10, color='#23282E', family='Tomorrow, sans-serif'),
                showlegend=False,
                name=kr['kr']
            ))
        fig.update_layout(
            height=max(280, len(kr_data)*55),
            margin=dict(l=300, r=60, t=20, b=20),
            plot_bgcolor='#FAF7EC', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(range=[0,120], showgrid=False, zeroline=False,
                       tickfont=dict(size=9, color='#23282E', family='Tomorrow, sans-serif'),
                       title=dict(text='', font=dict(color='#23282E'))),
            yaxis=dict(showgrid=False, zeroline=False, automargin=False,
                       tickfont=dict(size=10, color='#23282E', family='Tomorrow, sans-serif'),
                       title=dict(text='', font=dict(color='#23282E'))),
            title=dict(text='', font=dict(color='#23282E')),
            bargap=0.35,
        )
        st.plotly_chart(fig, use_container_width=True)

        sec("Status das Ações")
        status_counts = {
            'Em andamento': andamento,
            'A iniciar': a_iniciar,
            'Concluído': concluidos,
            'Atrasado': len(atrasadas)
        }
        status_counts = {k:v for k,v in status_counts.items() if v > 0}
        fig2 = go.Figure(go.Pie(
            values=list(status_counts.values()),
            labels=list(status_counts.keys()),
            hole=0.55,
            marker_colors=['#1A6B45','#D4C9A8','#003C28','#C0392B'],
            textinfo='percent+label',
            textfont=dict(size=10, color='#23282E', family='Tomorrow, sans-serif'),
        ))
        fig2.update_layout(
            height=260, margin=dict(l=0,r=0,t=10,b=10),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            title=dict(text='', font=dict(color='#23282E')),
        )
        st.plotly_chart(fig2, use_container_width=True)

    if len(atrasadas) > 0:
        sec("⚠ Ações Atrasadas")
        for _, a in atrasadas.head(10).iterrows():
            p = priority_badge(a['prioridade'])
            st.markdown(f"""<div class="acao-row">
                <div class="acao-text">{a['descricao']} {p}</div>
                <div class="acao-meta">Dono: {a['dono']} · Prazo: {fmt_date(a['prazo'])} · {a['ctx_kr']}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# POR OBJETIVO
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📌  Por Objetivo":
    hdr("OKR 2026 — Por Objetivo", "Hierarquia completa")

    objs = df[df['nivel']=='objetivo']['tipo'].unique()
    obj_sel = st.selectbox("", objs,
                            format_func=lambda x: f"{x}: {df[df['tipo']==x]['descricao'].iloc[0][:60]}…",
                            label_visibility="collapsed")

    obj_desc = df[df['tipo']==obj_sel]['descricao'].iloc[0]
    obj_acoes = acoes[acoes['ctx_obj']==obj_sel]
    tot_o = len(obj_acoes)
    conc_o = obj_acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
    pct_o  = int(conc_o/tot_o*100) if tot_o else 0

    st.markdown(f"""<div class="obj-card">
        <div class="obj-label">{obj_sel}</div>
        <div class="obj-title">{obj_desc}</div>
        <div class="obj-bar-bg"><div class="obj-bar-fg" style="width:{pct_o}%"></div></div>
        <div class="obj-stats">{pct_o}% concluído · {tot_o} ações totais</div>
    </div>""", unsafe_allow_html=True)

    # KRs deste objetivo
    krs_obj = df[(df['nivel']=='kr') & (df['ctx_obj']==obj_sel)]
    for _, kr in krs_obj.iterrows():
        kr_acoes = acoes[acoes['ctx_kr']==kr['tipo']]
        tot_k = len(kr_acoes); conc_k = kr_acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
        and_k = kr_acoes['status'].str.contains('andamento', case=False, na=False).sum()
        pct_k = int(conc_k/tot_k*100) if tot_k else 0

        with st.expander(f"**{kr['tipo']}** — {kr['descricao']}", expanded=True):
            st.markdown(f"""<div class="kr-card">
                <div class="kr-label">{kr['tipo']}</div>
                <div class="kr-title">{kr['descricao']}</div>
                <div class="kr-meta">Dono: {kr['dono']} · Fiscal: {kr['socio']} · {pct_k}% concluído · {and_k} em andamento · {tot_k} ações</div>
            </div>""", unsafe_allow_html=True)

            # Iniciativas deste KR
            inis = df[(df['nivel']=='iniciativa') & (df['ctx_kr']==kr['tipo'])]
            for _, ini in inis.iterrows():
                p = priority_badge(ini['prioridade'])
                ini_acoes = df[(df['nivel']=='acao') & (df['ctx_kr']==kr['tipo']) &
                               df['tipo'].str.startswith(f"Ação {ini['tipo'].split()[-1]}")]
                st.markdown(f"""<div class="ini-card">
                    <div class="ini-title">{ini['tipo']}: {ini['descricao']} {p}</div>
                    <div class="ini-meta">Dono: {ini['dono']} · Prazo: {fmt_date(ini['prazo'])} · {status_badge(ini['status'])}</div>
                </div>""", unsafe_allow_html=True)

                # Ações desta iniciativa
                num_ini = ini['tipo'].split()[-1]
                acs = df[(df['nivel']=='acao') & (df['ctx_kr']==kr['tipo']) &
                         df['tipo'].str.match(f"Ação {num_ini}\\.")]
                for _, ac in acs.iterrows():
                    late = is_late(ac['prazo'], ac['status'])
                    late_badge = '<span class="badge badge-atrasado">Atrasado</span> ' if late else ''
                    p2 = priority_badge(ac['prioridade'])
                    st.markdown(f"""<div class="acao-row">
                        <div class="acao-text">{late_badge}{ac['tipo']}: {ac['descricao']} {p2}</div>
                        <div class="acao-meta">Dono: {ac['dono']} · Prazo: {fmt_date(ac['prazo'])} · {status_badge(ac['status'])}</div>
                    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# POR RESPONSÁVEL
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "👤  Por Responsável":
    hdr("OKR 2026 — Por Responsável", "Carga e progresso por pessoa")

    donos = sorted(df[df['dono'].notna() & ~df['dono'].eq('Dono')]['dono'].unique())
    c_cols = st.columns(len(donos))
    for i, dono in enumerate(donos):
        d_acoes = acoes[acoes['dono']==dono]
        tot_d = len(d_acoes)
        conc_d = d_acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
        and_d  = d_acoes['status'].str.contains('andamento', case=False, na=False).sum()
        pct_d  = int(conc_d/tot_d*100) if tot_d else 0
        late_d = d_acoes[d_acoes.apply(lambda r: is_late(r['prazo'], r['status']), axis=1)]
        variant = 'alert' if len(late_d) > 3 else ('dim' if pct_d > 30 else '')
        kpi_card(c_cols[i], dono.upper(), f"{pct_d}%",
                 f"{tot_d} ações · {len(late_d)} atrasadas", variant)

    sec("Ações por responsável")
    dono_sel2 = st.selectbox("Selecionar responsável", donos, label_visibility="collapsed")
    tabs = st.tabs(["Em Andamento", "A Iniciar", "Atrasadas", "Todas"])

    def render_acoes(df_sub):
        for _, a in df_sub.iterrows():
            late = is_late(a['prazo'], a['status'])
            late_b = '<span class="badge badge-atrasado">Atrasado</span> ' if late else ''
            p = priority_badge(a['prioridade'])
            st.markdown(f"""<div class="acao-row">
                <div class="acao-text">{late_b}{a['tipo']}: {a['descricao']} {p}</div>
                <div class="acao-meta">{a['ctx_obj']} · {a['ctx_kr']} · Prazo: {fmt_date(a['prazo'])} · {status_badge(a['status'])}</div>
            </div>""", unsafe_allow_html=True)

    d_acoes2 = acoes[acoes['dono']==dono_sel2]
    with tabs[0]: render_acoes(d_acoes2[d_acoes2['status'].str.contains('andamento', case=False, na=False)])
    with tabs[1]: render_acoes(d_acoes2[d_acoes2['status'].str.contains('iniciar', case=False, na=False)])
    with tabs[2]: render_acoes(d_acoes2[d_acoes2.apply(lambda r: is_late(r['prazo'], r['status']), axis=1)])
    with tabs[3]: render_acoes(d_acoes2.sort_values('prazo'))

# ═══════════════════════════════════════════════════════════════════════════════
# PRIORIDADES
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "🔥  Prioridades":
    hdr("OKR 2026 — Prioridades", "Ações prioritárias e próximos vencimentos")

    p1 = acoes[acoes['prioridade']==1.0].sort_values('prazo')
    p2 = acoes[acoes['prioridade']==2.0].sort_values('prazo')

    k1,k2,k3 = st.columns(3)
    kpi_card(k1, "Prioridade 1", str(len(p1)), "ações críticas")
    kpi_card(k2, "Prioridade 2", str(len(p2)), "ações importantes", "dim")
    kpi_card(k3, "Vencendo em 30d", str(len(acoes[acoes['prazo'].apply(
        lambda d: False if pd.isna(d) else
        (pd.to_datetime(d, errors='coerce').date() - date.today()).days <= 30
        if not isinstance(d, str) else False)])), "requer atenção", "warn")

    c1, c2 = st.columns(2)
    with c1:
        sec("P1 — Críticas")
        for _, a in p1.iterrows():
            late = is_late(a['prazo'], a['status'])
            late_b = '<span class="badge badge-atrasado">Atrasado</span> ' if late else ''
            st.markdown(f"""<div class="acao-row" style="border-left:2px solid #00FF00">
                <div class="acao-text">{late_b}{a['descricao']}</div>
                <div class="acao-meta">Dono: {a['dono']} · Prazo: {fmt_date(a['prazo'])} · {status_badge(a['status'])}</div>
            </div>""", unsafe_allow_html=True)

    with c2:
        sec("P2 — Importantes")
        for _, a in p2.iterrows():
            late = is_late(a['prazo'], a['status'])
            late_b = '<span class="badge badge-atrasado">Atrasado</span> ' if late else ''
            st.markdown(f"""<div class="acao-row">
                <div class="acao-text">{late_b}{a['descricao']}</div>
                <div class="acao-meta">Dono: {a['dono']} · Prazo: {fmt_date(a['prazo'])} · {status_badge(a['status'])}</div>
            </div>""", unsafe_allow_html=True)

    sec("Próximos vencimentos (todos)")
    upcoming = acoes[acoes['prazo'].notna()].copy()
    upcoming['prazo_dt'] = pd.to_datetime(upcoming['prazo'], errors='coerce')
    upcoming = upcoming[upcoming['prazo_dt'].notna()].sort_values('prazo_dt')
    upcoming['dias'] = (upcoming['prazo_dt'].dt.date - date.today()).apply(lambda x: x.days)
    for _, a in upcoming.head(20).iterrows():
        dias = a['dias']
        cor  = '#C0392B' if dias < 0 else ('#F0E8C8' if dias <= 30 else '#23282E')
        dias_txt = f"<b style='color:{cor}'>{abs(dias)}d {'atrás' if dias<0 else 'restantes'}</b>"
        p = priority_badge(a['prioridade'])
        st.markdown(f"""<div class="acao-row">
            <div class="acao-text">{a['descricao']} {p}</div>
            <div class="acao-meta">Dono: {a['dono']} · {fmt_date(a['prazo'])} · {dias_txt} · {status_badge(a['status'])}</div>
        </div>""", unsafe_allow_html=True)
