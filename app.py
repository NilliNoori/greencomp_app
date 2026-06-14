from supabase import create_client
import streamlit as st
import random

# -----------------------------
# SUPABASE SETUP
# -----------------------------

SUPABASE_URL = "https://zmauhcorzekczvywmmvp.supabase.co"
SUPABASE_KEY = "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InptYXVoY29yemVrY3p2eXdtbXZwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODEzODUxODIsImV4cCI6MjA5Njk2MTE4Mn0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    "valuing_sustainability": "Sustainability values",
    "supporting_fairness": "Fairness & inclusion",
    "promoting_nature": "Nature & biodiversity",
    "systems_thinking": "Systems thinking",
    "critical_thinking": "Critical thinking",
    "problem_framing": "Problem framing",
    "futures_literacy": "Future thinking",
    "adaptability": "Adaptability",
    "exploratory_thinking": "Creativity & innovation",
    "political_agency": "Policy & governance",
    "collective_action": "Collaboration",
    "individual_initiative": "Individual action"
}

# -----------------------------
# PAGE SETUP
# -----------------------------

st.set_page_config(page_title="GreenComp Study", layout="wide")

st.title("🌱 GreenComp Classification Tool")

# -----------------------------
# PARTICIPANT FLOW (FIXED)
# -----------------------------

if "participant_id" not in st.session_state:
    st.session_state.participant_id = ""

if st.session_state.participant_id == "":
    st.subheader("Start experiment")

    pid_input = st.text_input("Enter participant ID (e.g. p1, john_01)")

    if st.button("Start quiz"):
        if pid_input.strip() == "":
            st.error("Please enter a valid participant ID")
        else:
            st.session_state.participant_id = pid_input
            st.rerun()

    st.stop()

# -----------------------------
# SESSION STATE INIT
# -----------------------------

if "order" not in st.session_state:
    st.session_state.order = random.sample(keywords, len(keywords))

if "i" not in st.session_state:
    st.session_state.i = 0

if "selected" not in st.session_state:
    st.session_state.selected = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

i = st.session_state.i
total = len(st.session_state.order)

# -----------------------------
# RESET SELECTION PER QUESTION
# -----------------------------

if "last_i" not in st.session_state:
    st.session_state.last_i = -1

if st.session_state.last_i != i:
    st.session_state.selected = None
    st.session_state.submitted = False
    st.session_state.last_i = i

# -----------------------------
# PROGRESS
# -----------------------------

st.sidebar.header("Progress")
st.sidebar.progress(i / total)
st.sidebar.write(f"{i} / {total}")

if st.sidebar.button("Reset"):
    st.session_state.i = 0
    st.session_state.selected = None
    st.session_state.submitted = False
    st.session_state.order = random.sample(keywords, len(keywords))
    st.rerun()

# -----------------------------
# END SCREEN
# -----------------------------

if i >= total:
    st.success("🎉 Finished!")
    st.stop()

# -----------------------------
# QUESTION
# -----------------------------

keyword = st.session_state.order[i]

st.markdown("## Keyword")
st.markdown(f"### **{keyword}**")

st.divider()

st.markdown("## Choose competence")

# -----------------------------
# SELECTION UI
# -----------------------------

for comp, desc in competences.items():
    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("Select", key=f"{comp}_{i}"):
            st.session_state.selected = comp
            st.session_state.submitted = False

    with col2:
        st.markdown(f"### {comp}")
        st.caption(desc)

st.divider()

# -----------------------------
# NOT SURE
# -----------------------------

if st.button("🤷 I’m not sure"):
    st.session_state.selected = "unknown"
    st.session_state.submitted = False

# -----------------------------
# SUBMIT (FIXED FLOW)
# -----------------------------

if st.session_state.selected and not st.session_state.submitted:

    if st.button("Submit answer"):

        try:
            supabase.table("responses").insert({
                "participant_id": st.session_state.participant_id,
                "keyword": keyword,
                "assigned": st.session_state.selected
            }).execute()

            st.session_state.submitted = True
            st.session_state.i += 1
            st.session_state.selected = None

            st.rerun()

        except Exception as e:
            st.error(f"Error saving to Supabase: {e}")
