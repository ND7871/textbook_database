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
def insert_textbook(db_name, t_bookname, t_class, t_professor, t_ebook, t_required, t_link ):
    try:
        conn = sqlite3.connect(db_name)
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

def insert_user(db_name, u_email, u_fname, u_lname, u_password):
    try: 
        conn = sqlite3.connect(db_name)
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
def insert_listing(db_name, l_id, l_bookname, l_email, l_condition, l_price):
    try: 
        conn = sqlite3.connect(db_name)
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
def user_table_test():
    cursor.execute("""SELECT*FROM tbl_users""")
    user = cursor.fetchall()

    for users in user:
        print(user) 

def textbook_table_test():
    cursor.execute("""SELECT*FROM tbl_textbooks""")
    textbook = cursor.fetchall()

    for textbooks in textbook:
        print(textbook)

def listing_table_test():
    cursor.execute("""SELECT*FROM tbl_listings""")
    listing = cursor.fetchall()

    for listings in listing:
        print(listing)

cursor.execute(create_table_textbooks)
cursor.execute(create_table_users)
cursor.execute(create_table_listings)

insert_listing('test.db','1','Math for Dummies','tester123@gmail.com','Good','20.00')
textbook_table_test()
user_table_test()
listing_table_test()

conn.commit()
conn.close()
