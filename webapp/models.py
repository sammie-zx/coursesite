from . import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    @property
    def password(self):
        raise ArithmeticError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # ... relationships
    courses = db.relationship('Course', backref='user')
    orders = db.relationship('Order', backref='user')

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    accepted = db.Column(db.Boolean, default=False)

    # foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __repr__(self) -> str:
        return f'<Order {self.timestamp}>'
    

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail = db.Column(db.String, default='thumbnail/no-thumbnail.png')
    description = db.Column(db.Text)
    details = db.Column(db.Text)
    link = db.Column(db.String(50), unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # relationships
    orders = db.relationship('Order', backref='course')
    sections = db.relationship('Section', backref='course')

    # foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'<Course {self.title}>'


class Section(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)

    # relationship with file
    files = db.relationship('File', backref='section')

    # foreign key
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))


    def __repr__(self) -> str:
        return f'<Sections {self.title}>'


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Integer, nullable=True)
    filetype = db.Column(db.String, nullable=False)
    path = db.Column(db.String, nullable=False)
    restrict_access = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # foreign key
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))

    def __repr__(self) -> str:
        return f'<File {self.title}>'