const API_BASE_URL = "http://localhost:8000";

// Helper function for API calls
const apiCall = async (endpoint, options = {}) => {
  const token = localStorage.getItem("access_token");
  
  const headers = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API Error");
  }

  return response.json();
};

// =====================
// AUTH ENDPOINTS
// =====================

export const auth = {
  signup: (username, password) =>
    apiCall("/users/signup", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  login: (username, password) =>
    apiCall("/users/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),

  getProfile: (userId) =>
    apiCall(`/users/profile/${userId}`),

  getProfileByUsername: (username) =>
    apiCall(`/users/profile/username/${username}`),
};

// =====================
// POSTS ENDPOINTS
// =====================

export const posts = {
  createPost: (imageUrl, caption) =>
    apiCall("/posts/", {
      method: "POST",
      body: JSON.stringify({ image_url: imageUrl, caption }),
    }),

  getPost: (postId) =>
    apiCall(`/posts/${postId}`),

  getUserPosts: (userId) =>
    apiCall(`/posts/user/${userId}`),

  uploadAndCreatePost: async (file, caption = "") => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("caption", caption);

    const token = localStorage.getItem("access_token");
    const headers = {};

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/upload/post`, {
      method: "POST",
      headers,
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Upload failed");
    }

    return response.json();
  },
};

// =====================
// LIKES ENDPOINTS
// =====================

export const likes = {
  likePost: (postId) =>
    apiCall("/likes/", {
      method: "POST",
      body: JSON.stringify({ post_id: postId }),
    }),

  unlikePost: (postId) =>
    apiCall(`/likes/${postId}`, {
      method: "DELETE",
    }),

  getLikeCount: (postId) =>
    apiCall(`/likes/count/${postId}`),

  getLikers: (postId) =>
    apiCall(`/likes/${postId}`),
};

// =====================
// COMMENTS ENDPOINTS
// =====================

export const comments = {
  createComment: (postId, text) =>
    apiCall("/comments/", {
      method: "POST",
      body: JSON.stringify({ post_id: postId, text }),
    }),

  getComments: (postId) =>
    apiCall(`/comments/${postId}`),

  getCommentCount: (postId) =>
    apiCall(`/comments/count/${postId}`),

  updateComment: (commentId, text) =>
    apiCall(`/comments/${commentId}`, {
      method: "PUT",
      body: JSON.stringify({ text }),
    }),

  deleteComment: (commentId) =>
    apiCall(`/comments/${commentId}`, {
      method: "DELETE",
    }),
};

// =====================
// FOLLOW ENDPOINTS
// =====================

export const follow = {
  followUser: (followingId) =>
    apiCall("/follow/", {
      method: "POST",
      body: JSON.stringify({ following_id: followingId }),
    }),
};

// =====================
// FEED ENDPOINTS
// =====================

export const feed = {
  getPersonalizedFeed: (skip = 0, limit = 10) =>
    apiCall(`/feed/?skip=${skip}&limit=${limit}`),

  getExploreFeed: (skip = 0, limit = 10) =>
    apiCall(`/feed/explore?skip=${skip}&limit=${limit}`),

  getTrendingFeed: (skip = 0, limit = 10) =>
    apiCall(`/feed/trending?skip=${skip}&limit=${limit}`),
};

// =====================
// SEARCH ENDPOINTS
// =====================

export const search = {
  globalSearch: (query, limit = 5) =>
    apiCall(`/search/?q=${encodeURIComponent(query)}&limit=${limit}`),

  searchUsers: (query, limit = 10) =>
    apiCall(`/search/users?q=${encodeURIComponent(query)}&limit=${limit}`),

  searchPosts: (query, limit = 10) =>
    apiCall(`/search/posts?q=${encodeURIComponent(query)}&limit=${limit}`),

  searchHashtags: (hashtag, limit = 10) =>
    apiCall(`/search/hashtags?tag=${encodeURIComponent(hashtag)}&limit=${limit}`),
};

// =====================
// NOTIFICATIONS ENDPOINTS
// =====================

export const notifications = {
  getNotifications: (skip = 0, limit = 10) =>
    apiCall(`/notifications/?skip=${skip}&limit=${limit}`),

  markAsRead: (notificationId) =>
    apiCall(`/notifications/${notificationId}/read`, {
      method: "PUT",
    }),

  markAllAsRead: () =>
    apiCall("/notifications/read-all", {
      method: "PUT",
    }),

  deleteNotification: (notificationId) =>
    apiCall(`/notifications/${notificationId}`, {
      method: "DELETE",
    }),

  getUnreadCount: () =>
    apiCall("/notifications/count/unread"),
};

// =====================
// UPLOAD ENDPOINTS
// =====================

export const upload = {
  uploadImage: async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const token = localStorage.getItem("access_token");
    const headers = {};

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/upload/image`, {
      method: "POST",
      headers,
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Upload failed");
    }

    return response.json();
  },

  uploadProfileImage: async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const token = localStorage.getItem("access_token");
    const headers = {};

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/upload/profile`, {
      method: "POST",
      headers,
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Upload failed");
    }

    return response.json();
  },
};