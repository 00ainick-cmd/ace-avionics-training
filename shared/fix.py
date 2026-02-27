import os
import glob

base_dir = r'c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\question-banks\modules\caet-entry\shared\training'
for f in glob.glob(os.path.join(base_dir, '*-rise.html')):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # The erroneous duplicate text that got left behind
    bad_text = """    </div>
            <div class="keyboard-hint">Press <kbd>ESC</kbd> to exit</div>
        </div>
    </div>

    <div class="loading-overlay" id="loadingOverlay">"""
    
    good_text = """    </div>

    <div class="loading-overlay" id="loadingOverlay">"""
    
    content = content.replace(bad_text, good_text)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print('Fixed!')
