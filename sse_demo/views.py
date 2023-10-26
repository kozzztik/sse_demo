import json

import redis
from redis import asyncio as aioredis

from django_h2.sse import SSEResponse

from django.views import generic
from django.conf import settings
from django import http


class HomeView(generic.TemplateView):
    template_name = 'home.html'


channel_name = 'sse_channel'
id_counter = 'id_counter'


class SSEAPI(generic.View):
    def get(self, request):
        return RedisChannel(request).response

    def post(self, request):
        message = json.loads(request.body)
        client = redis.from_url(settings.REDIS_LOCATION)
        pk = client.incr(id_counter, 1)
        name = message['name']
        data = message['data']
        listeners = client.publish(
            channel_name,
            json.dumps({'id': pk, 'name': name, 'data': data})
        )
        return http.JsonResponse({'id': pk, 'listeners': listeners})


class RedisChannel:
    def __init__(self, request):
        self.response = SSEResponse(request, handler=self.handler())

    async def handler(self):
        redis = aioredis.from_url(settings.REDIS_LOCATION)
        pubsub = redis.pubsub()
        await pubsub.subscribe(**{channel_name: self._get_message})
        await pubsub.run(poll_timeout=30)

    async def _get_message(self, message):
        message = json.loads(message['data'])
        await self.response.send_event(
            message['name'],
            json.dumps(message['data']),
            event_id=message['id']
        )
