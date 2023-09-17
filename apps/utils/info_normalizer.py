
def get_user_info(request):
    try:
        device = (str(request.user_agent).split("/")[0]).strip()
    except:
        pass
    else:
        user_info_model = {
            'user_agent_unparsed': str(request.user_agent),
            'device': device,
            'os': request.user_agent.os.family,
            'browser': request.user_agent.browser.family,
            'ref_link': request.META.get("HTTP_REFERER", "Not defined"),
            'user_ip': request.META.get("REMOTE_ADDR", "Not defined"),
        }
        return user_info_model
