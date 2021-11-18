from django.template import Library

register = Library()


@register.inclusion_tag("templatetags/show_posts.html")
def show_posts(posts, is_go_deeper=False):
    return {"posts": posts, "is_go_deeper": is_go_deeper}
