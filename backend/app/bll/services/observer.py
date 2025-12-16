"""Observer pattern implementation."""
from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """Observer interface."""
    
    @abstractmethod
    def update(self, event: Any) -> None:
        """Update observer with event."""
        pass


class SubscriptionObserver(Observer):
    """Observer for subscription events."""
    
    def __init__(self, notification_service):
        self.notification_service = notification_service
    
    def update(self, event: Any) -> None:
        """Handle subscription events."""
        if event.get("type") == "subscription_upgraded":
            user_id = event.get("user_id")
            subscription_type = event.get("subscription_type")
            # Send welcome notification for premium subscriptions
            if subscription_type in ["paid", "premium"]:
                self.notification_service.send_notification(
                    user_id=user_id,
                    notification_type="author_update",
                    data={
                        "title": "Welcome to Premium!",
                        "message": f"Thank you for upgrading to {subscription_type}!",
                    }
                )




