from django.http import HttpResponse
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
RESPONSE_TYPE = "code"
AUTHIF = "0"
ALLOWED_REDIRECT_URIS = {
    "www.dazn.com/account/last-step",
    "stag.dazn.com/account/last-step",
    "test.dazn.com/account/last-step"
}

@require_GET
def signin(request):
    for required_qp in REQUIRED_SIGNIN_QUERY_PARAMS:
        if required_qp not in request.GET:
            msg = u"Missing required parameter `{0}`".format(required_qp)
            return HttpResponse(msg, status=400)
    if request.GET['client_id'] != CLIENT_ID:
        msg = u"Invalid client_id, for testing use `{0}`".format(CLIENT_ID)
        return HttpResponse(msg, status=400) 
    if request.GET['redirect_uri'] not in ALLOWED_REDIRECT_URIS:
        msg = u"Invalid redirect_uri, should be one of `{0}`".format(list(ALLOWED_REDIRECT_URIS))
        return HttpResponse(msg, status=400)
    if request.GET['response_type'] != RESPONSE_TYPE:
        msg = u"Invalid response_type, should be `{0}`".format(RESPONSE_TYPE)
        return HttpResponse(msg, status=400) 
    if request.GET['authif'] != AUTHIF:
        msg = u"Invalid autif, should be `{0}`".format(AUTHIF)
    return render(request, 'common/signin.html', {
        'redirect_uri': request.GET['redirect_uri'],
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
        response['Location'] = "https://{0}?code={1}&state={2}".format(redirect_uri, "12345", state)
    else:
        response['Location'] = "https://{0}?error={1}".format(redirect_uri, "something-very-wrong")
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
