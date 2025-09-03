import streamlit as st
from fetcher import get_upcoming_launches

# Page setup
st.set_page_config(page_title="🚀 Space Launch Tracker", layout="wide")
st.title("🚀 Space Launch Tracker")

# --- CSS for cards + badges ---
st.markdown("""
<style>
.card{padding:1rem;border:1px solid #ececec;border-radius:14px;
      box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:1rem;background:#fff}
.title{font-weight:700;font-size:1.1rem;margin-bottom:.4rem}
.badge{display:inline-block;padding:.2rem .6rem;border-radius:999px;
       font-size:.8rem;font-weight:700;border:1px solid transparent}
.badge-green{background:#e9f7ec;color:#1b5e20;border-color:#cfead7}
.badge-red{background:#fdecea;color:#b71c1c;border-color:#f5c6c3}
.badge-yellow{background:#fff8e1;color:#8d6e00;border-color:#ffe0a3}
</style>
""", unsafe_allow_html=True)

def badge_html(status: str) -> str:
    """Return a colored badge based on status text."""
    text = (status or "Unknown").strip()
    s = text.lower()
    cls = "badge badge-yellow"
    if "success" in s or "go" in s:
        cls = "badge badge-green"
    elif "fail" in s or "abort" in s or "scrub" in s or "hold" in s:
        cls = "badge badge-red"
    return f'<span class="{cls}">{text}</span>'

# --- Controls ---
top_left, _ = st.columns([1, 5])
with top_left:
    if st.button("🔄 Refresh"):
        st.rerun()

limit = st.slider("How many upcoming launches to show?", 1, 20, 6)
search = st.text_input("🔍 Search by mission name or provider:")

# Auto-refresh every 10 seconds
# st.autorefresh(interval=10 * 1000, key="launch_autorefresh")

# --- Data ---
launches = get_upcoming_launches(limit)

# --- Apply search filter ---
if search:
    launches = [
        l for l in launches
        if search.lower() in (l.get("name") or "").lower()
        or search.lower() in (l.get("provider") or "").lower()
    ]

# --- Render ---
if not launches:
    st.warning("⚠️ Could not fetch launch data. Try again later.")
else:
    cols = st.columns(2)  # two-column grid
    for i, launch in enumerate(launches):
        name = launch.get("name") or "Unnamed"
        status = launch.get("status") or "Unknown"
        provider = launch.get("provider") or "—"
        pad = launch.get("pad") or "—"
        location = launch.get("location") or "—"
        net = launch.get("net") or "—"

        badge = badge_html(status)
        card_html = f"""
<div class="card">
  <div class="title">🚀 {name}</div>
  <div style="margin-bottom:.5rem">{badge}</div>
  <div>🛰️ <b>Provider:</b> {provider}</div>
  <div>📍 <b>Pad:</b> {pad}</div>
  <div>🌍 <b>Location:</b> {location}</div>
  <div>⏰ <b>Launch (UTC):</b> {net}</div>
</div>
"""
        with cols[i % 2]:
            st.markdown(card_html, unsafe_allow_html=True)