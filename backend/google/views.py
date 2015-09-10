from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.conf import settings
from django.core import serializers
from cr_search.helpers import is_member, get_index_name_from_request, get_group_from_index_name, get_user_group
from elasticsearch import Elasticsearch
from elasticsearch import TransportError
from cr_search.models import SavedSearch
import json
import urllib
import requests

FMT_TYPE_MAPPING = {
    "csv": "text/csv",
    "json": "application/json",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"}

es = Elasticsearch([settings.ES_HOST])

@api_view(['POST'])
def search(request):
    """
    simply take the raw query body from frontend, and route to elasticsearch;

    if query failed, return a json object containing
    error: a string error message from elasticsearch server
    info: returned error info in dict format from elasticsearch server
    as well as the response status code

    if success, the raw response from elasticsearch will be returned.
    """
    index_name = get_index_name_from_request(request)
    if not index_name in settings.ES_INDEX.values():
        return HttpResponseBadRequest("Index Not Found")
    if not is_member(request.user, get_group_from_index_name(index_name)):
        return HttpResponseForbidden("You don't have permission to access this database")

    try:
        res = es.search(index=index_name, doc_type=index_name, body=request.data['search'])
    except TransportError as e:
        code = e.status_code
        res = {"error": e.error, "info": e.info, "status_code": code}
        return Response(res, status=code)
    return Response(res, status=status.HTTP_200_OK)


def export(request):
    """
    Export search result as output in different format.
    Currently csv, xls, xlsx and json formats are supported.
    Require elasticsearch data format plugin; install it by
    $ES_HOME/bin/plugin --install org.codelibs/elasticsearch-dataformat/1.6.0

    The request should send a json object in the following format,
    /_export?format=xls&body={"_source":["severity","queue"],"query":{"match":{"what_happened":"bank"}}}

     'format' indicates the file format of the output file
     'body' contains a regular ES query body
     '_source' in 'body' is optional and it limits the output for selected fields.
     """
    index_name = get_index_name_from_request(request)
    if not index_name in settings.ES_INDEX.values():
        return HttpResponseBadRequest("Index Not Found")
    if not is_member(request.user, get_group_from_index_name(index_name)):
        return HttpResponseForbidden("You don't have permission to access this database")

    fmt = request.GET.get('format', 'csv').lower()
    media_type = FMT_TYPE_MAPPING.get(fmt, None)
    if not media_type:
        msg = {"error": "format %s not supported" % fmt}
        return HttpResponse(json.dumps(msg), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    body = request.GET.get('search', None)
    if body:
        try:
            body = json.loads(body)
        except ValueError:
            msg = {"error": "query body not in right format"}
            return HttpResponse(json.dumps(msg), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)
    else:
        msg = {"error": "you must provide a query body"}
        return HttpResponse(json.dumps(msg), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)

    params = {"format": fmt,
              "source": json.dumps(body)}
    params = urllib.urlencode(params)
    url = "%s/%s/%s/_data?%s" %(settings.ES_HOST, index_name, index_name, params)
    res = requests.get(url)

    if res.ok:
        response = HttpResponse(res.content, content_type=media_type)
        response['Content-Disposition'] = 'attachment; filename="exported.%s"' %fmt
        return response
    else:
        return HttpResponse(res.content, content_type="application/json", status=res.status_code)


@api_view(['POST'])
def suggest(request):
    """
    Implement the autocomplete feature for search
    The request should POST a json object like
    {"text": "xxxx", "size": 10}
    where text is the user input, and size is how many suggestions should be returned.
    size is optional, if skipped, maximum 6 suggestions will be returned.
    """
    index_name = get_index_name_from_request(request)
    if not index_name in settings.ES_INDEX.values():
        return HttpResponseBadRequest("Index Not Found")
    if not is_member(request.user, get_group_from_index_name(index_name)):
        return HttpResponseForbidden("You don't have permission to access this database")

    s = request.data.get('text', None)
    size = request.data.get('size', 6)

    if not s:
        msg = {"error": "text key is missing"}
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    body = {"sgg": {"text":"%s" %s, "completion": {"field":"suggest", "size": size}}}

    try:
        res = es.suggest(index=index_name, body=body)
        candidates = [e['text'] for e in res['sgg'][0]['options']]
        return Response(candidates, status=status.HTTP_200_OK)
    except TransportError as e:
        code = e.status_code
        res = {"error": e.error, "info": e.info, "status_code": code}
        return Response(res, status=code)


# leave it here in case we may want to use json
# @api_view(['GET'])
# def item(request, id):
#     try:
#         doc = es.get(index=settings.ES_INDEX[get_group_name(request.user)], doc_type=settings.ES_TYPE, id=id)['_source']
#         return Response(doc, status=status.HTTP_200_OK)
#     except TransportError as e:
#         code = e.status_code
#         res = {"info": e.info, "status_code": code}
#         return Response(res, status=code)


def document(request, id):
    index_name = get_index_name_from_request(request)
    if not index_name in settings.ES_INDEX.values():
        return HttpResponseBadRequest("Index Not Found")
    if not is_member(request.user, get_group_from_index_name(index_name)):
        return HttpResponseForbidden("You don't have permission to access this database")

    try:
        doc = es.get(index=index_name, doc_type=index_name, id=id)['_source']
    except TransportError as e:
        return render_to_response('item.html', {'doc': None})
    dt_fields = ['created_time', 'date_sent_to_company']
    for f in dt_fields:
        if doc.get(f, None):
            doc[f] = datetime.strptime(doc[f], '%Y-%m-%dT%H:%M:%SZ').strftime("%m/%d/%Y")
    return render_to_response('item.html', {'doc': doc})


def save_search(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        user = request.user or None
        try:
            name = body['name']
            data = body['search']
            search_term = body['search_term']
            params = body['params']
            SavedSearch().create(user, name, data, search_term, params)
            return HttpResponse("Saved Successfully")
        except:
            return HttpResponseBadRequest("Error while saving! Invalid request body.")
    else:
        return HttpResponseBadRequest("This endpoint only accepts POST request")


def get_saved_search(request):
    if request.method == 'GET':
        try:
            limit = int(request.GET.get('limit'))
        except:
            limit = 10
        user = request.user
        try:
            data = serializers.serialize('json',
                SavedSearch.objects.filter(user=user).order_by('-time')[:limit],
                fields=('name', 'search_term', 'params', 'time'))
            return HttpResponse(data, content_type="application/json")
        except:
            return HttpResponseBadRequest("Error while getting saved seaches.")
    else:
        return HttpResponseBadRequest("This endpoint only accepts GET request")
