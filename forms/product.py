from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    amount = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Добавить в корзину')
