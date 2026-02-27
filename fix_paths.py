import os
import glob
import shutil

files = glob.glob('training_modules/*.html')
fixed_count = 0

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Only rewrite if there is actual content
        if content.strip():
            # Fix supabase path
            content = content.replace('../../../shared/js/supabase-client.js', '../shared/js/supabase-client.js')
            
            # Fix index.html return link to dashboard
            content = content.replace('href="index.html"', 'href="../dashboard.html"')
            content = content.replace("href='index.html'", "href='../dashboard.html'")
            
            # Write to temp file first to avoid truncation
            temp_file = f + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write(content)
                
            shutil.move(temp_file, f)
            fixed_count += 1
            
    except Exception as e:
        print(f"Error processing {f}: {e}")

print(f"Fixed {fixed_count} files safely.")
