from .models import Cart

def check_cart_existing(view):
    def wrap(self, request, *args, **kwargs):
        if request.user.is_authenticated and \
                not hasattr(request.user, 'cart'):
            Cart.objects.create(user=request.user)
        return view(self, request, *args, **kwargs)
    return wrap