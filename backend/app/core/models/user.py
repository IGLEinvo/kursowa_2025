"""User domain model."""
from datetime import datetime
from enum import Enum
from typing import Optional


class SubscriptionType(str, Enum):
    """Subscription type enumeration."""
    FREE = "free"
    PAID = "paid"
    PREMIUM = "premium"


class User:
    """User domain entity."""
    
    def __init__(
        self,
        id: Optional[int] = None,
        username: str = "",
        email: str = "",
        password_hash: str = "",
        full_name: Optional[str] = None,
        subscription_type: SubscriptionType = SubscriptionType.FREE,
        is_active: bool = True,
        is_admin: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.subscription_type = subscription_type
        self.is_active = is_active
        self.is_admin = is_admin
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def can_access_exclusive_content(self) -> bool:
        """Check if user can access exclusive content."""
        return self.subscription_type in [SubscriptionType.PAID, SubscriptionType.PREMIUM]
    
    def has_ad_free_experience(self) -> bool:
        """Check if user has ad-free experience."""
        return self.subscription_type in [SubscriptionType.PAID, SubscriptionType.PREMIUM]




