from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from .models import Auction
from .models import Bid
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from time import time
from django.template import RequestContext
import datetime
from django.contrib.auth.hashers import check_password
from django.utils import translation
from django.core.mail import send_mail
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from serializer import myserializer

sender_email= 'sasghar@abo.fi'

def MyAuctions(request):
    if request.user.is_authenticated():
        dbData= Auction.objects.filter(authName=request.user.username)
        dbuser= User.objects.get(username=request.user.username)
        if dbuser.is_superuser == False:
            return render(request, 'view_all.html',
                          {'data': dbData,'msg':'',
                           'req':session_info(request),
                           'loggedin':1})
        else:
            return render(request, 'view_all.html',
                          {'data': dbData,
                           'req': session_info(request),
                           'msg':'',
                           'loggedin':2})
    else:
        return HttpResponse('Bad Request', status = 404)

def Auctions(request):
    dbData = Auction.objects.all()
    if request.user.is_authenticated():
        dbuser= User.objects.get(username=request.user.username)
        if dbuser.is_superuser == False:
            dbData = Auction.objects.filter(is_banned=False)
            return render(request, 'view_all.html',
                          {'data': dbData,
                           'msg':'',
                           'req':session_info(request),
                           'loggedin':1})
        else:
            return render(request, 'view_all.html',
                          {'data': dbData,
                           'msg':'',
                           'req':session_info(request),
                           'loggedin':2})
    else:
         dbData = Auction.objects.filter(is_banned=False)
         return render(request,
                       'view_all.html',
                       {'data': dbData,
                        'msg':'',
                        'req':session_info(request),
                        'loggedin':0})

def editpswd(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'change_password.html')
        else:
            return render(request, 'login.html', {'error': 'You should Login First'})
    elif request.method == 'POST':
        if request.user.is_authenticated():
            dbData= User.objects.get(username=request.user.username)
            oldpswd=request.POST['oldpswd']
            newpswd=request.POST['newpswd']
            if check_password(oldpswd,dbData.password):
                dbData.set_password(newpswd)
                dbData.save()
                dbData1= Auction.objects.filter(authName=request.user.username)
                return render(request, 'view_all.html', {'data': dbData1,'msg':'Your Passwrod Has been Updated But You Are Logged Out Now.... Please Login Again.','req':session_info(request), 'loggedin':1},context_instance= RequestContext(request))
            else:
                return render(request, 'change_password.html', {'msg':'Old Password is Incorrect... please re-enter','req':session_info(request), 'loggedin':1},context_instance= RequestContext(request))
        else:
            return render(request, 'login.html', {'error': 'You should Login First'})

def editemail(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            user= User.objects.get(username=request.user.username)
            user.email=request.POST['email']
            user.save()
            dbData= Auction.objects.filter(authName=request.user.username)
            return render(request, 'view_all.html',
                          {'data': dbData,
                           'msg':'Your Email has been updated in Database.',
                           'req':session_info(request), 'loggedin':1})
        else:
            return render(request, 'login.html', {'error': 'You should Login First'})
    if request.method == 'GET':
        if request.user.is_authenticated():
            user= User.objects.get(username=request.user.username)
            return render(request, 'change_email.html',{'data': user})
        else:
            return render(request, 'login.html', {'error': 'You should Login First'})

def allblogs(request):

    if request.user.is_authenticated():
        dbData= Auction.objects.filter(authName=request.user.username)
        return render(request, 'view_all.html',
                      {'data': dbData,'msg':'New Auction has been added','req':session_info(request), 'loggedin':1})
    else:
        dbData = Auction.objects.all()
        return render(request, 'view_all.html',
                      {'data': dbData,'msg':'New Auction has been added','req':session_info(request), 'loggedin':0})


def single_auction(request, id):
        Id = id
        try:
           auctiondata = Auction.objects.get(id=Id)
           biddata = Bid.objects.filter(auction=Id)
        except Exception as p:
            return HttpResponse('Bad request pal! Item no exist.', status = 404)
        view = request.session.get('view', 0)
        request.session['view'] = view + 1
        return render(request, 'singleauction.html', {"data": auctiondata,'bidData':biddata,'req':session_info(request)});

def email(to, title, id ):
    body = "New auction has been created at:" \
           " http://127.0.0.1:8000/myauction/" + \
           str(id)
    send_mail('Fresh Auction Email', body, sender_email, [to], fail_silently=False)
    return HttpResponse('The email has been sent')

def delete_auction(request, id):
    if request.user.is_authenticated():
        Id = id
        try:
            Auction.objects.get(id=Id,authName=request.user.username)
        except Exception as p:
            return HttpResponse('Bad request pal! Item no exist.', status = 404)
        try:
            delete = request.session.get('delete', 0)
            request.session['delete'] = delete + 1
            Auction.objects.filter(pk=id,authName=request.user.username)[0].delete()
            return HttpResponseRedirect('/myauction/')
        except:
            return HttpResponse('Not allowed to delete the blog', status = 404)
    else:

            return render(request, 'login.html', {'error': 'You should login first'})

def bannedauction(request, id):
    if request.method=='GET':
        if request.user.is_authenticated():
            dbuser= User.objects.get(username= request.user.username)
            auction= Auction.objects.get(id=id)
            if dbuser.is_superuser:
                auction.is_banned=True
                auction.save()
                return HttpResponseRedirect('/allauction/')
            else:
                return render(request, 'login.html', {'error': 'Please Login with Super User...'})

def changelanguage(request, lang_code):
    languagecode = lang_code
    translation.activate(languagecode)
    request.session[translation.LANGUAGE_SESSION_KEY] = languagecode
    return HttpResponseRedirect('/allauction/')

def changeLanguagePage(request):
    if (request.user.is_authenticated()):
        return render(request, 'language.html')
    else:
        return render(request, 'language.html')


def editAuction(request, id):
    if request.user.is_authenticated():
        Id = id
        try:
           dbData = Auction.objects.get(id=Id)
        except Exception as p:
            return HttpResponse('Bad request pal! Item no exist.', status = 404)
        try:
           auction = Auction.objects.filter(pk=Id,authName=request.user.username)[0]

           if request.method == 'GET' and dbData.tala==False:
               auction.tala=True
               auction.save()

               return render(request, 'edit_auction.html',
                             {"data": dbData,
                              'req':session_info(request)})

           if request.method== 'GET' and dbData.tala==True:
               return HttpResponse('The auction is currently in being edited',
                                   status = 404)

           if request.method == 'POST':
               edit = int(request.session.get('edit', 0))
               request.session['edit'] = edit + 1
               auction.title = request.POST['title']
               auction.desc = request.POST['desc']
               auction.createdAt = timezone.now()
               auction.tala=False
               auction.min_price= request.POST['desc']
               auction.save()
               return HttpResponseRedirect('/myauction')

        except Exception as p:
            return HttpResponse('User is not authorized to Edit!', status = 404)
    else:
        return render(request, 'login.html', {'error': 'You should Login First'})



def reset(request, action = None):
    if action == 'reset' and request.method == 'POST':
            request.session.flush()
            return HttpResponseRedirect('/myauction')
def addAuction(request):
    if request.method == 'GET':
        return render(request,'add.html')
    if request.method == 'POST':
        if request.user.is_authenticated():
           newAuction = Auction()
           newAuction.title = request.POST['title']
           newAuction.desc= request.POST['desc']
           newAuction.authName=request.user.username
           newAuction.seller=request.user
           newAuction.min_price=request.POST['minprice']
           newAuction.deadline=request.POST['deadline']
           newAuction.createdAt=timezone.now()
           newAuction.save()
           to=request.user.email
           title=request.POST['title']
           auction = Auction.objects.get(title=title,authName=request.user.username)
           email(to,title,auction.id)
           add = request.session.get('add', 0)
           request.session['add'] = add + 1
           return HttpResponseRedirect('/myauction/')
        else:
            return render(request, 'login.html', {'error': 'You should Login First'})
    else:
        return HttpResponseRedirect('/myauction/')

def session_info(request):

        ses = request.session
        return {'session_start': datetime.datetime.fromtimestamp(int(ses.get('time', time()))),
                'blog_visited': int(ses.get('view', 0)),
                'blog_edited': int(ses.get('edit', 0)),
                'blog_created': int(ses.get('add', 0)),
                'blog_deleted': int(ses.get('delete', 0)),
                'blog_start': int(ses.get('start', 0))}

def newuser(request):

    if request.method == 'POST':

        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password,
                                        first_name=name,email=email)
        user.save()

        return HttpResponseRedirect('/allauction/')
    else:
        return render(request, 'signup.html')

def UserCreated(request, action = None):
    if action == 'newuser' and request.method == 'POST':
            return HttpResponseRedirect('/myauction/')


def userlogin(request , action = None):

    if request.method == 'POST':
        username = request.POST['username']

        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:

            auth.login(request,user)

            return HttpResponseRedirect('/myauction/')
        else:
            return HttpResponse('user not exist', status = 404)
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return HttpResponse("Logged out successfully")


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def search(request):
    if request.method == 'POST':
        try:
            title = request.POST['title']
            dbData = Auction.objects.get(title=title)
            view = request.session.get('view', 0)
            request.session['view'] = view + 1
            return render(request, 'singleauction.html', {"data": dbData, 'bidData': '', 'req': session_info(request)})
        except Exception as p:
            return HttpResponse('Bad request pal! Item no exist.', status=404)

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def search_api(request):

    if request.method=='POST':

        data = request.data

        try:
                title = data['title']
                dbData = Auction.objects.get(title=title)
                view = request.session.get('view', 0)
                request.session['view'] = view + 1
                serializer = myserializer(dbData)
                return JSONResponse(serializer.data)

        except Exception as p:
                return JSONResponse('Bad request pal. Item no exist.', status = 404)

def bid_auction_helper(request, id, data, responseWriter=HttpResponse, redirector=None):
    if request.user.is_authenticated():
        id = data.get('auction',id)
        try:
            dbData = Auction.objects.get(id=id)
        except Exception as p:
            return responseWriter({'Message': 'Auction no exists'})
        try:
            Auction.objects.filter(pk=id)[0]
            if request.method == 'POST' and dbData.authName != request.user.username:
                edit = int(request.session.get('edit', 0))
                request.session['edit'] = edit + 1
                price = data['price']
                if float(price) < dbData.min_price:
                    return responseWriter({'Message': 'Bid too low'})
                if float(price) > dbData.min_price:

                    try:
                        biddata = Bid.objects.filter(auctionid=id)
                        x = 0.0
                        y = 0.0
                        for bid in biddata:
                            if bid.price >= y:
                                y = bid.price
                        if y > float(price):
                            message ='Your Bid is too low'
                            if redirector:
                                return responseWriter(message)
                            else:
                                return responseWriter({'Message':message})
                        if float(price) > y:
                            for bid in biddata:
                                if bid.bidder == request.user.username:
                                    message='You have already Bid for this Auction'
                                    if redirector:
                                        return responseWriter(message)
                                    else:
                                        return responseWriter({'Message': message})
                            bid = Bid()
                            bid.price = price
                            bid.auctioner = dbData.authName
                            bid.auction = dbData.id
                            bid.bidder = request.user.username
                            bid.save()
                            message='Your Bid Successfully Added'
                            if redirector:
                                return redirector('/myauction/' + str(id))
                            else:
                                return responseWriter({'Message': message})
                    except Exception as p:

                        bid = Bid()
                        bid.price = price
                        bid.auctioner = dbData.authName
                        bid.auction = dbData.id
                        bid.bidder = request.user.username
                        bid.save()
                        message = 'Your Bid Successfully Added'
                        if redirector:
                            return redirector('/myauction/' + str(id))
                        else:
                            return responseWriter({'Message': message})

            if request.method == 'POST' and dbData.authName == request.user.username:
                message='Owner not allowed to bid in an auction'
                if redirector:
                    return responseWriter(message)
                else:
                    return responseWriter({'Message': message})
        except Exception as p:
            message='UnAuthorized to bid for this auction'
            if redirector:
                return responseWriter(message)
            else:
                return responseWriter({'Message': message})
    else:
        message = 'Login First'
        if redirector:
            return render_to_response(request, 'login.html', {'error': message})
        else:
            return responseWriter({'Message': message})

def bid_auction(request, id):
    return bid_auction_helper(request, id, request.POST, HttpResponse, HttpResponseRedirect)

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def bid_auction_api(request):
    data = request.data
    return bid_auction_helper(request, None, data, JSONResponse, None)