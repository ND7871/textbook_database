from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    try:
        conn = sqlite3.connect('test.db')  
        conn.row_factory = sqlite3.Row  
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None

@app.route('/search')
def search():
    query = request.args.get('query', '')

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT t_name, t_class FROM tbl_textbooks WHERE t_name LIKE ?", ('%' + query + '%',))
    textbooks = cursor.fetchall()
    conn.close()

    return jsonify([dict(textbook) for textbook in textbooks])

@app.route('/textbook')
def get_textbook():
    textbook_name = request.args.get('id', '')

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tbl_textbooks WHERE t_name = ?", (textbook_name,))
    textbook = cursor.fetchone()
    conn.close()
    
    if textbook:
        return jsonify(dict(textbook))
    return jsonify({"error": "Textbook not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
