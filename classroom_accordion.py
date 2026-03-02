import os
import re

with open('classroom.html', 'r', encoding='utf-8') as f:
    html = f.read()

# --- 1. CSS UPDATES ---
css_replacement = """        /* CATEGORY ACCORDIONS */
        .resource-section {
            margin-bottom: 32px;
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }

        .category-accordion {
            background: rgba(20, 24, 38, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            margin-bottom: 16px;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .category-accordion.open {
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .accordion-header {
            padding: 24px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.02));
        }

        .accordion-header:hover {
            background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(255,255,255,0.05));
        }

        .accordion-title-area {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .accordion-title {
            font-size: 18px;
            font-weight: 700;
            color: white;
            letter-spacing: 0.5px;
        }

        .accordion-subtitle {
            font-size: 14px;
            color: var(--text-muted);
        }

        .chevron {
            width: 24px;
            height: 24px;
            color: var(--text-muted);
            transition: transform 0.3s ease;
        }

        .category-accordion.open .chevron {
            transform: rotate(180deg);
            color: white;
        }

        .accordion-content {
            display: none;
            padding: 0 32px 32px 32px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        .category-accordion.open .accordion-content {
            display: block;
            animation: slideDown 0.3s ease-out;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Inner Content Grid */
        .content-split {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 40px;
            margin-top: 32px;
        }

        .content-column h3 {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .content-column h3::after {
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, rgba(255,255,255,0.1), transparent);
        }

        .items-grid {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        /* Adjust card styles for accordion layout */
        .resource-card {
            display: flex; /* Back to flex, no longer inline */
            width: 100%;
            position: relative;
            align-items: center;
            gap: 20px;
            background: rgba(20, 24, 38, 0.4);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transform-style: preserve-3d;
            box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
            z-index: 1;
            transition: all 0.3s ease;
        }
        
        .card-cat-badge {
            position: absolute;
            top: -10px;
            right: 20px;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            z-index: 20;
            background: var(--surface);
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            transform: translateZ(20px);
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
            content: ''; position: absolute; inset: 0; border-radius: 16px;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.02) 2px, rgba(255,255,255,0.02) 4px);
            pointer-events: none; mix-blend-mode: overlay; z-index: 2;
        }
        .resource-card::after {
            content: ''; position: absolute; inset: -2px;
            background: linear-gradient(45deg, transparent, transparent, transparent);
            border-radius: 18px; z-index: -1; opacity: 0; transition: opacity 0.3s;
        }
        .resource-card:hover::after { opacity: 1; }
        .resource-card.rise::after { background: linear-gradient(135deg, rgba(212, 168, 83, 0.3), transparent); box-shadow: 0 0 30px rgba(212, 168, 83, 0.15); }
        .resource-card.notebook::after { background: linear-gradient(135deg, rgba(45, 189, 137, 0.3), transparent); box-shadow: 0 0 30px rgba(45, 189, 137, 0.15); }

        .resource-card:hover { z-index: 10; transform: translateY(-4px) scale(1.02); }

        .resource-icon {
            width: 48px; height: 48px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0; transition: transform 300ms ease;
            position: relative; transform: translateZ(30px);
        }
        .resource-card:hover .resource-icon { transform: translateZ(30px) scale(1.1) rotate(5deg); }

        .resource-card.rise .resource-icon { background: rgba(212, 168, 83, 0.1); color: var(--gold); border: 1px solid rgba(212, 168, 83, 0.3); box-shadow: 0 0 15px rgba(212, 168, 83, 0.15) inset; }
        .resource-card.notebook .resource-icon { background: rgba(45, 189, 137, 0.1); color: #2DBD89; border: 1px solid rgba(45, 189, 137, 0.3); box-shadow: 0 0 15px rgba(45, 189, 137, 0.15) inset; }
        
        .resource-icon svg { width: 24px; height: 24px; filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5)); }

        .resource-info { flex: 1; min-width: 0; transform: translateZ(30px); }
        .resource-name { font-size: 16px; font-weight: 700; color: white; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.3px; }
        .resource-meta { font-size: 12px; color: var(--text-muted); line-height: 1.5; display: flex; align-items: center; gap: 6px; }

        .resource-action {
            width: 36px; height: 36px; border-radius: 50%;
            background: rgba(255, 255, 255, 0.03); display: flex; align-items: center; justify-content: center;
            color: var(--text-muted); transition: all 400ms ease;
            opacity: 0; border: 1px solid rgba(255, 255, 255, 0.1);
            transform: translateZ(30px) translateX(-10px) scale(0.8);
        }
        .resource-card:hover .resource-action { opacity: 1; transform: translateZ(30px) translateX(0) scale(1); }
        .resource-card.rise:hover .resource-action { color: var(--gold); background: rgba(212, 168, 83, 0.15); border-color: rgba(212, 168, 83, 0.3); }
        .resource-card.notebook:hover .resource-action { color: #2DBD89; background: rgba(45, 189, 137, 0.15); border-color: rgba(45, 189, 137, 0.3); }

        /* Notebook Instructions */
        .notebook-instructions {
            background: rgba(45, 189, 137, 0.05);
            border: 1px dashed rgba(45, 189, 137, 0.2);
            border-radius: 12px;
            padding: 16px;
            margin-top: 16px;
        }
        .notebook-instructions h4 {
            color: #2DBD89;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .notebook-instructions ol {
            margin: 0;
            padding-left: 20px;
            color: var(--text-muted);
            font-size: 13px;
            line-height: 1.6;
        }
        .notebook-instructions li::marker {
            color: #2DBD89;
            font-weight: bold;
        }
"""
html = re.sub(r'/\* CURRICULUM TRACKS \(NETFLIX STYLE\) \*/.*?(?=@media \(max-width: 768px\))', css_replacement, html, flags=re.DOTALL)


# --- 2. HTML UPDATES ---
html_replacement = """        <!-- MARQUEE: CONTINUE LEARNING -->
        <div class="resource-section" style="margin-top: 24px;">
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
                <h2 style="font-size: 18px; font-weight: 800; text-transform: uppercase; letter-spacing: 2px; color: var(--gold); display: flex; align-items: center; gap: 12px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px;">
                        <polygon points="5 3 19 12 5 21 5 3"/>
                    </svg>
                    Up Next For You
                </h2>
                <div style="flex: 1; height: 1px; background: linear-gradient(90deg, rgba(212, 168, 83, 0.3), transparent);"></div>
            </div>
            
            <a href="shared/course-viewer.html?path=rise-modules/electricity-dc/fundamentals-of-direct-current&title=Direct Current Fundamentals" 
               class="resource-card rise" style="padding: 32px; gap: 32px;">
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

        <!-- CATEGORY ACCORDIONS AREA -->
        <div class="resource-section" id="accordionContainer">
            <!-- Populated by JS -->
        </div>"""

html = re.sub(r'<!-- MARQUEE: CONTINUE LEARNING -->.*?(?=</main>)', html_replacement + '\n    ', html, flags=re.DOTALL)


# --- 3. JS UPDATES ---
js_replacement = """        const CATEGORIES = [
            { id: 'MRD', name: 'Maintenance Regulations', desc: 'Aviation Regulations, Forms & Records' },
            { id: 'BET', name: 'Basic Electricity Tech', desc: 'DC, AC, Solid State, and Aircraft Electrical' },
            { id: 'CNS', name: 'Comm, Nav & Surveillance', desc: 'Radio Comm, Dependent Navigation, Surveillance' },
            { id: 'FI', name: 'Flight Instruments', desc: 'Pitot-Static and Primary Flight Instruments' },
            { id: 'DDS', name: 'Digital Data Systems', desc: 'Digital Electronics and Data Bus' },
            { id: 'AWH', name: 'Aircraft Wiring', desc: 'Building a Wire Harness' },
            { id: 'TTE', name: 'Tools & Test Equipment', desc: 'Basic Hand Tools & Hardware' },
            { id: 'SSP', name: 'Shop Safety', desc: 'Safety Essentials in Aviation' },
            { id: 'ALL', name: 'General CAET Prep', desc: 'Comprehensive Study Guides' }
        ];

        function toggleAccordion(element) {
            const accordion = element.closest('.category-accordion');
            accordion.classList.toggle('open');
        }

        function buildAccordionHtml() {
            let html = '';
            
            CATEGORIES.forEach(cat => {
                // Find modules and notebooks for this category
                const catModules = MODULES.filter(m => m.num === cat.id);
                const catNotebooks = NOTEBOOK_LINKS.filter(n => n.cat === cat.id);
                
                // Skip if category has no content
                if (catModules.length === 0 && catNotebooks.length === 0) return;
                
                const modulesHtml = catModules.map(m => `
                    <a href="${m.path}" class="resource-card rise">
                        <div class="card-cat-badge cat-${m.num.toLowerCase()}">${m.num}</div>
                        <div class="resource-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                        </div>
                        <div class="resource-info">
                            <div class="resource-name" title="${m.name}">${m.name}</div>
                            <div class="resource-meta">Rise 360 &bull; Interactive</div>
                        </div>
                        <div class="resource-action"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
                    </a>
                `).join('');

                const notebooksHtml = catNotebooks.map(n => `
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
                            <div class="resource-meta">Study Boss &bull; Ask AI</div>
                        </div>
                        <div class="resource-action"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg></div>
                    </a>
                `).join('');

                const instructionsHtml = catNotebooks.length > 0 ? `
                    <div class="notebook-instructions">
                        <h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg> How to use AI Guides</h4>
                        <ol>
                            <li>Download the official training PDF from Rise.</li>
                            <li>Upload it to the NotebookLM guide linked above.</li>
                            <li>Ask the AI to explain concepts, quiz you, or summarize chapters!</li>
                        </ol>
                    </div>
                ` : '';

                html += `
                <div class="category-accordion">
                    <div class="accordion-header" onclick="toggleAccordion(this)">
                        <div class="accordion-title-area">
                            <span class="card-cat-badge cat-${cat.id.toLowerCase()}" style="position:static; margin:0; transform:none;">${cat.id}</span>
                            <div>
                                <div class="accordion-title">${cat.name}</div>
                                <div class="accordion-subtitle">${cat.desc}</div>
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 16px;">
                            <div style="display:flex; gap: 8px;">
                                ${catModules.length > 0 ? `<span class="section-badge">${catModules.length} Modules</span>` : ''}
                                ${catNotebooks.length > 0 ? `<span class="section-badge green">${catNotebooks.length} AI Guides</span>` : ''}
                            </div>
                            <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
                        </div>
                    </div>
                    <div class="accordion-content">
                        <div class="content-split">
                            ${catModules.length > 0 ? `
                            <div class="content-column">
                                <h3>Interactive Training</h3>
                                <div class="items-grid">
                                    ${modulesHtml}
                                </div>
                            </div>
                            ` : '<div></div>'}
                            
                            ${catNotebooks.length > 0 ? `
                            <div class="content-column">
                                <h3>AI Study Guides</h3>
                                <div class="items-grid">
                                    ${notebooksHtml}
                                </div>
                                ${instructionsHtml}
                            </div>
                            ` : '<div></div>'}
                        </div>
                    </div>
                </div>
                `;
            });
            
            document.getElementById('accordionContainer').innerHTML = html;
        }

        // Initialize accordion layout
        buildAccordionHtml();
"""

html = re.sub(r'function scrollTrack\(id, amount\).*?document\.querySelector\(\'\.section-badge\.green\'\)\.textContent = `\$\{NOTEBOOK_LINKS\.length\} Notebooks`;', js_replacement, html, flags=re.DOTALL)

with open('classroom.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS refactored classroom.html to use Category Accordions")
