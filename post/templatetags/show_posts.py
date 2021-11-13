from django.template import Library

register = Library()


@register.inclusion_tag("post/templatetags/show_posts.html")
def show_posts(posts):
    return {"posts": posts}
