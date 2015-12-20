from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter
from swampdragon.pubsub_providers.data_publisher import publish_data
from django.conf import settings
from google.models import Search

cache = settings.CACHE


class GeoRouter(BaseRouter):
    route_name = 'geo_task'
    valid_verbs = ['subscribe']

    def get_subscription_channels(self, **kwargs):
        channel = 'project_%s_geo' % kwargs.get('project')
        return [channel]


class SearchRouter(BaseRouter):
    route_name = 'search_task'
    valid_verbs = ['subscribe']

    def get_subscription_channels(self, **kwargs):
        channel = 'project_%s_search' % kwargs.get('project')
        print channel
        return [channel]

route_handler.register(GeoRouter)
route_handler.register(SearchRouter)
