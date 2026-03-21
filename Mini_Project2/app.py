from flask import Flask, render_template, request
import mysql.connector 
import config

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

# 🔹 Initialize DB (creates table if not exists)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/submit', methods=['POST'])
def submit_feedback():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Connect DB
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert data
        query = "INSERT INTO feedback (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, message))

        conn.commit()

        cursor.close()
        conn.close()

        return "Feedback stored successfully"

    except Exception as e:
        return f"Error: {e}"


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/add', methods=['GET','POST'])
def add_feedback():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')

        return f"Feedback submitted by {name} with message {message}"

    return render_template('add_feedback.html')


@app.route('/test-env')
def test_env():
    return f"{config.DB_HOST}, {config.DB_USER}"

if __name__ == "__main__":
   init_db()
   app.run(port=5000, debug=config.DEBUG)
