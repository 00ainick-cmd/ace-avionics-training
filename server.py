import http.server
import socketserver
import sqlite3
import json
import os
import urllib.parse
import mimetypes
import random

PORT = 8000
DB_FILE = 'caet_students.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Students table
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            background TEXT,
            branch TEXT,
            mos TEXT,
            employer TEXT,
            experience TEXT,
            certs TEXT,
            date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Category Scores table
    c.execute('''
        CREATE TABLE IF NOT EXISTS diagnostic_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            category TEXT,
            score_percent INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        )
    ''')
    
    # Enable cascaded deletes
    c.execute('PRAGMA foreign_keys = ON;')
    
    conn.commit()
    conn.close()
    print("Database initialized.")


class CAETRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def end_headers(self):
        # Add CORS and no-cache headers for API routes
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API Route: Get all students for admin dashboard
        if parsed_path.path == '/api/students':
            try:
                conn = sqlite3.connect(DB_FILE)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                
                # Fetch students
                c.execute('SELECT * FROM students ORDER BY date_joined DESC')
                students = [dict(row) for row in c.fetchall()]
                
                # Fetch and attach scores
                for student in students:
                    c.execute('SELECT category, score_percent FROM diagnostic_scores WHERE student_id = ?', (student['id'],))
                    student['scores'] = [dict(row) for row in c.fetchall()]
                
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(students).encode('utf-8'))
                return
                
            except Exception as e:
                print(f"Error fetching students: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        # Fallback to serving static files (SimpleHTTPRequestHandler behavior)
        super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API Route: Onboard new student
        if parsed_path.path == '/api/students':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Empty payload"}')
                return

            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                data = json.loads(post_data)
                
                profile = data.get('profile', {})
                scores = data.get('scores', [])
                
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                
                # Insert Student
                c.execute('''
                    INSERT INTO students (name, background, branch, mos, employer, experience, certs)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    profile.get('name'),
                    profile.get('background'),
                    profile.get('branch'),
                    profile.get('mos'),
                    profile.get('employer'),
                    profile.get('experience'),
                    json.dumps(profile.get('certs', [])) # Store array as JSON string
                ))
                
                student_id = c.lastrowid
                
                # Insert Scores
                for score in scores:
                    c.execute('''
                        INSERT INTO diagnostic_scores (student_id, category, score_percent)
                        VALUES (?, ?, ?)
                    ''', (
                        student_id,
                        score.get('category'),
                        score.get('score_percent')
                    ))
                
                conn.commit()
                conn.close()
                
                self.send_response(201)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "student_id": student_id}).encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
            except Exception as e:
                print(f"Error saving student: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        # API Route: Seed dummy students for testing
        if parsed_path.path == '/api/students/seed':
            content_length = int(self.headers.get('Content-Length', 0))
            count = 5
            if content_length > 0:
                try:
                    body = json.loads(self.rfile.read(content_length).decode('utf-8'))
                    count = int(body.get('count', 5))
                except: pass

            FIRST_NAMES = ['Alex', 'Jordan', 'Casey', 'Taylor', 'Morgan', 'Riley', 'Avery', 'Jamie', 'Drew', 'Skyler', 'Marcus', 'Elena', 'Devon', 'Reese', 'Quinn', 'Dakota', 'Kendall', 'Blake', 'Tatum', 'Rowan']
            LAST_NAMES = ['Johnson', 'Williams', 'Chen', 'Garcia', 'Kim', 'Patel', 'Nguyen', 'Martinez', 'Brown', 'Okafor', 'Schmidt', 'Takahashi', 'Davis', 'Wilson', 'Lopez', 'Anderson', 'Thomas', 'Jackson', 'White', 'Harris']
            BACKGROUNDS = ['military', 'military', 'part147', 'technician', 'other']
            BRANCHES = ['Air Force', 'Army', 'Navy', 'Marines', 'Coast Guard']
            MOS_CODES = {
                'Air Force': ['2A373', '2A571', '2A090', '2A353'],
                'Army': ['94D', '94E', '94H', '94R'],
                'Navy': ['AT', 'AE', 'AO', 'ET'],
                'Marines': ['6323', '6324', '6326', '6317'],
                'Coast Guard': ['AET', 'ET', 'AVI', 'MST']
            }
            EMPLOYERS = ['Delta Air Lines', 'United Airlines', 'Boeing', 'Lockheed Martin', 'L3Harris', 'Northrop Grumman', 'Raytheon', 'Spirit AeroSystems', 'Textron Aviation', 'StandardAero', 'AAR Corp', 'ST Engineering', 'Honeywell Aerospace', 'Collins Aerospace', 'GE Aviation']
            EXP_LEVELS = ['0-2', '3-5', '5-10', '10+']
            CERT_OPTIONS = ['A&P', 'NCATT', 'FCC GROL']
            CATEGORIES = ['cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7', 'cat8']

            created_ids = []
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            for _ in range(count):
                first = random.choice(FIRST_NAMES)
                last = random.choice(LAST_NAMES)
                name = f'{first} {last}'
                bg = random.choice(BACKGROUNDS)
                branch = ''
                mos = ''
                if bg == 'military':
                    branch = random.choice(BRANCHES)
                    mos = random.choice(MOS_CODES[branch])
                employer = random.choice(EMPLOYERS)
                exp = random.choice(EXP_LEVELS)
                num_certs = random.randint(0, 3)
                certs = json.dumps(random.sample(CERT_OPTIONS, min(num_certs, len(CERT_OPTIONS))))

                c.execute('INSERT INTO students (name, background, branch, mos, employer, experience, certs) VALUES (?,?,?,?,?,?,?)',
                    (name, bg, branch, mos, employer, exp, certs))
                sid = c.lastrowid
                created_ids.append(sid)

                for cat in CATEGORIES:
                    base = random.randint(20, 100)
                    if bg == 'military' and cat in ['cat1', 'cat3', 'cat5']:
                        base = min(100, base + random.randint(5, 20))
                    c.execute('INSERT INTO diagnostic_scores (student_id, category, score_percent) VALUES (?,?,?)',
                        (sid, cat, base))

            conn.commit()
            conn.close()

            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'created': len(created_ids), 'ids': created_ids}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API Route: Purge ALL students
        if parsed_path.path == '/api/students/all':
            try:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute('DELETE FROM diagnostic_scores')
                c.execute('DELETE FROM students')
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': 'All student data purged'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        # API Route: Delete Single Student
        if parsed_path.path.startswith('/api/students/'):
            try:
                student_id = int(parsed_path.path.split('/')[-1])
                
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                # PRAGMA foreign_keys = ON must be set per connection for CASCADE delete to work
                c.execute('PRAGMA foreign_keys = ON;') 
                
                c.execute('DELETE FROM students WHERE id = ?', (student_id,))
                deleted = c.rowcount > 0
                
                conn.commit()
                conn.close()
                
                if deleted:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Student not found"}).encode('utf-8'))
                    
            except ValueError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid ID format"}')
            except Exception as e:
                print(f"Error deleting student: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    init_db()
    
    # Change into the directory where the script is located to serve files correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CAETRequestHandler) as httpd:
        print(f"CAET Local Server running at http://localhost:{PORT}")
        print(f"Database: {DB_FILE}")
        print("Serving files and API... Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()
