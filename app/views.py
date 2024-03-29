

# Create your views here.

from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render
from decimal import *

import json
import smtplib
import base64
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import TemplateView
from datetime import date, datetime

from calendar import monthrange
from .models import UserProfile, Items, Transactions, Project, Bid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from django.db.models import Sum


@login_required
def home(request):
    context = {}
    user_profile = UserProfile.objects.get(user=request.user)
    current_date = datetime.now()
    month, year, day = current_date.strftime("%m"), current_date.now().strftime("%Y"), current_date.now().strftime("%d")
    bids = Bid.objects.exclude(bid_user=user_profile).filter(bidder='N')
    if bids:
        min_amt = min(user_profile.credit_balance, bids[0].bid_qty)
    else:
        min_amt = user_profile.credit_balance
 
    context.update({'user_profile': user_profile,'bids':bids,'min_amt':min_amt})
    return render(request, 'index.html', context)

def about_us(request):
    context = {}
    return render(request, 'about_us.html', context)

@login_required
def contact_us(request):
    context = {}
    return render(request, 'contact_us.html', context)

@login_required
def flight_booking(request):
    context = {}
    return render(request, 'flight_booking.html', context)

@login_required
def train_booking(request):
    context = {}
    return render(request, 'train_booking.html', context)

@login_required
def bus_booking(request):
    context = {}

    print ("request ", request.POST)
    
    return render(request, 'bus_booking.html', context)

@login_required
def fertilizers(request):
    context = {}
    return render(request, 'fertilizers.html', context)

@login_required
def fuel(request):
    context = {}
    return render(request, 'fuel.html', context)

@login_required
def recycle(request):
    context = {}
    return render(request, 'recycle.html', context)


@login_required
def go_green_kitty(request):
    trans = Transactions.objects.aggregate(total_price=Sum('green_amount'))
 
  
                            
    prjs = Project.objects.all()
    pr = Project.objects.aggregate(total_price=Sum('amount'))
    tot  = trans.get('total_price') - pr.get('total_price')
    context = {'trans': tot, 'prjs': prjs}
    return render(request, 'green_kitty.html', context)

@login_required
def reports(request):
    trans = Transactions.objects.aggregate(total_price=Sum('green_amount'))
    pr = Project.objects.aggregate(total_price=Sum('amount'))
    tot  = trans.get('total_price') - pr.get('total_price')
    prjs = Project.objects.all()
    context = {'trans': tot, 'prjs': prjs}
    return render(request, 'reports.html', context)

@login_required
def investments(request):
    trans = Transactions.objects.aggregate(total_price=Sum('green_amount'))
    pr = Project.objects.aggregate(total_price=Sum('amount'))
    tot  = trans.get('total_price') - pr.get('total_price')
    context = {'trans': tot}
    if request.POST:
        prj_name = request.POST.get('prj_name')
        amount = request.POST.get('amount') 
        category = request.POST.get('category')
        region = request.POST.get('region')
        prj_obj = Project()
        prj_obj.project_name = prj_name
        prj_obj.category = category
        prj_obj.region = region
        prj_obj.amount = int(amount)
        prj_obj.save()        
        return HttpResponseRedirect('/go-green-kitty/')
    return render(request, 'invest.html', context)

@login_required
def dbmall(request):
    print ("request ", request)
    items = Items.objects.all()
    context = {'items': items}
    return render(request, 'dbmall.html', context)

@login_required
def transfer_credit(request):
    user = UserProfile.objects.get(user=request.user)
    context = {'user': user, 'user_profiles': UserProfile.objects.exclude(user=request.user)}
    if request.POST:
        account_number = request.POST.get('account')
        amount = request.POST.get('amount')
        cash = request.POST.get('cash_amount')
        up = UserProfile.objects.get(account_number=account_number) 
        up.credit_balance = up.credit_balance + int(amount)
        user.credit_balance = user.credit_balance - int(amount)
        up.cash_balance = up.cash_balance - int(cash) * int(amount)
        user.cash_balance = user.cash_balance + int(amount)*int(cash)
        up.save()
        user.save()
        return HttpResponseRedirect('/') 

    return render(request, 'transfer_credit.html', context)

@login_required
def buy(request, item_id=None):
    item = get_object_or_404(Items, id=item_id)
    user = UserProfile.objects.get(user=request.user)
    user.save()
    if request.POST:
        obj = Transactions()
        obj.item = item
        obj.qty = Decimal(request.POST.get('qty', '0.0'))
        obj.total_price = item.item_price * obj.qty
        obj.rounded_price = Decimal(request.POST.get('total_price', '0.0'))
        total_carbon_credit = user.credit_balance - obj.qty*item.carbon_credits
        user.credit_balance = total_carbon_credit
        total_cash_balance = user.cash_balance - obj.rounded_price 
        user.cash_balance = total_cash_balance
        user.save()
        obj.green_amount = obj.rounded_price - obj.total_price
        obj.green_points = 0
        obj.user_profile = user
        obj.save() 
        return HttpResponseRedirect('/transactions/') 
    return render(request, 'payment.html', {'item': item, "user":user})

def accept_bid(request, user_id):
    logged_user = UserProfile.objects.get(user=request.user)
    user = get_object_or_404(UserProfile, id=user_id)
    if request.POST:
        acpt_qty = request.POST.get('acpt_qty')
        acpt_amt = request.POST.get('acpt_amt')
        bid = request.POST.get('bid')
        logged_user.credit_balance = logged_user.credit_balance - int(acpt_qty)
        logged_user.cash_balance = logged_user.cash_balance + Decimal(acpt_amt)
        user.credit_balance = user.credit_balance + int(acpt_qty)
        user.cash_balance = user.cash_balance - Decimal(acpt_amt)
        bid = Bid.objects.get(id=bid)
        #bid.accepted = user
        bid.accepted_flag = 'Y'
        bid.bidder = 'Y'
        bid.save()
        logged_user.save()
        user.save()
        return HttpResponseRedirect('/')

@login_required
def bid(request):
    trans = Transactions.objects.aggregate(total_price=Sum('green_amount'))
    user = UserProfile.objects.get(user=request.user)
    context = {'trans': trans,'user':user}
    if request.POST:
        bid_qty = request.POST.get('bid_qty')
        bid_price= request.POST.get('bid_price')
        bid_amount = request.POST.get('bid_amount')
        
        prj_obj = Bid()
        prj_obj.bid_qty = bid_qty
        prj_obj.price = Decimal(bid_price)
        prj_obj.amount = Decimal(bid_amount)
        prj_obj.bid_user = user
        prj_obj.bidder = 'Y'
        #prj_obj.accepted = user
        prj_obj.accepted_flag = 'N'
        prj_obj.save()
        sellers = UserProfile.objects.filter(credit_balance__gte=0).exclude(user=request.user)
        for x in sellers:
            prj_obj = Bid()
            prj_obj.bid_qty = bid_qty
            prj_obj.price = Decimal(bid_price)
            prj_obj.amount = Decimal(bid_amount)
            prj_obj.bid_user = UserProfile.objects.get(user=x.user)
            prj_obj.bidder = 'N'
            prj_obj.save() 

        return HttpResponseRedirect('/')

    return render(request, 'bid.html', context)

@login_required
def transactions(request):
    user = UserProfile.objects.get(user=request.user)

    trans = Transactions.objects.filter(user_profile=user)
    return render(request, 'trans.html', {'trans': trans})
