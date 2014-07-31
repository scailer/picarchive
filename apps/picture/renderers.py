# -*- coding: utf-8 -*-

from rest_framework import renderers
from . import tasks


class SendToMailRenderer(renderers.StaticHTMLRenderer):
    format = 'email'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get('request')
        pk_list = [x.get('id') for x in data['results']]

        # Запускаем асинхронную задачу
        tasks.send_pictures.apply_async((), {
            'email': request.user.email,
            'picture_pk_list': pk_list
        })

        return super(SendToMailRenderer,  self).render(
            u'Картинки отправлены на email',
            accepted_media_type, renderer_context)
