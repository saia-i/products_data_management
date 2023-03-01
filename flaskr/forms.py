from flask_wtf import FlaskForm
from wtforms.fields import StringField,FloatField,TextAreaField,SelectField,RadioField,SubmitField,HiddenField,IntegerField,PasswordField
from wtforms.validators import DataRequired,NumberRange,Email,EqualTo
from wtforms import ValidationError



# 商品追加用フォーム
class AddItemForm(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    price=FloatField("price",validators=[DataRequired()])
    parent_category=SelectField("category",choices=[("","--parentCategory--")],validate_choice=False)
    child_category=SelectField("",choices=[("","--childCategory--")],validate_choice=False)
    grand_child_category=SelectField("",choices=[("","--grandChild--")],validators=[DataRequired()])
    brand=StringField("brand")
    condition=RadioField("condition",validators=[DataRequired()],choices=[(1,"Mint"),(2,"Near Mint"),(3,"Excellent"),(4,"Very Good"),(5,"Good")])
    description=TextAreaField("description")
    submit=SubmitField("Submit")
    
    def validate(self):
        if self.name.data==None or self.price.data==None or self.grand_child_category.data=="" or self.condition.data==None:
            return False
        return True
    
    
# 商品編集用フォーム
class EditItemForm(FlaskForm):
    id=HiddenField()
    name=StringField("name",validators=[DataRequired()])
    price=FloatField("price",validators=[DataRequired()])
    parent_category=SelectField("category",validate_choice=False)
    child_category=SelectField("",validate_choice=False)
    grand_child_category=SelectField("",validators=[DataRequired()])
    brand=StringField("brand")
    condition=RadioField("condition",validators=[DataRequired()],choices=[(1,"Mint"),(2,"Near Mint"),(3,"Excellent"),(4,"Very Good"),(5,"Good")],coerce=int)
    description=TextAreaField("description")
    submit=SubmitField("Submit")
    
    def validate(self):
        if self.name.data==None or self.price.data==None or self.grand_child_category.data=="" or self.condition.data==None:
            return False
        return True
    
    
# 商品検索用フォーム
class SearchItemForm(FlaskForm):
    name=StringField("item name")
    parent_category=SelectField(choices=[("","--parentCategory--")])
    child_category=SelectField(choices=[("","--childCategory--")])
    grand_child_category=SelectField(choices=[("","--grandChild--")])
    brand=StringField("brand")
    submit=SubmitField("search")
    
    
# ページ遷移用フォーム
class ToPageForm(FlaskForm):
    page=IntegerField()
    name=HiddenField()
    brand=HiddenField()
    category_path=HiddenField()
    submit=SubmitField("Go")
    

# ユーザ登録用フォーム
class RegisterUserForm(FlaskForm):
    name=StringField("name",validators=[DataRequired()])
    mail_address=StringField("mail_address",validators=[Email(message="Incorrect email format")])
    password=PasswordField("password",validators=[DataRequired()])
    confirm_password=PasswordField("confirm_password",validators=[DataRequired()])
    submit=SubmitField("submit")
    
    
# ログイン用フォーム
class LoginForm(FlaskForm):
    mail_address=StringField("mail_address",validators=[DataRequired()])
    password=PasswordField("password",validators=[DataRequired()])
    submit=SubmitField("Login")
    