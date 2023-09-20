from apps.utils import requester


def get_user_info(request):
    try:
        device = (str(request.user_agent).split("/")[0]).strip()
    except:
        pass
    else:
        user_info_model = {
            'user_agent_unparsed': str(request.user_agent),
            'device': device,
            'os': str(request.user_agent.os.family),
            'browser': str(request.user_agent.browser.family),
            'ref_link': requester.extract_domain(request.META.get("HTTP_REFERER")),
            'user_ip': str(request.META.get("REMOTE_ADDR", "Undefined")),
        }
        return user_info_model
