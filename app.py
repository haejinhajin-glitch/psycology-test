import streamlit as st
import plotly.graph_objects as go

# 1. 페이지 설정
st.set_page_config(page_title="TEAM PROJECT SURVIVAL", layout="centered")

# 2. 커스텀 CSS (픽셀 RPG 스타일)
def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
    
    .stApp { background-color: #0a0a1a; color: #ffffff; font-family: 'VT323', monospace; }
    
    .pixel-box {
        border: 4px solid #ffffff;
        padding: 20px;
        background: #1a1a2e;
        box-shadow: 8px 8px 0px #4d0099;
        margin-bottom: 20px;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #1a1a2e;
        color: #00ffff;
        border: 2px solid #00ffff;
        font-family: 'Press Start 2P', cursive;
        padding: 15px;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #00ffff;
        color: #000000;
        box-shadow: 0 0 15px #00ffff;
    }
    
    .stats-bar { font-family: 'Press Start 2P'; font-size: 10px; color: #ffff00; }
    </style>
    """, unsafe_allow_html=True)

local_css()

# 3. 세션 상태 초기화
if 'stage' not in st.session_state: st.session_state.stage = 0

# 4. 화면 구성 함수
def render_stats():
    st.markdown("""
    <div class="stats-bar">
    LV.1 대학생 <br>
    HP [██████████] 100% <br>
    MENTAL [██████████] 100%
    </div>
    """, unsafe_allow_html=True)

# 5. 메인 로직
if st.session_state.stage == 0:
    st.markdown("<h1 style='text-align: center; font-family: \"Press Start 2P\";'>TEAM PROJECT SURVIVAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>조별과제 잔혹사</p>", unsafe_allow_html=True)
    if st.button("▶ START GAME"):
        st.session_state.stage = 1
        st.rerun()

elif st.session_state.stage == 1:
    render_stats()
    st.markdown("### 📜 QUEST 01: 마감 직전의 빌런 발생")
    st.write("팀원들이 전부 잠수탔다... 당신의 선택은?")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⚔️ 내가 캐리한다"):
            st.session_state.stage = 2
    with col2:
        if st.button("🛡️ 현실을 받아들인다"):
            st.session_state.stage = 2
        
