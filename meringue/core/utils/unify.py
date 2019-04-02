# -*- coding:utf-8 -*-


def unify_email(origin_email):
    """
        unify email address
        remove tags
    """
    if not origin_email or not '@' in origin_email[1:-3]:
        return None
    user, domain = origin_email.strip().rsplit('@', 1)
    user = user.split('+')[0]
    email = '@'.join([user, domain])
    email = email.lower()
    return email


def unify_phone(origin_phone):
    """
        default country code use if cant parse phone number
    """

    import phonenumbers as pn

    try:
        phone = pn.parse(origin_phone)
    except pn.phonenumberutil.NumberParseException:
        phone = pn.parse(origin_phone, default_country)

    result = pn.format_number(phone, pn.PhoneNumberFormat.INTERNATIONAL)
    return result
