from flask import jsonify, request, url_for
from . import api
from .. import mongo
from ..logger import log
from ..exceptions import ValidationError
from datetime import datetime
from bson import ObjectId


@api.route('/locations/<string:slug>', methods=['POST'])
def create_location(slug):

    log.info('api_create_new_location: slug {0}'.format(slug))
    account = mongo.db.accounts.find_one_or_404({'slug': slug})
    json = request.json

    # validate schema
    title = json.get('title')
    if title is None:
        raise ValidationError('title cannot be empty')

    location = {
        'account_id': account.get('_id'),
        'title': json.get('title'),
        'latitude': json.get('latitude'),
        'longitude': json.get('longitude'),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow(),
        'metadata': json.get('metadata')
    }

    result = mongo.db.locations.insert_one(location)
    log.info('api_create_new_location - document inserted in db: {0}'.format(result.inserted_id))
    location['url'] = url_for('main.get_location', location_id=str(result.inserted_id))
    return jsonify(), 201


@api.route('/locations/<string:slug>', methods=['GET'])
def get_locations(slug):

    log.info('api_get_locations: slug {0}'.format(slug))

    account = mongo.db.accounts.find_one_or_404({'slug': slug})
    locations = mongo.db.locations.find({'account_id': account.get('_id')})

    return jsonify([
        {
            'title': location.get('title'),
            'latitude': location.get('latitude'),
            'longitude': location.get('longitude'),
            'created_at': location.get('created_at'),
            'updated_at': location.get('updated_at'),
            'metadata': location.get('metadata'),
            'url': url_for('main.get_location', location_id=str(location.get('_id')), _external=True)
        } for location in locations])


@api.route('/locations/<string:location_id>', methods=['PUT'])
def update_location(location_id):

    log.info('api_update_location: location_id {0}'.format(location_id))
    mongo.db.locations.find_one_or_404({'_id': ObjectId(location_id)})
    json = request.json

    # validate schema
    latitude = json.get('latitude')
    longitude = json.get('longitude')

    if latitude is None or longitude is None:
        raise ValidationError('latitude and longitude cannot be empty')

    data = {
        "$set": {
            'latitude': json.get('latitude'),
            'longitude': json.get('longitude')
        }
    }

    result = mongo.db.locations.update_one({'_id': ObjectId(location_id)}, data)
    log.info('api_update_location: result {0}'.format(result.raw_result))

    return jsonify()
