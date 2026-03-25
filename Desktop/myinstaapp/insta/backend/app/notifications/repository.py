from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.notifications.models import Notification
from sqlalchemy import func


# Create notification
async def create_notification(
    db: AsyncSession,
    recipient_id: int,
    actor_id: int,
    notification_type: str,
    post_id: int = None,
    comment_id: int = None,
    message: str = None
):
    """Create a new notification"""
    
    notification = Notification(
        recipient_id=recipient_id,
        actor_id=actor_id,
        notification_type=notification_type,
        post_id=post_id,
        comment_id=comment_id,
        message=message
    )
    
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    
    return notification


# Get single notification
async def get_notification(db: AsyncSession, notification_id: int):
    """Get notification by ID"""
    
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    
    return result.scalar_one_or_none()


# Get user notifications
async def get_user_notifications(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    """Get all notifications for a user"""
    
    result = await db.execute(
        select(Notification)
        .where(Notification.recipient_id == user_id)
        .order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    
    return result.scalars().all()


# Get unread notification count
async def get_unread_count(db: AsyncSession, user_id: int):
    """Get count of unread notifications"""
    
    result = await db.execute(
        select(func.count(Notification.id)).where(
            (Notification.recipient_id == user_id) & 
            (Notification.is_read == False)
        )
    )
    
    return result.scalar() or 0


# Mark notification as read
async def mark_as_read(db: AsyncSession, notification_id: int):
    """Mark notification as read"""
    
    notification = await get_notification(db, notification_id)
    
    if notification:
        notification.is_read = True
        await db.commit()
        await db.refresh(notification)
    
    return notification


# Mark all notifications as read
async def mark_all_as_read(db: AsyncSession, user_id: int):
    """Mark all notifications for user as read"""
    
    await db.execute(
        select(Notification)
        .where(
            (Notification.recipient_id == user_id) & 
            (Notification.is_read == False)
        )
    )
    
    # Update all
    result = await db.execute(
        select(Notification).where(Notification.recipient_id == user_id)
    )
    
    notifications = result.scalars().all()
    
    for notif in notifications:
        notif.is_read = True
    
    await db.commit()


# Delete notification
async def delete_notification(db: AsyncSession, notification_id: int):
    """Delete a notification"""
    
    await db.execute(
        delete(Notification).where(Notification.id == notification_id)
    )
    
    await db.commit()


# Check if notification already exists
async def notification_exists(
    db: AsyncSession,
    recipient_id: int,
    actor_id: int,
    notification_type: str,
    post_id: int = None
):
    """Check if similar notification already exists"""
    
    result = await db.execute(
        select(Notification).where(
            (Notification.recipient_id == recipient_id) &
            (Notification.actor_id == actor_id) &
            (Notification.notification_type == notification_type) &
            (Notification.post_id == post_id) &
            (Notification.is_read == False)
        )
    )
    
    return result.scalar_one_or_none()