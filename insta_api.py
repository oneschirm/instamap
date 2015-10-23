from instagram.client import InstagramAPI
import json
from datetime import datetime
import web
import urlparse


def get_insta():
    parameters = urlparse.parse_qs(web.ctx.query[1:])
    CLIENT_ID = 'something secret'
    CLIENT_SECRET = 'should have been in env variables'
    latitude = float(parameters['lat'][0])
    longitude = float(parameters['lng'][0])
    distance = int(parameters['distance'][0])
    count = int(parameters['count'][0])

    api = InstagramAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    results = api.media_search(
        lat=latitude, lng=longitude, count=count, distance=distance)

    total_pre_json = []

    for picture in results:
        pre_json = {}
        pre_json['created_time'] = (
            datetime.today().utcnow() - picture.created_time).days
        pre_json['username'] = picture.user.username
        pre_json['location_name'] = picture.location.name
        pre_json['latlng'] = {
            'lat': picture.location.point.latitude, 'lng': picture.location.point.longitude}
        pre_json['photo_url'] = picture.images['standard_resolution'].url
        pre_json['tags'] = [x.name for x in picture.tags]
        pre_json['comments'] = [
            ':'.join([x.user.username, x.text]) for x in picture.comments]
        total_pre_json.append(pre_json)

    return json.dumps(total_pre_json)
