import base64
import warnings

from Crypto.Cipher import AES

from meringue.conf import m_settings

__all__ = [
    "decrypt_message",
    "encrypt_message",
]


def _warn_deprecated() -> None:
    """
    Warn about deprecated encryption helpers.
    """

    msg = (
        "`encrypt_message` and `decrypt_message` are deprecated and will be removed in a future "
        "version. Use `django.core.signing` for signed payloads or server-side opaque random "
        "tokens for short secret links."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)


def _urlsafe_b64decode(msg: str) -> bytes:
    """
    Decode URL-safe base64 with optional padding.
    """

    padding = "=" * (-len(msg) % 4)
    return base64.urlsafe_b64decode(f"{msg}{padding}".encode())


def encrypt_message(msg: str) -> str:
    """
    Deprecated method for encrypting a message with AES algorithm and the GCM method.

    Attributes:
        msg: Message to Encrypt.

    Returns:
        Encrypted message.
    """

    _warn_deprecated()

    cipher = AES.new(m_settings.CRYPTO_KEY.encode("utf8"), AES.MODE_GCM)
    encrypted_msg = cipher.encrypt(msg.encode("utf8"))
    nonce = cipher.nonce
    result = base64.urlsafe_b64encode(nonce + encrypted_msg).rstrip(b"=").decode("utf-8")
    return result


def decrypt_message(msg: str) -> str:
    """
    Deprecated method for decrypting a message encrypted with
    [encrypt_message][meringue.core.utils.crypt.encrypt_message].

    Attributes:
        msg: Message to decrypt.

    Returns:
        Decrypted message.
    """

    _warn_deprecated()

    raw_msg = _urlsafe_b64decode(msg)
    nonce, raw_msg = raw_msg[: AES.block_size], raw_msg[AES.block_size :]
    cipher = AES.new(m_settings.CRYPTO_KEY.encode("utf-8"), AES.MODE_GCM, nonce=nonce)
    decrypted_msg = cipher.decrypt(raw_msg).decode("utf-8")
    return decrypted_msg
