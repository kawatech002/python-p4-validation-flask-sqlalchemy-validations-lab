from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
   __tablename__ = 'authors'

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String, unique=True, nullable=False)
   phone_number = db.Column(db.String)
   created_at = db.Column(db.DateTime, server_default=db.func.now())
   updated_at = db.Column(db.DateTime, onupdate=db.func.now())

   @validates('name')
   def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name")
        existing_author = Author.query.filter(db.func.lower(Author.name) == db.func.lower(name)).first()
        if existing_author:
            raise ValueError("Author name must be unique")
        return name

   @validates('phone_number')
   def validate_phone_number(self, key, phone_number):
       if phone_number and (not phone_number.isdigit() or len(phone_number) != 10):
           raise ValueError("Phone number must be 10 digits")
       return phone_number

   def __repr__(self):
       return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
   __tablename__ = 'posts'

   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String, nullable=False)
   content = db.Column(db.String)
   category = db.Column(db.String)
   summary = db.Column(db.String)
   created_at = db.Column(db.DateTime, server_default=db.func.now())
   updated_at = db.Column(db.DateTime, onupdate=db.func.now())

   @validates('title')
   def validate_title(self, key, title):
    if not title:
        raise ValueError("Post must have a title")
    clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
    if not any(word in title for word in clickbait_words):
        raise ValueError("Post title must be clickbait-y")
    return title


   @validates('content')
   def validate_content(self, key, content):
        if content is not None and len(content) < 250:
            raise ValueError("Post content must be at least 250 characters")
        return content

   @validates('summary')
   def validate_summary(self, key, summary):
        if summary is not None and len(summary) > 250:
            raise ValueError("Post summary must be 250 characters or less")
        return summary

   @validates('category')
   def validate_category(self, key, category):
    allowed_categories = ['Fiction', 'Non-Fiction']
    if category not in allowed_categories:
        raise ValueError("Invalid category")
    return category

   
   def __repr__(self):
       return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'