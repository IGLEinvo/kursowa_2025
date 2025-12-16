# Use Case Diagram - Online News Newspaper

## Actors

1. **Guest User** (Unauthenticated)
2. **Registered User** (Authenticated)
3. **Editor**
4. **Administrator**

## Use Cases

### Guest User
- View news feed
- View article details
- Search articles
- Browse categories
- Register account
- Login

### Registered User
- All Guest User capabilities +
- View personalized recommendations
- Like articles
- Save articles for later
- Comment on articles
- Reply to comments
- Subscribe to subscription tiers
- Manage subscription
- Follow authors
- Unfollow authors
- View saved articles
- View notifications
- Manage notification preferences
- Update profile
- View subscription status

### Editor
- All Registered User capabilities +
- Create articles
- Edit articles
- Delete articles
- Publish articles
- Mark articles as breaking news
- Set articles as premium
- View article statistics

### Administrator
- All Editor capabilities +
- Manage users
- Activate/deactivate users
- Create categories
- Edit categories
- Delete categories
- Manage subscription tiers
- View system statistics

## Use Case Diagram (Text Representation)

```
┌─────────────────────────────────────────────────────────────┐
│                    Online News Newspaper                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Guest User                                                 │
│  ├── View News Feed                                         │
│  ├── View Article                                           │
│  ├── Search Articles                                        │
│  ├── Browse Categories                                      │
│  ├── Register                                               │
│  └── Login                                                  │
│                                                              │
│  Registered User                                            │
│  ├── View Recommendations                                   │
│  ├── Like Article                                           │
│  ├── Save Article                                           │
│  ├── Comment on Article                                     │
│  ├── Reply to Comment                                       │
│  ├── Subscribe                                              │
│  ├── Manage Subscription                                    │
│  ├── Follow Author                                          │
│  ├── View Saved Articles                                    │
│  ├── View Notifications                                     │
│  ├── Manage Notification Preferences                        │
│  └── Update Profile                                         │
│                                                              │
│  Editor                                                     │
│  ├── Create Article                                         │
│  ├── Edit Article                                           │
│  ├── Delete Article                                         │
│  ├── Publish Article                                        │
│  ├── Mark Breaking News                                     │
│  └── Set Premium Article                                    │
│                                                              │
│  Administrator                                              │
│  ├── Manage Users                                           │
│  ├── Manage Categories                                      │
│  └── View System Statistics                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Use Cases

### UC1: View News Feed
- **Actor**: Guest User, Registered User
- **Preconditions**: None
- **Main Flow**:
  1. User navigates to home page
  2. System displays latest published articles
  3. User can filter by category
  4. User can search articles
- **Postconditions**: Articles displayed to user

### UC2: View Article
- **Actor**: Guest User, Registered User
- **Preconditions**: Article exists and is published
- **Main Flow**:
  1. User clicks on article
  2. System checks subscription if premium article
  3. System displays article content
  4. System increments view count
  5. System records view for recommendations (if logged in)
- **Postconditions**: Article displayed, view tracked

### UC3: Create Subscription
- **Actor**: Registered User
- **Preconditions**: User is logged in
- **Main Flow**:
  1. User selects subscription tier
  2. System calculates price using Strategy pattern
  3. User confirms subscription
  4. System creates subscription record
  5. System grants access based on tier
- **Postconditions**: User has active subscription

### UC4: Create Article
- **Actor**: Editor
- **Preconditions**: User is logged in as editor/admin
- **Main Flow**:
  1. Editor creates new article
  2. System validates article data
  3. System saves article as draft
  4. Editor can publish or save as draft
  5. If published, system sends breaking news notification (if marked)
- **Postconditions**: Article created in system

### UC5: Receive Breaking News Notification
- **Actor**: Registered User
- **Preconditions**: User has breaking news notifications enabled
- **Main Flow**:
  1. Editor publishes breaking news article
  2. System triggers notification service
  3. Observer pattern notifies all enabled users
  4. Users receive notifications
- **Postconditions**: Users notified of breaking news

