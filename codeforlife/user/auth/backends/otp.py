import typing as t

import pyotp
from django.contrib.auth.backends import BaseBackend
from django.utils import timezone

from ....request import WSGIRequest
from ...models import AuthFactor, User


class OtpBackend(BaseBackend):
    def authenticate(
        self,
        request: WSGIRequest,
        otp: t.Optional[str] = None,
        **kwargs,
    ):
        # Avoid near misses by getting the timestamp before any processing.
        now = timezone.now()

        if (
            otp is None
            or not isinstance(request.user, User)
            or not request.user.userprofile.otp_secret
            or not request.user.session.session_auth_factors.filter(
                auth_factor__type=AuthFactor.Type.OTP
            ).exists()
        ):
            return

        totp = pyotp.TOTP(request.user.userprofile.otp_secret)

        # Verify the otp is valid for now.
        if totp.verify(otp, for_time=now):
            # Deny replay attacks by rejecting the otp for last time.
            last_otp_for_time = request.user.userprofile.last_otp_for_time
            if last_otp_for_time and totp.verify(otp, last_otp_for_time):
                return
            request.user.userprofile.last_otp_for_time = now
            request.user.userprofile.save()

            # Delete OTP auth factor from session.
            request.user.session.session_auth_factors.filter(
                auth_factor__type=AuthFactor.Type.OTP
            ).delete()

            return request.user

    def get_user(self, user_id: int):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return