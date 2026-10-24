import hashlib
import hmac
import secrets
import smtplib
import ssl
import time
from email.message import EmailMessage
from threading import Lock


class OTPServiceError(Exception):
    pass


class OTPConfigurationError(OTPServiceError):
    pass


class OTPDeliveryError(OTPServiceError):
    pass


class OTPResendTooSoon(OTPServiceError):
    def __init__(self, retry_after_seconds: int):
        self.retry_after_seconds = retry_after_seconds
        super().__init__(f"Please wait {retry_after_seconds} seconds before requesting another code.")


class OTPVerificationError(OTPServiceError):
    pass


class EmailOTPService:
    MAX_ATTEMPTS = 5

    def __init__(self):
        self._codes = {}
        self._last_sent = {}
        self._lock = Lock()

    def send(self, email: str, config: dict) -> dict:
        server = config.get("MAIL_SERVER")
        sender = config.get("MAIL_DEFAULT_SENDER") or config.get("MAIL_USERNAME")
        if not server or not sender:
            raise OTPConfigurationError("Email delivery is not configured. Set the SMTP settings in backend/.env.")

        use_tls = bool(config.get("MAIL_USE_TLS"))
        use_ssl = bool(config.get("MAIL_USE_SSL"))
        if use_tls and use_ssl:
            raise OTPConfigurationError("Enable either SMTP TLS or SMTP SSL, not both.")

        ttl_seconds = max(60, int(config.get("OTP_TTL_SECONDS", 300)))
        cooldown_seconds = max(0, int(config.get("OTP_RESEND_COOLDOWN_SECONDS", 30)))
        now = time.monotonic()
        with self._lock:
            previous_send = self._last_sent.get(email)
            if previous_send is not None:
                remaining = cooldown_seconds - int(now - previous_send)
                if remaining > 0:
                    raise OTPResendTooSoon(remaining)

        code = f"{secrets.randbelow(1_000_000):06d}"
        try:
            self._deliver_email(config, email, code, ttl_seconds)
        except (OSError, smtplib.SMTPException, ssl.SSLError) as error:
            raise OTPDeliveryError("Could not send the verification email. Check the SMTP settings and try again.") from error

        with self._lock:
            self._codes[email] = {
                "digest": self._digest(code),
                "expires_at": time.monotonic() + ttl_seconds,
                "attempts": 0
            }
            self._last_sent[email] = time.monotonic()

        return {
            "email_masked": self._mask_email(email),
            "expires_in_seconds": ttl_seconds,
            "resend_after_seconds": cooldown_seconds
        }

    def verify(self, email: str, code: str) -> None:
        if not isinstance(code, str) or len(code) != 6 or not code.isdigit():
            raise OTPVerificationError("Enter the six-digit code from your email.")

        with self._lock:
            record = self._codes.get(email)
            if not record:
                raise OTPVerificationError("Request a new verification code and try again.")
            if time.monotonic() >= record["expires_at"]:
                self._codes.pop(email, None)
                raise OTPVerificationError("That verification code has expired. Request a new code.")
            if record["attempts"] >= self.MAX_ATTEMPTS:
                self._codes.pop(email, None)
                raise OTPVerificationError("Too many incorrect attempts. Request a new code.")

            record["attempts"] += 1
            if not hmac.compare_digest(record["digest"], self._digest(code)):
                if record["attempts"] >= self.MAX_ATTEMPTS:
                    self._codes.pop(email, None)
                    raise OTPVerificationError("Too many incorrect attempts. Request a new code.")
                raise OTPVerificationError("The verification code is incorrect.")

            self._codes.pop(email, None)

    @staticmethod
    def _digest(code: str) -> str:
        return hashlib.sha256(code.encode("utf-8")).hexdigest()

    @staticmethod
    def _mask_email(email: str) -> str:
        local, domain = email.split("@", 1)
        return f"{local[:1]}***@{domain}"

    @staticmethod
    def _deliver_email(config: dict, email: str, code: str, ttl_seconds: int) -> None:
        message = EmailMessage()
        message["Subject"] = "Your Smart Mock Test verification code"
        message["From"] = config.get("MAIL_DEFAULT_SENDER") or config.get("MAIL_USERNAME")
        message["To"] = email
        message.set_content(
            "Use this code to verify your email before starting the mock test:\n\n"
            f"{code}\n\n"
            f"This code expires in {max(1, ttl_seconds // 60)} minutes. Do not share it with anyone."
        )

        server = config["MAIL_SERVER"]
        port = int(config.get("MAIL_PORT", 587))
        username = config.get("MAIL_USERNAME")
        password = config.get("MAIL_PASSWORD")
        use_ssl = bool(config.get("MAIL_USE_SSL"))
        use_tls = bool(config.get("MAIL_USE_TLS"))

        if use_ssl:
            smtp_class = smtplib.SMTP_SSL
            smtp_options = {"timeout": 10, "context": ssl.create_default_context()}
        else:
            smtp_class = smtplib.SMTP
            smtp_options = {"timeout": 10}

        with smtp_class(server, port, **smtp_options) as smtp:
            if use_tls and not use_ssl:
                smtp.starttls(context=ssl.create_default_context())
            if username:
                smtp.login(username, password or "")
            smtp.send_message(message)