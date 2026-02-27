import os
import glob
import re

root_dir = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main"
index_files = glob.glob(os.path.join(root_dir, "**", "index.html"), recursive=True)

new_launch = """  /* ── Launch activity ── */
  function launchActivity(key, label) {
    let path = CAT_CONFIG.activities[key];
    if (!path) return;
    lsSet(`ace_cat_${CAT_CONFIG.id}_${key}_progress`, true);
    
    if (key === 'jeopardy' || key === 'practice') {
      const themeLink = document.querySelector('link[href*="shared/ace-theme.css"]');
      const sharedPrefix = themeLink ? themeLink.getAttribute('href').replace('ace-theme.css', '') : '../../../shared/';
      const absoluteDataUrl = new URL('data/questions.json', window.location.href).href;
      
      const targetHtml = key === 'jeopardy' ? 'jeopardy.html' : 'drill.html';
      
      path = sharedPrefix + targetHtml + '?cat=' + encodeURIComponent(CAT_CONFIG.id) + 
             '&title=' + encodeURIComponent(CAT_CONFIG.num + ': ' + CAT_CONFIG.title) + 
             '&color=' + encodeURIComponent(CAT_CONFIG.color) + 
             '&data=' + encodeURIComponent(absoluteDataUrl) +
             '&back=' + encodeURIComponent(window.location.href);
    }
    
    window.location.href = path;
  }"""

modified_count = 0
for filepath in index_files:
    if os.path.dirname(filepath) == root_dir:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'/\*\s*── Launch activity ──\s*\*/\s*function launchActivity\(key, label\) \{.*?\n  \}', content, re.DOTALL)
    if match:
        content = content[:match.start()] + new_launch + content[match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1
        print(f"Updated: {filepath}")

print(f"Modified {modified_count} index.html files.")
