from django.http import HttpResponseForbidden

from django.http import QueryDict
import json


class RequestToApi:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if len(request.path) > 4 and '/api' == request.path[:4]:
            if request.method == 'POST':
                data = json.loads(request.body.decode('utf-8'))
                q_data = QueryDict('', mutable=True)
                for value in data:
                    q_data.update({value: data[value]})
                request.JSON = q_data
            if request.method == 'POST' or request.method == 'DELETE':
                # TODO или выпилить или в зависимость от settings
                setattr(request, '_dont_enforce_csrf_checks', True)

        response = self.get_response(request)

        return response
