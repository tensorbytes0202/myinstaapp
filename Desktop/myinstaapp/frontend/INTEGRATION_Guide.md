# Frontend Integration Guide

## 📁 Project Structure

```
frontend/src/
├── api/
│   └── services.js              ← All API calls
├── context/
│   └── AuthContext.jsx          ← Auth state management
├── components/
│   ├── Feed.jsx                 ← Feed component
│   ├── PostCard.jsx             ← Individual post card
│   ├── Profile.jsx              ← User profile
│   ├── Search.jsx               ← Search functionality
│   └── Notifications.jsx        ← Notifications
├── pages/
│   └── (future: dedicated pages)
├── App.jsx                      ← Main app component
├── App.css                      ← Global styles
└── main.jsx                     ← Entry point
```

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
npm install axios react-router-dom
# or
yarn add axios react-router-dom
```

### 2. Update `main.jsx`

```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### 3. Copy All Files

Copy the following files to your `frontend/src/` directory:

- ✅ `api/services.js` - API service layer
- ✅ `context/AuthContext.jsx` - Auth context
- ✅ `components/Feed.jsx` - Feed component
- ✅ `components/PostCard.jsx` - Post card component
- ✅ `components/Profile.jsx` - Profile component
- ✅ `components/Search.jsx` - Search component
- ✅ `components/Notifications.jsx` - Notifications component
- ✅ `App.jsx` - Main app component
- ✅ `App.css` - Global styles

### 4. Start Backend Server

Make sure your backend is running:

```bash
cd insta/backend
python -m uvicorn app.main:app --reload
```

Server should be running on: `http://localhost:8000`

### 5. Start Frontend

```bash
npm run dev
```

Frontend should be running on: `http://localhost:5173` (or your configured port)

---

## 🔌 API Integration

### API Service (`services.js`)

All API calls are centralized in `api/services.js`:

```javascript
import { auth, posts, likes, comments, follow, feed, search, notifications } from '../api/services';

// Example usage:
const profile = await auth.getProfile(userId);
const feedPosts = await feed.getPersonalizedFeed(0, 10);
await likes.likePost(postId);
```

### Authentication Flow

```javascript
// Login
const response = await auth.login('username', 'password');
localStorage.setItem('access_token', response.access_token);

// Authenticated requests
// Token is automatically added to all requests in services.js
```

---

## 🎯 Component Overview

### Feed Component

Shows personalized feed, explore, and trending posts:

```jsx
<Feed />
```

**Features:**
- ✅ Switch between personalized, explore, and trending feeds
- ✅ Like/unlike posts
- ✅ View comments
- ✅ Add comments
- ✅ Pagination

---

### Profile Component

Shows user profile with posts:

```jsx
<Profile userId={1} />
```

**Features:**
- ✅ User info (username)
- ✅ Stats (posts, followers, following)
- ✅ Follow button
- ✅ Grid of user's posts

---

### Search Component

Global search for users and posts:

```jsx
<Search />
```

**Features:**
- ✅ Search users by username
- ✅ Search posts by caption
- ✅ Search hashtags
- ✅ Global search (all types)

---

### Notifications Component

Manage notifications:

```jsx
<Notifications />
```

**Features:**
- ✅ Display all notifications
- ✅ Mark as read
- ✅ Mark all as read
- ✅ Delete notifications
- ✅ Unread count

---

## 🔧 Customization

### Change API Base URL

Edit `api/services.js`:

```javascript
const API_BASE_URL = "http://localhost:8000"; // Change this
```

### Add Authentication Token to Headers

The token is automatically added from localStorage:

```javascript
const token = localStorage.getItem("access_token");
if (token) {
  headers["Authorization"] = `Bearer ${token}`;
}
```

### Handle Errors

All API calls have try-catch error handling:

```javascript
try {
  const data = await feed.getPersonalizedFeed();
} catch (err) {
  console.error(err.message);
  // Show error to user
}
```

---

## 📊 State Management

### Using Auth Context

```jsx
import { useAuth } from './context/AuthContext';

function MyComponent() {
  const { user, token, loading, login, logout } = useAuth();
  
  return (
    <>
      {loading ? 'Loading...' : <p>{user.username}</p>}
    </>
  );
}
```

---

## 🎨 Styling

### CSS Variables (Optional)

Add to `App.css` for easy theming:

```css
:root {
  --primary-color: #0a66c2;
  --border-color: #dbdbdb;
  --bg-color: #fafafa;
  --text-color: #262626;
  --text-secondary: #8e8e8e;
}
```

---

## 🧪 Testing Components

### Test Feed

1. Go to Feed tab
2. Click "Like" on any post
3. See likes_count increase
4. Click "Comment"
5. Add a comment
6. See it appear in comments list

### Test Search

1. Go to Search tab
2. Type a query (e.g., "travel")
3. See results for users and posts
4. Click on a result

### Test Notifications

1. Like a post
2. Go to Notifications tab
3. See "User X liked your post"
4. Click mark as read
5. Notification appearance changes

---

## 🚨 Common Issues

### "Access-Control-Allow-Origin" Error

**Problem:** CORS error when making API calls

**Solution:** Add CORS middleware to backend `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Token Not Being Sent

**Problem:** API calls return 401 Unauthorized

**Solution:** Check if token is in localStorage:

```javascript
console.log(localStorage.getItem("access_token"));
```

If not, user needs to login first.

### Image Not Loading

**Problem:** Post images show broken image icon

**Solution:** 
1. Check image URL is valid
2. Check AWS S3 bucket is public (if using S3)
3. Check CORS headers on CDN

---

## 📱 Responsive Design

The design is responsive with breakpoints:

- **Desktop:** 1024px+ (3-column layout)
- **Tablet:** 768px-1024px (2-column layout)
- **Mobile:** <768px (1-column layout)

---

## 🔐 Security Best Practices

1. **Store token securely:**
   ```javascript
   // Good for demo, consider using httpOnly cookies for production
   localStorage.setItem("access_token", token);
   ```

2. **Validate input:**
   ```javascript
   if (!query || query.trim().length < 2) {
     setError("Query too short");
     return;
   }
   ```

3. **Handle sensitive data:**
   ```javascript
   // Don't log passwords or tokens
   console.log(user); // ✅ Safe
   console.log(password); // ❌ Never
   ```

---

## 📈 Performance Tips

1. **Lazy load images:**
   ```jsx
   <img src={post.image_url} loading="lazy" />
   ```

2. **Memoize components:**
   ```jsx
   const PostCard = React.memo(({ post }) => {...});
   ```

3. **Debounce search:**
   ```javascript
   const [searchQuery, setSearchQuery] = useState("");
   
   const debouncedSearch = useCallback(
     debounce((query) => handleSearch(query), 300),
     []
   );
   ```

---

## 🎓 Next Steps

1. Add routing with React Router
2. Add file upload UI for posts
3. Add real-time notifications with WebSockets
4. Add dark mode
5. Add infinite scroll
6. Add user mentions in comments
7. Deploy to production

---

## 📞 Support

If you encounter issues:

1. Check backend is running: `http://localhost:8000`
2. Check frontend is running: `http://localhost:5173`
3. Open browser console (F12) for errors
4. Check network tab to see API calls
5. Verify token in localStorage

---

**Frontend Integration Complete! 🎉**