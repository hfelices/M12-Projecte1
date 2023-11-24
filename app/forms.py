from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SubmitField, SelectField, PasswordField, validators, DecimalField , TextAreaField, FileField , HiddenField


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
    seller_id = HiddenField(
        validators = [validators.InputRequired()]
        )  
    submit = SubmitField()
    

class CreateUserForm(FlaskForm):
    name = StringField(
        validators = [validators.DataRequired()]
        )
    email = EmailField (
        validators = [validators.DataRequired()]
        )
    password = PasswordField(
        validators = [validators.DataRequired()]
        )
    passConfirmation = PasswordField(
        validators = [validators.DataRequired()]
        )


class LoginForm(FlaskForm):
    name = StringField(
        validators = [validators.DataRequired()]
        )
    password = PasswordField(
        validators = [validators.DataRequired()]
        )
    
class ProfileForm(FlaskForm):
    name = StringField(
        validators = [validators.DataRequired()]
        )
    email = StringField(
        validators = [validators.DataRequired()]
        )
    password = PasswordField(
        "cambiar contraseña"
        )

    
class ResendForm(FlaskForm):
    email = EmailField(
        validators = [validators.DataRequired()]
        )
    password = PasswordField(
        validators = [validators.DataRequired()]
        
        )
   

class DeleteProductForm(FlaskForm):
    submit = SubmitField()