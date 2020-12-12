from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Float, ForeignKey, Boolean

from app import db, login_manager

from app.base.util import hash_pass

class User(db.Model, UserMixin):

    __tablename__ = 'User'

    MEMBER = 100
    ADMIN = 300

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)
    role = Column(Integer, default=100)
    orders = db.relationship('Order', backref='User', lazy=True)


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    # @cached_property
    # def permissions(self):
    #     return self.Permissions(self)

    # @cached_property
    # def provides(self):
    #     needs = [RoleNeed('authenticated'), UserNeed(self.id)]

    #     if self.is_member:
    #         needs.append(RoleNeed('member'))

    #     if self.is_admin:
    #         needs.append(RoleNeed('admin'))

    #     return needs

    # @property
    # def is_member(self):
    #     return self.role == self.MEMBER

    # @property
    # def is_admin(self):
    #     return self.role == self.ADMIN

    @classmethod
    def get_one(cls, id):

        def to_json(user):
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }

        return to_json(User.query.get(id))

    def __repr__(self):
        return str(self.username)

class Product(db.Model, UserMixin):

    __tablename__ = 'Product'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    image = Column(String, nullable=True)
    is_refundable = Column(Boolean, default=False)
    orders = db.relationship('Order', backref='Product', lazy=True)


    # def __repr__(self):
    #     return str(self.name)

    @classmethod
    def return_all(cls):
        
        def to_json(product):
            return {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'count': product.count,
                'image': product.image,
                'is_refundable': product.is_refundable
            }
        
        return {'products': [to_json(product) for product in Product.query.all()]}
    
    @classmethod
    def get_one(cls, id):

        def to_json(product):
            return {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'count': product.count,
                'image': product.image,
                'is_refundable': product.is_refundable
            }
            
        return to_json(Product.query.get(id))

class Order(db.Model):

    __tablename__ = 'Order'

    id = Column(Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),nullable=False)
    is_refunded = db.Column(Boolean, default=False)

    @classmethod
    def return_all(cls):
        
        def to_json(order):
            return {
                'id': order.id,
                'product': Product.get_one(order.product_id),
                'user': User.get_one(order.user_id),
                'refunded': order.is_refunded,
            }
        
        return {'orders': [to_json(order) for order in Order.query.all()]}


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
