from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage (used by later issues)
users = []
next_id = 1


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    global next_id
    data = request.get_json(silent=True) or {}

    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "'name' and 'email' are required"}), 400

    if any(u['email'] == email for u in users):
        return jsonify({"error": "Email already registered"}), 400

    user = {'id': next_id, 'name': name, 'email': email}
    users.append(user)
    next_id += 1

    return jsonify(user), 201


if __name__ == '__main__':
    app.run(port=5000, debug=True)
