from flask import jsonify, request

import string

from . import app, db
from .errors import InvalidAPIUsage
from .models import MAX_LEN_CUSTOM_ID, URLMap
from .views import get_unique_short_id




@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_link(short_id):
    if not URLMap.query.filter_by(short=short_id).all():
        raise InvalidAPIUsage('Указанный id не найден', status_code=404)

    urlmap = URLMap.query.filter_by(short=short_id).first()
    return jsonify(urlmap.to_api_get()), 200


@app.route('/api/id/', methods=['POST'])
def add_link():
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if URLMap.query.filter_by(original=data['url']).first() is not None:
        raise InvalidAPIUsage('Имя "{}" уже занято.'.format(data['custom_id']))

    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    else:

        if len(data['custom_id']) > MAX_LEN_CUSTOM_ID:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')

        for symb in data['custom_id']:
            if symb not in string.ascii_letters and symb not in string.digits:
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки')

        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(
                'Имя "{}" уже занято.'.format(data['custom_id']))

    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201
