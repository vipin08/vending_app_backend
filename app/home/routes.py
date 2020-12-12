from app.home import blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.base.models import Order, Product, User

@blueprint.route('/index')
@login_required
def index():
    user = User.query.count()
    total_order = Order.query.count()
    refunded_order = Order.query.filter_by(is_refunded=True).count()
    data = {"user": user, "total_order": total_order, "refunded_order": refunded_order}
    print(data)
    return render_template('index.html', data=data)

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        return render_template( template )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500
