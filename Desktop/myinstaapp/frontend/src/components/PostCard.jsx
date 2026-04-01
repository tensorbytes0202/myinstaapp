import React, { useState, useEffect } from "react";
import { likes, comments } from "../api/service";

const PostCard = ({ post, onLike, onUnlike }) => {
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likes_count || 0);
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState("");
  const [commentsList, setCommentsList] = useState([]);

  // 🔹 Fetch comments when opened
  const fetchComments = async () => {
    try {
      const res = await comments.getComments(post.id);
      setCommentsList(res.comments || res);
    } catch (err) {
      console.error("Error fetching comments:", err);
    }
  };

  // 🔹 Toggle Like
  const handleLikeToggle = async () => {
    try {
      if (liked) {
        await likes.unlikePost(post.id);
        setLikesCount((prev) => Math.max(prev - 1, 0));
        onUnlike && onUnlike();
      } else {
        await likes.likePost(post.id);
        setLikesCount((prev) => prev + 1);
        onLike && onLike();
      }
      setLiked(!liked);
    } catch (err) {
      console.error("Like error:", err);
    }
  };

  // 🔹 Add Comment
  const handleAddComment = async () => {
    if (!commentText.trim()) return;

    try {
      const newComment = await comments.createComment(post.id, commentText);

      setCommentsList((prev) => [...prev, newComment]);
      setCommentText("");
    } catch (err) {
      console.error("Comment error:", err);
    }
  };

  // 🔹 Open comments
  const toggleComments = () => {
    setShowComments(!showComments);
    if (!showComments) fetchComments();
  };

  return (
    <div className="post-card">
      {/* 🔹 Header */}
      <div className="post-header">
        <strong>{post.username || "User"}</strong>
      </div>

      {/* 🔹 Image */}
      <div className="post-image">
        <img
          src={post.image_url}
          alt="post"
          style={{ width: "100%", borderRadius: "8px" }}
        />
      </div>

      {/* 🔹 Actions */}
      <div className="post-actions">
        <button onClick={handleLikeToggle}>
          {liked ? "❤️ Unlike" : "🤍 Like"}
        </button>

        <button onClick={toggleComments}>
          💬 Comments
        </button>
      </div>

      {/* 🔹 Likes Count */}
      <p><strong>{likesCount}</strong> likes</p>

      {/* 🔹 Caption */}
      <p>
        <strong>{post.username}</strong> {post.caption}
      </p>

      {/* 🔹 Comments Section */}
      {showComments && (
        <div className="comments-section">
          <h4>Comments</h4>

          {commentsList.length === 0 && <p>No comments yet</p>}

          {commentsList.map((c, index) => (
            <p key={index}>
              <strong>{c.username || "User"}:</strong> {c.text}
            </p>
          ))}

          {/* 🔹 Add Comment */}
          <div className="add-comment">
            <input
              type="text"
              placeholder="Add a comment..."
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
            />
            <button onClick={handleAddComment}>Post</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PostCard;