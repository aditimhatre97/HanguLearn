
import random
import streamlit as st

st.set_page_config(
    page_title="HanguLearn | Korean Learning",
    page_icon="🇰🇷",
    layout="wide",
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fbf8ff, #f1eaff);
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #8064c8, #b49be8);
    color: white;
    padding: 30px;
    border-radius: 22px;
    margin-bottom: 22px;
}
.hero h1 { color: white; }
.hero p { font-size: 17px; }
div.stButton > button {
    border-radius: 12px;
    border: 1px solid #d8c9f5;
}
[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #e9defa;
}
</style>
""", unsafe_allow_html=True)

# ---------- LEARNING DATA ----------
hangul = {
    "Vowels": [
        ("ㅏ", "a", "Like 'a' in father"),
        ("ㅓ", "eo", "A sound similar to 'uh'"),
        ("ㅗ", "o", "Like 'o' in go"),
        ("ㅜ", "u", "Like 'oo' in moon"),
        ("ㅡ", "eu", "A Korean vowel with no exact English equivalent"),
        ("ㅣ", "i", "Like 'ee' in see"),
        ("ㅐ", "ae", "Similar to 'e' in bed for many speakers"),
        ("ㅔ", "e", "Often pronounced similarly to ㅐ"),
    ],
    "Consonants": [
        ("ㄱ", "g/k", "Between English g and k, depending on position"),
        ("ㄴ", "n", "Like n in nose"),
        ("ㄷ", "d/t", "Between English d and t, depending on position"),
        ("ㄹ", "r/l", "A sound that varies with position"),
        ("ㅁ", "m", "Like m in moon"),
        ("ㅂ", "b/p", "Between English b and p, depending on position"),
        ("ㅅ", "s", "Like s in sun, with contextual variations"),
        ("ㅇ", "ng / silent", "Silent at the start of a syllable; ng at the end"),
        ("ㅈ", "j", "Similar to j in jam"),
        ("ㅎ", "h", "Like h in hat"),
    ],
}

vocabulary = [
    {"korean": "안녕하세요", "meaning": "Hello", "category": "Greetings"},
    {"korean": "감사합니다", "meaning": "Thank you", "category": "Greetings"},
    {"korean": "네", "meaning": "Yes", "category": "Basics"},
    {"korean": "아니요", "meaning": "No", "category": "Basics"},
    {"korean": "물", "meaning": "Water", "category": "Everyday"},
    {"korean": "학교", "meaning": "School", "category": "Everyday"},
    {"korean": "친구", "meaning": "Friend", "category": "People"},
    {"korean": "사랑", "meaning": "Love", "category": "Everyday"},
    {"korean": "책", "meaning": "Book", "category": "Everyday"},
    {"korean": "한국", "meaning": "Korea", "category": "Places"},
    {"korean": "한국어", "meaning": "Korean language", "category": "Learning"},
    {"korean": "저는 아디티입니다", "meaning": "I am Aditi", "category": "Sentences"},
]

questions = [
    {"q": "What does 안녕하세요 mean?",
     "options": ["Goodbye", "Hello", "Sorry", "Good night"],
     "answer": "Hello"},
    {"q": "Which character represents the 'n' consonant?",
     "options": ["ㄱ", "ㄴ", "ㅁ", "ㅅ"],
     "answer": "ㄴ"},
    {"q": "What does 물 mean?",
     "options": ["Book", "School", "Water", "Friend"],
     "answer": "Water"},
    {"q": "Which vowel is romanized as 'i'?",
     "options": ["ㅏ", "ㅜ", "ㅗ", "ㅣ"],
     "answer": "ㅣ"},
    {"q": "What does 친구 mean?",
     "options": ["Teacher", "Friend", "Water", "Korea"],
     "answer": "Friend"},
    {"q": "What does 감사합니다 mean?",
     "options": ["Thank you", "Hello", "Yes", "No"],
     "answer": "Thank you"},
    {"q": "Which character is silent at the start of a syllable?",
     "options": ["ㅇ", "ㄴ", "ㅁ", "ㅎ"],
     "answer": "ㅇ"},
    {"q": "What does 한국어 mean?",
     "options": ["Korea", "Korean language", "School", "Book"],
     "answer": "Korean language"},
]

# ---------- SESSION STATE ----------
defaults = {
    "quiz_order": list(range(len(questions))),
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_answered": False,
    "quiz_feedback": "",
    "quiz_selected": None,
    "vocab_index": 0,
    "show_meaning": False,
    "learned": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🇰🇷 HanguLearn</h1>
    <p>Your little corner of Korean learning.</p>
    <p>Learn Hangul, explore vocabulary, and test your knowledge —
    one step at a time. 화이팅! (Hwaiting — You can do it!)</p>
</div>
""", unsafe_allow_html=True)

st.write("### 안녕하세요! Welcome back 👋")
st.write("Choose a learning space below and start practising.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔤 Hangul", "🗂️ Vocabulary", "🧠 Quiz", "📊 My Progress"
])

# ---------- HANGUL ----------
with tab1:
    st.subheader("Discover the Korean alphabet")
    kind = st.radio(
        "Choose a character group",
        list(hangul.keys()),
        horizontal=True,
        key="hangul_kind",
    )
    entries = hangul[kind]
    cols = st.columns(4)

    for i, (char, roman, hint) in enumerate(entries):
        with cols[i % 4]:
            with st.container(border=True):
                st.markdown(
                    f"<h1 style='text-align:center;color:#8064c8'>"
                    f"{char}</h1>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<p style='text-align:center'><b>{roman}</b></p>",
                    unsafe_allow_html=True,
                )
                st.caption(hint)
                if st.button(
                    "Practised ✓" if char in st.session_state.learned
                    else "Mark practised",
                    key=f"practice_{kind}_{char}",
                    use_container_width=True,
                ):
                    if char not in st.session_state.learned:
                        st.session_state.learned.append(char)
                    st.rerun()

    st.info(
        "Romanizations are learning aids, not exact pronunciation guides. "
        "Listening to native Korean speakers will help you learn the sounds."
    )

# ---------- VOCABULARY ----------
with tab2:
    st.subheader("Vocabulary flashcards")
    st.write("Try to remember the meaning before revealing the answer.")

    idx = st.session_state.vocab_index % len(vocabulary)
    word = vocabulary[idx]

    st.caption(f"Card {idx + 1} of {len(vocabulary)} · {word['category']}")

    with st.container(border=True):
        st.markdown(
            f"<h1 style='text-align:center;color:#8064c8'>"
            f"{word['korean']}</h1>",
            unsafe_allow_html=True,
        )
        if st.session_state.show_meaning:
            st.markdown(
                f"<h3 style='text-align:center'>{word['meaning']}</h3>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<p style='text-align:center'>"
                "Think of the English meaning...</p>",
                unsafe_allow_html=True,
            )

    left, right = st.columns(2)
    with left:
        if st.button("Reveal meaning", use_container_width=True):
            st.session_state.show_meaning = True
            st.rerun()
    with right:
        if st.button("Next card →", use_container_width=True):
            st.session_state.vocab_index = (idx + 1) % len(vocabulary)
            st.session_state.show_meaning = False
            st.rerun()

# ---------- QUIZ ----------
with tab3:
    st.subheader("Test your Korean knowledge")
    total = len(questions)
    idx = st.session_state.quiz_index

    if idx < total:
        q = questions[st.session_state.quiz_order[idx]]
        st.progress(idx / total, text=f"Question {idx + 1} of {total}")
        st.markdown(f"### {q['q']}")

        choice = st.radio(
            "Choose your answer",
            q["options"],
            index=None,
            disabled=st.session_state.quiz_answered,
            key=f"choice_{idx}",
        )

        if not st.session_state.quiz_answered:
            if st.button("Check answer", type="primary"):
                if choice is None:
                    st.warning("Choose an answer first!")
                else:
                    st.session_state.quiz_selected = choice
                    st.session_state.quiz_answered = True
                    if choice == q["answer"]:
                        st.session_state.quiz_score += 1
                        st.session_state.quiz_feedback = "correct"
                    else:
                        st.session_state.quiz_feedback = "incorrect"
                    st.rerun()
        else:
            if st.session_state.quiz_feedback == "correct":
                st.success("Correct! 잘했어요! (Well done!)")
            else:
                st.error(f"Not quite! The correct answer is: {q['answer']}")

            if st.button("Next question →", type="primary"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_feedback = ""
                st.session_state.quiz_selected = None
                st.rerun()

    else:
        st.balloons()
        score = st.session_state.quiz_score
        st.markdown("### Quiz complete! 🎉")
        st.metric("Your final score", f"{score} / {total}")
        st.write(f"You answered {score} out of {total} questions correctly.")
        if st.button("Try again"):
            st.session_state.quiz_order = random.sample(range(total), total)
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False
            st.session_state.quiz_feedback = ""
            st.session_state.quiz_selected = None
            st.rerun()

# ---------- PROGRESS ----------
with tab4:
    st.subheader("Your learning dashboard")
    practiced = len(st.session_state.learned)
    quiz_done = st.session_state.quiz_index
    score = st.session_state.quiz_score

    a, b, c = st.columns(3)
    a.metric("Characters practised", practiced)
    b.metric("Quiz questions completed", quiz_done)
    c.metric("Correct answers", score)

    st.write("#### Hangul practice")
    st.progress(practiced / 18, text=f"{practiced} of 18 characters practised")

    st.write("#### Quiz progress")
    st.progress(quiz_done / len(questions), text=f"{quiz_done} of {len(questions)} questions completed")

    st.caption(
        "This first version stores progress for the current session only. "
        "Persistent accounts and saved progress can be added in a future version."
    )

st.divider()
st.caption("HanguLearn · A beginner-friendly Korean learning project 🇰🇷")
