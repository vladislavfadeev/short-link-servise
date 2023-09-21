import uuid
from django.utils.deprecation import MiddlewareMixin


class UserUniqueUUIDMiddleware(MiddlewareMixin):
    
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
    

class SetRealRemoteAddrMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_REAL_IP']
        except KeyError:
            pass
        else:
            real_ip = real_ip.split(",")[0]
            request.META['REMOTE_ADDR'] = real_ip
