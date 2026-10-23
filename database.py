import sqlite3
from werkzeug.security import generate_password_hash

# database configuration
db_name = 'cybernews.db'

def get_connection():
    # returns an active sqlite3 connection
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # creates tables and populates initial demo data
    conn = get_connection()
    cursor = conn.cursor()

    # create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        )
    ''')

    # create articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            image_url TEXT NOT NULL,
            is_featured INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # insert default admin user (admin / admin123)
    admin_password = generate_password_hash('admin123')
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username, password, role)
        VALUES (1, 'admin', ?, 'admin')
    ''', (admin_password,))

    # insert sample articles reflecting standard news feeds
    sample_articles = [
        (
            'ThreatsDay Bulletin: Stealth Loaders, AI Chatbot Flaws, and Docker Hack',
            'Cyber Attacks',
            'The Hacker News',
            'Attackers are increasingly blending in, hijacking everyday tools and trusted apps.',
            'Detailed analysis on modern evasion techniques and living-off-the-land attacks...',
            'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=800&q=80',
            1
        ),
        (
            'The Breach You Did Not Expect: Your AppSec Stack',
            'AppSec',
            'SecurityWeek',
            'In a market undergoing rapid shifts, vendor instability poses real security risks.',
            'Comprehensive review of software supply chain security and third-party risk management...',
            'https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&q=80',
            0
        ),
        (
            'Pro-Russian Hackers Claim Cyberattack on French Postal Service',
            'Data Breaches',
            'SecurityWeek',
            'Central computer systems at La Poste knocked offline by coordinated DDoS campaigns.',
            'Technical post-mortem examining the volume and mitigation steps taken during the incident...',
            'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=800&q=80',
            0
        )
    ]

    cursor.executemany('''
        INSERT OR IGNORE INTO articles (id, title, category, source, summary, content, image_url, is_featured)
        VALUES (null, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_articles)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    # run initialization directly
    init_db()
    print('Database initialized successfully.')