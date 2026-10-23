import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import check_password_hash
from database import get_connection, init_db

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# secure secret key loaded from environment variable
app.secret_key = os.getenv('SECRET_KEY', 'cybernews_dev_fallback_key')

# session cookie security configuration
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# ensure database exists
init_db()

@app.route('/')
def index():
    # main news dashboard displaying featured and regular articles
    conn = get_connection()
    category = request.args.get('category')
    search_query = request.args.get('search')

    query = 'SELECT * FROM articles WHERE 1=1'
    params = []

    if category:
        query += ' AND category = ?'
        params.append(category)

    if search_query:
        query += ' AND (title LIKE ? OR summary LIKE ?)'
        wildcard = f'%{search_query}%'
        params.extend([wildcard, wildcard])

    query += ' ORDER BY created_at DESC'
    articles = conn.execute(query, params).fetchall()

    featured = conn.execute(
        'SELECT * FROM articles WHERE is_featured = 1 ORDER BY created_at DESC LIMIT 1'
    ).fetchone()

    conn.close()
    return render_template('index.html', articles=articles, featured=featured, selected_category=category)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    # individual article detail page
    conn = get_connection()
    article = conn.execute('SELECT * FROM articles WHERE id = ?', (article_id,)).fetchone()
    conn.close()

    if article is None:
        abort(404)

    return render_template('article.html', article=article)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # authentication handler for administrative access
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('admin'))
        else:
            error = 'Invalid credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # clear session data
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # administrative interface restricted to admin role
    if 'role' not in session or session['role'] != 'admin':
        abort(403)

    conn = get_connection()

    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        source = request.form.get('source')
        summary = request.form.get('summary')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        is_featured = 1 if request.form.get('is_featured') else 0

        conn.execute('''
            INSERT INTO articles (title, category, source, summary, content, image_url, is_featured)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, category, source, summary, content, image_url, is_featured))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    articles = conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('admin.html', articles=articles)

@app.route('/admin/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    # route to delete articles
    if 'role' not in session or session['role'] != 'admin':
        abort(403)

    conn = get_connection()
    conn.execute('DELETE FROM articles WHERE id = ?', (article_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)