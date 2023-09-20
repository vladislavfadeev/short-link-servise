import uuid
from django.utils.deprecation import MiddlewareMixin


class UserUniqueUUID(MiddlewareMixin):
    
    def process_response(self, request, response):
        # check the '_uid' attribute in cookies, if it not
        # exist we set it. This is necessary for create
        # relation between not autheticate user and
        # new created link
        c = request.COOKIES
        if c.get('_uid'):
            return response
        uid = str(uuid.uuid4())
        response.cookies['_uid'] = uid
        return response
    

class UserIPAdressFromNginx(MiddlewareMixin):
    def process_request(self, request):
        request.META["REMOTE_ADDR"] = request.META.get("HTTP_FORWARDED_FOR")
        return request