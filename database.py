import sqlite3
from sqlite3 import Error


def create_connection(db_file,verbose=False):
    """ Δημιουργεί μια σύνδεση στη βάση δεδομένων SQLite """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        if verbose:
            print("Connection to database established.")
    except Error as e:
        print(e)

    return conn

def execute_query(conn, query, params=None, verbose=False):
    """ Εκτελεί ένα ερώτημα στη βάση δεδομένων
        INSERT/UPDATE/DELETE """
    try:
        c = conn.cursor() # Δημιουργία cursor
        if params:
            c.execute(query, params) # Εκτέλεση ερωτήματος με παραμέτρους
        else:
            c.execute(query) # Εκτέλεση ερωτήματος χωρίς παραμέτρους
        conn.commit() # Αποθήκευση αλλαγών
        if verbose:
            print("Query executed successfully.") # Επιτυχής εκτέλεση ερωτήματος
    except Error as e:
        print(e) # Εκτύπωση σφάλματος σε περίπτωση αποτυχίας εκτέλεσης ερωτήματος


def execute_read_query(conn, query, params=None, verbose=False):
    """ Εκτελεί ένα ερώτημα ανάγνωσης στη βάση δεδομένων
        SELECT """
    try:
        c = conn.cursor() # Δημιουργία cursor
        if params:
            c.execute(query, params) # Εκτέλεση ερωτήματος με παραμέτρους
        else:
            c.execute(query) # Εκτέλεση ερωτήματος χωρίς παραμέτρους
        result = c.fetchall() # Ανάκτηση όλων των αποτελεσμάτων
        columns = [description[0] for description in c.description] # Λήψη ονομάτων στηλών
        if verbose:
            print("Read query executed successfully.") # Επιτυχής εκτέλεση ερωτήματος ανάγνωσης
        return columns, result
    except Error as e:
        print(e) # Εκτύπωση σφάλματος σε περίπτωση αποτυχίας εκτέλεσης ερωτήματος
        return None, None
    

def create_highscores_table(db_file):
    conn = create_connection(db_file)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS highscores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL
    );
    """
    execute_query(conn, create_table_query)
    conn.close()

def add_highscore(db_file, player_name, score):
    conn = create_connection(db_file)
    insert_query = """
    INSERT INTO highscores (player_name, score)
    VALUES (?, ?);
    """
    execute_query(conn, insert_query, (player_name, score))
    conn.close()

def get_highscores(db_file, limit=10):
    conn = create_connection(db_file)
    select_query = """
    SELECT player_name, score
    FROM highscores
    ORDER BY score DESC
    LIMIT ?;
    """
    columns, results = execute_read_query(conn, select_query, (limit,))
    conn.close()
    return columns, results