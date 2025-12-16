# System Architecture

## Overview

The Online News Newspaper system follows a three-tier architecture:

1. **Presentation Layer**: React frontend
2. **Application Layer**: Flask REST API
3. **Data Layer**: MySQL database

## Backend Architecture

### Layer Structure

```
backend/
├── app/
│   ├── __init__.py          # Application factory
│   ├── database.py          # Database connection (Singleton)
│   ├── routes/              # Route handlers (Controllers)
│   │   ├── auth.py
│   │   ├── news.py
│   │   ├── subscriptions.py
│   │   ├── notifications.py
│   │   ├── users.py
│   │   ├── admin.py
│   │   └── comments.py
│   ├── models/              # Domain models
│   │   ├── user.py
│   │   ├── article.py
│   │   └── category.py
│   ├── repositories/        # Data access layer (Repository Pattern)
│   │   ├── user_repository.py
│   │   ├── article_repository.py
│   │   └── category_repository.py
│   ├── services/            # Business logic layer
│   │   ├── subscription_service.py    # Strategy, Factory patterns
│   │   ├── notification_service.py    # Observer pattern
│   │   └── recommendation_service.py
│   └── middleware/          # Authentication decorators
│       └── auth.py
└── config/
    └── config.py            # Configuration (Singleton)
```

### Data Flow

1. **HTTP Request** → Route Handler (Controller)
2. **Route Handler** → Service Layer (Business Logic)
3. **Service** → Repository (Data Access)
4. **Repository** → Database
5. **Response flows back** through the layers

### Authentication Flow

1. User submits credentials
2. Auth route validates and creates JWT token
3. Token stored in frontend (localStorage)
4. Token included in Authorization header for protected routes
5. Middleware decorators verify token and check permissions

## Frontend Architecture

### Component Structure

```
frontend/src/
├── components/
│   └── Layout/
│       └── Navbar.jsx
├── pages/
│   ├── Home.jsx
│   ├── ArticleDetail.jsx
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Profile.jsx
│   ├── SavedArticles.jsx
│   └── AdminPanel.jsx
├── contexts/
│   └── AuthContext.jsx      # Global authentication state
├── api/
│   └── api.js               # API client functions
├── App.jsx
└── main.jsx
```

### State Management

- **Local State**: React hooks (useState, useEffect)
- **Global State**: React Context API (AuthContext)
- **API Calls**: Centralized in `api/api.js`

## Database Schema

### Core Tables

1. **users**: User accounts and authentication
2. **articles**: News articles and content
3. **categories**: Article categories
4. **subscription_tiers**: Available subscription plans
5. **user_subscriptions**: User subscription records
6. **comments**: Article comments (supporting replies)
7. **notifications**: User notifications
8. **user_preferences**: Personalization data
9. **article_views**: Tracking for recommendations
10. **author_subscriptions**: User follows authors

### Relationships

- Articles → Users (author)
- Articles → Categories (many-to-one)
- Comments → Articles (many-to-one)
- Comments → Users (author)
- User Subscriptions → Subscription Tiers
- User Preferences → Categories

## API Design

### REST Endpoints

**Authentication**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

**News**
- `GET /api/news` - Get news feed
- `GET /api/news/:id` - Get article details
- `GET /api/news/search` - Search articles
- `GET /api/news/categories` - Get categories
- `GET /api/news/recommended` - Get recommended articles
- `POST /api/news/:id/like` - Like article
- `POST /api/news/:id/save` - Save article

**Comments**
- `GET /api/comments/articles/:id/comments` - Get comments
- `POST /api/comments/articles/:id/comments` - Create comment

**Subscriptions**
- `GET /api/subscriptions` - Get user subscription
- `GET /api/subscriptions/tiers` - Get all tiers
- `POST /api/subscriptions` - Create subscription

**Notifications**
- `GET /api/notifications` - Get notifications
- `PUT /api/notifications/:id/read` - Mark as read
- `GET /api/notifications/preferences` - Get preferences
- `PUT /api/notifications/preferences` - Update preferences

**Admin**
- `GET /api/admin/articles` - List all articles
- `PUT /api/admin/articles/:id` - Update article
- `DELETE /api/admin/articles/:id` - Delete article
- `GET /api/admin/users` - List users (admin only)

## Security

1. **Password Hashing**: bcrypt
2. **JWT Authentication**: Flask-JWT-Extended
3. **Role-Based Access Control**: Admin, Editor, User roles
4. **CORS Configuration**: Restricted to frontend origin
5. **SQL Injection Prevention**: Parameterized queries
6. **XSS Prevention**: React automatically escapes content

## Scalability Considerations

1. **Database Indexing**: Indexes on frequently queried fields
2. **Pagination**: Implemented for article lists
3. **Caching**: Can be added for frequently accessed data
4. **Microservices Ready**: Services are loosely coupled
5. **Horizontal Scaling**: Stateless API allows multiple instances

