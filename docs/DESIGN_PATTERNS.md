# Design Patterns Used in Online News Newspaper

This document describes the GoF (Gang of Four) design patterns implemented in the project.

## 1. Singleton Pattern

**Location:** `backend/app/database.py`, `backend/config/config.py`

**Purpose:** Ensure only one instance of database connection and configuration exists.

**Implementation:**
- `DatabaseConnection` class: Manages a single database connection instance
- `Config` class: Provides single configuration instance for the application

**Benefits:**
- Prevents multiple database connections
- Centralized configuration management
- Resource efficiency

## 2. Factory Pattern

**Location:** `backend/app/services/subscription_service.py`

**Purpose:** Create subscription strategies based on subscription tier type without exposing creation logic.

**Implementation:**
- `SubscriptionStrategyFactory`: Creates appropriate strategy (Free, Paid, Student, Corporate) based on tier type

**Benefits:**
- Decouples object creation from usage
- Easy to add new subscription types
- Centralized creation logic

## 3. Strategy Pattern

**Location:** `backend/app/services/subscription_service.py`

**Purpose:** Define a family of algorithms (subscription pricing strategies) that are interchangeable.

**Implementation:**
- `SubscriptionStrategy` (abstract base)
- `FreeSubscriptionStrategy`
- `PaidSubscriptionStrategy`
- `StudentSubscriptionStrategy`
- `CorporateSubscriptionStrategy`

**Benefits:**
- Different pricing algorithms can be selected at runtime
- Open/Closed Principle: Easy to add new strategies without modifying existing code
- Eliminates conditional statements for pricing logic

## 4. Observer Pattern

**Location:** `backend/app/services/notification_service.py`

**Purpose:** Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified.

**Implementation:**
- `NotificationSubject`: Manages list of observers
- `NotificationObserver` (abstract): Observer interface
- `EmailNotificationObserver`: Sends email notifications
- `PushNotificationObserver`: Sends push notifications

**Benefits:**
- Loose coupling between subject and observers
- Dynamic addition/removal of observers
- Follows Open/Closed Principle

## 5. Repository Pattern

**Location:** `backend/app/repositories/`

**Purpose:** Abstraction layer between business logic and data access layer.

**Implementation:**
- `UserRepository`: Manages user data access
- `ArticleRepository`: Manages article data access
- `CategoryRepository`: Manages category data access

**Benefits:**
- Separation of concerns
- Easier testing (can mock repositories)
- Centralized data access logic
- Easy to change data source without affecting business logic

## 6. Decorator Pattern

**Location:** `backend/app/middleware/auth.py`

**Purpose:** Add behavior (authentication/authorization) to functions dynamically.

**Implementation:**
- `@admin_required`: Decorator for admin-only endpoints
- `@editor_required`: Decorator for editor/admin endpoints
- `@premium_required`: Decorator for premium subscription required
- `@optional_auth`: Decorator for optional authentication

**Benefits:**
- Add functionality without modifying original function
- Composable authentication logic
- Separation of concerns (auth logic separate from business logic)

## 7. Builder Pattern (Conceptual)

**Location:** Article creation in services

**Purpose:** Construct complex objects step by step.

**Implementation:**
- Article creation with various optional fields (breaking news, premium, etc.)

**Benefits:**
- Flexible object construction
- Readable code for complex objects

## SOLID Principles Applied

1. **Single Responsibility Principle**: Each class has one reason to change
   - Repositories handle data access
   - Services handle business logic
   - Routes handle HTTP requests

2. **Open/Closed Principle**: Open for extension, closed for modification
   - Strategy pattern allows adding new subscription types
   - Observer pattern allows adding new notification types

3. **Liskov Substitution Principle**: Subtypes must be substitutable for base types
   - All subscription strategies can be used interchangeably
   - All observers can be attached to subject

4. **Interface Segregation Principle**: Clients shouldn't depend on interfaces they don't use
   - Small, focused interfaces (NotificationObserver, SubscriptionStrategy)

5. **Dependency Inversion Principle**: Depend on abstractions, not concretions
   - Services depend on repository interfaces
   - Controllers depend on service abstractions

## GRASP Patterns

1. **Controller**: Route handlers act as controllers, coordinating between UI and business logic
2. **Creator**: Repositories create model instances
3. **Information Expert**: Services contain business logic for their domain
4. **Low Coupling**: Services and repositories are loosely coupled
5. **High Cohesion**: Related functionality is grouped together (e.g., all subscription logic in SubscriptionService)

