from django import shortcuts


def index(request):
    return shortcuts.render(
        request=request,
        context={},
        template_name='home/index.html'
    )
