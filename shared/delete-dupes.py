import os
import glob

root_dir = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main"
jeopardy_files = glob.glob(os.path.join(root_dir, "**", "jeopardy.html"), recursive=True)

deleted = 0
for f in jeopardy_files:
    # Do NOT delete the new shared one
    if os.path.normpath(f) == os.path.normpath(os.path.join(root_dir, "shared", "jeopardy.html")):
        continue
    
    os.remove(f)
    print("Deleted: " + f)
    deleted += 1

print(f"Deleted {deleted} duplicate jeopardy.html files.")
