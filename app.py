from flask import Flask, request, render_template, redirect, url_for
import sqlite3, os

app = Flask(__name__, static_folder='static', template_folder='templates')
DB = os.path.join(os.path.dirname(__file__), 'wiki.db')

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        conn.execute('CREATE TABLE pages (title TEXT PRIMARY KEY, content TEXT)')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    pages = [r[0] for r in conn.execute('SELECT title FROM pages ORDER BY title').fetchall()]
    conn.close()
    return render_template('index.html', pages=pages)

@app.route('/<title>')
def view(title):
    conn = sqlite3.connect(DB)
    row = conn.execute('SELECT content FROM pages WHERE title=?', (title,)).fetchone()
    conn.close()
    if row:
        return render_template('view.html', title=title, content=row[0])
    return redirect(url_for('edit', title=title))

@app.route('/edit/<title>', methods=['GET', 'POST'])
def edit(title):
    if request.method == 'POST':
        content = request.form.get('content','')
        conn = sqlite3.connect(DB)
        conn.execute('REPLACE INTO pages (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('view', title=title))
    else:
        conn = sqlite3.connect(DB)
        row = conn.execute('SELECT content FROM pages WHERE title=?', (title,)).fetchone()
        conn.close()
        content = row[0] if row else ''
        return render_template('edit.html', title=title, content=content)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
