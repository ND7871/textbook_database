from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/textbooks', methods=['POST'])
def add_textbook():
    data = request.get_json()
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO tbl_textbooks(t_name, t_class, t_professor, t_ebook, t_required, t_link)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        textbook_data = (data['t_name'], data['t_class'], data['t_professor'], data['t_ebook'], data['t_required'], data['t_link'])
        cursor.execute(insert_sql, textbook_data)
        conn.commit()
        return jsonify({'message': 'Textbook added successfully'}), 201
    except sqlite3.Error as error:
        return jsonify({'error': str(error)}), 400
    finally:
        if conn:
            conn.close()

@app.route('/search', methods=['GET'])
def search_textbooks():
    query = request.args.get('query')
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_textbooks WHERE t_name LIKE ?", ('%' + query + '%',))
        search_results = cursor.fetchall()
        return jsonify(search_results)
    except sqlite3.Error as error:
        return jsonify({'error': str(error)}), 400
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)
        
