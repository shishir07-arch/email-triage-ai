import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Email Triage Assistant", page_icon="📧")

st.title("📧 Email Triage Assistant")

# ---- SIDEBAR: Team Setup ----
st.sidebar.header("👥 Team Members")
st.sidebar.write("Add your team members and their roles below.")

if "team" not in st.session_state:
    st.session_state.team = []

with st.sidebar.form("add_member_form", clear_on_submit=True):
    member_name = st.text_input("Name")
    member_role = st.text_input("Role", placeholder="e.g. Billing Team, Engineering, Logistics...")
    add_button = st.form_submit_button("Add Member")
    if add_button and member_name.strip() and member_role.strip():
        st.session_state.team.append({"name": member_name.strip(), "role": member_role.strip()})

if st.session_state.team:
    st.sidebar.write("**Current Team:**")
    for i, member in enumerate(st.session_state.team):
        col1, col2 = st.sidebar.columns([3, 1])
        col1.write(f"**{member['name']}** — {member['role']}")
        if col2.button("❌", key=f"remove_{i}"):
            st.session_state.team.pop(i)
            st.rerun()
else:
    st.sidebar.info("No team members added yet.")

# ---- MAIN: Email Input ----
st.write("Paste a customer support email below and the AI will classify and assign it.")

email_input = st.text_area("Paste email here", height=200, placeholder="e.g. Hi, I was charged twice for my subscription this month...")

if st.button("Analyse Email"):
    if not email_input.strip():
        st.warning("Please paste an email first.")
    elif not st.session_state.team:
        st.warning("Please add at least one team member in the sidebar first.")
    else:
        with st.spinner("Analysing..."):

            team_list = "\n".join([f"- {m['name']} ({m['role']})" for m in st.session_state.team])

            prompt = f"""
You are a customer support triage assistant for a software company.

Here is the available team:
{team_list}

Read the email below and return ONLY the following in this exact format:
Category: <Billing / Bug Report / How-to>
Urgency: <High / Medium / Low>
Reason: <one sentence explaining why>
Suggested Assignee: <pick the most suitable person from the team above based on their role>

Rules:
- Billing = payment, invoice, charge, refund, subscription questions
- Bug Report = something is broken, not working, error, crash
- How-to = asking how to use a feature, setup help, general questions
- High urgency = user is angry, losing money, or system is down
- Medium urgency = issue is affecting work but not critical
- Low urgency = general question, no time pressure
- Only suggest someone from the provided team list

Email:
{email_input}
"""
            response = model.generate_content(prompt)
            result = response.text.strip()

            lines = result.split("\n")
            parsed = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    parsed[key.strip()] = value.strip()

            st.success("Analysis Complete!")

            col1, col2 = st.columns(2)

            with col1:
                category = parsed.get("Category", "Unknown")
                urgency = parsed.get("Urgency", "Unknown")

                if urgency == "High":
                    urgency_color = "🔴"
                elif urgency == "Medium":
                    urgency_color = "🟡"
                else:
                    urgency_color = "🟢"

                st.metric("Category", category)
                st.metric("Urgency", f"{urgency_color} {urgency}")

            with col2:
                assignee = parsed.get("Suggested Assignee", "Unknown")
                reason = parsed.get("Reason", "")
                st.metric("Assigned To", assignee)
                st.info(f"**Reason:** {reason}")