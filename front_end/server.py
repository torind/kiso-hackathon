import flask

from llm_endpoints import api_bp

app = flask.Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    