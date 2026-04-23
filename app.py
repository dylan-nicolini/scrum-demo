from flask import Flask, jsonify

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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
