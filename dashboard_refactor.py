import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add background elements
if '<div class="cyber-bg\">' not in text:
    text = text.replace('<body>', '<body>\n\n  <div class="cyber-bg"></div>\n  <div class="cyber-grid"></div>\n')

# 2. Replace CSS using string slicing between unique markers
css_start = text.find('/* ═══════════════════════════════════════════════════════════\n       DASHBOARD-SPECIFIC STYLES')
css_end = text.find('</style>', css_start)

if css_start != -1 and css_end != -1:
    new_css = r'''/* ═══════════════════════════════════════════════════════════
       PREMIUM COMMAND CENTER STYLES
    ═══════════════════════════════════════════════════════════ */

    /* HD Cinematic Background */
    .cyber-bg {
      position: fixed; inset: 0;
      background: radial-gradient(circle at 15% 50%, rgba(212, 168, 83, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 30%, rgba(34, 211, 238, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 100%, rgba(45, 189, 137, 0.05) 0%, transparent 50%),
        linear-gradient(180deg, rgba(8, 12, 26, 0) 0%, rgba(8, 12, 26, 0.9) 100%),
        url('data:image/svg+xml;utf8,<svg width="40" height="40" xmlns="http://www.w3.org/2000/svg"><path d="M0 40 L40 0" stroke="rgba(255,255,255,0.02)" stroke-width="1"/></svg>');
      z-index: -1; pointer-events: none;
    }

    .cyber-grid {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
      background-size: 50px 50px;
      transform: perspective(500px) rotateX(60deg) translateY(-100px) translateZ(-200px);
      transform-origin: center top; opacity: 0.3; z-index: -2; pointer-events: none;
      animation: gridMove 20s linear infinite;
    }
    @keyframes gridMove { 0% { background-position: 0 0; } 100% { background-position: 0 50px; } }
    @keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

    .main { max-width: 1400px; margin: 0 auto; padding: 40px 24px 80px; position: relative; z-index: 10; animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; opacity: 0; transform: translateY(20px); }

    /* HERO BANNER */
    .hero {
      display: flex; align-items: center; gap: 32px; margin-bottom: 48px; padding: 32px 40px;
      background: rgba(20, 24, 38, 0.4); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
      border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px;
      box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1); position: relative; overflow: hidden;
    }
    .hero::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: linear-gradient(to bottom, var(--gold), var(--blue)); box-shadow: 0 0 20px rgba(212, 168, 83, 0.8); }
    .hero-ace-wrap { position: relative; width: 130px; height: 130px; flex-shrink: 0; background: radial-gradient(circle, rgba(212, 168, 83, 0.1) 0%, transparent 70%); border-radius: 50%; }
    .hero-ace, .hero-ace-steam { position: absolute; top: 0; left: 0; width: 130px; height: 130px; image-rendering: pixelated; }
    .hero-content { flex: 1; }
    .hero-label { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); margin-bottom: 8px; }
    .hero-title { font-size: 36px; font-weight: 800; letter-spacing: -1px; margin-bottom: 24px; background: linear-gradient(180deg, #FFFFFF 0%, #A0AEC0 100%); -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .hero-stats { display: flex; align-items: center; gap: 24px; background: rgba(0,0,0,0.2); padding: 16px 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); flex-wrap: wrap; }
    .hero-stat { display: flex; flex-direction: column; gap: 4px; }
    .hero-stat-value { font-family: var(--font-mono); font-size: 28px; font-weight: 800; color: white; text-shadow: 0 0 15px rgba(255,255,255,0.2); line-height: 1; }
    .hero-stat-value.grade-a { color: var(--success); text-shadow: 0 0 15px rgba(52,211,153,0.3); }
    .hero-stat-value.grade-b { color: var(--warning); text-shadow: 0 0 15px rgba(251,191,36,0.3); }
    .hero-stat-value.grade-c { color: #fb923c; text-shadow: 0 0 15px rgba(251,146,60,0.3); }
    .hero-stat-value.grade-d { color: var(--danger); text-shadow: 0 0 15px rgba(248,113,113,0.3); }
    .hero-stat-value.grade-f { color: var(--text-muted); }
    .hero-stat-label { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }
    .hero-stat-sub { font-size: 10px; color: var(--gold); font-weight: 500; margin-top: 1px; }
    .hero-divider { width: 1px; height: 36px; background: rgba(255,255,255,0.1); }
    
    .hero-coaching { margin-top: 24px; padding: 16px 24px; background: rgba(212, 168, 83, 0.05); border: 1px solid rgba(212, 168, 83, 0.2); border-left: 4px solid var(--gold); border-radius: 16px; display: flex; align-items: flex-start; gap: 16px; box-shadow: 0 0 20px rgba(212, 168, 83, 0.1) inset; opacity: 0; transform: translateY(10px); transition: all 400ms ease;}
    .hero-coaching.visible { opacity: 1; transform: translateY(0); }
    .hero-coaching-icon { color: var(--gold); width: 24px; height: 24px; }
    .hero-coaching-title { font-size: 11px; font-weight: 800; color: var(--gold); letter-spacing: 1.5px; margin-bottom: 4px; }
    .hero-coaching-text { font-size: 15px; color: white; line-height: 1.5; }
    .hero-coaching-text a { color: var(--gold); text-decoration: underline; font-weight: 500; transition: color 200ms ease; }
    .hero-coaching-text a:hover { color: #FFF; }

    /* HOLOGRAPHIC MODE CARDS */
    .section-header { margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; }
    .section-title { font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; color: var(--text-muted); text-shadow: 0 0 10px rgba(255,255,255,0.1); }
    .mode-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; margin-bottom: 56px; }

    .holo-card { position: relative; background: rgba(20, 24, 38, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; text-decoration: none; color: inherit; display: flex; flex-direction: column; align-items: center; text-align: center; padding: 48px 32px; overflow: hidden; transform-style: preserve-3d; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); }
    .holo-card::before { content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px); pointer-events: none; mix-blend-mode: overlay; z-index: 2; }
    .holo-card::after { content: ''; position: absolute; inset: -2px; background: linear-gradient(45deg, transparent, transparent, transparent); border-radius: 26px; z-index: -1; opacity: 0; transition: opacity 0.3s; }
    .holo-card:hover::after { opacity: 1; }

    .holo-journey::after { background: linear-gradient(135deg, rgba(212, 168, 83, 0.4), transparent); box-shadow: 0 0 40px rgba(212, 168, 83, 0.15); }
    .holo-classroom::after { background: linear-gradient(135deg, rgba(45, 189, 137, 0.4), transparent); box-shadow: 0 0 40px rgba(45, 189, 137, 0.15); }
    .holo-practice::after { background: linear-gradient(135deg, rgba(34, 211, 238, 0.4), transparent); box-shadow: 0 0 40px rgba(34, 211, 238, 0.15); }

    .holo-content { z-index: 10; transform: translateZ(30px); display: flex; flex-direction: column; align-items: center; height: 100%; }
    .mode-icon { width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); margin-bottom: 24px; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .holo-journey .mode-icon { color: var(--gold); filter: drop-shadow(0 0 15px rgba(212, 168, 83, 0.3)); }
    .holo-classroom .mode-icon { color: #2DBD89; filter: drop-shadow(0 0 15px rgba(45, 189, 137, 0.3)); }
    .holo-practice .mode-icon { color: #22d3ee; filter: drop-shadow(0 0 15px rgba(34, 211, 238, 0.3)); }
    .holo-card:hover .mode-icon { transform: scale(1.15) translateY(-5px); }
    .mode-title { font-size: 28px; font-weight: 800; color: white; margin-bottom: 12px; }
    .mode-desc { font-size: 15px; color: var(--text-muted); line-height: 1.5; margin-bottom: 32px; flex: 1; }

    .card-arrow { width: 48px; height: 48px; border-radius: 50%; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center; color: white; transition: all 0.3s; }
    .holo-card:hover .card-arrow { transform: scale(1.1); background: rgba(255,255,255,0.15); box-shadow: 0 0 20px rgba(255,255,255,0.2); }
    .holo-card:hover .holo-journey-arrow { color: #000; background: var(--gold); border-color: var(--gold); box-shadow: 0 0 20px var(--gold); }
    .holo-card:hover .holo-classroom-arrow { color: #000; background: #2DBD89; border-color: #2DBD89; box-shadow: 0 0 20px #2DBD89; }
    .holo-card:hover .holo-practice-arrow { color: #000; background: #22d3ee; border-color: #22d3ee; box-shadow: 0 0 20px #22d3ee; }

    /* FINAL EXAM CARD */
    .final-exam-card { display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 32px 40px; background: rgba(248, 113, 113, 0.03); backdrop-filter: blur(24px); border: 1px solid rgba(248, 113, 113, 0.2); border-radius: 24px; text-decoration: none; color: inherit; position: relative; overflow: hidden; animation: pulseBorder 4s infinite alternate; }
    @keyframes pulseBorder { 0% { box-shadow: 0 0 20px rgba(248, 113, 113, 0.05) inset, 0 0 10px rgba(248, 113, 113, 0.05); } 100% { box-shadow: 0 0 40px rgba(248, 113, 113, 0.15) inset, 0 0 30px rgba(248, 113, 113, 0.2); border-color: rgba(248, 113, 113, 0.5); } }
    .final-exam-left { display: flex; align-items: center; gap: 24px; z-index: 10; }
    .final-exam-icon { width: 64px; height: 64px; border-radius: 20px; background: rgba(248, 113, 113, 0.1); border: 1px solid rgba(248, 113, 113, 0.3); display: flex; align-items: center; justify-content: center; color: var(--danger); filter: drop-shadow(0 0 15px rgba(248, 113, 113, 0.4)); }
    .final-exam-label { font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: var(--danger); margin-bottom: 4px; }
    .final-exam-title { font-size: 24px; font-weight: 800; color: white; margin-bottom: 4px; }
    .final-exam-desc { font-size: 14px; color: var(--text-muted); }
    .final-exam-meta { display: flex; align-items: center; gap: 32px; z-index: 10; width: auto; justify-content: flex-end; }
    .final-exam-stat { text-align: center; }
    .final-exam-stat-val { font-family: var(--font-mono); font-size: 24px; font-weight: 800; color: white; margin-bottom: 4px; line-height: 1; }
    .final-exam-stat-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; font-weight: 800;}
    .final-exam-btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 28px; background: linear-gradient(135deg, var(--danger), #b91c1c); border: none; border-radius: 12px; font-size: 15px; font-weight: 800; color: white; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 10px 20px rgba(248, 113, 113, 0.3); transition: all 0.3s; white-space: nowrap; }
    .final-exam-card:hover .final-exam-btn { transform: scale(1.05); box-shadow: 0 15px 30px rgba(248, 113, 113, 0.5); }

    @media (max-width: 1000px) {
      .mode-grid { grid-template-columns: 1fr; }
      .hero { flex-direction: column; text-align: center; }
      .hero-stats { justify-content: center; }
      .final-exam-card { flex-direction: column; align-items: center; text-align: center; }
      .final-exam-meta { width: 100%; justify-content: center; flex-wrap: wrap; }
    }
'''
    text = text[:css_start] + new_css + text[css_end:]

# 3. Replace card HTML structure
# Use string replacement for entire a tags to ensure accuracy
text = text.replace(
'''        <a href="journey.html" class="mode-card" data-mode="journey">
          <div class="mode-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <div class="mode-title">Learner's Journey</div>
          <div class="mode-desc">Embark on a guided, node-based microlesson adventure to master CAET standards
            step-by-step.</div>
          <div class="mode-btn">
            Enter Journey
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              style="width:16px; height:16px;">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </a>''',
'''        <a href="journey.html" class="holo-card holo-journey" data-mode="journey">
          <div class="holo-content">
            <div class="mode-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" /></svg>
            </div>
            <div class="mode-title">Learner's Journey</div>
            <div class="mode-desc">Embark on a guided, node-based microlesson adventure to master CAET standards step-by-step.</div>
            <div class="card-arrow holo-journey-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </div>
        </a>'''
)

text = text.replace(
'''        <a href="classroom.html" class="mode-card" data-mode="classroom">
          <div class="mode-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </div>
          <div class="mode-title">Classroom</div>
          <div class="mode-desc">The traditional path. Deep-dive into interactive Rise modules, textbooks, and AI
            notebook tracking.</div>
          <div class="mode-btn">
            Enter Classroom
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              style="width:16px; height:16px;">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </a>''',
'''        <a href="classroom.html" class="holo-card holo-classroom" data-mode="classroom">
          <div class="holo-content">
            <div class="mode-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
              </svg>
            </div>
            <div class="mode-title">Classroom</div>
            <div class="mode-desc">The traditional path. Deep-dive into interactive Rise modules, textbooks, and AI notebook tracking.</div>
            <div class="card-arrow holo-classroom-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </div>
        </a>'''
)

text = text.replace(
'''        <a href="practice.html" class="mode-card" data-mode="practice">
          <div class="mode-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
              <polyline points="14 2 14 8 20 8" />
              <circle cx="10" cy="13" r="2" />
              <path d="m14 17-2.5-3" />
            </svg>
          </div>
          <div class="mode-title">Practice Area</div>
          <div class="mode-desc">Prove what you know in the trenches! Test yourself with Flash Cards, Drills, and Battle
            ACE.</div>
          <div class="mode-btn">
            Enter Practice
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
              style="width:16px; height:16px;">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </div>
        </a>''',
'''        <a href="practice.html" class="holo-card holo-practice" data-mode="practice">
          <div class="holo-content">
            <div class="mode-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                <polyline points="14 2 14 8 20 8" />
                <circle cx="10" cy="13" r="2" />
                <path d="m14 17-2.5-3" />
              </svg>
            </div>
            <div class="mode-title">Practice Area</div>
            <div class="mode-desc">Prove what you know in the trenches! Test yourself with Flash Cards, Drills, and Battle ACE.</div>
            <div class="card-arrow holo-practice-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </div>
        </a>'''
)

# 4. Add the 3D script before closing body tag
script_addon = '''
  <script>
      // 3D Holographic Tilt Script
      document.querySelectorAll('.holo-card').forEach(card => {
          let rafId;
          let currentX = 0; let currentY = 0;
          let targetX = 0; let targetY = 0;
          const ease = 0.1; 
          const maxRot = 8; 

          function animate() {
              currentX += (targetX - currentX) * ease;
              currentY += (targetY - currentY) * ease;
              const rotateX = currentY * maxRot;
              const rotateY = currentX * -maxRot;
              
              card.style.transform = perspective(1000px) rotateX(deg) rotateY(deg) scale3d(1.02, 1.02, 1.02);
              rafId = requestAnimationFrame(animate);
          }

          card.addEventListener('mouseenter', () => { cancelAnimationFrame(rafId); animate(); });

          card.addEventListener('mousemove', e => {
              const rect = card.getBoundingClientRect();
              const x = e.clientX - rect.left;
              const y = e.clientY - rect.top;
              const centerX = rect.width / 2;
              const centerY = rect.height / 2;
              targetX = (x - centerX) / centerX;
              targetY = (y - centerY) / centerY;
          });
          
          card.addEventListener('mouseleave', () => {
              cancelAnimationFrame(rafId);
              card.style.transform = perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1);
              targetX = 0; targetY = 0; currentX = 0; currentY = 0;
          });
      });
  </script>
</body>'''

if '3D Holographic Tilt Script' not in text:
    text = text.replace('</body>', script_addon)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("SUCCESS")
