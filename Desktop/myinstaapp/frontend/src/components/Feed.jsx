import React, { useState, useEffect } from "react";
import { feed, likes } from "../api/service"; // ✅ FIXED PATH
import PostCard from "./PostCard";

const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [skip, setSkip] = useState(0);
  const [feedType, setFeedType] = useState("personalized");

  useEffect(() => {
    fetchFeed();
  }, [feedType, skip]);

  const fetchFeed = async () => {
    try {
      setLoading(true);
      setError(null);

      let response;

      if (feedType === "personalized") {
        response = await feed.getPersonalizedFeed(skip, 10);
      } else if (feedType === "explore") {
        response = await feed.getExploreFeed(skip, 10);
      } else {
        response = await feed.getTrendingFeed(skip, 10);
      }

      console.log("API Response:", response);

      // ✅ HANDLE BOTH CASES (array OR object)
      if (Array.isArray(response)) {
        setPosts(response);
      } else if (response.posts) {
        setPosts(response.posts);
      } else {
        setPosts([]);
      }

    } catch (err) {
      console.error("Feed Error:", err);
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (postId) => {
    try {
      await likes.likePost(postId);

      setPosts((prevPosts) =>
        prevPosts.map((post) =>
          post.id === postId
            ? { ...post, likes_count: (post.likes_count || 0) + 1 }
            : post
        )
      );
    } catch (err) {
      console.error("Like error:", err);
    }
  };

  const handleUnlike = async (postId) => {
    try {
      await likes.unlikePost(postId);

      setPosts((prevPosts) =>
        prevPosts.map((post) =>
          post.id === postId
            ? { ...post, likes_count: Math.max((post.likes_count || 1) - 1, 0) }
            : post
        )
      );
    } catch (err) {
      console.error("Unlike error:", err);
    }
  };

  return (
    <div className="feed-container">
      {/* Header */}
      <div className="feed-header">
        <h2>Feed</h2>

        <div className="feed-tabs">
          <button
            className={feedType === "personalized" ? "active" : ""}
            onClick={() => {
              setFeedType("personalized");
              setSkip(0);
            }}
          >
            For You
          </button>

          <button
            className={feedType === "explore" ? "active" : ""}
            onClick={() => {
              setFeedType("explore");
              setSkip(0);
            }}
          >
            Explore
          </button>

          <button
            className={feedType === "trending" ? "active" : ""}
            onClick={() => {
              setFeedType("trending");
              setSkip(0);
            }}
          >
            Trending
          </button>
        </div>
      </div>

      {/* Loading */}
      {loading && <p className="loading">Loading posts...</p>}

      {/* Error */}
      {error && <p className="error">Error: {error}</p>}

      {/* Posts */}
      <div className="posts-list">
        {posts.length === 0 && !loading && <p>No posts found</p>}

        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onLike={() => handleLike(post.id)}
            onUnlike={() => handleUnlike(post.id)}
          />
        ))}
      </div>

      {/* Pagination */}
      {posts.length > 0 && (
        <div className="pagination">
          {skip > 0 && (
            <button onClick={() => setSkip(skip - 10)}>
              ← Previous
            </button>
          )}

          <button onClick={() => setSkip(skip + 10)}>
            Next →
          </button>
        </div>
      )}
    </div>
  );
};

export default Feed;