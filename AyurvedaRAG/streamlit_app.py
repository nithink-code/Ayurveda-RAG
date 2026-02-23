import asyncio
from pathlib import Path
import time
import os
import uuid as _uuid

import streamlit as st
import inngest
from dotenv import load_dotenv
import requests

import json
from pathlib import Path

load_dotenv(override=True)

# ──────────────────────────────────────────────
#  Persistence Helpers
# ──────────────────────────────────────────────
SESSION_DIR = Path(__file__).parent / "sessions"
SESSION_DIR.mkdir(exist_ok=True)

def save_user_session(user_id: str, data: dict):
    session_file = SESSION_DIR / f"{user_id}.json"
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_user_session(user_id: str) -> dict:
    session_file = SESSION_DIR / f"{user_id}.json"
    if session_file.exists():
        with open(session_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# ──────────────────────────────────────────────
#  Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AyurvedaRAG — Personalized Treatment Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
#  Load Custom CSS
# ──────────────────────────────────────────────
def local_css(file_name):
    css_file = Path(__file__).parent / file_name
    with open(css_file, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# ──────────────────────────────────────────────
#  Inngest Helpers
# ──────────────────────────────────────────────
def get_inngest_client() -> inngest.Inngest:
    return inngest.Inngest(
        app_id="study-rag",
        is_production=os.getenv("INNGEST_DEV", "false").lower() != "true",
        signing_key=os.getenv("INNGEST_SIGNING_KEY"),
        event_key=os.getenv("INNGEST_EVENT_KEY"),
    )

async def _send_event(name: str, data: dict) -> str:
    client = get_inngest_client()
    result = await client.send(inngest.Event(name=name, data=data))
    return result[0]

def _inngest_api_base() -> str:
    # Use local dev server only if INNGEST_DEV is explicitly set to "true"
    if os.getenv("INNGEST_DEV", "false").lower() == "true":
        return "http://localhost:8288/v1"
    return os.getenv("INNGEST_API_BASE", "https://api.inngest.com/v1")

def fetch_runs(event_id: str) -> list[dict]:
    url = f"{_inngest_api_base()}/events/{event_id}/runs"
    headers = {}
    signing_key = os.getenv("INNGEST_SIGNING_KEY")
    if signing_key:
        headers["Authorization"] = f"Bearer {signing_key}"
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except Exception:
        return []

def wait_for_run_output(event_id: str, timeout_s: float = 60.0, poll_interval_s: float = 0.5) -> dict:
    """Fast polling for quick feedback."""
    start = time.time()
    last_status = None
    while True:
        runs = fetch_runs(event_id)
        if runs:
            run = runs[0]
            status = run.get("status")
            last_status = status or last_status
            if status in ("Completed", "Succeeded", "Success", "Finished"):
                return run.get("output") or {}
            if status in ("Failed", "Cancelled"):
                raise RuntimeError(f"Function run {status}")
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Timed out waiting for output (last status: {last_status})")
        time.sleep(poll_interval_s)

# ──────────────────────────────────────────────
#  Ayurvedic Helpers
# ──────────────────────────────────────────────
SUPPORTED_CONDITIONS = {
    "Diabetes": "🍬 Diabetes (Madhumeha)",
    "Acidity": "🔥 Acidity (Amlapitta)",
    "Thyroid": "🦋 Thyroid (Galaganda)",
    "Anxiety": "🧘 Anxiety (Chittodvega)",
    "Custom": "➕ Add Custom Condition...",
}

DOSHA_INFO = {
    "Diabetes": ("Kapha", "#059669", "green"),
    "Acidity": ("Pitta", "#dc2626", "red"),
    "Thyroid": ("Kapha-Vata", "#7c3aed", "purple"),
    "Anxiety": ("Vata", "#2563eb", "blue"),
}

def trigger_ayurveda_plan(condition: str, user_id: str) -> str:
    return asyncio.run(_send_event("ayurveda/generate-plan", {
        "condition": condition,
        "user_id": user_id,
    }))

def trigger_seed_kb(force: bool = False) -> str:
    return asyncio.run(_send_event("ayurveda/seed-kb", {"force": force}))

def trigger_log_progress(user_id: str, condition: str, week: int, progress: dict) -> str:
    return asyncio.run(_send_event("ayurveda/log-progress", {
        "user_id": user_id,
        "condition": condition,
        "week": week,
        **progress,
    }))


# ──────────────────────────────────────────────
#  PDF Export Helper (fpdf2)
# ──────────────────────────────────────────────
def st_pdf_download(condition: str, plan_text: str):
    """Generates a premium server-side PDF for better reliability and encoding."""
    from fpdf import FPDF
    import io
    import re

    # Clean text for standard PDF fonts (Latin-1)
    # Replace common Unicode characters with Latin-1 equivalents to avoid encoding errors
    def clean_for_pdf(text):
        replacements = {
            '\u2013': '-', '\u2014': '-', 
            '\u2018': "'", '\u2019': "'", 
            '\u201c': '"', '\u201d': '"', 
            '\u2022': '*', '\u2026': '...',
            '\u2122': '(TM)', '\u00ae': '(R)', '\u00a9': '(C)'
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        # Remove any other non-latin-1 characters
        return text.encode('latin-1', 'replace').decode('latin-1')

    class AyurvedaPDF(FPDF):
        def header(self):
            # Banner background (dark green matching the theme)
            self.set_fill_color(27, 67, 50) 
            self.rect(0, 0, 210, 40, 'F')
            
            # Logo/Icon area (Subtle circle)
            self.set_fill_color(45, 106, 79)
            self.ellipse(10, 10, 20, 20, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('helvetica', 'B', 15)
            self.set_xy(10, 10)
            self.cell(20, 20, 'A-R', align='C')
            
            self.set_y(12)
            self.set_x(35)
            self.set_font('helvetica', 'B', 22)
            self.cell(0, 10, 'Ayurvedic Intelligence Report', ln=True)
            
            self.set_x(35)
            self.set_font('helvetica', '', 10)
            self.set_text_color(200, 200, 200)
            self.cell(0, 5, f'Personalized Treatment Strategy for: {condition}', ln=True)
            self.ln(20)

        def footer(self):
            self.set_y(-15)
            self.set_font('helvetica', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f'Page {self.page_no()} | Confidential | Generated by AyurvedaRAG Intelligence', align='C')

    pdf = AyurvedaPDF()
    pdf.set_margins(20, 20, 20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Body Styling
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("helvetica", size=11)
    
    lines = plan_text.split('\n')
    for line in lines:
        val = line.strip()
        if not val:
            pdf.ln(5)
            continue
            
        # Detect Headers (Markdown style)
        if val.startswith('#') or (val.startswith('**') and val.endswith('**') and len(val) < 64):
            h_txt = clean_for_pdf(val.replace('#', '').replace('*', '').strip())
            pdf.ln(4)
            pdf.set_font("helvetica", 'B', 13)
            pdf.set_text_color(27, 67, 50)
            pdf.cell(0, 10, h_txt, ln=True)
            
            # Sub-separator line
            curr_y = pdf.get_y()
            pdf.set_draw_color(45, 106, 79)
            pdf.set_line_width(0.4)
            pdf.line(20, curr_y - 1, 80, curr_y - 1)
            pdf.ln(3)
            
            pdf.set_font("helvetica", '', 11)
            pdf.set_text_color(40, 40, 40)
        else:
            # Bullet point detection
            if val.startswith('- ') or val.startswith('* ') or (len(val) > 2 and val[0].isdigit() and val[1] == '.'):
                old_margin = pdf.l_margin
                pdf.set_left_margin(25)
                # If it was a dash/star bullet, use a dot
                prefix = "• " if val.startswith(('- ', '* ')) else ""
                content = val[2:].strip() if val.startswith(('- ', '* ')) else val
                b_txt = clean_for_pdf(f"{prefix}{content}")
                pdf.multi_cell(0, 7, b_txt)
                pdf.set_left_margin(old_margin)
            else:
                b_txt = clean_for_pdf(val)
                pdf.multi_cell(0, 7, b_txt)
            pdf.ln(1)

    # Generate Bytes
    try:
        # fpdf2 output() returns bytes if no name is provided
        pdf_output = pdf.output()
        if isinstance(pdf_output, bytearray):
            pdf_output = bytes(pdf_output)
    except Exception as e:
        # Fallback
        pdf_output = b"Error generating PDF content: " + str(e).encode('ascii', 'ignore')

    st.download_button(
        label="📥 Download Premium PDF Report",
        data=pdf_output,
        file_name=f"Ayurveda_Report_{condition.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True,
        key=f"pdf_download_{condition}_{hash(plan_text)}" # Dynamic key to avoid Streamlit state issues
    )



# ══════════════════════════════════════════════
#  TAB: Treatment Planner
# ══════════════════════════════════════════════
def tab_ayurveda():
    st.markdown("""
    <div class="ayur-hero">
        <div class="ayur-hero-icon">🌿</div>
        <h2 class="ayur-hero-title">Instant Ayurvedic Treatment Insights</h2>
        <p class="ayur-hero-sub">Select your condition to generate a personalized treatment plan in seconds</p>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_side = st.columns([3, 2], gap="large")

    with col_main:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🩺 Condition Selection")

        condition_label = st.selectbox(
            "Select Condition",
            list(SUPPORTED_CONDITIONS.values()),
            label_visibility="collapsed",
        )
        
        # Determine the internal key
        condition_key = next(k for k, v in SUPPORTED_CONDITIONS.items() if v == condition_label)
        
        # Show text input if "Custom" is selected
        final_condition = condition_key
        if condition_key == "Custom":
            st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
            search_col1, search_col2 = st.columns([4, 1])
            with search_col1:
                custom_text = st.text_input("Describe your condition/symptoms", placeholder="e.g. Migraine, Insomnia, Joint Pain...", label_visibility="collapsed")
            with search_col2:
                search_btn = st.button("🔍 Search", use_container_width=True)
            
            if custom_text:
                final_condition = custom_text
            else:
                final_condition = "Custom Condition"
            
            # Use the search button as a trigger for generation if it's visible
            if search_btn:
                gen_btn = True
        else:
            final_condition = condition_key

        if "user_id" not in st.session_state:
            # Fallback if main() hasn't run or for some context
            st.session_state["user_id"] = st.query_params.get("uid", str(_uuid.uuid4())[:8])
        user_id = st.session_state["user_id"]

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        if condition_key in DOSHA_INFO:
            dosha, color, _ = DOSHA_INFO[condition_key]
            st.markdown(f"""
            <div class="dosha-badge" style="border-color:{color}40;background:{color}15;">
                <span class="dosha-label">Primary Dosha Balance:</span>
                <span class="dosha-value" style="color:{color}">{dosha}</span>
            </div>
            """, unsafe_allow_html=True)
        elif condition_key == "Custom" and final_condition != "Custom Condition":
             st.markdown(f"""
            <div class="dosha-badge" style="border-color:var(--gold)40;background:rgba(212,168,90,0.1);">
                <span class="dosha-label">Analysis Type:</span>
                <span class="dosha-value" style="color:var(--gold)">Dynamic Custom Report</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

        gen_col, clr_col, seed_col = st.columns([3, 1, 1])
        with gen_col:
            gen_btn = st.button("🌿 Generate Instant Plan", use_container_width=True, type="primary")
        with clr_col:
            clr_btn = st.button("🗑️ Clear", use_container_width=True, help="Clear current display")
        with seed_col:
            seed_btn = st.button("🌱 Seed", use_container_width=True, help="Update knowledge base")

        if clr_btn:
            # Re-initialize current state for planner (clears display)
            if "current_plan" in st.session_state:
                del st.session_state["current_plan"]
            if "current_condition" in st.session_state:
                del st.session_state["current_condition"]
            
            # Update persisted disk state to reflect no 'current' plan while keeping history
            save_user_session(user_id, {
                "plan_history": st.session_state.get("plan_history", {}),
                "current_plan": "",
                "current_condition": ""
            })
            st.rerun()

        if seed_btn:
            with st.spinner("Updating KB..."):
                try:
                    ev_id = trigger_seed_kb()
                    wait_for_run_output(ev_id, timeout_s=60)
                    st.success("✅ Knowledge base updated!")
                except Exception as e:
                    st.error(f"Update failed: {e}")

        if gen_btn:
            if condition_key == "Custom" and final_condition == "Custom Condition":
                st.warning("Please describe your condition first.")
            else:
                with st.status(f"🛠️ Analyzing {final_condition}...", expanded=False) as status:
                    try:
                        ev_id = trigger_ayurveda_plan(final_condition, user_id)
                        output = wait_for_run_output(ev_id, timeout_s=45)
                        plan = output.get("plan", "")
                        if plan:
                            # Store in history
                            if "plan_history" not in st.session_state:
                                st.session_state["plan_history"] = {}
                            st.session_state["plan_history"][final_condition] = plan
                            
                            st.session_state["current_plan"] = plan
                            st.session_state["current_condition"] = final_condition
    
                            # --- PERSIST TO DISK ---
                            save_user_session(user_id, {
                                "plan_history": st.session_state["plan_history"],
                                "current_plan": plan,
                                "current_condition": final_condition
                            })
                            
                            status.update(label="✅ Ready!", state="complete")
                            st.rerun()
                    except Exception as e:
                        status.update(label="❌ Generation failed", state="error")
                        st.error(f"Error: {e}")

        if "current_plan" in st.session_state and st.session_state.get("current_condition") == final_condition:
            plan = st.session_state["current_plan"]
            cond = st.session_state["current_condition"]

            st.markdown(f"""
            <div class="plan-header">
                <span class="plan-badge">🌿 Your Personalized Plan</span>
                <h3 class="plan-condition">{cond}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Quick display of plan sections
            sections = []
            current_section = []
            current_title = "Overview"
            for line in plan.split("\n"):
                if line.startswith("##") or (line.startswith("**") and line.strip().endswith("**") and any(f"{i}." in line for i in range(1, 9))):
                    if current_section:
                        sections.append((current_title, "\n".join(current_section)))
                    current_title = line.lstrip("#").strip().lstrip("*").rstrip("*").strip()
                    current_section = []
                else:
                    current_section.append(line)
            if current_section:
                sections.append((current_title, "\n".join(current_section)))

            for title, content in sections:
                with st.expander(f"📌 {title}", expanded=True):
                    st.markdown(content)

            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button("📄 Download Text", plan.encode("utf-8"), f"plan_{cond.lower()}.txt", use_container_width=True)
            with dl2:
                st_pdf_download(cond, plan)

    with col_side:
        st.markdown("""
        <div class="glass-card">
            <h4 style="margin-top:0;color:#d4a85a;">☯️ Dosha Guide</h4>
            <div class="dosha-ref">
                <div class="dosha-item vata"><div class="dosha-name">🌬️ Vata</div><div class="dosha-desc">Air + Space</div></div>
                <div class="dosha-item pitta"><div class="dosha-name">🔥 Pitta</div><div class="dosha-desc">Fire + Water</div></div>
                <div class="dosha-item kapha"><div class="dosha-name">🌊 Kapha</div><div class="dosha-desc">Earth + Water</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        st.markdown('<div class="disclaimer-card"><strong>⚕️ Disclaimer</strong><br>For educational use only. Consult a doctor before starting treatment.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  TAB: Progress Dashboard
# ══════════════════════════════════════════════
def tab_progress():
    st.markdown("""
    <div class="ayur-hero" style="background:linear-gradient(135deg,#0a1a12,#1b4332,#0a1a12);">
        <div class="ayur-hero-icon">�</div>
        <h2 class="ayur-hero-title">Your Treatment History</h2>
        <p class="ayur-hero-sub">Review and download your recently generated intelligence reports</p>
    </div>
    """, unsafe_allow_html=True)

    history = st.session_state.get("plan_history", {})

    if not history:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 60px;">
            <div style="font-size: 48px; margin-bottom: 20px;">📜</div>
            <h3 style="color: var(--gold);">No reports found yet</h3>
            <p style="color: var(--text-secondary);">Go to the <b>Treatment Planner</b> to generate your first personalized Ayurvedic plan.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("### � Recently Generated Plans")
    
    # Display history items in a grid or list
    for condition, plan in reversed(list(history.items())):
        with st.container():
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid var(--green-light);">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <span class="plan-badge">Intelligence Report</span>
                        <h4 style="margin: 4px 0; color: var(--gold);">{condition}</h4>
                        <p style="font-size: 13px; color: var(--text-muted); margin-top: 8px;">
                            Generated in this session. Full personalized protocol ready for review.
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Action buttons side by side
            btn_col1, btn_col2 = st.columns([3, 1])
            with btn_col1:
                if st.button(f"👁️ View Plan: {condition}", key=f"view_{condition}", use_container_width=True):
                    st.session_state["current_plan"] = plan
                    st.session_state["current_condition"] = condition
                    st.session_state["active_tab"] = "ayurveda"
                    st.rerun()
            with btn_col2:
                st_pdf_download(condition, plan)
            
            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  Main Layout
# ══════════════════════════════════════════════
def main():
    # ── Initialize Session & Persistence ──
    if "uid" in st.query_params:
        user_id = st.query_params["uid"]
        st.session_state["user_id"] = user_id
        
        # Load data from disk if not already in session_state
        if "plan_history" not in st.session_state:
            data = load_user_session(user_id)
            if data:
                st.session_state["plan_history"] = data.get("plan_history", {})
                st.session_state["current_plan"] = data.get("current_plan", "")
                st.session_state["current_condition"] = data.get("current_condition", "")
    else:
        # New session
        user_id = str(_uuid.uuid4())[:8]
        st.query_params["uid"] = user_id
        st.session_state["user_id"] = user_id
        st.session_state["plan_history"] = {}

    st.markdown("""
    <div class="top-nav"><div class="nav-brand">🌿 AyurvedaRAG</div></div>
    <div style="height:10px"></div>
    """, unsafe_allow_html=True)

    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "ayurveda"

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🌿 Treatment Planner", use_container_width=True, type="primary" if st.session_state["active_tab"] == "ayurveda" else "secondary"):
            st.session_state["active_tab"] = "ayurveda"
            st.rerun()
    with c2:
        if st.button("� Intelligence Dashboard", use_container_width=True, type="primary" if st.session_state["active_tab"] == "progress" else "secondary"):
            st.session_state["active_tab"] = "progress"
            st.rerun()

    if st.session_state["active_tab"] == "ayurveda":
        tab_ayurveda()
    else:
        tab_progress()


if __name__ == "__main__":
    main()
