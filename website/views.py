from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from yelpapi import get_my_key
import requests

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        location = request.form.get('location')
        term=request.form.get('cuisine')
        #Gets the note from the HTML 
        API_KEY=get_my_key()
        ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
        HEADERS={'Authorization': 'bearer %s' %API_KEY}

        #define parameters
        PARAMETERS={'term':term,
                    'limit':50,
                    'radius':1000,
                    'location': location}

        #make a request to the yelp API

        response=requests.get(url=ENDPOINT, params=PARAMETERS,headers=HEADERS)
        #if response.status_code == 200:
        data = response.json()
        return render_template('results.html', restaurants=data['businesses'])
            # Pass the API data to the template for rendering
    return render_template('home.html', user=current_user)


