from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def on_user_signed_up(request, user, **kwargs):
    user.is_superuser = True
    user.is_staff = True
    user.save(update_fields=('is_superuser', 'is_superuser'))
