from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

bootstrap=Bootstrap()
db=SQLAlchemy()
moment=Moment()
ckeditor=CKEditor()
mail = Mail()
login_manager=LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    print("雨晨雨晨")
    from kkblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user



login_manager.login_view = 'auth.login'
login_manager.login_message = '无权访问后台，你需要先登录'
login_manager.login_message_category = 'warning'