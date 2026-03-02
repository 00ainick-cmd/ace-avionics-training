import os
import re

with open('classroom.html', 'r', encoding='utf-8') as f:
    html = f.read()

notebook_links_code = """        const NOTEBOOK_LINKS = [
            { cat: 'ALL', name: 'CAET Study Boss (Comprehensive)', url: 'https://notebooklm.google.com/notebook/5bdd750c-8b81-4a09-9ec5-daf7e685f600' },
            { cat: 'MRD', name: 'Regulations, Forms & Records', url: 'https://notebooklm.google.com/notebook/4ec730e9-f975-4645-8224-381cd7cb1261' },
            { cat: 'BET', name: 'Fundamentals of Electricity', url: 'https://notebooklm.google.com/notebook/64f77e37-194f-48bf-b2f3-de3558ba1b62' },
            { cat: 'BET', name: 'Direct Current', url: 'https://notebooklm.google.com/notebook/0d8bdfcc-eef6-4dca-87c2-c71894115a80' },
            { cat: 'BET', name: 'Alternating Current', url: 'https://notebooklm.google.com/notebook/2f53925c-3def-467e-909d-9493da687371' },
            { cat: 'BET', name: 'Solid State Devices', url: 'https://notebooklm.google.com/notebook/7e9fde9e-eb66-45e2-82f7-9b081929864b' },
            { cat: 'BET', name: 'Aircraft Electrical', url: 'https://notebooklm.google.com/notebook/dad78107-8b8c-4121-a152-bec2492dbfc2' },
            { cat: 'CNS', name: 'CNS Systems', url: 'https://notebooklm.google.com/notebook/e5f4f1aa-0a29-497b-8a88-1d2ef0175387' },
            { cat: 'FI', name: 'Pitot-Static Systems', url: 'https://notebooklm.google.com/notebook/8073baef-d9cf-4153-8e35-90279a8e1b2b' },
            { cat: 'DDS', name: 'Digital Electronics', url: 'https://notebooklm.google.com/notebook/64bf4b91-6dbe-437b-873d-9e6673d94f60' },
            { cat: 'DDS', name: 'Digital Data Bus Systems', url: 'https://notebooklm.google.com/notebook/033c0b10-c82c-4d2c-b2bb-f23bb22d4491' },
            { cat: 'AWH', name: 'Aircraft Wiring', url: 'https://notebooklm.google.com/notebook/37abaeae-80fe-47cd-a6b3-dae7cebb69dd' },
            { cat: 'TTE', name: 'Aircraft Handtools & Hardware', url: 'https://notebooklm.google.com/notebook/dbcb4510-acc0-4cec-87e6-45ac538d6327' },
            { cat: 'SSP', name: 'Aviation Safety', url: 'https://notebooklm.google.com/notebook/73ca69b8-23b9-44fe-b18d-cf5b83810be2' }
        ];"""

html = re.sub(r'(const CATEGORIES = \[)', notebook_links_code + r'\n\n        \1', html)

with open('classroom.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("SUCCESS restored NOTEBOOK_LINKS")
