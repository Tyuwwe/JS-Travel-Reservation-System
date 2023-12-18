from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 导入 CORS
from sqlalchemy import func

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
    custid = db.Column(db.Integer, nullable=False)

class Reservation(db.Model):
    __tablename__ = 'reservations'
    resvkey = db.Column(db.Integer, primary_key=True)  # 自动增长的ID
    custname = db.Column(db.String(255), db.ForeignKey('customers.custName'), nullable=False)
    resvtype = db.Column(db.Integer, nullable=False)
    flightid = db.Column(db.Integer, db.ForeignKey('flights.id'))  # 外键引用
    busid = db.Column(db.Integer, db.ForeignKey('bus.id'))  # 外键引用
    hotellocation = db.Column(db.String(255), db.ForeignKey('hotels.location'))  # 外键引用

# 示例路由：获取所有航班信息
@app.route('/flights', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    return jsonify([flight.flightnum for flight in flights])

@app.route('/flights/<from_city>', methods=['GET'])
def get_flights_by_city(from_city):
    # 将传入的城市名称转换为小写，并查询数据库
    flights = Flight.query.filter(func.lower(Flight.fromcity) == func.lower(from_city)).all()

    # 将航班信息转换为JSON格式
    flights_data = []
    for flight in flights:
        flight_data = {
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



# 示例路由：获取所有宾馆信息
@app.route('/hotels', methods=['GET'])
def get_hotels():
    hotels = Hotel.query.all()
    return jsonify([hotel.location for hotel in hotels])

# 主函数
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
