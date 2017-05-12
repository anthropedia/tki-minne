from flask import redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user
from .models import User as ModelUser

from core import app


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


ModelUser.meta = {'allow_inheritance': True}


class AuthUser(UserMixin):
    user = ModelUser

    def get_id(self):
        return str(self.user.id)

    def has_role(self, role):
        return role in self.user.roles


@login_manager.user_loader
def load_user(user_id):
    auth_user = AuthUser()
    try:
        auth_user.user = ModelUser.objects.get(id=user_id)
    except ModelUser.DoesNotExist:
        return None
    return auth_user


def login(email, password):
    auth_user = AuthUser()
    try:
        auth_user.user = ModelUser.objects.get(email=email)
    except ModelUser.DoesNotExist:
        return None
    return login_user(auth_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
