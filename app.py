import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="일상의 선택 & 합리성 진단", page_icon="🧠", layout="centered")

# 2. UI 디자인 및 폰트 크기 확대 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.06);
        margin-bottom: 25px;
        border: 1px solid #eef2f6;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #1A365D;
        margin-bottom: 12px;
    }
    .sub-title {
        font-size: 1.3rem;
        text-align: center;
        color: #4A5568;
        margin-bottom: 35px;
        font-weight: 500;
    }
    .q-badge {
        background-color: #FFF5F5;
        color: #C53030;
        padding: 6px 14px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.05rem;
        display: inline-block;
        margin-bottom: 15px;
    }
    .q-text {
        font-size: 1.45rem;
        font-weight: 700;
        color: #2D3748;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .type-container {
        background-color: #F7FAFC;
        padding: 28px;
        border-radius: 16px;
        border-left: 5px solid #3182CE;
        margin-bottom: 25px;
    }
    .type-container h4 {
        font-size: 1.4rem !important;
        font-weight: 700;
        margin-bottom: 15px;
    }
    .type-container p {
        font-size: 1.15rem !important;
        line-height: 1.7;
        color: #2D3748;
        margin-bottom: 10px;
    }
    
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.2rem !important;
        line-height: 1.6;
    }
    
    .solution-box {
        background-color: #F8FAFC;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 18px;
        border: 1px solid #E2E8F0;
    }
    .solution-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2C5282;
        margin-bottom: 10px;
    }
    .solution-desc {
        font-size: 1.15rem !important;
        color: #4A5568;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_selections' not in st.session_state:
    st.session_state.user_selections = {}

# 일상 체감형 공감 데이터셋
questions = [
    {
        "id": "낙관성 편향",
        "badge": "👥 조별과제 잔혹사",
        "text": "팀 프로젝트에서 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 줍니다. 속이 타들어 가는 상황, 당신의 무의식적 생각은 어느 쪽에 가깝나요?",
        "options": ["'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.", "'조원들이 안 도와주면 현실적으로 한계가 있지.' 마음을 비우고 상황에 맞춰 타협한다."]
    },
    {
        "id": "가용성 편향",
        "badge": "💬 단톡방의 침묵과 오해",
        "text": "최근 친구와 가벼운 말다툼이 있은 후, 오랜만에 단톡방에 말을 뱉었는데 아무도 답장을 안 하고 읽씹이 이어집니다. 이때 밀려오는 생각은?",
        "options": ["'혹시 그때 내가 한 말 때문에 다들 나한테 서운해서 일부러 씹나?' 하고 과거의 특정 기억을 떠올리며 불안해한다.", "'다들 그냥 우연히 타이밍이 겹쳐서 바쁘거나 카톡을 못 본 거겠지' 하고 대수롭지 않게 넘긴다."]
    },
    {
        "id": "매몰비용 오류",
        "badge": "💸 쓰지 않는 구독과 미련 소비",
        "text": "매달 자동으로 15,000원씩 결제되지만 지난 세 달 동안 한 번도 켜지 않은 OTT(넷플릭스 등) 구독권이 있습니다. 해지하려니 괜히 망설여지는데, 그 이유는?",
        "options": ["'언젠가는 볼 텐데 지금 해지하면 손해 같고, 그동안 낸 돈이 아까워서' 일단 유지한다.", "'어차피 지난 석 달 안 봤으면 앞으로도 안 본다.' 이미 날린 돈은 잊고 즉시 해지한다."]
    },
    {
        "id": "틀 효과",
        "badge": "💼 알바/직장 사장님의 한마디",
        "text": "아르바이트나 직장에서 근무 중입니다. 사장님이 다가와 내 업무 결과에 대해 피드백을 주는데, 당신의 멘탈을 더 흔드는 말은 무엇인가요?",
        "options": ["'A 방식: 자네가 올린 기획안은 반려될 확률이 30%나 되네.' (부정적 실패율 강조)", "'B 방식: 자네가 올린 기획안은 통과될 확률이 70%나 되네.' (긍정적 성공률 강조)"]
    },
    {
        "id": "결합 오류",
        "badge": "🔎 SNS 속 완벽한 인플루언서",
        "text": "내 피드에 자주 뜨는 대학 동창은 매일 명품을 인증하고, 화려한 파티에 가며, 인생이 늘 행복해 보입니다. 이 친구의 실제 삶으로 '확률상' 더 맞는 모습은 어느 쪽일까요?",
        "options": ["겉은 화려해 보여도 남들과 똑같이 취업 스트레스와 남모를 불안을 겪는 평범한 사람이다.", "부유한 집안 환경을 가졌으면서, 동시에 성격도 모난 곳 없이 늘 행복감만 느끼는 완벽한 사람이다."]
    },
    {
        "id": "전망 이론",
        "badge": "💰 소소한 보상 고르기",
        "text": "이벤트에 당첨되어 보상을 고를 수 있게 되었습니다. 당신의 심리를 가장 자극하는 정산 방식은 무엇인가요?",
        "options": ["안정형: 조건 없이 무조건 현금 20만 원을 즉시 수령한다.", "도박형: 동전을 던져 앞면이 나오면 50만 원을 받고, 뒷면이 나오면 한 푼도 받지 못한다."]
    }
]

# --- 🏠 화면 0: 첫 인트로 페이지 ---
if st.session_state.step == 0:
    st.write("")
    st.markdown("<div class='main-title'>🎯 일상 행동 및 선택 경향 테스트</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>“나는 평소에 얼마나 현명한 선택을 내릴까?”<br><span style='font-size:1.05rem; color:#718096;'>조별과제, 단톡방, 소비 습관으로 알아보는 나의 멘탈과 행동 유형</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-container'>
        <p style='line-height: 1.9; color: #4A5568; font-size: 1.2rem; margin: 0; text-align: center;'>
        <b>조별 과제 잔혹사부터 단톡방 안 읽씹, 아까워서 못 끊는 구독 서비스까지!</b> 🤦‍♂️<br><br>
        우리는 일상 속에서 매 순간 최선의 선택을 내린다고 생각하지만,<br>
        사실 무의식적인 감정과 착각, '생각의 덫'에 걸려 스스로 스트레스를 키우곤 합니다.<br><br>
        주변에서 흔히 겪는 6가지 현실 공감 상황을 통해,<br>
        내가 일상에서 어떤 유형으로 행동하고 대처하는지 대시보드로 확인해 보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👉 나의 일상 행동 유형 알아보기 (Start)", use_container_width=True, type="primary"):
        st.session_state.step = 1
        st.rerun()

# --- 📝 화면 1 ~ 6: 질문 스텝 ---
elif 1 <= st.session_state.step <= 6:
    current_idx = st.session_state.step - 1
    q_data = questions[current_idx]
    
    st.progress(st.session_state.step / 6)
    st.caption(f"Progress: {st.session_state.step} / 6 문항 진행 중")
    
    st.markdown(f"""
    <div class='card-container'>
        <div class='q-badge'>{q_data['badge']}</div>
        <div class='q-text'>{q_data['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_choice = st.radio("보기 중 하나를 선택하세요:", q_data['options'], index=0, label_visibility="collapsed")
    
    st.write("")
    if st.button("선택 완료 및 다음 문항으로 ➡️", use_container_width=True):
        st.session_state.user_selections[q_data['id']] = user_choice
        st.session_state.step += 1
        st.rerun()

# --- 📊 화면 7: 종합 분석 대시보드 ---
elif st.session_state.step == 7:
    st.markdown("<div class='main-title'>📊 나의 일상 진단 리포트</div>", unsafe_allow_html=True)
    st.write("")
    
    scores = {}
    bias_count = 0
    
    if st.session_state.user_selections.get("낙관성 편향") == "'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.":
        scores["조별과제 과신 지수"] = 100; bias_count += 1
    else: scores["조별과제 과신 지수"] = 20
        
    if st.session_state.user_selections.get("가용성 편향") == "'혹시 그때 내가 한 말 때문에 다들 나한테 서운해서 일부러 씹나?' 하고 과거의 특정 기억을 떠올리며 불안해한다.":
        scores["인간관계 예민도"] = 100; bias_count += 1
    else: scores["인간관계 예민도"] = 20
        
    if st.session_state.user_selections.get("매몰비용 오류") == "'언젠가는 볼 텐데 지금 해지하면 손해 같고, 그동안 낸 돈이 아까워서' 일단 유지한다.":
        scores["소비 미련 지수"] = 100; bias_count += 1
    else: scores["소비 미련 지수"] = 20
        
    if st.session_state.user_selections.get("틀 효과") == "'A 방식: 자네가 올린 기획안은 반려될 확률이 30%나 되네.' (부정적 실패율 강조)":
        scores["말장난 프레임 취약도"] = 100; bias_count += 1
    else: scores["말장난 프레임 취약도"] = 20
        
    if st.session_state.user_selections.get("결합 오류") == "부유한 집안 환경을 가졌으면서, 동시에 성격도 모난 곳 없이 늘 행복감만 느끼는 완벽한 사람이다.":
        scores["SNS 필터링 왜곡도"] = 100; bias_count += 1
    else: scores["SNS 필터링 왜곡도"] = 20

    if st.session_state.user_selections.get("전망 이론") == "동전을 던져 앞면이 나오면 50만 원을 받고, 뒷면이 나오면 한 푼도 받지 못한다.":
        scores["리스크 추구 성향"] = 100; bias_count += 1
    else: scores["리스크 회피 성향"] = 20

    df_result = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
    fig = px.line_polar(df_result, r='r', theta='theta', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', fillcolor='rgba(59, 130, 246, 0.25)', line_color='#3B82F6', line_width=3)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    final_avg = sum(scores.values()) / 6
    st.markdown(f"<h2 style='text-align:center; margin-bottom: 25px;'>나의 일상 비합리성 지수: <span style='color:#E53E3E;'>{final_avg:.0f}점</span></h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏹 나의 합리성 행동 유형")
    
    # 💡 각 유형별 [추천 역할] 및 [주주의할 점] 섹션 대폭 강화
    if bias_count <= 1:
        st.markdown("""
        <div class='type-container'>
            <h4 style='color:#2B6CB0; margin-top:0;'>🤖 유형 1: 냉철한 팩트주의 셜록 (Fact Bomber)</h4>
            <p><b>성향 특징:</b> 감정이나 그럴듯한 핑계에 휘둘리지 않으며, 철저히 통계와 이성에 의해서만 움직이는 소유자입니다. 단톡방 읽씹이나 사소한 서운함에 에너지를 쓰지 않는 강철 멘탈을 가졌습니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[자료조사 및 데이터 분석가], [최종 검수 담당]</b><br>정보의 사실 유무를 판단하고, 잘못된 논리나 오탈자를 귀신같이 찾아내는 피드백 역할에 최적화되어 있습니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 타인에게 가끔 '차가운 로봇' 같거나 공감 능력이 부족하다는 인상을 줄 수 있습니다. 조원들의 피치 못할 사정이나 인간적인 감정 교류를 수치로만 판단하려다 묘한 갈등이 생길 수 있으니 약간의 유연함이 필요합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 2 <= bias_count <= 3:
        st.markdown("""
        <div class='type-container' style='border-left-color:#319795;'>
            <h4 style='color:#234E52; margin-top:0;'>🧠 유형 2: 유연한 현실주의 실무자 (Pragmatic Realist)</h4>
            <p><b>성향 특징:</b> 대다수의 평범한 사람들이 속하는 가장 건강한 밸런스 캐릭터입니다. 기본적인 논리와 이성을 유지하면서도, 상황에 따라 팀원들의 인간적인 직관이나 분위기를 적절히 맞출 줄 압니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[중간 조율자(커뮤니케이터)], [실무 기획 및 작성]</b><br>한쪽으로 치우치지 않는 상식적인 시선을 가졌기 때문에, 의견이 대립할 때 합리적인 타협안을 제시하며 실질적인 결과물을 만들어내는 데 능숙합니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 주변 사람들에게 '든든하고 무난한 사람'이라는 평을 듣지만, 결정적인 순간에 분위기나 본전 심리에 휩쓸려 우유부단해질 때가 있습니다. 손해를 보면서도 착한 아이 콤플렉스 때문에 리더의 의견에 끌려다니지 않도록 맺고 끊음을 명확히 하세요.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 4 <= bias_count <= 5:
        st.markdown("""
        <div class='type-container' style='border-left-color:#DD6B20;'>
            <h4 style='color:#7B341E; margin-top:0;'>❤️ 유형 3: 감성 과몰입 서포터 (Emotional Supporter)</h4>
            <p><b>성향 특징:</b> 딱딱한 데이터보다는 눈앞의 분위기, 내 직감과 인간관계를 더 신뢰하는 따뜻한 심장의 소유자입니다. 단톡방 침묵이나 사장님의 지적 한마디에 생각의 꼬리를 물며 오해를 키우기 쉽습니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[발표자], [팀 분위기 메이커(동기부여가)]</b><br>공감 능력이 뛰어나고 스토리텔링 재능이 있어 청중의 마음을 움직이는 발표나, 갈등이 생긴 팀원들의 마음을 다독여 다시 뭉치게 만드는 서포트 역할에 뛰어납니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 주변에서 '정이 많고 같이 있으면 편안한 사람'으로 통하지만, 정과 미련 때문에 조원들의 잠수를 눈감아 주다가 혼자 총대를 메고 독박을 쓸 위험이 매우 큽니다. 타인의 평가나 거절에 너무 상처받지 않도록 마인드 컨트롤이 필요합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='type-container' style='border-left-color:#E53E3E;'>
            <h4 style='color:#9B2C2C; margin-top:0;'>🔮 유형 4: 폭풍 직관의 프로 총대러 (Hyper Intuitive)</h4>
            <p><b>성향 특징:</b> "조원들이 안 도와줘도 내가 주말에 밤새 캐리하면 돼!"라는 강력한 추진력과 초긍정 낙관주의로 똘똘 뭉친 유형입니다. 리스크를 두려워하지 않고 직관적인 판단을 즐깁니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[조장(PM)], [아이디어 브레인스토머]</b><br>아무도 선뜻 나서지 않는 위기 상황에서 강력한 리더십으로 판을 짜고, 번뜩이는 창의적 아이디어로 프로젝트의 방향성을 제시하는 시동 장치 역할을 잘 해냅니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 추진력이 시원시원해 보이지만, 주변 사람 눈에는 '혼자 고집 부리며 폭주하는 사람' 혹은 '대책 없는 근거 없는 자신감'으로 비춰질 수 있습니다. 무너진 관계나 실패한 계획을 미련 때문에 붙잡고 있다가 스스로 고통을 키울 수 있으니 항상 플랜B를 염두에 두어야 합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    # 🛠️ 일상 속 비합리성 극복 방법 솔루션 대시보드
    st.markdown("---")
    st.markdown("### 🛠️ 일상에서 실천하는 스트레스 & 선택 장애 극복법")
    st.markdown("""
    <div class='solution-box'>
        <div class='solution-title'>1. 관계와 단톡방에서 '나' 분리하기 (자기 이격)</div>
        <div class='solution-desc'>
        카톡 읽씹이나 타인의 반응에 심장이 쿵쾅거릴 때는 <b>'내 친구가 이 상황이라면 내가 뭐라고 해줄까?'</b>라고 삼인칭으로 생각해 보세요. 주관적인 불안 프레임이 걷히고 '그냥 바쁜가 보다' 하는 객관적인 팩트가 보입니다.
        </div>
    </div>
    <div class='solution-box'>
        <div class='solution-title'>2. 매몰비용 손절 기준 만들기 (구독/소비 브레이크)</div>
        <p class='solution-desc'>
        "아까워서" 붙잡고 있는 옷, 물건, 인간관계가 있다면 <b>'최근 3달 동안 나에게 긍정적인 가치를 줬는가?'</b>라는 명확한 기준을 적용해 보세요. 기준을 넘지 못했다면 미래의 기회비용을 위해 과감히 해지하거나 정리하는 것이 훨씬 이득입니다.
        </p>
    </div>
    <div class='solution-box'>
        <div class='solution-title'>3. 조별과제나 일할 때 '최악의 시나리오' 먼저 적기</div>
        <p class='solution-desc'>
        근거 없는 자신감으로 총대를 메기 전에, <b>'조원들이 끝까지 잠수타면 내 학점과 일정은 어떻게 되지?'</b>라는 최악의 상황을 먼저 글로 적어보세요. 시각화된 리스크를 보면 무리한 하드캐리를 멈추고 냉정하게 역할을 분담할 용기가 생깁니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 테스트 처음부터 다시 하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
