import os

file_path = r'c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\shared\course-viewer.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject CSS for Flight Path
css_inject = """        .flight-path-container { margin: 8px 0 24px 0; padding: 0 10px; display: none; }
        .pomodoro-panel.visible .flight-path-container { display: block; }
        .flight-path-label { font-size: 10px; color: var(--gold); text-transform: uppercase; font-weight: 700; text-align: center; margin-bottom: 8px; letter-spacing: 1px; transition: color 0.3s; }
        .flight-path-track { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; position: relative; }
        .flight-path-fill { position: absolute; top: 0; left: 0; height: 100%; background: var(--success); border-radius: 2px; width: 0%; transition: width 1s linear; box-shadow: 0 0 10px var(--success); }
        .flight-airplane { position: absolute; right: -12px; top: -8px; color: var(--success); filter: drop-shadow(0 0 5px rgba(0,255,65,0.6)); transition: all 0.3s ease; }
        .flight-airplane svg { width: 20px; height: 20px; transform: rotate(45deg); }

        .notes-btn {"""
content = content.replace("        .notes-btn {", css_inject)

# 2. Inject HTML for Flight Path
html_inject = """                    <div class="pomodoro-panel" id="pomodoroPanel">
                        <div class="pomodoro-display" id="pomodoroDisplay">25:00</div>
                        <div class="flight-path-container" id="flightPathContainer">
                            <div class="flight-path-label" id="flightPathLabel">Ready for Takeoff</div>
                            <div class="flight-path-track">
                                <div class="flight-path-fill" id="flightPathFill">
                                    <div class="flight-airplane" id="flightAirplane">
                                        <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z"/></svg>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="pomodoro-controls">"""
content = content.replace('                    <div class="pomodoro-panel" id="pomodoroPanel">\n                        <div class="pomodoro-display" id="pomodoroDisplay">25:00</div>\n                        <div class="pomodoro-controls">', html_inject)

# 3. Inject Auto-Save into startStudyTimer
timer_inject = """        // --- STUDY TIMER ---
        function startStudyTimer() { 
            studyTimerInterval = setInterval(updateStudyTimer, 1000); 
            setInterval(saveSessionData, 10000); // Auto-save every 10 seconds
        }"""
content = content.replace("        // --- STUDY TIMER ---\n        function startStudyTimer() { studyTimerInterval = setInterval(updateStudyTimer, 1000); }", timer_inject)

# 4. Inject Confetti Function
confetti_inject = """        function playPomodoroComplete() { try { const a = new (window.AudioContext || window.webkitAudioContext)(), o = a.createOscillator(), g = a.createGain(); o.connect(g); g.connect(a.destination); o.frequency.value = 800; o.type = 'sine'; g.gain.value = 0.3; o.start(); setTimeout(() => { o.stop(); a.close(); }, 500); } catch (e) { } }

        function fireConfetti() {
            const duration = 3000;
            const end = Date.now() + duration;

            (function frame() {
                const confetto = document.createElement('div');
                confetto.style.position = 'fixed';
                confetto.style.left = Math.random() * 100 + 'vw';
                confetto.style.top = '-10px';
                confetto.style.width = '8px';
                confetto.style.height = '16px';
                confetto.style.backgroundColor = hsl(, 100%, 60%);
                confetto.style.zIndex = '99999';
                confetto.style.pointerEvents = 'none';
                confetto.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
                document.body.appendChild(confetto);

                const fallDuration = Math.random() * 2000 + 1000;
                const animation = confetto.animate([
                    { transform: 	ranslate3d(0,0,0) rotate(0deg), opacity: 1 },
                    { transform: 	ranslate3d(px, 100vh, 0) rotate(deg), opacity: 0 }
                ], {
                    duration: fallDuration,
                    easing: 'cubic-bezier(.37,0,.63,1)'
                });

                animation.onfinish = () => confetto.remove();
                if (Date.now() < end) requestAnimationFrame(frame);
            }());
        }

        // --- POMODORO TIMER GAMIFICATION ---"""
content = content.replace("        function playPomodoroComplete() { try { const a = new (window.AudioContext || window.webkitAudioContext)(), o = a.createOscillator(), g = a.createGain(); o.connect(g); g.connect(a.destination); o.frequency.value = 800; o.type = 'sine'; g.gain.value = 0.3; o.start(); setTimeout(() => { o.stop(); a.close(); }, 500); } catch (e) { } }", confetti_inject)


# 5. Overhaul Pomodoro Update and Setup Logic
import re
pomo_pattern = re.compile(r"        function formatPomodoroTime[\s\S]*?updatePomodoroDisplay\(\); }")

new_pomo_logic = """        function formatPomodoroTime(t) { return ${Math.floor(t / 60).toString().padStart(2, '0')}:; }
        
        function updatePomodoroDisplay() { 
            const d = document.getElementById('pomodoroDisplay'); 
            if (d) { 
                d.textContent = formatPomodoroTime(pomodoroSeconds); 
                d.classList.toggle('running', pomodoroRunning); 
            } 
            
            // Gamification: Update Flight Path progress
            const fill = document.getElementById('flightPathFill');
            const label = document.getElementById('flightPathLabel');
            if (fill && label) {
                if (!pomodoroRunning && pomodoroSeconds === pomodoroInitialSeconds) {
                    fill.style.width = '0%';
                    label.textContent = 'Ready for Takeoff';
                    label.style.color = 'var(--text-muted)';
                } else {
                    const pct = Math.max(0, Math.min(100, ((pomodoroInitialSeconds - pomodoroSeconds) / pomodoroInitialSeconds) * 100));
                    fill.style.width = pct + '%';
                    
                    if (pct === 100) { label.textContent = 'Touchdown! Focus complete.'; label.style.color = 'var(--gold)'; }
                    else if (pct > 90) { label.textContent = 'Final Approach...'; label.style.color = 'var(--warning)'; }
                    else if (pct > 10) { label.textContent = 'Cruising Altitude (Focus Mode)'; label.style.color = 'var(--success)'; }
                    else { label.textContent = 'Climbing...'; label.style.color = 'var(--module-color)'; }
                }
            }
        }
        
        function togglePomodoro() {
            const btn = document.getElementById('pomoStart');
            if (pomodoroRunning) { 
                // Forest app style abort warning
                if(confirm("Abort the flight? Your focus progress will be lost.")){
                    resetPomodoro();
                }
            }
            else {
                pomodoroRunning = true; btn.innerHTML = '&#10074;&#10074;'; /* Pause bars */ btn.classList.add('playing');
                pomodoroInterval = setInterval(() => { 
                    if (pomodoroSeconds > 0) { 
                        pomodoroSeconds--; 
                        updatePomodoroDisplay(); 
                    } else { 
                        clearInterval(pomodoroInterval); 
                        pomodoroRunning = false; 
                        btn.innerHTML = '&#9654;'; /* Play icon */
                        btn.classList.remove('playing'); 
                        updatePomodoroDisplay();
                        playPomodoroComplete(); 
                        fireConfetti();
                    } 
                }, 1000);
            } 
            updatePomodoroDisplay();
        }
        function resetPomodoro() { clearInterval(pomodoroInterval); pomodoroRunning = false; pomodoroSeconds = pomodoroInitialSeconds; const b = document.getElementById('pomoStart'); if (b) { b.innerHTML = '&#9654;'; b.classList.remove('playing'); } updatePomodoroDisplay(); }
        function setPomodoro(min) { clearInterval(pomodoroInterval); pomodoroRunning = false; pomodoroSeconds = min * 60; pomodoroInitialSeconds = min * 60; const b = document.getElementById('pomoStart'); if (b) { b.innerHTML = '&#9654;'; b.classList.remove('playing'); } updatePomodoroDisplay(); }"""

content = pomo_pattern.sub(new_pomo_logic, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Script completed successfully.')
