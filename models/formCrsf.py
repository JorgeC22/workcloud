import imp
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField


class formProtectionCsrf(FlaskForm):
    notificacion = HiddenField(default="true")