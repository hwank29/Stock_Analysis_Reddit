from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entry_content = request.form
    return render_template('home.html',)

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/Registration')
def registration():
    return render_template('registration.html')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
