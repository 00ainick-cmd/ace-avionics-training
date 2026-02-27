import os
import glob
import re

root_dir = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main"
index_files = glob.glob(os.path.join(root_dir, "**", "index.html"), recursive=True)

old_launch = """  /* ── Launch activity ── */
  function launchActivity(key, label) {
    const path = CAT_CONFIG.activities[key];
    if (!path) return;
    lsSet(`ace_cat_${CAT_CONFIG.id}_${key}_progress`, true);
    window.location.href = path;
  }"""

new_launch = """  /* ── Launch activity ── */
  function launchActivity(key, label) {
    let path = CAT_CONFIG.activities[key];
    if (!path) return;
    lsSet(`ace_cat_${CAT_CONFIG.id}_${key}_progress`, true);
    
    if (key === 'jeopardy') {
      const themeLink = document.querySelector('link[href*="shared/ace-theme.css"]');
      const sharedPrefix = themeLink ? themeLink.getAttribute('href').replace('ace-theme.css', '') : '../../../shared/';
      path = sharedPrefix + 'jeopardy.html?cat=' + encodeURIComponent(CAT_CONFIG.id) + 
             '&title=' + encodeURIComponent(CAT_CONFIG.num + ': ' + CAT_CONFIG.title) + 
             '&color=' + encodeURIComponent(CAT_CONFIG.color) + 
             '&data=data/questions.json' +
             '&back=' + encodeURIComponent(window.location.href);
    }
    
    window.location.href = path;
  }"""

modified_count = 0
for filepath in index_files:
    # Skip root dashboard index.html
    if os.path.dirname(filepath) == root_dir:
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "function launchActivity(key, label) {" in content and "window.location.href = path;" in content:
        # Regex replace is safer if whitespace slightly varies but a direct replace should work if exact
        if old_launch in content:
            content = content.replace(old_launch, new_launch)
        else:
            # Fallback regex replace for whitespace differences
            pattern = re.compile(r'/\*\s*── Launch activity ──\s*\*/\s*function launchActivity\(key, label\) \{.*\}', re.DOTALL)
            content = pattern.sub(new_launch, content)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_count += 1
        print(f"Updated: {filepath}")

print(f"Modified {modified_count} index.html files.")
