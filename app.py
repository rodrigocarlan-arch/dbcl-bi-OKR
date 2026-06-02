import streamlit as st
import pandas as pd
import io, requests
from datetime import date

st.set_page_config(page_title="DBCL — OKR 2026", page_icon="🎯", layout="wide",
                   initial_sidebar_state="expanded")

OKR_ID = "1WI7ogJK_s0gcDbMVFBtb0BuxzCWyyzmO"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Tomorrow:wght@400;600;700;900&display=swap');

@keyframes fadeUp { from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)} }
@keyframes pulse  { 0%,100%{opacity:1}50%{opacity:.2} }
@keyframes prog   { from{width:0} }

/* ── Reset & base ── */
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],
[data-testid="stMainBlockContainer"],.main,section.main,.block-container,
[data-testid="block-container"]{background-color:#FAF7EC!important;color:#23282E!important;font-family:'Lora',Georgia,serif!important}
*{box-sizing:border-box}

/* ── Sidebar ── */
[data-testid="stSidebar"]{background:#003C28!important;border-right:1px solid rgba(0,255,0,.1)!important}
[data-testid="stSidebar"] *{color:#FAF7EC!important;font-family:'Tomorrow',sans-serif!important}
[data-testid="stSidebar"] hr{border-color:rgba(0,255,0,.12)!important;margin:10px 0!important}
[data-testid="stSidebar"] label{color:rgba(250,247,236,.4)!important;font-size:8px!important;text-transform:uppercase!important;letter-spacing:2px!important;font-weight:700!important}
[data-testid="stSidebar"] [data-baseweb="radio"] label span{font-size:12px!important;letter-spacing:.3px!important;text-transform:none!important;white-space:nowrap!important}
[data-testid="stSidebar"] [data-baseweb="tag"]{background:rgba(0,255,0,.1)!important;border:1px solid rgba(0,255,0,.25)!important;border-radius:2px!important}
[data-testid="stSidebar"] [data-baseweb="tag"] [role="button"]{color:rgba(0,255,0,.6)!important}

/* ── Expander: fix black-on-green ── */
[data-testid="stExpander"]{border:1px solid rgba(0,60,40,.12)!important;border-radius:2px!important;background:#FAF7EC!important}
[data-testid="stExpander"] summary,[data-testid="stExpander"] details>summary{
    background:rgba(0,60,40,.06)!important;color:#003C28!important;
    font-family:'Tomorrow',sans-serif!important;font-size:11px!important;font-weight:600!important;
    padding:12px 16px!important;border-radius:2px!important}
[data-testid="stExpander"] summary:hover{background:rgba(0,60,40,.1)!important}
[data-testid="stExpander"] [data-testid="stExpanderDetails"]{padding:0!important}

/* ── Header ── */
.hdr{background:#003C28;border-radius:2px;border:1px solid rgba(0,255,0,.15);padding:18px 26px;margin-bottom:22px;display:flex;align-items:center;gap:18px;animation:fadeUp .3s ease}
.hdr-logo{display:flex;flex-direction:column;gap:1px;padding-right:18px;border-right:1px solid rgba(250,247,236,.15);flex-shrink:0}
.hdr-logo .dbcl{font-family:'Tomorrow',sans-serif;font-size:18px;font-weight:700;color:#FAF7EC;line-height:1;letter-spacing:1px}
.hdr-logo .adv{font-family:'Tomorrow',sans-serif;font-size:7px;color:rgba(250,247,236,.4);letter-spacing:4px;text-transform:uppercase;margin-top:2px}
.hdr-ctx{display:flex;flex-direction:column;gap:3px;padding-left:4px}
.hdr-ctx .pg{font-family:'Tomorrow',sans-serif;font-size:13px;font-weight:600;color:#FAF7EC}
.hdr-ctx .sub{font-family:'Tomorrow',sans-serif;font-size:9px;color:rgba(250,247,236,.45);letter-spacing:1.5px;text-transform:uppercase}
.hdr-right{margin-left:auto;display:flex;align-items:center;gap:6px;font-family:'Tomorrow',sans-serif;font-size:8px;color:rgba(0,255,0,.65);letter-spacing:2px;text-transform:uppercase;flex-shrink:0}
.hdr-dot{width:5px;height:5px;border-radius:50%;background:#00FF00;animation:pulse 2s infinite}

/* ── KPI cards ── */
.kpi{background:#003C28;border-radius:2px;padding:16px 18px;border-left:3px solid #00FF00;animation:fadeUp .25s ease}
.kpi.dim{border-left-color:rgba(0,255,0,.25)}
.kpi.warn{border-left-color:#C9A227}
.kpi.alert{border-left-color:#C0392B}
.kpi .lbl{font-family:'Tomorrow',sans-serif;font-size:8px;font-weight:700;color:rgba(250,247,236,.45);text-transform:uppercase;letter-spacing:2px;margin-bottom:7px}
.kpi .val{font-family:'Tomorrow',sans-serif;font-size:24px;font-weight:700;color:#FAF7EC;line-height:1}
.kpi .sub{font-family:'Tomorrow',sans-serif;font-size:9px;color:rgba(250,247,236,.4);margin-top:5px}

/* ── Section title ── */
.sec{font-family:'Tomorrow',sans-serif;font-size:9px;font-weight:700;color:rgba(0,60,40,.6);text-transform:uppercase;letter-spacing:2.5px;border-left:1.5px solid #00FF00;padding:5px 12px;background:rgba(0,255,0,.04);border-radius:0 2px 2px 0;margin:20px 0 12px}

/* ── Objective card ── */
.obj-card{background:#003C28;border-radius:2px;border:1px solid rgba(0,255,0,.18);padding:18px 20px 14px;margin-bottom:10px;animation:fadeUp .25s ease}
.obj-num{font-family:'Tomorrow',sans-serif;font-size:8px;font-weight:700;color:rgba(0,255,0,.5);text-transform:uppercase;letter-spacing:2px;margin-bottom:5px}
.obj-title{font-family:'Lora',serif;font-size:15px;font-weight:700;color:#FAF7EC;line-height:1.4;margin-bottom:14px}
.obj-bar-bg{background:rgba(0,255,0,.1);height:3px;border-radius:1px}
.obj-bar-fg{background:#00FF00;height:3px;border-radius:1px;animation:prog .8s ease}
.obj-stats{font-family:'Tomorrow',sans-serif;font-size:9px;color:rgba(250,247,236,.4);margin-top:6px}

/* ── KR progress card ── */
.kr-card{background:#FFFFFF;border-radius:2px;border:1px solid rgba(0,60,40,.1);border-left:3px solid rgba(0,255,0,.4);padding:14px 16px;margin-bottom:8px;animation:fadeUp .2s ease}
.kr-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-bottom:10px}
.kr-card-info{flex:1}
.kr-card-num{font-family:'Tomorrow',sans-serif;font-size:8px;font-weight:700;color:#1A6B45;letter-spacing:2px;text-transform:uppercase;margin-bottom:3px}
.kr-card-title{font-family:'Lora',serif;font-size:13px;font-weight:600;color:#003C28;line-height:1.4}
.kr-card-pct{font-family:'Tomorrow',sans-serif;font-size:28px;font-weight:900;color:#003C28;line-height:1;flex-shrink:0}
.kr-bar-bg{background:rgba(0,60,40,.08);height:4px;border-radius:1px}
.kr-bar-fg{height:4px;border-radius:1px;animation:prog .8s ease}
.kr-card-meta{display:flex;gap:14px;margin-top:8px;flex-wrap:wrap}
.kr-card-meta span{font-family:'Tomorrow',sans-serif;font-size:9px;color:#8FB89A}
.kr-card-meta .highlight{color:#1A6B45;font-weight:700}

/* ── Status bar (visão geral) ── */
.status-bar{display:flex;height:8px;border-radius:2px;overflow:hidden;margin:8px 0 6px;gap:2px}
.status-seg{height:100%;border-radius:1px}
.status-legend{display:flex;gap:16px;flex-wrap:wrap;margin-top:4px}
.status-leg-item{display:flex;align-items:center;gap:5px;font-family:'Tomorrow',sans-serif;font-size:9px;color:#8FB89A}
.status-leg-dot{width:6px;height:6px;border-radius:50%;flex-shrink:0}

/* ── KR block inside expander ── */
.kr-block{background:rgba(250,247,236,.8);border-radius:2px;border:1px solid rgba(0,60,40,.1);border-left:3px solid rgba(0,255,0,.35);padding:14px 16px;margin:8px 0 4px}
.kr-block-num{font-family:'Tomorrow',sans-serif;font-size:8px;font-weight:700;color:#1A6B45;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px}
.kr-block-title{font-family:'Lora',serif;font-size:14px;font-weight:600;color:#003C28;line-height:1.4}
.kr-block-meta{display:flex;gap:12px;margin-top:8px;flex-wrap:wrap}
.kr-block-meta span{font-family:'Tomorrow',sans-serif;font-size:9px;color:#8FB89A;display:flex;align-items:center;gap:4px}

/* ── Iniciativa row ── */
.ini-row{background:#FFFFFF;border-radius:2px;border-left:3px solid #D4C9A8;padding:12px 14px;margin:5px 0 2px 8px;display:flex;align-items:flex-start;justify-content:space-between;gap:12px}
.ini-left{flex:1;min-width:0}
.ini-title{font-family:'Lora',serif;font-size:13px;font-weight:600;color:#003C28;line-height:1.4}
.ini-meta{font-family:'Tomorrow',sans-serif;font-size:9px;color:#8FB89A;margin-top:5px;display:flex;gap:10px;flex-wrap:wrap}
.ini-right{flex-shrink:0;display:flex;flex-direction:column;align-items:flex-end;gap:5px}

/* ── Prazo badge ── */
.prazo{font-family:'Tomorrow',sans-serif;font-size:9px;font-weight:600;letter-spacing:.5px;display:flex;align-items:center;gap:4px}
.prazo.late{color:#C0392B}
.prazo.soon{color:#C9A227}
.prazo.ok{color:#8FB89A}

/* ── Ação row ── */
.acao-row{padding:10px 14px 10px 20px;border-bottom:1px solid rgba(0,60,40,.05);background:rgba(250,247,236,.5);display:flex;align-items:center;justify-content:space-between;gap:14px}
.acao-left{flex:1;min-width:0}
.acao-text{font-family:'Lora',serif;font-size:12px;color:#23282E;line-height:1.5}
.acao-meta{font-family:'Tomorrow',sans-serif;font-size:9px;color:#8FB89A;margin-top:3px;display:flex;gap:10px;flex-wrap:wrap}
.acao-right{flex-shrink:0;display:flex;align-items:center;gap:6px}

/* ── Pills ── */
.spill{font-family:'Tomorrow',sans-serif;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;padding:3px 8px;border-radius:2px;white-space:nowrap}
.dpill{font-family:'Tomorrow',sans-serif;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:1px;padding:2px 7px;border-radius:2px;background:rgba(0,60,40,.07);color:#1A6B45;border:1px solid rgba(0,60,40,.15);white-space:nowrap}
.p1{font-family:'Tomorrow',sans-serif;font-size:7px;font-weight:900;color:#00FF00;border:1px solid rgba(0,255,0,.4);padding:2px 5px;border-radius:2px;letter-spacing:1px}
.p2{font-family:'Tomorrow',sans-serif;font-size:7px;font-weight:700;color:#D4C9A8;border:1px solid rgba(212,201,168,.35);padding:2px 5px;border-radius:2px;letter-spacing:1px}

/* ── Responsible cards ── */
.resp-card{background:#003C28;border-radius:2px;border-left:3px solid #00FF00;padding:14px 16px;animation:fadeUp .2s ease}
.resp-card.warn{border-left-color:#C9A227}
.resp-card.alert{border-left-color:#C0392B}
.resp-name{font-family:'Tomorrow',sans-serif;font-size:9px;font-weight:700;color:rgba(250,247,236,.5);text-transform:uppercase;letter-spacing:2px;margin-bottom:5px}
.resp-pct{font-family:'Tomorrow',sans-serif;font-size:26px;font-weight:700;color:#FAF7EC;line-height:1}
.resp-meta{font-family:'Tomorrow',sans-serif;font-size:9px;color:rgba(250,247,236,.4);margin-top:5px}
.resp-bar-bg{background:rgba(0,255,0,.1);height:3px;border-radius:1px;margin-top:8px}
.resp-bar-fg{background:#00FF00;height:3px;border-radius:1px}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{background:rgba(0,60,40,.06);border-radius:2px;padding:3px;gap:2px;border:1px solid rgba(0,255,0,.1)}
.stTabs [data-baseweb="tab"]{border-radius:2px;padding:7px 16px;font-family:'Tomorrow',sans-serif!important;font-size:9px!important;font-weight:700!important;text-transform:uppercase!important;letter-spacing:1.5px!important;color:rgba(0,60,40,.5)!important}
.stTabs [aria-selected="true"]{background:#003C28!important;color:#FAF7EC!important;border:1px solid rgba(0,255,0,.2)!important}

hr{border:none;border-top:1px solid rgba(0,255,0,.08);margin:14px 0}
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

STATUS_STYLES = {
    'concluído': ('background:#1A6B45;color:#FFFFFF;border:1px solid #1A6B45', 'CONCLUÍDO'),
    'andamento': ('background:#C9A227;color:#23282E;border:1px solid #C9A227', 'EM ANDAMENTO'),
    'iniciar':   ('background:rgba(212,201,168,.3);color:#5A4020;border:1px solid rgba(212,201,168,.5)', 'A INICIAR'),
    'atrasado':  ('background:#C0392B;color:#FFFFFF;border:1px solid #C0392B', 'ATRASADO'),
}

def get_status_key(status, late=False):
    if late: return 'atrasado'
    s = str(status).lower()
    if 'concluí' in s or 'concluido' in s: return 'concluído'
    if 'andamento' in s: return 'andamento'
    return 'iniciar'

def spill(status, late=False):
    k = get_status_key(status, late)
    style, label = STATUS_STYLES[k]
    return f'<span class="spill" style="{style}">{label}</span>'

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

def safe_dt(d):
    try:
        if pd.isna(d): return None
        result = pd.to_datetime(d, errors='coerce', dayfirst=True)
        return None if pd.isna(result) else result
    except: return None

def days_left(d):
    try:
        dt = safe_dt(d)
        if dt is None: return None
        return (dt.date() - date.today()).days
    except: return None

def prazo_badge(d, status=''):
    dias = days_left(d)
    if dias is None: return '<span class="prazo ok">Sem prazo</span>'
    dt = safe_dt(d)
    date_str = dt.strftime('%d/%m/%y') if dt else '—'
    s = str(status).lower()
    concluido = 'concluí' in s or 'concluido' in s
    if concluido:
        return f'<span class="prazo ok">✓ {date_str}</span>'
    if dias < 0:
        return f'<span class="prazo late">⚠ {date_str} ({abs(dias)}d atraso)</span>'
    if dias <= 14:
        return f'<span class="prazo soon">⏱ {date_str} ({dias}d)</span>'
    return f'<span class="prazo ok">📅 {date_str}</span>'

def is_late(row):
    dias = days_left(row['prazo'])
    if dias is None: return False
    s = str(row['status']).lower()
    return dias < 0 and 'concluí' not in s and 'concluido' not in s

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
    raw = raw.rename(columns={cols[0]:'tipo',cols[1]:'descricao',cols[7]:'dono',
                               cols[8]:'socio',cols[9]:'prazo',cols[10]:'status_mai',
                               cols[11]:'status_jun',cols[12]:'prioridade'})
    for c in cols[2:7]:
        if c in raw.columns:
            mask = raw['descricao'].isna() & raw[c].notna()
            raw.loc[mask,'descricao'] = raw.loc[mask,c]
    raw = raw[raw['tipo'].notna()].copy()
    raw = raw[~raw['tipo'].str.strip().eq('OKR - PLANEJAMENTO ESTRATÉGICO')]
    def level(t):
        t=str(t).strip()
        if t.startswith('Objetivo'): return 'objetivo'
        if t.startswith('KR'):       return 'kr'
        if t.startswith('Inicia'):   return 'iniciativa'
        if t.startswith('Ação'):     return 'acao'
        return 'outro'
    raw['nivel'] = raw['tipo'].apply(level)
    co,ck,cod,ckd=[],[],[],[]
    curr_obj=curr_kr=curr_obj_desc=curr_kr_desc=None
    for _,row in raw.iterrows():
        if row['nivel']=='objetivo': curr_obj=row['tipo'];curr_obj_desc=str(row['descricao']).strip();curr_kr=None;curr_kr_desc=None
        elif row['nivel']=='kr':     curr_kr=row['tipo']; curr_kr_desc=str(row['descricao']).strip()
        co.append(curr_obj);ck.append(curr_kr);cod.append(curr_obj_desc);ckd.append(curr_kr_desc)
    raw['ctx_obj']=co;raw['ctx_kr']=ck;raw['ctx_obj_desc']=cod;raw['ctx_kr_desc']=ckd
    raw['status'] = raw['status_jun'].where(
        raw['status_jun'].notna()&raw['status_jun'].apply(lambda x:isinstance(x,str)),raw['status_mai'])
    raw['status'] = raw['status'].apply(lambda x: x if isinstance(x,str) else 'A iniciar')
    raw['prazo_dt'] = raw['prazo'].apply(safe_dt)
    return raw

# ── Load ──────────────────────────────────────────────────────────────────────
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
concluidos = acoes['status'].str.contains('concluí|concluido',case=False,na=False).sum()
andamento  = acoes['status'].str.contains('andamento',case=False,na=False).sum()
a_iniciar  = tots - concluidos - andamento
atrasadas  = acoes[acoes['late']]
pct = int(concluidos/tots*100) if tots else 0

# ══════════════════════════════════════════════════════════════════
# VISÃO GERAL
# ══════════════════════════════════════════════════════════════════
if page == "🎯  Visão Geral":
    hdr("OKR 2026 — Visão Geral","Planejamento estratégico DBCL")

    k1,k2,k3,k4,k5 = st.columns(5)
    kpi_card(k1,"Progresso Geral",f"{pct}%",f"{concluidos}/{tots} concluídas")
    kpi_card(k2,"Em Andamento",str(andamento),"ações ativas","warn")
    kpi_card(k3,"A Iniciar",str(a_iniciar),"não iniciadas","dim")
    kpi_card(k4,"Atrasadas",str(len(atrasadas)),"prazo vencido","alert")
    kpi_card(k5,"2 Obj · 5 KRs","65 ações","22 iniciativas","dim")

    # Status bar visual
    if tots > 0:
        w_c = round(concluidos/tots*100,1)
        w_a = round(andamento/tots*100,1)
        w_l = round(len(atrasadas)/tots*100,1)
        w_i = round(100-w_c-w_a-w_l,1)
        st.markdown(f"""<div style="margin:12px 0 4px">
            <div class="status-bar">
                <div class="status-seg" style="width:{w_c}%;background:#1A6B45"></div>
                <div class="status-seg" style="width:{w_a}%;background:#C9A227"></div>
                <div class="status-seg" style="width:{w_l}%;background:#C0392B"></div>
                <div class="status-seg" style="width:{w_i}%;background:rgba(212,201,168,.4)"></div>
            </div>
            <div class="status-legend">
                <div class="status-leg-item"><div class="status-leg-dot" style="background:#1A6B45"></div>{concluidos} Concluídas</div>
                <div class="status-leg-item"><div class="status-leg-dot" style="background:#C9A227"></div>{andamento} Em andamento</div>
                <div class="status-leg-item"><div class="status-leg-dot" style="background:#C0392B"></div>{len(atrasadas)} Atrasadas</div>
                <div class="status-leg-item"><div class="status-leg-dot" style="background:rgba(212,201,168,.6)"></div>{a_iniciar} A iniciar</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:4px 0 16px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])

    with c1:
        sec("Progresso por Objetivo")
        for obj_key in df[df['nivel']=='objetivo']['tipo'].tolist():
            oa = acoes[acoes['ctx_obj']==obj_key]
            obj_desc = df[df['tipo']==obj_key]['descricao'].iloc[0]
            tot_o=len(oa); conc_o=oa['status'].str.contains('concluí|concluido',case=False,na=False).sum()
            and_o=oa['status'].str.contains('andamento',case=False,na=False).sum()
            pct_o=int(conc_o/tot_o*100) if tot_o else 0
            late_o=oa[oa.apply(is_late,axis=1)]
            st.markdown(f"""<div class="obj-card">
                <div class="obj-num">{obj_key}</div>
                <div class="obj-title">{obj_desc}</div>
                <div class="obj-bar-bg"><div class="obj-bar-fg" style="width:{pct_o}%"></div></div>
                <div class="obj-stats">{pct_o}% concluído &nbsp;·&nbsp; {and_o} em andamento &nbsp;·&nbsp; {len(late_o)} atrasadas &nbsp;·&nbsp; {tot_o} ações</div>
            </div>""", unsafe_allow_html=True)

        if len(atrasadas) > 0:
            sec("⚠ Atrasadas agora")
            for _,a in atrasadas.head(6).iterrows():
                st.markdown(f"""<div class="acao-row" style="border-left:3px solid #C0392B">
                    <div class="acao-left">
                        <div class="acao-text">{a['descricao']}</div>
                        <div class="acao-meta"><span>{a['ctx_kr']}</span></div>
                    </div>
                    <div class="acao-right">{dpill(a['dono'])}{prazo_badge(a['prazo'],a['status'])}</div>
                </div>""", unsafe_allow_html=True)

    with c2:
        sec("Progresso por KR")
        for _,kr in df[df['nivel']=='kr'].iterrows():
            ka = acoes[acoes['ctx_kr']==kr['tipo']]
            tot_k=len(ka); conc_k=ka['status'].str.contains('concluí|concluido',case=False,na=False).sum()
            and_k=ka['status'].str.contains('andamento',case=False,na=False).sum()
            pct_k=int(conc_k/tot_k*100) if tot_k else 0
            bar_color = '#1A6B45' if pct_k>50 else ('#C9A227' if pct_k>0 else 'rgba(0,60,40,.15)')
            desc_short = str(kr['descricao'])[:60]+'…' if len(str(kr['descricao']))>60 else kr['descricao']
            st.markdown(f"""<div class="kr-card">
                <div class="kr-card-top">
                    <div class="kr-card-info">
                        <div class="kr-card-num">{kr['tipo']}</div>
                        <div class="kr-card-title">{desc_short}</div>
                    </div>
                    <div class="kr-card-pct" style="color:{bar_color}">{pct_k}%</div>
                </div>
                <div class="kr-bar-bg"><div class="kr-bar-fg" style="width:{pct_k}%;background:{bar_color}"></div></div>
                <div class="kr-card-meta">
                    <span class="highlight">{and_k} em andamento</span>
                    <span>{conc_k} concluídas</span>
                    <span>{tot_k} totais</span>
                    <span>{dpill(kr['dono'])}</span>
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# POR OBJETIVO
# ══════════════════════════════════════════════════════════════════
elif page == "📌  Por Objetivo":
    hdr("OKR 2026 — Por Objetivo","Hierarquia completa")

    objs = df[df['nivel']=='objetivo']['tipo'].tolist()
    obj_sel = st.selectbox("", objs,
        format_func=lambda x: f"{x}: {str(df[df['tipo']==x]['descricao'].iloc[0])[:60]}…",
        label_visibility="collapsed")

    obj_desc = df[df['tipo']==obj_sel]['descricao'].iloc[0]
    oa=acoes[acoes['ctx_obj']==obj_sel]; tot_o=len(oa)
    conc_o=oa['status'].str.contains('concluí|concluido',case=False,na=False).sum()
    and_o=oa['status'].str.contains('andamento',case=False,na=False).sum()
    pct_o=int(conc_o/tot_o*100) if tot_o else 0
    st.markdown(f"""<div class="obj-card" style="margin-bottom:16px">
        <div class="obj-num">{obj_sel}</div>
        <div class="obj-title">{obj_desc}</div>
        <div class="obj-bar-bg"><div class="obj-bar-fg" style="width:{pct_o}%"></div></div>
        <div class="obj-stats">{pct_o}% concluído &nbsp;·&nbsp; {and_o} em andamento &nbsp;·&nbsp; {tot_o} ações</div>
    </div>""", unsafe_allow_html=True)

    for _,kr in df[(df['nivel']=='kr')&(df['ctx_obj']==obj_sel)].iterrows():
        ka=acoes[acoes['ctx_kr']==kr['tipo']]
        tot_k=len(ka); conc_k=ka['status'].str.contains('concluí|concluido',case=False,na=False).sum()
        and_k=ka['status'].str.contains('andamento',case=False,na=False).sum()
        pct_k=int(conc_k/tot_k*100) if tot_k else 0

        with st.expander(f"{kr['tipo']} — {kr['descricao']}", expanded=True):
            st.markdown(f"""<div class="kr-block">
                <div class="kr-block-num">{kr['tipo']}</div>
                <div class="kr-block-title">{kr['descricao']}</div>
                <div class="kr-block-meta">
                    <span>👤 {kr['dono']}</span>
                    <span>🔍 {kr['socio']}</span>
                    <span style="color:#1A6B45;font-weight:700">{pct_k}% concluído</span>
                    <span>{and_k} em andamento</span>
                    <span>{tot_k} ações</span>
                </div>
            </div>""", unsafe_allow_html=True)

            for _,ini in df[(df['nivel']=='iniciativa')&(df['ctx_kr']==kr['tipo'])].iterrows():
                p=ppill(ini['prioridade']); late_ini=is_late(ini)
                st.markdown(f"""<div class="ini-row">
                    <div class="ini-left">
                        <div class="ini-title">{ini['tipo']}: {ini['descricao']}</div>
                        <div class="ini-meta">{prazo_badge(ini['prazo'],ini['status'])}</div>
                    </div>
                    <div class="ini-right">{dpill(ini['dono'])}{p}{spill(ini['status'],late_ini)}</div>
                </div>""", unsafe_allow_html=True)

                num=ini['tipo'].split()[-1]
                for _,ac in df[(df['nivel']=='acao')&(df['ctx_kr']==kr['tipo'])&df['tipo'].str.match(f"Ação {num}\\.")].iterrows():
                    late_ac=is_late(ac); p2=ppill(ac['prioridade'])
                    st.markdown(f"""<div class="acao-row">
                        <div class="acao-left">
                            <div class="acao-text">{ac['tipo']}: {ac['descricao']}</div>
                            <div class="acao-meta">{prazo_badge(ac['prazo'],ac['status'])}</div>
                        </div>
                        <div class="acao-right">{dpill(ac['dono'])}{p2}{spill(ac['status'],late_ac)}</div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# POR RESPONSÁVEL
# ══════════════════════════════════════════════════════════════════
elif page == "👤  Por Responsável":
    hdr("OKR 2026 — Por Responsável","Carga e progresso por pessoa")

    donos = sorted(df[df['dono'].notna()&~df['dono'].isin(['Dono','nan'])]['dono'].unique())
    cols = st.columns(len(donos))
    for i,dono in enumerate(donos):
        da=acoes[acoes['dono']==dono]
        tot_d=len(da); conc_d=da['status'].str.contains('concluí|concluido',case=False,na=False).sum()
        and_d=da['status'].str.contains('andamento',case=False,na=False).sum()
        pct_d=int(conc_d/tot_d*100) if tot_d else 0
        late_d=da[da.apply(is_late,axis=1)]
        v='alert' if len(late_d)>2 else ('warn' if and_d>0 else 'dim')
        with cols[i]:
            st.markdown(f"""<div class="resp-card {v}">
                <div class="resp-name">{dono}</div>
                <div class="resp-pct">{pct_d}%</div>
                <div class="resp-meta">{tot_d} ações · {len(late_d)} atrasadas</div>
                <div class="resp-bar-bg"><div class="resp-bar-fg" style="width:{pct_d}%"></div></div>
            </div>""", unsafe_allow_html=True)

    sec("Detalhe por responsável")
    dono_sel = st.selectbox("", donos, label_visibility="collapsed")
    d_acoes = acoes[acoes['dono']==dono_sel].copy()

    def render_list(df_sub):
        if df_sub.empty:
            st.markdown("<div style='font-family:Tomorrow,sans-serif;font-size:10px;color:#8FB89A;padding:14px 0'>Nenhuma ação neste filtro.</div>", unsafe_allow_html=True)
            return
        for _,a in df_sub.iterrows():
            late=is_late(a); p=ppill(a['prioridade'])
            st.markdown(f"""<div class="acao-row">
                <div class="acao-left">
                    <div class="acao-text">{a['tipo']}: {a['descricao']}</div>
                    <div class="acao-meta">
                        <span>{a['ctx_kr']}</span>
                        {prazo_badge(a['prazo'],a['status'])}
                    </div>
                </div>
                <div class="acao-right">{p}{spill(a['status'],late)}</div>
            </div>""", unsafe_allow_html=True)

    tabs = st.tabs(["▶ Em Andamento","○ A Iniciar","⚠ Atrasadas","≡ Todas"])
    with tabs[0]: render_list(d_acoes[d_acoes['status'].str.contains('andamento',case=False,na=False)])
    with tabs[1]: render_list(d_acoes[d_acoes['status'].str.contains('iniciar',case=False,na=False)])
    with tabs[2]: render_list(d_acoes[d_acoes.apply(is_late,axis=1)])
    with tabs[3]: render_list(d_acoes.sort_values('prazo_dt',na_position='last'))

# ══════════════════════════════════════════════════════════════════
# PRIORIDADES
# ══════════════════════════════════════════════════════════════════
elif page == "🔥  Prioridades":
    hdr("OKR 2026 — Prioridades","Ações críticas e próximos vencimentos")

    p1 = acoes[acoes['prioridade']==1.0].copy()
    p2 = acoes[acoes['prioridade']==2.0].copy()
    p1_late = p1[p1.apply(is_late,axis=1)]
    upcoming = acoes[acoes['prazo_dt'].notna()].copy()
    upcoming['dias'] = upcoming['prazo_dt'].apply(lambda d: (d.date()-date.today()).days if d else None)
    venc30 = upcoming[(upcoming['dias'].notna())&(upcoming['dias']<=30)&(upcoming['dias']>=0)]

    k1,k2,k3,k4 = st.columns(4)
    kpi_card(k1,"P1 — Críticas",str(len(p1)),f"{len(p1_late)} atrasadas","alert" if len(p1_late)>0 else "")
    kpi_card(k2,"P2 — Importantes",str(len(p2)),"","dim")
    kpi_card(k3,"Vencendo em 30d",str(len(venc30)),"requer atenção","warn")
    kpi_card(k4,"Atrasadas totais",str(len(atrasadas)),"prazo vencido","alert" if len(atrasadas)>0 else "dim")

    c1, c2 = st.columns(2)
    def render_priority(df_sub):
        if df_sub.empty:
            st.markdown("<div style='font-family:Tomorrow,sans-serif;font-size:10px;color:#8FB89A;padding:14px 0'>Nenhuma ação.</div>", unsafe_allow_html=True)
            return
        for _,a in df_sub.sort_values('prazo_dt',na_position='last').iterrows():
            late=is_late(a)
            st.markdown(f"""<div class="acao-row" style="{'border-left:3px solid #C0392B' if late else 'border-left:3px solid rgba(0,255,0,.3)'}">
                <div class="acao-left">
                    <div class="acao-text">{a['descricao']}</div>
                    <div class="acao-meta"><span>{a['ctx_kr']}</span>{prazo_badge(a['prazo'],a['status'])}</div>
                </div>
                <div class="acao-right">{dpill(a['dono'])}{spill(a['status'],late)}</div>
            </div>""", unsafe_allow_html=True)

    with c1:
        sec("P1 — Críticas")
        render_priority(p1)
    with c2:
        sec("P2 — Importantes")
        render_priority(p2)

    sec("Linha do tempo — próximos vencimentos")
    shown = upcoming.sort_values('prazo_dt',na_position='last').head(30)
    for _,a in shown.iterrows():
        late=is_late(a); p=ppill(a['prioridade'])
        st.markdown(f"""<div class="acao-row">
            <div class="acao-left">
                <div class="acao-text">{a['descricao']}</div>
                <div class="acao-meta"><span>{a['ctx_kr']}</span></div>
            </div>
            <div class="acao-right">{dpill(a['dono'])}{p}{prazo_badge(a['prazo'],a['status'])}{spill(a['status'],late)}</div>
        </div>""", unsafe_allow_html=True)
