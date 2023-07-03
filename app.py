from flask import Flask, render_template, url_for, request, redirect,session, Blueprint
import db,string,random

app= Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

# ログイン画面
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail')
    password = request.form.get('pass')
    
    if mail == '' or password == '' :
        error = 'メールアドレスとパスワードを入力してください'
        input_data = {'mail':mail}
        return render_template('index.html',error = error,data=input_data)       
    
    if db.login(mail,password):
        rank = db.account_sort(mail)
        if(int(rank[0])==3):
            session['user'] = True
            return redirect(url_for('mypage'))
        
        elif(int(rank[0])==2):
            session['user'] = True
            return redirect(url_for('mypage2'))
        else:
            error = 'メールアドレス または パスワードが違います'
            input_data ={'mail':mail,}
        return render_template('index.html',error=error,data=input_data)
    else :
        error = 'メールアドレス または パスワードが違います'
        input_data ={
            'mail':mail,
        }
        return render_template('index.html',error=error,data=input_data)

#ログアウト
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))

# メニュー
@app.route('/mypage')
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/mypage2')
def mypage2():
    if 'user' in session:
        return render_template('mypage2.html')
    else:
        return redirect(url_for('index'))

#　新規登録
@app.route('/register_accounts')
def register_accounts():
    return render_template('register_accounts.html')

@app.route('/register_success')
def register_success():
    return render_template('register_success.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    email = request.form.get('email')
    password = request.form.get('pass')
    if email == '' or password == '' :
        error = 'メールアドレスとパスワードを入力してください'
        input_data = {'email':email}
        return render_template('register_accounts.html',error = error,data=input_data)        
     
    count = db.insert_user(email, password)
    
    if count == 1:
        return redirect(url_for('register_success'))
    
    else:
        error = 'このメールアドレスは使用されています'
        input_data = {'email':email}
        return render_template('register_accounts.html',error = error,data=input_data) 
# だいじ
if __name__ == '__main__':
    app.run(debug=True)