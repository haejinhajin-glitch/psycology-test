import streamlit as st
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="TEAM PROJECT SURVIVAL", layout="centered")

# 2. CSS 디자인 (픽셀 RPG 스타일 + 네온)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    .stApp { background-color: #050510; color: #fff; font-family: 'VT323', monospace; }
    .rpg-box { border: 4px solid #fff; padding: 20px; background: #0d0d2b; box-shadow: 6px 6px 0px #4d0099; margin: 20px 0; }
    h1, h2 { font-family: 'Press Start 2P', cursive; color: #00ffff; text-align: center; }
    .stButton>button { width: 100%; border: 3px solid #00ffff; background: #1a1a2e; color: #00ffff; 
                       font-family: 'Press Start 2P'; padding: 15px; margin: 5px 0; }
    .stButton>button:hover { background: #00ffff; color: #000; box-shadow: 0 0 15px #00ffff; }
    .hud { font-family: 'Press Start 2P'; font-size: 12px; color: #ffff00; text-align: center; border: 2px solid #fff; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 초기화
if 'stage' not in st.session_state: st.session_state.stage = 'intro'
if 's1_score' not in st.session_state: st.session_state.s1_score = 0
if 's2_score' not in st.session_state: st.session_state.s2_score = 0
if 'q_idx' not in st.session_state: st.session_state.q_idx = 0

# 4. 질문 데이터
questions = [
    {"q": "📜 QUEST 01: 마감 직전 빌런 등장", "a1": "내가 밤새서 캐리한다 (낙관성 편향)", "a2": "팀원에게 역할 분담 재공지 (이성적 대처)"},
    {"q": "📜 QUEST 02: 단톡방의 침묵", "a1": "나를 싫어하나? 불안해함 (가용성 편향)", "a2": "바쁘겠거니 하고 기다림 (객관적 판단)"},
    {"q": "📜 QUEST 03: 주제와 안 맞는 자료", "a1": "밤새 만든 게 아까워 PPT 포함 (매몰비용)", "a2": "과감히 삭제하고 다시 작성 (합리적 선택)"},
    {"q": "📜 QUEST 04: 학점 성적표 프레임", "a1": "C학점 이하 30%라는 말에 좌절 (틀 효과)", "a2": "A학점 방어 70%에 집중 (이성적 사고)"},
    {"q": "📜 QUEST 05: 완벽한 옆 조 조장", "a1": "금수저+천재라고 단정 (결합 오류)", "a2": "평범한 학생일 것이라 추측 (확률적 사고)"},
    {"q": "QUEST 06: 무임승차 고발", "a1": "내 점수 안전 보장 선택 (위험 회피)", "a2": "가산점을 위해 모험 선택 (위험 추구)"}
]

# 5. 로직 실행
if st.session_state.stage == 'intro':
    st.markdown("<h1>TEAM PROJECT<br>SURVIVAL</h1>", unsafe_allow_html=True)
    st.write("조별과제 잔혹사: 당신의 인지 편향을 진단합니다.")
    if st.button("▶ START GAME"):
        st.session_state.stage = 'quiz'
        st.rerun()

elif st.session_state.stage == 'quiz':
    q_data = questions[st.session_state.q_idx]
    st.markdown(f"<div class='hud'>STAGE {st.session_state.q_idx + 1}/6</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='rpg-box'><h3>{q_data['q']}</h3></div>", unsafe_allow_html=True)
    
    if st.button(q_data['a1']):
        st.session_state.s1_score += 1
        st.session_state.q_idx += 1
    if st.button(q_data['a2']):
        st.session_state.s2_score += 1
        st.session_state.q_idx += 1
        
    if st.session_state.q_idx >= 6:
        st.session_state.stage = 'result'
        st.rerun()

elif st.session_state.stage == 'result':
    st.markdown("<h2>MISSION COMPLETE</h2>", unsafe_allow_html=True)
    
    # 레이더 차트 (심리 분석 결과)
    fig = go.Figure(data=go.Scatterpolar(
      r=[st.session_state.s1_score*2, st.session_state.s2_score*2, 5, 5, 5],
      theta=['직관(S1)', '이성(S2)', '협동', '멘탈', '창의'],
      fill='toself', line_color='#bf00ff'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig)
    
    st.write(f"분석 결과: 당신은 {'직관적(System 1)' if st.session_state.s1_score > st.session_state.s2_score else '숙고적(System 2)'} 성향이 강합니다.")
    
    if st.button("🔄 RESTART"):
        st.session_state.s1_score = 0
        st.session_state.s2_score = 0
        st.session_state.q_idx = 0
        st.session_state.stage = 'intro'
        st.rerun()
