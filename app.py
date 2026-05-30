import streamlit as st
import pandas as pd
import time
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="조별과제 잔혹사: 나의 팀플 성향 진단", page_icon="📝", layout="centered")

# 2. 세련된 스타일을 위한 CSS (폰트 및 레이아웃 개선)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Gowun+Dodum&display=swap');
    
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #f7f3f9 100%); }
    h1 { font-family: 'Black Han Sans', sans-serif !important; color: #4A235A; text-align: center; margin-bottom: 20px; }
    h3 { font-family: 'Black Han Sans', sans-serif !important; color: #6C3483 !important; }
    .intro-text { font-family: 'Gowun Dodum', sans-serif; text-align: center; color: #5D6D7E; font-size: 1.1rem; line-height: 1.6; margin-bottom: 30px; }
    .q-card { background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .q-badge { background-color: #FEF9E7; color: #7D6608; padding: 6px 16px; border-radius: 30px; font-weight: bold; font-size: 0.9rem; display: inline-block; margin-bottom: 10px; border: 1px solid #F9E79F; }
    .type-container { background-color: #ffffff; padding: 30px; border-radius: 20px; border: 2px solid #BB8FCE; margin-bottom: 25px; box-shadow: 0px 4px 12px rgba(187, 143, 206, 0.1); }
    .solution-box { background-color: #ffffff; padding: 24px; border-radius: 16px; margin-bottom: 18px; border-left: 6px solid #BB8FCE; border: 1px solid #EAECEE; box-shadow: 0px 4px 10px rgba(0,0,0,0.02); }
    .stButton>button { width: 100%; border-radius: 50px !important; height: 3rem !important; font-weight: bold; background: #6C3483 !important; color: white !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 질문 및 점수 데이터
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

# 4. 앱 로직
if 'step' not in st.session_state: st.session_state.step = 0
if 'results' not in st.session_state: st.session_state.results = {}
if 'scores' not in st.session_state: st.session_state.scores = {}

if st.session_state.step == 0:
    st.markdown("<h1>👥 조별과제 잔혹사</h1>", unsafe_allow_html=True)
    st.markdown("<p class='intro-text'>현실적인 팀플 돌발 상황들로 정밀하게 파악해보는<br>나의 인지 편향 지수 테스트</p>", unsafe_allow_html=True)
    if st.button("👉 나의 팀플 성향 진단 시작하기"):
        st.session_state.step = 1; st.rerun()

elif 1 <= st.session_state.step <= 6:
    q = questions[st.session_state.step - 1]
    st.progress(st.session_state.step / 6)
    st.markdown(f"""
        <div class='q-card'>
            <div class='q-badge'>{q['badge']}</div>
            <div style='font-size: 1.2rem; font-weight: bold;'>{q['text']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    choice = st.radio("선택지:", list(q['options'].keys()), label_visibility="collapsed")
    if st.button("답변 선택 완료 ➡️"):
        st.session_state.scores[q['id']] = q['options'][choice]
        st.session_state.step += 1; st.rerun()

elif st.session_state.step == 7:
    with st.spinner('당신의 팀플 DNA 분석 중...'):
        time.sleep(1.5)
        st.balloons()
    
    st.markdown("<h1>📊 팀플 인지오류 진단 결과</h1>", unsafe_allow_html=True)
    bias_count = sum(1 for s in st.session_state.scores.values() if s == 100)
    
    # 레이더 차트
    df = pd.DataFrame({'측정 항목': st.session_state.scores.keys(), '점수': st.session_state.scores.values()})
    fig = px.line_polar(df, r='점수', theta='측정 항목', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', fillcolor='rgba(187, 143, 206, 0.2)', line_color='#BB8FCE')
    st.plotly_chart(fig, use_container_width=True)

    # 유형별 상세 결과 (내용 유지)
    if bias_count <= 1:
        st.markdown("<div class='type-container'><h4>🦅 유형 1: 팩트 독수리</h4><p>감정에 휘둘리지 않고 철저히 효율과 데이터로 움직입니다. 조원들이 잠수를 타면 상처받지 않고 칼같이 대처하는 냉철한 영웅입니다.</p></div>", unsafe_allow_html=True)
    elif 2 <= bias_count <= 3:
        st.markdown("<div class='type-container'><h4>🦫 유형 2: 실무 비버</h4><p>묵묵히 제 몫을 다하는 평화주의자입니다. 가끔 미련을 두기도 하지만, 상황에 맞춰 실질적인 결과물을 빌딩해 나갑니다.</p></div>", unsafe_allow_html=True)
    elif 4 <= bias_count <= 5:
        st.markdown("<div class='type-container'><h4>🐰 유형 3: 불안 보스 토끼</h4><p>유리 멘탈과 따뜻한 정을 가진 감성 요정입니다. 조원들의 상황에 감정이입을 너무 많이 하여 속앓이를 자주 합니다.</p></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='type-container'><h4>🦖 유형 4: 폭주 공룡</h4><p>답답해서 못 살겠다! 혼자서라도 캐리해서 A+를 받겠다는 마이웨이 초긍정 낙관 몬스터입니다.</p></div>", unsafe_allow_html=True)

    # 솔루션 가이드 유지
    st.markdown("### 🛠️ 조별과제 '생각의 덫' 탈출 가이드")
    st.markdown("<div class='solution-box'><b>1. 낙관성 편향:</b> 나 혼자 밤새우면 끝난다는 생각을 버리고 최악의 시나리오를 대비하세요.</div>", unsafe_allow_html=True)
    st.markdown("<div class='solution-box'><b>2. 매몰비용 오류:</b> 과감하게 버려야 전체 학점을 살릴 수 있습니다.</div>", unsafe_allow_html=True)
    st.markdown("<div class='solution-box'><b>3. 가용성 편향:</b> 단톡방 침묵으로 혼자 소설 쓰지 마세요.</div>", unsafe_allow_html=True)
    
    if st.button("🔄 테스트 다시 하기"):
        st.session_state.step = 0; st.session_state.scores = {}; st.rerun()
