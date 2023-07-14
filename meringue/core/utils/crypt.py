import base64

from Crypto.Cipher import AES

from meringue.conf import m_settings


__all__ = [
    "encrypt_message",
    "decrypt_message",
]


def encrypt_message(msg: str) -> str:
    """
    Method for encrypting a message with AES algorithm and the GCM method.

    Attributes:
        msg: Message to Encrypt.

    Returns:
        Encrypted message.
    """

    cipher = AES.new(m_settings.CRYPTO_KEY.encode("utf8"), AES.MODE_GCM)
    encrypted_msg = cipher.encrypt(msg.encode("utf8"))
    nonce = cipher.nonce
    result = base64.urlsafe_b64encode(nonce + encrypted_msg).decode("utf-8")
    return result


def decrypt_message(msg: str) -> str:
    """
    Method for decrypting a message encrypted with AES algorithm and the GCM method.

    Attributes:
        msg: Message to decrypt.

    Returns:
        Decrypted message.
    """
    raw_msg = base64.urlsafe_b64decode(msg.encode("utf-8"))
    nonce, raw_msg = raw_msg[: AES.block_size], raw_msg[AES.block_size :]
    cipher = AES.new(m_settings.CRYPTO_KEY.encode("utf-8"), AES.MODE_GCM, nonce=nonce)
    decrypted_msg = cipher.decrypt(raw_msg).decode("utf-8")
    return decrypted_msg
