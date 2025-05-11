
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    message = request.form.get('message')
    print(f"Received contact - Name: {name}, Phone: {phone}, Message: {message}")
    return "Thank you for contacting us!"

if __name__ == '__main__':
    app.run(debug=True)
