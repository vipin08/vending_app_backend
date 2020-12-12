from flask import jsonify, render_template, redirect, request, url_for, flash
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.base import blueprint
from app.base.forms import LoginForm, CreateAccountForm, ProductForm
from app.base.models import User, Product, Order

from app.base.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))

## Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        
        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()
        
        # Check the password
        if user and verify_pass( password, user.password) and user.role == 300:

            login_user(user)
            return redirect(url_for('base_blueprint.route_default'))

        # Something (user or pass) is not ok
        return render_template( 'accounts/login.html', msg='Wrong user or password', form=login_form)

    if not current_user.is_authenticated:
        return render_template( 'accounts/login.html',
                                form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    login_form = LoginForm(request.form)
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username  = request.form['username']
        email     = request.form['email'   ]

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Username already registered',
                                    success=False,
                                    form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template( 'accounts/register.html', 
                                    msg='Email already registered', 
                                    success=False,
                                    form=create_account_form)

        # else we can create the user
        user = User(**request.form)
        db.session.add(user)
        db.session.commit()

        return render_template( 'accounts/register.html', 
                                msg='User created please <a href="/login">login</a>', 
                                success=True,
                                form=create_account_form)

    else:
        return render_template( 'accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))

@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

@blueprint.route('/products')
@login_required
def products_list():
    products = Product.query.all()
    print(list(products))
    return render_template( 'products/list.html', 
                                msg='List', 
                                success=True,
                                products=list(products))


@blueprint.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """
    Add a Product to the database
    """
    # check_admin()

    add_product = True

    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data,
                                price=form.price.data,
                                count=form.count.data,
                                image=form.image.data
                                )
        try:
            # add product to the database
            db.session.add(product)
            db.session.commit()
            flash('You have successfully added a new product.')
        except:
            # in case product name already exists
            flash('Error: product name already exists.')

        # redirect to product page
        return redirect(url_for('base_blueprint.products_list'))

    # load department template
    return render_template('products/add.html', action="Add",
                           add_product=add_product, form=form,
                           title="Add Product")


@blueprint.route('/product/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """
    Edit a Product
    """
    # check_admin()

    add_product = False

    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        product.name=form.name.data
        product.price=form.price.data
        product.count=form.count.data
        product.image=form.image.data
        db.session.commit()
        flash('You have successfully edited the Product.')

        # redirect to the departments page
        return redirect(url_for('base_blueprint.products_list'))

    form.name.data = product.name
    form.price.data = product.price
    form.count.data = product.count
    form.image.data = product.image

    return render_template('products/edit.html', action="Edit",
                           add_product=add_product, form=form,
                           product=product, title="Edit Product")


@blueprint.route('/products/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    """
    Delete a Product from the database
    """
    # check_admin()

    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('You have successfully deleted the product.')

    # redirect to the products page
    return redirect(url_for('base_blueprint.products_list'))

    return render_template(title="Delete Product")


@blueprint.route('/orders/', methods=['GET'])
@login_required
def order_list():
    """
    List a Product from the database
    """
    # check_admin()

    orders = Order.return_all()

    if not orders.get('orders'):
        orders = []
    # redirect to the orders page
    return render_template( 'orders/list.html', 
                                msg='Orders', 
                                success=True,
                                orders=orders)

## Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('page-403.html'), 403

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500
