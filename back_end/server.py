import flask

app = flask.Flask(__name__)

@app.route('/api/summary', methods=['POST'])
def summary():
    notebook = flask.request.json

    # Call the OpenAI

    return 200