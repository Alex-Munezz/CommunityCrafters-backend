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


# {
#     "services": [
#         {
#             "id": 1,
#             "service_description": "We offer expert plumbing solutions for all your plumbing needs.",
#             "service_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRbvGLS5mjh3GzSxDaEzoR2Whs9OXCmGLQLBfIfGzES0RjCwm9QhrLEFeyRUrqQjzRWXw&usqp=CAU",
#             "service_name": "Plumbing Services"
#         },
#         {
#             "id": 2,
#             "service_description": "Do you have an event and dont know what to do with matters food? Say less, know why, we also got you covered!!",
#             "service_image": "https://st.depositphotos.com/1003697/2570/i/950/depositphotos_25709887-stock-photo-buffet-food.jpg",
#             "service_name": "Catering Services"
#         },
#         {
#             "id": 4,
#             "service_description": "We know you value and treasure you car. Let us take care of you plus your car with our top notch and best drivers.",
#             "service_image": "data:image/jpeg;base64,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",
#             "service_name": "Chauffering Services"
#         },
#         {
#             "id": 5,
#             "service_description": "Leave you child/ren to us and let us improve her/his academic performance.",
#             "service_image": "https://homeschool.co.ke/storage/NHS-1.jpg",
#             "service_name": "Tutoring/Home Schooling Services"
#         },
#         {
#             "id": 6,
#             "service_description": "Leave you hair to us and let us treat you look like the queen you are.",
#             "service_image": "https://i0.wp.com/www.hadviser.com/wp-content/uploads/2020/04/2-stunning-african-braids-CLPMe82H6Kw.jpg?resize=1073%2C1080&ssl=1",
#             "service_name": "Braiding Services"
#         },
#         {
#             "id": 7,
#             "service_description": "Leave you home to us and be sure everything will be safe and find it as you left it.",
#             "service_image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSBKxp-BFy5a336hk4y9-PTT9Qw77UFWgCDiQ&usqp=CAU",
#             "service_name": "Home Sitting Services"
#         },
#         {
#             "id": 8,
#             "service_description": "Leave the cleaning to us and enjoy a sparkling clean space.",
#             "service_image": "https://nextdaycleaning.com/wp-content/uploads/2020/06/Main-Benefits-of-Residential-Cleaning-Services-1024x663.jpg",
#             "service_name": "Cleaning Services"
#         },
#         {
#             "id": 9,
#             "service_description": "Our skilled electricians provide safe and reliable electrical services.",
#             "service_image": "https://us.123rf.com/450wm/bermek/bermek2304/bermek230403255/202409630-power-cord-plugged-into-electrical-outlet-on-insulated-wall-in-hospital-room.jpg?ver=6",
#             "service_name": "Electrical Services"
#         }
#     ]
# }