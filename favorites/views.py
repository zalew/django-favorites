from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from models import Favorite


@login_required
def create_favorite(request, object_id, queryset, redirect_to=None,
        template_name=None, extra_context=None):
    """
    Generic `add to favorites` view

    `queryset` - required for content object retrieving
    `redirect_to` is set to `favorites` by default - change it if needed

    Raises Http404 if content object does not exist.

    Example of usage (urls.py):
        url(r'favorites/add/(?P<object_id>\d+)/$', 
            'favorites.views.create_favorite', kwargs={
                'queryset': MyModel.objects.all(),
            }, name='add-to-favorites')
        
    """
    obj = get_object_or_404(queryset, pk=object_id)
    content_type=ContentType.objects.get_for_model(obj)

    if Favorite.objects.filter(content_type=content_type, object_id=object_id):
        return redirect(redirect_to or 'favorites')

    favorite = Favorite.objects.create_favorite(obj, request.user)
    return redirect(redirect_to or 'favorites')


@login_required
def favorite_list(request, model_class, **kwargs):
    """
    Generic `favorites list` view based on generic object_list

    `model_class` - required valid model class
    `template_name` - default is "favorites/favorite_list.html"
                      used by generic object_list view

    Other parameters are same as object_list.

    Example of usage (urls.py):
        url(r'favorites/my_model/$', 
            'favorites.views.favorite_list', kwargs={
                'template_name': 'favorites/mymodel_list.html',
                'model_class': get_model('my_app.MyModel'),
                'paginate_by': 25,
            }, name='favorites-mymodel')
    """
    queryset = kwargs.get('queryset',Favorite.objects.favorites_for_model(
        model_class, request.user))
    return object_list(request, queryset, **kwargs)


