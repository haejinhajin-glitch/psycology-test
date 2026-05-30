import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="TEAM PROJECT SURVIVAL",
    page_icon="🎮",
    layout="centered"
)

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');

html, body, [class*="css"] {
    font-family: 'Gowun Dodum', sans-serif;
}

.stApp{
    background:
    linear-gradient(
        180deg,
        #0F172A 0%,
        #111827 100%
    );
}

/* 타이틀 */

.game-title{
    text-align:center;
    color:white;
    margin-top:30px;
}

.game-title h1{
    font-size:3rem;
    color:#FACC15;
    margin-bottom:10px;
}

.game-title h2{
    font-size:1.4rem;
    color:#E2E8F0;
    margin-bottom:25px;
}

/* 카드 */

.game-card{
    background:#1E293B;
    border:2px solid #8B5CF6;
    border-radius:20px;
    padding:25px;
    color:white;
    box-shadow:0px 0px 25px rgba(139,92,246,0.3);
    margin-bottom:20px;
}

.quest-card{
    background:#1E293B;
    border-left:8px solid #FACC15;
    border-radius:18px;
    padding:25px;
    color:white;
    margin-bottom:20px;
}

/* 상태창 */

.status-box{
    background:#111827;
    border:1px solid #334155;
    border-radius:15px;
    padding:15px;
    text-align:center;
    color:white;
    margin-top:15px;
}

/* QUEST */

.quest-title{
    color:#FACC15;
    font-size:1.5rem;
    font-weight:bold;
    margin-bottom:15px;
}

.quest-sub{
    color:#CBD5E1;
    margin-bottom:15px;
}

/* 버튼 */

.stButton button{
    width:100%;
    height:60px;
    border-radius:15px;
    border:none;
    background:#8B5CF6;
    color:white;
    font-size:1.1rem;
    font-weight:bold;
}

.stButton button:hover{
    background:#7C3AED;
}

/* radio */

div[data-testid="stRadio"] label{
    color:white !important;
    font-size:1.05rem !important;
}

div[data-testid="stRadio"] > div{
    background:#1E293B;
    padding:15px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SESSION
# =====================================

if "step" not in st.session_state:
    st.session_state.step = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

# =====================================
# QUESTIONS
# =====================================

questions = [
    {
        "id":"optimism",
        "badge":"📢 마감 직전의 빌런 발생",
        "text":"팀 프로젝트 마감은 코앞인데 조원들이 잠수를 타거나 결과물을 엉망으로 던져줬습니다. 속이 타들어 가는 순간, 내 머릿속 스치는 생각은?",
        "options":[
            "'내가 오늘 밤새워서 하드캐리하면 무조건 완벽한 A+ 받아낼 수 있어!'라며 독박을 자처한다.",
            "'조원들이 안 도와주면 현실적으로 한계가 있지.' 마음을 비우고 상황에 맞춰 교수님과 타협한다."
        ]
    },

    {
        "id":"availability",
        "badge":"💬 단톡방의 불길한 침묵",
        "text":"조장이 단톡방에 '자료조사 언제쯤 끝날까요?'라고 물었는데 아무도 답장 없이 3시간 동안 안읽씹이 이어집니다. 이때 밀려오는 나의 생각은?",
        "options":[
            "'설마 다들 나 몰래 따로 방 파서 내 뒷담화하고 있나?' 에타에서 본 단톡방 왕따 썰을 떠올리며 불안해한다.",
            "'그냥 마침 타이밍이 겹쳐서 다들 바쁘거나 폰을 안 보고 있겠지.' 하고 대수롭지 않게 넘긴다."
        ]
    },

    {
        "id":"sunk",
        "badge":"📂 산으로 가는 PPT 미련",
        "text":"팀원 한 명이 이틀 밤을 새워 자료를 조사해 왔는데, 우리 조 발표 주제와 전혀 맞지 않는 쓸모없는 자료입니다. 이때 당신의 대처는?",
        "options":[
            "'그래도 밤새 고생해서 찾아온 자료인데 아까우니까...' 어떻게든 욱여넣어 발표 슬라이드에 포함한다.",
            "'주제와 안 맞으면 냉정하게 버려야지.' 고생한 건 미안하지만 과감히 제외하고 새로 조사한다."
        ]
    },

    {
        "id":"frame",
        "badge":"🐻 교수님의 무서운 한마디",
        "text":"교수님이 피드백 도중 우리 조 기획안을 보며 한마디 하십니다. 당신의 멘탈을 더 와르르 무너뜨리는 멘트는?",
        "options":[
            "'C학점 이하로 삐끗할 확률이 30%나 되네.'",
            "'A학점 이상 받을 확률이 70%나 되네.'"
        ]
    },

    {
        "id":"conjunction",
        "badge":"🔎 옆 조 조장의 정체",
        "text":"옆 조 조장은 매일 인스타에 화려한 술자리와 명품을 인증하면서도 팀플 학점까지 A+인 것처럼 보입니다.",
        "options":[
            "평범한 대학생일 가능성이 더 높다.",
            "금수저 + 천재 + 팀원복까지 갖춘 완벽한 존재일 것이다."
        ]
    },

    {
        "id":"prospect",
        "badge":"💰 무임승차 고발하기",
        "text":"회의에 한 번도 안 나온 조원을 교수님께 고발할 기회가 생겼다.",
        "options":[
            "안전하게 내 점수만 지킨다.",
            "대박을 노리고 위험을 감수한다."
        ]
    }
]

# =====================================
# INTRO
# =====================================

if st.session_state.step == 0:

    st.markdown("""
    <div class='game-title'>
        <h1>🎮 TEAM PROJECT SURVIVAL</h1>
        <h2>조별과제 잔혹사</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='game-card'>

    이번 학기,

    당신은 수많은 팀플과
    단톡방 안읽씹,
    PPT 빌런,
    무임승차 조원들을 마주하게 됩니다.

    과연 당신은

    <b>학점과 멘탈을 모두 지켜낼 수 있을까요?</b>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='status-box'>
    ⚡ 멘탈 : 100<br>
    📚 학점 : A+<br>
    🎒 경험치 : 0
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 게임 시작"):
        st.session_state.step = 1
        st.rerun()

# =====================================
# QUESTIONS
# =====================================

elif 1 <= st.session_state.step <= 6:

    idx = st.session_state.step - 1

    q = questions[idx]

    st.progress(st.session_state.step / 6)

    st.markdown(
        f"""
        <div class='quest-card'>
            <div class='quest-title'>
            QUEST {st.session_state.step:02d}
            </div>

            <div class='quest-sub'>
            {q["badge"]}
            </div>

            <h4>MISSION</h4>

            <p>{q["text"]}</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    choice = st.radio(
        "",
        q["options"],
        index=0
    )

    if st.button("⚔️ 결정하기"):
        st.session_state.answers[q["id"]] = choice
        st.session_state.step += 1
        st.rerun()

# ===== PART 1 END =====
# =====================================
# RESULT CALCULATION
# =====================================

elif st.session_state.step == 7:

    scores = {}

    bias_count = 0

    # 낙관성 편향
    if "하드캐리" in st.session_state.answers["optimism"]:
        scores["낙관성"] = 100
        bias_count += 1
    else:
        scores["낙관성"] = 20

    # 가용성 편향
    if "뒷담화" in st.session_state.answers["availability"]:
        scores["가용성"] = 100
        bias_count += 1
    else:
        scores["가용성"] = 20

    # 매몰비용
    if "아까우니까" in st.session_state.answers["sunk"]:
        scores["매몰비용"] = 100
        bias_count += 1
    else:
        scores["매몰비용"] = 20

    # 프레이밍
    if "30%" in st.session_state.answers["frame"]:
        scores["틀 효과"] = 100
        bias_count += 1
    else:
        scores["틀 효과"] = 20

    # 결합 오류
    if "완벽한 존재" in st.session_state.answers["conjunction"]:
        scores["결합 오류"] = 100
        bias_count += 1
    else:
        scores["결합 오류"] = 20

    # 전망 이론
    if "위험" in st.session_state.answers["prospect"]:
        scores["위험추구"] = 100
        bias_count += 1
    else:
        scores["위험추구"] = 20

    # =====================================
    # 결과 점수
    # =====================================

    total_score = round(sum(scores.values()) / 6)

    st.markdown("""
    <div class='game-title'>
        <h1>🏆 MISSION COMPLETE</h1>
        <h2>팀플 생존 결과 분석</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class='game-card'>

    ⚡ 인지오류 노출도

    <h1 style='color:#FACC15; text-align:center;'>{total_score}점</h1>

    점수가 높을수록
    인지편향의 영향을 많이 받는 플레이어입니다.

    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # 레벨 계산
    # =====================================

    level = max(1, 100 - total_score)

    st.markdown(f"""
    <div class='status-box'>

    🎖️ 플레이어 레벨 : LV.{level}

    🧠 판단력 : {100-total_score}%

    ⚔️ 팀플 생존력 : {level}%

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # =====================================
    # RADAR CHART
    # =====================================

    st.subheader("🧠 인지편향 레이더")

    radar_df = pd.DataFrame(
        dict(
            r=list(scores.values()),
            theta=list(scores.keys())
        )
    )

    fig = px.line_polar(
        radar_df,
        r="r",
        theta="theta",
        line_close=True,
        range_r=[0,100]
    )

    fig.update_traces(
        fill="toself",
        fillcolor="rgba(139,92,246,0.35)",
        line_color="#FACC15",
        line_width=4
    )

    fig.update_layout(
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font_color="white",
        showlegend=False,
        polar=dict(
            bgcolor="#0F172A",
            radialaxis=dict(
                visible=True,
                range=[0,100]
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("📚 편향별 분석")

    # =====================================
    # 개별 분석
    # =====================================

    for bias, value in scores.items():

        if value >= 80:

            st.markdown(f"""
            <div class='game-card'>

            <h4>⚠️ {bias}</h4>

            현재 이 영역의 인지편향 영향이 강하게 나타났습니다.

            팀플 상황에서 판단보다 감정이나 직관에
            영향을 받을 가능성이 있습니다.

            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
            <div class='game-card'>

            <h4>✅ {bias}</h4>

            비교적 안정적인 판단을 유지하고 있습니다.

            감정적 반응보다 현실적인 선택을 할
            가능성이 높습니다.

            </div>
            """, unsafe_allow_html=True)

# ===== PART 2 END =====
    # =====================================
    # PLAYER TYPE
    # =====================================

    st.markdown("---")

    st.markdown("""
    <div class='game-title'>
        <h2>🏅 최종 플레이어 유형</h2>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------
    # TYPE 1
    # -------------------------------------

    if bias_count <= 1:

        st.markdown("""
        <div class='game-card'>

        <h2 style='color:#FACC15;'>🏆 학점 수호자</h2>

        <h4>LV.MAX 냉철한 전략가</h4>

        <p>
        당신은 조별과제 속에서도 비교적
        감정에 휘둘리지 않고 현실적인 판단을 내리는 플레이어입니다.
        </p>

        <p>
        단톡방이 조용하다고 바로 최악을 상상하지 않고,
        밤새 만든 자료라도 필요 없으면 과감히 버릴 수 있습니다.
        </p>

        <p>
        조별과제라는 혼돈 속에서도
        학점과 멘탈을 함께 지켜내는 타입입니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        partner = "🔥 독박 캐리어"

    # -------------------------------------
    # TYPE 2
    # -------------------------------------

    elif bias_count <= 3:

        st.markdown("""
        <div class='game-card'>

        <h2 style='color:#FACC15;'>🛠️ 현실 적응 전문가</h2>

        <h4>균형 잡힌 실무형 플레이어</h4>

        <p>
        가장 많은 대학생이 속하는 유형입니다.
        </p>

        <p>
        가끔 흔들리기도 하지만
        결국에는 현실적인 판단으로 돌아옵니다.
        </p>

        <p>
        팀플에서도 지나치게 독주하지 않고
        적절하게 협력하며 결과물을 만들어냅니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        partner = "🏆 학점 수호자"

    # -------------------------------------
    # TYPE 3
    # -------------------------------------

    elif bias_count <= 5:

        st.markdown("""
        <div class='game-card'>

        <h2 style='color:#FACC15;'>😰 과몰입 감시자</h2>

        <h4>눈치 레이더 MAX</h4>

        <p>
        당신은 팀 분위기와 사람들의 반응에
        매우 민감한 플레이어입니다.
        </p>

        <p>
        단톡방 침묵만으로도
        수십 가지 시나리오를 상상할 수 있습니다.
        </p>

        <p>
        공감 능력은 뛰어나지만
        불필요한 걱정으로 스스로를 지치게 할 수 있습니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        partner = "🛠️ 현실 적응 전문가"

    # -------------------------------------
    # TYPE 4
    # -------------------------------------

    else:

        st.markdown("""
        <div class='game-card'>

        <h2 style='color:#FACC15;'>🔥 독박 캐리어</h2>

        <h4>하드캐리 전설 등급</h4>

        <p>
        당신은 위기가 닥치면
        '내가 하면 되지!' 모드가 발동하는 플레이어입니다.
        </p>

        <p>
        강한 추진력과 자신감을 가지고 있지만
        때로는 과도한 낙관주의 때문에
        모든 일을 혼자 떠맡을 수 있습니다.
        </p>

        <p>
        팀플이 끝나면 학점보다
        체력이 먼저 사라질 가능성이 높습니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        partner = "😰 과몰입 감시자"

    # =====================================
    # BEST PARTNER
    # =====================================

    st.markdown(f"""
    <div class='game-card'>

    <h3>🤝 최고의 팀플 파트너</h3>

    <h2 style='color:#FACC15;'>{partner}</h2>

    서로의 약점을 보완하며
    최고의 팀플 시너지를 낼 수 있습니다.

    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # SURVIVAL GUIDE
    # =====================================

    st.markdown("---")

    st.markdown("""
    <div class='game-title'>
        <h2>📜 팀플 생존 가이드</h2>
    </div>
    """, unsafe_allow_html=True)

    guides = [
        (
            "⚡ 낙관성 편향",
            "혼자 다 할 수 있다는 생각이 들 때는 최악의 상황도 함께 적어보세요."
        ),
        (
            "📂 매몰비용 오류",
            "이미 투자한 시간보다 앞으로의 효과를 기준으로 판단하세요."
        ),
        (
            "💬 가용성 편향",
            "단톡방 침묵이 반드시 부정적인 의미는 아닙니다."
        ),
        (
            "🎯 틀 효과",
            "같은 정보라도 표현 방식이 판단을 바꿀 수 있다는 점을 기억하세요."
        ),
        (
            "🔎 결합 오류",
            "극적인 이야기보다 실제 확률이 더 중요합니다."
        ),
        (
            "🎲 전망 이론",
            "손실을 피하려는 감정이 위험한 선택으로 이어질 수 있습니다."
        )
    ]

    for title, desc in guides:

        st.markdown(f"""
        <div class='game-card'>

        <h4>{title}</h4>

        <p>{desc}</p>

        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # FINAL SCORE CARD
    # =====================================

    st.markdown("---")

    st.markdown(f"""
    <div class='game-card'>

    <h2 style='text-align:center; color:#FACC15;'>

    🎓 이번 학기 생존 결과

    </h2>

    <h1 style='text-align:center;'>

    {100-total_score}점

    </h1>

    <p style='text-align:center;'>

    당신은 조별과제 세계에서
    꽤 높은 생존력을 가진 플레이어입니다.

    </p>

    </div>
    """, unsafe_allow_html=True)

    # =====================================
    # RESTART
    # =====================================

    st.write("")

    if st.button("🔄 새로운 학기 시작하기"):

        st.session_state.step = 0
        st.session_state.answers = {}

        st.rerun()
