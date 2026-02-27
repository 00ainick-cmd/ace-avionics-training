import os
import glob
import re

base_dir = r'c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\question-banks\modules\caet-entry\shared\training'

for f in glob.glob(os.path.join(base_dir, '*-rise.html')):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    bad_js = """        function goBack() {
            saveSessionData();
            if (studyTimerInterval) clearInterval(studyTimerInterval);
            if (pomodoroInterval) clearInterval(pomodoroInterval);
            if (isEmbedded) { window.parent.postMessage({ type: 'ACE_CLOSE' }, '*'); }
            else { window.history.back(); }
        }
    </script>"""
    
    # We need to find the actual bad string. The previous script replacement went wrong because it was trying to match:
    # function goBack\(\) \{.*?\}  (non-greedy)
    # The original goBack in maintenance-regs was:
    '''
    function goBack() {
        saveSessionData();
        if (studyTimerInterval) clearInterval(studyTimerInterval);
        if (pomodoroInterval) clearInterval(pomodoroInterval);
        if (isEmbedded) { window.parent.postMessage({ type: 'ACE_CLOSE' }, '*'); }
        else { window.location.href = '../../../../../dashboard.html'; }
    }
    '''
    # The subagent reported:
    '''
    else { window.history.back(); }
    }, '*'); } // <--- Syntax error here
    else { window.location.href = '../../../../../dashboard.html'; }
    '''
    
    pattern = r"function goBack\(\) \{[\s\S]*?else \{ window\.history\.back\(\); \}\n        \}([\s\S]*?else \{ window\.location\.href.*?;\s*\})"
    
    # Let's just cleanly rip out everything from 'function goBack()' to the end of the script tag and replace it properly.
    clean_js = """        function goBack() {
            saveSessionData();
            if (studyTimerInterval) clearInterval(studyTimerInterval);
            if (pomodoroInterval) clearInterval(pomodoroInterval);
            if (isEmbedded) { window.parent.postMessage({ type: 'ACE_CLOSE' }, '*'); }
            else { window.history.back(); }
        }
    </script>"""

    content = re.sub(r"function goBack\(\) \{[\s\S]*?</script>", clean_js, content)

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print('Fixed JS Syntax Error!')
