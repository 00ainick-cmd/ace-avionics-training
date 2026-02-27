import os
import glob
import re

base_dir = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\question-banks\modules\caet-entry\shared\training"
rise_base = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\rise-modules"

if not os.path.exists(rise_base):
    os.makedirs(rise_base)

css_addition = """
        .focus-tool { display: flex; align-items: stretch; background: rgba(255,255,255,0.05); border-radius: 10px; border: 1px solid rgba(255,255,255,0.1); overflow: visible; }
        .focus-study { display: flex; align-items: center; gap: 8px; padding: 4px 12px; }
        .pomodoro-btn { width: 44px; height: 100%; display: flex; align-items: center; justify-content: center; background: rgba(255,99,71,0.1); border: none; border-left: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: all 0.2s ease; padding: 0; border-radius: 0 10px 10px 0; }
        .pomodoro-btn:hover { background: rgba(255,99,71,0.2); }
        .notes-btn { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; padding: 8px 16px; border-radius: 10px; font-family: 'Chakra Petch', sans-serif; font-size: 14px; cursor: pointer; transition: all 0.3s ease; }
        .notes-btn:hover { background: rgba(212, 168, 83, 0.2); border-color: rgba(212, 168, 83, 0.5); }
        .notes-btn svg { width: 16px; height: 16px; color: var(--gold); }
        .notes-panel { position: fixed; top: 60px; right: -400px; width: 350px; bottom: 0; background: rgba(20,24,38,0.95); backdrop-filter: blur(20px); border-left: 1px solid rgba(255,255,255,0.1); z-index: 999; transition: right 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); display: flex; flex-direction: column; box-shadow: -10px 0 30px rgba(0,0,0,0.5); }
        .notes-panel.open { right: 0; }
        .notes-header { display: flex; align-items: center; justify-content: space-between; padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .notes-header h3 { font-size: 16px; color: var(--gold); margin: 0; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
        .close-notes { background: none; border: none; color: var(--text-muted); font-size: 24px; cursor: pointer; transition: color 0.2s; line-height: 1; }
        .close-notes:hover { color: white; }
        .notes-body { flex: 1; padding: 20px; display: flex; flex-direction: column; }
        .notes-textarea { flex: 1; width: 100%; background: transparent; border: none; color: var(--text-primary); font-family: 'Inter', sans-serif; font-size: 14px; line-height: 1.6; resize: none; outline: none; }
        .notes-textarea::placeholder { color: var(--text-muted); }
"""

html_replacement = """        <div class="timer-section">
            <div class="focus-tool" id="focusToolWidget">
                <div class="focus-study" title="Total Study Time">
                    <span class="timer-icon">&#128337;</span>
                    <div class="timer-display">
                        <span class="timer-label">Study Time</span>
                        <span class="timer-value" id="studyTimer">00:00:00</span>
                    </div>
                </div>
                <div class="pomodoro-widget" id="pomodoroWidget">
                    <button class="pomodoro-btn" id="pomodoroBtn" title="Pomodoro Timer (P)">
                        <svg viewBox="0 0 24 24" fill="currentColor" style="width:20px;height:20px;"><circle cx="12" cy="14" r="8" fill="#ff6347"/><path d="M12 6 L12 2 M10 3 L14 3" stroke="#228B22" stroke-width="2" fill="none"/><ellipse cx="12" cy="10" rx="5" ry="2" fill="rgba(255,255,255,0.3)"/></svg>
                    </button>
                    <div class="pomodoro-panel" id="pomodoroPanel">
                        <div class="pomodoro-display" id="pomodoroDisplay">25:00</div>
                        <div class="pomodoro-controls">
                            <button class="pomo-ctrl-btn" id="pomoStart">&#9654;</button>
                            <button class="pomo-ctrl-btn" id="pomoReset">&#8634;</button>
                        </div>
                        <div class="pomodoro-presets">
                            <button class="pomo-preset" data-minutes="25">25m</button>
                            <button class="pomo-preset" data-minutes="15">15m</button>
                            <button class="pomo-preset" data-minutes="5">5m</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <button class="notes-btn" id="notesBtn" title="Take Notes">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                <span>Notes</span>
            </button>
            <div class="keyboard-hint">Press <kbd>ESC</kbd> to exit</div>
        </div>
    </div>

    <!-- Notes Panel -->
    <div class="notes-panel" id="notesPanel">
        <div class="notes-header">
            <h3>Module Notes</h3>
            <button class="close-notes" id="closeNotes">&times;</button>
        </div>
        <div class="notes-body">
            <textarea class="notes-textarea" id="notesArea" placeholder="Jot down important points, concepts, or questions here. These notes are saved automatically..."></textarea>
        </div>
    </div>"""

js_addition = """
        // --- NOTES SYSTEM ---
        const notesBtn = document.getElementById('notesBtn');
        const notesPanel = document.getElementById('notesPanel');
        const closeNotes = document.getElementById('closeNotes');
        const notesArea = document.getElementById('notesArea');
        const NOTES_KEY = `caet_notes_${LESSON_ID}`;

        if(notesBtn) notesBtn.addEventListener('click', () => notesPanel.classList.add('open'));
        if(closeNotes) closeNotes.addEventListener('click', () => notesPanel.classList.remove('open'));
        
        if(notesArea) {
            notesArea.value = localStorage.getItem(NOTES_KEY) || '';
            notesArea.addEventListener('input', () => {
                localStorage.setItem(NOTES_KEY, notesArea.value);
            });
        }
"""

js_back_fix = """        function goBack() {
            saveSessionData();
            if (studyTimerInterval) clearInterval(studyTimerInterval);
            if (pomodoroInterval) clearInterval(pomodoroInterval);
            if (isEmbedded) { window.parent.postMessage({ type: 'ACE_CLOSE' }, '*'); }
            else { window.history.back(); }
        }"""

for filename in glob.glob(os.path.join(base_dir, "*-rise.html")):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Get lesson id
    match = re.search(r"const LESSON_ID =\s*['\"]([^'\"]+)['\"]", content)
    if match:
        lesson_id = match.group(1)
        # Create folder in rise-modules
        mod_dir = os.path.join(rise_base, lesson_id)
        if not os.path.exists(mod_dir):
            os.makedirs(mod_dir)
            print(f"Created module dir: {lesson_id}")
            
    # Modify CSS 
    if ".notes-panel" not in content:
        content = content.replace("</style>", css_addition + "\n    </style>")
        
    # Replace Timer Section
    timer_pattern = r'<div class="timer-section">.*?</div>\s*</div>\s*</div>'
    if '<div class="notes-panel"' not in content:
        content = re.sub(timer_pattern, html_replacement, content, flags=re.DOTALL)
        
    # Inject JS
    if "NOTES_KEY" not in content:
        content = content.replace("function startStudyTimer", js_addition + "\n        function startStudyTimer")
        
    # Fix RISE_URL
    url_pattern = r"const RISE_URL = ['\"].*?['\"];"
    content = re.sub(url_pattern, "const RISE_URL = `../../../../../../rise-modules/${LESSON_ID}/index.html`;", content)
    
    # Fix goBack
    goback_pattern = r"function goBack\(\) \{.*?\}"
    content = re.sub(goback_pattern, js_back_fix, content, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Refactoring complete.")
