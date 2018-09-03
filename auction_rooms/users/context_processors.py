def favourites(request):
    if request.user.is_authenticated:
        return {'favourites': request.user.get_favourites()}
    return []
