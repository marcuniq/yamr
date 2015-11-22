from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    app.logger.debug('A value for debugging')
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
