from unittest.mock import patch


ЛУННАЯ_НОЧЬ = (
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
    Validating a tag with two completely different dates.
    """
    from meringue.core.utils.crypt import decrypt_message
    from meringue.core.utils.crypt import encrypt_message

    mocked_func.return_value = ЛУННАЯ_НОЧЬ.encode("utf-8")[:16]

    encrypted_msg = encrypt_message("test")
    decrypted_msg = decrypt_message(encrypted_msg)

    assert encrypted_msg == "0JHRg9C00LXRgiDQu9GD0DC1OFI="
    assert decrypted_msg == "test"
