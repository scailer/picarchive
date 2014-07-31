# -*- coding: utf-8 -*-

import os
import git
from django.conf import settings
from django.views import generic


class ProductInfoView(generic.TemplateView):
    template_name = 'info.html'

    def get_context_data(self, **kwargs):
        context = super(ProductInfoView, self).get_context_data(**kwargs)
        repo = git.Repo(os.path.join(settings.PROJECT_DIR, '.git'))
        context['repo'] = repo
        return context
