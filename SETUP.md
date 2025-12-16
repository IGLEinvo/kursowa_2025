# Quick Setup Guide

## Prerequisites Installation

### Python 3.9+
```bash
# Check Python version
python3 --version

# Install pip if needed
python3 -m ensurepip --upgrade
```

### Node.js 16+
```bash
# Check Node version
node --version

# Install from https://nodejs.org/ if needed
```

### MySQL 8.0+
```bash
# macOS
brew install mysql

# Ubuntu/Debian
sudo apt-get install mysql-server

# Start MySQL
mysql.server start  # macOS
sudo systemctl start mysql  # Linux
```

## Step-by-Step Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd Kursowa_4course
```

### 2. Database Setup

```bash
# Create database
mysql -u root -p
```

```sql
CREATE DATABASE news_newspaper CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

```bash
# Import schema
mysql -u root -p news_newspaper < database/schema.sql
```

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations (already done if schema.sql was imported)
# mysql -u root -p news_newspaper < ../database/schema.sql

# Start backend server
python run.py
```

Backend should be running on `http://localhost:5000`

### 4. Frontend Setup

```bash
# Open new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should be running on `http://localhost:3000`

## Verification

1. **Backend API**: Visit `http://localhost:5000/` - should see API message
2. **Frontend**: Visit `http://localhost:3000` - should see news app
3. **Database**: Verify tables exist
   ```sql
   mysql -u root -p news_newspaper
   SHOW TABLES;
   ```

## Creating Admin User

```sql
USE news_newspaper;

-- Create admin user (password will be hashed, this is just example)
-- Password should be hashed using bcrypt in production
-- Use registration endpoint first, then update role:

UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
```

Or register through the web interface and update role in database.

## Troubleshooting

### Backend won't start
- Check MySQL is running
- Verify database credentials in `.env`
- Check port 5000 is available

### Frontend won't start
- Check Node.js version (16+)
- Delete `node_modules` and `package-lock.json`, then `npm install`
- Check port 3000 is available

### Database connection errors
- Verify MySQL service is running
- Check database name, user, password in `.env`
- Test connection: `mysql -u root -p news_newspaper`

### CORS errors
- Ensure backend CORS_ORIGINS includes `http://localhost:3000`
- Check backend is running on port 5000

## Production Deployment

### Backend
- Use production WSGI server (Gunicorn)
- Set `DEBUG=False` in production
- Use environment variables for secrets
- Configure proper CORS origins

### Frontend
- Build production bundle: `npm run build`
- Serve static files with nginx or similar
- Configure API endpoint in production

### Database
- Use connection pooling
- Set up regular backups
- Configure proper indexes
- Monitor query performance

