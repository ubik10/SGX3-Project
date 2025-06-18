from flask import Flask, request

app = Flask(__name__)

# More lines of code
# More lines of code


@app.route('/', methods=['GET'])
def hello_world():
    return "Hello World!\n"


@app.route('/<name>/<number>', methods=['GET'])
def hello_name(name):
    return f'Hello, {name}!\n'


@app.route('/hello', methods=['GET'])
def hello():
    name =  request.args.get('name')
    number = request.args.get('favnum')
    return f'Hello, {name}! How are you doing? I see your favorite number is: {number}'

#the last line of your flask application
if __name__ == '__main__':
    print("********Hey Look! Something is happening********")
    app.run(debug=True, host='0.0.0.0', port=8076)

