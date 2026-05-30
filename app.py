<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        body { font-family: 'Press Start 2P', cursive; background-color: #fef3c7; }
        .pixel-border { border: 4px solid #000; box-shadow: 6px 6px 0px 0px rgba(0,0,0,1); }
        .pixel-btn:active { transform: translate(4px, 4px); box-shadow: none; }
    </style>
</head>
<body class="flex items-center justify-center min-h-screen p-4">

    <div id="app" class="max-w-md w-full bg-pink-200 p-8 rounded-2xl pixel-border text-center">
        <div id="screen-1">
            <h1 class="text-2xl mb-8 leading-relaxed">조별과제의<br>성 탈출기</h1>
            <button onclick="changeScreen(2)" class="pixel-btn bg-sky-300 px-6 py-4 pixel-border hover:bg-sky-400">게임 시작!</button>
        </div>

        <div id="screen-2" class="hidden">
            <h2 id="q-text" class="text-sm mb-6">질문이 로딩중...</h2>
            <div id="options" class="flex flex-col gap-4"></div>
        </div>

        <div id="screen-3" class="hidden">
            <h2 class="text-xl mb-4">당신의 유형은?</h2>
            <div id="result-box" class="bg-white p-4 mb-6 pixel-border text-sm"></div>
            <button onclick="changeScreen(4)" class="pixel-btn bg-yellow-300 px-6 py-4 pixel-border">교정 미션 시작!</button>
        </div>

        <div id="screen-4" class="hidden">
            <h2 class="text-sm mb-6">미션을 모두 클리어하세요!</h2>
            <div id="missions" class="space-y-4"></div>
            <div id="ending" class="hidden mt-6 text-red-500">축하합니다! A+ 탈출 성공! ✨</div>
        </div>
    </div>

    <script>
        let currentQ = 0;
        let score = { waddle: 0, ddd: 0, marx: 0, meta: 0, kain: 0 };
        
        const questions = [
            { q: "최근 뉴스 속 음모론이 떠오른다. 나는?", a: ["정보 수집!", "음모론 믿음(가용성)"], type: 'kain' },
            { q: "조장이 'D'라고 할 때 내 행동은?", a: ["열심히함(프레임)", "포기함"], type: 'meta' },
            { q: "망한 PPT, 시간 아까운데?", a: ["계속함(매몰비용)", "갈아엎음"], type: 'ddd' },
            { q: "대본 없어도 난 잘하겠지?", a: ["낙관적(낙관편향)", "불안함"], type: 'waddle' },
            { q: "저 사람은 코딩만 잘할 거야?", a: ["편견 가짐(결합오류)", "직접 확인"], type: 'marx' }
        ];

        function changeScreen(n) {
            document.querySelectorAll('#app > div').forEach(div => div.classList.add('hidden'));
            document.getElementById('screen-' + n).classList.remove('hidden');
            if(n === 2) renderQuestion();
            if(n === 4) renderMissions();
        }

        function renderQuestion() {
            if(currentQ >= questions.length) { showResult(); return; }
            const q = questions[currentQ];
            document.getElementById('q-text').innerText = q.q;
            const container = document.getElementById('options');
            container.innerHTML = '';
            q.a.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.className = "pixel-btn bg-white p-3 pixel-border text-xs";
                btn.innerText = opt;
                btn.onclick = () => { if(idx === 1) score[q.type]++; currentQ++; renderQuestion(); };
                container.appendChild(btn);
            });
        }

        function showResult() {
            changeScreen(3);
            document.getElementById('result-box').innerText = "당신은 '근자감 폭발 웨들디'형! 긍정적이지만 마감 직전 프리라이더가 될 위험이 있어요.";
        }

        function renderMissions() {
            const container = document.getElementById('missions');
            ['계획 짜기', '집착 지우기', '칭찬하기'].forEach((m, i) => {
                const div = document.createElement('div');
                div.className = "flex justify-between items-center p-2 border-b-2 border-black";
                div.innerHTML = `<span>${m}</span> <input type="checkbox" onchange="checkEnd()">`;
                container.appendChild(div);
            });
        }

        function checkEnd() {
            if(document.querySelectorAll('input:checked').length === 3) {
                document.getElementById('ending').classList.remove('hidden');
            }
        }
    </script>
</body>
</html>
