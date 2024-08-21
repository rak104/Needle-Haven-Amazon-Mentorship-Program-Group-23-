import functools
import os
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app, abort,jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from .db import get_db
from flask_mail import Mail, Message
from .auth import send_store_email
from datetime import datetime
import joblib
import pandas as pd
from chatbot.gpt import GPT
from stylist.STYLIST import ImageGenerator 

bp = Blueprint('blog', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

"""The following function loads the logged-in user from the database and stores it in the g object."""
"""Object can be used to store data that might be accessed by multiple functions during the request."""
'''
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        # Assuming user table does not have store_id, fetching it based on some relationship
        store = get_db().execute(
            'SELECT * FROM Store WHERE id = (SELECT store_id FROM some_user_store_relationship WHERE user_id = ?)',
            (user_id,)
        ).fetchone()

        if store:
            g.user['store_id'] = store['id']
        else:
            g.user['store_id'] = None

'''
"""The following functions fetch all products from the database and render them on the index page.  
The products are fetched by joining the Product and Store tables on the store_id column. 
I render the products on the index page using the render_template function."""    

def get_top_4():
    db = get_db()
    products = db.execute(
    '''
    SELECT * FROM Product
    ORDER BY rating DESC
    LIMIT 4
    '''
    ).fetchall()
    return products

@bp.route('/index')
def index():
    products = get_top_4()
    return render_template('index.html',products=products)  


@bp.route('/contact_us', methods=('GET', 'POST'))
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        msg = request.form['message']

        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        elif not email:
            error = 'Email is required.'
        elif not phone_number:
            error = 'Phone number is required.'
        elif not msg:
            error = 'Description is required.'

        if error is None:
            message = "Contact Us"
            message_body =  f"Name: {name}\n"+f"Store email:{email}\n"+ f"Phone_number:{phone_number}\n"+f"Message:{msg}\n"
            send_store_email(message,message_body)
            conf = "We will reply as soon as possible!!"
            flash(conf)
    return redirect(url_for('blog.index') + '#contact-form')

@bp.route('/shop')
def shop():
    return redirect(url_for('blog.category',category_name="Womenswear"))

@bp.route('/category/<string:category_name>')
def category(category_name):
    (category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores)=categorize(category_name)
    return render_template('shop.html',category_name=category_name,clothing=clothing,shoes=shoes,accessories=accessories,productsnewin = productsnewin,productstrendingnow = productstrendingnow,stores=stores)

def categorize(category_name):
    db = get_db()  # Get the database connection
    cursor = db.execute('SELECT * FROM Store')  # Execute the SQL query
    stores = cursor.fetchall()  # Fetch all the results
    if category_name == 'Womenswear':
        clothing = [
            'Dresses',
            'Tops & Blouses',
            'T-shirts & Tanks',
            'Sweaters & Cardigans',
            'Jackets & Coats',
            'Pants & Leggings',
            'Skirts',
            'Shorts',
            'Jeans',
            'Suits & Blazers',
            'Activewear',
            'Swimwear'
        ]
        shoes = ['Heels', 'Flats', 'Boots', 'Sneakers', 'Sandals']
        accessories = ['Bags', 'Belts', 'Hats', 'Jewelry', 'Scarves']
        productsnewin = db.execute(
            '''
            SELECT * FROM Product
            WHERE category = 'Womenswear'
            ORDER BY date_of_release DESC
            LIMIT 4
            '''
        ).fetchall()
        productstrendingnow = db.execute(
        '''
        SELECT * FROM Product
        WHERE category = 'Womenswear'
        ORDER BY rating DESC
        LIMIT 4
        '''
        ).fetchall()
    elif category_name == 'Menswear':
        clothing = [
                'T-Shirts & Polos', 'Shirts', 'Sweaters & Hoodies', 
                'Jackets & Coats', 'Suits & Blazers', 'Pants & Chinos', 
                'Jeans', 'Shorts', 'Activewear', 'Swimwear'
            ]
        shoes = ['Boots', 'Sneakers', 'Loafers', 'Oxfords', 'Sandals']
        accessories = ['Bags', 'Belts', 'Hats', 'Watches', 'Sunglasses']
        productsnewin = db.execute(
            '''
            SELECT * FROM Product
            WHERE category = 'Menswear'
            ORDER BY date_of_release DESC
            LIMIT 4
            '''
        ).fetchall()
        productstrendingnow = db.execute(
        '''
        SELECT * FROM Product
        WHERE category = 'Menswear'
        ORDER BY rating DESC
        LIMIT 4
        '''
        ).fetchall()
    else:
        clothing = ['Tops', 'Pants', 'Dresses', 'Outerwear', 'Swimwear']
        shoes = ['Boots', 'Sneakers', 'Loafers', 'Oxfords', 'Sandals']
        accessories = ['Hats', 'Bags', 'Scarves', 'Gloves']
        productsnewin = db.execute(
            '''
            SELECT * FROM Product
            WHERE category = 'Kidswear'
            ORDER BY date_of_release DESC
            LIMIT 4
            '''
        ).fetchall()
        productstrendingnow = db.execute(
        '''
        SELECT * FROM Product
        WHERE category = 'Kidswear'
        ORDER BY rating DESC
        LIMIT 4
        '''
        ).fetchall()
    print(productsnewin)
    return category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores

@bp.route('/shop/category/<string:category_name>/store/<string:store>/subcategory/<string:subcategory>/type/<string:type>', methods=['GET'])
def filter_products(category_name, subcategory,type,store):
    (category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores)=categorize(category_name)
    (subcategory, type , products, store) = filter(category_name,subcategory,type,store)
    return render_template('items.html', category_name=category_name, subcategory=subcategory,store = store, type = type , products=products,clothing=clothing,shoes=shoes,accessories=accessories,stores=stores)

def filter(category_name,subcategory,type,store):
    db = get_db()
    sort_option = request.args.get('sort', 'newest-first')  # Default sort option

    # Construct the base query
    if store != ':':
        query = 'SELECT * FROM Product WHERE category = ? AND store = ?'
        params = (category_name, store)
    elif type == ":":
        query = 'SELECT * FROM Product WHERE category = ? AND subcategory = ?'
        params = (category_name, subcategory)
    else:
        query = 'SELECT * FROM Product WHERE category = ? AND subcategory = ? AND type = ?'
        params = (category_name, subcategory, type)

    # Add sorting logic
    if sort_option == 'high-to-low':
        query += ' ORDER BY price DESC'
    elif sort_option == 'low-to-high':
        query += ' ORDER BY price ASC'
    elif sort_option == 'newest-first':
        query += ' ORDER BY date_of_release DESC'

    products = db.execute(query, params).fetchall()

    return subcategory, type , products, store

@bp.route('/product/<int:product_id>', methods=['GET'])
def item_details(product_id):
    (item,sizes,category) = item_fetch(product_id)
    (category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores)=categorize(category)
    return render_template('item_details.html', product_id = product_id, item = item, sizes=sizes,category_name = category_name,clothing = clothing,sheos = shoes,accessories = accessories,stores=stores)

def item_fetch(product_id):
    # Get the database connection
    db = get_db()

    # Fetch the specific product details from the database using the given product_id
    product = db.execute(
        'SELECT * FROM Product WHERE id = ?',
        (product_id,)
    ).fetchone()

    # Check if the product exists
    if product is None:
        abort(404, description="Product not found")

    # Fetch all sizes for the same product (excluding the size attribute)
    sizes = db.execute(
        '''
        SELECT DISTINCT size FROM Product 
        WHERE name = ? AND category = ? AND subcategory = ? AND type = ? AND store = ? AND color = ? AND description = ? AND price = ? AND rating = ? AND store_id = ? AND image_path = ?
        ''',
        (product['name'], product['category'], product['subcategory'], product['type'], product['store'], product['color'], product['description'], product['price'], product['rating'], product['store_id'], product['image_path'])
    ).fetchall()

    # Extract sizes into a list
    size_list = [size['size'] for size in sizes]

    # Render the template with the product details and the sizes list
    return product, size_list, product['category']


def user_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('user_id'):
            flash('User login required.')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

def store_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('store_id'):
            flash('Store login required.')
            return redirect(url_for('auth.store_login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/upload_product', methods=('GET', 'POST'))
@store_required
def upload_product():
    if request.method == 'POST':
        name = request.form['item_name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        type = request.form['type']
        color = request.form['color']
        description = request.form['description']
        price = request.form['price']
        size = request.form['size']
        store_id = session.get('store_id')
        date_of_release = datetime.now().date()  # Get the current date

        # Fetch the store's name based on the store_id from the session
        db = get_db()
        store = db.execute('SELECT name FROM Store WHERE id = ?', (store_id,)).fetchone()
        store_name = store['name'] if store else None

        # Initialize the image paths
        image_paths = [''] * 5  # Empty list for up to 5 images

        # Handle multiple image uploads
        for i in range(5):  # Assuming up to 5 images
            image = request.files.get(f'image{i + 1}')
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image.save(image_path)
                image_paths[i] = image_path

        error = None

        if not name:
            error = 'Product name is required.'
        elif not category:
            error = 'Category is required.'
        elif not subcategory:
            error = 'Subcategory is required.'
        elif not type:
            error = 'Type is required.'
        elif not color:
            error = 'Color is required.'
        elif not description:
            error = 'Description is required.'
        elif not price:
            error = 'Price is required.'
        elif not size:
            error = "Size is required."
        elif not store_name:
            error = 'Store could not be found.'
        elif not any(image_paths):  # Ensure at least one image was uploaded
            error = 'At least one image is required.'

        if error is None:
            try:
                # Insert the product along with the store's name, image paths, and date of release into the Product table
                db.execute(
                    '''INSERT INTO Product (name, category, subcategory, store, store_id, type, description, price, color, size, 
                    image_path, image_path_2, image_path_3, image_path_4, image_path_5, date_of_release) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name, category, subcategory, store_name, store_id, type, description, price, color, size, 
                    image_paths[0], image_paths[1], image_paths[2], image_paths[3], image_paths[4], date_of_release)
                )
                db.commit()

                flash('Product successfully uploaded.')
                return redirect(url_for('blog.store_home'))
            except db.IntegrityError as e:
                error = f"Product {name} already exists. Error details: {str(e)}"

    return render_template('myprofile_store.html')

"""delete product function"""  
@bp.route('/delete_product/<int:product_id>', methods=('POST',))
@store_required
def delete_product(product_id):
    db = get_db()
    store_id = session.get('store_id')

    # Ensure the product belongs to the logged-in store
    product = db.execute(
        'SELECT id FROM Product WHERE id = ? AND store_id = ?', (product_id, store_id)
    ).fetchone()

    if product is None:
        flash('Product not found or you do not have permission to delete this product.')
        return redirect(url_for('blog.index'))

    # Delete the product
    db.execute('DELETE FROM Product WHERE id = ? AND store_id = ?', (product_id, store_id))
    db.commit()

    flash('Product successfully deleted.')
    return redirect(url_for('blog.index'))


"""edit product function"""  
@bp.route('/edit_product/<int:product_id>', methods=('GET', 'POST'))
@store_required
def edit_product(product_id):
    db = get_db()
    store_id = session.get('store_id')

    # Fetch the product to be edited
    product = db.execute(
        'SELECT * FROM Product WHERE id = ? AND store_id = ?', (product_id, store_id)
    ).fetchone()

    if product is None:
        flash('Product not found or you do not have permission to edit this product.')
        return redirect(url_for('blog.index'))

    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        subcategory = request.form['subcategory']
        type = request.form['type']
        description = request.form['description']
        price = request.form['price']
        color = request.form['color']
        date_of_release = request.form['date_of_release']
        size = request.form['size']

        # Handle the uploaded image
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
        else:
            image_path = product['image_path']  # Keep the current image if none is uploaded

        error = None

        if not name:
            error = 'Product name is required.'
        elif not category:
            error = 'Category is required.'
        elif not subcategory:
            error = 'Subcategory is required.'
        elif not type:
            error = 'Brand is required.'
        elif not description:
            error = 'Description is required.'
        elif not price:
            error = 'Price is required.'
        elif not color:
            error = 'Color is required.'
        elif not date_of_release:
            error = 'Date of release is required.'
        elif not size:
            error = 'Size is required.'

        if error is None:
            try:
                # Update the product in the database
                db.execute(
                    'UPDATE Product SET name = ?, category = ?, subcategory = ?, type= ?, description = ?, price = ?, color = ?, date_of_release = ?,size = ? ,image_path = ? '
                    'WHERE id = ? AND store_id = ?',
                    (name, category, subcategory, type, description, price, color, date_of_release,size, image_path, product_id, store_id)
                )
                db.commit()
                flash('Product successfully updated.')
                return redirect(url_for('blog.index'))
            except db.IntegrityError:
                error = f"Product {name} already exists."

        flash(error)

    return render_template('edit_product.html', product=product)

@bp.route('/profile')
def profile():
    if session.get('user_id'):
        return redirect(url_for('blog.user_home'))  # Redirect to the user's profile
    elif session.get('store_id'):
        return redirect(url_for('blog.store_home'))  # Redirect to the store's profile
    else:
        return redirect(url_for('auth.login'))  # Redirect to the login page


@bp.route('/user_profile')
def user_home():
    # Ensure the user is logged in
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))

    # Query the database for the user's details
    db = get_db()
    user = db.execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()

    if user is None:
        return redirect(url_for('auth.login'))

    # Pass the user's details to the template
    return render_template('myprofile_user.html', user=user)

@bp.route('/store_profile')
def store_home():
    # Ensure the store is logged in
    store_id = session.get('store_id')
    if store_id is None:
        return redirect(url_for('auth.login'))

    # Query the database for the store's details
    db = get_db()
    store = db.execute(
        'SELECT * FROM store WHERE id = ?', (store_id,)
    ).fetchone()

    if store is None:
        return redirect(url_for('auth.login'))

    # Pass the store's details to the template
    return render_template('myprofile_store.html', store=store)

@bp.route('/change_password',methods=['GET','POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        db = get_db()
        error = None

        # Check if the passwords match
        if new_password != confirm_password:
            error = 'New passwords do not match.'

        if session.get('user_id'):
            user_id = session['user_id']
            user = db.execute(
                'SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

            # Verify if the old password is correct
            if user is None or not check_password_hash(user['password_hash'], current_password):
                error = 'Incorrect current password.'

            if error is None:
                db.execute(
                    'UPDATE user SET password_hash = ? WHERE id = ?',
                    (generate_password_hash(new_password), user_id)
                )
                db.commit()
                flash('Your password has been updated.')
            if error != None:
                flash(error)
            return redirect(url_for('blog.user_home'))

        elif session.get('store_id'):
            store_id = session['store_id']
            store = db.execute(
                'SELECT * FROM store WHERE id = ?', (store_id,)
            ).fetchone()

            # Verify if the old password is correct
            if store is None or not check_password_hash(store['password_hash'], current_password):
                error = 'Incorrect current password.'

            if error is None:
                db.execute(
                    'UPDATE store SET password_hash = ? WHERE id = ?',
                    (generate_password_hash(new_password), store_id)
                )
                db.commit()
                flash('Your password has been updated.')
            if error != None:
                flash(error)
            return redirect(url_for('blog.store_home'))

        else:
            error = 'You need to be logged in to change your password.'

        if error:
            flash(error)

    return render_template('myprofile_user.html')


@bp.route('/search/<string:page>', methods=['GET'])
def search(page):
    db = get_db()
    query = request.args.get('query', '')
    tab = request.args.get('tab', 'items')
    if page == 'items':
        category_name = request.args.get('category_name', '')
        subcategory = request.args.get('subcategory', '')
        type = request.args.get('type', '')
        store = request.args.get('store','')
        (category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores)=categorize(category_name)
        (subcategory, type , products,store) = filter(category_name,subcategory,type,store)
    elif page == 'shop':
        category_name = request.args.get('category_name', '')
        (category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores)=categorize(category_name)
    elif page == 'item_details':
        product_id = request.args.get('product_id','')
        (item,sizes,category) = item_fetch(product_id)
        (category_name,clothing,shoes,accessories,productsnewin,productstrendingnow,stores)=categorize(category)
    else:
        products_index = get_top_4()

    if not query:
        if page == 'items':
            return render_template('items.html', results=[], tab=tab, query=query, sidebar_open=True, category_name=category_name, subcategory=subcategory,store = store, type = type , products=products,clothing=clothing,shoes=shoes,accessories=accessories,stores=stores)
        elif page == 'shop':
            return render_template('shop.html',results=[], tab=tab, query=query, sidebar_open=True,category_name=category_name,clothing=clothing,shoes=shoes,accessories=accessories,productsnewin=productsnewin,productstrendingnow=productstrendingnow,stores=stores)
        elif page == 'item_details':
            return render_template('item_details.html', results=[], tab=tab, query=query, sidebar_open=True, product_id = product_id,item = item, sizes=sizes,category_name = category_name,clothing = clothing,sheos = shoes,accessories = accessories,stores=stores)
        else:
            return render_template(page+'.html', results=[], tab=tab, query=query, sidebar_open=True,products=products_index)

    if tab == 'stores':
        stores = db.execute(
            'SELECT * FROM Store WHERE name LIKE ?',
            ('%' + query + '%',)
        ).fetchall()
        if page == 'items':
            return render_template('items.html', results=stores, tab=tab, query=query, sidebar_open=True, category_name=category_name, subcategory=subcategory,store = store, type = type , products=products,clothing=clothing,shoes=shoes,accessories=accessories,stores=stores)
        elif page == 'shop':
            return render_template('shop.html',results=stores, tab=tab, query=query, sidebar_open=True,category_name=category_name,clothing=clothing,shoes=shoes,accessories=accessories,productsnewin=productsnewin,productstrendingnow=productstrendingnow,stores=stores)
        elif page == 'item_details':
            return render_template('item_details.html', results=stores, tab=tab, query=query, sidebar_open=True, product_id = product_id, item = item, sizes=sizes,category_name = category_name,clothing = clothing,sheos = shoes,accessories = accessories,stores=stores)
        else:
            return render_template(page+'.html', results=stores, tab=tab, query=query, sidebar_open=True,products=products_index)
    
    elif tab == 'items':
        items = db.execute(
            '''SELECT * FROM Product WHERE 
            name LIKE ? OR 
            category LIKE ? OR 
            subcategory LIKE ? OR 
            type LIKE ? OR 
            description LIKE ? OR 
            store LIKE ? OR
            color LIKE ?''',
            ('%' + query + '%', '%' + query + '%', '%' + query + '%',  '%' + query + '%','%' + query + '%', '%' + query + '%', '%' + query + '%')
        ).fetchall()
        if page == 'items':
            return render_template('items.html', results=items, tab=tab, query=query, sidebar_open=True, category_name=category_name, subcategory=subcategory,store = store, type = type , products=products,clothing=clothing,shoes=shoes,accessories=accessories,stores=stores)
        elif page == 'shop':
            return render_template('shop.html',results=items, tab=tab, query=query, sidebar_open=True,category_name=category_name,clothing=clothing,shoes=shoes,accessories=accessories,productsnewin=productsnewin,productstrendingnow=productstrendingnow,stores=stores)
        elif page == 'item_details':
            return render_template('item_details.html', results=items, tab=tab, query=query, sidebar_open=True, product_id = product_id,item = item, sizes=sizes,category_name = category_name,clothing = clothing,sheos = shoes,accessories = accessories,stores=stores)
        else:
            return render_template(page+'.html', results=items, tab=tab, query=query, sidebar_open=True,products=products_index)

    if page == 'items':
        return render_template('items.html',results=[], tab=tab, query=query, sidebar_open=True, category_name=category_name, subcategory=subcategory,store = store, type = type , products=products,clothing=clothing,shoes=shoes,accessories=accessories,stores=stores)
    elif page == 'shop':
        return render_template('shop.html',results=[], tab=tab, query=query, sidebar_open=True,category_name=category_name,clothing=clothing,shoes=shoes,accessories=accessories,productsnewin=productsnewin,productstrendingnow=productstrendingnow,stores=stores)
    elif page == 'item_details':
        return render_template('item_details.html', results=[], tab=tab, query=query, sidebar_open=True, product_id = product_id, item = item, sizes=sizes,category_name = category_name,clothing = clothing,sheos = shoes,accessories = accessories,stores=stores)
    else:
        return render_template(page+'.html', results=[], tab=tab, query=query, sidebar_open=True,products=products_index)


@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    
    if 'cart' not in session:
        session['cart'] = []
    
    session['cart'].append(product_id)
    session.modified = True  # Mark the session as modified to save changes
    return redirect(url_for('blog.item_details', product_id=product_id))

def get_cart_items():
    cart_items = []
    db = get_db()
    if 'cart' in session:
        product_ids = session['cart']
        for product_id in product_ids:
            product = db.execute('SELECT * FROM Product WHERE id = ?', (product_id,)).fetchone()
            if product:
                cart_items.append(product)
    
    return cart_items

@bp.route('/view_cart', methods=['GET'])
def view_cart():
    cart_items = get_cart_items()  # Fetch all items in the cart
    subtotal = sum(item['price'] for item in cart_items) 
    return render_template('shopping_bag.html', cart_items=cart_items,subtotal=subtotal)

@bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    item_id = request.form['item_id']
    
    # Assuming 'cart' is a list of item ids in the session
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if str(item) != str(item_id)]
        session.modified = True  # Ensure the session is saved

    return redirect(url_for('blog.view_cart'))  # Redirect back to the cart view


@bp.route('/proceed_to_buy', methods=['POST'])
@user_required
def proceed_to_buy():
    cart_items = get_cart_items()  # Fetch all items in the cart
    subtotal = sum(item['price'] for item in cart_items) 
    return render_template('checkout.html',subtotal=subtotal)

def send_emails_to_stores(products):
    db = get_db()
    for product in products:
        store_name = product['store']
        store_email = db.execute('SELECT email FROM Store WHERE name = ?', (store_name,)).fetchone()
        store_email = store_email[0]
        product_details = f"Product: {product['name']}\nPrice: ${product['price']}\nSize: {product['size']}"

        with current_app.app_context():
            msg = Message("Order Placement",recipients=[store_email])
            msg.body = f"Product Details: {product_details}"
            mail = Mail(current_app)  # Ensure mail is configured properly in your app
            mail.send(msg)

@bp.route('/process_order', methods=['POST'])
def process_order():
    # Retrieve form data
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    address = request.form.get('address')
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    country = request.form.get('country')
    phone = request.form.get('phone')
    email = request.form.get('email')

    user_id = session.get('user_id')
    # Retrieve cart items from session
    cart_items = get_cart_items()  # Assume you have a function to get cart items
    subtotal = sum(item['price'] for item in cart_items) 
    total = subtotal + 3
    # Process the order (e.g., save it to the database)
    db = get_db()
    order_id = db.execute(
        'INSERT INTO Orders (user_id,first_name, last_name, address, city, state, zip_code, country, phone, email, total_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (user_id,first_name, last_name, address, city, state, zip_code, country, phone, email,total)
    ).lastrowid
    
    for item in cart_items:
        db.execute(
            'INSERT INTO OrderItems (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
            (order_id, item['id'], 1, item['price'])  # Adjust quantity as needed
        )

    db.commit()

    send_emails_to_stores(cart_items)

    # Clear the cart
    session.pop('cart', None)

    # Redirect to a confirmation page or display a success message
    flash('Your order has been successfully placed!')
    return render_template('checkout.html',subtotal = 0)


@bp.route('/personalized_stylist')
def personalized_stylist():
    return render_template('personalized_stylist.html')

@bp.route('/fashion_expert')
def fashion_expert():
    return render_template('fashion_expert.html')

@bp.route('/product_finder')
def product_finder():
    return render_template('product_finder.html')

@bp.route('/virtual_model')
def virtual_model():
    return render_template('virtual_model.html')

@bp.route('/price_predict', methods=['POST'])
def price_predict():
    data = request.form
    brand = data.get('brand')
    category = data.get('category')
    color = data.get('color')
    size = data.get('size')
    material = data.get('material')

    # Load the model
    
    model_path = '/home/rawad/Documents/Amazon/Needle-Haven/main_models_classes/clothes_price_pred/clothes_price_predprice_prediction_model.pkl'
    model = joblib.load(model_path)

    # Create the input data
    input_data = {
        'Brand': [brand],
        'Category': [category],
        'Color': [color],
        'Size': [size],
        'Material': [material]
    }

    # Predict price
    predicted_price = model.predict(pd.DataFrame(input_data))

    return jsonify({'predicted_price': predicted_price[0]})


@bp.route('/average_rating_predict', methods=['POST'])
def average_rating_predict():
    data = request.form
    product_name = data.get('product_name')
    gender = data.get('gender')
    category = data.get('category')
    color = data.get('color')
    age_group = data.get('age_group')
    season = data.get('season')
    price = data.get('price')
    material = data.get('material')
    sales_count = data.get('sales_count')
    brand = data.get('brand')
    discount = data.get('discount')

    # Load the model
    model_path = '/home/rawad/Documents/Amazon/Needle-Haven/main_models_classes/rating/average_rating_prediction_model.pkl'
    model = joblib.load(model_path)

    # Create the input data
    input_data = {
        'product_name': [product_name],
        'gender': [gender],
        'category': [category],
        'color': [color],
        'age_group': [age_group],
        'season': [season],
        'price': [price],
        'material': [material],
        'sales_count': [sales_count],
        'brand': [brand],
        'discount': [discount]
    }

    # Predict average rating
    predicted_rating = model.predict(pd.DataFrame(input_data))

    return jsonify({'predicted_rating': predicted_rating[0]})


@bp.route('/eps_predict', methods=['POST'])
def eps_predict():
    data = request.form
    cagr_net_income = float(data.get('cagr_net_income'))
    cagr_revenues = float(data.get('cagr_revenues'))

    # Load the model
    model_path = '/home/rawad/Documents/Amazon/Needle-Haven/main_models_classes/eps/growth_prediction_model.pkl'
    model = joblib.load(model_path)

    # Create the input data
    input_data = {
        'CAGR_Net_Income_5Y': [cagr_net_income],
        'CAGR_Revenues_5Y': [cagr_revenues]
    }

    # Predict EPS
    predicted_eps = model.predict(pd.DataFrame(input_data))

    return jsonify({'predicted_eps': predicted_eps[0]})


@bp.route('/size_predict', methods=['POST'])
def size_predict():
    data = request.form
    weight = float(data.get('weight'))
    age = float(data.get('age'))
    height = float(data.get('height'))

    # Load the model and label encoder
    model_path = '/home/rawad/Documents/Amazon/Needle-Haven/main_models_classes/size/size_prediction_model.pkl'
    label_encoder_path ='/home/rawad/Documents/Amazon/Needle-Haven/main_models_classes/size/size_label_encoder.pkl'
    model = joblib.load(model_path)
    label_encoder = joblib.load(label_encoder_path)

    # Create the input data
    input_data = {
        'weight': [weight],
        'age': [age],
        'height': [height]
    }

    # Predict size (encoded) and decode it
    predicted_size_encoded = model.predict(pd.DataFrame(input_data))
    predicted_size = label_encoder.inverse_transform(predicted_size_encoded)

    return jsonify({'predicted_size': predicted_size[0]})



#personlized stylist 
@bp.route('/gpt_ask', methods=['POST'])
def gpt_ask():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Initialize GPT instance and get response
    gpt_instance = GPT()
    response = gpt_instance.general_search(user_message)
    
    return jsonify({'response': response}) 

#fashion expert 
@bp.route('/gpt_wiki', methods=['POST']) 
def gpt_wiki():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Initialize GPT instance and get response
    gpt_instance = GPT()
    response = gpt_instance.wiki_search(user_message)
    
    return jsonify({'response': response})  

#database 
@bp.route('/gpt_stores', methods=['POST']) 
def gpt_stores():
    data = request.get_json()
    user_message = data.get('message', '')
    
    # Initialize GPT instance and get response
    gpt_instance = GPT()
    response = gpt_instance.stores_search(user_message)
    
    return jsonify({'response': response})   

@bp.route('/virtual_stylist', methods=['POST'])
def virtual_stylist():
    data = request.form  # Get form data
    model_type = data.get('model')
    size = data.get('size')
    image = request.files['image']
    image_path = os.path.join('path/to/save/uploads', image.filename)
    image.save(image_path)  # Save the uploaded image
    generator = ImageGenerator(region_name="us-east-1", model_id="amazon.titan-image-generator-v2:0")
    generated_image_path = os.path.join('path/to/save/generated/images', f'generated_{image.filename}')
    generator.generate_image(
        model=model_type,
        item="clothing",
        image_path=image_path,  # Use the path to the uploaded image
        size=size
    )

    # Return the path to the generated image as a response
    return jsonify({'generated_image_path': generated_image_path})

