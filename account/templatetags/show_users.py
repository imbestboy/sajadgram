from django.template import Library

register = Library()


@register.inclusion_tag("templatetags/show_users.html")
def show_users(accounts, is_go_deeper=False, followers=False):
    if is_go_deeper:
        if followers:
            accounts = (account.from_user for account in accounts)
        else:
            accounts = (account.to_user for account in accounts)

    return {"accounts": accounts}
