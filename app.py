import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정 및 반응형 최적화
st.set_page_config(page_title="말랑말랑 일상 선택 & 비합리성 진단", page_icon="🧠", layout="centered")

# 2. 아기자기하고 귀여운 파스텔톤 일상 UI 디자인 (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=400;500;700&display=swap');
    * { font-family: 'Noto Sans KR', sans-serif; }
    
    .stApp {
        background-color: #FDFBF7;
    }
    
    .card-container {
        background-color: #ffffff;
        padding: 35px;
        border-radius: 28px;
        box-shadow: 0px 10px 25px rgba(229, 220, 203, 0.4);
        margin-bottom: 25px;
        border: 2px solid #F3EFE0;
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #4A3E3D;
        margin-bottom: 12px;
    }
    .sub-title {
        font-size: 1.3rem;
        text-align: center;
        color: #8A7E72;
        margin-bottom: 35px;
        font-weight: 500;
    }
    
    .q-badge {
        background-color: #FFF0F5;
        color: #FF6B8B;
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1.05rem;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px dashed #FFB6C1;
    }
    .q-text {
        font-size: 1.45rem;
        font-weight: 700;
        color: #4A3E3D;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    
    .type-container {
        background-color: #FAFAFA;
        padding: 30px;
        border-radius: 24px;
        border: 2px solid #E2E8F0;
        margin-bottom: 25px;
    }
    .character-avatar {
        font-size: 3.5rem;
        text-align: center;
        margin-bottom: 10px;
    }
    .type-container h4 {
        font-size: 1.4rem !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 20px;
    }
    .type-container p {
        font-size: 1.15rem !important;
        line-height: 1.7;
        color: #554A42;
        margin-bottom: 12px;
    }
    
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.25rem !important;
        color: #554A42;
        line-height: 1.6;
    }
    
    .solution-box {
        background-color: #FFFDF9;
        padding: 24px;
        border-radius: 20px;
        margin-bottom: 18px;
        border: 2px solid #F5EBE6;
    }
    .solution-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #D97706;
        margin-bottom: 10px;
    }
    .solution-desc {
        font-size: 1.15rem !important;
        color: #6B5E53;
        line-height: 1.7;
    }
    
    .stButton>button {
        border-radius: 50px !important;
        font-size: 1.15rem !important;
        padding: 10px 25px !important;
        background-color: #FF8A8A !important;
        color: white !important;
        border: none !important;
        box-shadow: 0px 4px 10px rgba(255, 138, 138, 0.3) !important;
    }
    .stButton>button:hover {
        background-color: #FF6B6B !important;
        transform: scale(1.02);
        transition: all 0.2s;
    }
    </style>
""", unsafe_allow_html=True)

if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_selections' not in st.session_state:
    st.session_state.user_selections = {}

# 일상 상황 속 심리 이론 질문 데이터셋 (배지는 귀여운 스타일 유지)
questions = [
    {
        "id": "낙관성 편향",
        "badge": "🦖 조별과제 잔혹사",
        "text": "팀 프로젝트에서 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 줍니다. 속이 타들어 가는 상황, 당신의 무의식적 생각은 어느 쪽에 가깝나요?",
        "options": ["'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.", "'조원들이 안 도와주면 현실적으로 한계가 있지.' 마음을 비우고 상황에 맞춰 타협한다."]
    },
    {
        "id": "가용성 편향",
        "badge": "💬 단톡방 침묵의 소심이",
        "text": "최근 친구와 가벼운 말다툼이 있은 후, 오랜만에 단톡방에 말을 뱉었는데 아무도 답장을 안 하고 읽씹이 이어집니다. 이때 밀려오는 생각은?",
        "options": ["'혹시 그때 내가 한 말 때문에 다들 나한테 서운해서 일부러 씹나?' 하고 과거의 특정 기억을 떠올리며 불안해한다.", "'다들 그냥 우연히 타이밍이 겹쳐서 바쁘거나 카톡을 못 본 거겠지' 하고 대수롭지 않게 넘긴다."]
    },
    {
        "id": "매몰비용 오류",
        "badge": "💸 통장을 스치는 구독 미련몬",
        "text": "매달 자동으로 15,000원씩 결제되지만 지난 세 달 동안 한 번도 켜지 않은 OTT(넷플릭스 등) 구독권이 있습니다. 해지하려니 괜히 망설여지는데, 그 이유는?",
        "options": ["'언젠가는 볼 텐데 지금 해지하면 손해 같고, 그동안 낸 돈이 아까워서' 일단 유지한다.", "'어차피 지난 석 달 안 봤으면 앞으로도 안 본다.' 이미 날린 돈은 잊고 즉시 해지한다."]
    },
    {
        "id": "틀 효과",
        "badge": "💼 알바나라 멘탈 쿠키",
        "text": "아르바이트나 직장에서 근무 중입니다. 사장님이 다가와 내 업무 결과에 대해 피드백을 주는데, 당신의 멘탈을 더 흔드는 말은 무엇인가요?",
        "options": ["'A 방식: 자네가 올린 기획안은 반려될 확률이 30%나 되네.' (부정적 실패율 강조)", "'B 방식: 자네가 올린 기획안은 통과될 확률이 70%나 되네.' (긍정적 성공률 강조)"]
    },
    {
        "id": "결합 오류",
        "badge": "🔎 SNS 돋보기 속 부러움이",
        "text": "내 피드에 자주 뜨는 대학 동창은 매일 명품을 인증하고, 화려한 파티에 가며, 인생이 늘 행복해 보입니다. 이 친구의 실제 삶으로 '확률상' 더 맞는 모습은 어느 쪽일까요?",
        "options": ["겉은 화려해 보여도 남들과 똑같이 취업 스트레스와 남모를 불안을 겪는 평범한 사람이다.", "부유한 집안 환경을 가졌으면서, 동시에 성격도 모난 곳 없이 늘 행복감만 느끼는 완벽한 사람이다."]
    },
    {
        "id": "전망 이론",
        "badge": "🦊 소소한 보상 앞의 밀당이",
        "text": "이벤트에 당첨되어 보상을 고를 수 있게 되었습니다. 당신의 심리를 가장 자극하는 정산 방식은 무엇인가요?",
        "options": ["안정형: 조건 없이 무조건 현금 20만 원을 즉시 수령한다.", "도박형: 동전을 던져 앞면이 나오면 50만 원을 받고, 뒷면이 나오면 한 푼도 받지 못한다."]
    }
]

# --- 🏠 화면 0: 첫 인트로 페이지 (수정 전 문구 + 귀여운 디자인) ---
if st.session_state.step == 0:
    st.write("")
    st.markdown("<div class='main-title'>🧸 일상 행동 및 선택 경향 테스트</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>“나는 평소에 얼마나 현명한 선택을 내릴까?”<br><span style='font-size:1.05rem; color:#A08E81;'>조별과제, 단톡방, 소비 습관으로 알아보는 나의 멘탈과 행동 유형</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-container' style='text-align: center;'>
        <div style='font-size: 4.5rem; margin-bottom: 15px;'>🐥 🥣 🥑 💤</div>
        <p style='line-height: 1.9; color: #554A42; font-size: 1.2rem; margin: 0;'>
        <b>조별 과제 잔혹사부터 단톡방 안 읽씹, 아까워서 못 끊는 구독 서비스까지!</b> 🤦‍♂️<br><br>
        우리는 일상 속에서 매 순간 최선의 선택을 내린다고 생각하지만,<br>
        사실 무의식적인 감정과 착각, '생각의 덫'에 걸려 스스로 스트레스를 키우곤 합니다.<br><br>
        주변에서 흔히 겪는 6가지 현실 공감 상황을 통해,<br>
        내가 일상에서 어떤 유형으로 행동하고 대처하는지 대시보드로 확인해 보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👉 나의 일상 행동 유형 알아보기 (Start)", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# --- 📝 화면 1 ~ 6: 질문 스텝 ---
elif 1 <= st.session_state.step <= 6:
    current_idx = st.session_state.step - 1
    q_data = questions[current_idx]
    
    st.progress(st.session_state.step / 6)
    st.caption(f"🐾 캐릭터가 열심히 걸어가고 있어요: {st.session_state.step} / 6 문항 진행 중")
    
    st.markdown(f"""
    <div class='card-container'>
        <div class='q-badge'>{q_data['badge']}</div>
        <div class='q-text'>{q_data['text']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    user_choice = st.radio("보기 중 하나를 선택하세요:", q_data['options'], index=0, label_visibility="collapsed")
    
    st.write("")
    if st.button("고르고 다음 골목으로 가기 ➡️", use_container_width=True):
        st.session_state.user_selections[q_data['id']] = user_choice
        st.session_state.step += 1
        st.rerun()

# --- 📊 화면 7: 종합 분석 대시보드 ---
elif st.session_state.step == 7:
    st.markdown("<div class='main-title'>📊 나의 일상 진단 리포트</div>", unsafe_allow_html=True)
    st.write("")
    
    scores = {}
    bias_count = 0
    
    # 그래프 축 이름을 심리 이론 명칭으로 명확하게 셋팅
    if st.session_state.user_selections.get("낙관성 편향") == "'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.":
        scores["낙관성 편향"] = 100; bias_count += 1
    else: scores["낙관성 편향"] = 20
        
    if st.session_state.user_selections.get("가용성 편향") == "'혹시 그때 내가 한 말 때문에 다들 나한테 서운해서 일부러 씹나?' 하고 과거의 특정 기억을 떠올리며 불안해한다.":
        scores["가용성 편향"] = 100; bias_count += 1
    else: scores["가용성 편향"] = 20
        
    if st.session_state.user_selections.get("매몰비용 오류") == "'언젠가는 볼 텐데 지금 해지하면 손해 같고, 그동안 낸 돈이 아까워서' 일단 유지한다.":
        scores["매몰비용 오류"] = 100; bias_count += 1
    else: scores["매몰비용 오류"] = 20
        
    if st.session_state.user_selections.get("틀 효과") == "'A 방식: 자네가 올린 기획안은 반려될 확률이 30%나 되네.' (부정적 실패율 강조)":
        scores["틀 효과(프레이밍)"] = 100; bias_count += 1
    else: scores["틀 효과(프레이밍)"] = 20
        
    if st.session_state.user_selections.get("결합 오류") == "부유한 집안 환경을 가졌으면서, 동시에 성격도 모난 곳 없이 늘 행복감만 느끼는 완벽한 사람이다.":
        scores["결합 오류"] = 100; bias_count += 1
    else: scores["결합 오류"] = 20

    if st.session_state.user_selections.get("전망 이론") == "동전을 던져 앞면이 나오면 50만 원을 받고, 뒷면이 나오면 한 푼도 받지 못한다.":
        scores["위험추구(전망이론)"] = 100; bias_count += 1
    else: scores["위험회피(전망이론)"] = 20

    df_result = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
    fig = px.line_polar(df_result, r='r', theta='theta', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', fillcolor='rgba(255, 138, 138, 0.25)', line_color='#FF8A8A', line_width=3)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ECE6DC")), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    final_avg = sum(scores.values()) / 6
    st.markdown(f"<h2 style='text-align:center; margin-bottom: 25px; color:#4A3E3D;'>나의 일상 비합리성 지수: <span style='color:#FF6B6B;'>{final_avg:.0f}점</span></h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏹 나의 합리성 행동 유형")
    
    # 귀여운 캐릭터 뼈대 + 심리 이론 결과 분석 융합
    if bias_count <= 1:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #4A5568;'>
            <div class='character-avatar'>🤖</div>
            <h4 style='color:#2D3748;'>유형 1: 시크하고 단단한 철벽 로봇봇 (Fact Sherlock)</h4>
            <p><b>성향 특징:</b> 조별과제에서 조원들이 잠수를 타면 감정적으로 분노하기보다 칼같이 역할을 재분배하고, 안 읽씹에 상처받지 않는 강철 멘탈의 소유자입니다. 일상 소비에서도 가성비와 실제 사용 빈도를 엄격하게 따집니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[자료조사 및 데이터 분석가], [오탈자 최종 검수 빌런]</b><br>팀원의 감정에 휘둘리지 않고 과제의 완성도와 팩트만 기가 막히게 발굴해 냅니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 타인에게 가끔 '차가운 로봇' 같거나 공감 능력이 부족하다는 인상을 줄 수 있습니다. 조원들의 피치 못할 사정이나 인간적인 감정 교류를 수치로만 판단하려다 묘한 갈등이 생길 수 있으니 약간의 유연함이 필요합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 2 <= bias_count <= 3:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #319795;'>
            <div class='character-avatar'>🐹</div>
            <h4 style='color:#234E52;'>유형 2: 상식 가득 든든한 웰시코기 (Pragmatic Corgi)</h4>
            <p><b>성향 특징:</b> 가장 상식적이고 무난한 밸런스 캐릭터입니다. 가끔은 "아까워서" 구독을 유지하거나 피드백에 욱하기도 하지만, 이내 이성을 찾고 현실적인 플랜B를 가동해 상황을 수습하는 능력이 뛰어납니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[중간 조율자(커뮤니케이터)], [실무 파워포인트 작성]</b><br>한쪽으로 치우치지 않는 상식적인 시선을 가졌기 때문에, 의견이 대립할 때 합리적인 타협안을 제시하며 실질적인 결과물을 만들어내는 데 능숙합니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 주변 사람들에게 '든든하고 무난한 사람'이라는 평을 듣지만, 결정적인 순간에 분위기나 본전 심리에 휩쓸려 우유부단해질 때가 있습니다. 손해를 보면서도 착한 아이 콤플렉스 때문에 리더의 의견에 끌려다니지 않도록 맺고 끊음을 명확히 하세요.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 4 <= bias_count <= 5:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #ED8936;'>
            <div class='character-avatar'>🐰</div>
            <h4 style='color:#7B341E;'>유형 3: 눈물 퐁퐁 예민 보스 토끼 (Soft Bunny)</h4>
            <p><b>성향 특징:</b> 단톡방 침묵에 밤새 잠을 설치거나, 사장님의 지적 한마디에 하루 종일 우울해지기 쉽습니다. 조별과제에서도 미련과 정 때문에 총대를 멨다가 혼자 고생하는 타입이지만, 그만큼 주변 사람을 챙기는 정이 많습니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[비주얼 발표자], [팀 분위기 메이커(동기부여가)]</b><br>공감 능력이 뛰어나고 스토리텔링 재능이 있어 청중의 마음을 움직이는 발표나, 갈등이 생긴 팀원들의 마음을 다독여 다시 뭉치게 만드는 서포트 역할에 뛰어납니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 나에게 상처만 주는 연인이나 친구인데도 "그동안 함께한 세월이 몇 년인데..."라는 미련(매몰비용) 때문에 질질 끌려다닐 수 있습니다. 정 때문에 조원들의 프리라이딩을 방치하다 독박을 쓸 위험이 크니 스스로의 방어벽이 필요합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #E53E3E;'>
            <div class='character-avatar'>🦖</div>
            <h4 style='color:#9B2C2C;'>유형 4: 무지성 하드캐리 폭주 렉스 (Hyper Rex)</h4>
            <p><b>성향 특징:</b> "내가 다 메우면 되지!"라는 초긍정 낙관주의와 직관으로 무장해 늘 사건사고의 중심에 서는 스타일입니다. SNS의 화려함에 쉽게 현혹되거나 충동적인 결정을 내리기 쉬우니 주의가 필요합니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[카리스마 총대 조장(PM)], [아이디어 브레인스토머]</b><br>아무도 선뜻 나서지 않는 위기 상황에서 강력한 리더십으로 판을 짜고, 번뜩이는 창의적 아이디어로 프로젝트의 방향성을 제시하는 시동 장치 역할을 잘 해냅니다.</p>
            <p><b>⚠️ 주변 사람들의 시선 (주의점):</b> 추진력이 시원시원해 보이지만, 팀원들 눈에는 '자기 생각대로만 우기는 고집불통 대장'으로 오해받을 수 있습니다. 무너진 관계나 실패한 계획을 미련 때문에 붙잡고 있다가 스스로 고통을 키울 수 있으니 항상 플랜B를 염두에 두어야 합니다.</p>
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
