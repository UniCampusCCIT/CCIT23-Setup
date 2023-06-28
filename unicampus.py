from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DATABASE_FILE = 'flags.db'

def get_flag_stats():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM submitted_flags WHERE already_sent=1")
    sent_flags_count = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM submitted_flags WHERE already_sent=0")
    unsent_flags_count = c.fetchone()[0]

    conn.close()
    return sent_flags_count, unsent_flags_count

@app.route('/')
def index():
    sent_flags_count, unsent_flags_count = get_flag_stats()
    return render_template('./index.html', sent_flags_count=sent_flags_count, unsent_flags_count=unsent_flags_count)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
