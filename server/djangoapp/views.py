# Uncomment the required imports before adding the code

# from django.shortcuts import render
# from django.http import HttpResponseRedirect, HttpResponse
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth import logout
# from django.contrib import messages
# from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
import logging
import json
from django.views.decorators.csrf import csrf_exempt

from .populate import initiate
from .models import CarMake, CarModel

# ✅ REST API helper'ları
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST method is allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    username = data.get("userName")
    password = data.get("password")

    if not username or not password:
        return JsonResponse({"userName": username, "status": "Failed"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({"userName": username, "status": "Failed"}, status=401)

    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)


@csrf_exempt
def logout_user(request):
    if request.method != "GET":
        return JsonResponse({"message": "Only GET method is allowed"}, status=405)

    logout(request)
    data = {"userName": ""}
    return JsonResponse(data, status=200)


# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST method is allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"message": "Invalid JSON"}, status=400)

    username = data.get("userName")
    password = data.get("password")
    first_name = data.get("firstName")
    last_name = data.get("lastName")
    email = data.get("email")

    if not username or not password:
        return JsonResponse({"userName": username, "status": "Failed"}, status=400)

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except User.DoesNotExist:
        logger.debug(f"{username} is new user")

    if not username_exist:
        user = User.objects.create_user(
            username=username,
            first_name=first_name or "",
            last_name=last_name or "",
            password=password,
            email=email or ""
        )
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"}, status=400)


def get_cars(request):
    # If there are no CarModel records, populate initial data.
    if CarModel.objects.count() == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make").all()
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    return JsonResponse({"CarModels": cars}, status=200)


# Update the `get_dealerships` render list of dealerships all by default,
# particular state if state is passed
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state

    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    # if dealer id has been provided
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)

        # Her review için sentiment ekle
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail["review"])
            print(response)
            review_detail["sentiment"] = response["sentiment"]

        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


@csrf_exempt
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"message": "Only POST method is allowed"}, status=405)

    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            print(response)
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Exception:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
