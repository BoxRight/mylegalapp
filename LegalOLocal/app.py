# app.py

# Import necessary packages and modules
from flask import Flask, render_template, request, jsonify
import json  # Make sure to import this for JSON formatting
from data_processing import process_selected_numbers  # Functions for data processing
from database import rows, statement_dict, get_matches_from_db  # Data structures storing the rows and statement mapping
from deduction_module import main  # Deduction logic

# Generate the tensors
all_tensors = main()

# Create the Flask application instance
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = None
    formatted_results = None

    if request.method == 'POST':
        selected_numbers = request.form.getlist('selection[]')
        selected_numbers = [int(num) for num in selected_numbers]
        results = process_selected_numbers(selected_numbers, all_tensors, statement_dict)
        formatted_results = json.dumps(results, indent=4)  # Convert the results to a formatted string
    return render_template('index.html', results=results, formatted_results= formatted_results)

@app.route('/autocomplete', methods=['GET', 'POST'])
def autocomplete():
    query = request.args.get('query')
    if not query:
        return render_template("input_form.html")
    matches = get_matches_from_db(query)
    return jsonify({'matches': matches})

if __name__ == "__main__":
    # Start the Flask development server
    app.run
    app.debug=True

