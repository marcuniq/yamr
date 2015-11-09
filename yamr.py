from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('helloworld.html')


if __name__ == '__main__':
    app.run()
