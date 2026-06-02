import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import io, requests
from datetime import date

st.set_page_config(page_title="DBCL — OKR 2026", page_icon="🎯", layout="wide",
                   initial_sidebar_state="expanded")

OKR_ID = "1WI7ogJK_s0gcDbMVFBtb0BuxzCWyyzmO"

# Status palette
S = {
    'Concluído':    {'bg':'#1A6B45', 'text':'#FFFFFF', 'border':'#1A6B45'},
    'Em andamento': {'bg':'#C9A227', 'text':'#23282E', 'border':'#C9A227'},
    'A iniciar':    {'bg':'rgba(212,201,168,.25)', 'text':'#5A4A28', 'border':'rgba(212,201,168,.6)'},
    'Atrasado':     {'bg':'#C0392B', 'text':'#FFFFFF', 'border':'#C0392B'},
}

def s_color(status, late=False):
    if late: return S['Atrasado']
    for k, v in S.items():
        if k.lower() in str(status).lower(): return v
    return S['A iniciar']

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600;700&family=Tomorrow:wght@400;600;700;900&display=swap');

@keyframes fadeUp { from { opacity:0; transform:translateY(6px) } to { opacity:1; transform:translateY(0) } }
@keyframes pulse  { 0%,100% { opacity:1 } 50% { opacity:.2 } }

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

/* Sidebar */
[data-testid="stSidebar"] { background: #003C28 !important; border-right: 1px solid rgba(0,255,0,.1) !important; }
[data-testid="stSidebar"] * { color: #FAF7EC !important; font-family: 'Tomorrow', sans-serif !important; }
[data-testid="stSidebar"] hr { border-color: rgba(0,255,0,.12) !important; margin: 10px 0 !important; }
[data-testid="stSidebar"] label { color: rgba(250,247,236,.45) !important; font-size: 9px !important; text-transform: uppercase !important; letter-spacing: 2px !important; font-weight: 700 !important; }
[data-testid="stSidebar"] [data-baseweb="radio"] label span { font-size: 11px !important; letter-spacing:.3px !important; text-transform:none !important; white-space:nowrap !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] { background: rgba(0,255,0,.1) !important; border: 1px solid rgba(0,255,0,.25) !important; border-radius: 2px !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] span { color: #FAF7EC !important; }
[data-testid="stSidebar"] [data-baseweb="tag"] [role="button"] { color: rgba(0,255,0,.6) !important; }

/* Header */
.hdr { background:#003C28; border-radius:2px; border:1px solid rgba(0,255,0,.15); padding:18px 26px; margin-bottom:20px; display:flex; align-items:center; gap:18px; animation:fadeUp .3s ease; }
.hdr-logo { display:flex; flex-direction:column; gap:1px; padding-right:18px; border-right:1px solid rgba(250,247,236,.15); flex-shrink:0; }
.hdr-logo .dbcl { font-family:'Tomorrow',sans-serif; font-size:18px; font-weight:700; color:#FAF7EC; line-height:1; letter-spacing:1px; }
.hdr-logo .adv  { font-family:'Tomorrow',sans-serif; font-size:7px; color:rgba(250,247,236,.4); letter-spacing:4px; text-transform:uppercase; margin-top:2px; }
.hdr-ctx { display:flex; flex-direction:column; gap:3px; padding-left:4px; }
.hdr-ctx .pg  { font-family:'Tomorrow',sans-serif; font-size:13px; font-weight:600; color:#FAF7EC; }
.hdr-ctx .sub { font-family:'Tomorrow',sans-serif; font-size:9px; color:rgba(250,247,236,.45); letter-spacing:1.5px; text-transform:uppercase; }
.hdr-right { margin-left:auto; display:flex; align-items:center; gap:6px; font-family:'Tomorrow',sans-serif; font-size:8px; color:rgba(0,255,0,.65); letter-spacing:2px; text-transform:uppercase; flex-shrink:0; }
.hdr-dot { width:5px; height:5px; border-radius:50%; background:#00FF00; animation:pulse 2s infinite; }

/* KPI cards */
.kpi { background:#003C28; border-radius:2px; padding:14px 16px 12px; border-left:3px solid #00FF00; animation:fadeUp .25s ease; }
.kpi.dim   { border-left-color:rgba(0,255,0,.3); }
.kpi.warn  { border-left-color:#C9A227; }
.kpi.alert { border-left-color:#C0392B; }
.kpi .lbl { font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:700; color:rgba(250,247,236,.45); text-transform:uppercase; letter-spacing:2px; margin-bottom:6px; }
.kpi .val { font-family:'Tomorrow',sans-serif; font-size:22px; font-weight:700; color:#FAF7EC; line-height:1; }
.kpi .sub { font-family:'Tomorrow',sans-serif; font-size:9px; color:rgba(250,247,236,.4); margin-top:5px; }

/* Section */
.sec { font-family:'Tomorrow',sans-serif; font-size:9px; font-weight:700; color:rgba(0,60,40,.65); text-transform:uppercase; letter-spacing:2.5px; border-left:1.5px solid #00FF00; padding:5px 12px; background:rgba(0,255,0,.04); border-radius:0 2px 2px 0; margin:18px 0 10px; }

/* Objective card */
.obj-card { background:#003C28; border-radius:2px; border:1px solid rgba(0,255,0,.2); padding:18px 22px 16px; margin-bottom:10px; animation:fadeUp .25s ease; }
.obj-num  { font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:700; color:rgba(0,255,0,.55); text-transform:uppercase; letter-spacing:2.5px; margin-bottom:5px; }
.obj-title { font-family:'Lora',serif; font-size:15px; font-weight:700; color:#FAF7EC; line-height:1.4; margin-bottom:12px; }
.obj-bar-bg { background:rgba(0,255,0,.1); height:3px; border-radius:1px; }
.obj-bar-fg { background:#00FF00; height:3px; border-radius:1px; }
.obj-stats  { font-family:'Tomorrow',sans-serif; font-size:8px; color:rgba(250,247,236,.45); margin-top:6px; letter-spacing:.5px; }

/* KR block */
.kr-block { background:rgba(250,247,236,.6); border-radius:2px; border:1px solid rgba(0,60,40,.12); border-left:3px solid rgba(0,255,0,.4); padding:12px 16px; margin:8px 0 4px; }
.kr-num   { font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:700; color:#1A6B45; letter-spacing:2px; text-transform:uppercase; margin-bottom:3px; }
.kr-title { font-family:'Lora',serif; font-size:13px; font-weight:600; color:#003C28; line-height:1.4; }
.kr-meta  { font-family:'Tomorrow',sans-serif; font-size:9px; color:#8FB89A; margin-top:6px; display:flex; gap:12px; flex-wrap:wrap; }
.kr-meta span { display:flex; align-items:center; gap:4px; }

/* Iniciativa */
.ini-row { background:#FFFFFF; border-radius:2px; border-left:3px solid #D4C9A8; padding:10px 14px; margin:5px 0 3px 12px; display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.ini-left { flex:1; }
.ini-title { font-family:'Lora',serif; font-size:12px; font-weight:600; color:#003C28; line-height:1.4; }
.ini-meta  { font-family:'Tomorrow',sans-serif; font-size:9px; color:#8FB89A; margin-top:4px; }
.ini-right { flex-shrink:0; display:flex; flex-direction:column; align-items:flex-end; gap:4px; }

/* Ação */
.acao-row { padding:8px 14px 8px 24px; border-bottom:1px solid rgba(0,60,40,.05); background:rgba(250,247,236,.4); display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
.acao-left { flex:1; }
.acao-text { font-family:'Lora',serif; font-size:11px; color:#23282E; line-height:1.5; }
.acao-meta { font-family:'Tomorrow',sans-serif; font-size:8px; color:#8FB89A; margin-top:3px; display:flex; gap:10px; flex-wrap:wrap; }
.acao-right { flex-shrink:0; display:flex; flex-direction:column; align-items:flex-end; gap:3px; }

/* Status pill */
.spill { font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:700; text-transform:uppercase; letter-spacing:1.5px; padding:3px 8px; border-radius:2px; white-space:nowrap; }

/* Dono pill */
.dpill { font-family:'Tomorrow',sans-serif; font-size:8px; font-weight:700; text-transform:uppercase; letter-spacing:1px; padding:2px 7px; border-radius:2px; background:rgba(0,60,40,.08); color:#003C28; border:1px solid rgba(0,60,40,.15); white-space:nowrap; }

/* Priority */
.p1 { font-family:'Tomorrow',sans-serif; font-size:7px; font-weight:900; color:#00FF00; border:1px solid rgba(0,255,0,.4); padding:2px 5px; border-radius:2px; letter-spacing:1px; }
.p2 { font-family:'Tomorrow',sans-serif; font-size:7px; font-weight:700; color:#D4C9A8; border:1px solid rgba(212,201,168,.35); padding:2px 5px; border-radius:2px; letter-spacing:1px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background:rgba(0,60,40,.06); border-radius:2px; padding:3px; gap:2px; border:1px solid rgba(0,255,0,.1); }
.stTabs [data-baseweb="tab"] { border-radius:2px; padding:6px 16px; font-family:'Tomorrow',sans-serif !important; font-size:9px !important; font-weight:700 !important; text-transform:uppercase !important; letter-spacing:1.5px !important; color:rgba(0,60,40,.5) !important; }
.stTabs [aria-selected="true"] { background:#003C28 !important; color:#FAF7EC !important; border:1px solid rgba(0,255,0,.2) !important; }

hr { border:none; border-top:1px solid rgba(0,255,0,.08); margin:16px 0; }
[data-testid="stDataFrame"] { border-radius:2px; border:1px solid rgba(0,60,40,.1); }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def hdr(page, sub):
    st.markdown(f"""<div class="hdr">
        <div class="hdr-logo"><div class="dbcl">dbcl</div><div class="adv">Advogados</div></div>
        <div class="hdr-ctx"><div class="pg">{page}</div><div class="sub">{sub}</div></div>
        <div class="hdr-right"><div class="hdr-dot"></div>OKR 2026</div>
    </div>""", unsafe_allow_html=True)

def kpi_card(col, label, value, sub='', variant=''):
    with col:
        st.markdown(f"""<div class="kpi {variant}">
            <div class="lbl">{label}</div><div class="val">{value}</div>
            {'<div class="sub">'+sub+'</div>' if sub else ''}
        </div>""", unsafe_allow_html=True)

def sec(title):
    st.markdown(f'<div class="sec">{title}</div>', unsafe_allow_html=True)

def spill(status, late=False):
    sc = s_color(status, late)
    return f'<span class="spill" style="background:{sc["bg"]};color:{sc["text"]};border:1px solid {sc["border"]}">{("ATRASADO" if late else status.upper())}</span>'

def dpill(dono):
    if not isinstance(dono, str) or dono in ('Dono','nan',''): return ''
    return f'<span class="dpill">{dono}</span>'

def ppill(p):
    try:
        v = int(float(p))
        if v == 1: return '<span class="p1">P1</span>'
        if v == 2: return '<span class="p2">P2</span>'
    except: pass
    return ''

def fmt_date(d):
    if pd.isna(d): return '—'
    try: return pd.to_datetime(d, errors='coerce').strftime('%d/%m/%y')
    except: return str(d)[:10]

def safe_prazo(d):
    """Convert prazo to datetime safely, return NaT on failure."""
    if pd.isna(d): return pd.NaT
    try: return pd.to_datetime(d, errors='coerce', dayfirst=True)
    except: return pd.NaT

def is_late(row):
    dt = safe_prazo(row['prazo'])
    if pd.isna(dt): return False
    status = str(row['status']).lower()
    return dt.date() < date.today() and 'concluí' not in status and 'concluido' not in status

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch():
    try:
        r = requests.get(f"https://docs.google.com/spreadsheets/d/{OKR_ID}/export?format=xlsx", timeout=30)
        return r.content if r.status_code == 200 else None
    except: return None

@st.cache_data(show_spinner=False)
def load(b):
    raw = pd.read_excel(io.BytesIO(b), sheet_name=0, header=0)
    raw.columns = [str(c).strip() for c in raw.columns]
    cols = list(raw.columns)
    raw = raw.rename(columns={cols[0]:'tipo', cols[1]:'descricao', cols[7]:'dono',
                               cols[8]:'socio', cols[9]:'prazo', cols[10]:'status_mai',
                               cols[11]:'status_jun', cols[12]:'prioridade'})
    for c in [cols[2],cols[3],cols[4],cols[5],cols[6]]:
        if c in raw.columns:
            mask = raw['descricao'].isna() & raw[c].notna()
            raw.loc[mask,'descricao'] = raw.loc[mask,c]
    raw = raw[raw['tipo'].notna()].copy()
    raw = raw[~raw['tipo'].str.strip().eq('OKR - PLANEJAMENTO ESTRATÉGICO')]
    def level(t):
        t = str(t).strip()
        if t.startswith('Objetivo'): return 'objetivo'
        if t.startswith('KR'):       return 'kr'
        if t.startswith('Inicia'):   return 'iniciativa'
        if t.startswith('Ação'):     return 'acao'
        return 'outro'
    raw['nivel'] = raw['tipo'].apply(level)
    curr_obj = curr_kr = curr_obj_desc = curr_kr_desc = None
    co,ck,cod,ckd = [],[],[],[]
    for _,row in raw.iterrows():
        if row['nivel']=='objetivo': curr_obj=row['tipo']; curr_obj_desc=str(row['descricao']).strip(); curr_kr=None; curr_kr_desc=None
        elif row['nivel']=='kr':     curr_kr=row['tipo'];  curr_kr_desc=str(row['descricao']).strip()
        co.append(curr_obj); ck.append(curr_kr); cod.append(curr_obj_desc); ckd.append(curr_kr_desc)
    raw['ctx_obj']=co; raw['ctx_kr']=ck; raw['ctx_obj_desc']=cod; raw['ctx_kr_desc']=ckd
    raw['status'] = raw['status_jun'].where(
        raw['status_jun'].notna() & raw['status_jun'].apply(lambda x: isinstance(x,str)),
        raw['status_mai'])
    raw['status'] = raw['status'].apply(lambda x: x if isinstance(x,str) else 'A iniciar')
    # safe prazo_dt for sorting
    raw['prazo_dt'] = raw['prazo'].apply(safe_prazo)
    return raw

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="padding:18px 4px 12px">
        <div style="font-family:'Tomorrow',sans-serif;font-size:18px;font-weight:700;color:#FAF7EC;letter-spacing:1px">dbcl</div>
        <div style="font-family:'Tomorrow',sans-serif;font-size:7px;color:rgba(250,247,236,.4);letter-spacing:4px;text-transform:uppercase;margin-top:2px">Advogados</div>
        <div style="margin-top:10px;display:flex;align-items:center;gap:5px">
          <div style="width:5px;height:5px;border-radius:50%;background:#00FF00;animation:pulse 2s infinite"></div>
          <span style="font-family:'Tomorrow',sans-serif;font-size:7px;color:rgba(0,255,0,.6);letter-spacing:2px;text-transform:uppercase">OKR 2026</span>
        </div></div>""", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["🎯  Visão Geral","📌  Por Objetivo","👤  Por Responsável","🔥  Prioridades"],
                    label_visibility="collapsed")
    st.markdown("---")
    donos_f = []
    status_f = []

# ── Load ──────────────────────────────────────────────────────────────────────
raw_bytes = fetch()
if not raw_bytes:
    hdr("OKR 2026","Carregando…")
    st.warning("Não foi possível conectar ao Google Drive.")
    st.stop()

with st.spinner(""):
    df = load(raw_bytes)

acoes = df[df['nivel']=='acao'].copy()
acoes['late'] = acoes.apply(is_late, axis=1)
tots = len(acoes)
concluidos = acoes['status'].str.contains('concluí|concluido', case=False, na=False).sum()
andamento  = acoes['status'].str.contains('andamento', case=False, na=False).sum()
a_iniciar  = tots - concluidos - andamento
atrasadas  = acoes[acoes['late']]
pct = int(concluidos/tots*100) if tots else 0

# ══════════════════════════════════════════════════════════════════════
# VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════
if page == "🎯  Visão Geral":
    hdr("OKR 2026 — Visão Geral", "Planejamento estratégico DBCL")
    k1,k2,k3,k4,k5 = st.columns(5)
    kpi_card(k1,"Progresso Geral",f"{pct}%",f"{concluidos}/{tots} ações concluídas")
    kpi_card(k2,"Em Andamento",str(andamento),"ações ativas","warn")
    kpi_card(k3,"A Iniciar",str(a_iniciar),"ainda não iniciadas","dim")
    kpi_card(k4,"Atrasadas",str(len(atrasadas)),"prazo vencido","alert")
    kpi_card(k5,"Estrutura","2 Obj · 5 KRs","22 iniciativas · 65 ações","dim")
    st.markdown("---")
    c1, c2 = st.columns([1,1])

    with c1:
        sec("Progresso por Objetivo")
        for obj_key in df[df['nivel']=='objetivo']['tipo'].tolist():
            obj_desc = df[df['tipo']==obj_key]['descricao'].iloc[0]
            oa = acoes[acoes['ctx_obj']==obj_key]
            tot_o=len(oa); conc_o=oa['status'].str.contains('concluí|concluido',case=False,na=False).sum()
            and_o=oa['status'].str.contains('andamento',case=False,na=False).sum()
            pct_o=int(conc_o/tot_o*100) if tot_o else 0
            st.markdown(f"""<div class="obj-card">
                <div class="obj-num">{obj_key}</div>
                <div class="obj-title">{obj_desc}</div>
                <div class="obj-bar-bg"><div class="obj-bar-fg" style="width:{pct_o}%"></div></div>
                <div class="obj-stats">{pct_o}% concluído &nbsp;·&nbsp; {and_o} em andamento &nbsp;·&nbsp; {tot_o} ações totais</div>
            </div>""", unsafe_allow_html=True)

        sec("Status das Ações")
        sc = {'Concluído':concluidos,'Em andamento':andamento,'A iniciar':a_iniciar,'Atrasado':len(atrasadas)}
        sc = {k:v for k,v in sc.items() if v>0}
        colors = {'Concluído':'#1A6B45','Em andamento':'#C9A227','A iniciar':'#D4C9A8','Atrasado':'#C0392B'}
        fig2 = go.Figure(go.Pie(
            values=list(sc.values()), labels=list(sc.keys()), hole=0.55,
            marker_colors=[colors[k] for k in sc],
            textinfo='percent+label',
            textfont=dict(size=10, color='#23282E', family='Tomorrow, sans-serif'),
        ))
        fig2.update_layout(height=240, margin=dict(l=0,r=0,t=10,b=10),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False, title=dict(text='',font=dict(color='#23282E')))
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        sec("Progresso por KR")
        krs = df[df['nivel']=='kr']
        fig = go.Figure()
        for _,kr in krs.iterrows():
            ka=acoes[acoes['ctx_kr']==kr['tipo']]
            tot_k=len(ka); conc_k=ka['status'].str.contains('concluí|concluido',case=False,na=False).sum()
            pct_k=int(conc_k/tot_k*100) if tot_k else 0
            label=f"{kr['tipo']}: {str(kr['descricao'])[:40]}…" if len(str(kr['descricao']))>40 else f"{kr['tipo']}: {kr['descricao']}"
            fig.add_trace(go.Bar(x=[pct_k],y=[label],orientation='h',
                marker_color='#1A6B45' if pct_k>50 else ('#C9A227' if pct_k>0 else 'rgba(0,60,40,.12)'),
                marker_line_width=0,
                text=f" {pct_k}%", textposition='outside',
                textfont=dict(size=10,color='#23282E',family='Tomorrow, sans-serif'),
                showlegend=False,name=kr['tipo']))
        fig.update_layout(height=max(260,len(krs)*56), margin=dict(l=300,r=60,t=10,b=10),
            plot_bgcolor='#FAF7EC', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(range=[0,130],showgrid=False,zeroline=False,
                tickfont=dict(size=9,color='#23282E',family='Tomorrow, sans-serif'),
                title=dict(text='',font=dict(color='#23282E'))),
            yaxis=dict(showgrid=False,zeroline=False,automargin=False,
                tickfont=dict(size=10,color='#23282E',family='Tomorrow, sans-serif'),
                title=dict(text='',font=dict(color='#23282E'))),
            title=dict(text='',font=dict(color='#23282E')), bargap=0.4)
        st.plotly_chart(fig, use_container_width=True)

        if len(atrasadas) > 0:
            sec("⚠ Atrasadas")
            for _,a in atrasadas.head(8).iterrows():
                st.markdown(f"""<div class="acao-row">
                    <div class="acao-left">
                        <div class="acao-text">{a['descricao']}</div>
                        <div class="acao-meta"><span>{a['ctx_kr']}</span><span>Prazo: {fmt_date(a['prazo'])}</span></div>
                    </div>
                    <div class="acao-right">{dpill(a['dono'])}{spill(a['status'],True)}</div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# POR OBJETIVO
# ══════════════════════════════════════════════════════════════════════
elif page == "📌  Por Objetivo":
    hdr("OKR 2026 — Por Objetivo","Hierarquia completa")
    objs = df[df['nivel']=='objetivo']['tipo'].tolist()
    obj_sel = st.selectbox("", objs,
        format_func=lambda x: f"{x}: {df[df['tipo']==x]['descricao'].iloc[0][:55]}…",
        label_visibility="collapsed")

    obj_desc = df[df['tipo']==obj_sel]['descricao'].iloc[0]
    oa=acoes[acoes['ctx_obj']==obj_sel]; tot_o=len(oa)
    conc_o=oa['status'].str.contains('concluí|concluido',case=False,na=False).sum()
    pct_o=int(conc_o/tot_o*100) if tot_o else 0
    and_o=oa['status'].str.contains('andamento',case=False,na=False).sum()
    st.markdown(f"""<div class="obj-card">
        <div class="obj-num">{obj_sel}</div>
        <div class="obj-title">{obj_desc}</div>
        <div class="obj-bar-bg"><div class="obj-bar-fg" style="width:{pct_o}%"></div></div>
        <div class="obj-stats">{pct_o}% concluído &nbsp;·&nbsp; {and_o} em andamento &nbsp;·&nbsp; {tot_o} ações totais</div>
    </div>""", unsafe_allow_html=True)

    for _,kr in df[(df['nivel']=='kr')&(df['ctx_obj']==obj_sel)].iterrows():
        ka=acoes[acoes['ctx_kr']==kr['tipo']]
        tot_k=len(ka); conc_k=ka['status'].str.contains('concluí|concluido',case=False,na=False).sum()
        and_k=ka['status'].str.contains('andamento',case=False,na=False).sum()
        pct_k=int(conc_k/tot_k*100) if tot_k else 0
        with st.expander(f"{kr['tipo']} — {kr['descricao']}", expanded=True):
            st.markdown(f"""<div class="kr-block">
                <div class="kr-num">{kr['tipo']}</div>
                <div class="kr-title">{kr['descricao']}</div>
                <div class="kr-meta">
                    <span>👤 {kr['dono']}</span>
                    <span>🔍 Fiscal: {kr['socio']}</span>
                    <span>📊 {pct_k}% concluído</span>
                    <span>▶ {and_k} em andamento</span>
                    <span>📋 {tot_k} ações</span>
                </div>
            </div>""", unsafe_allow_html=True)

            for _,ini in df[(df['nivel']=='iniciativa')&(df['ctx_kr']==kr['tipo'])].iterrows():
                p = ppill(ini['prioridade'])
                late_ini = is_late(ini)
                st.markdown(f"""<div class="ini-row">
                    <div class="ini-left">
                        <div class="ini-title">{ini['tipo']}: {ini['descricao']}</div>
                        <div class="ini-meta">Prazo: {fmt_date(ini['prazo'])}</div>
                    </div>
                    <div class="ini-right">{dpill(ini['dono'])}{p}{spill(ini['status'],late_ini)}</div>
                </div>""", unsafe_allow_html=True)

                num = ini['tipo'].split()[-1]
                acs = df[(df['nivel']=='acao')&(df['ctx_kr']==kr['tipo'])&df['tipo'].str.match(f"Ação {num}\\.")]
                for _,ac in acs.iterrows():
                    late_ac = is_late(ac)
                    p2 = ppill(ac['prioridade'])
                    st.markdown(f"""<div class="acao-row">
                        <div class="acao-left">
                            <div class="acao-text">{ac['tipo']}: {ac['descricao']}</div>
                            <div class="acao-meta"><span>Prazo: {fmt_date(ac['prazo'])}</span></div>
                        </div>
                        <div class="acao-right">{dpill(ac['dono'])}{p2}{spill(ac['status'],late_ac)}</div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# POR RESPONSÁVEL
# ══════════════════════════════════════════════════════════════════════
elif page == "👤  Por Responsável":
    hdr("OKR 2026 — Por Responsável","Carga e status por pessoa")
    donos = sorted(df[df['dono'].notna()&~df['dono'].isin(['Dono','nan'])]['dono'].unique())
    cols = st.columns(len(donos))
    for i,dono in enumerate(donos):
        da=acoes[acoes['dono']==dono]
        tot_d=len(da); conc_d=da['status'].str.contains('concluí|concluido',case=False,na=False).sum()
        and_d=da['status'].str.contains('andamento',case=False,na=False).sum()
        pct_d=int(conc_d/tot_d*100) if tot_d else 0
        late_d=da[da.apply(is_late,axis=1)]
        v='alert' if len(late_d)>2 else ('warn' if and_d>0 else 'dim')
        kpi_card(cols[i],dono.upper(),f"{pct_d}%",f"{tot_d} ações · {len(late_d)} atrasadas",v)

    sec("Detalhe por responsável")
    dono_sel = st.selectbox("", donos, label_visibility="collapsed")
    d_acoes = acoes[acoes['dono']==dono_sel].copy()

    def render_list(df_sub):
        if df_sub.empty:
            st.markdown("<div style='font-family:Tomorrow,sans-serif;font-size:10px;color:#8FB89A;padding:12px'>Nenhuma ação neste filtro.</div>", unsafe_allow_html=True)
            return
        for _,a in df_sub.iterrows():
            late=is_late(a); p=ppill(a['prioridade'])
            st.markdown(f"""<div class="acao-row">
                <div class="acao-left">
                    <div class="acao-text">{a['tipo']}: {a['descricao']}</div>
                    <div class="acao-meta"><span>{a['ctx_obj']}</span><span>{a['ctx_kr']}</span><span>Prazo: {fmt_date(a['prazo'])}</span></div>
                </div>
                <div class="acao-right">{p}{spill(a['status'],late)}</div>
            </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["▶ Em Andamento","○ A Iniciar","⚠ Atrasadas","≡ Todas"])
    with tabs[0]: render_list(d_acoes[d_acoes['status'].str.contains('andamento',case=False,na=False)])
    with tabs[1]: render_list(d_acoes[d_acoes['status'].str.contains('iniciar',case=False,na=False)])
    with tabs[2]: render_list(d_acoes[d_acoes.apply(is_late,axis=1)])
    with tabs[3]: render_list(d_acoes.sort_values('prazo_dt', na_position='last'))

# ══════════════════════════════════════════════════════════════════════
# PRIORIDADES
# ══════════════════════════════════════════════════════════════════════
elif page == "🔥  Prioridades":
    hdr("OKR 2026 — Prioridades","Ações críticas e próximos vencimentos")

    p1 = acoes[acoes['prioridade']==1.0].copy()
    p2 = acoes[acoes['prioridade']==2.0].copy()
    p1_late = p1[p1.apply(is_late,axis=1)]

    upcoming = acoes[acoes['prazo_dt'].notna()].copy()
    upcoming = upcoming.sort_values('prazo_dt', na_position='last')
    upcoming['dias'] = (upcoming['prazo_dt'].dt.date - date.today()).apply(lambda x: x.days if pd.notna(x) else None)
    venc30 = upcoming[upcoming['dias'].notna() & (upcoming['dias']<=30) & (upcoming['dias']>=0)]

    k1,k2,k3,k4 = st.columns(4)
    kpi_card(k1,"Prioridade 1",str(len(p1)),"ações críticas")
    kpi_card(k2,"P1 Atrasadas",str(len(p1_late)),"urgente","alert" if len(p1_late)>0 else "dim")
    kpi_card(k3,"Prioridade 2",str(len(p2)),"ações importantes","dim")
    kpi_card(k4,"Vencendo em 30d",str(len(venc30)),"requer atenção","warn")

    c1, c2 = st.columns(2)
    with c1:
        sec("P1 — Críticas")
        if p1.empty:
            st.markdown("<div style='font-family:Tomorrow,sans-serif;font-size:10px;color:#8FB89A;padding:12px'>Nenhuma ação P1.</div>", unsafe_allow_html=True)
        for _,a in p1.sort_values('prazo_dt', na_position='last').iterrows():
            late=is_late(a)
            st.markdown(f"""<div class="acao-row" style="border-left:3px solid {'#C0392B' if late else '#00FF00'}">
                <div class="acao-left">
                    <div class="acao-text">{a['descricao']}</div>
                    <div class="acao-meta"><span>{a['ctx_kr']}</span><span>Prazo: {fmt_date(a['prazo'])}</span></div>
                </div>
                <div class="acao-right">{dpill(a['dono'])}{spill(a['status'],late)}</div>
            </div>""", unsafe_allow_html=True)

    with c2:
        sec("P2 — Importantes")
        if p2.empty:
            st.markdown("<div style='font-family:Tomorrow,sans-serif;font-size:10px;color:#8FB89A;padding:12px'>Nenhuma ação P2.</div>", unsafe_allow_html=True)
        for _,a in p2.sort_values('prazo_dt', na_position='last').iterrows():
            late=is_late(a)
            st.markdown(f"""<div class="acao-row">
                <div class="acao-left">
                    <div class="acao-text">{a['descricao']}</div>
                    <div class="acao-meta"><span>{a['ctx_kr']}</span><span>Prazo: {fmt_date(a['prazo'])}</span></div>
                </div>
                <div class="acao-right">{dpill(a['dono'])}{spill(a['status'],late)}</div>
            </div>""", unsafe_allow_html=True)

    sec("Próximos vencimentos")
    for _,a in upcoming.head(25).iterrows():
        dias=a['dias']
        if dias is None: continue
        late=is_late(a)
        if dias < 0:   cor='#C0392B'; txt=f"{abs(int(dias))}d atraso"
        elif dias <=7: cor='#C9A227'; txt=f"{int(dias)}d restantes"
        elif dias <=30:cor='#1A6B45'; txt=f"{int(dias)}d restantes"
        else:          cor='#8FB89A'; txt=f"{int(dias)}d restantes"
        p=ppill(a['prioridade'])
        dias_badge=f'<span style="font-family:Tomorrow,sans-serif;font-size:8px;font-weight:700;color:{cor}">{txt}</span>'
        st.markdown(f"""<div class="acao-row">
            <div class="acao-left">
                <div class="acao-text">{a['descricao']}</div>
                <div class="acao-meta"><span>{a['ctx_kr']}</span><span>{fmt_date(a['prazo'])}</span>{dias_badge}</div>
            </div>
            <div class="acao-right">{dpill(a['dono'])}{p}{spill(a['status'],late)}</div>
        </div>""", unsafe_allow_html=True)
