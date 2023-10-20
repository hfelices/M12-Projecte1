from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, PasswordField, validators, DecimalField , TextAreaField, FileField


class ProductForm(FlaskForm):
    title = StringField(
        validators = [validators.DataRequired()]
        )
    description = TextAreaField(
        validators = [validators.DataRequired()]
        )
    photo = FileField(
        validators = [validators.DataRequired()]
        )
    price = DecimalField(
        validators = [validators.DataRequired(), validators.NumberRange(min=0, message='El precio debe ser mayor o igual a cero')]
        )
    category_id = SelectField(
        validators = [validators.InputRequired()]
        )  
    submit = SubmitField()