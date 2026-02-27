import os

filepath = 'c:\\Users\\nickb\\Downloads\\ace-avionics-training-main\\ace-avionics-training-main\\shared\\jeopardy.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace paths
content = content.replace('../../../../shared/', '')
content = content.replace('../../../shared/', '')
content = content.replace('../../../../dashboard.html', '../dashboard.html')

# Add badge ID
content = content.replace('<div class="badge">Battle Against Ace</div>', '<div class="badge" id="gameTitleBadge">Battle Against Ace</div>')

# Replace the data load section
old_load = """    const _jParams = new URLSearchParams(location.search);
    const _backUrl = _jParams.get('back') || '../../../../dashboard.html';
    const fetchUrl = _jParams.get('data') || 'data/questions.json';"""

new_load = """    const _jParams = new URLSearchParams(location.search);
    const _backUrl = _jParams.get('back') || '../dashboard.html';
    const fetchUrl = _jParams.get('data') || 'data/questions.json';
    const _catParam = _jParams.get('cat') || 'jeopardy';
    const _titleParam = _jParams.get('title');
    const _colorParam = _jParams.get('color');

    if (_colorParam) { document.documentElement.style.setProperty('--gold', _colorParam); document.documentElement.style.setProperty('--player', _colorParam); }
    if (_titleParam) {
      document.title = _titleParam + " | ACE CAET Prep";
      const badge = document.getElementById('gameTitleBadge');
      if (badge) badge.textContent = _titleParam;
    }"""
content = content.replace(old_load, new_load)

# Replace the gamification tracker category references
# Instead of hardcoded 'jeopardy', we will use _catParam if available (as global),
# but wait, the moduleName inside reportModuleCompletion('jeopardy', ...) is at the bottom, and _catParam is inside the load function async scope.
# We need to make _catParam available globally or inject it similarly.
