from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@parking-db:5432/parking')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class ParkingSpot(db.Model):
    __tablename__ = 'parking_spots'
    spot_number = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer)
    occupied = db.Column(db.String(3))
    car_plate = db.Column(db.String(20))

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head><title>Приложение парковки</title></head>
<body>
<h1> Приложение парковки</h1>
<a href="/empty-spots"><button>Узнать количество пустых мест</button></a><br><br>
<a href="/car-spot"><button>Проверить место автомобиля </button></a><br><br>
</body>
</html>
'''

@app.route('/empty-spots')
def empty_spots():
    empty_count = ParkingSpot.query.filter_by(occupied='Нет').count()
    return f'''
<!DOCTYPE html>
<html>
<head><title>Пустые места</title></head>
<body>
<h1> Количество пустых парковочных мест</h1>
<h2>Пустых мест: {empty_count}</h2>
<a href="/">← На главную</a>
</body>
</html>
'''

@app.route('/car-spot', methods=['GET', 'POST'])
def car_spot():
    error = ''
    result = ''
    if request.method == 'POST':
        car_plate = request.form.get('car_plate')
        if car_plate:
            spot = ParkingSpot.query.filter_by(car_plate=car_plate).first()
            if spot:
                result = f'''
<h2> Место вашего автомобиля</h2>
<p>Номер машиноместа: {spot.spot_number}</p>
<p>Занято: {spot.occupied}</p>
'''
            else:
                error = 'Номер автомобиля не найден в базе данных (проверьте правильность ввода)'
        else:
            error = 'Введите номер автомобиля'
    return f'''
<!DOCTYPE html>
<html>
<head><title>Проверить место автомобиля</title></head>
<body>
<h1> Проверить место автомобиля</h1>
<form method="post">
<label>Государственный номер автомобиля: <input name="car_plate" type="text" placeholder="мо550с77"></label><br><br>
<button type="submit">Проверить</button>
</form>
{"<p style='color:red'>" + error + "</p>" if error else ''}
''' + (result or '') + '''
<a href="/">← На главную страницу</a>
</body>
</html>
'''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

