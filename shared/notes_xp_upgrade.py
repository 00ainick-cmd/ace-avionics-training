import os
import re

file_path = r'c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\shared\course-viewer.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CSS Injection
css_inject = """        /* Tooltip */
        .pomo-info-wrapper { position: relative; display: inline-block; }
        .pomo-tooltip { visibility: hidden; width: 250px; background-color: rgba(20, 24, 38, 0.95); color: #fff; text-align: left; border-radius: 8px; padding: 12px; position: absolute; z-index: 1001; bottom: 125%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.3s; border: 1px solid rgba(255, 255, 255, 0.1); font-size: 11px; line-height: 1.4; font-weight: normal; text-transform: none; pointer-events: none; }
        .pomo-info-wrapper:hover .pomo-tooltip { visibility: visible; opacity: 1; }
        
        /* Notes Toolbar */
        .notes-toolbar { display: flex; gap: 4px; padding: 8px 24px; background: rgba(0,0,0,0.2); border-bottom: 1px solid rgba(255,255,255,0.05); align-items: center; flex-wrap: wrap; }
        .toolbar-btn { background: transparent; border: 1px solid transparent; color: var(--text-secondary); border-radius: 4px; padding: 4px 8px; cursor: pointer; transition: all 0.2s; font-size: 13px; font-weight: 600; }
        .toolbar-btn:hover { background: rgba(255,255,255,0.1); color: white; border-color: rgba(255,255,255,0.2); }
        
        /* Formula Drawer */
        .formula-drawer { display: none; position: absolute; top: 120px; right: 390px; width: 250px; background: rgba(20, 24, 38, 0.95); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px; z-index: 1000; box-shadow: -5px 5px 20px rgba(0,0,0,0.5); }
        .formula-drawer.open { display: block; }
        .formula-item { padding: 8px; cursor: pointer; border-radius: 4px; border: 1px solid transparent; transition: all 0.2s; margin-bottom: 4px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-secondary); }
        .formula-item:hover { background: rgba(255,255,255,0.05); color: var(--gold); border-color: rgba(212, 168, 83, 0.3); }
        .formula-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; font-size: 12px; font-weight: bold; color: white; }
        .formula-close { background: none; border: none; color: var(--text-muted); cursor: pointer; }
        .formula-close:hover { color: white; }

        /* XP Float */
        .xp-float { position: absolute; top: -30px; left: 50%; transform: translateX(-50%); color: var(--gold); font-weight: bold; font-size: 18px; pointer-events: none; animation: floatUp 2s ease-out forwards; text-shadow: 0 0 10px rgba(212, 168, 83, 0.5); z-index: 1002; }
        @keyframes floatUp { 0% { opacity: 0; transform: translate(-50%, 10px) scale(0.8); } 20% { opacity: 1; transform: translate(-50%, 0) scale(1.1); } 80% { opacity: 1; } 100% { opacity: 0; transform: translate(-50%, -40px) scale(1); } }
        
        .notes-panel {"""
content = content.replace("        .notes-panel {", css_inject)

# 2. HTML Inject - Pomodoro Tooltip
pomo_html_old = """                            <div class="pomo-info" title="The Pomodoro Technique: Focus deeply on the material without distractions for 25 minutes, then take a 5-minute break to improve retention. Gamified as a 'Focus Flight'.">
                                <svg viewBox="0 0 24 24" fill="none" class="info-icon" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
                            </div>"""
pomo_html_new = """                            <div class="pomo-info-wrapper">
                                <div class="pomo-info">
                                    <svg viewBox="0 0 24 24" fill="none" class="info-icon" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg>
                                </div>
                                <div class="pomo-tooltip"><strong>The Pomodoro Technique:</strong> Focus deeply on the material without distractions for 25 minutes, then take a 5-minute break to improve retention. <br><br><em>Gamified as a 'Focus Flight'.</em></div>
                            </div>"""
content = content.replace(pomo_html_old, pomo_html_new)


# 3. HTML Inject - Notes Toolbar and Formula Drawer
notes_body_old = """        <div class="notes-body">
            <textarea class="notes-textarea" id="notesArea\""""
notes_body_new = """        <div class="notes-toolbar">
            <button class="toolbar-btn" data-tag="h1" title="Header 1">H1</button>
            <button class="toolbar-btn" data-tag="h2" title="Header 2">H2</button>
            <button class="toolbar-btn" data-tag="bold" title="Bold">B</button>
            <button class="toolbar-btn" data-tag="italic" title="Italic">I</button>
            <button class="toolbar-btn" data-tag="ul" title="Bulleted List">• List</button>
            <button class="toolbar-btn" data-tag="ol" title="Numbered List">1. List</button>
            <button class="toolbar-btn" id="openFormulasBtn" style="margin-left:auto; color:var(--gold);" title="Formulas">? Formulas</button>
        </div>
        <div class="notes-body">
            <textarea class="notes-textarea" id="notesArea\""""
content = content.replace(notes_body_old, notes_body_new)

# Add formula drawer to body
drawer_html = """    <!-- Formula Drawer -->
    <div class="formula-drawer" id="formulaDrawer">
        <div class="formula-header">
            <span>Aviation Formulas</span>
            <button class="formula-close" id="closeFormulasBtn">?</button>
        </div>
        <div class="formula-item" data-formula="E = I × R">Ohm's Law: E = I × R</div>
        <div class="formula-item" data-formula="P = I × E">Power: P = I × E</div>
        <div class="formula-item" data-formula="Rt = R1 + R2 + R3">Series Resistance: Rt = R1 + R2 + ...</div>
        <div class="formula-item" data-formula="1/Rt = 1/R1 + 1/R2 + 1/R3">Parallel Res.: 1/Rt = 1/R1 + ...</div>
        <div class="formula-item" data-formula="F = P × A">Force: F = P × A (Hydraulics)</div>
        <div class="formula-item" data-formula="W = F × D">Work: W = F × D</div>
    </div>
"""
content = content.replace("    <div class=\"loading-overlay\" id=\"loadingOverlay\">", drawer_html + "\n    <div class=\"loading-overlay\" id=\"loadingOverlay\">")

# 4. JS Inject - Fix Download + Add Toolbar Logic + XP Logic
js_replace_target = """                    const cleanTitle = moduleTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase();
                    a.download = caet_notes_.txt;"""
js_replace_new = """                    const cleanTitle = moduleTitle.replace(/[^a-z0-9]/gi, '_').toLowerCase();
                    a.download = caet_notes_.md;"""
content = content.replace(js_replace_target, js_replace_new)

js_logic_inject = """            if (downloadBtn && notesArea) {
                downloadBtn.addEventListener('click', () => {
"""

js_toolbar_logic = """
            // Toolbar Logic
            const formatText = (prefix, suffix, defaultText) => {
                const start = notesArea.selectionStart;
                const end = notesArea.selectionEnd;
                const selectedText = notesArea.value.substring(start, end);
                const replacement = prefix + (selectedText || defaultText) + suffix;
                notesArea.value = notesArea.value.substring(0, start) + replacement + notesArea.value.substring(end);
                notesArea.focus();
                notesArea.setSelectionRange(start + prefix.length, start + prefix.length + (selectedText || defaultText).length);
                // trigger save
                localStorage.setItem(NOTES_KEY, notesArea.value);
            };

            document.querySelectorAll('.toolbar-btn[data-tag]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const tag = e.target.getAttribute('data-tag');
                    if (tag === 'h1') formatText('# ', '', 'Header 1');
                    if (tag === 'h2') formatText('## ', '', 'Header 2');
                    if (tag === 'bold') formatText('**', '**', 'bold text');
                    if (tag === 'italic') formatText('_', '_', 'italic text');
                    if (tag === 'ul') formatText('\\n- ', '', 'list item');
                    if (tag === 'ol') formatText('\\n1. ', '', 'list item');
                });
            });

            // Formula Drawer Logic
            const formBtn = document.getElementById('openFormulasBtn');
            const drawer = document.getElementById('formulaDrawer');
            if (formBtn && drawer) {
                formBtn.addEventListener('click', () => drawer.classList.toggle('open'));
                document.getElementById('closeFormulasBtn').addEventListener('click', () => drawer.classList.remove('open'));
                
                document.querySelectorAll('.formula-item').forEach(item => {
                    item.addEventListener('click', (e) => {
                        const formula = e.target.getAttribute('data-formula');
                        formatText('\\n**' + formula + '**\\n', '', '');
                        drawer.classList.remove('open');
                    });
                });
            }

            // XP System Helpers
            window.awardXP = function(amount, reason) {
                let currentXp = parseInt(localStorage.getItem('caet_total_xp')) || 0;
                currentXp += amount;
                localStorage.setItem('caet_total_xp', currentXp);
                console.log(Awarded  XP for: . Total: );
                
                // Show floating XP text if pomodoro widget is active
                const widget = document.getElementById('pomodoroWidget');
                if (widget) {
                    const floater = document.createElement('div');
                    floater.className = 'xp-float';
                    floater.textContent = + XP;
                    widget.appendChild(floater);
                    setTimeout(() => floater.remove(), 2500);
                }
            };

            if (downloadBtn && notesArea) {"""

content = content.replace(js_logic_inject, js_toolbar_logic)

# Replace play Pomodoro Complete to add XP
xp_inject = """                setTimeout(() => {
                    fill.style.boxShadow = '0 0 10px var(--success)';
                    airplane.style.filter = 'drop-shadow(0 0 5px rgba(0,255,65,0.6))';
                    airplane.style.transform = 'scale(1) rotate(45deg)';
                }, 3000);
                
                // Award XP!
                if (window.awardXP) window.awardXP(50, 'Completed Focus Flight');"""

content = content.replace("                setTimeout(() => {\n                    fill.style.boxShadow = '0 0 10px var(--success)';\n                    airplane.style.filter = 'drop-shadow(0 0 5px rgba(0,255,65,0.6))';\n                    airplane.style.transform = 'scale(1) rotate(45deg)';\n                }, 3000);", xp_inject)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Upgrade script ran successfully.')
