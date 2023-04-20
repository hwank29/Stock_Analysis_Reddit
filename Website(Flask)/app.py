from flask import Flask, render_template, request

app = Flask(__name__, static_folder="static")

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        start_date = request.form.get("start")
        end_date = request.form.get("end")
        return f"Your start date is {start_date} and your end date is {end_date}"
    return render_template('main.html')



if __name__ == '__main__':
    app.run(port=5001, debug=True)
