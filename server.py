from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_code', methods=['POST'])
def execute_code():
    output = ''
    for i in range(1, 101):
        output += 'Hi' * i + '\n'
    return jsonify({'output': output})

@app.route('/web_print', methods=['POST'])
def web_print():
    message = request.json.get('message', '')
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run()
