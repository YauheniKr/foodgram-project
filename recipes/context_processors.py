def shop_list_size(request):
    user = request.user
    count = user.purchase_by.all().count() if user.is_authenticated else 0
    return {'shop_list_size': count}
