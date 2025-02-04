from .models import Client

class AutoCreateClientProfile:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not hasattr(request.user, 'client_profile'):
            Client.objects.create(user=request.user)
        return self.get_response(request)