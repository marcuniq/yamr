from flask import Flask, jsonify, render_template, request
from yamr_ml.recommender import RecommendationEngine

app = Flask(__name__)


@app.route('/')
def hello_world():
    app.logger.debug('A value for debugging')
    return render_template('helloworld.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
