import os
from html import escape
from decimal import Decimal

import pandas as pd
import plotly.express as px
import streamlit as st

from services.api import call

APP_DIR = os.path.dirname(__file__)
LOCAL_LOGO = os.path.join(APP_DIR, "assets", "pumphouseup-logo-circle.png")
SYSTEM_VERSION = "1.0"

st.set_page_config(page_title="Pumphouseup | Gestão", page_icon=LOCAL_LOGO, layout="wide", initial_sidebar_state="auto")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Manrope:wght@400;600;700;800&display=swap');
:root { --red:#f04438; --ink:#111214; --paper:#f4f4f2; --line:#deded9; }
html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
html, body, #root, .stApp { min-width:0; overflow-x:hidden; }
.stApp { background: var(--paper); }
header, header[data-testid="stHeader"] { display:none !important; }
section[data-testid="stSidebar"] { background:var(--ink); }
section[data-testid="stSidebar"] * { color:#fff; }
h1,h2,h3 { font-family:'Barlow Condensed', sans-serif; letter-spacing:0; text-transform:uppercase; }
.metric-card { background:#fff; border:1px solid var(--line); border-left:4px solid var(--red); padding:18px; min-height:112px; }
.metric-label { color:#777; font-size:.78rem; text-transform:uppercase; font-weight:700; }
.metric-value { color:var(--ink); font-size:1.75rem; font-weight:800; margin-top:8px; }
.theme-marker { display:none; }
.st-key-login-shell, .st-key-internal-shell { min-height:100vh; }
.st-key-internal-shell { background:var(--app-bg, #f4f4f2); color:var(--app-text, #171a21); }
.st-key-internal-shell.theme-dark { --app-bg:#080a0d; --app-surface:#101318; --app-surface-2:#15191f; --app-border:rgba(255,255,255,.09); --app-text:#f5f7fa; --app-muted:#9aa1ac; }
.st-key-internal-shell.theme-light { --app-bg:#f5f6f8; --app-surface:#fff; --app-surface-2:#f1f3f6; --app-border:#e2e5e9; --app-text:#171a21; --app-muted:#69707d; }
.st-key-internal-shell { box-sizing:border-box; min-width:0; width:100%; }
.st-key-internal-shell section[data-testid="stMain"] .main .block-container,
.stApp section[data-testid="stMain"] .main .block-container { box-sizing:border-box; margin:0 auto; max-width:1500px; min-width:0; padding:76px clamp(18px, 3vw, 48px) 42px; width:100%; }
.stApp section[data-testid="stSidebar"] { box-sizing:border-box; min-width:248px; width:248px; }
.stApp section[data-testid="stSidebar"] > div:first-child { width:248px; }
.stApp section[data-testid="stSidebar"] [data-testid="stSidebarContent"] { box-sizing:border-box; min-width:0; overflow-x:hidden; padding:18px 14px 22px; }
.st-key-login-shell { background:#080a0d; color:#f5f7fa; }
.st-key-login-shell header { display:none; }
.st-key-login-shell section[data-testid="stMain"] { padding-top:0; }
.st-key-login-shell .main .block-container { align-items:flex-start; box-sizing:border-box; display:flex; max-width:none; min-height:100dvh; padding:0 clamp(18px, 4vw, 64px); }
.st-key-login-shell { align-items:center; box-sizing:border-box; display:flex; height:calc(100dvh - 42px); justify-content:center; margin:0 auto; max-width:1240px; min-height:560px; padding:34px 0 28px; width:100%; }
.st-key-login-shell [data-testid="stHorizontalBlock"] { align-items:flex-start; gap:clamp(30px, 5vw, 72px); margin:0 auto; max-width:1180px; min-height:0; width:100%; }
.st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] { padding:0; }
.st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child { max-width:650px; }
.st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child { max-width:480px; }
.st-key-login-shell [data-testid="stColumn"] { position:relative; overflow:hidden; background:rgba(16,19,24,.94); border:1px solid rgba(255,255,255,.09); border-radius:18px; box-shadow:0 26px 80px rgba(0,0,0,.38), 0 0 70px rgba(240,68,56,.07); padding:42px clamp(28px, 4vw, 48px) 30px !important; }
.st-key-login-shell [data-testid="stColumn"] h2 { color:#f5f7fa; font-family:'Barlow Condensed', sans-serif; font-size:2rem; letter-spacing:.02em; margin:0; text-transform:uppercase; }
.st-key-login-shell [data-testid="stColumn"] label { color:#c9ced6 !important; font-size:.75rem !important; font-weight:700 !important; }
.st-key-login-shell [data-testid="stColumn"] input { background:#11141a !important; color:#fff; }
.st-key-login-shell [data-testid="stColumn"] div[data-testid="stButton"] button { min-height:48px; background:#d9362c; border:1px solid #f04438; border-radius:8px; color:#fff; }
.st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div { min-width:0; }
.st-key-login-shell img { max-width:100%; }
.stApp:has(.st-key-login-shell) { background:#080a0d; }
.st-key-login-shell { margin:0 auto; width:100%; }
.st-key-login-shell .main .block-container { margin:0 auto; width:100%; }
.stApp:has(.st-key-login-shell) section[data-testid="stMain"] { padding:0; }
.stApp:has(.st-key-login-shell) section[data-testid="stMain"] .main .block-container { align-items:flex-start; box-sizing:border-box; display:flex; max-width:none; min-height:100dvh; padding:0 clamp(18px, 4vw, 64px); }
.stApp:has(.st-key-internal-shell) section[data-testid="stMain"] .main .block-container { box-sizing:border-box; min-width:0; padding-top:76px; }
.stApp:has(.st-key-login-shell) .system-ribbon,
.system-ribbon { align-items:center; background:#101318; border-bottom:1px solid rgba(255,255,255,.09); box-sizing:border-box; color:#f5f7fa; display:flex; font-size:.66rem; justify-content:space-between; left:0; letter-spacing:.08em; min-height:42px; padding:0 clamp(18px, 4vw, 56px); position:fixed; right:0; text-transform:uppercase; top:0; z-index:1000; }
.system-ribbon-brand { color:#f5f7fa; }
.system-ribbon-version { color:#f5f7fa; font-weight:800; }
.system-ribbon-author, .system-ribbon-meta { color:#9aa1ac; }
.stApp:has(.theme-marker) { background:#f5f6f8; }
.stApp:has(.theme-marker) .system-ribbon { background:#101318; color:#f5f7fa; }
section[data-testid="stSidebar"] [data-testid="stImage"] img { max-height:220px; object-fit:contain; }
.stApp:has(.theme-marker) section[data-testid="stMain"] .main .block-container { max-width:1500px; padding-top:76px; }
.stApp:has(.theme-marker) h1, .stApp:has(.theme-marker) h2, .stApp:has(.theme-marker) h3 { color:#172235; }
.stApp:has(.theme-marker) .page-title { color:#172235; }
.stApp:has(.theme-marker) .topbar { border-bottom-color:#e2e5e9; }
.stApp:has(.theme-dark-marker) { background:#080a0d; color:#f5f7fa; }
.stApp:has(.theme-dark-marker) section[data-testid="stSidebar"] { background:#101318; border-right:1px solid rgba(255,255,255,.08); }
.stApp:has(.theme-dark-marker) section[data-testid="stSidebar"] * { color:#f5f7fa; }
.stApp:has(.theme-dark-marker) section[data-testid="stMain"] .main .block-container { background:#080a0d; }
.stApp:has(.theme-dark-marker) h1, .stApp:has(.theme-dark-marker) h2, .stApp:has(.theme-dark-marker) h3 { color:#f5f7fa; }
.stApp:has(.theme-dark-marker) .page-title,
.stApp:has(.theme-dark-marker) .page-header h1,
.stApp:has(.theme-dark-marker) .topbar-user,
.stApp:has(.theme-dark-marker) .page-header h2,
.stApp:has(.theme-dark-marker) .page-header h3 { color:#f5f7fa !important; }
.stApp:has(.theme-dark-marker) .page-subtitle, .stApp:has(.theme-dark-marker) .topbar-context { color:#b8c0cc !important; }
.stApp:has(.theme-dark-marker) .topbar { border-bottom-color:rgba(255,255,255,.09); }
.stApp:has(.theme-dark-marker) [data-testid="stTextInputRootElement"], .stApp:has(.theme-dark-marker) [data-baseweb="input"], .stApp:has(.theme-dark-marker) [data-baseweb="select"] { background:#11141a; border-color:#252a32; }
.stApp:has(.theme-dark-marker) input, .stApp:has(.theme-dark-marker) textarea { color:#f5f7fa; }
.stApp:has(.theme-dark-marker) .surface, .stApp:has(.theme-dark-marker) .metric-card, .stApp:has(.theme-dark-marker) .empty-state { background:#101318; border-color:rgba(255,255,255,.09); color:#f5f7fa; }
.stApp:has(.theme-dark-marker) .metric-label, .stApp:has(.theme-dark-marker) .empty-state-copy { color:#9aa1ac; }
.stApp:has(.theme-dark-marker) .metric-value, .stApp:has(.theme-dark-marker) .empty-state-title { color:#f5f7fa; }
.stApp:has(.theme-dark-marker) .theme-toggle button { background:#15191f !important; border:1px solid rgba(255,255,255,.14) !important; color:#f5f7fa !important; }
.stApp:has(.theme-dark-marker) [data-testid="stDataFrame"], .stApp:has(.theme-dark-marker) [data-testid="stTable"] { background:#101318; border:1px solid rgba(255,255,255,.12); }
.stApp:has(.theme-dark-marker) [data-testid="stExpander"], .stApp:has(.theme-dark-marker) [data-testid="stForm"] { background:#101318; border:1px solid rgba(255,255,255,.1); }
.stApp:has(.theme-dark-marker) [data-testid="stExpander"] summary, .stApp:has(.theme-dark-marker) [data-testid="stExpander"] summary span { color:#f5f7fa !important; }
.stApp:has(.theme-dark-marker) label, .stApp:has(.theme-dark-marker) [data-testid="stCaptionContainer"], .stApp:has(.theme-dark-marker) [data-testid="stMarkdownContainer"] p { color:#d5dae2; }
.stApp:has(.theme-dark-marker) [data-testid="stAlert"] { background:#15191f; border:1px solid rgba(255,255,255,.14); color:#f5f7fa; }
.stApp:has(.theme-dark-marker) [data-testid="stAlert"] p { color:#f5f7fa !important; }
.stApp:has(.theme-dark-marker) div.stButton > button:not([kind="primary"]), .stApp:has(.theme-dark-marker) button[data-testid="baseButton-secondary"], .stApp:has(.theme-dark-marker) [data-testid="stDownloadButton"] button { background:#15191f !important; border:1px solid rgba(255,255,255,.16) !important; color:#f5f7fa !important; }
.stApp:has(.theme-dark-marker) div.stButton > button:not([kind="primary"]):hover, .stApp:has(.theme-dark-marker) button[data-testid="baseButton-secondary"]:hover, .stApp:has(.theme-dark-marker) [data-testid="stDownloadButton"] button:hover { background:#202630 !important; border-color:rgba(240,68,56,.55) !important; color:#fff !important; }
.stApp:has(.theme-dark-marker) [data-baseweb="select"] *, .stApp:has(.theme-dark-marker) [data-baseweb="popover"] * { color:#f5f7fa !important; }
.stApp:has(.theme-dark-marker) [data-baseweb="popover"] { background:#15191f; border:1px solid rgba(255,255,255,.14); }
.stApp:has(.theme-light-marker) { background:#f5f6f8; color:#171a21; }
.stApp:has(.theme-light-marker) section[data-testid="stSidebar"] { background:#f9fafb; border-right:1px solid #e2e5e9; }
.stApp:has(.theme-light-marker) section[data-testid="stSidebar"] * { color:#30343b; }
.stApp:has(.theme-light-marker) section[data-testid="stMain"] .main .block-container { background:#f5f6f8; }
.stApp:has(.theme-light-marker) h1, .stApp:has(.theme-light-marker) h2, .stApp:has(.theme-light-marker) h3, .stApp:has(.theme-light-marker) .page-title { color:#172235; }
.stApp:has(.theme-light-marker) .page-subtitle, .stApp:has(.theme-light-marker) .topbar-context { color:#69707d; }
.stApp:has(.theme-light-marker) [data-testid="stTextInputRootElement"], .stApp:has(.theme-light-marker) [data-baseweb="input"], .stApp:has(.theme-light-marker) [data-baseweb="select"] { background:#fff; border-color:#dfe3e8; }
.stApp:has(.theme-light-marker) input, .stApp:has(.theme-light-marker) textarea { color:#171a21; }
.stApp:has(.theme-light-marker) .surface, .stApp:has(.theme-light-marker) .metric-card, .stApp:has(.theme-light-marker) .empty-state { background:#fff; border-color:#e2e5e9; color:#171a21; }
.stApp:has(.theme-light-marker) .metric-label, .stApp:has(.theme-light-marker) .empty-state-copy { color:#69707d; }
.stApp:has(.theme-light-marker) .metric-value, .stApp:has(.theme-light-marker) .empty-state-title { color:#171a21; }
.stApp:has(.theme-light-marker) .theme-toggle button { background:#fff !important; border:1px solid #dfe3e8 !important; color:#30343b !important; }
.stApp:has(.theme-dark-marker) section[data-testid="stSidebar"] div.stButton > button,
.stApp:has(.theme-light-marker) section[data-testid="stSidebar"] div.stButton > button { background:#d9362c !important; border:1px solid #f04438 !important; border-radius:7px; color:#fff !important; min-height:38px; }
.stApp:has(.theme-dark-marker) section[data-testid="stSidebar"] div.stButton > button:hover,
.stApp:has(.theme-light-marker) section[data-testid="stSidebar"] div.stButton > button:hover { background:#ef493d !important; border-color:#ff7067 !important; color:#fff !important; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] { background:#101318; border-right:1px solid rgba(255,255,255,.08); }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stImage"] { padding:12px 22px 0; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] > label { color:#8f98a5 !important; font-size:.65rem !important; font-weight:800 !important; letter-spacing:.12em; text-transform:uppercase; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap:4px; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] { min-height:42px; padding:0 12px; border-left:3px solid transparent; border-radius:6px; color:#aeb5c0; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] { background:rgba(240,68,56,.14); border-left-color:#f04438; color:#fff; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] > div:first-child { display:none; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] p { font-size:.8rem; font-weight:700; }
.page-header { display:flex; align-items:flex-end; justify-content:space-between; gap:24px; margin:0 0 26px; }
.page-kicker { color:#f04438; font-size:.68rem; font-weight:800; letter-spacing:.14em; margin:0 0 7px; text-transform:uppercase; }
.page-title { color:var(--app-text, #171a21); font-family:'Barlow Condensed', sans-serif; font-size:clamp(2rem, 3vw, 3.2rem); line-height:1; margin:0; text-transform:uppercase; }
.page-subtitle { color:var(--app-muted, #69707d); font-size:.84rem; margin:8px 0 0; }
.topbar { align-items:center; border-bottom:1px solid var(--app-border, #e2e5e9); display:flex; justify-content:space-between; margin-bottom:26px; padding:0 0 18px; }
.topbar-context { color:var(--app-muted, #69707d); font-size:.72rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.topbar-user { color:var(--app-text, #171a21); font-size:.78rem; font-weight:800; }
.topbar-user:before { background:#f04438; border-radius:50%; content:""; display:inline-block; height:8px; margin-right:8px; width:8px; }
.surface { background:var(--app-surface, #fff); border:1px solid var(--app-border, #e2e5e9); border-radius:10px; padding:22px; }
.metric-card { background:var(--app-surface, #fff); border:1px solid var(--app-border, #deded9); border-left:3px solid #f04438; border-radius:8px; color:var(--app-text, #171a21); min-height:122px; padding:18px; }
.metric-label { color:var(--app-muted, #69707d); }
.metric-value { color:var(--app-text, #171a21); }
.empty-state { background:var(--app-surface, #fff); border:1px dashed var(--app-border, #e2e5e9); border-radius:10px; padding:52px 24px; text-align:center; }
.empty-state-title { color:var(--app-text, #171a21); font-size:1.05rem; font-weight:800; margin:0 0 8px; }
.empty-state-copy { color:var(--app-muted, #69707d); font-size:.82rem; margin:0; }
.app-shell.app-shell-internal [data-testid="stDataFrame"] { border:1px solid rgba(255,255,255,.08); }
.app-shell.app-shell-internal [data-testid="stTextInputRootElement"], .app-shell.app-shell-internal [data-baseweb="select"], .app-shell.app-shell-internal [data-baseweb="input"] { background:#11141a; border-color:#252a32; }
.app-shell.app-shell-internal input, .app-shell.app-shell-internal textarea { color:#f5f7fa; }
.app-shell.app-shell-internal label, .app-shell.app-shell-internal p, .app-shell.app-shell-internal .stMarkdown { color:var(--app-muted); }
.app-shell.app-shell-internal h1, .app-shell.app-shell-internal h2, .app-shell.app-shell-internal h3 { color:#f5f7fa; }
.app-shell.app-shell-internal div.stButton > button[kind="primary"] { background:#d9362c; border-color:#f04438; color:#fff; }
.app-shell.app-shell-internal header, .app-shell.app-shell-internal header[data-testid="stHeader"] { background:var(--app-bg, #080a0d) !important; border-bottom:1px solid var(--app-border, rgba(255,255,255,.08)); }
.app-shell.app-shell-internal div.stButton > button:not([kind="primary"]), .app-shell.app-shell-internal button[data-testid="baseButton-secondary"] { background:#15191f !important; border:1px solid rgba(255,255,255,.1) !important; color:#f5f7fa !important; }
.app-shell.app-shell-internal div.stButton > button:not([kind="primary"]):hover { background:#202630 !important; border-color:rgba(240,68,56,.45) !important; color:#fff !important; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] { display:none !important; }
.app-shell.app-shell-internal .theme-toggle button { align-items:center; background:var(--app-surface-2, #15191f); border:1px solid var(--app-border, rgba(255,255,255,.1)); border-radius:8px; color:var(--app-text, #f5f7fa); display:flex; font-size:1rem; height:38px; justify-content:center; min-width:38px; padding:0; transition:background-color .2s ease, border-color .2s ease, color .2s ease, transform .2s ease; width:38px; }
.app-shell.app-shell-internal .theme-toggle button:hover { background:rgba(240,68,56,.12); border-color:rgba(240,68,56,.4); color:#f04438; transform:translateY(-1px); }
.app-shell.app-shell-internal section[data-testid="stSidebar"] div.stButton > button { background:rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.1); border-radius:7px; color:#f5f7fa; min-height:38px; transition:background-color .2s ease, border-color .2s ease, color .2s ease; }
.app-shell.app-shell-internal section[data-testid="stSidebar"] div.stButton > button:hover { background:rgba(229,57,53,.12); border-color:rgba(229,57,53,.35); color:#ffb5ae; }
.app-shell.app-shell-internal .system-ribbon { background:var(--app-surface, #101318); border-bottom-color:var(--app-border, rgba(255,255,255,.09)); color:var(--app-text, #f5f7fa); }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] { background:#f9fafb; border-right:1px solid #e2e5e9; }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] * { color:#30343b; }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] [data-testid="stRadio"] > label { color:#69707d !important; }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"] { color:#69707d; }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] [data-testid="stRadio"] [role="radio"][aria-checked="true"] { background:#fff1f1; color:#171a21; }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] div.stButton > button { background:#fff; border-color:#dfe3e8; color:#30343b; }
.app-shell.app-shell-internal.theme-light section[data-testid="stSidebar"] div.stButton > button:hover { background:#fff1f1; border-color:rgba(229,57,53,.45); color:#d9362c; }
.app-shell.app-shell-internal.theme-light .system-ribbon { background:#fff; color:#171a21; }
.app-shell.app-shell-internal.theme-light .system-ribbon-meta, .app-shell.app-shell-internal.theme-light .system-ribbon-author { color:#69707d; }
.app-shell.app-shell-internal .system-ribbon { align-items:center; background:rgba(10,12,16,.96); border-bottom:1px solid rgba(255,255,255,.09); box-sizing:border-box; color:#f5f7fa; display:flex; font-size:.66rem; justify-content:space-between; left:0; letter-spacing:.08em; min-height:42px; padding:0 clamp(18px, 4vw, 56px); pointer-events:none; position:fixed; right:0; text-transform:uppercase; top:0; z-index:1000; }
.system-ribbon-brand { align-items:center; display:flex; font-weight:800; gap:10px; }
.system-ribbon-brand:before { background:#f04438; border-radius:50%; box-shadow:0 0 12px rgba(240,68,56,.55); content:""; height:6px; width:6px; }
.system-ribbon-meta { align-items:center; color:#9aa1ac; display:flex; gap:18px; }
.system-ribbon-version { color:#f5f7fa; font-weight:800; }
.system-ribbon-author { color:#9aa1ac; }
.app-shell.login-shell { background:#080a0d; color:#f5f7fa; }
.app-shell.login-shell header { display:none; }
.app-shell.login-shell section[data-testid="stMain"] { padding-top:0; }
.app-shell.login-shell .main .block-container { align-items:center; box-sizing:border-box; display:flex; max-width:none; min-height:100dvh; padding:32px 40px; }
.app-shell.login-shell .main .block-container { padding-top:78px; }
.app-shell.login-shell div[data-testid="stImage"] img { height:112px !important; object-fit:contain; width:112px !important; }
.app-shell.login-shell div[data-testid="stImage"] img, .app-shell.app-shell-internal section[data-testid="stSidebar"] div[data-testid="stImage"] img { border-radius:50%; object-fit:cover; }
.app-shell.login-shell [data-testid="stHorizontalBlock"] { align-items:center; gap:clamp(38px, 5vw, 88px); margin:0 auto; max-width:1350px; min-height:0; width:100%; }
.app-shell.login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] { padding:0; }
.app-shell.login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child { max-width:650px; }
.app-shell.login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child { max-width:480px; }
.login-institutional { position:relative; padding:30px 0; }
.login-institutional:before { position:absolute; z-index:0; top:8%; left:2%; width:230px; height:230px; border-radius:50%; background:rgba(240,68,56,.13); filter:blur(70px); content:""; }
.login-brandline, .login-kicker, .login-title, .login-description, .login-benefits, .login-footnote { position:relative; z-index:1; }
.login-brandline { color:#f04438; font-size:.7rem; font-weight:800; letter-spacing:.18em; margin:18px 0 0; }
.login-kicker { color:#9aa1ac; font-size:.72rem; font-weight:800; letter-spacing:.16em; margin:24px 0 18px; }
.login-description { color:#9aa1ac; font-size:1rem; line-height:1.7; max-width:590px; margin:0; }
.login-description-mobile { display:none; }
.login-benefits { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:14px 28px; max-width:560px; margin:34px 0 0; }
.login-benefit { color:#d9dde3; font-size:.82rem; font-weight:600; }
.login-benefit:before { color:#f04438; content:"✓"; font-weight:800; margin-right:10px; }
.login-system-foot { color:#626a75; font-size:.7rem; letter-spacing:.08em; margin:56px 0 0; text-transform:uppercase; }
.app-shell.login-shell [data-testid="stColumn"] { position:relative; overflow:hidden; background:rgba(16,19,24,.94); border:1px solid rgba(255,255,255,.09); border-radius:18px; box-shadow:0 26px 80px rgba(0,0,0,.38), 0 0 70px rgba(240,68,56,.07); padding:42px clamp(28px, 4vw, 48px) 30px !important; }
.app-shell.login-shell [data-testid="stColumn"]:before { position:absolute; top:0; right:0; left:0; height:2px; background:linear-gradient(90deg, transparent, #f04438, transparent); content:""; }
.app-shell.login-shell [data-testid="stColumn"] h2 { color:#f5f7fa; font-family:'Barlow Condensed', sans-serif; font-size:2rem; letter-spacing:.02em; margin:0; text-transform:uppercase; }
.login-card-copy { color:#9aa1ac; font-size:.82rem; line-height:1.6; margin:8px 0 22px; }
.login-secure { color:#7fd49b; font-size:.7rem; font-weight:700; letter-spacing:.08em; margin:0 0 24px; text-transform:uppercase; }
.login-secure:before { color:#63d486; content:"●"; margin-right:8px; }
.app-shell.login-shell [data-testid="stColumn"] label { color:#c9ced6 !important; font-size:.75rem !important; font-weight:700 !important; }
.app-shell.login-shell [data-testid="stColumn"] div[data-baseweb="input"], .app-shell.login-shell [data-testid="stColumn"] div[data-baseweb="base-input"], .app-shell.login-shell [data-testid="stColumn"] input { background:#11141a !important; border-color:#252a32; border-radius:8px; transition:border-color .2s ease, box-shadow .2s ease; }
.app-shell.login-shell [data-testid="stColumn"] div[data-testid="stTextInputRootElement"] div[data-baseweb="base-input"] { background:#11141a !important; }
.app-shell.login-shell [data-testid="stColumn"] div[data-baseweb="input"]:focus-within { border-color:#f04438; box-shadow:0 0 0 3px rgba(240,68,56,.13); }
.app-shell.login-shell [data-testid="stColumn"] input { color:#fff; }
.app-shell.login-shell [data-testid="stColumn"] input::placeholder { color:#737983; }
.app-shell.login-shell [data-testid="stColumn"] div[data-testid="stButton"] button { min-height:48px; background:#d9362c; border:1px solid #f04438; border-radius:8px; box-shadow:0 10px 26px rgba(240,68,56,.2); color:#fff; font-size:.78rem; letter-spacing:.06em; transition:background .2s ease, box-shadow .2s ease, transform .2s ease; }
.app-shell.login-shell [data-testid="stColumn"] div[data-testid="stButton"] button:hover { background:#ef493d; box-shadow:0 14px 32px rgba(240,68,56,.3); transform:translateY(-1px); }
.app-shell.login-shell [data-testid="stColumn"] [data-testid="stAlert"] { background:rgba(240,68,56,.12); border:1px solid rgba(240,68,56,.4); border-radius:8px; color:#ffb5ae; }
.login-card-foot { border-top:1px solid rgba(255,255,255,.08); color:#727985; font-size:.7rem; line-height:1.5; margin-top:26px; padding-top:20px; }
.topbar-controls { align-items:center; display:flex; gap:10px; justify-content:flex-end; }
div.stButton > button { border-radius:2px; font-weight:800; }
#MainMenu, div[data-testid="stMainMenu"], div[data-testid="stToolbar"], div[data-testid="stDecoration"], div[data-testid="stStatusWidget"], footer, .stDeployButton { display:none !important; visibility:hidden !important; }
button[data-testid="stBaseButton-header"], button[data-testid="stBaseButton-elementToolbar"] { display:none !important; visibility:hidden !important; }
@media (max-width: 560px) {
    .system-ribbon { font-size:.56rem; min-height:38px; padding:0 14px; }
    .system-ribbon-meta { gap:8px; }
    .system-ribbon-author { display:none; }
    .app-shell.login-shell .main .block-container { padding-top:62px; }
}
@media (max-width: 768px) {
    .stApp section[data-testid="stSidebar"] { min-width:0; width:min(86vw, 300px); }
    .stApp section[data-testid="stSidebar"] > div:first-child { width:min(86vw, 300px); }
    .stApp section[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding:14px 12px 20px; }
    .stApp section[data-testid="stMain"] .main .block-container { padding:62px 14px 28px; }
    .st-key-login-shell .main .block-container { align-items:flex-start; min-height:100dvh; padding:0 14px; }
    .st-key-login-shell { align-items:flex-start; height:auto; margin:0 auto; max-width:520px; min-height:100dvh; padding:56px 0 26px; }
    .st-key-login-shell [data-testid="stHorizontalBlock"] { align-items:stretch; display:flex; flex-direction:column; gap:18px; max-width:520px; }
    .st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child,
    .st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child { max-width:none; width:100%; }
    .st-key-login-shell [data-testid="stColumn"] { border-radius:14px; padding:24px !important; }
    .st-key-login-shell [data-testid="stColumn"] h2 { font-size:1.75rem; }
    .st-key-login-shell [data-testid="stImage"] img { height:82px !important; width:82px !important; }
    .login-institutional { padding:0 4px; text-align:center; }
    .login-description { font-size:.84rem; line-height:1.55; margin:0 auto; max-width:390px; }
    .login-description-desktop { display:none; }
    .login-description-mobile { display:inline; }
    .login-benefits { gap:9px 12px; margin:20px auto 0; max-width:390px; text-align:left; }
    .login-benefit { font-size:.7rem; }
    .login-benefit-extra, .login-system-foot { display:none; }
}
@media (min-width: 769px) {
    .stApp section[data-testid="stMain"] .main .block-container { padding-left:clamp(24px, 3vw, 48px); padding-right:clamp(24px, 3vw, 48px); }
    .st-key-login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] { flex:1 1 0 !important; max-width:none !important; width:calc(50% - 18px) !important; }
}
@media (min-width: 769px) and (max-width: 1100px) {
    .st-key-login-shell { align-items:flex-start; margin-top:-72px; padding-top:34px; }
    .st-key-login-shell [data-testid="stColumn"] { padding:20px !important; }
    .st-key-login-shell [data-testid="stImage"] img { height:88px !important; width:88px !important; }
    .st-key-login-shell [data-testid="stColumn"] h2 { font-size:1.65rem; }
    .st-key-login-shell .login-card-copy { margin:4px 0 14px; }
    .st-key-login-shell .login-secure { margin-bottom:14px; }
    .login-description { font-size:.88rem; line-height:1.55; }
    .login-benefits { gap:10px 18px; margin-top:18px; }
    .login-system-foot { margin-top:22px; }
    .st-key-login-shell .login-card-foot { margin-top:16px; padding-top:12px; }
}
@media (max-width: 480px) {
    .st-key-login-shell { padding-top:48px; }
    .st-key-login-shell [data-testid="stColumn"] { padding:20px !important; }
    .login-brandline { font-size:.62rem; }
    .login-kicker { font-size:.62rem; margin:16px 0 14px; }
}
@media (max-width: 768px) {
    .app-shell.login-shell .main .block-container { align-items:flex-start; min-height:100dvh; padding:24px 16px 28px; }
    .app-shell.login-shell div[data-testid="stImage"] img { height:82px !important; width:82px !important; }
    .app-shell.login-shell [data-testid="stHorizontalBlock"] { display:flex; flex-direction:column; align-items:stretch; gap:18px; min-height:auto; }
    .app-shell.login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child,
    .app-shell.login-shell [data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:last-child { max-width:none; width:100%; }
    .login-institutional { padding:0 4px; text-align:center; }
    .login-institutional img { max-width:82px; }
    .login-brandline { margin-top:10px; font-size:.62rem; }
    .login-kicker { font-size:.62rem; margin:16px 0 14px; }
    .login-description { font-size:.83rem; line-height:1.55; margin:0 auto; max-width:350px; }
    .login-description-desktop { display:none; }
    .login-description-mobile { display:inline; }
    .login-benefits { gap:9px 12px; margin:20px auto 0; max-width:350px; text-align:left; }
    .login-benefit { font-size:.7rem; }
    .login-benefit-extra { display:none; }
    .login-system-foot { display:none; }
    .app-shell.login-shell [data-testid="stColumn"] { border-radius:14px; padding:24px !important; }
    .app-shell.login-shell [data-testid="stColumn"] h2 { font-size:1.75rem; }
}
</style>
""", unsafe_allow_html=True)


def money(value: object) -> str:
    return f"R$ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


DISPLAY_COLUMNS = {
    "id": "ID", "name": "Nome", "stock": "Estoque", "minimum": "Mínimo",
    "stock_quantity": "Estoque", "minimum_stock": "Estoque mínimo", "purchase_cost": "Custo de compra",
    "sale_price": "Preço de venda", "internal_code": "Código interno", "category_id": "Categoria",
    "transaction_type": "Tipo", "category": "Categoria", "description": "Descrição", "amount": "Valor",
    "payment_method": "Forma de pagamento", "status": "Situação", "transaction_date": "Data",
    "source_type": "Origem", "source_id": "ID da origem", "product_id": "ID do produto",
    "movement_type": "Tipo de movimentação", "quantity": "Quantidade", "previous_quantity": "Saldo anterior",
    "new_quantity": "Saldo novo", "unit_cost": "Custo unitário", "reason": "Motivo",
    "document_number": "Documento", "created_at": "Data e hora", "tipo": "Tipo",
    "produto_id": "ID do produto", "faturamento": "Faturamento", "cmv": "CMV", "lucro_bruto": "Lucro bruto",
    "pagamento": "Pagamento", "valor": "Valor", "origem": "Origem", "descricao": "Descrição",
}


def table(data: object) -> pd.DataFrame:
    return pd.DataFrame(data).rename(columns=DISPLAY_COLUMNS)


PAGE_META = {
    "Dashboard": ("Visão geral", "Acompanhe os principais indicadores da operação."),
    "Produtos": ("Produtos", "Cadastre, consulte e gerencie os produtos da loja."),
    "Categorias": ("Categorias", "Organize seu catálogo para encontrar tudo com rapidez."),
    "Estoque": ("Estoque", "Controle entradas, saldos e movimentações da operação."),
    "Vendas": ("Vendas", "Registre vendas e acompanhe a performance comercial."),
    "Financeiro": ("Financeiro", "Controle receitas, despesas e resultados."),
    "Relatórios": ("Relatórios", "Analise e exporte informações da operação."),
    "Importação": ("Importação de produtos", "Importe produtos em massa utilizando uma planilha CSV ou Excel."),
    "Usuários": ("Usuários", "Gerencie acessos, perfis e segurança da equipe."),
    "Auditoria": ("Auditoria", "Acompanhe acessos e operações relevantes realizadas no sistema."),
    "Configurações": ("Configurações", "Ajuste preferências e informações da empresa."),
}


def page_header(page: str) -> None:
    title, subtitle = PAGE_META.get(page, (page, ""))
    st.markdown(f'<div class="page-header"><div><p class="page-kicker">PUMPHOUSEUP / GESTÃO</p><h1 class="page-title">{title}</h1><p class="page-subtitle">{subtitle}</p></div></div>', unsafe_allow_html=True)


def empty_state(title: str, copy: str) -> None:
    st.markdown(f'<div class="empty-state"><p class="empty-state-title">{title}</p><p class="empty-state-copy">{copy}</p></div>', unsafe_allow_html=True)


@st.cache_data(ttl=10, show_spinner=False)
def branding() -> tuple[str, object]:
    company_name = "Pumphouseup Suplementos"
    image_source: object = LOCAL_LOGO
    try:
        data = call("GET", "/public/branding")
        company_name = data.get("company_name") or company_name
        if data.get("logo_available"):
            image_source = call("GET", "/public/logo", raw=True)
    except RuntimeError:
        pass
    return company_name, image_source


def login_screen() -> None:
    company_name, logo_source = branding()
    company_label = escape(company_name)
    st.markdown(f'<div class="system-ribbon"><span class="system-ribbon-brand">{company_label}</span><span class="system-ribbon-meta"><span class="system-ribbon-version">Versão {SYSTEM_VERSION}</span><span class="system-ribbon-author">Desenvolvido por Inova Prod</span></span></div>', unsafe_allow_html=True)
    institutional, access = st.columns([1.1, .9], gap="large")
    with institutional:
        if os.path.exists(LOCAL_LOGO) or isinstance(logo_source, bytes):
            st.image(logo_source, width=150)
        st.markdown(
            f'<p class="login-brandline">{company_label}</p>'
            f'<p class="login-kicker">SISTEMA DE GESTÃO {company_label}</p>'
            '<p class="login-description"><span class="login-description-desktop">Controle estoque, vendas, despesas, receitas e resultados financeiros em um único ambiente. Tenha uma visão completa da operação, acompanhe indicadores em tempo real e tome decisões com mais segurança.</span><span class="login-description-mobile">Controle estoque, vendas e resultados financeiros da Pumphouseup em um único ambiente.</span></p>'
            '<div class="login-benefits">'
            '<span class="login-benefit">Estoque sob controle</span>'
            '<span class="login-benefit">Gestão financeira integrada</span>'
            '<span class="login-benefit login-benefit-extra">Indicadores em tempo real</span>'
            '<span class="login-benefit login-benefit-extra">Dados centralizados e protegidos</span>'
            '</div>'
            ,
            unsafe_allow_html=True,
        )
    with access:
        st.markdown('<h2>Acesso administrativo</h2><p class="login-card-copy">Entre com suas credenciais para acessar o painel de gestão da Pumphouseup.</p><p class="login-secure">Ambiente seguro</p>', unsafe_allow_html=True)
        email = st.text_input("E-mail", placeholder="seu@email.com")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        if st.button("Entrar no sistema", type="primary", use_container_width=True):
            try:
                result = call("POST", "/auth/login", json={"email": email, "password": password})
                st.session_state.token = result["access_token"]
                st.session_state.pop("theme", None)
                st.rerun()
            except RuntimeError as error:
                st.error(str(error))
        st.markdown('<p class="login-card-foot">Acesso restrito ao administrador da Pumphouseup.</p>', unsafe_allow_html=True)


def metric(label: str, value: str) -> None:
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)


def dashboard(token: str) -> None:
    page_header("Dashboard")
    try:
        data = call("GET", "/dashboard", token)
    except RuntimeError as error:
        st.error(str(error)); return
    cols = st.columns(6)
    values = [("Faturamento", money(data["revenue"])), ("Lucro bruto", money(data["gross_profit"])), ("Resultado líquido", money(data["net_result"])), ("Despesas", money(data["expenses"])), ("Estoque", money(data["inventory_value"])), ("Estoque baixo", str(data["low_stock"]))]
    for col, (label, value) in zip(cols, values):
        with col: metric(label, value)
    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("Atalhos")
        if st.button("Nova venda", use_container_width=True): st.session_state.page = "Vendas"; st.rerun()
        if st.button("Nova entrada", use_container_width=True): st.session_state.page = "Estoque"; st.rerun()
        if st.button("Novo produto", use_container_width=True): st.session_state.page = "Produtos"; st.rerun()
        if st.button("Nova despesa", use_container_width=True): st.session_state.page = "Financeiro"; st.rerun()
    with right:
        st.subheader("Alertas de estoque")
        if data["low_stock_products"]:
            st.dataframe(table(data["low_stock_products"]), use_container_width=True, hide_index=True)
        else: st.success("Nenhum produto no estoque mínimo.")


def products(token: str) -> None:
    page_header("Produtos")
    categories_data = call("GET", "/categories", token)
    category_options = {"Sem categoria": None}
    category_options.update({f'{item["id"]} · {item["name"]}': item["id"] for item in categories_data})
    with st.expander("Cadastrar produto", expanded=True):
        with st.form("product"):
            code, name, category = st.columns(3)
            internal_code = code.text_input("Código interno *")
            product_name = name.text_input("Nome *")
            category_choice = category.selectbox("Categoria", list(category_options))
            category_id = category_options[category_choice]
            cost, price, margin = st.columns(3)
            purchase_cost = cost.number_input("Custo de compra", min_value=0.0, format="%.2f")
            sale_price = price.number_input("Preço de venda", min_value=0.0, format="%.2f")
            desired_margin = margin.number_input("Margem desejada (%)", min_value=0.0, max_value=99.0, format="%.2f")
            minimum_stock = st.number_input("Estoque mínimo", min_value=0.0, format="%.3f")
            if st.form_submit_button("Salvar produto", type="primary"):
                try:
                    call("POST", "/products", token, json={"internal_code": internal_code, "name": product_name, "category_id": category_id, "purchase_cost": purchase_cost, "sale_price": sale_price, "desired_margin": desired_margin / 100, "minimum_stock": minimum_stock})
                    st.success("Produto cadastrado."); st.rerun()
                except RuntimeError as error: st.error(str(error))
    data = call("GET", "/products", token)
    if data: st.dataframe(table(data), use_container_width=True, hide_index=True)
    else: empty_state("Nenhum produto cadastrado", "Cadastre um produto para começar a controlar seu catálogo.")


def categories(token: str) -> None:
    page_header("Categorias")
    with st.form("category"):
        name = st.text_input("Nome da categoria")
        if st.form_submit_button("Salvar categoria", type="primary"):
            try:
                call("POST", "/categories", token, json={"name": name})
                st.success("Categoria salva."); st.rerun()
            except RuntimeError as error: st.error(str(error))
    data = call("GET", "/categories", token)
    if data: st.dataframe(table(data), use_container_width=True, hide_index=True)
    else: empty_state("Nenhuma categoria cadastrada", "Crie categorias para organizar os produtos da Pumphouseup.")


def stock(token: str) -> None:
    page_header("Estoque")
    products_data = call("GET", "/products", token)
    if not products_data:
        empty_state("Seu estoque ainda está vazio", "Cadastre um produto e registre uma entrada para começar.")
        return
    options = {f'{item["id"]} · {item["name"]}': item["id"] for item in products_data}
    with st.form("entry"):
        selected = st.selectbox("Produto", list(options))
        quantity = st.number_input("Quantidade", min_value=0.001, format="%.3f")
        unit_cost = st.number_input("Custo unitário", min_value=0.0, format="%.2f")
        reason = st.text_input("Observação")
        if st.form_submit_button("Registrar entrada", type="primary"):
            try:
                call("POST", "/stock/entries", token, json={"product_id": options[selected], "quantity": quantity, "unit_cost": unit_cost, "reason": reason})
                st.success("Entrada registrada e estoque atualizado."); st.rerun()
            except RuntimeError as error: st.error(str(error))
    st.dataframe(table(pd.DataFrame(products_data)[["id", "name", "stock_quantity", "minimum_stock", "purchase_cost"]]), use_container_width=True, hide_index=True)
    with st.expander("Ajuste manual", expanded=False):
        with st.form("adjustment"):
            selected_adjustment = st.selectbox("Produto para ajuste", list(options), key="adjustment_product")
            adjustment_type = st.selectbox("Tipo", ["increase", "decrease", "set"], format_func=lambda value: {"increase": "Entrada de ajuste", "decrease": "Saída de ajuste", "set": "Definir saldo"}[value])
            adjustment_quantity = st.number_input("Quantidade/saldo", min_value=0.0, format="%.3f")
            adjustment_reason = st.text_input("Justificativa obrigatória")
            if st.form_submit_button("Registrar ajuste"):
                try:
                    call("POST", "/stock/adjustments", token, json={"product_id": options[selected_adjustment], "adjustment_type": adjustment_type, "quantity": adjustment_quantity, "reason": adjustment_reason})
                    st.success("Ajuste registrado."); st.rerun()
                except RuntimeError as error: st.error(str(error))
    st.subheader("Histórico de movimentações")
    movements = call("GET", "/stock/movements", token)
    if movements: st.dataframe(table(movements), use_container_width=True, hide_index=True)


def sales(token: str) -> None:
    page_header("Vendas")
    products_data = call("GET", "/products", token)
    if not products_data:
        empty_state("Não há produtos disponíveis para venda", "Cadastre um produto e registre uma entrada antes de vender.")
        return
    options = {f'{item["id"]} · {item["name"]} (saldo {item["stock_quantity"]})': item for item in products_data}
    with st.form("sale"):
        selected = st.selectbox("Produto", list(options))
        quantity = st.number_input("Quantidade", min_value=0.001, format="%.3f")
        price = st.number_input("Preço praticado (0 usa o cadastro)", min_value=0.0, format="%.2f")
        payment = st.selectbox("Forma de pagamento", ["pix", "dinheiro", "cartao", "transferencia"], format_func=lambda value: {"pix": "Pix", "dinheiro": "Dinheiro", "cartao": "Cartão", "transferencia": "Transferência"}[value])
        if st.form_submit_button("Concluir venda", type="primary"):
            product = options[selected]
            try:
                result = call("POST", "/sales", token, json={"items": [{"product_id": product["id"], "quantity": quantity, "unit_price": price or None}], "payment_method": payment})
                st.success(f'Venda #{result["id"]} concluída. Lucro bruto: {money(result["gross_profit"])}')
            except RuntimeError as error: st.error(str(error))


def finance(token: str) -> None:
    page_header("Financeiro")
    with st.form("finance"):
        kind = st.selectbox("Tipo", ["expense", "income"], format_func=lambda value: "Despesa" if value == "expense" else "Receita")
        category = st.text_input("Categoria")
        description = st.text_input("Descrição")
        amount = st.number_input("Valor", min_value=0.01, format="%.2f")
        if st.form_submit_button("Registrar lançamento", type="primary"):
            try:
                call("POST", "/finance", token, json={"transaction_type": kind, "category": category, "description": description, "amount": amount})
                st.success("Lançamento registrado.")
            except RuntimeError as error: st.error(str(error))
    transactions = call("GET", "/finance", token)
    if transactions: st.dataframe(table(transactions), use_container_width=True, hide_index=True)
    else: empty_state("Nenhuma movimentação financeira", "Registre uma receita ou despesa para acompanhar o resultado.")


def reports(token: str) -> None:
    page_header("Relatórios")
    report_labels = {"stock": "Posição de estoque", "low_stock": "Estoque baixo", "movements": "Movimentações", "sales": "Vendas por período", "revenue": "Faturamento", "profit": "Lucro", "income": "Receitas", "expenses": "Despesas", "financial": "Resultado financeiro", "top_products": "Produtos mais vendidos"}
    report_type = st.selectbox("Relatório", list(report_labels), format_func=lambda value: report_labels[value])
    data = call("GET", f"/reports/{report_type}", token)
    if data: st.dataframe(table(data), use_container_width=True, hide_index=True)
    else: st.info("Nenhum dado para os filtros atuais.")
    cols = st.columns(3)
    for col, file_format, label in zip(cols, ["xlsx", "csv", "pdf"], ["Excel", "CSV", "PDF"]):
        response = call("GET", f"/reports/{report_type}/export/{file_format}", token, raw=True)
        with col: st.download_button(f"Baixar {label}", response, file_name=f"pumphouseup-{report_type}.{file_format}")


def imports(token: str) -> None:
    page_header("Importação")
    st.download_button("Baixar template Excel", call("GET", "/imports/template", token, raw=True), file_name="template-produtos.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    uploaded = st.file_uploader("Envie um arquivo CSV ou Excel", type=["csv", "xlsx"], label_visibility="visible")
    if uploaded:
        if "import_preview" not in st.session_state or st.session_state.get("import_name") != uploaded.name:
            preview = call("POST", "/imports/preview", token, files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)})
            st.session_state.import_preview = preview; st.session_state.import_name = uploaded.name
        preview = st.session_state.import_preview
        st.write(f"Linhas: {preview['total']} | Válidas: {preview['valid']}")
        st.dataframe(table(preview["preview"]), use_container_width=True, hide_index=True)
        if preview["errors"]: st.error(table(preview["errors"]))
        elif st.button("Confirmar importação", type="primary"):
            result = call("POST", "/imports/products", token, files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)})
            st.success(f"{result['imported']} produtos importados."); st.session_state.pop("import_preview", None)


def settings_page(token: str) -> None:
    page_header("Configurações")
    current = call("GET", "/settings", token)
    with st.form("settings"):
        company = st.text_input("Nome da empresa", value=current.get("company_name", "Pumphouseup Suplementos"))
        backup = st.text_input("Orientações de backup", value=current.get("backup_info", "Backup local configurado"))
        if st.form_submit_button("Salvar configurações", type="primary"):
            call("PUT", "/settings", token, json={"company_name": company, "backup_info": backup})
            st.success("Configurações salvas.")
    st.subheader("Identidade da empresa")
    st.caption("Envie uma imagem PNG, JPG ou WEBP. Ela será exibida em formato circular no login e na navegação.")
    logo_upload = st.file_uploader("Logo da empresa", type=["png", "jpg", "jpeg", "webp"], key="company_logo_upload")
    if logo_upload and st.button("Atualizar logo", type="primary"):
        try:
            call("POST", "/settings/logo", token, files={"file": (logo_upload.name, logo_upload.getvalue(), logo_upload.type)})
            branding.clear()
            st.success("Logo atualizada com sucesso.")
            st.rerun()
        except RuntimeError as error:
            st.error(str(error))


def profile_page(token: str, user: dict) -> None:
    page_header("Meu perfil")
    with st.form("profile"):
        name = st.text_input("Nome completo", value=user.get("full_name") or "")
        email = st.text_input("E-mail", value=user.get("email", ""), disabled=True)
        phone = st.text_input("Telefone", value=user.get("phone") or "")
        job_title = st.text_input("Cargo / função", value=user.get("job_title") or "")
        if st.form_submit_button("Salvar perfil", type="primary"):
            try:
                call("PATCH", "/auth/profile", token, json={"full_name": name, "phone": phone, "job_title": job_title})
                st.success("Perfil atualizado com sucesso.")
            except RuntimeError as error:
                st.error(str(error))
    st.divider()
    st.subheader("Segurança")
    st.caption("Atualize sua senha periodicamente para manter o acesso protegido.")
    with st.form("change_password_profile"):
        current = st.text_input("Senha atual", type="password", key="profile_current_password")
        new = st.text_input("Nova senha", type="password", key="profile_new_password", help="Use no mínimo 8 caracteres.")
        confirm = st.text_input("Confirmar nova senha", type="password", key="profile_confirm_password")
        if st.form_submit_button("Alterar minha senha", type="primary"):
            try:
                call("POST", "/auth/change-password", token, json={"current_password": current, "new_password": new, "confirm_password": confirm})
                st.success("Senha alterada com sucesso.")
            except RuntimeError as error:
                st.error(str(error))


def audit_page(token: str) -> None:
    page_header("Auditoria")
    logs = call("GET", "/audit-logs", token)
    if logs:
        audit_data = pd.DataFrame(logs).rename(columns={"action": "Ação", "description": "Descrição", "result": "Resultado", "created_at": "Data e hora", "user_id": "Usuário"})
        st.dataframe(audit_data[["Data e hora", "Ação", "Usuário", "Resultado", "Descrição"]], use_container_width=True, hide_index=True)
    else:
        empty_state("Nenhum registro de auditoria", "Os acessos e operações relevantes aparecerão aqui.")


def users_page(token: str) -> None:
    page_header("Usuários")
    with st.expander("Novo usuário", expanded=False):
        with st.form("user"):
            full_name = st.text_input("Nome completo")
            email = st.text_input("E-mail do usuário")
            phone = st.text_input("Telefone")
            job_title = st.text_input("Cargo / função")
            role = st.selectbox("Perfil de acesso", ["operator", "admin"], format_func=lambda value: "Operador" if value == "operator" else "Administrador")
            password = st.text_input("Senha temporária", type="password")
            confirm = st.text_input("Confirmar senha temporária", type="password")
            if st.form_submit_button("Criar usuário", type="primary"):
                if password != confirm:
                    st.error("A confirmação da senha não confere.")
                else:
                    try:
                        call("POST", "/users", token, json={"email": email, "password": password, "full_name": full_name, "phone": phone, "job_title": job_title, "role": role, "must_change_password": True})
                        st.success("Usuário criado com sucesso.")
                        st.rerun()
                    except RuntimeError as error:
                        st.error(str(error))
    data = call("GET", "/users", token)
    if data:
        users_data = pd.DataFrame(data)
        users_data["Perfil"] = users_data.apply(lambda row: "Administrador" if row["is_admin"] else "Operador", axis=1)
        users_data["Status"] = users_data["is_active"].map({True: "Ativo", False: "Inativo"})
        users_data["Nome"] = users_data["full_name"].fillna("Sem nome")
        st.dataframe(users_data[["Nome", "email", "job_title", "Perfil", "Status", "created_at", "last_login_at"]].rename(columns={"email": "E-mail", "job_title": "Cargo", "created_at": "Criado em", "last_login_at": "Último acesso"}), use_container_width=True, hide_index=True)
    else:
        empty_state("Nenhum usuário cadastrado", "Crie um acesso para sua equipe operar o sistema.")


if "token" not in st.session_state:
    with st.container(key="login-shell"):
        login_screen()
else:
    try:
        current_user = call("GET", "/auth/me", st.session_state.token)
    except RuntimeError:
        del st.session_state.token
        st.rerun()
    company_name, logo_source = branding()
    theme = st.session_state.get("theme", current_user.get("theme_preference", "dark"))
    st.markdown(f'<div class="theme-marker theme-{theme}-marker"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="system-ribbon"><span class="system-ribbon-brand">{escape(company_name)}</span><span class="system-ribbon-meta"><span class="system-ribbon-version">Versão {SYSTEM_VERSION}</span><span class="system-ribbon-author">Desenvolvido por Inova Prod</span></span></div>', unsafe_allow_html=True)
    must_change = current_user.get("must_change_password", False)
    if must_change:
        st.session_state.page = "Meu perfil"
        st.warning("Defina uma nova senha para continuar.")
    with st.sidebar:
        if os.path.exists(LOCAL_LOGO) or isinstance(logo_source, bytes): st.image(logo_source, use_container_width=True)
        st.caption(company_name)
        st.caption("Gestão de estoque e resultado")
        pages = ["Meu perfil"] if must_change else ["Dashboard", "Produtos", "Categorias", "Estoque", "Vendas", "Financeiro", "Relatórios", "Importação"]
        if current_user["is_admin"]:
            pages.extend(["Usuários", "Auditoria", "Configurações"])
        if not must_change:
            pages.append("Meu perfil")
        page = st.radio("Navegação", pages, index=pages.index(st.session_state.get("page", "Dashboard")))
        st.session_state.page = page
        if st.button("Sair", use_container_width=True):
            try: call("POST", "/auth/logout", st.session_state.token)
            except RuntimeError: pass
            st.session_state.pop("theme", None)
            del st.session_state.token; st.rerun()
    current_page = st.session_state.get("page", "Dashboard")
    next_theme = "light" if theme == "dark" else "dark"
    theme_icon = "☀" if theme == "dark" else "☾"
    theme_help = "Ativar tema claro" if theme == "dark" else "Ativar tema escuro"
    top_left, top_right = st.columns([1, .22])
    with top_left:
        st.markdown(f'<div class="topbar"><span class="topbar-context">{PAGE_META.get(current_page, (current_page, ""))[1]}</span><span class="topbar-user">{current_user.get("full_name") or current_user.get("email", "Usuário")} · {"Administrador" if current_user.get("is_admin") else "Operador"}</span></div>', unsafe_allow_html=True)
    with top_right:
        st.markdown('<div class="theme-toggle">', unsafe_allow_html=True)
        if st.button(theme_icon, help=theme_help, key="theme_toggle"):
            updated = call("PUT", "/auth/preferences", st.session_state.token, json={"theme": next_theme})
            st.session_state.theme = updated["theme_preference"]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    try:
        pages_map = {"Dashboard": dashboard, "Produtos": products, "Categorias": categories, "Estoque": stock, "Vendas": sales, "Financeiro": finance, "Relatórios": reports, "Importação": imports, "Configurações": settings_page, "Usuários": users_page, "Auditoria": audit_page}
        if st.session_state.page == "Meu perfil": profile_page(st.session_state.token, current_user)
        else: pages_map[st.session_state.page](st.session_state.token)
    except RuntimeError as error:
        st.error(str(error))
