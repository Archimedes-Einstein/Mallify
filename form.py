from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,TextAreaField,IntegerField
from flask_ckeditor import CKEditorField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
     message=CKEditorField('MESSAGE',[DataRequired()],render_kw={'class':'fs-6 fw-bold'})
     submit=SubmitField('Send!',render_kw={'class':'rounded-0 btn-lg btn-dark'})
     
class ProductReviewForm(FlaskForm):
     user_name = StringField('User Name',[DataRequired()])
     product_name = StringField('Product Name',[DataRequired()])
     review = TextAreaField('Review',   [DataRequired()])
     rating = IntegerField('Rating: 0 - 5',[DataRequired()])
     submit = SubmitField('Send!',render_kw={'class':'rounded-0 btn-lg btn-dark'})