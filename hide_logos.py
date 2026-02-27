import os
import glob

base = r'c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\rise-modules'
htmls = glob.glob(os.path.join(base, '**', 'index.html'), recursive=True)
css = "<style> .brand, .brand--ui, .brand__logo, .nav-sidebar__logo-wrapper, .page__header-logo, .cover__logo, .theme-logo, img[src*='logo'], img[alt*='logo'] { display: none !important; } </style>"

for path in htmls:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        if css not in c and '</head>' in c:
            c = c.replace('</head>', f'    {css}\n</head>')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(c)
            print("Patched:", path)
    except Exception as e:
        print(e)
print("Done!")
