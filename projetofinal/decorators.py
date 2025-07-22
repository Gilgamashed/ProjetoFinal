from django.contrib.auth.decorators import user_passes_test


def management_required(view_func):
    def test_func(user):
        return user.is_authenticated and user.role == 'ADMIN'
    return user_passes_test(test_func)(view_func)

def team_lead_or_higher(view_func):
    def test_func(user):
        return user.is_authenticated and user.role in ['ADMIN', 'LEAD']
    return user_passes_test(test_func)(view_func)