from django.shortcuts import render


# Create your views here.
from lists.models import Item


def home_page(request):   # TODO: Take care of the empty saves to the database
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()
    return render(
        request,
        'home.html',
        {'new_item_text': request.POST.get('item_text', '')}
    )
