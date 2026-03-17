from flask import Flask, jsonify, request
from flask_cors import CORS  # Optional – enables cross-origin access (for frontend use)

app = Flask(__name__)
CORS(app)

# ------------------- DATABASE MOCK -------------------
# In-memory DB for demonstration purposes
student_database = {
    1: {"name": "Cha", "grade": 10, "section": "Arduino"}
}

# ------------------- UTILITY -------------------

def validate_student_data(data, require_all=True):
    """
    Validates input JSON for student data.
    If require_all=True, all keys are required.
    """
    required_fields = ("name", "grade", "section")
    if require_all and not all(key in data for key in required_fields):
        return "Missing required fields"
    
    if "grade" in data and not isinstance(data["grade"], int):
        return "Grade must be an integer"
    
    return None

# ------------------- ROUTES -------------------

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Student Management API!"})

# ---------- READ ----------
@app.route('/students', methods=['GET'])
def get_students():
    # Optional query filtering: e.g., /students?grade=10
    grade = request.args.get('grade', type=int)
    section = request.args.get('section', type=str)

    filtered_students = {
        sid: s for sid, s in student_database.items()
        if (grade is None or s["grade"] == grade) and
           (section is None or s["section"].lower() == section.lower())
    }
    return jsonify(filtered_students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = student_database.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"id": student_id, **student}), 200

# ---------- CREATE ----------
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json(force=True)
    error = validate_student_data(data, require_all=True)
    if error:
        return jsonify({"error": error}), 400

    new_id = max(student_database.keys(), default=0) + 1
    student_database[new_id] = {
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }

    return jsonify({
        "message": "Student created successfully",
        "student_id": new_id,
        "data": student_database[new_id]
    }), 201

# ---------- UPDATE ----------
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if student_id not in student_database:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json(force=True)
    error = validate_student_data(data, require_all=False)
    if error:
        return jsonify({"error": error}), 400

    student = student_database[student_id]
    student.update({k: v for k, v in data.items() if k in ("name", "grade", "section")})

    return jsonify({
        "message": "Student updated successfully",
        "data": student
    }), 200

# ---------- DELETE ----------
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if student_id not in student_database:
        return jsonify({"error": "Student not found"}), 404

    deleted = student_database.pop(student_id)
    return jsonify({
        "message": "Student deleted successfully",
        "deleted": deleted
    }), 200

# ------------------- ERROR HANDLERS -------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

# ------------------- MAIN -------------------

if __name__ == '__main__':
    app.run(debug=True)
