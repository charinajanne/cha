from flask import Flask, jsonify, request

app = Flask(__name__)

# Database now supports multiple students (dictionary keyed by ID)
student_database = {
    1: {"name": "Cha", "grade": 10, "section": "Arduino"}
}

@app.route('/')
def home():
    return "Welcome to my Flask API!"

# ------------------- READ -------------------

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(student_database)

# GET a single student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = student_database.get(student_id)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

# ------------------- CREATE -------------------

# Add a new student
@app.route('/add-student', methods=['POST'])
def add_student():
    data = request.get_json()

    # Validate required fields
    if not all(key in data for key in ("name", "grade", "section")):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate grade type
    if not isinstance(data["grade"], int):
        return jsonify({"error": "Grade must be an integer"}), 400

    # Generate new ID
    new_id = max(student_database.keys(), default=0) + 1
    student_database[new_id] = {
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }

    return jsonify({
        "message": "Student added successfully!",
        "student_id": new_id,
        "new_data": student_database[new_id]
    }), 201

# ------------------- UPDATE -------------------

# Update student by ID
@app.route('/update-student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    data = request.get_json()
    student = student_database.get(student_id)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # Validate and update fields
    if 'name' in data:
        student['name'] = data['name']
    if 'grade' in data:
        if isinstance(data['grade'], int):
            student['grade'] = data['grade']
        else:
            return jsonify({"error": "Grade must be an integer"}), 400
    if 'section' in data:
        student['section'] = data['section']

    return jsonify({
        "message": "Student updated successfully!",
        "new_data": student
    }), 200

# ------------------- DELETE -------------------

# Delete student by ID
@app.route('/delete-student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if student_id in student_database:
        deleted = student_database.pop(student_id)
        return jsonify({
            "message": "Student deleted successfully!",
            "deleted_data": deleted
        }), 200
    return jsonify({"error": "Student not found"}), 404

# ------------------- MAIN -------------------

if __name__ == '__main__':
    app.run(debug=True)
