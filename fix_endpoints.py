import glob
import shutil

files = glob.glob('training_modules/*.html')
fixed_count = 0

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        modified = False
        if "window.location.href = 'index.html';" in content:
            content = content.replace("window.location.href = 'index.html';", "window.location.href = '../dashboard.html';")
            modified = True
            
        if modified:
            temp_file = f + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write(content)
            shutil.move(temp_file, f)
            fixed_count += 1

    except Exception as e:
        print(f"Error processing {f}: {e}")

print(f"Fixed {fixed_count} endpoint links.")
