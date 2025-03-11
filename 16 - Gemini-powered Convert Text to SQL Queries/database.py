import sqlite3  # Import SQLite library for database operations

# Function to create the STUDENT table if it doesn't exist
def create_student_table():
    conn = sqlite3.connect("student.db")  # Connect to SQLite database (creates file if not exists)
    cur = conn.cursor()  # Create a cursor object to execute SQL queries

    # SQL query to create the STUDENT table with columns: NAME, CLASS, SECTION, SCORE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS STUDENT (
            NAME TEXT,
            CLASS TEXT,
            SECTION TEXT,
            SCORE INTEGER
        )
    ''')
    conn.commit()  # Commit changes
    conn.close()   # Close database connection

# Function to insert sample data (only if the table is empty)
def insert_sample_data():
    conn = sqlite3.connect("student.db")
    cur = conn.cursor()

    # Check if the table already has data
    cur.execute("SELECT COUNT(*) FROM STUDENT")
    if cur.fetchone()[0] == 0:  # If table is empty, insert sample data
        cur.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", [
            ('Rahman', 'Data Science', 'A', 95),
            ('Hasan', 'Data Science', 'B', 88),
            ('Fahim', 'Data Science', 'A', 92),
            ('Tariq', 'DEVOPS', 'A', 76),
            ('Imran', 'DEVOPS', 'A', 60),
            ('Naeem', 'AI & ML', 'B', 85),
            ('Samiul', 'AI & ML', 'A', 90),
            ('Rafiq', 'Cyber Security', 'B', 70),
            ('Shakib', 'Web Development', 'A', 80),
            ('Muntasir', 'Cloud Computing', 'A', 65),
        ])
        conn.commit()  # Commit changes

    conn.close()  # Close database connection

# Function to execute SQL queries on the database
def read_sql_query(sql_query, db="student.db"):
    try:
        conn = sqlite3.connect(db)  # Connect to the database
        cur = conn.cursor()  # Create a cursor object

        cur.execute(sql_query)  # Execute the SQL query
        rows = cur.fetchall()  # Fetch all results
        conn.close()  # Close connection

        return rows  # Return query result
    except sqlite3.Error as e:
        return [("Error:", str(e))]  # Return error message in case of failure

# Initialize database (Create table and insert data)
create_student_table()
insert_sample_data()