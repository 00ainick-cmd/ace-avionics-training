import os
import re

with open('classroom.html', 'r', encoding='utf-8') as f:
    html = f.read()

# --- CSS UPDATES ---

# Add the new track layout CSS, replacing the old grid layout
css_replacement = """
        /* CURRICULUM TRACKS (NETFLIX STYLE) */
        .resource-section {
            margin-bottom: 64px;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
            padding: 0 40px; /* Align with track padding */
        }

        .section-title {
            font-size: 18px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: white;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .section-badge {
            font-size: 11px;
            font-weight: 800;
            padding: 4px 12px;
            border-radius: 20px;
            letter-spacing: 1px;
            background: rgba(212, 168, 83, 0.1);
            color: var(--gold);
            border: 1px solid rgba(212, 168, 83, 0.3);
            box-shadow: 0 0 15px rgba(212, 168, 83, 0.15) inset;
        }

        .section-badge.green {
            background: rgba(45, 189, 137, 0.1);
            color: #2DBD89;
            border: 1px solid rgba(45, 189, 137, 0.3);
            box-shadow: 0 0 15px rgba(45, 189, 137, 0.15) inset;
        }

        /* The scrolling container */
        .track-container {
            position: relative;
            width: 100%;
            overflow-x: auto;
            overflow-y: hidden;
            white-space: nowrap;
            padding: 20px 40px 40px 40px; /* Extra padding for shadows/transforms */
            margin: -20px -40px -40px -40px; /* Offset the padding to align with container */
            scroll-behavior: smooth;
            /* Hide scrollbar */
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .track-container::-webkit-scrollbar { display: none; }

        /* Card styles specific to tracks */
        .resource-card {
            display: inline-flex;  /* Override the flex block */
            vertical-align: top;
            width: 400px; /* Fixed width for horizontal scrolling */
            margin-right: 24px;
            white-space: normal; /* Allow text to wrap inside the card */
            
            position: relative;
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
            /* overflow: hidden; Removed so the 3D perspective doesn't clip */
            transform-style: preserve-3d;
            box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            z-index: 1;
            transition: all 0.3s ease;
        }
        
        /* Add category badge inside the card */
        .card-cat-badge {
            position: absolute;
            top: -12px;
            right: 24px;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1px;
            z-index: 20;
            background: var(--surface);
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            transform: translateZ(40px);
        }
        
        .cat-mrd { color: #facc15; border: 1px solid rgba(250, 204, 21, 0.3); } /* Yellow */
        .cat-bet { color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3); } /* Blue */
        .cat-cns { color: #c084fc; border: 1px solid rgba(192, 132, 252, 0.3); } /* Purple */
        .cat-fi { color: #f472b6; border: 1px solid rgba(244, 114, 182, 0.3); } /* Pink */
        .cat-dds { color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); } /* Emerald */
        .cat-awh { color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); } /* Red */
        .cat-tte { color: #fb923c; border: 1px solid rgba(251, 146, 60, 0.3); } /* Orange */
        .cat-ssp { color: #a3e635; border: 1px solid rgba(163, 230, 53, 0.3); } /* Lime */
        .cat-all { color: var(--gold); border: 1px solid rgba(212, 168, 83, 0.3); background: rgba(212, 168, 83, 0.1);}

        .resource-card::before {
            content: ''; position: absolute; inset: 0; border-radius: 20px;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.02) 2px, rgba(255,255,255,0.02) 4px);
            pointer-events: none; mix-blend-mode: overlay; z-index: 2;
        }
        .resource-card::after {
            content: ''; position: absolute; inset: -2px;
            background: linear-gradient(45deg, transparent, transparent, transparent);
            border-radius: 22px; z-index: -1; opacity: 0; transition: opacity 0.3s;
        }
        .resource-card:hover::after { opacity: 1; }
        .resource-card.rise::after { background: linear-gradient(135deg, rgba(212, 168, 83, 0.3), transparent); box-shadow: 0 0 30px rgba(212, 168, 83, 0.15); }
        .resource-card.notebook::after { background: linear-gradient(135deg, rgba(45, 189, 137, 0.3), transparent); box-shadow: 0 0 30px rgba(45, 189, 137, 0.15); }

        .resource-card:hover { z-index: 10; }

        .resource-icon {
            width: 56px; height: 56px; border-radius: 16px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0; transition: transform 300ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative; transform: translateZ(30px);
        }
        .resource-card:hover .resource-icon { transform: translateZ(30px) scale(1.15) rotate(5deg); }

        .resource-card.rise .resource-icon { background: rgba(212, 168, 83, 0.1); color: var(--gold); border: 1px solid rgba(212, 168, 83, 0.3); box-shadow: 0 0 15px rgba(212, 168, 83, 0.15) inset; }
        .resource-card.notebook .resource-icon { background: rgba(45, 189, 137, 0.1); color: #2DBD89; border: 1px solid rgba(45, 189, 137, 0.3); box-shadow: 0 0 15px rgba(45, 189, 137, 0.15) inset; }
        
        .resource-icon svg { width: 28px; height: 28px; filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5)); }

        .resource-info { flex: 1; min-width: 0; transform: translateZ(30px); }
        .resource-name { font-size: 17px; font-weight: 700; color: white; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.3px; }
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

        /* Track Navigation Arrows */
        .track-nav {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: rgba(20, 24, 38, 0.8);
            border: 1px solid rgba(255,255,255,0.1);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 50;
            backdrop-filter: blur(10px);
            opacity: 0;
            transition: all 0.3s ease;
        }
        .resource-section:hover .track-nav { opacity: 1; }
        .track-nav:hover { background: rgba(255,255,255,0.1); transform: translateY(-50%) scale(1.1); }
        .track-nav.prev { left: 10px; }
        .track-nav.next { right: 10px; }

"""

# Regex out the old section styling and replace it
html = re.sub(r'/\* SECTION STYLING \*/.*?@media \(max-width: 768px\)', css_replacement + '        @media (max-width: 768px)', html, flags=re.DOTALL)


# --- HTML UPDATES ---

html_replacement = """        <!-- MARQUEE: CONTINUE LEARNING -->
        <div class="resource-section" style="margin-top: 24px;">
            <div class="section-header" style="justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="section-title" style="color: var(--gold);">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px;">
                            <polygon points="5 3 19 12 5 21 5 3"/>
                        </svg>
                        Up Next For You
                    </div>
                </div>
            </div>
            
            <a href="shared/course-viewer.html?path=rise-modules/electricity-dc/fundamentals-of-direct-current&title=Direct Current Fundamentals" 
               class="resource-card rise" style="display: flex; width: 100%; max-width: 800px; margin: 0 40px; padding: 32px; gap: 32px;">
                <div class="card-cat-badge cat-bet">BET</div>
                <div class="resource-icon" style="width: 80px; height: 80px; border-radius: 20px;">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:40px; height:40px;">
                    <polygon points="5 3 19 12 5 21 5 3"/>
                  </svg>
                </div>
                <div class="resource-info">
                  <div class="resource-meta" style="color: var(--gold); font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px;">Recommended Review</div>
                  <div class="resource-name" style="font-size: 24px;">Direct Current Fundamentals</div>
                  <div class="resource-meta" style="margin-top: 8px; color: rgba(255,255,255,0.6);">Based on your recent mock exam, you should review this module before proceeding to Alternating Current.</div>
                </div>
                <div class="resource-action" style="width: 56px; height: 56px;"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
            </a>
        </div>

        <!-- TRACK 1: RISE MODULES -->
        <div class="resource-section">
            <div class="section-header">
                <div class="section-title">Interactive Modules <span class="section-badge">13 Available</span></div>
            </div>
            <div style="position: relative;">
                <button class="track-nav prev" onclick="scrollTrack('riseTrack', -600)"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg></button>
                <div class="track-container" id="riseTrack">
                    <!-- Populated by JS -->
                </div>
                <button class="track-nav next" onclick="scrollTrack('riseTrack', 600)"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></button>
            </div>
        </div>

        <!-- TRACK 2: AI NOTEBOOKS -->
        <div class="resource-section">
            <div class="section-header" style="justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 16px;">
                    <div class="section-title">AI Study Boss Guides <span class="section-badge green">Tools</span></div>
                </div>
                <button onclick="alert('NotebookLM Tutorial: 1. Download course PDF. 2. Upload to NotebookLM. 3. Ask it questions about the material!')" class="section-badge" style="cursor: pointer; background: transparent; color: var(--text-muted); border-color: rgba(255,255,255,0.2);">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px; margin-right:6px; vertical-align:middle;">
                        <circle cx="12" cy="12" r="10" />
                        <path d="M12 16v-4" />
                        <path d="M12 8h.01" />
                    </svg>
                    How to use Guides
                </button>
            </div>
            <div style="position: relative;">
                <button class="track-nav prev" onclick="scrollTrack('notebookTrack', -600)"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg></button>
                <div class="track-container" id="notebookTrack">
                    <!-- Populated by JS -->
                </div>
                <button class="track-nav next" onclick="scrollTrack('notebookTrack', 600)"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg></button>
            </div>
        </div>"""

html = re.sub(r'<div class="resource-section">.*?</div>\n        </div>\n    </main>', html_replacement + '\n    </main>', html, flags=re.DOTALL)

# --- JS UPDATES ---

js_replacement = """        function scrollTrack(id, amount) {
            document.getElementById(id).scrollBy({ left: amount, behavior: 'smooth' });
        }

        const listHtml = MODULES.map(m => `
      <a href="${m.path}" class="resource-card rise">
        <div class="card-cat-badge cat-${m.num.toLowerCase()}">${m.num}</div>
        <div class="resource-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="5 3 19 12 5 21 5 3"/>
          </svg>
        </div>
        <div class="resource-info">
          <div class="resource-name" title="${m.name}">${m.name}</div>
          <div class="resource-meta">Rise 360 &bull; Interactive</div>
        </div>
        <div class="resource-action"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
      </a>
    `).join('');
        document.getElementById('riseTrack').innerHTML = listHtml;

        const aiHtml = NOTEBOOK_LINKS.map(n => `
      <a href="${n.url}" target="_blank" class="resource-card notebook">
        <div class="card-cat-badge cat-${n.cat.toLowerCase()}">${n.cat}</div>
        <div class="resource-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 2A2 2 0 0 1 14 4V6H20A2 2 0 0 1 22 8V18A2 2 0 0 1 20 20H4A2 2 0 0 1 2 18V8A2 2 0 0 1 4 6H10V4A2 2 0 0 1 12 2z"/>
            <path d="M6 10H6.01"/><path d="M18 10H18.01"/><path d="M10 16H14"/>
          </svg>
        </div>
        <div class="resource-info">
          <div class="resource-name" title="${n.name}">${n.name}</div>
          <div class="resource-meta">Study Guide &bull; Ask AI</div>
        </div>
        <div class="resource-action"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg></div>
      </a>
    `).join('');
        document.getElementById('notebookTrack').innerHTML = aiHtml;"""

html = re.sub(r'const listHtml = MODULES.map.*?document\.getElementById\(\'aiGuidesList\'\)\.innerHTML = aiHtml;', js_replacement, html, flags=re.DOTALL)


with open('classroom.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS classroom.html horizontally redesigned")
