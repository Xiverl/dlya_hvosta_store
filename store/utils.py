from store.models import Order


def get_instanse(form, instance):
    form.first_name = instance.first_name
    form.last_name = instance.last_name
    form.city = instance.city
    form.street = instance.street
    form.building = instance.building
    form.number_phone = instance.number_phone
    form.location = instance.location
    return form


def get_info_order(user):
    order = Order.objects.create(
        user=user,
        first_name=user.first_name,
        last_name=user.last_name,
        number_phone=user.number_phone,
        city=user.city,
        street=user.street,
        building=user.building,
        entrance=user.entrance,
        location=user.location
    )
    return order
