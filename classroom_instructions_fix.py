import re

with open('classroom.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update NotebookLM instructions text
old_instructions = r"""                const instructionsHtml = catNotebooks\.length > 0 \? `
                    <div class="notebook-instructions">
                        <h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h\.01"/></svg> How to use AI Guides</h4>
                        <ol>
                            <li>Download the official training PDF from Rise\.</li>
                            <li>Upload it to the NotebookLM guide linked above\.</li>
                            <li>Ask the AI to explain concepts, quiz you, or summarize chapters!</li>
                        </ol>
                    </div>
                ` : '';"""

new_instructions = """                const instructionsHtml = catNotebooks.length > 0 ? `
                    <div class="notebook-instructions">
                        <h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg> AI Study Boss</h4>
                        <p style="color: var(--text-secondary); font-size: 13px; line-height: 1.6; margin: 4px 0 0 0;">
                            These dedicated Study Guides are pre-loaded with the official CAET documentation. Use them to safely interact with the coursework—ask it to explain complex concepts, generate practice quizzes, or summarize chapters, all without the risk of AI hallucination.
                        </p>
                    </div>
                ` : '';"""

html = re.sub(old_instructions, new_instructions, html)

with open('classroom.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS updated AI notebook instructions")
