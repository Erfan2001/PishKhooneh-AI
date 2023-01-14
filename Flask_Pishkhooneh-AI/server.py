from flask import Flask, request
import requests
from flask import render_template
import pickle
app = Flask(__name__)


@app.route('/predict')
def predictHouse():
    args = request.args.to_dict()
    area = None
    age = None
    region = None
    parking = None
    elevator = None
    if args.get('area'):
        args['area'] = int(args.get('area'))
        if args.get('area') < 0 or args.get('area') > 4000:
            return {'error': 'متراژ باید عددی بین 0 تا 4000 باشد'}, 400
        area = args.get('area')
    else:
        return {'error': 'مشکلی در درخواست شما به وجود آمده است'}, 400
    if args.get('age'):
        args['age'] = int(args.get('age'))
        if args.get('age') < 0 or args.get('age') >= 100:
            return {'error': 'سن بنا باید عددی بین 0 تا 100 باشد'}, 400
        age = args.get('age')
    else:
        return {'error': 'مشکلی در درخواست شما به وجود آمده است'}, 400
    if args.get('region'):
        args['region'] = int(args.get('region'))
        if args.get('region') <= 1728 or args.get('region') > 1790:
            return {'error':'منطقه وارد شده نادرست است'}, 400
        region = args.get('region')
    else:
        return {'error': 'مشکلی در درخواست شما به وجود آمده است'}, 400
    if args.get('parking'):
        args['parking'] = int(args.get('parking'))
        if args.get('parking') not in [0, 1]:
            return {'error':'مقدار وارد شده برای پارکینگ نادرست است'}, 400
        parking = args.get('parking')
    else:
        return {'error': 'مشکلی در درخواست شما به وجود آمده است'}, 400
    if args.get('elevator'):
        args['elevator'] = int(args.get('elevator'))
        if args.get('elevator') not in [0, 1]:
            return {'error': 'مقدار وارد شده برای آسانسور نادرست است'}, 400
        elevator = args.get('elevator')
    else:
        return {'error': 'مشکلی در درخواست شما به وجود آمده است'}, 400
    values = [[area, age, region, parking, elevator]]
    loaded_model = pickle.load(open('Flask_Pishkhooneh-AI/moamelati.sav', 'rb'))
    min_buy = loaded_model.predict(values)[0]
    loaded_model = pickle.load(open('Flask_Pishkhooneh-AI/buyBazar.sav', 'rb'))
    max_buy = loaded_model.predict(values)[0]
    loaded_model = pickle.load(open('Flask_Pishkhooneh-AI/karshenasi.sav', 'rb'))
    suitable_buy = loaded_model.predict(values)[0]

    loaded_model = pickle.load(open('Flask_Pishkhooneh-AI/rentCheap.sav', 'rb'))
    min_rent = loaded_model.predict(values)[0]
    loaded_model = pickle.load(open('Flask_Pishkhooneh-AI/rentExpensive.sav', 'rb'))
    max_rent = loaded_model.predict(values)[0]
    loaded_model = pickle.load(open('Flask_Pishkhooneh-AI/rentBazar.sav', 'rb'))
    suitable_rent = loaded_model.predict(values)[0]
    buyValues = [min_buy, max_buy, suitable_buy]
    rentValues = [min_rent, max_rent, suitable_rent]
    return {'buy': {'minimum': min(buyValues), 'maximum': max(buyValues)},
            'rent': {'minimum': min(rentValues), 'maximum': max(rentValues)}}


@app.errorhandler(404)
def page_not_found(e):
    return '<h1>You could not find me yet :)))</h1><br/><h2><a href="https://www.linkedin.com/in/erfan-nourbakhsh-221540197/">You can contact me</a></h2>'


if __name__ == '__main__':
    app.run()
