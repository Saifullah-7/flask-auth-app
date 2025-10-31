from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    IntegerField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    EqualTo,
    Optional,
    NumberRange,
)


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password"),
        ],
    )
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=13)])
    accept_terms = BooleanField("Terms", validators=[DataRequired()])
    submit = SubmitField("SignUp")
