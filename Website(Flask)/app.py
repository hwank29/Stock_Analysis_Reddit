from flask import Flask, render_template, request

app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        entry_content = request.form
    return render_template('main.html')



if __name__ == '__main__':
    app.run(port=5001, debug=True)
