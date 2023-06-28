import requests
import sqlite3
import time

TEAM_TOKEN = '9ea235c2089ff71e40192c3628ded1e6'
API_URL = 'http://10.10.0.1:8080/flags'
DATABASE_FILE = 'flags.db'
RATE_LIMIT = 15  # Maximum number of requests per minute

def create_database():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submitted_flags
                 (flag TEXT PRIMARY KEY, already_sent INTEGER)''')
    conn.commit()
    conn.close()

def check_flag_in_database(flag):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT flag FROM submitted_flags WHERE flag=?", (flag,))
    result = c.fetchone()
    conn.close()
    return result is not None

def add_flag_to_database(flag):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO submitted_flags VALUES (?, 0)", (flag,))
    conn.commit()
    conn.close()

def get_unsent_flags():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("SELECT flag FROM submitted_flags WHERE already_sent=0")
    unsent_flags = [row[0] for row in c.fetchall()]
    conn.close()
    return unsent_flags

def mark_flag_as_sent(flag):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute("UPDATE submitted_flags SET already_sent=1 WHERE flag=?", (flag,))
    conn.commit()
    conn.close()

def submit_flags(flags):
    num_flags = len(flags)
    batch_size = num_flags // 15  # Number of flags to send per batch

    if batch_size == 0:
        return

    for i in range(0, num_flags, batch_size):
        
        try:
            batch_flags = flags[i:i+batch_size]
        except:
            batch_flags = flags[i:]  # i+batch size exceeds array length

        if batch_flags == []:
            return

        response = requests.put(API_URL, headers={'X-Team-Token': TEAM_TOKEN}, json=batch_flags).json()

        try:
            for item in response:
                flag = item['flag']
                message = item['msg']
                status = item['status']
                print(f'[{flag}] {message}')

                if status or "old" in message:
                    mark_flag_as_sent(flag)
        except:
            pass

def main():
    create_database()
    
    while True:
        start_time = time.time()

        unsent_flags = get_unsent_flags()
        submit_flags(unsent_flags)
        
        end_time = time.time()
        delta = end_time - start_time

        try:
            time.sleep(60-delta)
        except:
            pass  # Minute already passed

if __name__ == '__main__':
    main()
