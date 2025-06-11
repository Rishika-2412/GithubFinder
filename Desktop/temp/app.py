from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'keep-it-secret'

users = {}
stocks = []
transactions = []
predictions = []

login_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div style="max-width: 400px; margin: 80px auto;" class="border rounded p-4 shadow-sm bg-white">
        <h2 class="text-center">Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" class="form-control my-2" required>
            <input type="password" name="password" placeholder="Password" class="form-control my-2" required>
            <button class="btn btn-primary w-100 my-2">Login</button>
            <a href="/signup" class="btn btn-outline-secondary w-100">Sign Up</a>
        </form>
    </div>
</body>
</html>
'''

signup_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div style="max-width: 400px; margin: 80px auto;" class="border rounded p-4 shadow-sm bg-white">
        <h2 class="text-center">Sign Up</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" class="form-control my-2" required>
            <input type="password" name="password" placeholder="Password" class="form-control my-2" required>
            <button class="btn btn-success w-100 my-2">Create Account</button>
            <a href="/login" class="btn btn-outline-secondary w-100">Back to Login</a>
        </form>
    </div>
</body>
</html>
'''

home_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container py-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Welcome, {{ user }}</h2>
            <a href="/logout" class="btn btn-danger">Logout</a>
        </div>

        <!-- Stocks Section -->
        <h4>Stocks</h4>
        <form method="POST" action="/add_stock" class="row g-2 mb-3">
            <div class="col-md-4"><input type="text" name="name" placeholder="Stock Name" class="form-control" required></div>
            <div class="col-md-3"><input type="number" name="price" placeholder="Price" class="form-control" required></div>
            <div class="col-md-3"><input type="number" name="quantity" placeholder="Quantity" class="form-control" required></div>
            <div class="col-md-2"><button class="btn btn-primary w-100">Add Stock</button></div>
        </form>
        <table class="table table-bordered">
            <thead><tr><th>#</th><th>Name</th><th>Price</th><th>Quantity</th><th>Actions</th></tr></thead>
            <tbody>
                {% for stock in stocks %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ stock.name }}</td>
                    <td>{{ stock.price }}</td>
                    <td>{{ stock.quantity }}</td>
                    <td>
                        <a href="/edit_stock/{{ loop.index0 }}" class="btn btn-sm btn-warning">Edit</a>
                        <a href="/delete_stock/{{ loop.index0 }}" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Transactions Section -->
        <h4>Transactions</h4>
        <form method="POST" action="/add_transaction" class="row g-2 mb-3">
            <div class="col-md-4"><input type="text" name="stock" placeholder="Stock Name" class="form-control" required></div>
            <div class="col-md-3"><input type="number" name="quantity" placeholder="Quantity" class="form-control" required></div>
            <div class="col-md-3"><input type="text" name="type" placeholder="Buy/Sell" class="form-control" required></div>
            <div class="col-md-2"><button class="btn btn-success w-100">Add Transaction</button></div>
        </form>
        <table class="table table-bordered">
            <thead><tr><th>#</th><th>Stock</th><th>Quantity</th><th>Type</th><th>Actions</th></tr></thead>
            <tbody>
                {% for tx in transactions %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ tx.stock }}</td>
                    <td>{{ tx.quantity }}</td>
                    <td>{{ tx.type }}</td>
                    <td>
                        <a href="/edit_transaction/{{ loop.index0 }}" class="btn btn-sm btn-warning">Edit</a>
                        <a href="/delete_transaction/{{ loop.index0 }}" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Predictions Section -->
        <h4>Predictions</h4>
        <form method="POST" action="/add_prediction" class="row g-2 mb-3">
            <div class="col-md-4"><input type="text" name="stock" placeholder="Stock Name" class="form-control" required></div>
            <div class="col-md-3"><input type="number" name="predicted_price" placeholder="Predicted Price" class="form-control" required></div>
            <div class="col-md-3"><input type="text" name="date" placeholder="Prediction Date" class="form-control" required></div>
            <div class="col-md-2"><button class="btn btn-info w-100">Add Prediction</button></div>
        </form>
        <table class="table table-bordered">
            <thead><tr><th>#</th><th>Stock</th><th>Predicted Price</th><th>Date</th><th>Actions</th></tr></thead>
            <tbody>
                {% for pred in predictions %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ pred.stock }}</td>
                    <td>{{ pred.predicted_price }}</td>
                    <td>{{ pred.date }}</td>
                    <td>
                        <a href="/edit_prediction/{{ loop.index0 }}" class="btn btn-sm btn-warning">Edit</a>
                        <a href="/delete_prediction/{{ loop.index0 }}" class="btn btn-sm btn-danger">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        if u in users and users[u] == p:
            session['user'] = u
            return redirect('/home')
    return render_template_string(login_template)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        u, p = request.form['username'], request.form['password']
        if u not in users:
            users[u] = p
            return redirect('/login')
    return render_template_string(signup_template)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/login')
    return render_template_string(home_template, user=session['user'], stocks=stocks, transactions=transactions, predictions=predictions)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    stocks.append({
        'name': request.form['name'],
        'price': request.form['price'],
        'quantity': request.form['quantity']
    })
    return redirect('/home')

@app.route('/delete_stock/<int:index>')
def delete_stock(index):
    if 0 <= index < len(stocks):
        stocks.pop(index)
    return redirect('/home')

@app.route('/edit_stock/<int:index>', methods=['GET', 'POST'])
def edit_stock(index):
    if request.method == 'POST':
        stocks[index] = {
            'name': request.form['name'],
            'price': request.form['price'],
            'quantity': request.form['quantity']
        }
        return redirect('/home')
    s = stocks[index]
    return f'''
        <form method="POST">
            <input name="name" value="{s['name']}">
            <input name="price" value="{s['price']}">
            <input name="quantity" value="{s['quantity']}">
            <button>Update</button>
        </form>
    '''

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transactions.append({
        'stock': request.form['stock'],
        'quantity': request.form['quantity'],
        'type': request.form['type']
    })
    return redirect('/home')

@app.route('/delete_transaction/<int:index>')
def delete_transaction(index):
    if 0 <= index < len(transactions):
        transactions.pop(index)
    return redirect('/home')

@app.route('/edit_transaction/<int:index>', methods=['GET', 'POST'])
def edit_transaction(index):
    if request.method == 'POST':
        transactions[index] = {
            'stock': request.form['stock'],
            'quantity': request.form['quantity'],
            'type': request.form['type']
        }
        return redirect('/home')
    t = transactions[index]
    return f'''
        <form method="POST">
            <input name="stock" value="{t['stock']}">
            <input name="quantity" value="{t['quantity']}">
            <input name="type" value="{t['type']}">
            <button>Update</button>
        </form>
    '''

# Predictions (NEW)
@app.route('/add_prediction', methods=['POST'])
def add_prediction():
    predictions.append({
        'stock': request.form['stock'],
        'predicted_price': request.form['predicted_price'],
        'date': request.form['date']
    })
    return redirect('/home')

@app.route('/delete_prediction/<int:index>')
def delete_prediction(index):
    if 0 <= index < len(predictions):
        predictions.pop(index)
    return redirect('/home')

@app.route('/edit_prediction/<int:index>', methods=['GET', 'POST'])
def edit_prediction(index):
    if request.method == 'POST':
        predictions[index] = {
            'stock': request.form['stock'],
            'predicted_price': request.form['predicted_price'],
            'date': request.form['date']
        }
        return redirect('/home')
    p = predictions[index]
    return f'''
        <form method="POST">
            <input name="stock" value="{p['stock']}">
            <input name="predicted_price" value="{p['predicted_price']}">
            <input name="date" value="{p['date']}">
            <button>Update</button>
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)