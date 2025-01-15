import requests
from httplib2.auth import params


class HTTPHandler(object):

    def forward_request(self, request):
        return self.perform_request(
            url=request.url,
            method=request,
            headers=request.headers,
            params=request.params,
            body=request.json()
        )

    def perform_request(self, url, method, headers=None, params=None, body=None, other_args=None):
        args = {
            'url': url,
            'method': method,
        }
        if headers:
            args['headers'] = headers
        if params:
            args['params'] = params
        if body:
            if isinstance(body, dict):
                args['json'] = body
            else:
                args['data'] = body
        if other_args:
            args.update(other_args)

        print(f'Performing request {args}', flush=True)
        resp = requests.request(**args)
        print(f'Received response {resp.status_code} - {resp.text}', flush=True)
        resp.raise_for_status()
        return resp

http_handler_obj = HTTPHandler()