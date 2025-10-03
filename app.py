# app.py
import streamlit as st
from llm_client import chat_completion
from prompts import SYSTEM_PROMPT, QUESTION_PROMPT_TEMPLATE
from storage import save_candidate
import re, json, time
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

END_KEYWORDS = {"exit", "quit", "bye", "stop", "end", "goodbye"}

# --- Helper Functions ---
def normalize_tech_stack(text: str):
    if not text:
        return []
    parts = re.split(r"[,\n/|]+|\sand\s", text, flags=re.I)
    return [p.strip() for p in parts if p.strip()]

def initialize():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "candidate" not in st.session_state:
        st.session_state.candidate = {}
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "questions_generated" not in st.session_state:
        st.session_state.questions_generated = False

def add_message(role, text):
    st.session_state.messages.append({"role": role, "text": text, "ts": int(time.time())})

def display_chat():
    """Render messages as card-style chat bubbles with mobile view design"""
    st.markdown("""
    <style>
        .chat-card {
            padding: 12px 18px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 90%;
            word-wrap: break-word;
        }
        .assistant-card {
            background-color: #f0f0f0;
            color: #000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .user-card {
            background-color: #0078d4;
            color: #fff;
            margin-left: auto;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }
        @media (max-width: 768px) {
            .chat-card { max-width: 100%; }
        }
    </style>
    """, unsafe_allow_html=True)

    for msg in st.session_state.messages:
        role_class = "assistant-card" if msg["role"] == "assistant" else "user-card"
        st.markdown(f"""
        <div class="chat-container">
            <div class="chat-card {role_class}">
                {msg['text']}
            </div>
        </div>
        """, unsafe_allow_html=True)

def extract_fields(text):
    out = {}
    m = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)
    if m: out["email"] = m.group(1)
    m = re.search(r"(\+?\d{7,15})", text)
    if m: out["phone"] = m.group(1)
    m = re.search(r"(\d+)\s*(?:years|yrs|yr)\s*(?:of\s*)?experience", text, re.I)
    if m: out["years_experience"] = m.group(1)
    m = re.search(r"full\s*name\s*[:\-]\s*(.+)", text, re.I)
    if m: out["full_name"] = m.group(1).split("\n")[0].strip()
    m = re.search(r"(?:position|role)\s*[:\-]\s*(.+)", text, re.I)
    if m: out["desired_position"] = m.group(1).split("\n")[0].strip()
    m = re.search(r"(?:location|city)\s*[:\-]\s*(.+)", text, re.I)
    if m: out["current_location"] = m.group(1).split("\n")[0].strip()
    m = re.search(r"tech\s*stack\s*[:\-]\s*(.+)", text, re.I)
    if m:
        out["tech_stack"] = normalize_tech_stack(m.group(1))
    return out

def generate_questions(candidate_name, techs, qcount=4):
    prompt = QUESTION_PROMPT_TEMPLATE.format(
        qcount=qcount,
        candidate_name=candidate_name or "Candidate",
        technologies=", ".join(techs)
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    resp = chat_completion(messages, max_tokens=1200, temperature=0.2)
    start = resp.find("{")
    try:
        json_text = resp[start:]
        parsed = json.loads(json_text)
        return parsed
    except Exception:
        return None

def validate_candidate_info(candidate):
    required_fields = ["full_name", "email", "phone", "years_experience", "desired_position", "current_location", "tech_stack"]
    missing = [f for f in required_fields if not candidate.get(f)]
    return missing

# --- Main App ---
def main():
    st.set_page_config(page_title="TalentScout Chatbot", layout="wide")
    initialize()
    st.title("🤖 TalentScout - AI Hiring Assistant")

    # Display chat messages
    display_chat()

    # Step 1: Candidate info card
    if not st.session_state.questions_generated:
        missing = validate_candidate_info(st.session_state.candidate)
        if missing:
            st.markdown("### Please fill in your information to continue")
            with st.form("candidate_form"):
                st.session_state.candidate["full_name"] = st.text_input("Full Name", value=st.session_state.candidate.get("full_name",""))
                st.session_state.candidate["email"] = st.text_input("Email", value=st.session_state.candidate.get("email",""))
                st.session_state.candidate["phone"] = st.text_input("Phone", value=st.session_state.candidate.get("phone",""))
                st.session_state.candidate["years_experience"] = st.text_input("Years of Experience", value=st.session_state.candidate.get("years_experience",""))
                st.session_state.candidate["desired_position"] = st.text_input("Desired Position", value=st.session_state.candidate.get("desired_position",""))
                st.session_state.candidate["current_location"] = st.text_input("Location", value=st.session_state.candidate.get("current_location",""))
                tech = st.text_area("Tech Stack (comma separated)", value=", ".join(st.session_state.candidate.get("tech_stack",[])))
                st.session_state.candidate["tech_stack"] = normalize_tech_stack(tech)
                st.session_state.candidate["consent"] = st.checkbox("Consent to anonymized storage", value=st.session_state.candidate.get("consent", False))
                submitted = st.form_submit_button("Submit")
                if submitted:
                    missing = validate_candidate_info(st.session_state.candidate)
                    if missing:
                        add_message("assistant", f"<span style='color:#000;'>Please complete all required fields: {', '.join(missing)}</span>")
                        st.experimental_rerun()
                    else:
                        add_message("assistant", "Thanks! Generating your technical questions...")
                        st.session_state.questions_generated = True
                        
        return

    # Step 2: Generate questions
    if "last_questions_json" not in st.session_state.candidate:
        parsed = generate_questions(st.session_state.candidate.get("full_name","Candidate"), st.session_state.candidate.get("tech_stack",[]))
        if parsed:
            st.session_state.candidate["last_questions_json"] = parsed
        else:
            add_message("assistant", "Failed to generate questions. Please try again later.")
            return

    # Step 3: Display questions in mobile-style cards with answer fields
    st.markdown("### Answer the following questions")
    for tech, qs in st.session_state.candidate["last_questions_json"].items():
        st.markdown(f"#### {tech} Questions")
        for idx, q in enumerate(qs, start=1):
            key = f"{tech}_{idx}"
            ans = st.text_input(f"{q['question']}", key=key, value=st.session_state.answers.get(key, ""))
            st.session_state.answers[key] = ans

    # Step 4: Finish and download
    st.markdown("---")
    if st.button("Finish and Download"):
        if st.session_state.candidate.get("consent"):
            save_candidate(st.session_state.candidate)
        # Prepare CSV
        rows = []
        for tech, qs in st.session_state.candidate["last_questions_json"].items():
            for idx, q in enumerate(qs, start=1):
                key = f"{tech}_{idx}"
                rows.append({
                    "Technology": tech,
                    "Question": q["question"],
                    "Answer": st.session_state.answers.get(key, "")
                })
        df = pd.DataFrame(rows)
        st.download_button("Download Answers CSV", data=df.to_csv(index=False), file_name="answers.csv", mime="text/csv")
        st.download_button("Download Answers JSON", data=json.dumps(rows, indent=2), file_name="answers.json", mime="application/json")
        add_message("assistant", "Thank you for completing the assessment!")

if __name__ == "__main__":
    main()
