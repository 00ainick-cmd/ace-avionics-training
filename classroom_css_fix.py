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
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            margin-bottom: 16px;
            overflow: hidden;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-card);
        }
        
        .category-accordion.open {
            border-color: var(--border-hover);
            box-shadow: var(--shadow-hover);
        }

        .accordion-header {
            padding: 24px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
            background: transparent;
            transition: background var(--transition);
        }

        .accordion-header:hover {
            background: var(--surface-hover);
        }

        .accordion-title-area {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .accordion-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
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
            color: var(--gold);
        }

        .accordion-content {
            display: none;
            padding: 0 32px 32px 32px;
            border-top: 1px solid var(--border);
            background: var(--bg);
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
            letter-spacing: 1.5px;
            color: var(--text-muted);
            margin-bottom: 16px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .content-column h3::after {
            content: '';
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, var(--border), transparent);
        }

        .items-grid {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        /* Adjust card styles for accordion layout */
        .resource-card {
            display: flex;
            width: 100%;
            position: relative;
            align-items: center;
            gap: 20px;
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 20px;
            text-decoration: none;
            color: inherit;
            transform-style: preserve-3d;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            z-index: 1;
            transition: all var(--transition-med);
        }
        
        .card-cat-badge {
            position: absolute;
            top: -10px;
            right: 20px;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1.5px;
            z-index: 20;
            background: var(--surface-3);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            transform: translateZ(20px);
            text-transform: uppercase;
        }

        /* Unified Brand Highlight */
        .resource-card:hover .card-cat-badge {
            color: var(--gold);
            border-color: rgba(212,168,83,0.3);
            background: var(--surface);
        }

        .resource-card::before {
            content: ''; position: absolute; inset: 0; border-radius: var(--radius-md);
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.01) 2px, rgba(255,255,255,0.01) 4px);
            pointer-events: none; mix-blend-mode: overlay; z-index: 2;
        }
        .resource-card::after {
            content: ''; position: absolute; inset: -1px;
            background: transparent;
            border-radius: 11px; z-index: -1; opacity: 0; transition: opacity 0.3s;
        }
        
        .resource-card:hover { z-index: 10; transform: translateY(-3px) scale(1.01); border-color: var(--border-hover); box-shadow: var(--shadow-hover); }
        .resource-card:hover::after { opacity: 1; }
        .resource-card.rise:hover::after { box-shadow: 0 0 20px var(--gold-glow); }
        .resource-card.notebook:hover::after { box-shadow: 0 0 20px var(--success-soft); }

        .resource-icon {
            width: 48px; height: 48px; border-radius: var(--radius-sm);
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0; transition: transform 300ms ease;
            position: relative; transform: translateZ(30px);
            background: var(--surface-3);
            border: 1px solid var(--border);
        }
        .resource-card:hover .resource-icon { transform: translateZ(30px) scale(1.08) rotate(3deg); border-color: var(--gold); color: var(--gold); }

        .resource-card.rise .resource-icon { color: var(--text-secondary); }
        .resource-card.notebook .resource-icon { color: var(--text-secondary); }
        
        .resource-icon svg { width: 22px; height: 22px; filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4)); }

        .resource-info { flex: 1; min-width: 0; transform: translateZ(30px); }
        .resource-name { font-size: 16px; font-weight: 700; color: var(--text-primary); margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -0.3px; }
        .resource-meta { font-size: 12px; color: var(--text-muted); line-height: 1.5; display: flex; align-items: center; gap: 6px; }

        .resource-action {
            width: 36px; height: 36px; border-radius: 50%;
            background: var(--surface-3); display: flex; align-items: center; justify-content: center;
            color: var(--text-muted); transition: all 300ms ease;
            opacity: 0; border: 1px solid var(--border);
            transform: translateZ(30px) translateX(-10px);
        }
        .resource-card:hover .resource-action { opacity: 1; transform: translateZ(30px) translateX(0); }
        .resource-card.rise:hover .resource-action { color: var(--gold); background: var(--gold-soft); border-color: var(--gold); }
        .resource-card.notebook:hover .resource-action { color: var(--success); background: var(--success-soft); border-color: var(--success); }

        /* Notebook Instructions */
        .notebook-instructions {
            background: var(--surface-3);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-top: 16px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
        }
        .notebook-instructions h4 {
            color: var(--success);
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
            font-weight: 800;
        }
        .notebook-instructions ol {
            margin: 0;
            padding-left: 20px;
            color: var(--text-secondary);
            font-size: 13px;
            line-height: 1.6;
        }
        .notebook-instructions li::marker {
            color: var(--success);
            font-weight: bold;
        }
"""
html = re.sub(r'/\* CATEGORY ACCORDIONS \*/.*?(?=@media \(max-width: 768px\))', css_replacement, html, flags=re.DOTALL)

with open('classroom.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS refactored classroom CSS")
