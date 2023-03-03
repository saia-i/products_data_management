from datetime import datetime

from flask import (
    Blueprint,
    abort,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from flaskr import db
from flaskr.models import Item,Brand,Category,User
from flaskr.forms import AddItemForm,EditItemForm,SearchItemForm,ToPageForm,RegisterUserForm,LoginForm
from flask_login import login_user, login_required, logout_user, current_user


bp = Blueprint("app", __name__, url_prefix="", static_folder="static")


@bp.route("/list",methods=["GET"])
def list():
    form=SearchItemForm(request.form)
    to_page_form=ToPageForm(request.form)
    items=None
    page=request.args.get("page",1,int)
    name=form.name.data=request.args.get("name","",str)
    brand=form.brand.data=request.args.get("brand","",str)
    category_path=request.args.get("category_path","",str)
    parent=category_path.split("/")[0] if category_path!="" else request.args.get("parent_category","",str)
    child=category_path.split("/")[1] if category_path!="" else request.args.get("child_category","",str)
    grand_child=category_path.split("/")[2] if category_path!="" else request.args.get("grand_child_category","",str)
    if category_path=="":
        if parent=="":
            category_path=""
        elif child=="":
            category_path=f"{parent}/"
        elif grand_child=="":
            category_path=f"{parent}/{child}/"
        else:
            category_path=f"{parent}/{child}/{grand_child}/"
        
    items=Item.get_list(name,category_path,brand,page)
    form.parent_category.choices = [(parent, parent)] if parent!="" else [("", "--parentCategory--")]
    form.child_category.choices = [(child, child)] if child!="" else [("", "--childCategory--")]
    form.grand_child_category.choices = [(grand_child, grand_child)] if grand_child!="" else [("", "--grandChild--")]
    
    next_page=url_for("app.list",name=name,category_path=category_path,brand=brand,page=items.next_num)
    prev_page=url_for("app.list",name=name,category_path=category_path,brand=brand,page=items.prev_num)
    
       
    return render_template("list.html",items=items,form=form,to_page_form=to_page_form,
                           next_page=next_page,prev_page=prev_page,category_path=category_path)


@bp.route("/detail/<int:item_id>",methods=["GET","POST"])
def detail(item_id):
    item=Item.load_item(item_id)
    return render_template("detail.html",item=item)

@bp.route("/add",methods=["GET","POST"])
@login_required
def add():
    form=AddItemForm(request.form)
    if request.method=="POST" and form.validate():
        brand_id=Brand.select_brand_by_name(form.brand.data).brand_id
        item=Item(form.name.data,form.condition.data,form.grand_child_category.data,brand_id,form.price.data,form.description.data)
        item_id=item.create_new_item()
        return redirect(url_for("app.detail",item_id=item_id))
    return render_template("add.html",form=form)

@bp.route("/edit/<int:item_id>",methods=["GET","POST"])
@login_required
def edit(item_id):
    form=EditItemForm(request.form)
    
    if request.method=="POST" and form.validate():
        brand_id=Brand.select_brand_by_name(form.brand.data).brand_id
        item=Item(form.name.data,form.condition.data,form.grand_child_category.data,brand_id,form.price.data,form.description.data)
        item.update_item(item_id)
        return redirect(url_for("app.detail",item_id=item_id))
    
    item=Item.load_item(item_id)
    # カテゴリプルダウンにカテゴリ名を入れる
    categories=item.path.split("/")
    form.parent_category.choices = [(categories[0], categories[0])]
    form.child_category.choices = [(categories[1], categories[1])]
    form.grand_child_category.choices = [(item.category_id, categories[2])]
    
    # ラジオボタンにチェックを入れる
    form.condition.default=item.condition_id
    form.process()
    
    # テキストエリアに説明文を入れる
    form.description.process_data(item.description)
    
    return render_template("edit.html",item=item,form=form)
    


@bp.route("/get_parent_category",methods=["GET","POST"])
def get_parent_category():
    result=Category.get_parent_category()
    categories=[]
    for category in result:
        detail={"id":category.category_id,"name":category.name} 
        categories.append(detail)    
    return jsonify(data=categories)


@bp.route("/get_child_category",methods=["GET","POST"])
def get_child_category():
    parent_name=request.args.get("path",type=str)
    hierarchy=request.args.get("hierarchy",type=int)
    result=Category.get_child_category(parent_name,hierarchy)
    categories=[]
    for category in result:
        detail={"id":category.category_id,"name":category.name} 
        categories.append(detail)    
    return jsonify(data=categories)


@bp.route("/register",methods=["GET","POST"])
def register():
    form=RegisterUserForm(request.form)
    if request.method=="POST" and form.validate():
        user=User(form.name.data,form.mail_address.data,form.password.data,1)
        user.password_hash()
        user.create_new_user()
        return redirect("app.login")
    return render_template("register.html",form=form)

@bp.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm(request.form)
    
    if request.method=="POST":
        user=User.select_user_by_mail_address(form.mail_address.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get("next") if request.args.get("next") else url_for("app.list")
            return redirect(next)
        else:
            flash("Email address or password is incorrect")    
    
    return render_template("login.html",form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("app.login"))