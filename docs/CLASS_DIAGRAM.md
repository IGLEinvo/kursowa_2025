# UML Class Diagram - Online News Newspaper

## Core Classes and Relationships

### Models

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ - id: int           │
│ - username: string  │
│ - email: string     │
│ - password_hash     │
│ - first_name        │
│ - last_name         │
│ - role: enum        │
│ - is_active: bool   │
│ - created_at        │
│ - updated_at        │
├─────────────────────┤
│ + hash_password()   │
│ + verify_password() │
│ + to_dict()         │
│ + from_dict()       │
└─────────────────────┘
          │
          │ 1
          │
          │ *
┌─────────────────────┐
│      Article        │
├─────────────────────┤
│ - id: int           │
│ - title: string     │
│ - slug: string      │
│ - content: text     │
│ - excerpt: text     │
│ - author_id: int    │
│ - category_id: int  │
│ - is_breaking: bool │
│ - is_premium: bool  │
│ - status: enum      │
│ - views_count: int  │
│ - likes_count: int  │
│ - published_at      │
├─────────────────────┤
│ + to_dict()         │
│ + from_dict()       │
└─────────────────────┘
          │
          │ *
          │
          │ 1
┌─────────────────────┐
│     Category        │
├─────────────────────┤
│ - id: int           │
│ - name: string      │
│ - slug: string      │
│ - description       │
└─────────────────────┘
```

### Repository Pattern

```
┌──────────────────────────┐
│   Repository (Abstract)  │
└──────────────────────────┘
           ▲
           │
    ┌──────┴──────┬──────────────┐
    │             │              │
┌───────────┐ ┌────────────┐ ┌──────────────┐
│UserRepo   │ │ArticleRepo │ │CategoryRepo  │
├───────────┤ ├────────────┤ ├──────────────┤
│+create()  │ │+create()   │ │+create()     │
│+find_by_id│ │+find_by_id │ │+find_by_id   │
│+update()  │ │+update()   │ │+find_all()   │
│+delete()  │ │+search()   │ │+update()     │
│           │ │            │ │+delete()     │
└───────────┘ └────────────┘ └──────────────┘
```

### Strategy Pattern (Subscription)

```
┌────────────────────────────┐
│ SubscriptionStrategy       │
│ (Abstract)                 │
├────────────────────────────┤
│ +calculate_price()         │
│ +get_features()            │
└────────────────────────────┘
           ▲
           │
    ┌──────┼──────┬──────────────┐
    │      │      │              │
┌──────────┐ ┌──────────┐ ┌─────────────┐
│Free      │ │Paid      │ │Student      │
│Strategy  │ │Strategy  │ │Strategy     │
├──────────┤ ├──────────┤ ├─────────────┤
│          │ │          │ │             │
└──────────┘ └──────────┘ └─────────────┘

┌────────────────────────────┐
│SubscriptionStrategyFactory │
├────────────────────────────┤
│ +create_strategy(type)     │
└────────────────────────────┘
```

### Observer Pattern (Notifications)

```
┌────────────────────────────┐
│  NotificationObserver      │
│  (Abstract)                │
├────────────────────────────┤
│ +notify(notification_data) │
└────────────────────────────┘
           ▲
           │
    ┌──────┴──────┐
    │             │
┌──────────────┐ ┌──────────────┐
│EmailObserver │ │PushObserver  │
├──────────────┤ ├──────────────┤
│              │ │              │
└──────────────┘ └──────────────┘

┌────────────────────────────┐
│  NotificationSubject       │
├────────────────────────────┤
│ -observers: List           │
├────────────────────────────┤
│ +attach(observer)          │
│ +detach(observer)          │
│ +notify_observers()        │
└────────────────────────────┘

┌────────────────────────────┐
│ NotificationService        │
│ extends Subject            │
├────────────────────────────┤
│ +create_notification()     │
│ +get_user_notifications()  │
│ +send_breaking_news()      │
│ +send_daily_digest()       │
└────────────────────────────┘
```

### Singleton Pattern

```
┌────────────────────────────┐
│    DatabaseConnection      │
│    (Singleton)             │
├────────────────────────────┤
│ -_instance                 │
│ -_connection               │
├────────────────────────────┤
│ +get_connection()          │
│ +get_cursor()              │
│ +close()                   │
└────────────────────────────┘

┌────────────────────────────┐
│         Config             │
│      (Singleton)           │
├────────────────────────────┤
│ -_instance                 │
│ -SECRET_KEY                │
│ -DB_HOST, DB_USER, etc.    │
├────────────────────────────┤
│ +DATABASE_URL              │
└────────────────────────────┘
```

### Services

```
┌────────────────────────────┐
│  SubscriptionService       │
├────────────────────────────┤
│ -user_repo                 │
├────────────────────────────┤
│ +get_user_subscription()   │
│ +create_subscription()     │
│ +has_premium_access()      │
└────────────────────────────┘

┌────────────────────────────┐
│  RecommendationService     │
├────────────────────────────┤
│ -user_repo                 │
│ -article_repo              │
├────────────────────────────┤
│ +update_user_preferences() │
│ +get_recommended_articles()│
│ +record_view()             │
└────────────────────────────┘
```

### Middleware (Decorator Pattern)

```
┌────────────────────────────┐
│  @admin_required           │
│  @editor_required          │
│  @premium_required         │
│  @optional_auth            │
└────────────────────────────┘
         │
         │ decorates
         ▼
┌────────────────────────────┐
│   Route Handlers           │
│   (Controllers)            │
└────────────────────────────┘
```

## Relationships Summary

1. **User** → **Article** (1-to-many): User can author many articles
2. **Category** → **Article** (1-to-many): Category contains many articles
3. **Repository** classes access **Model** classes
4. **Services** use **Repositories** and **Strategy** patterns
5. **NotificationService** uses **Observer** pattern
6. **Routes** use **Services** and **Middleware** decorators
7. **Singleton** classes provide single instances (Database, Config)

