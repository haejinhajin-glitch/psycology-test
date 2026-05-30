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
    .type-container {
        background-color: #F7FAFC;
        padding: 25px;
        border-radius: 16px;
        border-left: 5px solid #3182CE;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 및 페이지 상태 유지용 시스템 정의
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_selections' not in st.session_state:
    st.session_state.user_selections = {}

# 대학생 맞춤형 상황극 심리학 데이터셋 (총 6문항)
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
    },
    {
        "id": "전망 이론",
        "badge": "💰 장학금 고르기 기로",
        "text": "교내 학술 대회에 입상하여 장학금을 받게 되었습니다. 학생회에서 제시한 다음 두 가지 정산 방식 중 당신은 어떤 것을 수령하시겠습니까?",
        "options": ["확정안: 무조건 현금 50만 원을 즉시 수령한다.", "도박안: 동전을 던져 앞면이 나오면 100만 원을 받고, 뒷면이 나오면 한 푼도 받지 못한다."]
    }
]

# --- 🏠 화면 0: 첫 인트로 페이지 (문구 업그레이드) ---
if st.session_state.step == 0:
    st.write("")
    st.markdown("<div class='main-title'>🧠 생각의 덫(Cognitive Bias) 테스트</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>“나는 얼마나 합리적인 사람일까?”<br><span style='font-size:0.95rem; color:#718096;'>대학생 일상 상황극으로 보는 나의 비합리성 진단</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-container'>
        <p style='line-height: 1.8; color: #4A5568; font-size: 1.05rem; margin: 0; text-align: center;'>
        <b>혹시 자신은 늘 이성적이고 완벽한 선택을 내린다고 자부하시나요?</b> 🤔<br><br>
        심리학과 행동경제학의 수많은 연구에 따르면, 인간의 뇌는 생각보다 자주 치명적인 착각과 시스템 오류에 빠지곤 합니다.<br><br>
        조별 과제 잔혹사부터 축제 티켓 미련까지! 대학생 맞춤형 6가지 일상 상황을 통해<br>
        내 무의식 속에 숨어있는 <b>생각의 함정</b>을 찾아내고, 나의 <b>진짜 합리성 MBTI 유형</b>을 확인해 보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👉 나의 합리성 유형 알아보기 (Start)", use_container_width=True, type="primary"):
        st.session_state.step = 1
        st.rerun()

# --- 📝 화면 1 ~ 6: 1개씩 등장하는 질문 스텝 ---
elif 1 <= st.session_state.step <= 6:
    current_idx = st.session_state.step - 1
    q_data = questions[current_idx]
    
    # 상단 인터랙티브 진행 바
    st.progress(st.session_state.step / 6)
    st.caption(f"Progress: {st.session_state.step} / 6 문항 진행 중")
    
    # 질문 내용 레이아웃
    st.markdown(f"""
    <div class='card-container'>
        <div class='q-badge'>{q_data['badge']}</div>
        <div class='q-text'>{q_data['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 사용자의 선택을 저장할 임시 변수 연동
    user_choice = st.radio("보기 중 하나를 선택하세요:", q_data['options'], index=0, label_visibility="collapsed")
    
    st.write("")
    # 확인을 눌러야 다음 페이지로 전환되도록 설정
    if st.button("선택 완료 및 다음 문항으로 ➡️", use_container_width=True):
        st.session_state.user_selections[q_data['id']] = user_choice
        st.session_state.step += 1
        st.rerun()

# --- 📊 화면 7: 종합 분석 대시보드 (유형 분석 결과 포함) ---
elif st.session_state.step == 7:
    st.markdown("<div class='main-title'>📊 종합 진단 리포트</div>", unsafe_allow_html=True)
    st.write("")
    
    # 4. 심리학적 점수 계산 자동화 알고리즘
    scores = {}
    bias_count = 0  # 몇 개의 편향에 빠졌는지 체크
    
    # Q1 ~ Q6 채점 (편향적 선택 시 100점, 이성적 선택 시 20점)
    if st.session_state.user_selections.get("매몰비용 오류") == "아픈 몸을 이끌고 우비를 쓰고서라도 무조건 축제 현장에 간다.":
        scores["매몰비용 오류"] = 100; bias_count += 1
    else: scores["매몰비용 오류"] = 20
        
    if st.session_state.user_selections.get("결합 오류") == "지수는 평범한 대기업 회사원이면서 동시에 '사회적 기업의 정기 후원자'이다.":
        scores["결합 오류"] = 100; bias_count += 1
    else: scores["결합 오류"] = 20
        
    if st.session_state.user_selections.get("가용성 편향") == "뉴스 메인에 연일 도배되는 '비행기 추락이나 대형 테러 사고'":
        scores["가용성 편향"] = 100; bias_count += 1
    else: scores["가용성 편향"] = 20
        
    if st.session_state.user_selections.get("틀 효과") == "백신 A: 접종 시 학생 100명 중 30명이 무조건 사망하는 백신":
        scores["틀 효과"] = 100; bias_count += 1
    else: scores["틀 효과"] = 20
        
    if st.session_state.user_selections.get("낙관성 편향") == "80% 이상 - 조원들이 버려도 내 하드캐리로 무조건 성공시킨다.":
        scores["낙관성 편향"] = 100; bias_count += 1
    else: scores["낙관성 편향"] = 20

    if st.session_state.user_selections.get("전망 이론") == "동전을 던져 앞면이 나오면 100만 원을 받고, 뒷면이 나오면 한 푼도 받지 못한다.":
        scores["전망 이론(위험 추구)"] = 100; bias_count += 1
    else: scores["전망 이론(위험 회피)"] = 20

    # 육각형 방사형 차트 생성 (Plotly)
    df_result = pd.DataFrame(dict(
        r=list(scores.values()),
        theta=list(scores.keys())
    ))
    fig = px.line_polar(df_result, r='r', theta='theta', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', fillcolor='rgba(245, 158, 11, 0.25)', line_color='#F59E0B', line_width=3)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    final_avg = sum(scores.values()) / 6
    st.markdown(f"<h3 style='text-align:center; margin-bottom: 25px;'>당신의 평균 비합리성 지수: <span style='color:#E53E3E;'>{final_avg:.0f}점</span></h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏹 나의 합리성 행동 유형 (MBTI 스타일 분석)")
    
    # 편향에 걸린 개수(bias_count)에 따라 유형 결정
    if bias_count <= 1:
        st.markdown("""
        <div class='type-container'>
            <h4 style='color:#2B6CB0; margin-top:0;'>🤖 유형 1: 알파고형 이성주의자 (Perfect Rationalist)</h4>
            <p><b>성향 특징:</b> 감정이나 그럴듯한 이야기에 결코 휘둘리지 않으며, 철저히 통계와 기댓값에 의해서만 움직이는 차가운 이성의 소유자입니다.</p>
            <p><b>👍 좋은 점 (장점):</b> 사기를 당할 확률이 0%에 수렴합니다. 주식 투자를 하거나 중대한 결정을 내릴 때 손절을 가장 잘하며, 가성비와 효율을 극대화하여 인생을 설계합니다.</p>
            <p><b>👎 안 좋은 점 (단점):</b> 주변 사람들에게 가끔 '로봇' 같거나 정이 없다는 소리를 들을 수 있습니다. 이야기의 개연성이나 낭만을 즐기기보다 숫자의 본질만 보려 하기 때문에 인간관계에서 따뜻함이 부족해 보일 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 2 <= bias_count <= 3:
        st.markdown("""
        <div class='type-container' style='border-left-color:#319795;'>
            <h4 style='color:#234E52; margin-top:0;'>🧠 유형 2: 균형 잡힌 현실주의자 (Balanced Pragmatist)</h4>
            <p><b>성향 특징:</b> 대다수의 평범한 현대인이 속하는 가장 건강한 유형입니다. 기본적인 논리와 이성을 챙기면서도, 상황에 따라 인간적인 직관을 적절히 활용합니다.</p>
            <p><b>👍 좋은 점 (장점):</b> 상식적이고 합리적인 판단을 내리므로 사회 생활과 팀 프로젝트에서 가장 환영받는 무난하고 든든한 리더 혹은 조원입니다. 지나치게 깐깐하지 않아 타인과의 공감대도 잘 형성합니다.</p>
            <p><b>👎 안 좋은 점 (단점):</b> 결정적인 순간에 자극적인 뉴스 프레임에 흔들리거나, 본전 생각(매몰비용) 때문에 조금 더 끌려다니는 우유부단함이 발생할 수 있습니다. 큰 위기 상황에서는 조금 더 과감한 손절 본능이 필요합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 4 <= bias_count <= 5:
        st.markdown("""
        <div class='type-container' style='border-left-color:#DD6B20;'>
            <h4 style='color:#7B341E; margin-top:0;'>❤️ 유형 3: 감성 충만 직관주의자 (Intuitive Romantic)</h4>
            <p><b>성향 특징:</b> 딱딱한 데이터나 수학적 확률보다는 눈앞의 분위기, 그럴듯한 이야기, 그리고 내 직감과 낭만을 더 신뢰하는 뜨거운 심장의 소유자입니다.</p>
            <p><b>👍 좋은 점 (장점):</b> 공감 능력이 뛰어나고 이야기의 흐름을 잘 읽어 트렌디합니다. 팀플 조장을 맡았을 때 엄청난 긍정 마인드로 팀원들의 사기를 북돋아 주며, 영화나 문학 같은 서사적 콘텐츠에 깊게 몰입합니다.</p>
            <p><b>👎 안 좋은 점 (단점):</b> 마케팅 기업들의 말장난(틀 효과)이나 본전 심리에 속아 충동구매를 가장 많이 하는 유형입니다. 투자나 계약 등 거액이 오가는 비즈니스 상황에서는 반드시 '알파고형' 지인에게 검수를 받아야 안전합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='type-container' style='border-left-color:#E53E3E;'>
            <h4 style='color:#9B2C2C; margin-top:0;'>🔮 유형 4: 생각의 함정 컬렉터 (Bias Collector)</h4>
            <p><b>성향 특징:</b> 인간의 뇌가 빠질 수 있는 모든 생각의 덫에 기쁘게 걸려 넘어진 인간미 100%의 유형입니다. 철저히 직관과 낙관주의로 무장했습니다.</p>
            <p><b>👍 좋은 점 (장점):</b> 회복 탄력성이 엄청나고 세상을 아주 밝고 긍정적으로 봅니다. 아무리 힘든 환경이라도 '내 하드캐리로 성공한다'는 근거 없는 자신감으로 무장해 위기를 정면 돌파하는 파괴력이 있습니다.</p>
            <p><b>👎 안 좋은 점 (단점):</b> 이미 망해가는 프로젝트나 연애를 본전 생각 때문에 붙잡고 고통받기 쉬우며, 통계적 사실을 무시하고 소문만 믿다가 큰 손해를 입을 수 있습니다. 가끔은 한 발짝 물러서서 차가운 지표를 확인하는 습관이 절실합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 데이터 기반 행동 분석 피드백 (이론적 배경)")
    
    # 이론 설명 아코디언 (전망 이론 포함)
    for bias_name, score_value in scores.items():
        status_label = "⚠️ 편향 노출" if score_value == 100 else "✅ 이성적 방어 성공"
        with st.expander(f"{bias_name} : {status_label}"):
            if "매몰비용 오류" in bias_name:
                st.write("**학습 개념:** 이미 지출해 버려 회수가 불가능한 비용(시간, 자원)에 미련을 두어, 판단력이 흐려지고 미래에 더 큰 손실을 초래하는 오류입니다.")
            elif "결합 오류" in bias_name:
                st.write("**학습 개념:** 단독 사건의 발생 확률보다, 여러 조건이 결합된 사건의 발생 확률을 '그럴듯한 시나리오' 때문에 더 높게 착각하는 인지적 왜곡입니다.")
            elif "가용성 편향" in bias_name:
                st.write("**학습 개념:** 실제 발생 빈도와 통계와 무관하게, 내 기억 속에 자극적이고 강렬하게 각인되어 '쉽게 인출되는 정보'를 더 위험하다고 오판하는 심리입니다.")
            elif "틀 효과" in bias_name:
                st.write("**학습 개념:** 문제의 본질은 동일함에도 이를 '이익(생존)' 관점으로 서술하느냐, '손실(사망)' 관점으로 서술하느냐에 따라 선택이 달라지는 심리 효과입니다.")
            elif "낙관성 편향" in bias_name:
                st.write("**학습 개념:** 명확한 지표나 조건이 부재함에도 불구하고, '나에게는 언제나 행운과 긍정적인 결과만 따를 것'이라고 과신하는 경향입니다.")
            elif "전망 이론" in bias_name:
                st.write("**학습 개념:** 대니얼 카너먼의 **전망 이론(Prospect Theory)**에 따르면, 인간은 이익을 얻을 수 있는 상황에서는 확실한 이득을 취하려는 **'위험 회피(Risk Aversion)'** 성향을 보입니다. (즉, 기댓값은 100만 원 반반이나 무조건 50만 원을 받으려는 심리입니다.) 반대로 손실 상황이 오면 도박을 선택하는 특성을 가집니다.")

    st.write("")
    if st.button("🔄 테스트 처음부터 다시 하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
