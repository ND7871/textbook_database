from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import uuid
from datetime import datetime, timedelta
import os
import hashlib

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect("textbook_database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/textbooks', methods=['POST'])
def add_textbook():
    data = request.get_json()
    try:
        conn = sqlite3.connect('textbook_database.db')
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
    query = request.args.get('query', '').strip()
    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT t_name, t_class FROM tbl_textbooks WHERE t_name LIKE ? COLLATE NOCASE", ('%' + query + '%',))
        search_results = [{"t_name": row[0], "t_class": row[1]} for row in cursor.fetchall()]

        return jsonify(search_results)

    except sqlite3.Error as error:
        return jsonify({'error': str(error)}), 400
    finally:
        if conn:
            conn.close()
@app.route('/textbook', methods=['GET'])
def get_textbook():
    textbook_name = request.args.get('id', '').strip()
    if not textbook_name:
        return jsonify({'error': 'No textbook provided'}), 400

    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT t_name, t_class, t_professor, t_ebook, t_required, t_link FROM tbl_textbooks WHERE t_name = ? COLLATE NOCASE", (textbook_name,))
        row = cursor.fetchone()
        return jsonify({"t_name": row[0], "t_class": row[1], "t_professor": row[2] or "N/A", "t_ebook": bool(row[3]), "t_required": bool(row[4]), "t_link": row[5] or None}) if row else jsonify({'error': 'Textbook not found'}), 404

    except sqlite3.Error as error:
        return jsonify({'error': str(error)}), 500
    finally:
        conn.close()
@app.route('/debug', methods=['GET'])
def debug_database():
    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()
        
        # Fetch all rows from the database to check data
        cursor.execute("SELECT * FROM tbl_textbooks")
        all_rows = cursor.fetchall()
        
        return jsonify(all_rows)  # Print all database entries to check if "Test" exists
    except sqlite3.Error as error:
        return jsonify({'error': str(error)}), 400
    finally:
        if conn:
            conn.close()
@app.route('/check_test', methods=['GET'])
def check_test_entry():
    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()
        
        # Check if a book named "Test" exists
        cursor.execute("SELECT * FROM tbl_textbooks WHERE t_name LIKE '%Test%' COLLATE NOCASE")
        test_entry = cursor.fetchall()
        
        return jsonify(test_entry)
    except sqlite3.Error as error:
        return jsonify({'error': str(error)}), 400
    finally:
        if conn:
            conn.close()

@app.route("/signup", methods=["POST"])
def signup():
    try:
        # Get the data from the request
        data = request.get_json()
        print(f"Received data: {data}")  # Log the received data

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        # Validate the input
        if not first_name or not last_name or not email or not password:
            return jsonify({"success": False, "message": "All fields are required."}), 400

        # Check if email already exists
        conn = sqlite3.connect("textbook_database.db")  # Make sure the DB name matches the one used elsewhere
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE u_email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return jsonify({"success": False, "message": "User already exists with this email."}), 400

        # Hash the password using hashlib
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        # Insert the new user into the database
        cursor.execute("INSERT INTO tbl_users (u_fname, u_lname, u_email, u_password) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, email, hashed_pw))
       # Generate a unique session token (UUID)
        token = str(uuid.uuid4())

        # Store the session token in the database for the user

        expiry_time = datetime.now() + timedelta(hours=24)
        expiry_str = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO tbl_tokens (to_value, to_user_email, to_expiry) VALUES (?, ?, ?)",
                       (token, email, expiry_str))
        conn.commit()
        conn.close()

        # Respond with success, the session token, and expiration time
        return jsonify({
            "success": True,
            "message": "Account created successfully!",
            "token": token,
            "expires_at": expiry_str
        }), 200

    except Exception as e:
        # Log the error and return a response
        print(f"Error occurred during signup: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred during signup."}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    hashed_pw = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()

        # Verify user credentials
        cursor.execute("""
            SELECT u_email FROM tbl_users WHERE u_email = ? AND u_password = ?
        """, (email, hashed_pw))
        user = cursor.fetchone()

        if user:
            # Generate token
            token = str(uuid.uuid4())
            
            # Set expiration 24 hours from now
            expiry_time = datetime.now() + timedelta(hours=24)
            expiry_str = expiry_time.strftime('%Y-%m-%d %H:%M:%S')

            # Insert token into tbl_tokens
            cursor.execute("""
                INSERT INTO tbl_tokens (to_value, to_user_email, to_expiry)
                VALUES (?, ?, ?)
            """, (token, email, expiry_str))
            conn.commit()

            # Return token and expiration info
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'expires_at': expiry_str
            }), 200
        else:
            return jsonify({'error': 'Incorrect email or password'}), 401

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route("/account_listings", methods=["GET"])
def account_listings():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    token = auth_header.split(" ")[1]

    try:
        conn = sqlite3.connect("textbook_database.db")
        cursor = conn.cursor()

        # Get user email from token
        cursor.execute("SELECT to_user_email FROM tbl_tokens WHERE to_value = ?", (token,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return jsonify({"success": False, "message": "Invalid token"}), 401

        user_email = result[0]

        # Get user name
        cursor.execute("SELECT u_fname FROM tbl_users WHERE u_email = ?", (user_email,))
        user_row = cursor.fetchone()
        user_name = user_row[0] if user_row else "User"

        # Fetch listings
        cursor.execute("SELECT l_id, l_bookname, l_condition, l_price FROM tbl_listings WHERE l_email = ?", (user_email,))
        listings = cursor.fetchall()

        conn.close()

        listings_data = [
            {
                "l_id": row[0],
                "l_bookname": row[1],
                "l_condition": row[2],
                "l_price": row[3]
            }
            for row in listings
        ]

        return jsonify({"success": True, "name": user_name, "listings": listings_data}), 200

    except Exception as e:
        print(f"Error fetching listings: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route('/create_listing', methods=['POST'])
def create_listing():
    # Get the token from the request header
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'error': 'Token missing'}), 400

    # Extract token from "Bearer <token>"
    token = token.split(" ")[1] if token else None

    if not token:
        return jsonify({'error': 'Invalid token'}), 400

    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()

        # Query the token table to check if the token exists
        cursor.execute("""
            SELECT to_user_email FROM tbl_tokens WHERE to_value = ?
        """, (token,))
        user_data = cursor.fetchone()

        # If no user data is returned, the token doesn't exist or has expired
        if not user_data:
            return jsonify({'error': 'Token not found or expired'}), 401

        user_email = user_data[0]

        # Get the listing data from the request
        data = request.get_json()

        # Log incoming listing data for debugging
        print(f"[DEBUG] Incoming listing data: {data}")

        l_bookname = data.get('l_bookname')
        l_condition = data.get('l_condition')
        l_price = data.get('l_price')

        # Check if all required fields are present
        if not l_bookname or not l_condition or not l_price:
            return jsonify({'error': 'Missing data for listing'}), 400

        # Log the values to ensure they are being fetched correctly
        print(f"[DEBUG] Extracted values: {l_bookname}, {l_condition}, {l_price}")

        # Insert new listing into the database
        cursor.execute("""
            INSERT INTO tbl_listings (l_bookname, l_condition, l_price, l_email)
            VALUES (?, ?, ?, ?)
        """, (l_bookname, l_condition, l_price, user_email))

        # Commit the transaction
        conn.commit()

        # Log successful insertion
        print("[DEBUG] Listing inserted successfully.")

        return jsonify({'success': True, 'message': 'Listing created successfully.'}), 201

    except sqlite3.Error as e:
        # Log the error for debugging
        print(f"[ERROR] SQLite Error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

    except Exception as e:
        # Catch other unexpected errors and log them
        print(f"[ERROR] Unexpected Error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

    finally:
        # Ensure connection is closed
        if 'conn' in locals() and conn:
            conn.close()
            
@app.route('/remove_listing/<int:listing_id>', methods=['DELETE'])
def remove_listing(listing_id):
    token = request.headers.get('Authorization')

    if not token or not token.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid token'}), 400

    token = token.split(" ")[1]

    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()

        # Get the user's email from the token
        cursor.execute("SELECT to_user_email FROM tbl_tokens WHERE to_value = ?", (token,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Invalid or expired token'}), 401

        user_email = result[0]

        # Ensure the listing belongs to the user
        cursor.execute("SELECT l_id FROM tbl_listings WHERE l_id = ? AND l_email = ?", (listing_id, user_email))
        listing = cursor.fetchone()

        if not listing:
            return jsonify({'error': 'Listing not found or not authorized'}), 403

        # Delete the listing
        cursor.execute("DELETE FROM tbl_listings WHERE l_id = ?", (listing_id,))
        conn.commit()

        return jsonify({'success': True}), 200

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if conn:
            conn.close()
            
@app.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization')

    if not token or not token.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid token'}), 400

    token = token.split(" ")[1]  # Extract token from "Bearer <token>"

    try:
        conn = sqlite3.connect('textbook_database.db')
        cursor = conn.cursor()

        # Remove the token from the database to invalidate it
        cursor.execute("DELETE FROM tbl_tokens WHERE to_value = ?", (token,))
        conn.commit()

        return jsonify({'success': True}), 200

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if conn:
            conn.close()

            
if __name__ == '__main__':
    app.run(debug=True)