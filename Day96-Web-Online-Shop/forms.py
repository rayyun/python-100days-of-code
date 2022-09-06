from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

##WTForm
# class CreatePostForm(FlaskForm):
#     title = StringField("Blog Post Title", validators=[DataRequired()])
#     subtitle = StringField("Subtitle", validators=[DataRequired()])
#     img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
#     body = CKEditorField("Blog Content", validators=[DataRequired()])
#     submit = SubmitField("Submit Post")

# def is_equal(data):
#     message = 'Passwords must match'
#
#     def _equal(form, field):
#         if field.data != data:
#             raise ValidationError(message)

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()], render_kw={'autofocus': True})
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")



# re_password = PasswordField("Re-enter password", validators=[DataRequired()])

# def validate_re_password(self, password):
#
#     if field.data != password:


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")



class AddressForm(FlaskForm):
    name = StringField("Full Name (First and Last name)", validators=[DataRequired()], render_kw={'autofocus': True})
    street_1 = StringField("Address 1", validators=[DataRequired()])
    street_2 = StringField("Address 2", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    state = StringField("State", validators=[DataRequired()])
    zip_code = StringField("Password", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    submit = SubmitField("Use this address!")



    # name = db.Column(db.String(30), nullable=False)
    # a = db.Column(db.String(50), nullable=False)
    # street_2 = db.Column(db.String(50))
    # phone = db.Column(db.String(20), nullable=False)
    # city = db.Column(db.String(50), nullable=False)
    # state = db.Column(db.String(50), nullable=False)
    # zip_code = db.Column(db.String(20), nullable=False)


# class CommentForm(FlaskForm):
#     comment_text = CKEditorField("Comment", validators=[DataRequired()])
#     submit = SubmitField("Summit Comment")