import sqlite3

conn = sqlite3.connect('test.db')

cursor = conn.cursor()

create_table_textbooks = f"""
        CREATE TABLE IF NOT EXISTS tbl_textbooks (
            t_name VARCHAR(64) PRIMARY KEY NOT NULL,
            t_class VARCHAR(8) NOT NULL,
            t_professor VARCHAR(32),
            t_ebook INTEGER DEFAULT 0,  -- BOOLEAN field (0 for FALSE)
            t_required INTEGER DEFAULT 0,  -- BOOLEAN field (0 for FALSE)
            t_link VARCHAR(64)
        )
        """
create_table_users = f"""
        CREATE TABLE IF NOT EXISTS tbl_users (
            u_email VARCHAR(64) PRIMARY KEY NOT NULL,
            u_fname VARCHAR(16) NOT NULL,
            u_lname VARCHAR(16) NOT NULL,
            u_password VARCHAR(32) NOT NULL
        )
        """
create_table_listings = f"""
        CREATE TABLE IF NOT EXISTS tbl_listings (
            l_id VARCHAR(16) PRIMARY KEY NOT NULL,
            l_bookname VARCHAR(64) NOT NULL,
            l_email VARCHAR(64) NOT NULL,
            l_condition VARCHAR(12) NOT NULL,
            l_price INTEGER NOT NULL,
            FOREIGN KEY (l_bookname) REFERENCES tbl_textbooks(t_name),
            FOREIGN KEY (l_email) REFERENCES tbl_users(u_email)
        )
        """
def insert_textbook(t_bookname, t_class, t_professor, t_ebook, t_required, t_link ):
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        
        insert_sql = """
        INSERT INTO tbl_textbooks(t_name, t_class, t_professor, t_ebook, t_required, t_link)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        textbook_data = (t_bookname, t_class, t_professor, t_ebook, t_required, t_link)
        
        cursor.execute(insert_sql, textbook_data)
        conn.commit()
        
        print("Record inserted successfully.")
        
    except sqlite3.Error as error:
        print(f"Error while inserting data: {error}")
        
    finally:
        if conn:
            conn.close()

def insert_user(u_email, u_fname, u_lname, u_password):
    try: 
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO tbl_users(u_email, u_fname, u_lname, u_password)
        VALUES (?, ?, ?, ?)
        """
        user_data = (u_email, u_fname, u_lname, u_password)
        cursor.execute(insert_sql, user_data)
        conn.commit()

        print("Record inserted successfully.")

    except sqlite3.Error as error:
        print(f"Error while inserting data: {error}")
    
    finally:
        if conn:
            conn.close()
def insert_listing(l_id, l_bookname, l_email, l_condition, l_price):
    try: 
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        insert_sql = """
        INSERT INTO tbl_listings(l_id, l_bookname, l_email, l_condition, l_price)
        VALUES (?, ?, ?, ?, ?)
        """
        listing_data = (l_id, l_bookname, l_email, l_condition, l_price)
        cursor.execute(insert_sql, listing_data)
        conn.commit()

        print("Record inserted successfully.")

    except sqlite3.Error as error:
        print(f"Error while inserting data: {error}")
    
    finally:
        if conn:
            conn.close()
def remove_textbook(textbookname):
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        remove_sql = """DELETE FROM tbl_textbooks WHERE t_name = ? """
        cursor.execute(remove_sql, (textbookname,))
        conn.commit()

        print("Record removed sucesfully")

    except sqlite3.Error as error:
        print(f"Error while removing data: {error}")
    
    finally:
        if conn:
            conn.close()
def remove_user(useremail):
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        remove_sql = """DELETE FROM tbl_users WHERE u_email = ? """
        cursor.execute(remove_sql, (useremail,))
        conn.commit()

        print("Record removed sucesfully")

    except sqlite3.Error as error:
        print(f"Error while removing data: {error}")
    
    finally:
        if conn:
            conn.close()
def remove_listing(listingid):
    try:
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        remove_sql = """DELETE FROM tbl_listings WHERE l_id = ? """
        cursor.execute(remove_sql, (listingid,))
        conn.commit()

        print("Record removed sucesfully")

    except sqlite3.Error as error:
        print(f"Error while removing data: {error}")
    
    finally:
        if conn:
            conn.close()
def textbook_search(searchfield, keyword):
    try:
        if searchfield == 'Book Name':
            search_sql = """
            SELECT t_name, t_class, t_professor, t_ebook, t_required, t_link
            FROM tbl_textbooks
            WHERE t_name = ?
            """
        elif searchfield == 'Class':
            search_sql = """
            SELECT t_name, t_class, t_professor, t_ebook, t_required, t_link
            FROM tbl_textbooks
            WHERE t_class = ?
            """
        elif searchfield == 'Professor':
            search_sql = """
            SELECT t_name, t_class, t_professor, t_ebook, t_required, t_link
            FROM tbl_textbooks
            WHERE t_professor = ?
            """
        else:
            print(f"{searchfield} is not a valid field, please use Book Name, Class, or Professor")
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute(search_sql,(keyword,))
        search = cursor.fetchall()
        print(search)

    except sqlite3.Error as error:
        print(f"Error while searching: {error}")
    finally:
        if conn:
            conn.close()
        

def user_table_test():
    cursor.execute("""SELECT*FROM tbl_users""")
    user = cursor.fetchall()
    print(user) 

def textbook_table_test():
    cursor.execute("""SELECT*FROM tbl_textbooks""")
    textbook = cursor.fetchall()
    print(textbook)

def listing_table_test():
    cursor.execute("""SELECT*FROM tbl_listings""")
    listing = cursor.fetchall()
    print(listing)

cursor.execute(create_table_textbooks)
cursor.execute(create_table_users)
cursor.execute(create_table_listings)

textbook_table_test()
user_table_test()
listing_table_test()

conn.commit()
conn.close()
