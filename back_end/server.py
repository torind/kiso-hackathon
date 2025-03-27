import flask
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

app = flask.Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# # Test the OpenAI client with a simple API call
# try:
#     test_response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": "Hello"}],
#         max_tokens=10
#     )
#     print("Test response:", test_response.choices[0].message.content)
# except Exception as e:
#     print(f"Error initializing OpenAI client: {str(e)}")
#     raise e

@app.route('/api/summary', methods=['POST'])
def summary():
    print("Summary function called")
    # Load the Sales Demand Forecast notebook directly
    with open('notebooks/Sales Demand Forecast.ipynb', 'r') as f:
        notebook = json.loads(f.read())
    
    # Extract cells from the notebook
    cells = notebook.get('cells', [])
    
    # Combine cell contents into a single text
    notebook_content = ""
    for cell in cells:
        if cell.get('cell_type') == 'code':
            notebook_content += f"Code cell:\n{cell.get('source', '')}\n\n"
        elif cell.get('cell_type') == 'markdown':
            notebook_content += f"Markdown cell:\n{cell.get('source', '')}\n\n"
    
    # Create the prompt for OpenAI
    prompt = f"""Please provide a concise summary of this Jupyter notebook. Focus on:
1. The main purpose of the notebook
2. Key code implementations
3. Important findings or conclusions

Notebook content:
{notebook_content}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Jupyter notebooks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        print(summary)
        return #flask.jsonify({"summary": summary}), 200
    except Exception as e:
        return #flask.jsonify({"error": str(e)}), 500

summary()