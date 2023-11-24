from flask import Flask, request, redirect, url_for, render_template, abort
from flask_login import LoginManager, UserMixin
import flask_login
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash, safe_join

categories = []
db_file = "amazon.db"

def load_data():
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute("SELECT Name FROM Categories").fetchall()
    for ct in res:
        categories.append(ct[0])
        
    con.close()

load_data()

app = Flask(__name__)
app.config['SECRET_KEY'] = "943a776ef82f2ff9b6e394780dacf7b5bb24505f"

login_manager = LoginManager(app)

#Main page
@app.route("/")
def main_page():
    if flask_login.current_user.is_anonymous:
        print("The user is not logged in")
    else:
        print(f"The user is {flask_login.current_user.name}")
    return render_template("hello_world.html", title="Mamazon", content="<p>Hello world</p>", categories=categories, create_user=flask_login.current_user)

@app.route("/products")
def products_page():
    con = sql.connect(db_file)
    cur = con.cursor()
    
    f_category = ""
    if "Category" in request.args:
        for cat in request.args.getlist("Category"):
            res = cur.execute(f"SELECT Id FROM Categories WHERE Name = \"{cat}\"").fetchall()
            if len(res) == 0:
                continue
            
            cat_id = res[0][0]
            
            f_category += (" AND " if f_category != "" else "") + f"Id IN (SELECT ProductID FROM product_category WHERE CategoryId = {cat_id})"
    
    f_search = ""
    if "Search" in request.args: 
        search_q = request.args.get("Search")
        f_search = f"((Name LIKE \"%{search_q}%\" COLLATE NOCASE) OR (Description LIKE \"%{search_q}%\" COLLATE NOCASE))"
    f_category = "" if f_category == "" else f"({f_category})"
    
    filter_joined = ""
    if f_category != "" or f_search != "":
        join_str = " AND " if f_category != "" and f_search != "" else ""
        filter_joined = " WHERE " + f_search + join_str + f_category + ";"
    
    print("SELECT Name, Price, Description, Id FROM PRODUCTS"+filter_joined)
    res = cur.execute("SELECT Name, Price, Description, Id FROM PRODUCTS"+filter_joined).fetchall()
    
    products = []
    #res = cur.execute("SELECT Name, Price, Description, ProductId FROM Products").fetchall()
    for prod in res:
        products.append({"Name": prod[0], "Price": prod[1], "Description": prod[2],"Images": [], "pId": prod[3]})
        
        imgs = cur.execute(f"SELECT url FROM ProductImages WHERE fk_ProdId = {prod[3]}")
        for img in imgs:
            products[-1]["Images"].append(img[0])
        
    con.close()

    return render_template("products.html", title="Products - Mamazon", products=products, categories=categories, current_user=flask_login.current_user)

@app.route("/product")
def product_page():
    product_id = request.args["id"]
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    res = cur.execute(f"SELECT Name, Price, Description, StockSize FROM Products WHERE Id = {product_id}").fetchall()
    
    if len(res) == 0:
        return "Didint work little bro"
    
    res_img = cur.execute(f"SELECT Url FROM ProductImages WHERE fk_ProdId = {product_id}").fetchall()
    product_data = {"Name": res[0][0], "Price": res[0][1], "Description": res[0][2], "Stock": res[0][3], "Images":[]}
    for img in res_img:
        product_data["Images"].append(img[0])
    
    con.close()
    
    return render_template("product_page.html", categories=categories, current_user=flask_login.current_user, p_data= product_data)

@app.route("/mycart")
def cart_page():
    user = flask_login.current_user
    if user.is_anonymous:
        return "You must be loged in to acces this page"
    
    
    con = sql.connect(db_file)
    cur = con.cursor()
    cart_data = cur.execute(f"SELECT Id, Price FROM Carts WHERE UserId = {user.id}").fetchall()[0]
    p_ids = cur.execute(f"SELECT productId, Count FROM CartProducts WHERE cartId = {cart_data[0]}").fetchall()
    
    if len(p_ids) == 0:
        return "Your cart is empty bro" 

    products = []
    for prod in p_ids:
        res = cur.execute(f"SELECT Id, Name, Description, Price FROM Products WHERE Id={prod[0]}").fetchall()
        img = cur.execute(f"SELECT url FROM ProductImages WHERE fk_ProdId = {prod[0]} LIMIT 1").fetchall()[0][0]
        products.append({"id": res[0][0], "name": res[0][1], "description": res[0][2], "price": res[0][3]*prod[1], "count": prod[1], "image": img})

    return render_template("cart_page.html", categories=categories, current_user=flask_login.current_user, products=products, total=cart_data[1])
    
@app.route('/addtocart', methods=['POST'])
def add_to_cart():
    user = flask_login.current_user
    if user.is_anonymous:
        abort(401, 'Unauthorized: Bad Authentication')
        
    product_id = request.form.get("productid")
    count = int(request.form.get("count"))
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    cart_id = cur.execute(f"SELECT Id FROM Carts WHERE UserId = {user.id}").fetchall()[0][0]
    
    res = cur.execute(f"SELECT Count FROM CartProducts WHERE CartId = {cart_id} AND ProductId = {product_id}").fetchall()
    if len(res) == 0:
        cur.execute(f"INSERT INTO CartProducts(CartId, ProductId, Count) VALUES({cart_id}, {product_id}, {count})")
    else:
        cur.execute(f"UPDATE CartProducts SET Count = Count + {count} WHERE ProductId = {product_id} AND CartId = {cart_id}")
    
    prod_price = cur.execute(f"SELECT Price FROM Products WHERE Id = {product_id}").fetchall()[0][0]
    cur.execute(f"UPDATE Carts SET Price = Price + {count * prod_price} WHERE Id = {cart_id}")
    con.commit()
    
    return "200-OK"
# DB connection tests
@app.route("/db_products")
def db_products():
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute("SELECT * FROM Products").fetchall()
    print(type(res[0]))

    style_sheet = "table {border-collapse: collapse;border-spacing: 0px;}table,th,td{padding: 5px;border: 1px solid black;}"

    html_page = f"<html> <head><style>{style_sheet}</style></head>  <body><table> <tr> <th>Id</th> <th>Name</th> <th>Price</th> <th>Stock</th></tr>"
    for item in res:
        html_page += f"<tr><td>{item[0]}</td><td>{item[1]}</td><td>{item[2]}</td><td>{item[3]}</td></tr>"
    html_page += "</table> </body></html>"
    
    con.close()


    return html_page

@app.route("/db_insert")
def db_insert():
    html_page = f"""<form action="/db_insert_submit">
        <label for="fname">Product name:</label><br>
        <input type="text" id="name" name="name" value=""><br>
        <label for="lname">Price:</label><br>
        <input type="number" id="lname" name="price" value=""><br><br>
        <label for="lname">Stock quantity:</label><br>
        <input type="number" id="stock" name="stock" value=""><br><br>
        <input type="submit" value="Submit">
    </form>"""


    return html_page

@app.route("/db_insert_submit")
def db_insert_submit():
    name = request.args.get('name')
    price = request.args.get('price')
    stock = request.args.get('stock')
    
    if name is None or price is None or stock is None:
        return "<p>There was an error processing the insert querry into the database</p>"
    
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"INSERT INTO Products(Name, Price, StockSize) VALUES(\"{name}\", {price}, {stock})").fetchall()
    con.commit()
    print(f"INSERT INTO Products(Name, Price, StockSize) VALUES(\"{name}\", {price}, {stock})")
    con.close()
    
    return f"<p>name: {name}</p> <p>price: {price}</p> <p>stock: {stock}</p>"


#login shit
class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User {self.email}>"

def get_user(email):
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"SELECT * from Users where Email = \"{email}\"").fetchall()
    if(len(res) > 0):
        return User(str(res[0][0]), res[0][1], res[0][2], res[0][3])

    return None

def create_user(username, email, password):
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"SELECT * from Users where Email = \"{email}\"").fetchall()
    if(len(res) > 0):
        return False
    res = cur.execute(f"SELECT * from Users where Name = \"{username}\"").fetchall()
    if(len(res) > 0):
        return False
    
    password = generate_password_hash(password)
    cur.execute(f"INSERT INTO Users(Name, Email, PasswordHash) VALUES (\"{username}\", \"{email}\", \"{password}\")")
    con.commit()
    con.close()

    return True
    
    
    

@login_manager.user_loader
def load_user(user_id):
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"SELECT * from Users where Id = {user_id}").fetchall()
    if(len(res) > 0):
        return User(str(res[0][0]), res[0][1], res[0][2], res[0][3])

    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", create_user=flask_login.current_user, categories=categories)
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    password = str(request.form['password'])
    user = get_user(email)
    
    if user != None and check_password_hash(user.password, password):
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("login.html", create_user=flask_login.current_user, categories=categories)
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    username = request.form['username']
    email = request.form['email']
    password = str(request.form['password'])
    
    if create_user(username, email, password):
        return "Account created successfully"
    
    
    return "The username or the email is already in use"


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.name

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('main_page'))