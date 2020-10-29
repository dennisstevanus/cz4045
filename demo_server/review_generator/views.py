import logging

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from django.views import View

from . import utils


class ReviewGeneratorView(View):
    template = loader.get_template('review_generator/index.html')

    def get(self, request, *args, **kwargs):
        context = {
            'sample': 'abc sample here'
        }
        return HttpResponse(self.template.render(context, request))

    def post(self, request, *args, **kwargs):
        input_text = request.POST['prefix']
        logging.info(input_text)
        response = utils.generate_fake_review(input_text)
        context = {
            'review': response
        }

        return HttpResponse(self.template.render(context, request))
