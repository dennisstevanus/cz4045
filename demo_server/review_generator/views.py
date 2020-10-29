import logging
from django.views.generic import TemplateView

from . import utils


class ReviewGeneratorView(TemplateView):
    template_name = 'review_generator/index.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        input_text = request.POST['prefix']
        logging.info(input_text)
        response = utils.generate_fake_review(input_text)

        context['review'] = response

        return self.render_to_response(context)
