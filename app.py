import streamlit as st
import plotly.express as px
import pandas as pd
import time

# 1. 페이지 설정
st.set_page_config(page_title="조별과제 잔혹사: 나의 팀플 성향 진단", page_icon="📝", layout="centered")

# 2. CSS 스타일 (기존과 동일)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    * { font-family: 'Gowun Dodum', sans-serif !important; }
    .stApp { background-color: #F4F7F9; }
    .card-container { background-color: #ffffff; padding: 35px; border-radius: 20px; box-shadow: 0px 8px 16px rgba(187, 143, 206, 0.15); margin-bottom: 30px; border: 1px solid #E8DAEF; }
    .main-title { font-size: 2.1rem; font-weight: bold; text-align: center; color: #6C3483; line-height: 1.4; margin-bottom: 12px; }
    .sub-title { font-size: 1.15rem; text-align: center; color: #7FB3D5; margin-bottom: 35px; font-weight: 500; }
    .q-badge { background-color: #FEF9E7; color: #7D6608; padding: 6px 16px; border-radius: 30px; font-weight: bold; font-size: 1rem; display: inline-block; margin-bottom: 15px; border: 1px solid #F9E79F; }
    .q-text { font-size: 1.3rem; font-weight: bold; color: #2C3E50; line-height: 1.6; margin-bottom: 20px; }
    .type-container { background-color: #ffffff; padding: 30px; border-radius: 20px; border: 1px solid #BB8FCE; margin-bottom: 25px; }
    .character-avatar { font-size: 3rem; text-align: center; margin: 10px auto; width: 80px; height: 80px; background-color: #EBF5FB; border-radius: 50%; line-height: 80px; }
    .stButton>button { border-radius: 12px !important; font-size: 1.1rem !important; background-color: #BB8FCE !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 질문 데이터 구조화 (점수 가중치 포함)
questions = [
    {
        "id": "낙관성 편향", "badge": "📢 마감 직전의 빌런 발생",
        "text": "팀 프로젝트 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 던져줬습니다. 속이 타들어 가는 순간, 내 머릿속 스치는 생각은?",
        "options": {"'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.": 100, "'조원들이 안 도와주면 현실적으로 한계가 있지.' 마음을 비우고 상황에 맞춰 교수님과 타협한다.": 20}
    },
    {
        "id": "가용성 편향", "badge": "💬 단톡방의 불길한 침묵",
        "text": "조장이 단톡방에 '자료조사 언제쯤 끝날까요?'라고 물었는데 아무도 답장 없이 3시간 동안 안읽씹이 이어집니다. 이때 밀려오는 나의 생각은?",
        "options": {"'설마 다들 나 몰래 따로 방 파서 내 뒷담화하고 있나?' 에타에서 본 단톡방 왕따 썰을 떠올리며 불안해한다.": 100, "'그냥 마침 타이밍이 겹쳐서 다들 바쁘거나 폰을 안 보고 있겠지.' 하고 대수롭지 않게 넘긴다.": 20}
    },
    {
        "id": "매몰비용 오류", "badge": "📂 산으로 가는 PPT 미련",
        "text": "팀원 한 명이 이틀 밤을 새워 자료를 조사해 왔는데, 우리 조 발표 주제와 전혀 맞지 않는 쓸모없는 자료입니다. 이때 당신의 대처는?",
        "options": {"'그래도 밤새 고생해서 찾아온 자료인데 아까우니까...' 어떻게든 욱여넣어 발표 슬라이드에 포함한다.": 100, "'주제와 안 맞으면 냉정하게 버려야지.' 고생한 건 미안하지만 과감히 제외하고 새로 조사한다.": 20}
    },
    {
        "id": "틀 효과", "badge": "🐻 교수님의 무서운 한마디",
        "text": "교수님이 피드백 도중 우리 조 기획안을 보며 한마디 하십니다. 당신의 멘탈을 더 와르르 무너뜨리는 멘트는 어느 쪽인가요?",
        "options": {"'A 방식: 자네 조가 짠 기획안은 C학점 이하로 삐끗해서 미끄러질 확률이 30%나 되네.' (부정적 실패율 강조)": 100, "'B 방식: 자네 조가 짠 기획안은 안정적으로 A학점 이상 방어할 확률이 70%나 되네.' (긍정적 성공률 강조)": 20}
    },
    {
        "id": "결합 오류", "badge": "🔎 옆 조 조장의 정체",
        "text": "옆 조 조장은 매일 인스타에 화려한 술자리와 명품을 인증하면서도, 팀플 학점까지 매번 A+을 받는 것처럼 보입니다. 이 조장의 실제 모습으로 '확률상' 더 맞는 것은?",
        "options": {"인스타 피드만 화려해 보일 뿐, 남들과 똑같이 취업 걱정하고 조원 잔혹사에 시달리는 평범한 학생이다.": 20, "엄청난 금수저 집안이면서 동시에 지능도 천재적이고 팀원 복까지 타고나 스트레스를 아예 모르는 완벽한 존재이다.": 100}
    },
    {
        "id": "전망 이론", "badge": "💰 조별과제 무임승차 고발하기",
        "text": "조원 한 명이 한 번도 회의에 참여하지 않았습니다. 기말고사 직전, 이 빌런을 교수님께 찔러 조치할 기회가 생겼다면 당신의 선택은?",
        "options": {"안정형: 조건 없이 이 빌런의 이름만 칼같이 빼서 내 기여도와 점수를 안전하게 보장받는다.": 20, "리스크형: '이판사판이다!' 동전을 던지듯 도박하는 심정으로, 교수님께 고발해 잘되면 가산점을 받고 잘못 꼬이면 조 전체가 감점되는 리스크를 감수한다.": 100}
    }
]

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_selections' not in st.session_state: st.session_state.user_selections = {}

# 로직 실행부
if st.session_state.step == 0:
    st.markdown("<div class='main-title'>👥 조별과제 잔혹사<br>나의 팀플 성향 & 인지 오류 진단</div>", unsafe_allow_html=True)
    if st.button("👉 진단 시작하기", use_container_width=True):
        st.session_state.step = 1; st.rerun()

elif 1 <= st.session_state.step <= 6:
    q = questions[st.session_state.step - 1]
    st.progress(st.session_state.step / 6)
    st.markdown(f"<div class='card-container'><div class='q-badge'>{q['badge']}</div><div class='q-text'>{q['text']}</div></div>", unsafe_allow_html=True)
    
    choice = st.radio("선택지:", list(q['options'].keys()), label_visibility="collapsed")
    if st.button("다음 ➡️", use_container_width=True):
        st.session_state.user_selections[q['id']] = q['options'][choice]
        st.session_state.step += 1; st.rerun()

elif st.session_state.step == 7:
    with st.spinner('당신의 팀플 성향을 분석 중입니다...'):
        time.sleep(1.5)
        st.balloons()
        
    scores = st.session_state.user_selections
    df = pd.DataFrame({'bias': list(scores.keys()), 'score': list(scores.values())})
    fig = px.line_polar(df, r='score', theta='bias', line_close=True, range_r=[0, 100])
    fig.update_traces(fill='toself', fillcolor='rgba(187, 143, 206, 0.2)')
    st.plotly_chart(fig, use_container_width=True)
    
    bias_count = sum(1 for s in scores.values() if s == 100)
    st.markdown(f"### 🏹 당신의 팀플 유형: {'유형 1~4 상세 로직 생략'}")
    
    if st.button("🔄 다시 하기"):
        st.session_state.step = 0; st.session_state.user_selections = {}; st.rerun()
