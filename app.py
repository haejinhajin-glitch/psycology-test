import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="TEAM PROJECT SURVIVAL", page_icon="⚔️", layout="centered")

# 2. 게임 UI 테마 CSS (네이비, 딥 퍼플, 골드 포인트)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    
    * { font-family: 'Nanum Gothic', sans-serif !important; }
    
    .stApp { background-color: #1B1464; color: #FFFFFF; }
    
    /* 게임 상태창 카드 */
    .game-status-bar {
        background: linear-gradient(90deg, #2E1A47 0%, #1B1464 100%);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #F4D03F;
        margin-bottom: 20px;
        color: #F4D03F;
        font-weight: bold;
        display: flex;
        justify-content: space-between;
    }
    
    /* 퀘스트 카드 */
    .quest-card {
        background-color: #2E1A47;
        padding: 30px;
        border-radius: 20px;
        border-left: 10px solid #F4D03F;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    .quest-title { color: #F4D03F; font-size: 1.5rem; font-weight: 800; margin-bottom: 10px; }
    .mission-text { font-size: 1.2rem; color: #E8DAEF; margin-bottom: 20px; }
    
    /* 버튼 스타일 */
    div.stButton > button {
        background-color: #F4D03F;
        color: #1B1464;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        width: 100%;
        height: 50px;
    }
    
    .result-container {
        background-color: #ffffff;
        color: #333;
        padding: 30px;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 데이터 정의
questions = [
    {"id": "낙관성 편향", "badge": "📢 마감 직전의 빌런 발생", "text": "팀 프로젝트 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 던져줬습니다. 속이 타들어 가는 순간, 내 머릿속 스치는 생각은?", "options": ["'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.", "'조원들이 안 도와주면 현실적으로 한계가 있지.' 마음을 비우고 상황에 맞춰 교수님과 타협한다."]},
    {"id": "가용성 편향", "badge": "💬 단톡방의 불길한 침묵", "text": "조장이 단톡방에 '자료조사 언제쯤 끝날까요?'라고 물었는데 아무도 답장 없이 3시간 동안 안읽씹이 이어집니다. 이때 밀려오는 나의 생각은?", "options": ["'설마 다들 나 몰래 따로 방 파서 내 뒷담화하고 있나?' 에타에서 본 단톡방 왕따 썰을 떠올리며 불안해한다.", "'그냥 마침 타이밍이 겹쳐서 다들 바쁘거나 폰을 안 보고 있겠지.' 하고 대수롭지 않게 넘긴다."]},
    {"id": "매몰비용 오류", "badge": "📂 산으로 가는 PPT 미련", "text": "팀원 한 명이 이틀 밤을 새워 자료를 조사해 왔는데, 우리 조 발표 주제와 전혀 맞지 않는 쓸모없는 자료입니다. 이때 당신의 대처는?", "options": ["'그래도 밤새 고생해서 찾아온 자료인데 아까우니까...' 어떻게든 욱여넣어 발표 슬라이드에 포함한다.", "'주제와 안 맞으면 냉정하게 버려야지.' 고생한 건 미안하지만 과감히 제외하고 새로 조사한다."]},
    {"id": "틀 효과", "badge": "🐻 교수님의 무서운 한마디", "text": "교수님이 피드백 도중 우리 조 기획안을 보며 한마디 하십니다. 당신의 멘탈을 더 와르르 무너뜨리는 멘트는 어느 쪽인가요?", "options": ["'A 방식: 자네 조가 짠 기획안은 C학점 이하로 삐끗해서 미끄러질 확률이 30%나 되네.' (부정적 실패율 강조)", "'B 방식: 자네 조가 짠 기획안은 안정적으로 A학점 이상 방어할 확률이 70%나 되네.' (긍정적 성공률 강조)"]},
    {"id": "결합 오류", "badge": "🔎 옆 조 조장의 정체", "text": "옆 조 조장은 매일 인스타에 화려한 술자리와 명품을 인증하면서도, 팀플 학점까지 매번 A+을 받는 것처럼 보입니다. 이 조장의 실제 모습으로 '확률상' 더 맞는 것은?", "options": ["인스타 피드만 화려해 보일 뿐, 남들과 똑같이 취업 걱정하고 조원 잔혹사에 시달리는 평범한 학생이다.", "엄청난 금수저 집안이면서 동시에 지능도 천재적이고 팀원 복까지 타고나 스트레스를 아예 모르는 완벽한 존재이다."]},
    {"id": "전망 이론", "badge": "💰 조별과제 무임승차 고발하기", "text": "조원 한 명이 한 번도 회의에 참여하지 않았습니다. 기말고사 직전, 이 빌런을 교수님께 찔러 조치할 기회가 생겼다면 당신의 선택은?", "options": ["안정형: 조건 없이 이 빌런의 이름만 칼같이 빼서 내 기여도와 점수를 안전하게 보장받는다.", "리스크형: '이판사판이다!' 동전을 던지듯 도박하는 심정으로, 교수님께 고발해 잘되면 가산점을 받고 잘못 꼬이면 조 전체가 감점되는 리스크를 감수한다."]}
]

# 세션 상태 초기화
if 'step' not in st.session_state: st.session_state.step = 0
if 'user_selections' not in st.session_state: st.session_state.user_selections = {}

# --- [게임 로직] ---
if st.session_state.step == 0:
    st.markdown("## 🎮 TEAM PROJECT SURVIVAL")
    st.markdown("# 조별과제 잔혹사")
    st.markdown("<div class='game-status-bar'>⚡ ENERGY 100 | 💎 GPA 0 | 🏆 EXP 0</div>", unsafe_allow_html=True)
    if st.button(">>> [ START GAME ] <<<"):
        st.session_state.step = 1
        st.rerun()

elif 1 <= st.session_state.step <= 6:
    q_data = questions[st.session_state.step - 1]
    st.markdown(f"<div class='game-status-bar'>QUEST {st.session_state.step} / 6 진행 중</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='quest-card'>
            <div class='quest-title'>{q_data['badge']}</div>
            <div class='mission-text'>{q_data['text']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    choice = st.radio("행동을 선택하세요:", q_data['options'], label_visibility="collapsed")
    if st.button("결정하기"):
        st.session_state.user_selections[q_data['id']] = choice
        st.session_state.step += 1
        st.rerun()

elif st.session_state.step == 7:
    st.markdown("# MISSION COMPLETE")
    # (결과 페이지는 기존 로직을 사용하여 유지하되 위와 같은 게임 테마 CSS 적용 가능)
    st.write("결과 화면 로직이 실행됩니다.")
