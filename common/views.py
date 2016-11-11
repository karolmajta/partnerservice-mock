import base64
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render

REQUIRED_SIGNIN_QUERY_PARAMS = {
    'scope',
    'response_type',
    'client_id',
    'redirect_uri',
    'state',
    'nonce',
    'authif',
}
CLIENT_ID = "s6BhdRkqt3"
CLIENT_SECRET = "12345"
RESPONSE_TYPE = "code"
GRANT_TYPE = "authorization_code"
AUTHIF = "0"
ALLOWED_REDIRECT_URIS = {
    "dazn.com/account/last-step",
    "www.dazn.com/account/last-step",
    "stag.dazn.com/account/last-step",
    "test.dazn.com/account/last-step"
}
LOCALHOST_REGEX = r'^localhost([:]{0,1})(\d*)/account/last-step$'

@require_GET
def signin(request):
    for required_qp in REQUIRED_SIGNIN_QUERY_PARAMS:
        if required_qp not in request.GET:
            msg = u"Missing required parameter `{0}`".format(required_qp)
            return HttpResponse(msg, status=400)
    if request.GET['client_id'] != CLIENT_ID:
        msg = u"Invalid client_id, for testing use `{0}`".format(CLIENT_ID)
        return HttpResponse(msg, status=400) 
    redirect_uri = request.GET['redirect_uri']
    redirect_uri_is_production = redirect_uri in ALLOWED_REDIRECT_URIS
    redirect_uri_is_development = re.match(LOCALHOST_REGEX, redirect_uri)
    if not redirect_uri_is_production and not redirect_uri_is_development:
        msg = u"Invalid redirect_uri, should be one of `{0}` or localhost<:*>/account/last-step.".format(list(ALLOWED_REDIRECT_URIS))
        return HttpResponse(msg, status=400)
    if request.GET['response_type'] != RESPONSE_TYPE:
        msg = u"Invalid response_type, should be `{0}`".format(RESPONSE_TYPE)
        return HttpResponse(msg, status=400) 
    if request.GET['authif'] != AUTHIF:
        msg = u"Invalid autif, should be `{0}`".format(AUTHIF)
    scheme = "http" if redirect_uri_is_development else "https"
    return render(request, 'common/signin.html', {
        'redirect_uri': "{0}://{1}".format(scheme, redirect_uri),
        'state': request.GET['state']
    })

@require_GET
def signin_continue(request):
    return render(request, 'common/signin_continue.html', {
        'redirect_uri': request.GET['redirect_uri'],
        'state': request.GET['state']
    })

@require_POST
def signin_process(request):
    response = HttpResponse("", status=302)
    redirect_uri = request.POST['redirect_uri']
    state = request.POST['state']
    if request.POST['username'] == "docomo" and request.POST['password'] == "docomo":
        response['Location'] = "{0}?code={1}&state={2}".format(redirect_uri, "12345", state)
    else:
        response['Location'] = "{0}?error={1}".format(redirect_uri, "something-very-wrong")
    return response

@require_GET
def signup(request):
    return render(request, 'common/signup.html')

@require_GET
def signup_continue(request):
    return render(request, 'common/signup_continue.html')

@require_POST
def signup_process(request):
    response = HttpResponse("", status=302)
    response['Location'] = 'https://dazn.com/docomo/'
    return response

@csrf_exempt
@require_POST
def token(request):
    if request.META.get('HTTP_AUTHORIZATION', None) != 'Basic {0}'.format(base64.b64encode(CLIENT_ID + CLIENT_SECRET)):
        msg = u"Invalid `Authorization` header"
        return HttpResponse(msg, status=401)
    if request.POST.get('grant_type', None) != GRANT_TYPE:
        msg = u"`grant_type` parameter should be `{0}`".format(GRANT_TYPE)
        return HttpResponse(msg, status=400)
    if not request.POST.get('code', None) or len(request.POST['code']) != 5:
        msg = u"invalid `code` parameter"
        return HttpResponse(msg, status=401)
    redirect_uri = request.POST.get('redirect_uri', "")
    redirect_uri_is_production = redirect_uri in ALLOWED_REDIRECT_URIS
    redirect_uri_is_development = re.match(LOCALHOST_REGEX, redirect_uri)
    if not redirect_uri_is_production and not redirect_uri_is_development:
        msg = u"Invalid redirect_uri, should be one of `{0}` or localhost<:*>/account/last-step.".format(list(ALLOWED_REDIRECT_URIS))
        return HttpResponse(msg, status=400)
    return JsonResponse({
        'access_token': str(uuid.uuid4()),
        'token_type': "Bearer",
        'expires_in': 90*24*60*60,
        'scope': '',
        'id_token': str(uuid.uuid4())
    })
