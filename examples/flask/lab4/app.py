# Import necessary libraries from Flask
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask application
app = Flask(__name__)

# Sample data representing transactions
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Helper function to calculate total balance
def calculate_total_balance():
    return sum(transaction['amount'] for transaction in transactions)

# Read operation: Route to list all transactions
@app.route("/")
def get_transactions():
    balance = calculate_total_balance()
    return render_template("transactions.html", transactions=transactions, balance=balance)

# Create operation: Route to display and process add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    return render_template("form.html")

# Update operation: Route to display and process edit transaction form
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = float(request.form['amount'])

        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        return redirect(url_for("get_transactions"))

    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation: Route to delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Search operation: Route to search transactions by amount range
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == 'POST':
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])

        filtered_transactions = [
            transaction for transaction in transactions
            if min_amount <= transaction['amount'] <= max_amount
        ]

        balance = sum(transaction['amount'] for transaction in filtered_transactions)

        return render_template("transactions.html", transactions=filtered_transactions, balance=balance)

    return render_template("search.html")

# New route: Total balance as a plain text page
@app.route("/balance")
def total_balance():
    """Display total balance as plain text."""
    balance = calculate_total_balance()
    return f"Total Balance: {balance}"

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)