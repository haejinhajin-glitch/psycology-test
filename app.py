import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="조별과제 잔혹사", page_icon="📝", layout="centered")

# 2. 전체 스타일링 (Pretendard 폰트 및 디자인 요소)
st.markdown("""
    <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    * { font-family: 'Pretendard', sans-serif !important; }
    
    .stApp { background-color: #F4F7F9; }
    
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0px 8px 16px rgba(187, 143, 206, 0.15);
        margin-bottom: 30px;
        border: 1px solid #E8DAEF;
    }
    
    /* 표지 타이틀 스타일 */
    .title-box {
        text-align: center;
        padding: 50px 20px;
        background-color: #ffffff;
        border-radius: 30px;
        box-shadow: 0px 10px 25px rgba(187, 143, 206, 0.15);
        border: 2px solid #BB8FCE;
        margin-bottom: 30px;
    }
    .title-main { font-size: 3rem; font-weight: 800; color: #5B2C6F; margin-bottom: 10px; }
    .title-sub { font-size: 1.2rem; color: #7FB3D5; font-weight: 400; }
    .divider { width: 80px; height: 4px; background-color: #BB8FCE; margin: 20px auto; border-radius: 2px; }
    
    /* 질문 및 선택지 스타일 */
    .q-badge { background-color: #FEF9E7; color: #7D6608; padding: 5px 15px; border-radius: 20px; font-weight: bold; font-size: 0.9rem; display: inline-block; margin-bottom: 15px; border: 1px solid #F9E79F; }
    .q-text { font-size: 1.25rem; font-weight: 600; color: #2C3E50; line-height: 1.5; }
    
    div[data-testid="stRadio"] label { font-size: 1.1rem !important; color: #34495E !important; padding: 10px 0 !important; }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label { margin-bottom: 15px !important; }
    
    .stButton>button { border-radius: 12px !important; font-size: 1.1rem !important; padding: 10px 25px !important; background-color: #BB8FCE !important; color: white !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_selections' not in st.session_state: st.session_state.user_selections = {}

questions = [
    {"id": "낙관성 편향", "badge": "📢 마감 직전", "text": "마감은 코앞인데 조원들이 잠수를 탑니다. 당신은?", "options": ["내가 밤새서 하드캐리한다.", "상황에 맞춰 교수님과 타협한다."]},
    {"id": "가용성 편향", "badge": "💬 단톡방의 침묵", "text": "단톡방 안읽씹이 3시간째입니다. 당신은?", "options": ["나 몰래 단톡방을 따로 팠나 불안하다.", "그냥 다들 바쁘겠지 하고 넘긴다."]},
    {"id": "매몰비용 오류", "badge": "📂 산으로 가는 PPT", "text": "주제와 안 맞는 자료를 팀원이 고생해서 찾아왔습니다. 당신은?", "options": ["고생했으니 일단 넣는다.", "주제와 안 맞으면 과감히 버린다."]},
    {"id": "틀 효과", "badge": "🐻 교수님의 피드백", "text": "당신의 멘탈을 더 흔드는 멘트는?", "options": ["실패할 확률 30% 강조", "성공할 확률 70% 강조"]},
    {"id": "결합 오류", "badge": "🔎 옆 조 조장", "text": "엄친아 조장의 실제 모습은?", "options": ["남들처럼 똑같이 힘든 학생이다.", "모든 걸 갖춘 완벽한 존재다."]},
    {"id": "전망 이론", "badge": "💰 빌런 고발", "text": "무임승차 조원을 고발할 기회가 있다면?", "options": ["확실히 점수 챙기는 안정형", "리스크 감수하고 가산점 노리는 도박형"]}
]

# --- 메인 로직 ---
if st.session_state.step == 0:
    st.markdown("""
    <div class='title-box'>
        <div class='title-main'>조별과제 잔혹사</div>
        <div class='divider'></div>
        <div class='title-sub'>나의 팀플 성향 & 인지 오류 정밀 진단</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👉 진단 시작하기", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

elif 1 <= st.session_state.step <= 6:
    q = questions[st.session_state.step - 1]
    st.markdown(f"<div class='card-container'><div class='q-badge'>{q['badge']}</div><div class='q-text'>{q['text']}</div></div>", unsafe_allow_html=True)
    choice = st.radio("선택지:", q['options'], index=None, label_visibility="collapsed")
    if st.button("다음 ➡️"):
        if choice:
            st.session_state.user_selections[q['id']] = choice
            st.session_state.step += 1
            st.rerun()
        else: st.warning("선택지를 골라주세요!")

elif st.session_state.step == 7:
    st.title("📊 진단 결과")
    st.write("분석이 완료되었습니다. 결과에 따라 당신의 유형이 결정됩니다.")
    if st.button("🔄 다시 하기"):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
