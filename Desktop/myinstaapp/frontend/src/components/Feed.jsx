import React, { useState, useEffect } from "react";
import { feed, likes, comments } from "../api/services";
import PostCard from "./PostCard";

const Feed = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [skip, setSkip] = useState(0);
  const [feedType, setFeedType] = useState("personalized"); // personalized, explore, trending

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
      } else if (feedType === "trending") {
        response = await feed.getTrendingFeed(skip, 10);
      }

      setPosts(response.posts);
    } catch (err) {
      setError(err.message);
      console.error("Error fetching feed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (postId) => {
    try {
      await likes.likePost(postId);
      
      // Update UI
      setPosts(
        posts.map((post) =>
          post.id === postId
            ? { ...post, likes_count: post.likes_count + 1 }
            : post
        )
      );
    } catch (err) {
      console.error("Error liking post:", err);
    }
  };

  const handleUnlike = async (postId) => {
    try {
      await likes.unlikePost(postId);
      
      // Update UI
      setPosts(
        posts.map((post) =>
          post.id === postId
            ? { ...post, likes_count: post.likes_count - 1 }
            : post
        )
      );
    } catch (err) {
      console.error("Error unliking post:", err);
    }
  };

  return (
    <div className="feed-container">
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

      {loading && <p className="loading">Loading posts...</p>}
      {error && <p className="error">Error: {error}</p>}

      <div className="posts-list">
        {posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            onLike={() => handleLike(post.id)}
            onUnlike={() => handleUnlike(post.id)}
          />
        ))}
      </div>

      {posts.length > 0 && (
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

export default Feed;