import json
from django.conf import settings

def get_user_group(user):
    try:
        return user.groups.get().name
    except:
        return None

def get_group_from_index_name(index_name):
    for group, name in settings.ES_INDEX.iteritems():
        if name == index_name:
            return group

def is_member(user, group_name):
    if group_name == 'CCDB':
        return True;
    return user.groups.filter(name=group_name).exists()


def get_index_name_from_request(request):
    try:
        if request.method == 'POST':
            index_name = request.data['params']['index_name']
        else:
            index_name = json.loads(request.GET.get('params'))['index_name']
    except:
        if get_user_group(request.user):
            index_name = settings.ES_INDEX[get_user_group(request.user)]
        else:
            index_name = settings.ES_INDEX['CCDB'] #default index
    return index_name
