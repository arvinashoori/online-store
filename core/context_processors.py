from .models import Category 


def menu_urls(request):
    urls = Category.objects.all()
    return dict(urls=urls)