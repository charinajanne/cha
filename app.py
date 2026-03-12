from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to my Flask API!"

@app.route('/student')
def get_student():
    return jsonify({
        "name": "Cha",
        "grade": 10,
        "section": "Arduino"
    })

if __name__ == '__main__':
    # This block allows you to run the app directly using 'python app.py'
    app.run(debug=True)

