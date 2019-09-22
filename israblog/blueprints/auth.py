__author__ = 'yuchen'
__date__ = '2019/3/5 23:32'


from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'The login page'


@auth_bp.route('/logout')
def logout():
    return 'Logout'