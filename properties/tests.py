# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from django.test import Client
from django.urls import reverse
from django.utils.http import urlencode


class TestGeoqueryViews(TestCase):
    """The following unit tests validate that query views execute as expected.
        The unit tests follow the explanation given in the django tutorial listed below with modifications relevant to our query form setup.

        https://docs.djangoproject.com/en/2.0/intro/tutorial05/#test-a-view
    """
    fixtures = ['property-testdata']
    def test_lookup_success_view(self):
        #  create the client simulator
        client = Client()

        #  fake form data by building a query parameter string 
        #  using a dictionary giving location=1314+chavez+st%2C+las+vegas%2C+nm
        query_str = urlencode({'search':'bed'})
        
        #  build a complete url pattern from named pattern, 'lookup'. See geopydemo/urls.py
        #  then append the query parameter string
        #  should give: /lookup/?location=1314+chavez+st%2C+las+vegas%2C+nm
        url = reverse('properties:search') + '?' + query_str
        
        #  fake a client request to url and get response object (what is sent to browser from the associated view)
        response = client.get(url)

        #  Grab the context variable known as 'result'. See geoquery/views.py
        result_var = response.context['Matches']

        #  Verify that the result represents a match - a match was found for the given address...    
        self.assertEqual(len(result_var), 4)

    def test_GeoView(self):
        #  create the client simulator
        client = Client()

        #  fake form data by building a query parameter string 
        #  using a dictionary giving location=1314+chavez+st%2C+las+vegas%2C+nm
        query_str = urlencode({'address':'1009 diamond, las vegas, nm', 'miles':20})
        
        #  build a complete url pattern from named pattern, 'lookup'. See geopydemo/urls.py
        #  then append the query parameter string
        #  should give: /lookup/?location=1314+chavez+st%2C+las+vegas%2C+nm
        url = reverse('properties:distance') + '?' + query_str
        
        #  fake a client request to url and get response object (what is sent to browser from the associated view)
        response = client.get(url)

        #  Grab the context variable known as 'result'. See geoquery/views.py
        result_var = response.context['Matches']

        #  Verify that the result represents a match - a match was found for the given address...    
        self.assertEqual(len(result_var), 1)