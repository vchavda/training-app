from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route('/add')
def add():
    try:
        a = float(request.args.get('a', 0))
        b = float(request.args.get('b', 0))
    except ValueError:
        return jsonify({"error": "Invalid input"}), 400
    return jsonify({"result": a + b})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

