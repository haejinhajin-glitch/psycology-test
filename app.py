import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="TEAM PROJECT SURVIVAL", layout="centered")

# 2. 게임 UI 테마 CSS (픽셀 감성 UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    
    .stApp { background-color: #1a1a2e; color: #ffffff; font-family: 'Nanum Gothic', sans-serif; }
    
    /* 게임 헤더 바 */
    .game-header {
        background-color: #252545;
        border: 2px solid #555588;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* 퀘스트 카드 스타일 */
    .quest-box {
        background-color: #2d2d55;
        border: 4px solid #4a4a8c;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .quest-badge {
        background-color: #f4d03f;
        color: #1a1a2e;
        padding: 5px 15px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    /* 버튼 스타일 */
    div.stButton > button {
        background: linear-gradient(to bottom, #6c5ce7, #4834d4);
        color: white;
        border: 2px solid #a29bfe;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 0;
        width: 100%;
        text-transform: uppercase;
    }
    
    /* 라디오 버튼 커스텀 */
    div[data-testid="stRadio"] label {
        background-color: #3b3b6d;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: block;
        border: 1px solid #555588;
    }
    </style>
""", unsafe_allow_html=True)

# 질문 데이터 (이전 로직 유지)
questions = [
    {"id": "낙관성 편향", "badge": "📢 마감 직전의 빌런 발생", "text": "마감 직전 팀원들의 잠수... 당신의 선택은?", "options": ["독박 하드캐리", "교수님과 타협"]},
    # ... (나머지 5개 질문 동일)
]

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_selections' not in st.session_state: st.session_state.user_selections = {}

# --- 메인 화면 ---
if st.session_state.step == 0:
    st.markdown("""
        <div class='game-header'>
            <div>👤 Lv.1 | EXP 30/100</div>
            <div>⚡ 5/5 | 💎 100</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align:center;'>조별과제 잔혹사</h1>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/lib/streamlit/static/favicon.png", width=150) # 도트 캐릭터 자리
    
    if st.button("START: 테스트 시작하기"):
        st.session_state.step = 1
        st.rerun()

elif 1 <= st.session_state.step <= 6:
    q = questions[st.session_state.step - 1]
    st.markdown(f"<div class='quest-box'><span class='quest-badge'>{q['badge']}</span><br><br><h3>{q['text']}</h3></div>", unsafe_allow_html=True)
    
    choice = st.radio("상황 선택:", q['options'], label_visibility="collapsed")
    
    if st.button("결정하기"):
        st.session_state.user_selections[q['id']] = choice
        st.session_state.step += 1
        st.rerun()
