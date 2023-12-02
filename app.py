import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import User, db, Service, Booking, Airbnb
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///communitycrafters.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)

migrate = Migrate(app, db)
db.init_app(app)

secret_key = os.urandom(32)
app.secret_key = secret_key

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if user and user.password == password: 
        # access_token = create_access_token(identity=username)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(**data)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'firstname': user.firstname, 'lastname': user.lastname, 'username': user.username,
                 'email': user.email, 'phone_number': user.phone_number} for user in users]
    return jsonify(user_list)

# Get a specific user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'username': user.username,
            'email': user.email,
            'phone_number': user.phone_number
        })
    return jsonify({'message': 'User not found'}), 404

# Update a user by ID
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    for key, value in data.items():
        setattr(user, key, value)

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Delete a user by ID
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@app.route('/services', methods=['POST'])
def create_service():
    data = request.json
    
    service = Service(
        service_name=data['service_name'],
        service_image=data['service_image'],
        service_description=data['service_description']
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': 'Service created successfully'})

@app.route('/services', methods=['GET'])
def get_all_services():
    services = Service.query.all()
    service_list = []
    for service in services:
        service_data = {
            'id': service.id,
            'service_name': service.service_name,
            'service_image': service.service_image,
            'service_description': service.service_description
        }
        service_list.append(service_data)
    return jsonify({'services': service_list})

@app.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if service:
        service_data = {
            'id': service.id, 
            'service_name': service.service_name,
            'service_image': service.service_image,
            'service_description': service.service_description,
            'service_category': service.service_category
        }
        return jsonify({'service': service_data})
    return jsonify({'message': 'Service not found'}, 404)

@app.route('/services/<int:service_id>', methods=['PUT', 'PATCH'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}, 404)
    
    data = request.json
    service.service_name = data.get('service_name', service.service_name)
    service.service_image = data.get('service_image', service.service_image)
    service.service_description = data.get('service_description', service.service_description)
    service.service_category = data.get('service_category', service.service_category)
    
    db.session.commit()
    return jsonify({'message': 'Service updated successfully'})

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({'message': 'Service not found'}, 404)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Service deleted successfully'})

@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    # booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()

    new_booking = Booking(
        username=data['username'],
        email=data['email'],
        service_name=data['service_name'],
        booking_date=data['booking_date'],
        booking_time=data['booking_time']
    )

    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Booking created successfully'}), 201

@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    booking_list = []
    for booking in bookings:
        booking_list.append({
            'id': booking.id,
            'user_id': booking.user_id,
            'username':booking.username,
            'email':booking.email,
            'booking_date': booking.booking_date,
            'booking_time': booking.booking_time
        })
    return jsonify({'bookings': booking_list})

@app.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    data = request.get_json()
    booking.user_id = data.get('user_id', booking.user_id)
    booking.username = data.get('username', booking.username)
    booking.email = data.get('email', booking.email)
    booking.service_name = data.get('service_id', booking.service_id)
    booking.booking_date = data.get('booking_date', booking.booking_date)
    booking.booking_time = data.get('booking_time', booking.booking_time)

    db.session.commit()
    return jsonify({'message': 'Booking updated successfully'})

@app.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking deleted successfully'})


@app.route('/airbnbs', methods=['POST'])
def create_airbnb():
    data = request.get_json()
    new_airbnb = Airbnb(name=data['name'], image=data['image'], location=data['location'],
                        description=data['description'], price=data['price'])
    db.session.add(new_airbnb)
    db.session.commit()
    return jsonify({'message': 'Airbnb created successfully', 'id': new_airbnb.id})

# Read (Retrieve) Operations

# Get all Airbnbs
@app.route('/airbnbs', methods=['GET'])
def get_all_airbnbs():
    airbnbs = Airbnb.query.all()
    airbnb_list = [{'id': airbnb.id, 'name': airbnb.name, 'image': airbnb.image,
                    'location': airbnb.location, 'description': airbnb.description,
                    'price': airbnb.price} for airbnb in airbnbs]
    return jsonify({'airbnbs': airbnb_list})

# Get Airbnb by ID
@app.route('/airbnbs/<int:airbnb_id>', methods=['GET'])
def get_airbnb_by_id(airbnb_id):
    airbnb = Airbnb.query.get(airbnb_id)
    if airbnb:
        return jsonify({'id': airbnb.id, 'name': airbnb.name, 'image': airbnb.image,
                        'location': airbnb.location, 'description': airbnb.description,
                        'price': airbnb.price})
    else:
        return jsonify({'message': 'Airbnb not found'}), 404

# Update Operation
@app.route('/airbnbs/<int:airbnb_id>', methods=['PUT'])
def update_airbnb(airbnb_id):
    data = request.get_json()
    airbnb_to_update = Airbnb.query.get(airbnb_id)

    if not airbnb_to_update:
        return jsonify({'message': 'Airbnb not found'}), 404

    airbnb_to_update.name = data.get('name', airbnb_to_update.name)
    airbnb_to_update.image = data.get('image', airbnb_to_update.image)
    airbnb_to_update.location = data.get('location', airbnb_to_update.location)
    airbnb_to_update.description = data.get('description', airbnb_to_update.description)
    airbnb_to_update.price = data.get('price', airbnb_to_update.price)

    db.session.commit()
    return jsonify({'message': 'Airbnb updated successfully'})

# Delete Operation
@app.route('/airbnbs/<int:airbnb_id>', methods=['DELETE'])
def delete_airbnb(airbnb_id):
    airbnb_to_delete = Airbnb.query.get(airbnb_id)

    if not airbnb_to_delete:
        return jsonify({'message': 'Airbnb not found'}), 404

    db.session.delete(airbnb_to_delete)
    db.session.commit()
    return jsonify({'message': 'Airbnb deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True, port=5555)
