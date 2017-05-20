from flask import render_template, url_for
from . import main
from .. import mongo
from ..logger import log
from bson import ObjectId


@main.route('/', methods=['GET'])
def get_index():
    log.info('main_get_index')
    return render_template('index.html')


@main.route('/locations/<string:location_id>', methods=['GET'])
def get_location(location_id):

    log.info('main_get_location: location_id: {0}'.format(location_id))
    mongo.db.locations.find_one_or_404({'_id': ObjectId(location_id)})

    return render_template('update_location.html', url=url_for('api.update_location', location_id=location_id))


@main.route('/accounts/<string:slug>', methods=['GET'])
def get_locations(slug):

    log.info('main_get_locations: slug: {0}'.format(slug))
    account = mongo.db.accounts.find_one_or_404({'slug': slug})
    locations = list(mongo.db.locations.find({'account_id': account.get('_id')}))

    return render_template('map.html', locations=[
        {
            'title': location.get('title'),
            'latitude': location.get('latitude'),
            'longitude': location.get('longitude')
        } for location in locations])
