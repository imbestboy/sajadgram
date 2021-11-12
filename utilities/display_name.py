import random, string


def post_display_name_maker():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))
