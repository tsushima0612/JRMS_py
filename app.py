from flask import Flask, render_template, url_for, request, redirect
import db
app= Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_accounts')
def register_accounts():
    return render_template('register_accounts.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    email = request.form.get('mail')
    password = request.form.get('pass')
    print("email:"+email)
    if email == '' or password == '' :
        error = '登録に失敗しました'
        print(error)
        return render_template('register_accounts.html',error = error)        
     
    count = db.insert_user(email, password)
    
    if count == 1:
        msg = '登録成功しました'
        return redirect(url_for('index',msg=msg))
    
    else:
        error = '登録に失敗しました'
        print(error)
        return render_template('register_accounts.html',error = error)
    
if __name__ == '__main__':
    app.run(debug=True)