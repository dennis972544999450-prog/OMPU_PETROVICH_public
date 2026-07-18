class SatlinkError(Exception):
    """Base exception with a stable, receipt-safe verdict code."""

    code = "SATLINK_ERROR"

    def __init__(self, message: str = "satlink operation failed") -> None:
        super().__init__(message)


class SchemaError(SatlinkError):
    code = "SCHEMA_INVALID"


class BundleError(SatlinkError):
    code = "BUNDLE_INVALID"


class CryptoError(SatlinkError):
    code = "CRYPTO_FAILED"


class TrustError(SatlinkError):
    code = "TRUST_REJECTED"


class PolicyError(SatlinkError):
    code = "POLICY_REJECTED"


class StorageError(SatlinkError):
    code = "STORAGE_FAILED"
