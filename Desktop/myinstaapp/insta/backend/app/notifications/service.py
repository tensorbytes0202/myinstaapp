from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.notifications.repository import (
    create_notification,
    get_notification,
    get_user_notifications,
    get_unread_count,
    mark_as_read,
    mark_all_as_read,
    delete_notification,
    notification_exists
)
from app.users.repository import get_user_by_id


# Create like notification
async def notify_like(db: AsyncSession, post_owner_id: int, liker_id: int, post_id: int):
    """Create notification when someone likes a post"""
    
    # Don't notify user about their own likes
    if post_owner_id == liker_id:
        return None
    
    # Check if notification already exists (to avoid duplicates)
    existing = await notification_exists(
        db, post_owner_id, liker_id, "like", post_id
    )
    
    if existing:
        return existing
    
    notification = await create_notification(
        db,
        recipient_id=post_owner_id,
        actor_id=liker_id,
        notification_type="like",
        post_id=post_id,
        message="liked your post"
    )
    
    return notification


# Create comment notification
async def notify_comment(db: AsyncSession, post_owner_id: int, commenter_id: int, post_id: int, comment_id: int):
    """Create notification when someone comments on a post"""
    
    # Don't notify user about their own comments
    if post_owner_id == commenter_id:
        return None
    
    notification = await create_notification(
        db,
        recipient_id=post_owner_id,
        actor_id=commenter_id,
        notification_type="comment",
        post_id=post_id,
        comment_id=comment_id,
        message="commented on your post"
    )
    
    return notification


# Create follow notification
async def notify_follow(db: AsyncSession, user_id: int, follower_id: int):
    """Create notification when someone follows user"""
    
    # Don't notify user about their own follows
    if user_id == follower_id:
        return None
    
    # Check if notification already exists
    existing = await notification_exists(
        db, user_id, follower_id, "follow"
    )
    
    if existing:
        return existing
    
    notification = await create_notification(
        db,
        recipient_id=user_id,
        actor_id=follower_id,
        notification_type="follow",
        message="started following you"
    )
    
    return notification


# Get user notifications with actor info
async def get_user_notifications_with_actor(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    """Get notifications with actor username"""
    
    notifications = await get_user_notifications(db, user_id, skip, limit)
    unread_count = await get_unread_count(db, user_id)
    
    # Add actor info to each notification
    notifications_with_actor = []
    
    for notif in notifications:
        actor = await get_user_by_id(db, notif.actor_id)
        
        notifications_with_actor.append({
            "id": notif.id,
            "recipient_id": notif.recipient_id,
            "actor_id": notif.actor_id,
            "actor_username": actor.username if actor else "Unknown",
            "notification_type": notif.notification_type,
            "post_id": notif.post_id,
            "comment_id": notif.comment_id,
            "message": notif.message,
            "is_read": notif.is_read,
            "created_at": notif.created_at
        })
    
    return {
        "notifications": notifications_with_actor,
        "total": len(notifications_with_actor),
        "unread_count": unread_count
    }


# Mark single notification as read
async def read_notification(db: AsyncSession, notification_id: int, user_id: int):
    """Mark notification as read"""
    
    notification = await get_notification(db, notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if notification.recipient_id != user_id:
        raise HTTPException(status_code=403, detail="Not your notification")
    
    updated = await mark_as_read(db, notification_id)
    
    return updated


# Mark all notifications as read
async def read_all_notifications(db: AsyncSession, user_id: int):
    """Mark all notifications as read"""
    
    await mark_all_as_read(db, user_id)
    
    return {"message": "All notifications marked as read"}


# Delete notification
async def remove_notification(db: AsyncSession, notification_id: int, user_id: int):
    """Delete a notification"""
    
    notification = await get_notification(db, notification_id)
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    if notification.recipient_id != user_id:
        raise HTTPException(status_code=403, detail="Not your notification")
    
    await delete_notification(db, notification_id)
    
    return {"message": "Notification deleted"}