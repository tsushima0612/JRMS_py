import os, psycopg2, string, random, hashlib

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters+ string.digits
    salt = ''.join(random.choices(charset, k=10))
    return salt

def get_hash(password, salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')
    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1250).hex()
    return hashed_password

def insert_user(email,password):
    sql = 'INSERT INTO jrms_accounts VALUES(default, %s, %s, %s, %s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    print(hashed_password)
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (email, hashed_password, salt,"3"))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
    
    except psycopg2.DatabaseError:
        count = 0
    
    finally:
        cursor.close()
        connection.close()
        
    return count

def login(mail,password):
    sql = "SELECT hashed_password,salt FROM jrms_accounts WHERE mail = %s"
    flg = False
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            hashed_password = get_hash(password, salt)

            if hashed_password == user[0]:
                flg = True
                
    except psycopg2.DataError:
        flg = False
        
    finally :
        cursor.close()
        connection.close()
        
    return flg

def account_sort(mail):
    sql = "SELECT user_rank FROM jrms_accounts WHERE mail = %s"
    count = 0
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        count = cursor.fetchone()
        
    except psycopg2.DataError:
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count

def save_file(file_name):
    sql = "INSERT INTO jrms_file VALUES(default, %s, current_timestamp, '0')"
    count = 0
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (file_name,))
        count = cursor.rowcount #更新件数を取得
        connection.commit()
    
    except psycopg2.DatabaseError:
        count = 0
    
    finally:
        cursor.close()
        connection.close()
        
    return count

def search_file(keyword):
    sql = "SELECT * FROM jrms_file where file_name like %s"
    keyword = '%' + keyword + '%'
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(keyword,))
        rows = cursor.fetchall()
        
    except psycopg2.DataError:
         rows = 0
    
    finally :
         cursor.close()
         connection.close()
    
    print(rows)
    return rows