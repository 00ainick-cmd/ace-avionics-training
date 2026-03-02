
    // ============================================================
    // ACE AVIONICS — DRILL MODE (practice.html)
    // Immediate-feedback multiple-choice drill
    // ============================================================

    // ---- SYSTEM INTEGRATION ----
    function closeActivity() {
      const backUrl = new URLSearchParams(location.search).get('back') || '../practice.html';
      if (window.self !== window.top) {
        window.parent.postMessage({ type: 'ACE_CLOSE' }, '*');
      } else {
        window.location.href = backUrl;
      }
    }

    // ---- CONSTANTS ----
    const LESSON_ID = (function () {
      const p = new URLSearchParams(location.search);
      return p.get('lesson') || p.get('id') || 'drill';
    })();

    const ACE_COMMENTS_CORRECT = [
      "Nailed it. That's the kind of precision that keeps aircraft airworthy.",
      "Exactly right. Solid knowledge of that regulation.",
      "Correct — and knowing why is what separates good technicians from great ones.",
      "That's the one. Keep that in your memory bank.",
      "Spot on. You're building the right foundations.",
      "Perfect. Keep this momentum going.",
      "That's correct. The FAA would be pleased.",
      "Right answer. Safety starts with knowing your regs cold.",
      "Excellent recall. That one catches a lot of techs off-guard.",
      "Affirmative. That's exactly what you need to know for the exam."
    ];

    const ACE_COMMENTS_WRONG = [
      "Not quite — but now you know. Read the explanation carefully.",
      "Common miss. The explanation breaks down exactly why the right answer works.",
      "Easy to mix up. Spend a moment with the explanation and it'll stick.",
      "That one trips people up. Study the logic in the explanation.",
      "Good guess, wrong regulation. The correct answer is worth memorizing.",
      "It happens. The key is understanding the reasoning — check the explanation.",
      "Worth noting for your weak list. Review this concept before the exam.",
      "No worries — this is drill mode. Mistakes here mean mastery later.",
      "Close, but not quite. Re-read the explanation and flag this one.",
      "These details matter in the field. Take a moment to absorb the correct answer."
    ];

    const MOTIVATIONAL_MSGS = [
      "You're building something real.",
      "Excellence is a habit.",
      "Safety first, always.",
      "Knowledge is power.",
      "Precision matters.",
      "Stay focused.",
      "Keep it up.",
      "You've got this.",
      "One question at a time.",
      "Every rep counts."
    ];

    // ---- STATE ----
    let state = {
      questions: [],
      drillQueue: [],
      currentIdx: 0,
      answered: false,
      sessionStats: { seen: 0, correct: 0, missed: 0 },
      categoryStats: {},   // { catId: { correct, total, name } }
      loStats: {},          // { loId: { text, correct, total, category } }
      questionTimes: [],    // array of ms per question
      questionStartTime: 0, // timestamp when current question was shown
      answerLog: [],        // { qIdx, question, selected, correct, isCorrect, lo, category }
      weakList: [],
      lastResults: null,
      konamiProgress: 0,
      sessionStart: Date.now()
    };

    // ---- DATA LOADING ----
    // ---- DATA LOADING ----
    const DRILL_CATEGORIES = [
      { id: 'cat-1-maintenance-regs', num: 'MOD 1', name: 'Maintenance Regs', iconColor: '#D4A853', path: '../training/caet/mod1-maintenance-regs/data/questions.json', icon: '📋' },
      { id: 'cat-2-basic-electrical', num: 'MOD 2', name: 'Basic Electrical', iconColor: '#22d3ee', path: '../training/caet/mod2-basic-electrical/data/questions.json', icon: '⚡' },
      { id: 'cat-3-cns-systems', num: 'MOD 3', name: 'CNS Systems', iconColor: '#34d399', path: '../training/caet/mod3-cns-systems/data/questions.json', icon: '📡' },
      { id: 'cat-4-flight-instruments', num: 'MOD 4', name: 'Flight Instruments', iconColor: '#f472b6', path: '../training/caet/mod4-flight-instruments/data/questions.json', icon: '✈️' },
      { id: 'cat-5-digital-databus', num: 'MOD 5', name: 'Digital Databuses', iconColor: '#a78bfa', path: '../training/caet/mod5-digital-databus/data/questions.json', icon: '💻' },
      { id: 'cat-6-aircraft-wiring', num: 'MOD 6', name: 'Aircraft Wiring', iconColor: '#fb923c', path: '../training/caet/mod6-aircraft-wiring/data/questions.json', icon: '🔌' },
      { id: 'cat-7-tools-test-equipment', num: 'MOD 7', name: 'Tools & Test Eq.', iconColor: '#facc15', path: '../training/caet/mod7-tools-test-equipment/data/questions.json', icon: '🛠️' },
      { id: 'cat-8-shop-safety', num: 'MOD 8', name: 'Shop Safety', iconColor: '#ef4444', path: '../training/caet/mod8-shop-safety/data/questions.json', icon: '🧯' }
    ];

    async function loadSpecificData(url) {
      try {
        console.log('[ACE Drill] Loading specific data:', url);
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        let targetQuestions = data.questions || [];
        if (!Array.isArray(targetQuestions)) {
          if (Array.isArray(data)) targetQuestions = data;
        }

        const validQuestions = [];
        targetQuestions.forEach(q => {
          let entry;
          if (q.multipleChoice) {
            const mc = q.multipleChoice;
            const opts = mc.choices || mc.options;
            if (!mc.question || !opts || opts.length < 2) return;
            entry = {
              id: q.id,
              question: mc.question,
              options: opts,
              correct: mc.correctIndex !== undefined ? mc.correctIndex : 0,
              explanation: mc.explanation || q.explanation || '',
              category: q.category || 'general',
              tags: q.tags || [],
              difficulty: q.difficulty || 'medium',
              learningObjective: q.learningObjective || null,
              astmRef: q.astmRef || null
            };
          } else {
            const opts = q.options || q.choices;
            if (!q.question || !opts || opts.length < 2) return;
            entry = {
              id: q.id,
              question: q.question,
              options: opts,
              correct: q.correct !== undefined ? q.correct : 0,
              explanation: q.explanation || '',
              category: q.category || 'general',
              tags: q.tags || [],
              difficulty: q.difficulty || 'medium',
              learningObjective: q.learningObjective || null,
              astmRef: q.astmRef || null
            };
          }
          validQuestions.push(entry);
        });
        return validQuestions;
      } catch (e) {
        console.error('Failed to load data from ' + url, e);
        return [];
      }
    }

    async function initApp() {
      const params = new URLSearchParams(location.search);
      const directData = params.get('data');

      window._categories = DRILL_CATEGORIES;

      if (directData) {
        // Direct launch mode
        const qs = await loadSpecificData(directData);
        if (qs.length === 0) {
          alert("Failed to load questions from " + directData);
          return;
        }
        state.questions = qs;

        document.getElementById('launchPanel').style.display = 'none';
        state.drillQueue = shuffleArray([...qs]);

        let titleParam = params.get('title') || 'Module Drill';
        document.getElementById('drillCategoryTag').textContent = titleParam;

        document.getElementById('drillOverlay').classList.add('active');
        document.getElementById('btnEndDrill').classList.add('visible');

        loadSessionStats();
        bindEvents();
        startTimer();
        loadQuestion();
      } else {
        // Normal mode (show Launch Screen)
        renderCategories();
        loadSessionStats();
        bindEvents();
        startTimer();
      }
    }

    // Kick off initialization
    initApp();

    // ---- RENDER CATEGORIES ----
    function renderCategories() {
      const grid = document.getElementById('categoryGrid');
      grid.innerHTML = window._categories.map(cat => `
    <div class="category-card" data-cat="${cat.id}">
      <div class="category-icon" style="color:${cat.iconColor}">${cat.icon}</div>
      <div class="category-name">${cat.name}</div>
      <div class="category-count">${cat.num}</div>
    </div>
  `).join('');
      grid.querySelectorAll('.category-card').forEach(card => {
        card.addEventListener('click', () => selectCategory(card.dataset.cat));
      });
    }

    let selectedCatIds = [];

    function selectCategory(catId) {
      const idx = selectedCatIds.indexOf(catId);
      if (idx >= 0) {
        selectedCatIds.splice(idx, 1); // deselect
      } else {
        selectedCatIds.push(catId); // add to selection
      }
      document.querySelectorAll('.category-card').forEach(c => {
        c.classList.toggle('selected', selectedCatIds.includes(c.dataset.cat));
      });
      // Update summary
      const summaryEl = document.getElementById('selectedSummary');
      if (selectedCatIds.length === 0) {
        summaryEl.innerHTML = 'Select one or more categories to begin';
        document.getElementById('categoryBadge').textContent = 'None';
      } else {
        const names = selectedCatIds.map(id => {
          const cat = window._categories.find(c => c.id === id);
          return cat ? cat.name.split(' ').slice(0, 2).join(' ') : id;
        });
        summaryEl.innerHTML = `<strong>${selectedCatIds.length}</strong> ${selectedCatIds.length === 1 ? 'category' : 'categories'} selected`;
        document.getElementById('categoryBadge').textContent = selectedCatIds.length === 1 ? names[0] : `${selectedCatIds.length} categories`;
      }
      document.getElementById('btnStart').disabled = selectedCatIds.length === 0;
      // Sync Select All / Clear All button text
      const allIds = window._categories.map(c => c.id);
      const saBtn = document.getElementById('btnSelectAll');
      if (saBtn) saBtn.textContent = (allIds.length > 0 && allIds.every(id => selectedCatIds.includes(id))) ? 'Clear All' : 'Select All';
    }

    // ---- SESSION TIMER ----
    function startTimer() {
      function fmt(s) {
        const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), ss = s % 60;
        return h > 0
          ? `${h}:${String(m).padStart(2, '0')}:${String(ss).padStart(2, '0')}`
          : `${String(m).padStart(2, '0')}:${String(ss).padStart(2, '0')}`;
      }
      setInterval(() => {
        const el = document.getElementById('sessionTimeValue');
        if (el) el.textContent = fmt(Math.floor((Date.now() - state.sessionStart) / 1000));
      }, 1000);
    }

    // ---- HANGAR DOOR TRANSITION ----
    function doorsTransition(callback, midCallback) {
      const overlay = document.getElementById('hangarDoorsOverlay');
      overlay.classList.add('active');
      setTimeout(() => overlay.classList.add('doors-closed'), 80);
      setTimeout(() => { if (midCallback) midCallback(); }, 1100);
      setTimeout(() => overlay.classList.remove('doors-closed'), 1200);
      setTimeout(() => {
        overlay.classList.remove('active');
        if (callback) callback();
      }, 2300);
    }

    // ---- START DRILL ----
    async function startDrill() {
      if (selectedCatIds.length === 0) return;

      const startBtn = document.getElementById('btnStart');
      if (startBtn) startBtn.disabled = true;

      // Update drill header tag
      const tagText = selectedCatIds.length === 1
        ? window._categories.find(c => c.id === selectedCatIds[0])?.name || selectedCatIds[0]
        : `${selectedCatIds.length} Categories`;
      document.getElementById('drillCategoryTag').textContent = tagText;

      // Door transition: show drill overlay
      doorsTransition(
        async () => {
          // Load specific data files dynamically
          let pool = [];
          for (const catId of selectedCatIds) {
            const cat = window._categories.find(c => c.id === catId);
            if (cat && cat.path) {
              const qs = await loadSpecificData(cat.path);
              pool.push(...qs);
            }
          }

          if (pool.length === 0) {
            alert('No questions loaded. Check network or module selection.');
            if (startBtn) startBtn.disabled = false;
            return;
          }

          // Reset per-drill stats (keep session totals)
          state.categoryStats = {};
          state.loStats = {};
          state.questionTimes = [];
          state.answerLog = [];
          state.weakList = [];
          state.currentIdx = 0;
          state.answered = false;

          state.drillQueue = shuffleArray(pool);
          loadQuestion();
        },
        () => {
          document.getElementById('drillOverlay').classList.add('active');
          document.getElementById('btnEndDrill').classList.add('visible');
          if (startBtn) startBtn.disabled = false;
        }
      );
    }

    // ---- LOAD QUESTION ----
    function loadQuestion() {
      if (state.currentIdx >= state.drillQueue.length) {
        endDrill();
        return;
      }

      const q = state.drillQueue[state.currentIdx];
      state.answered = false;
      state.questionStartTime = Date.now();

      // Progress bar
      const pct = Math.round((state.currentIdx / state.drillQueue.length) * 100);
      document.getElementById('drillProgressFill').style.width = pct + '%';
      document.getElementById('drillProgressText').textContent = `${state.currentIdx + 1} / ${state.drillQueue.length}`;
      document.getElementById('qNumber').textContent = `Question ${state.currentIdx + 1} of ${state.drillQueue.length}`;

      // Question text
      document.getElementById('qText').textContent = q.question;

      // Tags
      const tagsEl = document.getElementById('qTags');
      tagsEl.innerHTML = q.tags.map(t => `<span class="q-tag">${t}</span>`).join('');

      // Reset card state
      const qCard = document.getElementById('qCard');
      qCard.className = 'q-card anim-in';

      // Reset: AcePopup self-closes on next; no inline elements to reset

      // Render options
      const LETTERS = ['A', 'B', 'C', 'D', 'E'];
      const optGrid = document.getElementById('optionsGrid');
      optGrid.innerHTML = q.options.map((opt, i) => {
        // Strip leading "A. " style prefix if present
        const cleanOpt = opt.replace(/^[A-D]\.\s*/, '');
        return `
      <button class="option-btn" data-idx="${i}" onclick="selectAnswer(${i})">
        <div class="option-letter">${LETTERS[i] || i}</div>
        <div class="option-text">${cleanOpt}</div>
      </button>`;
      }).join('');
    }

    // ---- SELECT ANSWER ----
    function selectAnswer(selectedIdx) {
      if (state.answered) return;
      state.answered = true;

      const q = state.drillQueue[state.currentIdx];
      const isCorrect = selectedIdx === q.correct;
      const LETTERS = ['A', 'B', 'C', 'D', 'E'];

      // Update stats
      state.sessionStats.seen++;
      if (isCorrect) {
        state.sessionStats.correct++;
      } else {
        state.sessionStats.missed++;
        if (!state.weakList.find(w => w.id === q.id)) {
          state.weakList.push(q);
        }
      }
      updateStatsDisplay();

      // Track category stats
      const catId = q.category;
      if (!state.categoryStats[catId]) {
        const cat = window._categories.find(c => c.id === catId);
        state.categoryStats[catId] = { correct: 0, total: 0, name: cat ? cat.name : catId };
      }
      state.categoryStats[catId].total++;
      if (isCorrect) state.categoryStats[catId].correct++;

      // Track LO stats — use question id as key, fullObjective for display
      const loId = q.id || q.learningObjective || 'unknown';
      if (!state.loStats[loId]) {
        state.loStats[loId] = {
          text: q.fullObjective || q.learningObjective || q.question || q.id,
          shortText: q.learningObjective || q.id,
          correct: 0, total: 0, category: q.category
        };
      }
      state.loStats[loId].total++;
      if (isCorrect) state.loStats[loId].correct++;

      // Track question timing
      const elapsed = Date.now() - (state.questionStartTime || Date.now());
      state.questionTimes.push(elapsed);

      // Log answer for review
      state.answerLog.push({
        qIdx: state.currentIdx,
        question: q.question,
        options: q.options,
        selected: selectedIdx,
        correct: q.correct,
        isCorrect: isCorrect,
        lo: q.learningObjective || '',
        category: q.category,
        elapsed: elapsed
      });

      // Style option buttons
      const btns = document.querySelectorAll('.option-btn');
      btns.forEach((btn, i) => {
        btn.disabled = true;
        if (i === q.correct) {
          btn.classList.add('correct');
          if (i === selectedIdx) {
            btn.classList.add('pulse');
          }
        } else if (i === selectedIdx && !isCorrect) {
          btn.classList.add('wrong', 'shake');
        } else {
          btn.classList.add('dimmed');
        }
      });

      // Update question card state
      const qCard = document.getElementById('qCard');
      qCard.className = isCorrect ? 'q-card answered-correct' : 'q-card answered-wrong';

      // Show ACE popup with per-question feedback
      const aceComments = isCorrect ? ACE_COMMENTS_CORRECT : ACE_COMMENTS_WRONG;
      const aceComment = aceComments[Math.floor(Math.random() * aceComments.length)];
      const isLast = (state.currentIdx + 1 >= state.drillQueue.length);
      AcePopup.show({
        correct: isCorrect,
        explanation: q.explanation || '',
        correctAnswer: isCorrect ? null : `${LETTERS[q.correct]}. ${q.options[q.correct]}`,
        aceComment: aceComment,
        sprite: isCorrect ? 'happy' : 'concerned',
        nextLabel: isLast ? 'See Results →' : 'Next Question →',
        onNext: () => nextQuestion()
      });

      // Analytics
      sendAnalyticsEvent('question_answered', {
        correct: isCorrect,
        category: q.category,
        learningObjective: q.learningObjective,
        module: 'drill'
      });

      // Achievement milestones
      if (state.sessionStats.correct > 0 && state.sessionStats.correct % 10 === 0) {
        showAchievement(`${state.sessionStats.correct} correct answers!`);
      }

      // ProgressTracker
      try {
        if (typeof ProgressTracker !== 'undefined' && q.id) {
          ProgressTracker.recordAnswer(LESSON_ID, 'drill', q.id, isCorrect, q.learningObjective, q.category);
          ProgressTracker.save();
        }
      } catch (e) { }

      // LO Mastery Tracker
      if (q.learningObjective && window.LOMasteryTracker) {
        window.LOMasteryTracker.record(LESSON_ID, q.learningObjective, isCorrect, 'drill');
      }

      updateWeakList();
      saveSessionStats();
    }

    // ---- NEXT QUESTION ----
    function nextQuestion() {
      state.currentIdx++;
      if (state.currentIdx >= state.drillQueue.length) {
        endDrill();
      } else {
        loadQuestion();
        // Scroll back to top of drill
        document.getElementById('drillOverlay').scrollTo({ top: 0, behavior: 'smooth' });
      }
    }

    // ---- END DRILL ----
    function endDrill() {
      state.lastResults = {
        seen: state.sessionStats.seen,
        correct: state.sessionStats.correct,
        missed: state.sessionStats.missed,
        categoryStats: { ...state.categoryStats },
        loStats: { ...state.loStats },
        questionTimes: [...state.questionTimes],
        answerLog: [...state.answerLog],
        weakList: [...state.weakList]
      };

      doorsTransition(
        () => {
          document.getElementById('drillOverlay').classList.remove('active');
          document.getElementById('btnEndDrill').classList.remove('visible');
          showResults();
        },
        () => {
          // nothing mid-transition
        }
      );
    }

    // ---- SHOW RESULTS ----
    function showResults() {
      const r = state.lastResults;
      const pct = r.seen > 0 ? Math.round((r.correct / r.seen) * 100) : 0;

      // Load previous session data for comparison
      const prevSession = loadPreviousSession();

      // --- 1. HEADER: ACE sprite + title + score ring ---
      let mood = 'idle';
      let title = 'Drill Complete!';
      if (pct >= 90) { mood = 'proud'; title = 'Outstanding!'; }
      else if (pct >= 75) { mood = 'happy'; title = 'Well Done!'; }
      else if (pct >= 60) { mood = 'idle'; title = 'Getting There!'; }
      else if (pct >= 45) { mood = 'concerned'; title = 'Keep Drilling!'; }
      else { mood = 'disgust'; title = 'Time to Study!'; }

      document.getElementById('resAceSprite').innerHTML =
        `<img src="./ace-sprites/ace-192-${mood}.png" alt="ACE">`;
      document.getElementById('resultsTitle').textContent = title;
      document.getElementById('resultsSubtitle').textContent = 'TRAINING SESSION SUMMARY';

      // Score ring
      document.getElementById('scorePct').textContent = pct + '%';
      const ringFill = document.getElementById('scoreRingFill');
      const circumference = 427;
      const offset = circumference - (pct / 100) * circumference;
      ringFill.style.stroke = pct >= 75 ? 'var(--success)' : pct >= 50 ? 'var(--warning)' : 'var(--danger)';
      ringFill.style.strokeDashoffset = circumference;
      requestAnimationFrame(() => {
        requestAnimationFrame(() => { ringFill.style.strokeDashoffset = offset; });
      });

      // --- 2. STATS ROW (4 cards) ---
      document.getElementById('resSeen').textContent = r.seen;
      document.getElementById('resCorrect').textContent = r.correct;
      document.getElementById('resMissed').textContent = r.missed;

      // Avg time per question
      const avgMs = r.questionTimes && r.questionTimes.length > 0
        ? r.questionTimes.reduce((a, b) => a + b, 0) / r.questionTimes.length : 0;
      const avgSec = Math.round(avgMs / 1000);
      document.getElementById('resAvgTime').textContent = avgMs > 0 ? avgSec + 's' : '--';

      // Delta indicators vs previous session
      renderDelta('resDeltaSeen', r.seen, prevSession ? prevSession.seen : null);
      renderDelta('resDeltaCorrect', r.correct, prevSession ? prevSession.correct : null);
      renderDelta('resDeltaMissed', r.missed, prevSession ? prevSession.missed : null, true);
      renderDelta('resDeltaTime', avgSec, prevSession ? prevSession.avgTime : null, true);

      // --- 3. ACE MENTOR FEEDBACK CARD ---
      renderMentorFeedback(pct, mood, r);

      // --- 4. LEARNING OBJECTIVE MASTERY ---
      renderLOMastery(r);

      // --- 5. RADAR CHART ---
      const catEntries = Object.entries(r.categoryStats);
      if (catEntries.length >= 3) {
        document.getElementById('radarSection').style.display = '';
        setTimeout(() => drawResRadarChart(r.categoryStats), 200);
      } else {
        document.getElementById('radarSection').style.display = 'none';
      }

      // --- 6. TOPIC BREAKDOWN (enhanced) ---
      const topicList = document.getElementById('topicList');
      if (catEntries.length > 0) {
        topicList.innerHTML = catEntries.map(([catId, cs]) => {
          const catPct = cs.total > 0 ? Math.round((cs.correct / cs.total) * 100) : 0;
          const color = catPct >= 75 ? 'var(--success)' : catPct >= 50 ? 'var(--warning)' : 'var(--danger)';
          return `
        <div class="topic-row">
          <div class="topic-name">${cs.name}</div>
          <div class="topic-bar-wrap">
            <div class="topic-bar-fill" style="width:${catPct}%;background:${color}"></div>
          </div>
          <div class="topic-pct" style="color:${color}">${catPct}%</div>
          <div class="topic-count">${cs.correct}/${cs.total}</div>
        </div>`;
        }).join('');
      } else {
        topicList.innerHTML = '<p style="font-size:0.8rem;color:var(--text-muted);font-style:italic;">No category data available.</p>';
      }

      // --- 7. WEAK AREAS ---
      const weakSection = document.getElementById('weakAreasSection');
      const weakList2 = document.getElementById('weakAreasList');
      const weakCats = catEntries.filter(([, cs]) => cs.total > 0 && (cs.correct / cs.total) < 0.6);
      if (weakCats.length > 0) {
        weakSection.style.display = 'block';
        weakList2.innerHTML = weakCats.map(([, cs]) => `
      <div class="weak-area-item">
        <div class="weak-dot"></div>
        <span><strong>${cs.name}</strong> — ${Math.round((cs.correct / cs.total) * 100)}% (${cs.correct}/${cs.total} correct). Review this topic.</span>
      </div>`).join('');
      } else {
        weakSection.style.display = 'none';
      }

      // --- 8. SESSION HISTORY SPARKLINE ---
      saveAndRenderSessionHistory(pct, r.seen);

      // Show view results button in sidebar
      document.getElementById('btnViewResults').style.display = 'block';

      // Open results
      document.getElementById('resultsOverlay').classList.add('active');

      // Report completion
      reportDrillCompletion(pct, r);
    }

    // ---- DELTA INDICATOR ----
    function renderDelta(elId, current, previous, invertBetter) {
      const el = document.getElementById(elId);
      if (!el) return;
      if (previous === null || previous === undefined) {
        el.textContent = '';
        return;
      }
      const diff = current - previous;
      if (diff === 0) {
        el.textContent = '= same';
        el.className = 'res-stat-delta same';
      } else {
        const isGood = invertBetter ? diff < 0 : diff > 0;
        el.textContent = (diff > 0 ? '+' : '') + diff + ' vs last';
        el.className = 'res-stat-delta ' + (isGood ? 'up' : 'down');
      }
    }

    // ---- PREVIOUS SESSION (from localStorage) ----
    function loadPreviousSession() {
      try {
        const key = `ace_drill_history_${LESSON_ID}`;
        const raw = localStorage.getItem(key);
        if (!raw) return null;
        const arr = JSON.parse(raw);
        if (!arr || arr.length === 0) return null;
        return arr[arr.length - 1]; // most recent completed session
      } catch (e) { return null; }
    }

    // ---- ACE MENTOR FEEDBACK ----
    function renderMentorFeedback(pct, mood, r) {
      // Sprite
      document.getElementById('resMentorSprite').innerHTML =
        `<img src="./ace-sprites/ace-192-${mood}.png" alt="ACE">`;

      // Border color by mood
      const card = document.getElementById('resMentorCard');
      const accentColor = pct >= 75 ? 'var(--success)' : pct >= 50 ? 'var(--warning)' : 'var(--danger)';
      card.style.borderColor = accentColor === 'var(--success)' ? 'rgba(63,185,80,0.4)' : accentColor === 'var(--warning)' ? 'rgba(227,179,65,0.4)' : 'rgba(248,81,73,0.4)';

      // Speech text
      const speeches = {
        proud: [
          "Absolutely outstanding work. You're demonstrating real mastery of this material. Keep pushing for perfection.",
          "Top-tier performance. You clearly know your regulations. Stay sharp and keep drilling to lock it in.",
          "That's the kind of score that gets you certified. Exceptional recall and accuracy."
        ],
        happy: [
          "Solid session. You've got a good handle on the fundamentals. Focus on the weak spots and you'll be at mastery level.",
          "Good work out there. A few areas need tightening up, but you're well on your way.",
          "Nice performance. Review the objectives you missed and you'll push into the 90s next time."
        ],
        idle: [
          "Decent effort, but there's room to grow. Focus on the red areas below and hit those objectives again.",
          "You're building a foundation. Spend extra time on the topics that tripped you up.",
          "Not bad, but not exam-ready yet. Target the weak learning objectives and drill again."
        ],
        concerned: [
          "This material needs more review time. Go back to the study materials for the red-flagged objectives.",
          "I can see some gaps in your knowledge. Don't rush it — review the explanations and try again.",
          "Let's be honest — you need more study time on these topics before you're exam-ready. Focus on the fundamentals."
        ],
        disgust: [
          "We've got serious work to do. Start with the study materials and come back when you've reviewed each objective.",
          "This score tells me we need to go back to basics. Review the learning materials thoroughly before drilling again.",
          "Don't get discouraged, but this needs attention. Study the core concepts and objectives, then come back for another round."
        ]
      };
      const pool = speeches[mood] || speeches.idle;
      document.getElementById('resMentorSpeech').textContent = pool[Math.floor(Math.random() * pool.length)];

      // Focus area tags
      const tagsEl = document.getElementById('resMentorTags');
      const catEntries = Object.entries(r.categoryStats);
      tagsEl.innerHTML = catEntries.map(([catId, cs]) => {
        const catPct = cs.total > 0 ? (cs.correct / cs.total) * 100 : 100;
        let cls = 'blue';
        if (catPct < 40) cls = 'red';
        else if (catPct < 65) cls = 'yellow';
        return `<span class="res-focus-tag ${cls}">${cs.name}</span>`;
      }).join('');
    }

    // ---- LEARNING OBJECTIVE MASTERY ----
    function renderLOMastery(r) {
      const focusEl = document.getElementById('loFocusArea');
      const cardsEl = document.getElementById('loCategoryCards');
      const section = document.getElementById('loMasterySection');
      const loEntries = Object.entries(r.loStats || {});

      if (loEntries.length === 0) {
        section.style.display = 'none';
        return;
      }
      section.style.display = '';

      // Build enriched LO array with percentages & trend data; persist to localStorage
      const enriched = loEntries.map(([loId, lo]) => {
        const pct = lo.total > 0 ? Math.round((lo.correct / lo.total) * 100) : 0;
        const loKey = `ace_lo_mastery_${LESSON_ID}_${loId}`;
        let trend = 'new';
        try {
          const prevRaw = localStorage.getItem(loKey);
          if (prevRaw) {
            const prev = JSON.parse(prevRaw);
            if (prev.lastPct !== undefined) {
              trend = pct > prev.lastPct ? 'up' : pct < prev.lastPct ? 'down' : 'flat';
            }
          }
        } catch (e) { }
        // Save cumulative
        try {
          const prevRaw = localStorage.getItem(loKey);
          let cc = lo.correct, ct = lo.total;
          if (prevRaw) { const p = JSON.parse(prevRaw); cc += (p.correct || 0); ct += (p.total || 0); }
          localStorage.setItem(loKey, JSON.stringify({ correct: cc, total: ct, lastPct: pct }));
        } catch (e) { }
        const catObj = window._categories.find(c => c.id === lo.category);
        return { loId, pct, trend, text: lo.text, shortText: lo.shortText || lo.text, catId: lo.category, catName: catObj ? catObj.name : lo.category, correct: lo.correct, total: lo.total };
      });

      // ── TOP 5 FOCUS AREAS ──
      const weakest = enriched.filter(l => l.pct < 80).sort((a, b) => a.pct - b.pct).slice(0, 5);
      if (weakest.length > 0) {
        let fHtml = `<div class="lo-focus-card"><div class="lo-focus-title"><span>&#9888;</span> Priority Review Areas</div>`;
        weakest.forEach((lo, i) => {
          const c = lo.pct < 40 ? 'var(--danger)' : lo.pct < 65 ? 'var(--warning)' : 'var(--ace-blue,#58a6ff)';
          const trendIcon = lo.trend === 'up' ? '&#8593;' : lo.trend === 'down' ? '&#8595;' : lo.trend === 'flat' ? '=' : '--';
          const trendClass = lo.trend;
          // Truncate display text to ~120 chars
          const dispText = lo.text.length > 120 ? lo.text.substring(0, 117) + '...' : lo.text;
          fHtml += `
        <div class="lo-focus-item">
          <div class="lo-focus-rank">${i + 1}</div>
          <div class="lo-focus-body">
            <div class="lo-focus-obj">${dispText}</div>
            <div class="lo-focus-meta">
              <span class="lo-focus-pct" style="color:${c}">${lo.pct}%</span>
              <span class="lo-trend ${trendClass}">${trendIcon}</span>
              <div class="lo-focus-bar"><div class="lo-focus-bar-fill" style="width:${lo.pct}%;background:${c}"></div></div>
              <span class="lo-focus-cat">${lo.catName}</span>
            </div>
          </div>
        </div>`;
        });
        fHtml += '</div>';
        focusEl.innerHTML = fHtml;
      } else {
        focusEl.innerHTML = `<div class="lo-focus-card" style="border-color:rgba(63,185,80,0.25);background:linear-gradient(135deg,rgba(63,185,80,0.06) 0%,rgba(63,185,80,0.02) 100%)"><div class="lo-focus-title" style="color:var(--success)"><span>&#10003;</span> All objectives at or above 80% — great work!</div></div>`;
      }

      // ── COLLAPSIBLE CATEGORY CARDS ──
      const groups = {};
      enriched.forEach(lo => {
        if (!groups[lo.catId]) groups[lo.catId] = { name: lo.catName, items: [] };
        groups[lo.catId].items.push(lo);
      });

      let cHtml = '';
      Object.entries(groups).forEach(([catId, group]) => {
        const catTotal = group.items.length;
        const mastered = group.items.filter(l => l.pct >= 80).length;
        const avgPct = catTotal > 0 ? Math.round(group.items.reduce((s, l) => s + l.pct, 0) / catTotal) : 0;
        const ringColor = avgPct >= 80 ? '#3fb950' : avgPct >= 50 ? '#f59e0b' : '#ff5555';
        const uid = 'locard_' + catId.replace(/[^a-z0-9]/gi, '_');

        cHtml += `<div class="lo-cat-card" id="${uid}">
      <div class="lo-cat-summary" onclick="document.getElementById('${uid}').classList.toggle('open')">
        <span class="lo-cat-chevron">&#9654;</span>
        <div class="lo-cat-ring"><canvas width="72" height="72" data-pct="${avgPct}" data-color="${ringColor}"></canvas><div class="lo-cat-ring-pct" style="color:${ringColor}">${avgPct}%</div></div>
        <div class="lo-cat-info">
          <div class="lo-cat-name">${group.name}</div>
          <div class="lo-cat-subtitle">${catTotal} objective${catTotal !== 1 ? 's' : ''} assessed</div>
        </div>
        <div class="lo-cat-mastered">${mastered}/${catTotal}</div>
      </div>
      <div class="lo-cat-detail">`;

        group.items.sort((a, b) => a.pct - b.pct).forEach(lo => {
          const c = lo.pct >= 80 ? 'var(--success)' : lo.pct >= 50 ? 'var(--warning)' : 'var(--danger)';
          const icon = lo.pct >= 80 ? '<span class="lo-item-icon" style="color:var(--success)">&#10003;</span>' : '<span class="lo-item-icon" style="color:var(--danger)">&#10007;</span>';
          const trendIcon = lo.trend === 'up' ? '&#8593;' : lo.trend === 'down' ? '&#8595;' : lo.trend === 'flat' ? '=' : '--';
          cHtml += `
        <div class="lo-item">
          ${icon}
          <div class="lo-item-body">
            <div class="lo-item-text">${lo.text}</div>
            <div class="lo-item-row">
              <div class="lo-bar-wrap"><div class="lo-bar-fill" style="width:${lo.pct}%;background:${c}"></div></div>
              <div class="lo-pct" style="color:${c}">${lo.pct}%</div>
              <span class="lo-trend ${lo.trend}">${trendIcon}</span>
            </div>
          </div>
        </div>`;
        });

        cHtml += '</div></div>';
      });

      cardsEl.innerHTML = cHtml;

      // Draw mini ring canvases
      cardsEl.querySelectorAll('.lo-cat-ring canvas').forEach(cv => {
        const pct = parseInt(cv.dataset.pct) || 0;
        const color = cv.dataset.color || '#58a6ff';
        const ctx = cv.getContext('2d');
        const cx = 36, cy = 36, r = 28, lw = 5;
        ctx.clearRect(0, 0, 72, 72);
        // BG ring
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, 2 * Math.PI);
        ctx.strokeStyle = 'rgba(255,255,255,0.08)'; ctx.lineWidth = lw; ctx.stroke();
        // Value arc
        if (pct > 0) {
          ctx.beginPath(); ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + (pct / 100) * 2 * Math.PI);
          ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.lineCap = 'round'; ctx.stroke();
        }
      });
    }

    // ---- RADAR CHART ----
    function drawResRadarChart(categoryStats) {
      const canvas = document.getElementById('resRadarChart');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      const radius = 120;
      const topics = Object.keys(categoryStats);
      const n = topics.length;
      if (n < 3) return;
      const step = (2 * Math.PI) / n;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Background rings
      ctx.strokeStyle = 'rgba(255,255,255,0.08)';
      ctx.lineWidth = 1;
      [20, 40, 60, 80, 100].forEach(lvl => {
        const r = (lvl / 100) * radius;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, 2 * Math.PI);
        ctx.stroke();
      });

      // Axis lines + labels
      ctx.strokeStyle = 'rgba(255,255,255,0.12)';
      ctx.font = '10px Inter, system-ui, sans-serif';
      ctx.fillStyle = '#8b949e';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      topics.forEach((t, i) => {
        const angle = i * step - Math.PI / 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.cos(angle) * radius, cy + Math.sin(angle) * radius);
        ctx.stroke();
        // Label
        const labelR = radius + 22;
        const lx = cx + Math.cos(angle) * labelR;
        const ly = cy + Math.sin(angle) * labelR;
        const name = categoryStats[t].name || t;
        const short = name.length > 14 ? name.substring(0, 12) + '..' : name;
        ctx.fillText(short, lx, ly);
      });

      const scores = topics.map(t => {
        const d = categoryStats[t];
        return d.total > 0 ? (d.correct / d.total) * 100 : 0;
      });

      // Filled polygon
      ctx.beginPath();
      scores.forEach((score, i) => {
        const angle = i * step - Math.PI / 2;
        const r = (score / 100) * radius;
        const x = cx + Math.cos(angle) * r;
        const y = cy + Math.sin(angle) * r;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.closePath();
      ctx.fillStyle = 'rgba(88,166,255,0.25)';
      ctx.fill();

      // Stroke polygon
      ctx.beginPath();
      scores.forEach((score, i) => {
        const angle = i * step - Math.PI / 2;
        const r = (score / 100) * radius;
        const x = cx + Math.cos(angle) * r;
        const y = cy + Math.sin(angle) * r;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.closePath();
      ctx.strokeStyle = '#58a6ff';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Data points
      scores.forEach((score, i) => {
        const angle = i * step - Math.PI / 2;
        const r = (score / 100) * radius;
        const x = cx + Math.cos(angle) * r;
        const y = cy + Math.sin(angle) * r;
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = score >= 80 ? '#3fb950' : score >= 60 ? '#e3b341' : '#f85149';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.stroke();
      });
    }

    // ---- SESSION HISTORY SPARKLINE ----
    function saveAndRenderSessionHistory(pct, seen) {
      const key = `ace_drill_history_${LESSON_ID}`;
      let history = [];
      try {
        const raw = localStorage.getItem(key);
        if (raw) history = JSON.parse(raw);
        if (!Array.isArray(history)) history = [];
      } catch (e) { history = []; }

      // Compute avg time for this session
      const avgMs = state.questionTimes && state.questionTimes.length > 0
        ? state.questionTimes.reduce((a, b) => a + b, 0) / state.questionTimes.length : 0;
      const avgSec = Math.round(avgMs / 1000);

      // Add current session
      history.push({ date: new Date().toISOString(), pct, seen, correct: state.lastResults.correct, missed: state.lastResults.missed, avgTime: avgSec });
      // Keep only last 10
      if (history.length > 10) history = history.slice(-10);
      try { localStorage.setItem(key, JSON.stringify(history)); } catch (e) { }

      // Render sparkline (last 5 sessions)
      const recent = history.slice(-5);
      const sparkSection = document.getElementById('sparklineSection');
      if (recent.length < 2) {
        sparkSection.style.display = 'none';
        return;
      }
      sparkSection.style.display = '';

      const canvas = document.getElementById('sparklineCanvas');
      const ctx = canvas.getContext('2d');
      const w = canvas.width, h = canvas.height;
      ctx.clearRect(0, 0, w, h);

      const padX = 20, padY = 10;
      const plotW = w - padX * 2, plotH = h - padY * 2;

      // Draw line
      ctx.beginPath();
      ctx.strokeStyle = '#58a6ff';
      ctx.lineWidth = 2;
      recent.forEach((s, i) => {
        const x = padX + (i / (recent.length - 1)) * plotW;
        const y = padY + plotH - (s.pct / 100) * plotH;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      });
      ctx.stroke();

      // Draw dots + labels
      recent.forEach((s, i) => {
        const x = padX + (i / (recent.length - 1)) * plotW;
        const y = padY + plotH - (s.pct / 100) * plotH;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fillStyle = s.pct >= 75 ? '#3fb950' : s.pct >= 50 ? '#e3b341' : '#f85149';
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 1;
        ctx.stroke();
        // Pct label
        ctx.fillStyle = '#8b949e';
        ctx.font = '9px Inter, system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(s.pct + '%', x, y - 9);
      });

      // Trend indicator
      const trendEl = document.getElementById('sparklineTrend');
      const first = recent[0].pct, last = recent[recent.length - 1].pct;
      if (last > first) {
        trendEl.textContent = 'Trending Up';
        trendEl.className = 'sparkline-trend up';
      } else if (last < first) {
        trendEl.textContent = 'Trending Down';
        trendEl.className = 'sparkline-trend down';
      } else {
        trendEl.textContent = 'Holding Steady';
        trendEl.className = 'sparkline-trend flat';
      }
    }

    // ---- ANSWER REVIEW ----
    function showAnswerReview() {
      const container = document.getElementById('answerReviewList');
      const log = state.lastResults.answerLog || [];
      const LETTERS = ['A', 'B', 'C', 'D', 'E'];

      if (log.length === 0) {
        container.innerHTML = '<p style="color:var(--text-muted);text-align:center;padding:2rem;">No answers recorded.</p>';
      } else {
        container.innerHTML = log.map((entry, idx) => {
          const correctText = (entry.options[entry.correct] || '').replace(/^[A-D]\.\s*/, '');
          const selectedText = (entry.options[entry.selected] || '').replace(/^[A-D]\.\s*/, '');
          return `
        <div class="review-item ${entry.isCorrect ? 'ri-correct' : 'ri-wrong'}">
          <div class="review-q-num">Question ${idx + 1} ${entry.isCorrect ? '— Correct' : '— Wrong'}</div>
          <div class="review-q-text">${entry.question}</div>
          <div class="review-answer-row">
            <span class="correct-ans">Correct: ${LETTERS[entry.correct]}. ${correctText}</span>
            ${!entry.isCorrect ? `<br><span class="your-ans">Your answer: ${LETTERS[entry.selected]}. ${selectedText}</span>` : ''}
          </div>
          ${entry.lo ? `<div class="review-lo">LO: ${entry.lo}</div>` : ''}
        </div>`;
        }).join('');
      }

      document.getElementById('answerReviewOverlay').classList.add('active');
    }

    function closeAnswerReview() {
      document.getElementById('answerReviewOverlay').classList.remove('active');
    }

    // ---- REPORT COMPLETION (no localStorage score for drill) ----
    function reportDrillCompletion(pct, stats) {
      // Send analytics to parent
      try {
        window.parent.postMessage({
          type: 'ACE_MODULE_COMPLETE',
          module: 'drill',
          score: pct,
          stats: {
            questionsAnswered: stats.seen,
            questionsCorrect: stats.correct,
            studyTimeSeconds: Math.floor((Date.now() - state.sessionStart) / 1000)
          }
        }, '*');
      } catch (e) { }

      // GameEngine XP (5 per question answered)
      try {
        if (typeof GameEngine !== 'undefined') {
          const xp = (stats.seen || 0) * 5;
          if (xp > 0) GameEngine.awardXP(xp, 'Drill Session', { lessonId: LESSON_ID });
          GameEngine.unlockBadge('first-steps');
        }
      } catch (e) { }
    }

    // ---- TRY AGAIN ----
    function tryAgain() {
      document.getElementById('resultsOverlay').classList.remove('active');
      document.getElementById('answerReviewOverlay').classList.remove('active');
      // Keep category selection, relaunch
      if (selectedCatIds.length > 0) startDrill();
    }

    // ---- STATS DISPLAY ----
    function updateStatsDisplay() {
      document.getElementById('statSeen').textContent = state.sessionStats.seen;
      document.getElementById('statCorrect').textContent = state.sessionStats.correct;
      document.getElementById('statMissed').textContent = state.sessionStats.missed;
      const pct = state.sessionStats.seen > 0
        ? Math.round((state.sessionStats.correct / state.sessionStats.seen) * 100) : 0;
      document.getElementById('accuracyFill').style.width = pct + '%';
      document.getElementById('accuracyPct').textContent = state.sessionStats.seen > 0 ? pct + '%' : '—';
      document.getElementById('accuracyFill').style.background =
        pct >= 75 ? 'var(--success)' : pct >= 50 ? 'var(--warning)' : 'var(--danger)';
    }

    function updateWeakList() {
      const el = document.getElementById('weakList');
      if (state.weakList.length === 0) {
        el.innerHTML = '<p class="weak-empty">Miss a question and it shows up here.</p>';
      } else {
        el.innerHTML = state.weakList.map(q => {
          const correctText = q.options[q.correct] || '';
          const clean = correctText.replace(/^[A-D]\.\s*/, '');
          return `
        <div class="weak-item">
          <div class="weak-item-q">${q.question}</div>
          <div class="weak-item-a">✓ ${clean}</div>
          <div class="weak-item-tags">${(q.tags || []).map(t => `<span class="weak-item-tag">${t}</span>`).join('')}</div>
        </div>`;
        }).join('');
      }
    }

    // ---- SESSION STATS (localStorage — session recovery only, no score saved) ----
    const SESSION_KEY = `ace_drill_session_${LESSON_ID}`;

    function saveSessionStats() {
      try {
        localStorage.setItem(SESSION_KEY, JSON.stringify({
          sessionStats: state.sessionStats,
          weakList: state.weakList,
          ts: Date.now()
        }));
      } catch (e) { }
    }

    function loadSessionStats() {
      try {
        const raw = localStorage.getItem(SESSION_KEY);
        if (!raw) return;
        const data = JSON.parse(raw);
        // Only restore if within 4 hours
        if (Date.now() - (data.ts || 0) < 4 * 3600 * 1000) {
          state.sessionStats = data.sessionStats || state.sessionStats;
          state.weakList = data.weakList || [];
        } else {
          localStorage.removeItem(SESSION_KEY);
        }
        updateStatsDisplay();
        updateWeakList();
      } catch (e) { }
    }

    function resetStats() {
      if (!confirm('Reset all session statistics and weak list?')) return;
      state.sessionStats = { seen: 0, correct: 0, missed: 0 };
      state.weakList = [];
      state.categoryStats = {};
      updateStatsDisplay();
      updateWeakList();
      try { localStorage.removeItem(SESSION_KEY); } catch (e) { }
      showAchievement('Stats reset. Fresh start!');
    }

    // ---- ANALYTICS ----
    function sendAnalyticsEvent(event, data) {
      try {
        window.parent.postMessage({ type: 'ACE_ANALYTICS', event, ...data }, '*');
      } catch (e) { }
    }

    // ---- ACHIEVEMENT POPUP ----
    function showAchievement(text) {
      const popup = document.getElementById('achievementPopup');
      popup.textContent = text;
      popup.classList.add('show');
      setTimeout(() => popup.classList.remove('show'), 3000);
    }

    // ---- EASTER EGGS ----
    const KONAMI = ['ArrowUp', 'ArrowDown', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'b', 'a', 'a'];
    document.addEventListener('keydown', e => {
      // Small helper to dynamically load canvas-confetti
      const fireConfetti = () => {
        if (!window.confetti) {
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js';
          script.onload = () => window.confetti({ particleCount: 200, spread: 120, origin: { y: 0.3 } });
          document.head.appendChild(script);
        } else {
          window.confetti({ particleCount: 200, spread: 120, origin: { y: 0.3 } });
        }
      };

      if (KONAMI[state.konamiProgress] === e.key.toLowerCase() || KONAMI[state.konamiProgress] === e.key) {
        state.konamiProgress++;
        if (state.konamiProgress === KONAMI.length) {
          document.body.classList.add('konami-active');
          showAchievement('KONAMI MODE ACTIVATED!');
          fireConfetti();

          let duration = 5 * 1000;
          let animationEnd = Date.now() + duration;
          let defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 9999 };

          function randomInRange(min, max) {
            return Math.random() * (max - min) + min;
          }

          let interval = setInterval(function () {
            let timeLeft = animationEnd - Date.now();
            if (timeLeft <= 0) {
              return clearInterval(interval);
            }
            let particleCount = 50 * (timeLeft / duration);
            if (window.confetti) {
              window.confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
              window.confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }
          }, 250);

          setTimeout(() => document.body.classList.remove('konami-active'), 10000);
          state.konamiProgress = 0;
        }
      } else {
        state.konamiProgress = 0;
      }
    });

    document.getElementById('brandTitle')?.addEventListener('click', () => {
      document.body.classList.add('boss-mode');
      showAchievement('BOSS MODE ENGAGED!');
      setTimeout(() => document.body.classList.remove('boss-mode'), 500);
    });

    // ---- KEYBOARD SHORTCUTS ----
    document.addEventListener('keydown', e => {
      const drillActive = document.getElementById('drillOverlay').classList.contains('active');
      if (!drillActive) return;

      // A/B/C/D to select option
      const map = { 'a': 0, 'b': 1, 'c': 2, 'd': 3 };
      const key = e.key.toLowerCase();

      // If the user is actively entering the B B A A sequence for the Konami code, let the Easter Egg listener handle it.
      if (state.konamiProgress >= 8 && (key === 'a' || key === 'b')) {
        return;
      }

      if (map[key] !== undefined && !state.answered) {
        const btns = document.querySelectorAll('.option-btn');
        if (btns[map[key]]) selectAnswer(map[key]);
        return;
      }

      // Enter / Space / Right arrow → next
      if ((e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowRight') && state.answered) {
        e.preventDefault();
        nextQuestion();
        return;
      }

      // Escape → exit
      if (e.key === 'Escape') {
        endDrill();
      }
    });

    // ---- SHUFFLE ----
    function shuffleArray(arr) {
      const a = [...arr];
      for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
      }
      return a;
    }

    // ---- BIND EVENTS ----
    function bindEvents() {
      document.getElementById('btnStart').addEventListener('click', startDrill);
      document.getElementById('btnEndDrill').addEventListener('click', endDrill);
      document.getElementById('drillExitBtn').addEventListener('click', endDrill);
      // btnNext removed — handled by AcePopup onNext callback
      document.getElementById('btnResetStats').addEventListener('click', resetStats);
      document.getElementById('btnTryAgain').addEventListener('click', tryAgain);
      document.getElementById('btnReviewAnswers').addEventListener('click', showAnswerReview);
      document.getElementById('btnCloseReview').addEventListener('click', closeAnswerReview);
      document.getElementById('btnCloseResults').addEventListener('click', closeActivity);
      document.getElementById('btnViewResults').addEventListener('click', () => {
        if (state.lastResults) showResults();
      });
      document.getElementById('btnSelectAll').addEventListener('click', () => {
        const allIds = window._categories.map(c => c.id);
        const allSelected = allIds.length > 0 && allIds.every(id => selectedCatIds.includes(id));
        if (allSelected) {
          selectedCatIds = [];
          document.querySelectorAll('.category-card').forEach(c => c.classList.remove('selected'));
        } else {
          selectedCatIds = [...allIds];
          document.querySelectorAll('.category-card').forEach(c => c.classList.add('selected'));
        }
        const btn = document.getElementById('btnSelectAll');
        btn.textContent = selectedCatIds.length === allIds.length ? 'Clear All' : 'Select All';
        // Update the summary
        const totalQ = selectedCatIds.reduce((sum, id) => {
          const cat = window._categories.find(c => c.id === id);
          return sum + (cat ? cat.items.length : 0);
        }, 0);
        const summaryEl = document.getElementById('selectedSummary');
        if (selectedCatIds.length === 0) {
          summaryEl.innerHTML = 'Select one or more categories to begin';
          document.getElementById('categoryBadge').textContent = 'None';
        } else {
          summaryEl.innerHTML = `<strong>${selectedCatIds.length}</strong> ${selectedCatIds.length === 1 ? 'category' : 'categories'} · <strong>${totalQ}</strong> questions`;
          document.getElementById('categoryBadge').textContent = `${selectedCatIds.length} categories`;
        }
        document.getElementById('btnStart').disabled = selectedCatIds.length === 0;
      });
    }

    // ---- beforeunload recovery ----
    window.addEventListener('beforeunload', () => {
      if (state.sessionStats.seen > 0) {
        saveSessionStats();
        try {
          if (typeof GameEngine !== 'undefined') {
            GameEngine.awardXP(state.sessionStats.seen * 5, 'Drill Session');
            GameEngine.addStudyTime(Math.floor((Date.now() - state.sessionStart) / 1000));
          }
        } catch (e) { }
      }
    });

    // Legacy compat
    window.reportTestScore = function (userScore, totalPossible) {
      const pct = Math.round((userScore / totalPossible) * 100);
      reportDrillCompletion(pct, { seen: totalPossible, correct: userScore, missed: totalPossible - userScore });
    };
  