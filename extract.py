import os
import glob
import zipfile
import re

base_dir = r"c:\Users\nickb\Downloads\ace-avionics-training-main\ace-avionics-training-main\rise-modules"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.zip'):
            zip_path = os.path.join(root, file)
            # e.g. dependent-navigation-systems-raw-1JxemDvW.zip
            m = re.match(r"(.*?)-raw-[^\.]+", file)
            if m:
                folder_name = m.group(1)
            else:
                folder_name = file.replace('.zip', '')
            
            extract_path = os.path.join(root, folder_name)
            if not os.path.exists(extract_path):
                os.makedirs(extract_path)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"Extracted {file} to {extract_path}")

