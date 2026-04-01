import React, { useState, useEffect } from "react";
import { auth, follow, posts } from "../api/service";

const Profile = ({ userId }) => {
  const [profile, setProfile] = useState(null);
  const [userPosts, setUserPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isFollowing, setIsFollowing] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);

      const userData = await auth.getProfile(userId);
      const postsData = await posts.getUserPosts(userId);

      console.log("Profile:", userData);
      console.log("Posts:", postsData);

      setProfile(userData);

      // Handle posts response safely
      if (Array.isArray(postsData)) {
        setUserPosts(postsData);
      } else if (postsData.posts) {
        setUserPosts(postsData.posts);
      } else {
        setUserPosts([]);
      }

    } catch (err) {
      console.error("Profile Error:", err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleFollowClick = async () => {
    try {
      await follow.followUser(userId);
      setIsFollowing(true);

      // update UI instantly
      setProfile((prev) => ({
        ...prev,
        followers_count: (prev.followers_count || 0) + 1,
      }));
    } catch (err) {
      console.error("Follow error:", err);
    }
  };

  if (loading) return <p className="loading">Loading profile...</p>;
  if (error) return <p className="error">Error: {error}</p>;
  if (!profile) return <p>Profile not found</p>;

  return (
    <div className="profile-container">
      {/* Header */}
      <div className="profile-header">
        <div className="profile-avatar">
          <div className="avatar-large">👤</div>
        </div>

        <div className="profile-info">
          <h1 className="username">{profile.username}</h1>

          <div className="profile-stats">
            <div className="stat">
              <p>{userPosts.length}</p>
              <p>Posts</p>
            </div>

            <div className="stat">
              <p>{profile.followers_count}</p>
              <p>Followers</p>
            </div>

            <div className="stat">
              <p>{profile.following_count}</p>
              <p>Following</p>
            </div>
          </div>

          <div className="profile-actions">
            <button
              onClick={handleFollowClick}
              disabled={isFollowing}
            >
              {isFollowing ? "Following" : "Follow"}
            </button>

            <button>Message</button>
          </div>
        </div>
      </div>

      {/* Posts */}
      <div className="user-posts">
        <h2>Posts</h2>

        {userPosts.length === 0 ? (
          <p>No posts yet</p>
        ) : (
          <div className="posts-grid">
            {userPosts.map((post) => (
              <div key={post.id} className="post-grid-item">
                <img src={post.image_url} alt="" />

                <div className="post-overlay">
                  ❤️ {post.likes_count || 0} | 💬 {post.comments_count || 0}
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