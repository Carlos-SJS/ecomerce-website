from flask import Flask, request, redirect, url_for, render_template, abort
from flask_login import LoginManager, UserMixin
import flask_login
import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash, safe_join
import os

categories = []
db_file = "gennady_store.db"

def load_data():
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute("SELECT Categoria FROM Categoria GROUP BY Categoria").fetchall()
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
    return render_template("basic_page.html", title="Gennady.Store", main_message="Bienvenido a Gennady.Store", secondary_message="La mejor tienda para los verdaderos ICPCerdos")
@app.route("/products")
def products_page():
    con = sql.connect(db_file)
    cur = con.cursor()
    
    f_category = ""
    if "Category" in request.args:
        for cat in request.args.getlist("Category"):            
            f_category += (" AND " if f_category != "" else "") + f"ID IN (SELECT ID_Producto FROM Categoria WHERE Categoria = \"{cat}\" COLLATE NOCASE)"
    
    f_search = ""
    if "Search" in request.args: 
        search_q = request.args.get("Search")
        f_search = f"((Nombre LIKE \"%{search_q}%\" COLLATE NOCASE) OR (Descripcion LIKE \"%{search_q}%\" COLLATE NOCASE))"
    f_category = "" if f_category == "" else f"({f_category})"
    
    filter_joined = ""
    if f_category != "" or f_search != "":
        join_str = " AND " if f_category != "" and f_search != "" else ""
        filter_joined = " WHERE " + f_search + join_str + f_category + ";"
    
    res = cur.execute("SELECT Nombre, Precio, Descripcion, ID FROM Producto"+filter_joined).fetchall()
    
    products = []
    #res = cur.execute("SELECT Name, Price, Description, ProductId FROM Products").fetchall()
    for prod in res:
        products.append({"Name": prod[0], "Price": prod[1], "Description": prod[2],"Images": [], "pId": prod[3]})
        
        imgs = cur.execute(f"SELECT Imagen FROM Imagenes_Producto WHERE ID_Producto = {prod[3]}")
        for img in imgs:
            products[-1]["Images"].append(img[0])
        
    con.close()

    return render_template("products.html", title="Products - Mamazon", products=products, categories=categories, current_user=flask_login.current_user)

@app.route("/product")
def product_page():
    product_id = request.args["id"]
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    res = cur.execute(f"SELECT Nombre, Precio, Descripcion, Stock, Descripcion_Larga, Vendedor FROM Producto WHERE ID = {product_id}").fetchall()
    
    if len(res) == 0:
        return "Didint work little bro"
    
    user = flask_login.current_user
    res_img = cur.execute(f"SELECT Imagen FROM Imagenes_Producto WHERE ID_Producto = {product_id}").fetchall()
    product_data = {"Name": res[0][0], "Price": res[0][1], "Description": res[0][2], "Full_Description": res[0][4], "Seller": res[0][5], "Stock": res[0][3], "Images":[]}
    
    if not user.is_anonymous:
        cart_id = cur.execute(f"SELECT ID FROM Carrito WHERE Usuario = {user.id}").fetchall()[0][0]
        count_in_cart = cur.execute(f"SELECT Count FROM Lista_Productos_Carrito WHERE ID_Producto = {product_id} AND ID_Carrito = {cart_id}").fetchall()
        if len(count_in_cart) > 0:
            product_data["CartMax"]=product_data["Stock"]-count_in_cart[0][0]
        else:
            product_data["CartMax"]=product_data["Stock"]   

    for img in res_img:
        product_data["Images"].append(img[0])
    
    con.close()
    
    return render_template("product_page.html", categories=categories, current_user=flask_login.current_user, p_data= product_data)

@app.route("/mycart")
def cart_page():
    user = flask_login.current_user
    if user.is_anonymous:
        return render_template("basic_page.html", title="Mi carrito", main_message="<You must be loged in to acces this page")
    
    
    con = sql.connect(db_file)
    cur = con.cursor()
    cart_data = cur.execute(f"SELECT ID, Total FROM Carrito WHERE Usuario = {user.id}").fetchall()[0]
    p_ids = cur.execute(f"SELECT ID_Producto, Count FROM Lista_Productos_Carrito WHERE ID_Carrito = {cart_data[0]}").fetchall()
    
    if len(p_ids) == 0:
        return render_template("basic_page.html", title="Mi carrito", main_message="Tu carrito esta vacio!", secondary_message="Visita la página de productos para llenar tu carrito")

    products = []
    for prod in p_ids:
        res = cur.execute(f"SELECT ID, Nombre, Descripcion, Precio FROM Producto WHERE ID={prod[0]}").fetchall()
        img = cur.execute(f"SELECT Imagen FROM Imagenes_Producto WHERE ID_Producto = {prod[0]} LIMIT 1").fetchall()[0][0]
        products.append({"id": res[0][0], "name": res[0][1], "description": res[0][2], "price": res[0][3]*prod[1], "count": prod[1], "image": img})

    return render_template("cart_page.html", categories=categories, current_user=flask_login.current_user, products=products, total=cart_data[1])

@app.route("/my_orders")
@flask_login.login_required
def orders_page():
    user = flask_login.current_user   
    
    con = sql.connect(db_file)
    cur = con.cursor()
    orders_data = cur.execute(f"SELECT ID, Total FROM Ordenes WHERE Usuario = {user.id}").fetchall()
    
    orders = []
    for order in orders_data:
        prods = cur.execute(f"Select ID_Producto, Count FROM Lista_Productos_Orden WHERE ID_Orden = {order[0]}").fetchall()
        order_d = {"price": order[1], "products": []}
        for p in prods:
            p_dat = cur.execute(f"SELECT Nombre, Precio FROM Producto WHERE ID = {p[0]}").fetchall()[0]
            img = cur.execute(f"SELECT Imagen FROM Imagenes_Producto WHERE ID_Producto = {p[0]}").fetchall()[0][0]
            prod = {"count": p[1], "image": img, "name": p_dat[0], "price": p_dat[1]*p[1], "id": p[0]}
            
            order_d["products"].append(prod)
        orders.append(order_d)
        print(order_d["products"])

    return render_template("orders_page.html", categories=categories, current_user=flask_login.current_user, orders=orders)
    
@app.route("/seller")
@flask_login.login_required
def seller_page():
    user = flask_login.current_user
    if not user.is_seller:
        return "Bad auth"
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    res = cur.execute(f"SELECT Nombre, Precio, Descripcion, ID FROM Producto WHERE Vendedor = {user.seller_id}").fetchall()
    
    products = []
    #res = cur.execute("SELECT Name, Price, Description, ProductId FROM Products").fetchall()
    for prod in res:
        products.append({"Name": prod[0], "Price": prod[1], "Description": prod[2],"Images": [], "pId": prod[3]})
        
        imgs = cur.execute(f"SELECT Imagen FROM Imagenes_Producto WHERE ID_Producto = {prod[3]}")
        for img in imgs:
            products[-1]["Images"].append(img[0])
        
    con.close()

    return render_template("products.html", title="Products - Mamazon", products=products, categories=categories, current_user=flask_login.current_user)    

@app.route('/addtocart', methods=['POST'])
def add_to_cart():
    user = flask_login.current_user
    if user.is_anonymous:
        abort(401, 'Unauthorized: Bad Authentication')
        
    product_id = request.form.get("productid")
    count = int(request.form.get("count"))
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    cart_id = cur.execute(f"SELECT ID FROM Carrito WHERE Usuario = {user.id}").fetchall()[0][0]
    prod_data = cur.execute(f"SELECT Precio, Stock FROM Producto WHERE ID = {product_id}").fetchall()
    
    res = cur.execute(f"SELECT Count FROM Lista_Productos_Carrito WHERE ID_Carrito = {cart_id} AND ID_Producto = {product_id}").fetchall()
    if len(res) == 0:
        count = min(count, prod_data[0][1])
        cur.execute(f"INSERT INTO Lista_Productos_Carrito(ID_Carrito, ID_Producto, Count) VALUES({cart_id}, {product_id}, {count})")
    else:
        count = min(count, prod_data[0][1] - cur.execute(f"SELECT Count FROM Lista_Productos_Carrito WHERE ID_Producto = {product_id} AND ID_Carrito = {cart_id}").fetchall()[0][0])
        cur.execute(f"UPDATE Lista_Productos_Carrito SET Count = Count + {count} WHERE ID_Producto = {product_id} AND ID_Carrito = {cart_id}")
    
    prod_price = prod_data[0][0]
    cur.execute(f"UPDATE Carrito SET Total = Total + {count * prod_price} WHERE ID = {cart_id}")
    con.commit()
    
    return "200-OK"

@app.route('/upload_image', methods=['POST'])
@flask_login.login_required
def upload_image():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = os.path.join("static/uploads", file.filename)
        file.save(filename)
        return 'File uploaded successfully'

@app.route("/create_product", methods=['GET', 'POST'])
@flask_login.login_required
def create_product():
    user = flask_login.current_user
    if not user.is_seller:
        return "You do not have permission to be here kido"
    
    if request.method == 'GET':
        return render_template("add_product.html" )
    
    p_name = request.form.get('name')
    p_sdesc = request.form.get('short_desc')
    p_fdesc = request.form.get('full_desc')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))
    images = request.form.getlist('image')
    
    con = sql.connect(db_file)
    cur = con.cursor()
    
    cur.execute(f"INSERT INTO Producto(Nombre, Precio, Descripcion, Descripcion_Larga, Stock, Vendedor, Cantidad_Vendida) VALUES (\"{p_name}\", {price}, \"{p_sdesc}\", \"{p_fdesc}\", {stock}, {user.seller_id}, {0})")
    new_pid =  cur.execute("SELECT last_insert_rowid()").fetchall()[0][0]

    for img in images:
        cur.execute(f"INSERT INTO Imagenes_Producto(ID_Producto, Imagen) VALUES ({new_pid}, \"{img}\")")
    
    con.commit()
    con.close()
    
    return "200-OK"
    
# DB connection tests
@app.route("/db_products")
def db_products():
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute("SELECT * FROM Producto").fetchall()
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
    def __init__(self, id, name, email, password, is_seller = False, seller_id = None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_seller = is_seller
        self.seller_id = seller_id
        
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<User {self.email}>"

def get_user(email):
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"SELECT * from Usuario where Email = \"{email}\"").fetchall()
    s_res = cur.execute(f"SELECT ID FROM Vendedor WHERE ID_Usuario = {res[0][0]}").fetchall()
    print(s_res)
    if(len(res) > 0):
        if(len(s_res) == 0):
            return User(str(res[0][0]), res[0][1], res[0][2], res[0][3])
        else:
            return User(str(res[0][0]), res[0][1], res[0][2], res[0][3], is_seller=True, seller_id=s_res[0][0])

    return None

def create_user(username, email, password):
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"SELECT * from Usuario where Email = \"{email}\"").fetchall()
    if(len(res) > 0):
        return False
    res = cur.execute(f"SELECT * from Usuario where Nombre = \"{username}\"").fetchall()
    if(len(res) > 0):
        return False
    
    password = generate_password_hash(password)
    cur.execute(f"INSERT INTO Usuario(Nombre, Email, Password) VALUES (\"{username}\", \"{email}\", \"{password}\")")
    new_id = cur.execute(f"SELECT ID from Usuario where Nombre = \"{username}\"").fetchall()[0][0]
    cur.execute(f"INSERT INTO Carrito(Usuario, Total) VALUES({new_id}, {0})")
    con.commit()
    con.close()

    return True

@login_manager.user_loader
def load_user(user_id):
    con = sql.connect(db_file)
    cur = con.cursor()

    res = cur.execute(f"SELECT * from Usuario where ID = \"{user_id}\"").fetchall()
    s_res = cur.execute(f"SELECT ID FROM Vendedor WHERE ID_Usuario = {res[0][0]}").fetchall()
    print(s_res)
    if(len(res) > 0):
        if(len(s_res) == 0):
            return User(str(res[0][0]), res[0][1], res[0][2], res[0][3])
        else:
            return User(str(res[0][0]), res[0][1], res[0][2], res[0][3], is_seller=True, seller_id=s_res[0][0])

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