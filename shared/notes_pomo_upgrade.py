import os

file_path = r'c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\shared\course-viewer.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS Injections
css_inject = """        .pomo-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .pomo-title { font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
        .pomo-info { color: var(--text-muted); cursor: help; display: flex; transition: color 0.2s; }
        .pomo-info:hover { color: var(--gold); }
        .pomo-info svg { width: 14px; height: 14px; }
        
        .notes-actions { display: flex; align-items: center; gap: 8px; }
        .notes-action-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: var(--text-secondary); width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }
        .notes-action-btn:hover { background: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2); }
        .notes-subheader { padding: 0 24px; font-size: 12px; color: var(--text-muted); line-height: 1.5; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 16px; }

        .notes-panel {"""
content = content.replace("        .notes-panel {", css_inject)


# 2. HTML Injections - Pomodoro
pomo_html_inject = """                    <div class="pomodoro-panel" id="pomodoroPanel">
                        <div class="pomo-header">
                            <span class="pomo-title">Focus Timer</span>
                            <div class="pomo-info" title="The Pomodoro Technique: Focus deeply on the material without distractions for 25 minutes, then take a 5-minute break to improve retention. Gamified as a 'Focus Flight'.">
                                <svg viewBox="0 0 24 24" fill="none" class="info-icon" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
                            </div>
                        </div>
                        <div class="pomodoro-display" id="pomodoroDisplay">25:00</div>"""
content = content.replace('                    <div class="pomodoro-panel" id="pomodoroPanel">\n                        <div class="pomodoro-display" id="pomodoroDisplay">25:00</div>', pomo_html_inject)

# 3. HTML Injections - Notes
notes_html_inject = """    <div class="notes-panel" id="notesPanel">
        <div class="notes-header">
            <h3>Module Notes</h3>
            <div class="notes-actions">
                <button class="notes-action-btn" id="copyNotesBtn" title="Copy to Clipboard">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
                </button>
                <button class="notes-action-btn" id="downloadNotesBtn" title="Download as .txt">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                </button>
                <button class="close-notes" id="closeNotes">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:18px;height:18px;"><path d="M18 6L6 18M6 6l12 12" /></svg>
                </button>
            </div>
        </div>
        <div class="notes-subheader">
            Use this space to log key CFRs, AD numbers, or specific torque values. Your notes are automatically saved locally to your device.
        </div>
        <div class="notes-body">
            <textarea class="notes-textarea" id="notesArea"
                placeholder="Example: ATA 34 Nav Systems - The VOR operates in the VHF band (108.00 - 117.95 MHz)..."></textarea>
        </div>
    </div>"""

import re
notes_pattern = re.compile(r'    <div class="notes-panel" id="notesPanel">[\s\S]*?</div>\n    </div>')
content = notes_pattern.sub(notes_html_inject, content)

# 4. JS Injections - Notes actions
js_inject = """            if (notesArea) {
                notesArea.value = localStorage.getItem(NOTES_KEY) || '';
                notesArea.addEventListener('input', () => {
                    localStorage.setItem(NOTES_KEY, notesArea.value);
                });
            }

            const copyBtn = document.getElementById('copyNotesBtn');
            const downloadBtn = document.getElementById('downloadNotesBtn');

            if (copyBtn && notesArea) {
                copyBtn.addEventListener('click', () => {
                    navigator.clipboard.writeText(notesArea.value).then(() => {
                        const originalSvg = copyBtn.innerHTML;
                        copyBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="#00ff41" stroke-width="2" style="width:14px;height:14px;"><polyline points="20 6 9 17 4 12"></polyline></svg>';
                        setTimeout(() => copyBtn.innerHTML = originalSvg, 2000);
                    });
                });
            }

            if (downloadBtn && notesArea) {
                downloadBtn.addEventListener('click', () => {
                    const blob = new Blob([notesArea.value], { type: 'text/plain' });
                    const a = document.createElement('a');
                    a.href = URL.createObjectURL(blob);
                    const cleanTitle = moduleTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase();
                    a.download = caet_notes_.txt;
                    a.click();
                    URL.revokeObjectURL(a.href);
                });
            }
        }"""
content = content.replace("            if (notesArea) {\n                notesArea.value = localStorage.getItem(NOTES_KEY) || '';\n                notesArea.addEventListener('input', () => {\n                    localStorage.setItem(NOTES_KEY, notesArea.value);\n                });\n            }\n        }", js_inject)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Script completed successfully.')
