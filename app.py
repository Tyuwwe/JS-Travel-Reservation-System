from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 导入 CORS
from sqlalchemy import func
from flask import abort

app = Flask(__name__)
CORS(app)  # 启用 CORS

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/TravelSystem'

db = SQLAlchemy(app)

# 定义数据模型
class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)  # 自动增长的ID
    flightnum = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    numseats = db.Column(db.Integer, nullable=False)
    numavail = db.Column(db.Integer, nullable=False)
    fromcity = db.Column(db.String(255), nullable=False)
    arivcity = db.Column(db.String(255), nullable=False)

class Hotel(db.Model):
    __tablename__ = 'hotels'
    location = db.Column(db.String(255), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    numrooms = db.Column(db.Integer, nullable=False)
    numavail = db.Column(db.Integer, nullable=False)

class Bus(db.Model):
    __tablename__ = 'bus'
    id = db.Column(db.Integer, primary_key=True)  # 自动增长的ID
    location = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    numbus = db.Column(db.Integer, nullable=False)
    numavail = db.Column(db.Integer, nullable=False)

class Customer(db.Model):
    __tablename__ = 'customers'
    custname = db.Column(db.String(255), primary_key=True)
    custid = db.Column(db.Integer, primary_key=True)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    resvkey = db.Column(db.Integer, primary_key=True)  # 自动增长的ID
    custname = db.Column(db.String(255), db.ForeignKey('customers.custname'), nullable=False)
    resvtype = db.Column(db.Integer, nullable=False)
    flightid = db.Column(db.Integer, db.ForeignKey('flights.id'))  # 外键引用
    busid = db.Column(db.Integer, db.ForeignKey('bus.id'))  # 外键引用
    hotellocation = db.Column(db.String(255), db.ForeignKey('hotels.location'))  # 外键引用

# 示例路由：获取所有航班信息
@app.route('/flights', methods=['GET'])
def get_flights():
    flights = Flight.query.all()

    # 将航班信息转换为JSON格式
    flights_data = []
    for flight in flights:
        flight_data = {
            'id' : flight.id,
            'flight_num': flight.flightnum,
            'from_city': flight.fromcity,
            'ariv_city': flight.arivcity,
            'num_seats': flight.numseats,
            'num_avail': flight.numavail,
            'price': flight.price
        }
        flights_data.append(flight_data)

    return jsonify(flights_data)

@app.route('/flights/<from_city>', methods=['GET'])
def get_flights_by_city(from_city):
    # 将传入的城市名称转换为小写，并查询数据库
    flights = Flight.query.filter(func.lower(Flight.fromcity) == func.lower(from_city)).all()

    # 将航班信息转换为JSON格式
    flights_data = []
    for flight in flights:
        flight_data = {
            'id' : flight.id,
            'flight_num': flight.flightnum,
            'from_city': flight.fromcity,
            'ariv_city': flight.arivcity,
            'num_seats': flight.numseats,
            'num_avail': flight.numavail,
            'price': flight.price
        }
        flights_data.append(flight_data)

    # 返回JSON响应
    return jsonify(flights_data)

# 新的路由：创建预定记录
@app.route('/flights', methods=['POST'])
def create_flight_reservation():
    # 获取前端POST的数据
    data = request.json

    # 确保必要的数据存在
    required_fields = ['custname', 'flight_id']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    # 解析数据
    custname = data['custname']
    flight_id = data['flight_id']

    # 检查用户是否存在，如果不存在则创建用户
    customer = Customer.query.filter_by(custname=custname).first()
    if customer is None:
        # 创建用户并获取自增的用户id
        new_customer = Customer(custname=custname)
        db.session.add(new_customer)
        db.session.commit()

    # 检查航班是否存在
    flight = Flight.query.get(flight_id)
    if flight is None:
        abort(404, description='Flight not found')

    # 检查可用座位是否足够
    if flight.numavail <= 0:
        abort(400, description='No available seats for this flight')

    # 创建预定记录
    reservation = Reservation(
        custname=custname,
        resvtype=1,  # 航班类型
        flightid=flight_id
    )
    
    # 更新可用座位数量
    flight.numavail -= 1

    # 保存到数据库
    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation created successfully'}), 201

# 删除预定信息的路由
@app.route('/reservations/<int:resvkey>', methods=['DELETE'])
def delete_reservation(resvkey):
    reservation = Reservation.query.get(resvkey)
    if reservation is None:
        abort(404, description="Reservation not found")

    # 根据预定类型更新相关数据
    if reservation.resvtype == 1:  # 航班
        flight = Flight.query.get(reservation.flightid)
        if flight:
            flight.numavail += 1
    elif reservation.resvtype == 2:  # 酒店
        hotel = Hotel.query.filter_by(location=reservation.hotellocation).first()
        if hotel:
            hotel.numavail += 1
    elif reservation.resvtype == 3:  # 巴士
        bus = Bus.query.get(reservation.busid)
        if bus:
            bus.numavail += 1

    # 删除预定记录
    db.session.delete(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation deleted successfully'}), 200


# 获取巴士信息
@app.route('/bus/<bus_location>', methods=['GET'])
def get_bus_by_location(bus_location):
    # 将传入的巴士位置名称转换为小写，并查询数据库
    buses = Bus.query.filter(func.lower(Bus.location) == func.lower(bus_location)).all()

    # 将巴士信息转换为JSON格式
    buses_data = []
    for bus in buses:
        bus_data = {
            'id': bus.id,
            'location': bus.location,
            'price': bus.price,
            'num_bus': bus.numbus,
            'num_avail': bus.numavail
        }
        buses_data.append(bus_data)

    # 返回JSON响应
    return jsonify(buses_data)

# 获取巴士信息
@app.route('/bus', methods=['GET'])
def get_bus():
    # 将传入的巴士位置名称转换为小写，并查询数据库
    buses = Bus.query.all()

    # 将巴士信息转换为JSON格式
    buses_data = []
    for bus in buses:
        bus_data = {
            'id': bus.id,
            'location': bus.location,
            'price': bus.price,
            'num_bus': bus.numbus,
            'num_avail': bus.numavail
        }
        buses_data.append(bus_data)

    # 返回JSON响应
    return jsonify(buses_data)

# 新的路由：创建预定记录
@app.route('/bus', methods=['POST'])
def create_bus_reservation():
    # 获取前端POST的数据
    data = request.json

    # 确保必要的数据存在
    required_fields = ['custname', 'bus_id']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    # 解析数据
    custname = data['custname']
    bus_id = data['bus_id']

    # 检查用户是否存在，如果不存在则创建用户
    customer = Customer.query.filter_by(custname=custname).first()
    if customer is None:
        # 创建用户并获取自增的用户id
        new_customer = Customer(custname=custname)
        db.session.add(new_customer)
        db.session.commit()

    # 检查航班是否存在
    bus = Bus.query.get(bus_id)
    if bus is None:
        abort(404, description='Bus not found')

    # 检查可用座位是否足够
    if bus.numavail <= 0:
        abort(400, description='No available seats for this flight')

    # 创建预定记录
    reservation = Reservation(
        custname=custname,
        resvtype=3,  # 巴士类型
        busid=bus_id
    )
    
    # 更新可用座位数量
    bus.numavail -= 1

    # 保存到数据库
    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation created successfully'}), 201

# 示例路由：获取所有宾馆信息
@app.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()

    # 将巴士信息转换为JSON格式
    hotels_data = []
    for hotel in hotels:
        hotel_data = {
            'location': hotel.location,
            'price': hotel.price,
            'num_rooms': hotel.numrooms,
            'num_avail': hotel.numavail
        }
        hotels_data.append(hotel_data)

    return jsonify(hotels_data)

# 获取酒店信息
@app.route('/hotels/<hotel_location>', methods=['GET'])
def get_hotel_by_location(hotel_location):
    # 将传入的酒店位置名称转换为小写，并查询数据库
    hotels = Hotel.query.filter(func.lower(Hotel.location) == func.lower(hotel_location)).all()

    # 将酒店信息转换为JSON格式
    hotels_data = []
    for hotel in hotels:
        hotel_data = {
            'location': hotel.location,
            'price': hotel.price,
            'num_rooms': hotel.numrooms,
            'num_avail': hotel.numavail
        }
        hotels_data.append(hotel_data)

    # 返回JSON响应
    return jsonify(hotels_data)

# 新的路由：创建预定记录
@app.route('/hotels', methods=['POST'])
def create_hotel_reservation():
    # 获取前端POST的数据
    data = request.json

    # 确保必要的数据存在
    required_fields = ['custname', 'hotel_location']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    # 解析数据
    custname = data['custname']
    hotellocation = data['hotel_location']

    # 检查用户是否存在，如果不存在则创建用户
    customer = Customer.query.filter_by(custname=custname).first()
    if customer is None:
        # 创建用户并获取自增的用户id
        new_customer = Customer(custname=custname)
        db.session.add(new_customer)
        db.session.commit()

    # 检查宾馆是否存在
    hotel = Hotel.query.filter_by(location=hotellocation).first()
    if hotel is None:
        abort(404, description='Bus not found')

    # 检查可用座位是否足够
    if hotel.numavail <= 0:
        abort(400, description='No available room')

    # 创建预定记录
    reservation = Reservation(
        custname=custname,
        resvtype=2,  # 酒店类型
        hotellocation=hotellocation
    )
    
    # 更新可用房间数量
    hotel.numavail -= 1

    # 保存到数据库
    db.session.add(reservation)
    db.session.commit()

    return jsonify({'message': 'Reservation created successfully'}), 201

# 新的路由：根据用户名查询预定信息
@app.route('/reserve', methods=['POST'])
def get_reservations_by_username():
    # 获取前端POST的数据
    data = request.json

    # 确保必要的数据存在
    required_fields = ['custname']
    if not all(field in data for field in required_fields):
        abort(400, description='Missing required fields')

    # 解析数据
    custname = data['custname']

    # 查询用户的所有预定信息
    reservations = Reservation.query.filter_by(custname=custname).all()

    # 将预定信息转换为JSON格式
    reservations_data = []
    for reservation in reservations:
        reservation_data = {
            'id': reservation.resvkey,
            'passenger_name': reservation.custname,
            'reservation_type': get_reservation_type(reservation.resvtype),
            'value': get_reservation_value(reservation)
        }
        reservations_data.append(reservation_data)

    # 检查路线是否完整
    is_route_complete = check_additional_functionality(reservations)
    reservations_data.append({'is_route_complete': is_route_complete})

    # 返回JSON响应
    return jsonify(reservations_data)

def check_additional_functionality(reservations):
    flight_reservations = [r for r in reservations if r.resvtype == 1]
    hotel_reservations = [r for r in reservations if r.resvtype == 2]
    bus_reservations = [r for r in reservations if r.resvtype == 3]

    if len(flight_reservations) == 0:
        return False

    # 用户只预定了航班的情况
    if len(hotel_reservations) == 0 and len(bus_reservations) == 0:
        return check_flights_complete_route(flight_reservations)

    # 用户预定了航班以及酒店或巴士的情况
    if len(flight_reservations) == 1:
        return check_single_flight_with_accommodations(flight_reservations[0], hotel_reservations, bus_reservations)

    return False

def check_flights_complete_route(flights):
    # 构建航班的起点到终点的映射
    flight_map = {}
    for flight_reservation in flights:
        flight = Flight.query.get(flight_reservation.flightid)
        if flight:
            flight_map[flight.fromcity] = flight.arivcity

    # 检查是否可以形成闭环
    if not flight_map:
        return False

    start_city = next(iter(flight_map))
    current_city = start_city

    for _ in range(len(flight_map)):
        current_city = flight_map.get(current_city)
        if not current_city:
            return False  # 如果某个城市没有下一个目的地，则不是闭环
        if current_city == start_city:
            return True  # 如果回到起点，则形成了闭环

    return False



def check_single_flight_with_accommodations(flight_reservation, hotel_reservations, bus_reservations):
    # 获取与预订关联的航班
    flight = Flight.query.get(flight_reservation.flightid)
    if not flight:
        return False  # 如果找不到航班，则返回False

    flight_destination = flight.arivcity

    # 获取与酒店预订关联的酒店
    hotels_at_destination = [Hotel.query.get(h.hotellocation) for h in hotel_reservations]

    # 检查是否预定了航班终点地址的酒店
    hotel_at_destination = any(hotel.location == flight_destination for hotel in hotels_at_destination if hotel)

    # 获取与巴士预订关联的巴士
    buses_at_destination = [Bus.query.get(b.busid) for b in bus_reservations]

    # 检查是否预定了航班终点地址的巴士
    bus_at_destination = any(bus.location == flight_destination for bus in buses_at_destination if bus)

    return hotel_at_destination and bus_at_destination



def get_reservation_type(resvtype):
    # 根据resvtype返回预定类型的字符串
    if resvtype == 1:
        return 'Flight'
    elif resvtype == 2:
        return 'Hotel'
    elif resvtype == 3:
        return 'Bus'
    else:
        return 'Unknown'

def get_reservation_value(reservation):
    if reservation.resvtype == 1:
        # 预定飞机，返回出发地-目的地
        flight = Flight.query.get(reservation.flightid)

        if flight:
            return f'{flight.fromcity}-{flight.arivcity}'
        else:
            return 'Unknown Flight'
    elif reservation.resvtype == 2:
        # 预定酒店，返回酒店的所在地
        hotel = Hotel.query.get(reservation.hotellocation)

        if hotel:
            return hotel.location
        else:
            return 'Unknown Hotel'
    elif reservation.resvtype == 3:
        # 预定巴士，返回巴士的所在地
        bus = Bus.query.get(reservation.busid)

        if bus:
            return bus.location
        else:
            return 'Unknown Bus'
    else:
        return 'Unknown'


# 主函数
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
