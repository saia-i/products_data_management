from flaskr import db,login_manager
from flask_login import UserMixin, current_user

from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import and_, desc,or_

import logging
 
logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Item(db.Model):
    
    __tablename__="items"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),index=True)
    condition_id=db.Column(db.Integer)
    category_id=db.Column(db.Integer,db.ForeignKey("categories.category_id"))
    brand_id=db.Column(db.Integer,db.ForeignKey("brands.brand_id"),nullable=False)
    price=db.Column(db.Float)
    shipping=db.Column(db.Integer)
    description=db.Column(db.String(255))
    
    def __init__(self,name,condition_id,category_id,brand_id,price,description):
        self.name=name
        self.condition_id=condition_id
        self.category_id=category_id
        self.brand_id=brand_id
        self.price=price
        self.description=description
        
    
    def create_new_item(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
        return self.id
    
    def update_item(self,item_id):
        item=db.session.query(Item).filter(Item.id==item_id).first()
        item.name=self.name
        item.condition_id=self.condition_id
        item.brand_id=self.brand_id
        item.category_id=self.category_id
        item.price=self.price
        item.descriptioin=self.description
        db.session.commit()
        
    @classmethod
    def get_list(cls,page=1,limit_value=30):
        items= db.session.query(cls).join(
            Category,
            Category.category_id==cls.category_id
        ).outerjoin(
            Brand,
            Brand.brand_id==cls.brand_id
        ).with_entities(
            cls.id,cls.name,cls.price,Category.path,Brand.name.label("brand_name"),cls.condition_id
        ).order_by(desc(cls.id)).paginate(page=page,per_page=limit_value)
        db.session.commit()
        
        return items


    @classmethod
    def get_list(cls,item_name,category_path,brand_name,page=1,limit_value=30):
        sub_query=cls.query.filter(
            cls.name.ilike(f"%{item_name}%")
        ).subquery("sub")
        
        items_pagenation=db.session.query(sub_query).filter(
        ).join(
            Category,
            and_(
                Category.category_id==sub_query.c.category_id,
                Category.path.like(f"{category_path}%")
            )
        ).join(
            Brand,
            and_(
                Brand.brand_id==sub_query.c.brand_id,
                Brand.name.ilike(f"%{brand_name}%")
            )
        ).with_entities(
            sub_query.c.id,sub_query.c.name,sub_query.c.price,Category.path,Brand.name.label("brand_name"),sub_query.c.condition_id
        ).order_by(desc(sub_query.c.id)).paginate(page=page,per_page=limit_value)
        
        db.session.commit()
        
        return items_pagenation
        
    @classmethod
    def load_item(cls,item_id):
        return cls.query.filter(
            cls.id==item_id
        ).outerjoin(
            Category,
            Category.category_id==cls.category_id
            
        ).outerjoin(
            Brand,
            Brand.brand_id==cls.brand_id
        ).with_entities(
            cls.id,cls.name,cls.price,cls.condition_id,cls.category_id,Category.path,Brand.name.label("brand_name"),cls.description
        ).first()
        
    @classmethod
    def select_condition(cls,condition_id):
        conditions=[(1,"Mint"),(2,"Near Mint"),(3,"Excellent"),(4,"Very Good"),(5,"Good")]
        return [condition[1] for condition,i in [(1,"Mint"),(2,"Near Mint"),(3,"Excellent"),(4,"Very Good"),(5,"Good")] if i+1==condition_id]
    
    
class Category(db.Model):
    
    __tablename__="categories"
    
    category_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    path=db.Column(db.String)
    hierarchy=db.Column(db.Integer)
    
    @classmethod
    def get_parent_category(cls):
        return cls.query.filter(
            cls.hierarchy==1
        ).all()
        
    @classmethod
    def get_child_category(cls,parent_name,hierarchy):
        return cls.query.filter(
            cls.path.like(f"{parent_name}%"),
            cls.hierarchy==hierarchy
        ).all()
        
    @classmethod
    def select_category_by_id(cls, id):
        return cls.query.get(id)

    
    
class Brand(db.Model):
    
    __tablename__="brands"
    
    brand_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    
    @classmethod
    def select_brand_by_name(cls,name):
        return cls.query.filter(
            cls.name.ilike(f"%{name}%")
        ).first()
    
    
class User(db.Model,UserMixin):
    
    __tablename__="users"
    
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    mail_address=db.Column(db.String(),index=True,nullable=False)
    password=db.Column(db.String(255))
    authority=db.Column(db.Integer)
    
    def __init__(self,name,mail_address,password,authority):
        self.name=name
        self.mail_address=mail_address
        self.password=password
        self.authority=authority
    
    def create_new_user(self):
        db.session.add(self)
        db.session.commit()
        
    def password_hash(self):
        self.password = generate_password_hash(self.password).decode()
        
    @classmethod
    def select_user_by_mail_address(cls,mail_address):
        return cls.query.filter_by(mail_address=mail_address).first()
    
    def check_password(self,password):
        return check_password_hash(self.password,password)

