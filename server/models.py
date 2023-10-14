from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, name, author_name):
        if ((not author_name) or (author_name in name)):
            raise ValueError("Author must have a unique name.")
        return author_name

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        if (len(number) != 10):
            raise ValueError('Failed phone number validation')
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content):
        if (len(content) <= 250):
            raise ValueError("Post content must be 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if (len(summary) > 250):
            raise ValueError("Post summary must not exceed 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if ((category != 'Fiction') and (category != 'Non-Fiction')):
            raise ValueError(
                "Post must be of either Fiction or Non-Fiction category.")
        return category

    @validates('title')
    def validates_title(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        title_split = title.split(" ")
        clickbait_flag = False
        for word in title_split:
            if (word in clickbait):
                clickbait_flag = True
        if (clickbait_flag):
            return title
        else:
            raise ValueError('Title not clickbait-y enough!')

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
