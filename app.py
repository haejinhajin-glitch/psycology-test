import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정 (모바일/웹 반응형 최적화)
st.set_page_config(page_title="합리성 진단 테스트", page_icon="🧠", layout="centered")

# 2. 전문적인 심리테스트 서비스 느낌의 고급 UI 디자인 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    /* 인트로 및 질문 카드 스타일 */
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.06);
        margin-bottom: 25px;
        border: 1px solid #eef2f6;
    }
    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        text-align: center;
        color: #1A365D;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 1.15rem;
        text-align: center;
        color: #4A5568;
        margin-bottom: 35px;
    }
    .q-badge {
        background-color: #EBF8FF;
        color: #2B6CB0;
        padding: 6px 14px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 15px;
    }
    .q-text {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2D3748;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 및 페이지 상태 유지용 시스템 정의
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_selections' not in st.session_state:
    st.session_state.user_selections = {}

# 대학생 맞춤형 상황극 심리학 데이터셋
questions = [
    {
        "id": "매몰비용 오류",
        "badge": "🎵 무대의 미련",
        "text": "밤새 대기 타서 겨우 예매한 5만 원짜리 축제 티켓이 있습니다. 그런데 당일 기습적인 폭우가 쏟아지고 몸살 기운이 심해 침대에서 인어처럼 늘어져 있습니다. 가봤자 고생길이 훤한 상황, 당신의 선택은?",
        "options": ["아픈 몸을 이끌고 우비를 쓰고서라도 무조건 축제 현장에 간다.", "5만 원은 이미 날린 셈 치고, 따뜻한 방에서 안전하게 쉰다."]
    },
    {
        "id": "결합 오류",
        "badge": "🏫 과대표의 비밀",
        "text": "우리 과대표 '지수'는 리더십이 뛰어나며, 발표 수업 때마다 사회적 불평등과 정의에 대해 열변을 토하곤 합니다. 졸업 후 현재 지수의 모습으로 '통계적 확률'이 더 높은 것은 어느 쪽일까요?",
        "options": ["지수는 평범한 대기업 회사원이다.", "지수는 평범한 대기업 회사원이면서 동시에 '사회적 기업의 정기 후원자'이다."]
    },
    {
        "id": "가용성 편향",
        "badge": "✈️ 머릿속의 공포",
        "text": "상담심리 센터로 이동하는 도중 문득 불안감이 밀려옵니다. 다음 중 통계적인 통계 분석상 '내가 실제로 1년 동안 겪을 확률'이 가장 높은 위험은 무엇일까요?",
        "options": ["뉴스 메인에 연일 도배되는 '비행기 추락이나 대형 테러 사고'", "뉴스에는 거의 나오지 않는 '계단이나 미끄러운 빙판길에서 넘어지는 낙상 사고'"]
    },
    {
        "id": "틀 효과",
        "badge": "💊 방역 책임자의 결단",
        "text": "캠퍼스 내에 치명적인 바이러스가 유행하여 당신이 방역 최고책임자가 되었습니다. 학생들을 지키기 위해 단 하나의 백신만 즉시 도입할 수 있다면 무엇을 고르시겠습니까?",
        "options": ["백신 A: 접종 시 학생 100명 중 30명이 무조건 사망하는 백신", "백신 B: 접종 시 학생 100명 중 70명이 무조건 생존하는 백신"]
    },
    {
        "id": "낙관성 편향",
        "badge": "📈 팀플 조장의 근거 없는 자신감",
        "text": "이번 학기 학점 빌런들을 만나 어쩌다 보니 독박 조장이 되었습니다. 내가 학과 내의 다른 '평균적인 조장들'보다 이 난관을 극복하고 완벽한 에이플(A+)을 받아낼 확률은 얼마나 될까요?",
        "options": ["80% 이상 - 조원들이 버려도 내 하드캐리로 무조건 성공시킨다.", "50% 내외 - 다른 조장들과 비슷하게 상황에 따라 평범한 학점을 받을 것이다."]
    }
]

# --- 🏠 화면 0: 첫 인트로 페이지 ---
if st.session_state.step == 0:
    st.write("")
    st.markdown("<div class='main-title'>🧠 생각의 덫(Cognitive Bias) 테스트</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>대학생 일상 상황극으로 보는 나의 비합리성 진단</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-container'>
        <p style='line-height: 1.8; color: #4A5568; font-size: 1.05rem; margin: 0;'>
        우리는 스스로가 늘 합리적이고 논리적인 판단을 내린다고 믿습니다. 하지만 심리학 연구에 따르면, 
        인간의 뇌는 생각보다 자주 치명적인 인지적 오류에 빠지곤 합니다.<br><br>
        본 어플리케이션은 <b>심리학개론</b> 교재에 등장하는 5가지 핵심 인지 편향 이론을 기반으로 제작되었습니다. 
        단 5개의 일상적인 질문을 통해 내가 어떤 생각의 함정에 취약한지 실시간 대시보드로 분석해 보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👉 나의 합리성 테스트 시작하기", use_container_width=True, type="primary"):
        st.session_state.step = 1
        st.rerun()

# --- 📝 화면 1 ~ 5: 1개씩 등장하는 질문 스텝 ---
elif 1 <= st.session_state.step <= 5:
    current_idx = st.session_state.step - 1
    q_data = questions[current_idx]
    
    # 상단 인터랙티브 진행 바
    st.progress(st.session_state.step / 5)
    st.caption(f"Progress: {st.session_state.step} / 5 문항 진행 중")
    
    # 질문 내용 레이아웃
    st.markdown(f"""
    <div class='card-container'>
        <div class='q-badge'>{q_data['badge']}</div>
        <div class='q-text'>{q_data['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 사용자의 선택을 저장할 임시 변수 연동
    default_choice = q_data['options'][0]
    user_choice = st.radio("보기 중 하나를 선택하세요:", q_data['options'], index=0, label_visibility="collapsed")
    
    st.write("")
    # 확인을 눌러야 다음 페이지로 전환되도록 설정
    if st.button("선택 완료 및 다음 문항으로 ➡️", use_container_width=True):
        st.session_state.user_selections[q_data['id']] = user_choice
        st.session_state.step += 1
        st.rerun()

# --- 📊 화면 6: 종합 분석 대시보드 (마지막 결과 페이지) ---
elif st.session_state.step == 6:
    st.markdown("<div class='main-title'>📊 종합 진단 리포트</div>", unsafe_allow_html=True)
    st.write("")
    
    # 4. 심리학적 점수 계산 자동화 알고리즘
    scores = {}
    
    # Q1. 매몰비용 오류
    if st.session_state.user_selections.get("매몰비용 오류") == "아픈 몸을 이끌고 우비를 쓰고서라도 무조건 축제 현장에 간다.":
        scores["매몰비용 오류"] = 100
    else: scores["매몰비용 오류"] = 20
        
    # Q2. 결합 오류
    if st.session_state.user_selections.get("결합 오류") == "지수는 대기업 회사원이면서 사회적 기업의 후원자이다.":
        scores["결합 오류"] = 100
    else: scores["결합 오류"] = 20
        
    # Q3. 가용성 편향
    if st.session_state.user_selections.get("가용성 편향") == "뉴스 메인에 연일 도배되는 '비행기 추락이나 대형 테러 사고'":
        scores["가용성 편향"] = 100
    else: scores["가용성 편향"] = 20
        
    # Q4. 틀 효과
    if st.session_state.user_selections.get("틀 효과") == "백신 A: 접종 시 학생 100명 중 30명이 무조건 사망하는 백신":
        scores["틀 효과"] = 100
    else: scores["틀 효과"] = 20
        
    # Q5. 낙관성 편향
    if st.session_state.user_selections.get("낙관성 편향") == "80% 이상 - 조원들이 버려도 내 하드캐리로 무조건 성공시킨다.":
        scores["낙관성 편향"] = 100
    else: scores["낙관성 편향"] = 20

    # 5. 오각형 방사형 차트 데이터 전처리 및 생성 (Plotly)
    df_result = pd.DataFrame(dict(
        r=list(scores.values()),
        theta=list(scores.keys())
    ))
    fig = px.line_polar(df_result, r='r', theta='theta', line_close=True, range_r=[0,100])
    fig.update_traces(fill='subsection', fillcolor='rgba(74, 144, 226, 0.25)', line_color='#3182CE', line_width=3)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    
    # 화면에 그래프 렌더링
    st.plotly_chart(fig, use_container_width=True)
    
    # 평균 점수에 기반한 최종 타이틀 출력
    final_avg = sum(scores.values()) / 5
    st.markdown(f"<h3 style='text-align:center; margin-bottom: 25px;'>당신의 평균 비합리성 지수: <span style='color:#E53E3E;'>{final_avg:.0f}점</span></h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🔍 데이터 기반 행동 분석 피드백")
    
    # 상세 내용 아코디언 컴포넌트 출력
    for bias_name, score_value in scores.items():
        status_label = "⚠️ 편향 노출" if score_value == 100 else "✅ 이성적 방어 성공"
        with st.expander(f"{bias_name} : {status_label}"):
            if bias_name == "매몰비용 오류":
                st.write("**학습 개념:** 이미 지출해 버려 회수가 불가능한 비용(시간, 자원)에 미련을 두어, 판단력이 흐려지고 미래에 더 큰 손실을 초래하는 오류입니다.")
                st.write("👉 *당신의 상태:* 본전 생각에 고통스러운 환경을 자처하는 편이시군요! '손절'도 훌륭한 전략임을 인지해야 합니다.")
            elif bias_name == "결합 오류":
                st.write("**학습 개념:** 단독 사건의 발생 확률보다, 여러 조건이 결합된 사건의 발생 확률을 '그럴듯한 시나리오' 때문에 더 높게 착각하는 인지적 왜곡입니다.")
                st.write("👉 *당신의 상태:* 이야기의 개연성에 속아 수학적 확률을 무시하셨습니다. 결합 사건은 단독 사건의 교집합이므로 확률이 무조건 더 낮습니다!")
            elif bias_name == "가용성 편향":
                st.write("**학습 개념:** 실제 발생 빈도와 통계와 무관하게, 내 기억 속에 자극적이고 강렬하게 각인되어 '쉽게 인출되는 정보'를 더 위험하다고 오판하는 심리입니다.")
                st.write("👉 *당신의 상태:* 미디어가 만든 자극적 프레임에 취약합니다. 직관보다 객관적인 지표를 신뢰하는 훈련이 필요합니다.")
            elif bias_name == "틀 효과":
                st.write("**학습 개념:** 문제의 본질은 동일함에도 이를 '이익(생존)' 관점으로 서술하느냐, '손실(사망)' 관점으로 서술하느냐에 따라 선택이 달라지는 심리 효과입니다.")
                st.write("👉 *당신의 상태:* '30명 사망'이라는 부정적 워딩에 동요되어 비합리적인 결정을 유도당하셨습니다. 프레임을 벗어나 숫자의 본질을 보는 눈을 기르세요.")
            elif bias_name == "낙관성 편향":
                st.write("**학습 개념:** 명확한 지표나 조건이 부재함에도 불구하고, '나에게는 언제나 행운과 긍정적인 결과만 따를 것'이라고 과신하는 경향입니다.")
                st.write("👉 *당신의 상태:* 팀플 조장으로서 지나친 캐리형 인물입니다. 근거 없는 낙관보다는 최악의 상황을 대비한 플랜B가 안전합니다.")

    st.write("")
    if st.button("🔄 테스트 처음부터 다시 하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
