from flask import Flask, jsonify, request

app = Flask(__name__)

# 1. Move the data into a dictionary variable so it can be modified
student_database = {
    "name": "Cha",
    "grade": 10,
    "section": "Arduino"
}

@app.route('/')
def home():
    return "Welcome to my Flask API!"

# 2. This route now returns the CURRENT state of the variable
@app.route('/student', methods=['GET'])
def get_student():
    return jsonify(student_database)

# 3. Add a route to UPDATE the data
@app.route('/update-student', methods=['POST'])
def update_student():
    # Get the JSON data sent from the user/client
    data = request.get_json()

    # Update only the fields provided in the request
    if 'name' in data:
        student_database['name'] = data['name']
    if 'grade' in data:
        student_database['grade'] = data['grade']
    if 'section' in data:
        student_database['section'] = data['section']

    return jsonify({
        "message": "Student updated successfully!",
        "new_data": student_database
    })

if __name__ == '__main__':
    app.run(debug=True)
