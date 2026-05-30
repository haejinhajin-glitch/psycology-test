import streamlit as st
import plotly.express as px
import pandas as pd

# 1. 페이지 설정 및 반응형 최적화
st.set_page_config(page_title="말랑말랑 일상 선택 테스트", page_icon="🧸", layout="centered")

# 2. 아기자기하고 귀여운 파스텔톤 일상 UI 디자인 (CSS 무결성 확보)
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
        font-size: 2.6rem;
        font-weight: 700;
        text-align: center;
        color: #4A3E3D;
        margin-bottom: 8px;
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
        font-size: 1.1rem;
        display: inline-block;
        margin-bottom: 18px;
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
        font-size: 1.45rem !important;
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

# 일상 체감형 공감 데이터셋
questions = [
    {
        "id": "낙관성 편향",
        "badge": "🦖 조별과제 잔혹사",
        "text": "팀 프로젝트 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 던져줬습니다. 속이 타들어 가는 순간, 내 머릿속 스치는 생각은?",
        "options": ["'지구 멸망급 위기군... 하지만 내가 오늘 밤새 하드캐리하면 무조건 A+ 받아낼 수 있어!' 하며 총대를 멘다.", "'조원들이 안 도와주면 현실적으로 한계가 있지 뭐...' 마음을 비우고 상황에 맞춰 타협한다."]
    },
    {
        "id": "가용성 편향",
        "badge": "🐱 단톡방 침묵의 소심이",
        "text": "친구와 살짝 어색한 말다툼을 한 뒤, 오랜만에 단톡방에 장난을 쳤는데 아무도 답장 없이 안읽씹이 이어집니다. 이때 밀려오는 내 생각은?",
        "options": ["'설마 그때 그 일 때문에 다들 나 왕따 시키나..?' 과거의 안 좋았던 기억을 짜내며 혼자 이불킥을 찬다.", "'다들 마침 바쁜 타이밍이 겹쳤거나 폰을 못 보고 있나 보네~' 하고 유튜브 쇼츠 보러 간다."]
    },
    {
        "id": "매몰비용 오류",
        "badge": "🐹 통장을 스치는 구독 미련몬",
        "text": "매달 자동으로 15,000원씩 결제되지만 지난 석 달 동안 바빠서 한 번도 켜지 않은 OTT 구독권이 있습니다. 해지하려니 망설여지는 이유는?",
        "options": ["'언젠가는 주말에 몰아볼 텐데... 그동안 낸 돈도 너무 아깝고 기회 봐서 유지하자!' 일단 놔둔다.", "'어차피 석 달 안 봤으면 평생 안 본다.' 이미 날린 돈은 눈물로 잊고 1초 만에 해지 버튼을 누른다."]
    },
    {
        "id": "틀 효과",
        "badge": "🐻 알바나라 멘탈 쿠키",
        "text": "아르바이트 근무 중에 사장님이 다가와 내 업무 결과에 대해 슥 피드백을 건넵니다. 내 유약한 유기농 멘탈을 더 와르르 무너뜨리는 사장님의 한마디는?",
        "options": ["'김 대리, 이번 기획안은 반려되거나 까일 확률이 30%나 된다네.' (부정적인 실패 확률 강조)", "'김 대리, 이번 기획안은 무사히 통과될 확률이 70%나 된다네.' (긍정적인 성공 확률 강조)"]
    },
    {
        "id": "결합 오류",
        "badge": "🐰 SNS 돋보기 속 부러움이",
        "text": "인스타 피드에 맨날 명품 언박싱을 올리고 화려한 핫플만 찾아다니며 인생이 늘 핑크빛 같아 보이는 동창이 있습니다. 이 친구의 진짜 삶으로 통계학적 '확률상' 더 맞는 모습은?",
        "options": ["피드만 화려할 뿐, 남들과 똑같이 취업 걱정하고 월요일을 싫어하는 평범한 사람이다.", "엄청난 금수저 집안이면서 동시에 성격도 티 없이 맑고 슬픔이란 감정은 아예 모르는 완벽한 존재이다."]
    },
    {
        "id": "전망 이론",
        "badge": "🦊 소소한 보상 앞의 밀당이",
        "text": "열심히 참여한 이벤트에 당첨되어 기분 좋은 보상을 고를 수 있게 되었습니다! 내 가슴을 가장 두근거리게 만드는 수령 방식은?",
        "options": ["조건 없이 무조건 현금 20만 원을 손에 쥐는 '안전빵 최고' 수령", "동전을 던져 앞면이 나오면 50만 원! 뒷면이 나오면 0원인 '인생은 한 방' 수령"]
    }
]

# --- 🏠 화면 0: 첫 인트로 페이지 ---
if st.session_state.step == 0:
    st.write("")
    st.markdown("<div class='main-title'>🧸 말랑말랑 일상 선택 테스트</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>“나는 평소에 얼마나 유연하고 현명한 선택을 할까?”<br><span style='font-size:1.05rem; color:#A08E81;'>귀여운 캐릭터들과 함께 알아보는 나의 멘탈 행동 유형 진단</span></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-container' style='text-align: center;'>
        <div style='font-size: 4.5rem; margin-bottom: 15px;'>🐥 🥣 🥑 💤</div>
        <p style='line-height: 1.9; color: #554A42; font-size: 1.2rem; margin: 0;'>
        조별 과제 대참사부터 단톡방 안 읽씹의 외로움, 아까워서 못 끊는 구독 서비스까지!<br>
        우리는 매일 완벽한 이성으로 선택을 내린다고 생각하지만,<br>
        사실 무의식적인 <b>말랑말랑한 착각의 늪</b>에 빠져 사서 고생하곤 합니다. 멍멍! 🐾<br><br>
        일상에서 흔히 만나는 귀여운 상황 속에서 내가 평소 어떤 유형으로 행동하는지<br>
        <b>나만의 일상 일러스트 캐릭터 유형</b>을 재미있게 확인해 보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✨ 나의 일상 캐릭터 알아보기 (Start)", use_container_width=True):
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
    st.markdown("<div class='main-title'>📊 진단 리포트가 나왔어요!</div>", unsafe_allow_html=True)
    st.write("")
    
    scores = {}
    bias_count = 0
    
    if st.session_state.user_selections.get("낙관성 편향") == "'지구 멸망급 위기군... 하지만 내가 오늘 밤새 하드캐리하면 무조건 A+ 받아낼 수 있어!' 하며 총대를 멘다.":
        scores["팀플 독박 과신"] = 100; bias_count += 1
    else: scores["팀플 독박 과신"] = 20
        
    if st.session_state.user_selections.get("가용성 편향") == "'설마 그때 그 일 때문에 다들 나 왕따 시키나..?' 과거의 안 좋았던 기억을 짜내며 혼자 이불킥을 찬다.":
        scores["카톡 예민 지수"] = 100; bias_count += 1
    else: scores["카톡 예민 지수"] = 20
        
    if st.session_state.user_selections.get("매몰비용 오류") == "'언젠가는 주말에 몰아볼 텐데... 그동안 낸 돈도 너무 아깝고 기회 봐서 유지하자!' 일단 놔둔다.":
        scores["구독 미련 지수"] = 100; bias_count += 1
    else: scores["구독 미련 지수"] = 20
        
    if st.session_state.user_selections.get("틀 효과") == "'김 대리, 이번 기획안은 반려되거나 까일 확률이 30%나 된다네.' (부정적인 실패 확률 강조)":
        scores["쿠키 멘탈 지수"] = 100; bias_count += 1
    else: scores["쿠키 멘탈 지수"] = 20
        
    if st.session_state.user_selections.get("결합 오류") == "엄청난 금수저 집안이면서 동시에 성격도 티 없이 맑고 슬픔이란 감정은 아예 모르는 완벽한 존재이다.":
        scores["인스타 필터 오해"] = 100; bias_count += 1
    else: scores["인스타 필터 오해"] = 20

    if st.session_state.user_selections.get("전망 이론") == "동전을 던져 앞면이 나오면 50만 원! 뒷면이 나오면 0원인 '인생은 한 방' 수령":
        scores["인생 한방 리스크"] = 100; bias_count += 1
    else: scores["인생 한방 리스크"] = 20

    df_result = pd.DataFrame(dict(r=list(scores.values()), theta=list(scores.keys())))
    fig = px.line_polar(df_result, r='r', theta='theta', line_close=True, range_r=[0,100])
    fig.update_traces(fill='toself', fillcolor='rgba(255, 138, 138, 0.25)', line_color='#FF8A8A', line_width=3)
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], gridcolor="#ECE6DC")), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    final_avg = sum(scores.values()) / 6
    st.markdown(f"<h2 style='text-align:center; margin-bottom: 25px; color:#4A3E3D;'>나의 일상 말랑 지수: <span style='color:#FF6B6B;'>{final_avg:.0f}점</span></h2>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏹 나의 합리성 행동 유형")
    
    if bias_count <= 1:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #4A5568;'>
            <div class='character-avatar'>🤖</div>
            <h4 style='color:#2D3748;'>유형 1: 시크하고 단단한 철벽 로봇봇 (Fact Sherlock)</h4>
            <p><b>성향 특징:</b> 조원들이 잠수를 타도 "그럼 이름 빼야지" 하고 칼같이 대처하며 단톡방의 읽씹에 전혀 타격을 입지 않는 무감정 레이더의 소유자입니다. 일상 소비 지출도 필터 없이 완벽하게 계산합니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[자료조사 및 데이터 분석가], [오탈자 최종 검수 빌런]</b><br>팀원의 감정에 휘둘리지 않고 과제의 완성도와 팩트만 기가 막히게 발굴해 냅니다.</p>
            <p><b>⚠️ 주변 사람들의 시선:</b> 주변 친구들이 가끔 "너 혹시 로봇이야?"라며 정이 부족하다는 농담을 건넬 수 있어요. 가끔은 조원들의 눈물 겨운 지각 사정에 이모지 하나 정도 달아주는 유연함을 발휘해 보세요!</p>
        </div>
        """, unsafe_allow_html=True)
    elif 2 <= bias_count <= 3:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #319795;'>
            <div class='character-avatar'>🐹</div>
            <h4 style='color:#234E52;'>유형 2: 상식 가득 든든한 웰시코기 (Pragmatic Corgi)</h4>
            <p><b>성향 특징:</b> 현대 대학생들의 가장 귀여운 표준형입니다! 가끔은 아까워서 구독을 유지하고 사장님 눈치에 삐지기도 하지만, 이내 꼬리를 흔들며 현실적인 플랜B를 찾아 일상을 씩씩하게 복구합니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[중간 조율 소통 요정], [실무 파워포인트 작성]</b><br>성격이 유순하고 상식적인 선을 지키기 때문에 팀플에서 갈등이 터졌을 때 조원들을 중간에서 잇는 최고의 징검다리가 됩니다.</p>
            <p><b>⚠️ 주변 사람들의 시선:</b> "같이 있으면 제일 편하고 든든한 친구"라는 호평을 받습니다. 하지만 가끔 거절을 못 해 본전 심리에 끌려다니거나 과도한 부탁을 수락할 수 있으니 싫은 건 싫다고 멍멍! 외칠 줄 알아야 합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    elif 4 <= bias_count <= 5:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #ED8936;'>
            <div class='character-avatar'>🐰</div>
            <h4 style='color:#7B341E;'>유형 3: 눈물 퐁퐁 예민 보스 토끼 (Soft Bunny)</h4>
            <p><b>성향 특징:</b> 유리 같은 투명 멘탈과 따뜻한 정을 가진 감성 주의자입니다. 단톡방이 조용하면 '내가 싫나?' 소설을 쓰고, 사장님의 말 한마디에 하루 종일 당도가 떨어집니다. 조별과제에서도 미련 때문에 고생을 사서 합니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[비주얼 발표자], [팀 프로젝트 사기 메이커]</b><br>공감 능력이 200%라 청중의 감성을 터치하는 발표 무대에 강하며, 조원들을 간식으로 독려하며 분위기를 훈훈하게 만드는 데 도사입니다.</p>
            <p><b>⚠️ 주변 사람들의 시선:</b> "정이 많고 사랑스러운 사람"이라는 평이 지배적이지만, 나쁜 마음을 먹은 조원 빌런들에게 이용당해 총대를 메고 독박을 쓸 확률이 가장 높습니다! 스스로의 마음의 벽을 지키는 연습이 필요합니다.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='type-container' style='border-left: 6px solid #E53E3E;'>
            <div class='character-avatar'>🦖</div>
            <h4 style='color:#9B2C2C;'>유형 4: 무지성 하드캐리 폭주 렉스 (Hyper Rex)</h4>
            <p><b>성향 특징:</b> "조원 다 잠수 타도 내 솜씨로 찢어서 A+ 받으면 그만!"이라는 마이웨이 초긍정 낙관 몬스터입니다. 직관과 근거 없는 자신감을 좋아하며, 리스크가 큰 베팅도 시원하게 즐기는 상남자형 스타일입니다.</p>
            <p><b>🧩 조별과제 추천 역할:</b> <b>[카리스마 총대 조장(PM)], [아이디어 뱅크 크리에이터]</b><br>아무도 고르지 않는 똥망 진흙탕 상황에서 특유의 화력으로 판을 주도해 프로젝트를 억지로라도 굴러가게 만드는 견인차 역할을 합니다.</p>
            <p><b>⚠️ 주변 사람들의 시선:</b> 추진력은 우주 최강이지만, 팀원들 눈에는 '자기 생각대로만 우기는 고집불통 대장'으로 오해받을 수 있습니다. 실패한 관계나 마케팅 프레임에 걸려 고꾸라질 수 있으니 늘 주위를 살피며 속도를 조절해야 합니다.</p>
        </div>
        """, unsafe_allow_html=True)

    # 🛠️ 일상 속 비합리성 극복 방법 솔루션 대시보드
    st.markdown("---")
    st.markdown("### 🛠️ 일상에서 실천하는 멘탈 수호 & 대처법")
    st.markdown("""
    <div class='solution-box'>
        <div class='solution-title'>1. 단톡방과 타인 반응에서 내 마음 지키기 (🐰 토끼 방어법)</div>
        <div class='solution-desc'>
        카톡 읽씹이나 상대방의 사소한 날 선 반응에 심장이 두근거릴 때는 <b>'내 귀여운 친구가 이 상황이라면 내가 뭐라고 다독여줄까?'</b>라고 삼인칭으로 소환해 보세요. 억울한 감정 거품이 빠지고 '그냥 바쁜가 보다' 하는 상식적인 팩트가 눈에 들어옵니다.
        </div>
    </div>
    <div class='solution-box'>
        <div class='solution-title'>2. 아까워서 쟁여둔 미련 소비 정리하기 (🐹 코기 손절법)</div>
        <p class='solution-desc'>
        "돈 아까워서" 붙잡고 있는 유행 지난 옷, 안 보는 OTT 구독, 상처만 주는 관계가 있다면 <b>'최근 3달 동안 나에게 진짜 미소를 줬는가?'</b>라는 칼 같은 기준을 선물해 보세요. 통과하지 못했다면 과감히 리셋하는 것이 내 지갑과 정신건강에 훨씬 이득입니다.
        </p>
    </div>
    <div class='solution-box'>
        <div class='solution-title'>3. 독박 총대 메기 전에 리스크 메모하기 (🦖 렉스 제동법)</div>
        <p class='solution-desc'>
        근거 없는 초긍정 자신감으로 무작정 총대를 매기 전에, <b>'조원들이 끝까지 도망가면 내 일정과 학점은 어떻게 꼬이지?'</b>라는 최악의 외나무다리 시나리오를 메모장에 딱 세 줄만 적어보세요. 시각화된 경고등을 보는 순간 무리한 폭주를 멈추고 현명하게 역할을 쪼갤 용기가 생깁니다.
        </p>
    </div>
""", unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 테스트 골목길 처음으로 돌아가기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.user_selections = {}
        st.rerun()
