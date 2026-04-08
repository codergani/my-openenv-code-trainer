// ===== PAGE NAVIGATION =====
function showPage(id) {
    document.querySelectorAll('.page').forEach(function(p) { p.classList.add('hidden'); });
    document.getElementById(id).classList.remove('hidden');
}

function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function sleep(ms) { return new Promise(function(r) { setTimeout(r, ms); }); }

document.addEventListener('DOMContentLoaded', function() {

    // ================================================================
    //  CODE TRAINER
    // ================================================================
    var TOTAL = 10, runCount = 0, botBrain = {};
    var guesses = ['print','True','42','list','None','for','def','class','return','import'];

    var trainBtn = document.getElementById('train-btn');
    var clearBtn = document.getElementById('clear-btn');

    function updateBrain() {
        var el = document.getElementById('brain-size');
        if (el) el.textContent = Object.keys(botBrain).length + ' / ' + TOTAL + ' learned';
    }

    if (trainBtn) trainBtn.onclick = function() { trainBot(); };
    if (clearBtn) clearBtn.onclick = function() { clearCodeBot(); };

    var mta = document.getElementById('modal-train-again');
    if (mta) mta.onclick = function() {
        document.getElementById('overlay').classList.add('hidden');
        trainBot();
    };

    async function trainBot() {
        runCount++;
        trainBtn.disabled = true;
        clearBtn.disabled = true;
        var overlay = document.getElementById('overlay');
        if (overlay) overlay.classList.add('hidden');
        var fb = document.getElementById('feedback');
        if (fb) fb.classList.add('hidden');
        var log = document.getElementById('training-log');
        if (log) log.innerHTML = '';

        setStats(0, 0, 0, 0);
        addLog('══ Run #' + runCount + ' | Brain: ' + Object.keys(botBrain).length + '/' + TOTAL + ' ══', 'log-bot');

        // Reset environment
        var resetData;
        try {
            var resp = await fetch('/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({})
            });
            resetData = await resp.json();
            addLog('Environment reset OK', 'log-correct');
        } catch (err) {
            addLog('ERROR: Cannot connect to server! ' + err.message, 'log-wrong');
            trainBtn.disabled = false;
            clearBtn.disabled = false;
            return;
        }

        var currentMsg = resetData.observation ? resetData.observation.echoed_message : '';

        for (var step = 1; step <= TOTAL; step++) {
            // Bot decides
            var answer, source;
            if (botBrain[step]) {
                answer = botBrain[step];
                source = 'memory';
            } else {
                answer = guesses[Math.floor(Math.random() * guesses.length)];
                source = 'guess';
            }

            showChallenge(currentMsg, answer, source, step);
            addLog('#' + step + ': "' + answer + '" (' + source + ')');

            await sleep(400);

            // Submit answer
            var stepData;
            try {
                var stepResp = await fetch('/step', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: { message: answer } })
                });
                stepData = await stepResp.json();
            } catch (err) {
                addLog('ERROR: Step failed! ' + err.message, 'log-wrong');
                break;
            }

            var obs = stepData.observation ? stepData.observation.echoed_message : '';
            var reward = stepData.reward || 0;

            if (obs.indexOf('CORRECT') >= 0) {
                addLog('  ✅ Correct!', 'log-correct');
                botBrain[step] = answer;
                showFeedback('✅ #' + step + ' Correct!', true);
            } else {
                var correctAns = '';
                var m = obs.match(/The answer was:\s*(.*)/);
                if (m) correctAns = m[1].trim();
                addLog('  ❌ Wrong' + (correctAns ? ' → learned: "' + correctAns + '"' : ''), 'log-wrong');
                if (correctAns) {
                    botBrain[step] = correctAns;
                    addLog('  🧠 Stored in memory!', 'log-bot');
                }
                showFeedback('❌ #' + step + ' Wrong (learned!)', false);
            }

            // Update stats from message
            var cMatch = obs.match(/✅\s*(\d+)/);
            var wMatch = obs.match(/❌\s*(\d+)/);
            setStats(reward, cMatch ? cMatch[1] : 0, wMatch ? wMatch[1] : 0, step);
            updateBrain();

            if (stepData.done) {
                await sleep(200);
                showModal(stepData);
                break;
            }

            currentMsg = obs;
            await sleep(100);
        }

        // History
        var hist = document.getElementById('history');
        if (hist) {
            if (runCount === 1) hist.innerHTML = '';
            var e = document.createElement('div');
            e.className = 'history-entry';
            e.innerHTML = '#' + runCount + ': ' + document.getElementById('score').textContent + 'pts (' + document.getElementById('correct').textContent + '/' + TOTAL + ')';
            hist.prepend(e);
        }

        trainBtn.disabled = false;
        clearBtn.disabled = false;
    }

    function setStats(score, correct, wrong, step) {
        var s = document.getElementById('score'); if (s) s.textContent = parseFloat(score).toFixed(1);
        var c = document.getElementById('correct'); if (c) c.textContent = correct;
        var w = document.getElementById('wrong'); if (w) w.textContent = wrong;
        var p = document.getElementById('progress'); if (p) p.style.width = (step / TOTAL * 100) + '%';
        var pt = document.getElementById('progress-text'); if (pt) pt.textContent = step + ' / ' + TOTAL;
    }

    function addLog(text, cls) {
        var log = document.getElementById('training-log');
        if (!log) return;
        var span = document.createElement('span');
        if (cls) span.className = cls;
        span.textContent = text;
        log.appendChild(span);
        log.appendChild(document.createElement('br'));
        log.scrollTop = log.scrollHeight;
    }

    function showFeedback(text, isCorrect) {
        var fb = document.getElementById('feedback');
        if (!fb) return;
        fb.textContent = text;
        fb.className = 'feedback ' + (isCorrect ? 'correct-fb' : 'wrong-fb');
    }

    function showChallenge(msg, botAnswer, source, stepNum) {
        var area = document.getElementById('challenge');
        if (!area) return;

        // Parse question from message
        var lines = msg.split('\n');
        var qLines = [], collecting = false;
        for (var i = 0; i < lines.length; i++) {
            if (lines[i].indexOf('━━━') >= 0) { if (!collecting) { collecting = true; continue; } else break; }
            if (collecting) qLines.push(lines[i]);
        }
        var question = qLines.join('\n').trim() || msg;

        // Format code blocks
        var formatted = question
            .replace(/```python\n([\s\S]*?)```/g, function(m, c) { return '<div class="code-block">' + esc(c.trim()) + '</div>'; })
            .replace(/```([\s\S]*?)```/g, function(m, c) { return '<div class="code-block">' + esc(c.trim()) + '</div>'; })
            .replace(/\n/g, '<br>');

        var srcLabel = source === 'memory' ? '🧠 From Memory' : '🎲 Random Guess';

        area.innerHTML =
            '<div class="challenge-card">' +
            '<div class="challenge-meta"><span class="badge category">Challenge ' + stepNum + '/' + TOTAL + '</span></div>' +
            '<div class="challenge-question">' + formatted + '</div>' +
            '<div class="bot-answer"><div class="bot-answer-label">🤖 BOT ANSWER (' + srcLabel + ')</div>' +
            '<div class="bot-answer-text">' + esc(botAnswer) + '</div></div></div>';
    }

    function showModal(data) {
        var mc = document.getElementById('modal-content');
        var ov = document.getElementById('overlay');
        if (!mc || !ov) return;
        var rw = data.reward || 0;
        var msg = data.observation ? data.observation.echoed_message : '';
        var rm = msg.match(/Rank:\s*(.*)/);
        var am = msg.match(/Accuracy:\s*(.*)/);
        mc.innerHTML =
            '<div style="font-size:2.5rem">🤖</div>' +
            '<h2 style="margin:0.5rem 0">Run #' + runCount + ' Done!</h2>' +
            '<p style="font-size:1.8rem;font-weight:800;color:#6366f1">' + rw.toFixed(1) + ' pts</p>' +
            (am ? '<p style="color:#94a3b8">' + am[1] + '</p>' : '') +
            (rm ? '<p style="font-weight:700;margin-top:0.3rem">' + rm[1] + '</p>' : '') +
            '<p style="color:#f59e0b;margin-top:0.5rem;font-size:0.8rem">Brain: ' + Object.keys(botBrain).length + '/' + TOTAL + '</p>';
        ov.classList.remove('hidden');
    }

    function clearCodeBot() {
        botBrain = {}; runCount = 0; updateBrain();
        var h = document.getElementById('history'); if (h) h.innerHTML = '<span class="muted-text">No runs yet</span>';
        var l = document.getElementById('training-log'); if (l) l.innerHTML = '';
        var fb = document.getElementById('feedback'); if (fb) fb.classList.add('hidden');
        setStats(0, 0, 0, 0);
        var area = document.getElementById('challenge');
        if (area) area.innerHTML = '<div class="welcome-state"><div style="font-size:4rem;margin-bottom:1rem">🧹</div><h2>Memory Cleared!</h2><p style="color:#64748b;margin-top:0.5rem">Train again from scratch!</p></div>';
    }

    updateBrain();

    // ================================================================
    //  CUSTOM BOT TRAINER
    // ================================================================
    var customData = [
        { q: "What is Python?", a: "Python is a high-level, interpreted programming language known for its simple syntax and readability." },
        { q: "What is a variable?", a: "A variable is a named container that stores a value in memory. Example: x = 10" },
        { q: "What is a function?", a: "A function is a reusable block of code that performs a specific task. Defined with 'def' keyword." },
        { q: "What is a loop?", a: "A loop repeats a block of code multiple times. Python has 'for' loops and 'while' loops." },
        { q: "What is a list?", a: "A list is an ordered, mutable collection of items. Example: [1, 2, 3]" },
        { q: "What is a dictionary?", a: "A dictionary stores key-value pairs. Example: {'name': 'Alice', 'age': 25}" },
        { q: "What is an if statement?", a: "An if statement executes code only when a condition is True. Example: if x > 0: print('positive')" },
        { q: "What is a class?", a: "A class is a blueprint for creating objects. It bundles data and functions together." }
    ];
    var customBrain = {};
    var isTrained = false;

    var tdQ = document.getElementById('td-question');
    var tdA = document.getElementById('td-answer');
    var addBtn = document.getElementById('add-data-btn');
    var dataListEl = document.getElementById('data-list');
    var countEl = document.getElementById('custom-data-count');
    var cTrainBtn = document.getElementById('custom-train-btn');
    var cClearBtn = document.getElementById('custom-clear-btn');
    var chatMsgs = document.getElementById('chat-messages');
    var chatIn = document.getElementById('chat-input');
    var chatSend = document.getElementById('chat-send');
    var botNameIn = document.getElementById('bot-name');
    var botNameDisp = document.getElementById('bot-name-display');

    if (botNameIn) botNameIn.oninput = function() { if (botNameDisp) botNameDisp.textContent = botNameIn.value || 'MyBot'; };

    if (addBtn) addBtn.onclick = function() {
        var q = tdQ.value.trim(), a = tdA.value.trim();
        if (!q || !a) return;
        customData.push({ q: q, a: a });
        tdQ.value = ''; tdA.value = ''; tdQ.focus();
        renderData();
    };

    if (tdQ) tdQ.onkeydown = function(e) { if (e.key === 'Enter') tdA.focus(); };

    function renderData() {
        if (!dataListEl) return;
        if (customData.length === 0) {
            dataListEl.innerHTML = '<p class="muted-text" style="padding:1rem">Add data pairs →</p>';
            if (countEl) countEl.textContent = '0 pairs';
            if (cTrainBtn) cTrainBtn.disabled = true;
            return;
        }
        var html = '';
        for (var i = 0; i < customData.length; i++) {
            html += '<div class="data-item"><button class="data-remove" data-i="' + i + '">✕</button><div class="data-q">Q: ' + esc(customData[i].q) + '</div><div class="data-a">A: ' + esc(customData[i].a) + '</div></div>';
        }
        dataListEl.innerHTML = html;
        if (countEl) countEl.textContent = customData.length + ' pairs';
        if (cTrainBtn) cTrainBtn.disabled = false;

        dataListEl.querySelectorAll('.data-remove').forEach(function(b) {
            b.onclick = function() { customData.splice(parseInt(b.dataset.i), 1); renderData(); };
        });
    }

    // Train custom bot
    if (cTrainBtn) cTrainBtn.onclick = async function() {
        if (customData.length === 0) return;
        isTrained = false;
        customBrain = {};
        var name = (botNameIn ? botNameIn.value : '') || 'MyBot';

        if (chatMsgs) chatMsgs.innerHTML = '<div class="chat-msg bot-msg"><span class="chat-who">⚙️ System</span><span class="chat-text">Training ' + esc(name) + ' on ' + customData.length + ' data pairs...</span></div>';

        for (var i = 0; i < customData.length; i++) {
            await sleep(200);
            customBrain[i] = customData[i];
            if (chatMsgs) {
                chatMsgs.innerHTML += '<div class="chat-msg bot-msg"><span class="chat-who">⚙️</span><span class="chat-text">✅ Learned: "' + esc(customData[i].q.substring(0, 50)) + '"</span></div>';
                chatMsgs.scrollTop = chatMsgs.scrollHeight;
            }
        }

        await sleep(200);
        isTrained = true;
        if (chatMsgs) {
            chatMsgs.innerHTML += '<div class="chat-msg bot-msg"><span class="chat-who">🤖 ' + esc(name) + '</span><span class="chat-text">Training complete! I learned ' + customData.length + ' things. Ask me anything!</span></div>';
            chatMsgs.scrollTop = chatMsgs.scrollHeight;
        }
        if (chatIn) { chatIn.disabled = false; chatIn.focus(); }
        if (chatSend) chatSend.disabled = false;
    };

    // Chat
    function doChat() {
        var msg = chatIn.value.trim();
        if (!msg || !isTrained) return;
        var name = (botNameIn ? botNameIn.value : '') || 'MyBot';

        chatMsgs.innerHTML += '<div class="chat-msg user-msg"><span class="chat-who">👤 You</span><span class="chat-text">' + esc(msg) + '</span></div>';
        chatIn.value = '';

        var answer = findAnswer(msg);
        setTimeout(function() {
            chatMsgs.innerHTML += '<div class="chat-msg bot-msg"><span class="chat-who">🤖 ' + esc(name) + '</span><span class="chat-text">' + esc(answer) + '</span></div>';
            chatMsgs.scrollTop = chatMsgs.scrollHeight;
        }, 300);
    }

    function findAnswer(input) {
        var words = input.toLowerCase().split(/[\s?!.,]+/).filter(function(w) { return w.length > 2; });
        var bestScore = 0, bestAns = "I haven't been trained on this yet. Try asking about something in my training data!";

        for (var i = 0; i < customData.length; i++) {
            var qWords = customData[i].q.toLowerCase().split(/[\s?!.,]+/).filter(function(w) { return w.length > 2; });
            var score = 0;
            for (var j = 0; j < words.length; j++) {
                for (var k = 0; k < qWords.length; k++) {
                    if (qWords[k].indexOf(words[j]) >= 0 || words[j].indexOf(qWords[k]) >= 0) { score++; break; }
                }
            }
            var norm = score / Math.max(words.length, 1);
            if (norm > bestScore) { bestScore = norm; bestAns = customData[i].a; }
        }

        return bestScore >= 0.15 ? bestAns : "I haven't been trained on this topic. Try asking about Python, variables, functions, loops, lists, dictionaries, classes, or if statements!";
    }

    if (chatSend) chatSend.onclick = doChat;
    if (chatIn) chatIn.onkeydown = function(e) { if (e.key === 'Enter') doChat(); };

    // Clear custom
    if (cClearBtn) cClearBtn.onclick = function() {
        customData = [];
        customBrain = {};
        isTrained = false;
        renderData();
        if (chatMsgs) chatMsgs.innerHTML = '<div class="chat-msg bot-msg"><span class="chat-who">🤖 Bot</span><span class="chat-text">All training cleared! Add data and train me again.</span></div>';
        if (chatIn) chatIn.disabled = true;
        if (chatSend) chatSend.disabled = true;
    };

    // Init custom page
    renderData();
});
