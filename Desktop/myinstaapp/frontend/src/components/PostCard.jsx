import React, { useState } from "react";
import { comments as commentService } from "../api/services";

const PostCard = ({ post, onLike, onUnlike }) => {
  const [showComments, setShowComments] = useState(false);
  const [postComments, setPostComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [commentsLoading, setCommentsLoading] = useState(false);
  const [liked, setLiked] = useState(false);

  const fetchComments = async () => {
    try {
      setCommentsLoading(true);
      const response = await commentService.getComments(post.id);
      setPostComments(response);
    } catch (err) {
      console.error("Error fetching comments:", err);
    } finally {
      setCommentsLoading(false);
    }
  };

  const handleToggleComments = async () => {
    if (!showComments) {
      await fetchComments();
    }
    setShowComments(!showComments);
  };

  const handleAddComment = async () => {
    if (!newComment.trim()) return;

    try {
      const comment = await commentService.createComment(post.id, newComment);
      setPostComments([comment, ...postComments]);
      setNewComment("");
    } catch (err) {
      console.error("Error creating comment:", err);
    }
  };

  const handleLikeClick = () => {
    if (liked) {
      onUnlike();
      setLiked(false);
    } else {
      onLike();
      setLiked(true);
    }
  };

  return (
    <div className="post-card">
      {/* Post Header */}
      <div className="post-header">
        <div className="user-info">
          <div className="avatar">👤</div>
          <div className="user-details">
            <p className="username">User {post.user_id}</p>
            <p className="timestamp">
              {new Date(post.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>

      {/* Post Image */}
      <div className="post-image">
        <img src={post.image_url} alt={post.caption} />
      </div>

      {/* Post Actions */}
      <div className="post-actions">
        <button
          className={`action-btn like-btn ${liked ? "liked" : ""}`}
          onClick={handleLikeClick}
        >
          ❤️ Like
        </button>
        <button
          className="action-btn comment-btn"
          onClick={handleToggleComments}
        >
          💬 Comment
        </button>
        <button className="action-btn share-btn">📤 Share</button>
      </div>

      {/* Likes and Comments Count */}
      <div className="post-stats">
        <p>
          <strong>{post.likes_count}</strong> likes
        </p>
        <p>
          <strong>{post.comments_count}</strong> comments
        </p>
      </div>

      {/* Post Caption */}
      <div className="post-caption">
        <p>
          <strong>User {post.user_id}</strong> {post.caption}
        </p>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="comments-section">
          <div className="comments-list">
            {commentsLoading ? (
              <p>Loading comments...</p>
            ) : postComments.length === 0 ? (
              <p>No comments yet</p>
            ) : (
              postComments.map((comment) => (
                <div key={comment.id} className="comment">
                  <p>
                    <strong>User {comment.user_id}</strong> {comment.text}
                  </p>
                  <p className="comment-time">
                    {new Date(comment.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))
            )}
          </div>

          {/* Add Comment Form */}
          <div className="add-comment">
            <input
              type="text"
              placeholder="Add a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleAddComment();
                }
              }}
            />
            <button onClick={handleAddComment} disabled={!newComment.trim()}>
              Post
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PostCard;