from flask import Flask, json, jsonify, render_template, request, url_for
from functions import create_db, search_errors, search_exact, search_trigrams
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
create_db()

@app.route("/")
def index():
    return render_template("base.html", title="Index")

@app.route("/search", methods=["GET", "POST"])
def search_page():
    if request.method == "POST":
        canonical_query = str(request.form["query"]).lower()

        # Perform progressively more expensive operations, so look for an
        # exact match first before doing any computations.
        if search_exact(canonical_query):
            return jsonify([{"rank": 1, "artistName": str(request.form["query"])}])

        trigram_results = search_trigrams(canonical_query)
        if len(trigram_results) > 0:
            return jsonify([{"rank": i, "artistName": name.name} for i, name in enumerate(trigram_results, 1)])
        else:
            return search_errors(canonical_query) 

    return render_template("search.html", title="MusicFox")

# Boilerplate error handling
@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response