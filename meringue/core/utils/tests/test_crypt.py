from unittest.mock import patch

import pytest

from meringue.core.utils.crypt import decrypt_message
from meringue.core.utils.crypt import encrypt_message

MOONLIT_NIGHT = (
    "Будет луна."
    "Есть уже"
    "немножко."
    "А вот и полная повисла в воздухе."
    "Это Бог, должно быть,"
    "дивной"
    "серебряной ложкой"
    "роется в звёзд ухе."
)  # Владимир Маяковский, 1916 г.


@patch("Crypto.Random.get_random_bytes")
def test_encrypt(mocked_func):
    """
    Checking deprecated encryption preserves the legacy token format.
    """

    mocked_func.return_value = MOONLIT_NIGHT.encode("utf-8")[:16]

    with pytest.warns(DeprecationWarning, match="`encrypt_message` and `decrypt_message`"):
        encrypted_msg = encrypt_message("test")
    with pytest.warns(DeprecationWarning, match="`encrypt_message` and `decrypt_message`"):
        decrypted_msg = decrypt_message(encrypted_msg)

    assert encrypted_msg == "0JHRg9C00LXRgiDQu9GD0DC1OFI"
    assert decrypted_msg == "test"


def test_decrypt_message():
    """
    Checking backward compatibility with the old padded token format.
    """

    with pytest.warns(DeprecationWarning, match="`encrypt_message` and `decrypt_message`"):
        decrypted_msg = decrypt_message("0JHRg9C00LXRgiDQu9GD0DC1OFI=")

    assert decrypted_msg == "test"


def test_decrypt_message_without_padding():
    """
    Checking token format without base64 padding.
    """

    with pytest.warns(DeprecationWarning, match="`encrypt_message` and `decrypt_message`"):
        decrypted_msg = decrypt_message("0JHRg9C00LXRgiDQu9GD0DC1OFI")

    assert decrypted_msg == "test"
