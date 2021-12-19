from django.template import Library

register = Library()


@register.inclusion_tag("templatetags/show_profile_photo.html")
def show_profile_photo(account, classes="", alt=""):
    return {"account": account, "classes": classes, "alt": alt}
