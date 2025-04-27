# Import the Flask class and necessary functions
from flask import Flask, request, make_response

# Create an instance of the Flask class
app = Flask(__name__)

# Define sample data
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]

# Routes

@app.route("/")
def index():
    """Handle requests to root URL and return a simple greeting."""
    return "hello world"

@app.route("/no_content")
def no_content():
    """Return 'no content found' with a 204 No Content status."""
    return ({"message": "No content found"}, 204)

@app.route("/exp")
def index_explicit():
    """Return a 'Hello World' message with status code 200."""
    resp = make_response({"message": "Hello World"})
    resp.status_code = 200
    return resp

@app.route("/students")
def get_students():
    """Return the list of students as JSON."""
    return ({"students": data}, 200)

@app.route("/data")
def get_data():
    """Check if data exists and return its length, or handle errors."""
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    """Find a person in the database by first name."""
    query = request.args.get('q')

    if not query:
        return {"message": "Query parameter 'q' is missing"}, 422

    for person in data:
        if query.lower() in person["first_name"].lower():
            return person, 200

    return {"message": "Person not found"}, 404

@app.route("/person/<var_name>", methods=['GET'])
def find_by_uuid(var_name):
    """Find a person in the database by UUID."""
    for person in data:
        if person["id"] == str(var_name):
            return person, 200

    return {"message": "Person not found"}, 404

@app.route("/person/<var_name>", methods=['DELETE'])
def delete_person(var_name):
    """Delete a person from the database by UUID."""
    for person in data:
        if person["id"] == str(var_name):
            data.remove(person)
            return {"message": "Person with ID deleted"}, 200

    return {"message": "Person not found"}, 404

@app.route("/person", methods=['POST'])
def add_by_uuid():
    """Add a new person to the database."""
    new_person = request.json

    if not new_person:
        return {"message": "Invalid input parameter"}, 422

    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": f"{new_person['id']}"}, 200

# Error Handling

@app.errorhandler(404)
def api_not_found(error):
    """Custom error handler for 404 Not Found."""
    return {"message": "API not found"}, 404

# Run app
if __name__ == "__main__":
    app.run(debug=True)