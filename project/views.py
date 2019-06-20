from django import shortcuts
from django.core import urlresolvers


def index(request):
    return shortcuts.redirect(urlresolvers.reverse('home:index'))
