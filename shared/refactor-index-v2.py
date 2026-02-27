import os
import glob
import re

root_dir = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main"
index_files = glob.glob(os.path.join(root_dir, "**", "index.html"), recursive=True)

old_launch_pattern = re.compile(r'/\*\s*── Launch activity ──\s*\*/\s*function launchActivity\(key, label\) \{.*\}', re.DOTALL)

new_launch = """  /* ── Launch activity ── */
  function launchActivity(key, label) {
    let path = CAT_CONFIG.activities[key];
    if (!path) return;
    lsSet(`ace_cat_${CAT_CONFIG.id}_${key}_progress`, true);
    
    if (key === 'jeopardy') {
      const themeLink = document.querySelector('link[href*="shared/ace-theme.css"]');
      const sharedPrefix = themeLink ? themeLink.getAttribute('href').replace('ace-theme.css', '') : '../../../shared/';
      const absoluteDataUrl = new URL('data/questions.json', window.location.href).href;
      
      path = sharedPrefix + 'jeopardy.html?cat=' + encodeURIComponent(CAT_CONFIG.id) + 
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

    # Find where the old launchActivity starts and ends.
    # Because we already replaced it once, we should match the current new_launch and replace it again!
    start_idx = content.find("/* ── Launch activity ── */")
    if start_idx != -1:
        end_idx = content.find("/* ── Training modules ── */")
        if end_idx == -1: # Some might have different trailing sections
            # fallback: find next function or simply replace using regex
            match = re.search(r'/\*\s*── Launch activity ──\s*\*/\s*function launchActivity\(key, label\) \{.*?\n  \}', content, re.DOTALL)
            if match:
                content = content[:match.start()] + new_launch + content[match.end():]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")
        else:
            # Safer to use regex to find the whole function body
            match = re.search(r'/\*\s*── Launch activity ──\s*\*/\s*function launchActivity\(key, label\) \{.*?\n  \}', content, re.DOTALL)
            if match:
                content = content[:match.start()] + new_launch + content[match.end():]
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_count += 1
                print(f"Updated: {filepath}")

print(f"Modified {modified_count} index.html files.")
