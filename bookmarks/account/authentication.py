from .models import Profile


class EmailAuthBackend:
    """
    e-mail addressdan foydalangan holda tasdiqdan o'tkazish
    Authenticate using e-mail address.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = Profile.objects.get(email=username)
            if user.check_password(password):
                return user
            return None

        except (Profile.DoesNotExist, Profile.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return Profile.objects.get(pk=user_id)

        except Profile.DoesNotExist:
            return None



