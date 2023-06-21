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
    print('salt:'+salt)
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