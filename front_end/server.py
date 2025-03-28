import flask
import os
import json

from llm_endpoints import api_bp

notebook_name = 'Sales Demand Forecast.ipynb'

app = flask.Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/notebook-content')
def get_notebook():
    try:
        # Construct the path to the notebook
        notebook_path = os.path.join('notebooks', notebook_name)
        
        # Check if file exists
        if not os.path.exists(notebook_path):
            return flask.jsonify({'error': 'Notebook not found'}), 404
            
        # Read the notebook file
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
            
        # Convert notebook cells to markdown
        markdown_content = ""
        for cell in notebook['cells']:
            if cell['cell_type'] == 'markdown':
                markdown_content += ''.join(cell['source']) + '\n\n'
            elif cell['cell_type'] == 'code':
                markdown_content += '```python\n' + ''.join(cell['source']) + '\n```\n\n'
                
        return markdown_content
        
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    