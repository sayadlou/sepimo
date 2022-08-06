from copy import copy

from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

from apps.store.models import Cart


class SessionStore(DbSessionStore):
    def cycle_key(self):
        old_session_key = self.session_key
        if old_session_key:
            old_cart = Cart.objects.get(session__session_key=old_session_key)
            old_cart.session_id =None
            old_cart.save()
            super().cycle_key()
            old_cart.session_id = self.session_key
            old_cart.save()
        else:
            super().cycle_key()
