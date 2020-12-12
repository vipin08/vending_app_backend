from flask import jsonify, render_template, redirect, request, url_for, flash, make_response
# from flask_marshmallow import Marshmallow


from app import db, login_manager
from app.api.v1 import blueprint
from app.base.forms import LoginForm, CreateAccountForm, ProductForm
from app.base.models import User, Product, Order

from app.base.util import verify_pass


@blueprint.route('/api/<version>/products')
def products(version):
    """
        return all products api
    """
    print(Product.query.first().orders)
    return Product.return_all() 

@blueprint.route('/api/<version>/products/<int:id>/buy', methods=['PUT'])
def products_edit(version, id):
    """
        Buy product API
        Create dummy User who make order
    """
    data = request.get_json(force=True)

    user = User.query.filter_by(username=data['user_name']).first()

    product = Product.query.get_or_404(id)
    if product is not None and data is not None:
        if not user:
            # create dummy user
            user = User(username=data['user_name'], password='pass', email=data['user_name']+"@gmail.com")
            db.session.add(user)
            db.session.commit()
        order = Order(product_id=product.id, user_id=user.id)
        db.session.add(order)
        product.count = product.count - 1
        db.session.commit()
        return {"status": "true", "id": product.id, "price": product.price, "count": product.count}
    return {"status": "false"}

@blueprint.route('/api/<version>/products/<int:id>/refund', methods=['PUT'])
def products_refund(version, id):
    """
        Refund Product API
    """
    data = request.get_json(force=True)
    product = Product.query.get_or_404(id)

    if not product.is_refundable:
        return {"status": "false", "message": "product not eligible for refund"}

    if product is not None and data is not None:
        user = User.query.filter_by(username=data['user_name']).first()
        order = Order.query.filter_by(user_id=user.id, product_id=product.id, is_refunded=False).first()
        if not order:
            return {"status": "false", "message": "invalid order"}

        if not order.is_refunded:
            order.is_refunded = True
            # db.session.delete(order)
            product.count = product.count + 1
            db.session.commit()
            return {"status": "true", "id": product.id, "price": product.price, "count": product.count}
        elif order.is_refunded:
            return {"status": "false", "message": "order already refunded"}
        else:
            return {"status": "false", "message": "invalid order"}
    return {"status": "false", "message": "invalid request"}

@blueprint.route('/api/<version>/users/<int:id>/add_balance', methods=['PUT'])
def add_balance(version, id):
    """
        Add balance Product API
    """
    data = request.get_json(force=True)
    user = User.query.get_or_404(id)

    if not user.role != 100:
        return {"status": "false", "message": "invalid user"}

    if user is not None and data is not None:
            return {"status": "true", "id": product.id, "price": product.price, "count": product.count}

    return {"status": "false", "message": "invalid request"}



