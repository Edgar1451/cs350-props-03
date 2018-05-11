# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Property
from geopy.distance import distance
from geopy.geocoders import Nominatim
from .forms import LookupForm, GeoForm


# Show the all the properties in the db.

class PropertyListView(generic.ListView):
    model = Property
    template_name = "properties/list.html"

    def get_context_data(self, **kwargs):
        context = super(PropertyListView, self).get_context_data(**kwargs) 
        
        # The GET query param might be null. Proceed silently to exception clause
        try:
            q = self.request.GET['location'] 
            geolocator = Nominatim()

            # Retrieve Location object for submitted query in form
            loc = geolocator.geocode(q)
            if not loc:
                context['result'] = 'Location not found in Nominatim'
            else:
                # Write location object to template variable. See related template to view how this is displayed.
                context['result'] = loc
        except:
            pass

        return context

class PropertyDetailView(generic.DetailView):
    model = Property
    template_name = "properties/detail.html"


class PropertyCreateView(generic.CreateView):
    model = Property  # what type of object we are creating?
    template_name = "properties/create.html"  # the page to display the form.
    fields = ['prop_type', 'address', 'zip_code', 'description', 'picture_url', 'price',]
    success_url = reverse_lazy('properties:list')


class PropertyUpdateView(generic.UpdateView):
    model = Property  # what type of object we are editing?
    template_name = "properties/edit.html"  # the page to display the form.
    fields = ['prop_type', 'address', 'zip_code', 'description', 'picture_url', 'price',]
    success_url = reverse_lazy('properties:list')

class PropertyLookupView(generic.FormView):
    template_name = "properties/search.html"
    form_class = LookupForm


    def get_context_data(self, **kwargs):
        context = super(PropertyLookupView, self).get_context_data(**kwargs) 
        
        # The GET query param might be null. Proceed silently to exception clause
        try:
            q = self.request.GET['search'] 
            ls = []
            for i in Property.objects.all():
                if q in i.description: 
                    ls.append(i)
            context['Matches']= ls

        except:
            pass
        return context

class GeoView(generic.FormView):
    template_name = 'properties/search.html'
    form_class = GeoForm

    def get_context_data(self, **kwargs):
        context = super(GeoView, self).get_context_data(**kwargs) 
        
        # The GET query param might be null. Proceed silently to exception clause
        try:
            q = self.request.GET['address']  
            x = self.request.GET['miles']
            geolocator = Nominatim()
            qx = []
            # Retrieve Location object for submitted query in form
            loc = geolocator.geocode(q)
            for i in Property.objects.all():
                prop_loc = geolocator.geocode(i.address) #  get geocode for property.address > prop-loc
                d = distance((loc.latitude, loc.longitude), (prop_loc.latitude, prop_loc.longitude)).miles
                if d < int(x):
                    qx.append(i)
            context['Matches'] = qx
                    
            """if not loc:
                context['result'] = 'Location not found in Nominatim'
            else:
                # Write location object to template variable. See related template to view how this is displayed.
                context['result'] = loc"""
        except Exception as e:
            print e

        return context

