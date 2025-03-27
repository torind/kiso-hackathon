import flask
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

api_bp = flask.Blueprint('llm_endpoints', __name__)

@api_bp.route('/summary', methods=['GET'])
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
    prompt = f"""Please provide a high-level summary of this Jupyter notebook focusing on knowledge transfer.

1. Executive Summary
   - What is the main purpose and objective of this notebook?
   - What approach was taken and what conclusions were drawn?

2. Technical Details
   - What key libraries and frameworks were used?
   - What core algorithms and data processing techniques were implemented?
   - What notable code patterns or architectural decisions were made?

3. Knowledge Transfer Notes
   - What are the key points someone needs to understand this notebook?
   - Are there any potential knowledge gaps or areas needing clarification?

Please provide your response in clear, concise bullet points.

Notebook content:
{notebook_content}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Jupyter notebooks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        return flask.jsonify(summary), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    

@api_bp.route('/cell_deep_dive', methods=['GET'])
def cell_deep_dive(cell_id=6):
    print("Cell deep dive")
    # Load the Sales Demand Forecast notebook directly
    with open('notebooks/Sales Demand Forecast.ipynb', 'r') as f:
        notebook = json.loads(f.read())
    # Extract cells from the notebook
    cells = notebook.get('cells', [])
    
    # Get the specific cell content
    notebook_content = ""
    if 0 <= cell_id < len(cells):
        cell = cells[cell_id]
        notebook_content = cell.get('source', '')
    
    # Create the prompt for OpenAI
    prompt = f"""This is a specific cell from a Jupyter notebook. Explain in detail what it does.

Notebook content:
{notebook_content}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Jupyter notebooks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        return flask.jsonify(summary), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    

@api_bp.route('/extract_knowledge_creator', methods=['GET'])
def extract_knowledge_creator():
    print("Extract knowledge creator")
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
    prompt = f"""Please analyze this notebook to extract the domain-specific knowledge and human reasoning applied by the creator.

1. Domain Knowledge (1-2 sentences)
   - What specific business/domain concepts are being addressed?
   - What assumptions and constraints were considered?
   - What domain-specific rules or patterns were applied?

2. Problem-Solving Approach (1-2 sentences)
   - What was the creator's thought process in approaching this problem?
   - What key decisions or trade-offs were made and why?
   - How were edge cases and special scenarios handled?

3. Expert Insights (1-2 sentences)
   - What specialized knowledge seems to come from experience?
   - What non-obvious considerations were factored in?
   - What business or domain context influenced the implementation?

4. Knowledge Gaps (1-2 sentences)
   - What implicit knowledge might not be documented?
   - What domain expertise would someone need to fully understand this?
   - What contextual information might be missing?

Please provide detailed insights focusing on the human reasoning and domain expertise, not the technical implementation.

Notebook content:
{notebook_content}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Jupyter notebooks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        return flask.jsonify(summary), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    

@api_bp.route('/test_comprehension', methods=['GET'])
def test_comprehension():
    print("Test comprehension")
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
    prompt = f"""Please analyze this notebook and create a multiple choice question that tests understanding of the key concepts.

The question should:
1. Focus on a core concept or technique used in the notebook
2. Have 4 possible answers (A, B, C, D)
3. Include an explanation of why the correct answer is right
4. Explain why the incorrect answers are wrong
5. Suggest a small code modification that would make each incorrect answer correct

Format your response as:
Question: [The question text]
A) [First option]
B) [Second option] 
C) [Third option]
D) [Fourth option]

Correct Answer: [Letter]

Explanation:
[Detailed explanation of correct answer]

Why other answers are incorrect:
[Explanation for each wrong answer and how to modify the code to make it work]

Notebook content:
{notebook_content}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Jupyter notebooks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        return flask.jsonify(summary), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    
@api_bp.route('/question_choices_creator', methods=['GET'])
def question_choices_creator():
    print("Question choices creator")
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
    prompt = f"""Please analyze this Jupyter notebook and identify aspects that require clarification from the creator for a proper handover:

1. Domain-Specific Knowledge Gaps (1-2 sentences)
   - What domain expertise or business context is assumed but not explained?
   - Are there any industry-specific terms or metrics that need definition?
   - What prior knowledge is required to fully understand this analysis?

2. Implementation Quirks (1-2 sentences)
   - Are there any unusual or non-standard approaches used?
   - What custom functions or utilities need additional explanation?
   - Are there any hardcoded values or magic numbers that need context?

3. Data Understanding (1-2 sentences)
   - What assumptions are made about the data structure and quality?
   - Are there any data preprocessing steps that need clarification?
   - What business rules or domain constraints influenced the data handling?

4. Maintenance Concerns (1-2 sentences)
   - Are there any fragile components or potential breaking points?
   - What dependencies or external systems need to be maintained?
   - What regular updates or monitoring might be required?

Please identify and explain any unclear or potentially confusing elements that would benefit from creator explanation.

Notebook content:
{notebook_content}"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes Jupyter notebooks."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content
        return flask.jsonify(summary), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    
@api_bp.route('/question_creator_context', methods=['POST'])
def question_creator_context():
    print("Question with context")
    
    # Get question from request
    data = flask.request.get_json()
    if not data or 'message' not in data:
        return flask.jsonify({"error": "Question is required"}), 400
    
    question = data['message']
    
    # Load the notebook
    with open('notebooks/Sales Demand Forecast.ipynb', 'r') as f:
        notebook = json.loads(f.read())
    
    # Load the context file
    try:
        with open('notebooks/context.txt', 'r') as f:
            context = f.read()
    except FileNotFoundError:
        context = "No additional context available."
    
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
    prompt = f"""Please answer the following question about this Jupyter notebook. Use both the notebook content and the additional context provided to give a complete answer.

Question: {question}

Notebook content:
{notebook_content}

Additional context:
{context}

only use 2 sentences for the answer"""

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about Jupyter notebooks using both the notebook content and additional context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        return flask.jsonify(answer), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


@api_bp.route('/get_context', methods=['GET'])
def get_context():
    try:
        with open('notebooks/context.txt', 'r') as f:
            context = f.read()
        return flask.jsonify(context), 200
    except FileNotFoundError:
        return flask.jsonify("No additional context available."), 404
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500
    
@api_bp.route('/update_context', methods=['POST'])
def update_context():
    try:
        # Get the new context from the request body
        new_context = flask.request.get_json().get('context')
        
        if not new_context:
            return flask.jsonify({"error": "No context provided in request"}), 400
            
        # Write the new context to the file
        with open('notebooks/context.txt', 'w') as f:
            f.write(new_context)
            
        return flask.jsonify({"message": "Context updated successfully"}), 200
    except Exception as e:
        return flask.jsonify({"error": str(e)}), 500


