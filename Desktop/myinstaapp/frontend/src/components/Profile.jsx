import React, { useState, useEffect } from "react";
import { auth, follow } from "../api/services";

const Profile = ({ userId }) => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isFollowing, setIsFollowing] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await auth.getProfile(userId);
      setProfile(response);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching profile:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFollowClick = async () => {
    try {
      await follow.followUser(userId);
      setIsFollowing(true);
      
      // Update follower count
      if (profile) {
        setProfile({
          ...profile,
          followers_count: profile.followers_count + 1,
        });
      }
    } catch (err) {
      console.error("Error following user:", err);
    }
  };

  if (loading) return <p className="loading">Loading profile...</p>;
  if (error) return <p className="error">Error: {error}</p>;
  if (!profile) return <p>Profile not found</p>;

  return (
    <div className="profile-container">
      {/* Profile Header */}
      <div className="profile-header">
        <div className="profile-avatar">
          <div className="avatar-large">👤</div>
        </div>

        <div className="profile-info">
          <h1 className="username">{profile.username}</h1>

          <div className="profile-stats">
            <div className="stat">
              <p className="stat-value">{profile.posts_count}</p>
              <p className="stat-label">Posts</p>
            </div>
            <div className="stat">
              <p className="stat-value">{profile.followers_count}</p>
              <p className="stat-label">Followers</p>
            </div>
            <div className="stat">
              <p className="stat-value">{profile.following_count}</p>
              <p className="stat-label">Following</p>
            </div>
          </div>

          <div className="profile-actions">
            <button
              className={`follow-btn ${isFollowing ? "following" : ""}`}
              onClick={handleFollowClick}
              disabled={isFollowing}
            >
              {isFollowing ? "Following" : "Follow"}
            </button>
            <button className="message-btn">Message</button>
          </div>
        </div>
      </div>

      {/* User Posts */}
      <div className="user-posts">
        <h2>Posts</h2>

        {profile.posts && profile.posts.length === 0 ? (
          <p className="no-posts">No posts yet</p>
        ) : (
          <div className="posts-grid">
            {profile.posts &&
              profile.posts.map((post) => (
                <div key={post.id} className="post-grid-item">
                  <img src={post.image_url} alt={post.caption} />
                  <div className="post-overlay">
                    <p>
                      ❤️ {post.likes_count} | 💬 {post.comments_count}
                    </p>
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;