from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter
from models import GeoSearch


class GeoRouter(BaseRouter):
    route_name = 'geo_task'
    valid_verbs = ['get_status', 'subscribe']

    def get_subscription_channels(self, **kwargs):
        channel = 'project_%s_geo' % kwargs.get('project')
        return [channel]


class SearchRouter(BaseRouter):
    route_name = 'search_task'
    valid_verbs = ['get_status', 'subscribe']

    def get_subscription_channels(self, **kwargs):
        channel = 'project_%s_geo' % kwargs.get('project')
        return [channel]

route_handler.register(GeoRouter)
route_handler.register(SearchRouter)
