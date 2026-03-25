import React, { useState, useEffect } from "react";
import { notifications as notificationService } from "../api/services";

const Notifications = () => {
  const [notifs, setNotifs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [unreadCount, setUnreadCount] = useState(0);
  const [skip, setSkip] = useState(0);

  useEffect(() => {
    fetchNotifications();
    fetchUnreadCount();

    // Poll for new notifications every 10 seconds
    const interval = setInterval(() => {
      fetchUnreadCount();
    }, 10000);

    return () => clearInterval(interval);
  }, [skip]);

  const fetchNotifications = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await notificationService.getNotifications(skip, 10);
      setNotifs(response.notifications);
      setUnreadCount(response.unread_count);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching notifications:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchUnreadCount = async () => {
    try {
      const response = await notificationService.getUnreadCount();
      setUnreadCount(response.unread_count);
    } catch (err) {
      console.error("Error fetching unread count:", err);
    }
  };

  const handleMarkAsRead = async (notificationId) => {
    try {
      await notificationService.markAsRead(notificationId);

      // Update UI
      setNotifs(
        notifs.map((notif) =>
          notif.id === notificationId ? { ...notif, is_read: true } : notif
        )
      );

      // Update unread count
      setUnreadCount(Math.max(0, unreadCount - 1));
    } catch (err) {
      console.error("Error marking notification as read:", err);
    }
  };

  const handleMarkAllAsRead = async () => {
    try {
      await notificationService.markAllAsRead();

      // Update UI
      setNotifs(notifs.map((notif) => ({ ...notif, is_read: true })));
      setUnreadCount(0);
    } catch (err) {
      console.error("Error marking all as read:", err);
    }
  };

  const handleDeleteNotification = async (notificationId) => {
    try {
      await notificationService.deleteNotification(notificationId);

      // Update UI
      setNotifs(notifs.filter((notif) => notif.id !== notificationId));
    } catch (err) {
      console.error("Error deleting notification:", err);
    }
  };

  const getNotificationIcon = (type) => {
    switch (type) {
      case "like":
        return "❤️";
      case "comment":
        return "💬";
      case "follow":
        return "👥";
      default:
        return "📢";
    }
  };

  const getNotificationMessage = (notif) => {
    switch (notif.notification_type) {
      case "like":
        return `${notif.actor_username} liked your post`;
      case "comment":
        return `${notif.actor_username} commented on your post`;
      case "follow":
        return `${notif.actor_username} started following you`;
      default:
        return notif.message || "New notification";
    }
  };

  return (
    <div className="notifications-container">
      {/* Notifications Header */}
      <div className="notifications-header">
        <h2>
          Notifications
          {unreadCount > 0 && <span className="unread-badge">{unreadCount}</span>}
        </h2>

        {unreadCount > 0 && (
          <button onClick={handleMarkAllAsRead} className="mark-all-btn">
            Mark all as read
          </button>
        )}
      </div>

      {/* Loading and Error */}
      {loading && <p className="loading">Loading notifications...</p>}
      {error && <p className="error">Error: {error}</p>}

      {/* Notifications List */}
      {!loading && notifs.length === 0 && (
        <p className="no-notifications">No notifications yet</p>
      )}

      <div className="notifications-list">
        {notifs.map((notif) => (
          <div
            key={notif.id}
            className={`notification-item ${notif.is_read ? "read" : "unread"}`}
          >
            <div className="notification-icon">
              {getNotificationIcon(notif.notification_type)}
            </div>

            <div className="notification-content">
              <p className="notification-message">
                {getNotificationMessage(notif)}
              </p>
              <p className="notification-time">
                {new Date(notif.created_at).toLocaleDateString()}
              </p>
            </div>

            <div className="notification-actions">
              {!notif.is_read && (
                <button
                  onClick={() => handleMarkAsRead(notif.id)}
                  className="mark-read-btn"
                  title="Mark as read"
                >
                  ✓
                </button>
              )}

              <button
                onClick={() => handleDeleteNotification(notif.id)}
                className="delete-btn"
                title="Delete"
              >
                ✕
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {notifs.length > 0 && (
        <div className="pagination">
          {skip > 0 && (
            <button onClick={() => setSkip(skip - 10)}>← Previous</button>
          )}
          <button onClick={() => setSkip(skip + 10)}>Next →</button>
        </div>
      )}
    </div>
  );
};

export default Notifications;