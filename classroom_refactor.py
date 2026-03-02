import os

with open('classroom.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace bg-orbs with cyber-bg
bg_old = """    <div class="bg-orbs">
        <div class="orb-1"></div>
        <div class="orb-2"></div>
        <div class="orb-3"></div>
    </div>"""
bg_new = """    <div class="cyber-bg"></div>
    <div class="cyber-grid"></div>"""
html = html.replace(bg_old, bg_new)

# Replace the Animated Background Orbs CSS
css_old = html[html.find('/* BASE & BACKGROUND */'):html.find('/* PREMIUM HERO BANNER */')]
css_new = """/* BASE & BACKGROUND */
        body {
            position: relative;
            background-color: transparent !important;
            overflow-x: hidden;
            min-height: 100vh;
        }

        /* PREMIUM COMMAND CENTER BACKGROUND */
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

        .main {
"""
html = html.replace(css_old, css_new)

# Replace the GLASSMORPHIC CARDS CSS
cards_old = html[html.find('/* GLASSMORPHIC CARDS */'):html.find('        @media (max-width: 768px) {')]

cards_new = """/* HOLOGRAPHIC 3D CARDS */
        .resource-card {
            position: relative;
            display: flex;
            align-items: center;
            gap: 20px;
            background: rgba(20, 24, 38, 0.4);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 24px;
            text-decoration: none;
            color: inherit;
            overflow: hidden;
            transform-style: preserve-3d;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            z-index: 1;
        }
        .resource-card::before {
            content: ''; position: absolute; inset: 0;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.03) 2px, rgba(255,255,255,0.03) 4px);
            pointer-events: none; mix-blend-mode: overlay; z-index: 2;
        }
        .resource-card::after {
            content: ''; position: absolute; inset: -2px;
            background: linear-gradient(45deg, transparent, transparent, transparent);
            border-radius: 22px; z-index: -1; opacity: 0; transition: opacity 0.3s;
        }
        .resource-card:hover::after { opacity: 1; }
        .resource-card.rise::after { background: linear-gradient(135deg, rgba(212, 168, 83, 0.4), transparent); box-shadow: 0 0 40px rgba(212, 168, 83, 0.15); }
        .resource-card.notebook::after { background: linear-gradient(135deg, rgba(45, 189, 137, 0.4), transparent); box-shadow: 0 0 40px rgba(45, 189, 137, 0.15); }
        .resource-card.book::after { background: linear-gradient(135deg, rgba(97, 175, 239, 0.4), transparent); box-shadow: 0 0 40px rgba(97, 175, 239, 0.15); }

        .resource-card:hover { z-index: 10; transform: translateY(-6px) scale(1.02); }

        .resource-icon {
            width: 56px; height: 56px; border-radius: 16px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0; transition: transform 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative; transform: translateZ(30px);
        }
        .resource-card:hover .resource-icon { transform: translateZ(30px) scale(1.15) rotate(5deg); }

        .resource-card.rise .resource-icon { background: rgba(212, 168, 83, 0.1); color: var(--gold); border: 1px solid rgba(212, 168, 83, 0.3); box-shadow: 0 0 15px rgba(212, 168, 83, 0.15) inset; }
        .resource-card.notebook .resource-icon { background: rgba(45, 189, 137, 0.1); color: #2DBD89; border: 1px solid rgba(45, 189, 137, 0.3); box-shadow: 0 0 15px rgba(45, 189, 137, 0.15) inset; }
        .resource-card.book .resource-icon { background: rgba(97, 175, 239, 0.1); color: var(--blue); border: 1px solid rgba(97, 175, 239, 0.3); box-shadow: 0 0 15px rgba(97, 175, 239, 0.15) inset; }
        .resource-icon svg { width: 28px; height: 28px; filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5)); }

        .resource-info { flex: 1; min-width: 0; transform: translateZ(30px); }
        .resource-name { font-size: 17px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.3px; }
        .resource-meta { font-size: 13px; color: var(--text-muted); line-height: 1.5; display: flex; align-items: center; gap: 6px; }

        .resource-action {
            width: 40px; height: 40px; border-radius: 50%;
            background: rgba(255, 255, 255, 0.03); display: flex; align-items: center; justify-content: center;
            color: var(--text-muted); transition: all 400ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
            opacity: 0; border: 1px solid rgba(255, 255, 255, 0.1);
            transform: translateZ(30px) translateX(-15px) scale(0.8);
        }
        .resource-card:hover .resource-action { opacity: 1; transform: translateZ(30px) translateX(0) scale(1); }
        .resource-card.rise:hover .resource-action { color: var(--gold); background: rgba(212, 168, 83, 0.15); border-color: rgba(212, 168, 83, 0.3); }
        .resource-card.notebook:hover .resource-action { color: #2DBD89; background: rgba(45, 189, 137, 0.15); border-color: rgba(45, 189, 137, 0.3); }
        .resource-card.book:hover .resource-action { color: var(--blue); background: rgba(97, 175, 239, 0.15); border-color: rgba(97, 175, 239, 0.3); }

"""
if cards_old and len(cards_old) > 50:
    html = html.replace(cards_old, cards_new)

# Add Script at the bottom

script_body = """
    <!-- 3D Holographic Tilt Script -->
    <script>
        document.querySelectorAll('.resource-card').forEach(card => {
            let rafId;
            let currentX = 0; let currentY = 0;
            let targetX = 0; let targetY = 0;
            const ease = 0.1; 
            const maxRot = 5; 

            function animate() {
                currentX += (targetX - currentX) * ease;
                currentY += (targetY - currentY) * ease;
                const rotateX = currentY * maxRot;
                const rotateY = currentX * -maxRot;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
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
                card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
                targetX = 0; targetY = 0; currentX = 0; currentY = 0;
            });
        });
    </script>
</body>"""

if '3D Holographic Tilt Script' not in html:
    html = html.replace('</body>', script_body)

with open('classroom.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS classroom.html updated")
