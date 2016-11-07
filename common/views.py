from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render

def signin(request):
    return render(request, 'common/signin.html')

def signin_continue(request):
    print "whatevr..."
    return render(request, 'common/signin_continue.html')

@require_POST
def signin_process(request):
    response = HttpResponse("", status=302)
    if request.POST['username'] == "docomo" and request.POST['password'] == "docomo":
        response['Location'] = "https://dazn.com/account/docomo/signin/?token=12345"
    else:
        response['Location'] = "https://dazn.com/account/docomo/signin/?error=loginfailed"
    return response

def signup(request):
    return render(request, 'common/signup.html')

def signup_continue(request):
    return render(request, 'common/signup_continue.html')

@require_POST
def signup_process(request):
    response = HttpResponse("", status=302)
    response['Location'] = 'https://dazn.com/docomo/'
    return response
