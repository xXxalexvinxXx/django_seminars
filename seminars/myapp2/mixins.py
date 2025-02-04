from django.core.exceptions import PermissionDenied

class ClientRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'client_profile'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)