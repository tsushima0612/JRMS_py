from flask import Flask, render_template, url_for
app= Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register_accounts')
def register_accounts():
    return render_template('register_accounts.html')

if __name__ == '__main__':
    app.run(debug=True)