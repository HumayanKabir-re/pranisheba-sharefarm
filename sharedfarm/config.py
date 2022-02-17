class PayStatus:
    PENDING = 0
    COMPLETE = 1
    FAILED = 2
    EXPIRED = 3

    CHOICES = (
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Failed"),
        (EXPIRED, "Expired")
    )

    spChoices = (
        ("CANCEL", "CANCEL"),
        ("FAIL", "FAIL"),
        ("SUCCESS", "SUCCESS")
    )


class SurjoPayConfig:
    # MERCHANT_USERNAME = 'smprani'
    # MERCHANT_PASSWORD = 'Kpkf9nNk5NTB'
    # SHURJOPAY_URL = 'https://www.shurjopay.com/sp-data.php'
    # DECRYPT_URL = 'https://www.shurjopay.com/merchant/decrypt.php'
    # MERCHANT_PREFIX = 'PRM'
    MERCHANT_USERNAME = 'spaytest'
    MERCHANT_PASSWORD = 'JehPNXF58rXs'
    SHURJOPAY_URL = 'https://www.shurjopay.com/sp-data.php'
    DECRYPT_URL = 'https://www.shurjopay.com/merchant/decrypt.php'
    MERCHANT_PREFIX = 'NOK'
