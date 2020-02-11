from django import template

register = template.Library()


COIN_OFFSET_PIXELS = 9
TOPMOST_OFFSET_PIXELS = 130


@register.filter(name="get_coin_offset")
def coin_offset(coin_num):
    """
    Calculate the top pixel offset of a coin based on its number in the total
    array of coins.
    """
    return TOPMOST_OFFSET_PIXELS - (COIN_OFFSET_PIXELS * coin_num)
