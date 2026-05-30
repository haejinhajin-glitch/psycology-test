import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정 및 반응형 최적화
st.set_page_config(page_title="조별과제 잔혹사: 나의 팀플 성향 진단", page_icon="📝", layout="centered")

# 2. 연보라 & 하늘 & 노랑 베이스의 단정하고 깔끔한 UI 디자인 (CSS)
st.markdown("""
    <style>
    /* 구글 폰트에서 얇고 깔끔한 개구(Gaegu)체 불러오기 */
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
    
    /* 전체 서체를 개구체로 깔끔하게 통일 */
    * { 
        font-family: 'Gowun Dodum', sans-serif !important; 
    }
    
    /* 전체 배경: 매우 부드럽고 연한 하늘빛 도는 화이트 */
    .stApp {
        background-color: #F4F7F9;
    }
    
    /* 메인 카드 박스: 연보라색 얇은 테두리와 정갈한 레이아웃 */
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 20px;
        box-shadow: 0px 8px 16px rgba(187, 143, 206, 0.15);
        margin-bottom: 30px; /* 아래 선택지와의 간격을 위해 마진 확대 */
        border: 1px solid #E8DAEF; /* 연보라색 기본 테두리 */
        line-height: 2.0;
    }
    
    /* 메인 타이틀: 차분한 딥 연보라 컬러 */
    .main-title {
        font-size: 2.1rem;
        font-weight: bold;
        text-align: center;
        color: #6C3483; /* 딥 연보라 */
        line-height: 1.8;
        margin-bottom: 12px;
    }
    
    .sub-title {
        font-size: 1.15rem;
        text-align: center;
        color: #7FB3D5; /* 부드러운 하늘색 */
        margin-bottom: 35px;
        font-weight: 500;
        line-height: 1.8;
    }
    
    /* 질문 카드 위 배지: 은은한 파스텔 노랑 */
    .q-badge {
        background-color: #FEF9E7; /* 파스텔 노랑 */
        color: #7D6608;
        padding: 6px 16px;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1rem;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #F9E79F;
    }
    
    .q-text {
        font-size: 1.3rem;
        font-weight: bold;
        color: #2C3E50;
        line-height: 1.9;
        margin-bottom: 20px;
    }
    
    /* 🛠️ 라디오 버튼(선택지) 가독성 극대화 커스텀 스타일 */
    div[data-testid="stRadio"] {
        margin-top: 15px !important; /* 질문 박스(위쪽)와 선택지 사이의 간격 확보 */
    }
    
    /* 각 선택지 아이템 간의 상하 간격을 넓히고 패딩 추가 */
    div[data-testid="stRadio"] [data-testid="stWidgetLabel"] + div > div {
        margin-bottom: 16px !important; /* 첫 번째 선택지와 두 번째 선택지 사이 띄우기 */
        padding: 10px 14px !important;  /* 선택지 글씨 주변에 여유 공간 주기 */
        background-color: #ffffff;      /* 선택지 배경을 흰색 박스로 감싸서 단정하게 변경 */
        border-radius: 10px;
        border: 1px solid #EAECEE;
    }
    
    /* 라디오 버튼 선택지 내부 글씨 스타일 정돈 */
    div[data-testid="stRadio"] label {
        font-size: 1.08rem !important;
        color: #2C3E50 !important;
        line-height: 1.8 !important;
        cursor: pointer;
    }
    
    /* 결과 캐릭터 카드 컨테이너 */
    .type-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #BB8FCE; /* 파스텔 연보라 테두리 */
        margin-bottom: 25px;
        box-shadow: 0px 4px 12px rgba(187, 143, 206, 0.1);
        line-height: 1.9;
    }
    
    /* 캐릭터 아바타 배경 원형 처리 */
    .character-avatar {
        font-size: 3rem;
        text-align: center;
        margin: 10px auto;
        width: 80px;
        height: 80px;
        background-color: #EBF5FB; /* 파스텔 하늘색 배경 */
        border-radius: 50%;
        line-height: 80px;
    }
    
    .type-container h4 {
        font-size: 1.4rem !important;
        font-weight: bold;
        text-align: center;
        color: #5B2C6F; /* 연보라 계열 */
        margin-top: 12px;
        margin-bottom: 18px;
    }
    
    .type-container p {
        font-size: 1.05rem !important;
        line-height: 1.9;
        color: #566573;
        margin-bottom: 10px;
    }
    
    /* 기본 텍스트 크기 가독성 최적화 */
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.1rem !important;
        color: #34495E;
        line-height: 1.9;
    }
    
    h3 {
        font-size: 1.6rem !important;
        color: #6C3483 !important; /* 연보라색 타이틀 */
        font-weight: bold !important;
        line-height: 1.8;
    }
    
    /* 솔루션 메모장 스타일 박스 */
    .solution-box {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 18px;
        border-left: 6px solid #BB8FCE; /* 연보라색 포인트 바 */
        border-top: 1px solid #F4F6F7;
        border-right: 1px solid #F4F6F7;
        border-bottom: 1px solid #F4F6F7;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.02);
        line-height: 1.9;
    }
    .solution-title {
        font-size: 1.15rem;
        font-weight: bold;
        color: #5B2C6F;
        margin-bottom: 6px;
    }
    .solution-desc {
        font-size: 1.05rem !important;
        color: #5D6D7E;
        line-height: 1.9;
    }
    
    /* 하단 버튼들: 심플하고 단정한 라운드 스타일 */
    .stButton>button {
        border-radius: 12px !important;
        font-size: 1.1rem !important;
        padding: 8px 25px !important;
        background-color: #BB8FCE !important; /* 차분한 파스텔 연보라 */
        color: white !important;
        border: none !important;
        box-shadow: 0px 4px 8px rgba(187, 143, 206, 0.3) !important;
        transition: all 0.15s ease;
    }
    .stButton>button:hover {
        background-color: #A569BD !important; /* 살짝 짙은 연보라 */
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_selections' not in st.session_state:
    st.session_state.user_selections = {}

# 질문 데이터셋
questions = [
    {
        "id": "낙관성 편향",
        "badge": "📢 마감 직전의 빌런 발생",
        "text": "팀 프로젝트 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 던져줬습니다. 속이 타들어 가는 순간, 내 머릿속 스치는 생각은?",
        "options": ["'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.", "'조원들이 안 도와주면 현실적으로 한계가 있지.' 마음을 비우고 상황에 맞춰 교수님과 타협한다."]
    },
    {
        "id": "가용성 편향",
        "badge": "💬 단톡방의 불길한 침묵",
        "text": "조장이 단톡방에 '자료조사 언제쯤 끝날까요?'라고 물었는데 아무도 답장 없이 3시간 동안 안읽씹이 이어집니다. 이때 밀려오는 나의 생각은?",
        "options": ["'설마 다들 나 몰래 따로 방 파서 내 뒷담화하고 있나?' 에타에서 본 단톡방 왕따 썰을 떠올리며 불안해한다.", "'그냥 마침 타이밍이 겹쳐서 다들 바쁘거나 폰을 안 보고 있겠지.' 하고 대수롭지 않게 넘긴다."]
    },
    {
        "id": "매몰비용 오류",
        "badge": "📂 산으로 가는 PPT 미련",
        "text": "팀원 한 명이 이틀 밤을 새워 자료를 조사해 왔는데, 우리 조 발표 주제와 전혀 맞지 않는 쓸모없는 자료입니다. 이때 당신의 대처는?",
        "options": ["'그래도 밤새 고생해서 찾아온 자료인데 아까우니까...' 어떻게든 욱여넣어 발표 슬라이드에 포함한다.", "'주제와 안 맞으면 냉정하게 버려야지.' 고생한 건 미안하지만 과감히 제외하고 새로 조사한다."]
    },
    {
        "id": "틀 효과",
        "badge": "🐻 교수님의 무서운 한마디",
        "text": "교수님이 피드백 도중 우리 조 기획안을 보며 한마디 하십니다. 당신의 멘탈을 더 와르르 무너뜨리는 멘트는 어느 쪽인가요?",
        "options": ["'A 방식: 자네 조가 짠 기획안은 C학점 이하로 삐끗해서 미끄러질 확률이 30%나 되네.' (부정적 실패율 강조)", "'B 방식: 자네 조가 짠 기획안은 안정적으로 A학점 이상 방어할 확률이 70%나 되네.' (긍정적 성공률 강조)"]
    },
    {
        "id": "결합 오류",
        "badge": "🔎 옆 조 조장의 정체",
        "text": "옆 조 조장은 매일 인스타에 화려한 술자리와 명품을 인증하면서도, 팀플 학점까지 매번 A+을 받는 것처럼 보입니다. 이 조장의 실제 모습으로 '확률상' 더 맞는 것은?",
        "options": ["인스타 피드만 화려해 보일 뿐, 남들과 똑같이 취업 걱정하고 조원 잔혹사에 시달리는 평범한 학생이다.", "엄청난 금수저 집안이면서 동시에 지능도 천재적이고 팀원 복까지 타고나 스트레스를 아예 모르는 완벽한 존재이다."]
    },
    {
        "id": "전망 이론",
        "badge": "💰 조별과제 무임승차 고발하기",
        "text": "조원 한 명이 한 번도 회의에 참여하지 않았습니다. 기말고사 직전, 이 빌런을 교수님께 찔러 조치할 기회가 생겼다면 당신의 선택은?",
        "options": ["안정형: 조건 없이 이 빌런의 이름만 칼같이 빼서 내 기여도와 점수를 안전하게 보장받는다.", "리스크형: '이판사판이다!' 동전을 던지듯 도박하는 심정으로, 교수님께 고발해 잘되면 가산점을 받고 잘못 꼬이면 조 전체가 감점되는 리스크를 감수한다."]
    }
]

# --- 🏠 화면 0: 첫 인트로 페이지 ---
if st.session_state.step == 0:
    st.write("")
    st.markdown("<div class='main-title'>👥 조별과제 잔혹사<br>나의 팀플 성향 & 인지 오류 진단</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>“과연 나는 팀플에서 얼마나 이성적이고 합리적일까?”<br><span style='font-size:1rem; color:#85929E;'>현실적인 팀플 돌발 상황들로 정밀하게 파악해보는 나의 인지 편향 지수</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-container'>
        <p style='line-height: 2.0; color: #2C3E50; font-size: 1.1rem; text-align: center; margin: 0;'>
        <b>대학 생활의 최대 고비, 이름만 들어도 아찔한 '조별과제'</b><br><br>
        우리는 늘 팀플에서 이성적으로 판단하고 최선의 선택을 내린다고 믿지만,<br>
        사실 조원 빌런들을 마주하면 무의식적인 감정과 인지적 착각, '생각의 덫'에 걸려<br>
        스스로 스트레스를 키우거나 독박을 자처하곤 합니다.<br><br>
        6가지 리얼 팀플 상황을 통해 내 안의 숨겨진 비합리성 지수를 정교하게 측정하고,<br>
        <b>나를 꼭 닮은 조별과제 동물 캐릭터 유형과 최고의 팀플 파트너</b>를 매칭해 보세요.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👉 나의 팀플 성향 진단 시작하기", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# --- 📝 화면 1 ~ 6: 질문 스텝 ---
elif 1 <= st.session_state.step <= 6:
    current_idx = st.session_state.step - 1
    q_data = questions[current_idx]
    
    st.progress(st.session_state.step / 6)
    st.caption(f"진단 문항 진행 중: {st.session_state.step} / 6 완료")
    
    st.markdown(f"""
    <div class='card-container'>
        <div class='q-badge'>{q_data['badge']}</div>
        <div class='q-text'>{q_data['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 간격 조정이 반영된 라디오 버튼 호출
    user_choice = st.radio("보기 중 하나를 선택하세요:", q_data['options'], index=0, label_visibility="collapsed")
    
    st.write("")
    if st.button("답변 선택 완료 ➡️", use_container_width=True):
        st.session_state.user_selections[q_data['id']] = user_choice
        st.session_state.step += 1
        st.rerun()

# --- 📊 화면 7: 종합 분석 대시보드 ---
elif st.session_state.step == 7:
    st.markdown("<div class='main-title'>📊 팀플 인지오류 진단 결과</div>", unsafe_allow_html=True)
    st.write("")
    
    scores = {}
    bias_count = 0
    
    if st.session_state.user_selections.get("낙관성 편향") == "'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.":
        scores["낙관성 편향"] = 100; bias_count += 1
    else: scores["낙관성 편향"] = 20
        
    if st.session_state.user_selections.get("가용성 편향") == "'설마 다들 나 몰래 따로 방 파서 내 뒷담화하고 있나?' 에타에서 본 단톡방 왕따 썰을 떠올리며 불안해한다.":
        scores["가용성 편향"] = 100; bias_count += 1
    else: scores["가용성 편향"] = 20
        
    if st.session_state.user_selections.get("매몰비용 오류") == "'그래도 밤새 고생해서 찾아온 자료인데 아까우니까...' 어떻게든 욱여넣어 발표 슬라이드에 포함한다.":
        scores["매몰비용 오류"] = 100; bias_count += 1
    else: scores["매몰비용 오류"] = 20
        
    if st.session_state.user_selections.get("틀 효과") == "'A 방식: 자네 조가 짠 기획안은 C학점 이하로 삐끗해서 미끄러질 확률이 30%나 되네.' (부정적 실패율 강조)":
        scores["틀 효과(프레이밍)"] = 100; bias_count += 1
    else: scores["틀 효과(프레이밍)"] = 20
        
    if st.session_state.user_selections.get("결합 오류") == "엄청난 금수저 집안이면서 동시에 지능도 천재적이고 팀원 복까지 타고나 스트레스를 아예 모르는 완벽한 존재이다.":
        scores["결합 오류"] = 100; bias_count += 1
    else: scores["결합 오류"] = 20

    if st.session_state.user_selections.get("전망 이론") == "리스크형: '이판사판이다!' 동전을 던지듯 도박하는 심정으로, 교수님께 고발해 잘되면 가산점을 받고 잘못 꼬이면 조 전체가 감점되는 리스크를 감수한다.":
        scores["위험추구(전망이론)"] = 100; bias_count += 1
    else: scores["위험회피(전망이론)"] = 20

    df_result = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
    fig = px.line_polar(df_result, r='r', theta='theta', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', fillcolor='rgba(187, 143, 206, 0.2)', line_color='#BB8FCE', line_width=3)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#EAEDED"), bgcolor="white"), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    final_avg = sum(scores.values()) / 6
    st.markdown(f"<h2 style='text-align:center; margin-bottom: 30px; color:#6C3483; font-weight:bold;'>나의 팀플 착각 지수: {final_avg:.0f}점</h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏹 나의 조별과제 행동 유형 결과")
    
    if bias_count <= 1:
        st.markdown("""
        <div class='type-container' style='border-color: #AED6F1;'>
            <div class='character-avatar'>🦅</div>
            <h4>유형 1: 칼같고 이성적인 팀플 매크로, '팩트 독수리'</h4>
            <p><b>팀플 성향:</b> 감정이나 미련에 휘둘리지 않고 철저히 효율과 데이터로만 움직입니다. 조원들이 헛소리를 하거나 잠수를 타면 상처받지 않고 "이름 뺍니다"라며 칼같이 대처하는 냉철한 영웅입니다.</p>
            <p><b>🧩 추천 역할:</b> <b>[자료조사 총괄 및 데이터 팩트 체커]</b><br>엉터리 정보를 귀신같이 가려내고 논리적 결함을 교정하는 최종 검수 역할에 최적화되어 있습니다.</p>
            <p><b>⚠️ 타인이 나를 볼 때 주의할 점:</b> 조원들에게 가끔 '피도 눈물도 없는 인공지능 로봇' 같다는 인상을 주어 묘한 거리감을 유발할 수 있습니다. 피치 못할 사정이 생긴 조원에게 약간의 이모지와 따뜻한 말투를 건네면 팀 분위기가 훨씬 살아납니다.</p>
            <hr style='border: 1px dashed #AED6F1; margin: 15px 0;'>
            <p style='font-size: 1.05rem !important; color: #2C3E50; font-weight: bold;'><b>🤝 같이 조 짜면 대박 나는 환상의 파트너:</b></p>
            <p style='font-size: 1rem !important; margin-left: 10px;'>
            • <b>🦫 실무 비버:</b> 당신의 차가운 뼈대에 살을 붙여줄 최고의 메이커! 당신이 정교하게 발굴한 팩트와 가이드라인을 토대로 군말 없이 완벽한 고퀄리티 PPT를 찍어내 줄 고마운 존재입니다.<br>
            • <b>🐰 불안 보스 토끼:</b> 당신에게 부족한 '감성과 감정 케어'의 마술사! 딱딱한 팀 분위기를 유연하게 풀어주고, 대중의 마음을 흔드는 감성적 발표로 당신의 논리를 200% 빛내줍니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    elif 2 <= bias_count <= 3:
        st.markdown("""
        <div class='type-container' style='border-color: #F9E79F;'>
            <div class='character-avatar'>🦫</div>
            <h4>유형 2: 묵묵히 제 몫을 다하는 평화주의자, '실무 비버'</h4>
            <p><b>팀플 성향:</b> 대다수 선량한 대학생들이 속하는 든든한 황금 밸런스 유형입니다! 가끔 밤샘 자료가 아깝다며 미련을 두거나 단톡방 침묵에 흠칫하기도 하지만, 이내 멘탈을 잡고 현실적인 대안을 묵묵히 빌딩해 나갑니다.</p>
            <p><b>🧩 추천 역할:</b> <b>[자료 편집 및 PPT 실무 제작자]</b><br>상식적이고 조화로운 시선을 가졌기 때문에 대립하는 의견을 융합해 실질적인 결과물로 시각화하는 데 도사입니다.</p>
            <p><b>⚠️ 타인이 나를 볼 때 주의할 점:</b> 무난하고 착한 성격 때문에 무임승차 빌런들이 은근슬쩍 숟가락을 얹으려 표적으로 삼기 쉽습니다. 단호한 리더의 의견에 무조건 끌려다니기만 하면 독박을 쓸 수 있으니 본인의 핵심 주장은 명확히 어필하세요.</p>
            <hr style='border: 1px dashed #F9E79F; margin: 15px 0;'>
            <p style='font-size: 1.05rem !important; color: #2C3E50; font-weight: bold;'><b>🤝 같이 조 짜면 대박 나는 환상의 파트너:</b></p>
            <p style='font-size: 1rem !important; margin-left: 10px;'>
            • <b>🦅 팩트 독수리:</b> 당신의 등 뒤를 지켜줄 든든한 보디가드! 당신이 정 때문에 빌런들에게 거절하지 못하고 쩔쩔매고 있을 때, 앞에서 칼같이 무임승차를 쳐내고 교통정리를 해줍니다.<br>
            • <b>🦖 폭주 공룡:</b> 최고의 시동 모터! 당신이 방향성을 고민하며 주저하고 있을 때, "가자!"를 외치며 폭발적인 추진력과 기발한 아이디어로 판을 깔아주어 작업을 빠르게 시작하게 만듭니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    elif 4 <= bias_count <= 5:
        st.markdown("""
        <div class='type-container' style='border-color: #D2B4DE;'>
            <div class='character-avatar'>🐰</div>
            <h4>유형 3: 눈치 보며 속앓이하는 감성 요정, '불안 보스 토끼'</h4>
            <p><b>팀플 성향:</b> 유리 같은 투명 멘탈과 따뜻한 정을 가졌습니다. 단톡방이 조용하면 '나 때문에 화났나?' 하고 혼자 소설을 쓰며, 교수의 날 선 피드백 한마디에 하루 종일 당도가 떨어집니다. 조원들의 고생에 감정이입을 너무 많이 합니다.</p>
            <p><b>🧩 추천 역할:</b> <b>[청중의 마음을 훔치는 발표자], [팀 분위기 메이커]</b><br>공감 능력과 표현력이 뛰어나 청중을 설득하는 스토리텔링 발표나, 가라앉은 조원들의 사기를 북돋는 정신적 지주 역할에 강합니다.</p>
            <p><b>⚠️ 타인이 나를 볼 때 주의할 점:</b> '정이 많고 부드러운 사람'이라 다들 좋아하지만, 빌런 조원들의 불쌍한 척 핑계에 마음이 약해져 무임승차를 눈감아주다 결국 혼자 우는 비극의 주인공이 되기 쉽습니다. 팀플은 공과 사를 나누어야 본인의 정신건강을 지킵니다.</p>
            <hr style='border: 1px dashed #D2B4DE; margin: 15px 0;'>
            <p style='font-size: 1.05rem !important; color: #2C3E50; font-weight: bold;'><b>🤝 같이 조 짜면 대박 나는 환상의 파트너:</b></p>
            <p style='font-size: 1rem !important; margin-left: 10px;'>
            • <b>🦅 팩트 독수리:</b> 유리 멘탈인 당신을 위한 완벽한 방호벽! 당신이 "저기.. 혹시.." 하면서 눈치 볼 때, "안 됩니다." 한마디로 가스라이팅과 빌런들의 공격을 차단해 주는 든든한 멘탈 파수꾼입니다.<br>
            • <b>🦫 실무 비버:</b> 든든하고 포근한 마음의 안식처! 당신이 쓸데없는 걱정으로 소설을 쓰며 불안해할 때, 묵묵히 서포트하며 "그거 아니야, 우리 잘하고 있어"라고 이성적인 안도감을 선사합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='type-container' style='border-color: #BB8FCE;'>
            <div class='character-avatar'>🦖</div>
            <h4>유형 4: 다 비켜! 내가 혼자 다 한다, '폭주 공룡(리더렉스)'</h4>
            <p><b>팀플 성향:</b> "답답해서 못 살겠다! 조원 다 잠수 타도 내 솜씨로 캐리해서 A+ 받으면 그만!"을 외치는 마이웨이 초긍정 낙관 몬스터입니다. 직관과 근거 없는 자신감을 사랑하며 위기 속에서 아드레날린을 느낍니다.</p>
            <p><b>🧩 추천 역할:</b> <b>[전쟁터를 이끄는 조장(PM)], [아이디어 파괴자]</b><br>아무도 리더를 안 하려는 헬(Hell) 상황에서 압도적인 추진력으로 판을 짜고, 멱살 잡고 하드캐리해 프로젝트를 기한 내 골인시키는 견인차입니다.</p>
            <p><b>⚠️ 타인이 나를 볼 때 주의할 점:</b> 추진력은 시원시원해 보이지만, 팀원들 눈에는 '조원들의 피드백을 무시하고 혼자 고집 부리며 폭주하는 독재자'로 보일 위험이 큽니다. 잘못된 방향인데도 미련 때문에 밀어붙이다가 다 같이 침몰할 수 있으니 늘 나침반(팀원 의견)을 확인하세요.</p>
            <hr style='border: 1px dashed #BB8FCE; margin: 15px 0;'>
            <p style='font-size: 1.05rem !important; color: #2C3E50; font-weight: bold;'><b>🤝 같이 조 짜면 대박 나는 환상의 파트너:</b></p>
            <p style='font-size: 1rem !important; margin-left: 10px;'>
            • <b>🦫 실무 비버:</b> 폭주하는 공룡을 제어할 유일한 브레이크이자 살림꾼! 당신이 거친 아이디어를 마구 던지면, 현실적으로 실현 가능한 영역만 추려내 정돈된 고퀄리티 작업물로 다듬어 줍니다.<br>
            • <b>🐰 불안 보스 토끼:</b> 당신의 거친 독주에 상처받은 조원들을 달래줄 힐러! 당신이 앞만 보고 달리느라 놓친 팀원들의 스케줄과 마음을 섬세하게 케어해 조가 공중분해되는 것을 막아줍니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 🛠️ 팀플 인지오류 극복 방안 솔루션
    st.markdown("---")
    st.markdown("### 🛠️ 조별과제 '생각의 덫' 탈출 가이드")
    st.markdown("""
    <div class='solution-box'>
        <div class='solution-title'>1. 낙관성 편향 탈출: 무리한 '하드캐리' 전 경고등 켜기</div>
        <div class='solution-desc'>
        "나 혼자 밤새우면 끝나겠지"라는 근거 없는 자신감이 발동할 때, <b>'만약 조원들이 마감 1시간 전까지 잠수를 탄다면 내 학점과 멘탈은 어떻게 꼬이지?'</b>라는 최악의 시나리오를 글로 적어보세요. 리스크가 시각화되면 독박을 자처하기 전에 교수님께 신고하거나 역할을 분담할 냉정함이 생깁니다.
        </div>
    </div>
    <div class='solution-box'>
        <div class='solution-title'>2. 매몰비용 오류 탈출: 밤샘 자료 과감히 손절하기</div>
        <p class='solution-desc'>
        팀원이 고생해서 찾아왔다는 이유로 주제에 안 맞는 슬라이드를 억지로 넣지 마세요. <b>'이 자료가 과연 교수님의 평가 기준에 1점이라도 기여하는가?'</b>만 냉정하게 생각해야 합니다. 과거의 고생(매몰비용)에 발목 잡히면 전체 학점이 감점되는 미래의 더 큰 손해를 보게 됩니다.
        </p>
    </div>
    <div class='solution-box'>
        <div class='solution-title'>3. 가용성 편향 탈출: 단톡방 침묵을 소설로 쓰지 않기</div>
        <p class='solution-desc'>
        단톡방 안읽씹이 이어질 때 에타의 빌런 썰들을 기억하며 '나 왕따 시키나?' 소설을 쓰지 마세요. <b>'내 친한 친구가 이 상황이라면 내가 뭐라고 해줄까?'</b>라고 제3자 시선으로 생각해보면, 그저 다들 시험 기간이거나 알바 중이라는 아주 보편적인 상식적 이유가 보니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 새로운 프로젝트 조 짜러 가기 (다시하기)", use_container_width=True):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
