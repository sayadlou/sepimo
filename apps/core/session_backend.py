from django.contrib.sessions.backends.db import SessionStore as DbSessionStore
from django.contrib.sessions.models import Session

from apps.store.models import Cart


class SessionStore(DbSessionStore):
    def cycle_key(self):
        old_session_key = super().session_key
        old_cart_id = Cart.objects.get(session__session_key=old_session_key).id
        super().cycle_key()
        self.save()
        session_model = Session.objects.get(session_key=self.session_key)
        if old_session_key:
            Cart.objects.filter(id=old_cart_id).update(session=session_model)
