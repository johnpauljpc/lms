from django import template
import math
register = template.Library()


@register.simple_tag
def discount_calculation(price, discount):
    if not discount or discount <= 0:
        return price
    if discount >= 100:
        return 0
    sellprice = price - (price * discount / 100)
    return math.floor(sellprice)


@register.filter
def naira(value):
    if value is None:
        value = 0
    try:
        value = int(value)
    except (TypeError, ValueError):
        return '₦0'
    return '₦{:,.0f}'.format(value).replace(',', ',')