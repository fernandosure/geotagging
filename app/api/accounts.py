from flask import jsonify, request, url_for, abort
from . import api
from .. import mongo
from ..logger import log
from ..exceptions import ValidationError
from datetime import datetime


@api.route('/accounts', methods=['GET'])
def get_accounts():

    log.info('api_get_accounts')
    accounts = mongo.db.accounts.find({})

    return jsonify([
        {
            'name': account.get('name'),
            'slug': account.get('slug')
        }
        for account in list(accounts)])


@api.route('/accounts', methods=['POST'])
def create_account():

    log.info('api_create_new_account')
    json = request.json
    accounts = mongo.db.accounts.find({'slug': json.get('slug')}).count()

    if accounts > 0:
        abort(303)

    # validate schema
    if json.get('name') is None or json.get('slug') is None:
        raise ValidationError('name or slug cannot be empty')

    location = {
        'name': json.get('name'),
        'slug': json.get('slug'),
        'created_at': datetime.utcnow(),
        'updated_at': datetime.utcnow()
    }

    result = mongo.db.accounts.insert_one(location)
    log.info('api_create_new_account - document inserted in db: {0}'.format(result.inserted_id))
    return jsonify(), 201
