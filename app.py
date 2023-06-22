from flask import Flask, render_template, url_for, request, redirect
import db
app= Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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
    
if __name__ == '__main__':
    app.run(debug=True)