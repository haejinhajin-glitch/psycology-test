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
        padding: 40px;
        border-radius: 24px;
        box-shadow: 0px 10px 20px rgba(187, 143, 206, 0.1);
        margin-bottom: 30px;
        border: 1px solid #E8DAEF;
    }
    
    /* 고급스러운 표지 타이틀 디자인 */
    .title-box {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, #FDF2F9 0%, #F4F7F9 100%);
        border-radius: 30px;
        border: 2px solid #BB8FCE;
        margin-bottom: 40px;
    }
    .title-main { font-size: 3.2rem; font-weight: 800; color: #5B2C6F; margin-bottom: 15px; letter-spacing: -1px; }
    .title-sub { font-size: 1.3rem; color: #7FB3D5; font-weight: 400; line-height: 1.8; }
    .divider { width: 100px; height: 5px; background-color: #BB8FCE; margin: 30px auto; border-radius: 3px; }
    
    /* 질문지 가독성 강화 */
    .q-badge { background-color: #FEF9E7; color: #7D6608; padding: 6px 20px; border-radius: 20px; font-weight: 700; font-size: 0.95rem; display: inline-block; margin-bottom: 20px; border: 1px solid #F9E79F; }
    .q-text { font-size: 1.4rem; font-weight: 700; color: #2C3E50; line-height: 1.8; margin-bottom: 25px; }
    
    /* 라디오 버튼 간격 조절 */
    div[data-testid="stRadio"] label { font-size: 1.15rem !important; color: #34495E !important; padding: 15px 10px !important; line-height: 1.6 !important; }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label { margin-bottom: 20px !important; background: white; border-radius: 15px; border: 1px solid #EAECEE; transition: 0.3s; }
    
    .stButton>button { border-radius: 15px !important; font-size: 1.2rem !important; font-weight: 600; padding: 12px 30px !important; background-color: #BB8FCE !important; color: white !important; border: none !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_selections' not in st.session_state: st.session_state.user_selections = {}

# 질문 데이터 (생략된 부분은 기존과 동일하게 유지)
questions = [
    {"id": "낙관성 편향", "badge": "📢 마감 직전의 위기", "text": "팀 프로젝트 마감은 코앞인데 조원들이 잠수를 탑니다. 당신의 선택은?", "options": ["밤새서 하드캐리한다.", "상황에 맞춰 교수님과 타협한다."]},
    {"id": "가용성 편향", "badge": "💬 단톡방의 침묵", "text": "단톡방 안읽씹이 3시간째입니다. 당신의 생각은?", "options": ["나 몰래 따로 방 팠나 불안하다.", "그냥 바쁘겠지 하고 넘긴다."]},
    {"id": "매몰비용 오류", "badge": "📂 산으로 가는 자료", "text": "팀원이 고생해서 찾아왔지만 주제와 안 맞는 자료. 당신은?", "options": ["고생했으니 일단 넣는다.", "냉정하게 버리고 새로 조사한다."]},
    {"id": "틀 효과", "badge": "🐻 교수님의 피드백", "text": "멘탈을 더 흔드는 피드백은?", "options": ["실패율 30% 강조", "성공률 70% 강조"]},
    {"id": "결합 오류", "badge": "🔎 옆 조 조장", "text": "잘나가는 옆 조 조장의 실제 모습은?", "options": ["평범한 학생이다.", "모든 걸 갖춘 완벽한 존재다."]},
    {"id": "전망 이론", "badge": "💰 빌런 고발", "text": "무임승차 조원을 고발할 기회. 당신의 선택은?", "options": ["안전하게 점수 챙기기", "리스크 감수하고 가산점 노리기"]}
]

# --- 메인 로직 ---
if st.session_state.step == 0:
    st.markdown("""
    <div class='title-box'>
        <div class='title-main'>조별과제 잔혹사</div>
        <div class='divider'></div>
        <div class='title-sub'>나의 팀플 성향 & 인지 오류 정밀 진단<br>6가지 질문을 통해 당신의 팀플 유형을 분석합니다.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("👉 진단 시작하기", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

elif 1 <= st.session_state.step <= 6:
    q = questions[st.session_state.step - 1]
    st.markdown(f"<div class='card-container'><div class='q-badge'>{q['badge']}</div><div class='q-text'>{q['text']}</div></div>", unsafe_allow_html=True)
    choice = st.radio(" ", q['options'], index=None, label_visibility="collapsed")
    if st.button("다음 ➡️"):
        if choice:
            st.session_state.user_selections[q['id']] = choice
            st.session_state.step += 1
            st.rerun()
        else: st.warning("선택지를 골라주세요!")

elif st.session_state.step == 7:
    st.title("📊 분석 완료")
    if st.button("🔄 다시 하기"):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
