from ipware import get_client_ip


class SetCorrectIPMiddleware:
    """
    Make sure that django has the correct IP even if there is a proxy/CDN
    so we can rely on request.META["REMOTE_ADDR"] to get the correct remote IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        if ip is not None:
            request.META["HTTP_X_FORWARDED_FOR"] = ip
            request.META["REMOTE_ADDR"] = ip

        return self.get_response(request)
