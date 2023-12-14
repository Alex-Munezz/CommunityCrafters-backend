from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class Service(db.Model):
    __tablename__ ='service'    
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(120), unique=True, nullable=False)
    service_image = db.Column(db.String(800), unique=True, nullable=False)
    service_description = db.Column(db.Text, nullable=False)

class Airbnb(db.Model):
    __tablename__='airbnb'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    image = db.Column(db.String(2000), unique=True, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.String(100), nullable=False)

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey('user.username'))
    email = db.Column(db.String(300), db.ForeignKey('user.email'))
    service_name = db.Column(db.Integer, db.ForeignKey('service.service_name'))
    booking_date = db.Column(db.String, nullable=False)
    booking_time = db.Column(db.String, nullable=False)

class Review(db.Model):
    __tablename__ ='review'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    payment_date = db.Column(db.Date)



