from flask import Blueprint, render_template, redirect, request, session

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, hash_password

from flask_security.models import fsqla_v3 as fsqla

from flask_login import current_user

dashapp1_bp = Blueprint('dashapp1_bp', __name__)

'''
@dashapp1_bp.before_request
def check_route_access():
    if request.endpoint is None:
        return redirect("/login")
 
    func = @dashapp1_bp.view_functions[request.endpoint]
    if (getattr(func, "is_public", False)):
        return  # Access granted

    # check if user is logged in (using session variable)
    user = session.get("user", None)
    if not user:
        redirect("/login")
    else:
        return  # Access granted```

def public_route(function):
    function.is_public = True
    return function
'''

@dashapp1_bp.route('/app/dashapp0')
def dashapp0():
    return redirect('/app/wsgi_app0', code=302)

@dashapp1_bp.route('/app/dashapp1')
def dashapp1():
    return redirect('/app/wsgi_app1', code=302)

@dashapp1_bp.route('/app/dashapp2')
@auth_required()
def dashapp2():
    return redirect('/app/wsgi_app2', code=302)

@dashapp1_bp.route('/app/session_app1')
def dashapp3():
    return redirect('/session_app', code=302)
