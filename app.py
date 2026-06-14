from supabase import create_client
import streamlit as st
import pandas as pd
import os
import random

SUPABASE_URL = "https://zmauhcorzekczvywmmvp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InptYXVoY29yemVrY3p2eXdtbXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzODUxODIsImV4cCI6MjA5Njk2MTE4Mn0.r6NOWNdZVSwg4NgYAdPkfttUrRbP4IesfcBmbVLXIfc"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

if "participant_id" not in st.session_state:
    st.session_state.participant_id = st.text_input("Enter participant ID")

if not st.session_state.participant_id:
    st.stop()

# -----------------------------
# DATA
# -----------------------------

keywords = [
    "sustainability",
    "environmental responsibility",
    "ethical behaviour",
    "fairness",
    "equity",
    "inclusion",
    "biodiversity",
    "climate action",
    "environmental protection",
    "renewable energy",
    "systems thinking",
    "interconnections",
    "lifecycle thinking",
    "critical thinking",
    "evidence-based thinking",
    "evaluation",
    "risk assessment",
    "problem definition",
    "stakeholder analysis",
    "root cause analysis",
    "sustainability challenge",
    "future thinking",
    "scenario planning",
    "long-term strategy",
    "forecasting",
    "resilience",
    "adaptability",
    "change management",
    "continuous learning",
    "innovation",
    "creativity",
    "experimentation",
    "design thinking",
    "policy",
    "governance",
    "regulation",
    "advocacy",
    "collaboration",
    "stakeholder engagement",
    "initiative"
]

competences = {
    "valuing_sustainability": "Recognising the importance of sustainability for people and planet.",
    "supporting_fairness": "Promoting equity, justice, and inclusion in society.",
    "promoting_nature": "Understanding and protecting natural systems and biodiversity.",
    "systems_thinking": "Seeing how elements are interconnected within complex systems.",
    "critical_thinking": "Evaluating information and evidence to form reasoned judgments.",
    "problem_framing": "Defining and structuring complex sustainability problems.",
    "futures_literacy": "Thinking about long-term consequences and possible futures.",
    "adaptability": "Adapting to change and uncertainty in dynamic environments.",
    "exploratory_thinking": "Generating new ideas through creativity and experimentation.",
    "political_agency": "Engaging with policies, governance, and societal rules.",
    "collective_action": "Working together with others toward shared goals.",
    "individual_initiative": "Taking responsibility and proactive action individually."
}

# -----------------------------
# SETUP
# -----------------------------

st.set_page_config(page_title="GreenComp Quiz", layout="wide")

st.title("🌱 GreenComp Keyword Classification Tool")

# -----------------------------
# SESSION STATE
# -----------------------------

if "order" not in st.session_state:
    random.shuffle(keywords)
    st.session_state.order = keywords

if "i" not in st.session_state:
    st.session_state.i = 0

i = st.session_state.i
total = len(st.session_state.order)

# -----------------------------
# SIDEBAR PROGRESS
# -----------------------------

st.sidebar.header("Progress")

st.sidebar.progress(i / total if total > 0 else 1)
st.sidebar.write(f"{i} / {total} completed")

if st.sidebar.button("Reset session"):
    st.session_state.i = 0
    random.shuffle(st.session_state.order)
    st.rerun()

# -----------------------------
# END SCREEN
# -----------------------------

if i >= total:
    st.success("🎉 You completed the classification!")

    if os.path.exists("results.csv"):
        st.dataframe(pd.read_csv("results.csv"))

    st.stop()

# -----------------------------
# CURRENT KEYWORD
# -----------------------------

keyword = st.session_state.order[i]

st.markdown("## Keyword")
st.markdown(f"### **{keyword}**")

st.divider()

st.markdown("## Choose the best matching competence")

# -----------------------------
# CARD STYLE SELECTION UI
# -----------------------------

selected = None

for comp, desc in competences.items():
    with st.container():
        col1, col2 = st.columns([1, 6])

        with col1:
            if st.button("Select", key=comp):
                selected = comp

        with col2:
            st.markdown(f"### {comp}")
            st.markdown(f"<span style='color:gray'>{desc}</span>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# NOT SURE OPTION
# -----------------------------

if st.button("🤷 I’m not sure"):
    selected = "unknown"

# -----------------------------
# SUBMIT
# -----------------------------

if selected:
    try:
        supabase.table("responses").insert({
            "keyword": keyword,
            "assigned": selected,
            "participant_id": st.session_state.get("participant_id", "unknown")
        }).execute()

        st.session_state.i += 1
        st.rerun()

    except Exception as e:
        st.error(f"Error saving to Supabase: {e}")
        


