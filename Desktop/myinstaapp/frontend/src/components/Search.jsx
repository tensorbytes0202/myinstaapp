import React, { useState } from "react";
import { search } from "../api/services";

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchType, setSearchType] = useState("global"); // global, users, posts, hashtags

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      setError(null);

      let response;

      if (searchType === "global") {
        response = await search.globalSearch(query, 10);
      } else if (searchType === "users") {
        response = await search.searchUsers(query, 10);
        response = { results: response.results };
      } else if (searchType === "posts") {
        response = await search.searchPosts(query, 10);
        response = { results: response.results };
      } else if (searchType === "hashtags") {
        response = await search.searchHashtags(query, 10);
        response = { results: response.results };
      }

      setResults(response);
    } catch (err) {
      setError(err.message);
      console.error("Error searching:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="search-container">
      {/* Search Header */}
      <div className="search-header">
        <h2>Search</h2>

        {/* Search Tabs */}
        <div className="search-tabs">
          <button
            className={searchType === "global" ? "active" : ""}
            onClick={() => setSearchType("global")}
          >
            All
          </button>
          <button
            className={searchType === "users" ? "active" : ""}
            onClick={() => setSearchType("users")}
          >
            Users
          </button>
          <button
            className={searchType === "posts" ? "active" : ""}
            onClick={() => setSearchType("posts")}
          >
            Posts
          </button>
          <button
            className={searchType === "hashtags" ? "active" : ""}
            onClick={() => setSearchType("hashtags")}
          >
            Hashtags
          </button>
        </div>
      </div>

      {/* Search Input */}
      <div className="search-input-container">
        <input
          type="text"
          placeholder={
            searchType === "hashtags"
              ? "Search hashtags..."
              : "Search here..."
          }
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          className="search-input"
        />
        <button onClick={handleSearch} className="search-btn">
          🔍 Search
        </button>
      </div>

      {/* Loading and Error */}
      {loading && <p className="loading">Searching...</p>}
      {error && <p className="error">Error: {error}</p>}

      {/* Results */}
      {results && (
        <div className="search-results">
          {/* Global Search Results */}
          {searchType === "global" && (
            <>
              {/* Users Results */}
              {results.users && results.users.length > 0 && (
                <div className="results-section">
                  <h3>Users</h3>
                  <div className="results-list">
                    {results.users.map((user) => (
                      <div key={user.id} className="search-result-item">
                        <div className="avatar">👤</div>
                        <div className="result-info">
                          <p className="result-name">{user.username}</p>
                          <p className="result-type">User</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Posts Results */}
              {results.posts && results.posts.length > 0 && (
                <div className="results-section">
                  <h3>Posts</h3>
                  <div className="results-grid">
                    {results.posts.map((post) => (
                      <div key={post.id} className="post-result-item">
                        <img src={post.image_url} alt={post.caption} />
                        <div className="post-overlay">
                          <p>{post.caption}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Users Only Results */}
          {searchType === "users" && results.results && (
            <div className="results-list">
              {results.results.map((user) => (
                <div key={user.id} className="search-result-item">
                  <div className="avatar">👤</div>
                  <div className="result-info">
                    <p className="result-name">{user.username}</p>
                    <p className="result-id">@{user.username}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Posts Only Results */}
          {(searchType === "posts" || searchType === "hashtags") &&
            results.results && (
              <div className="results-grid">
                {results.results.map((post) => (
                  <div key={post.id} className="post-result-item">
                    <img src={post.image_url} alt={post.caption} />
                    <div className="post-overlay">
                      <p>{post.caption}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}

          {/* No Results */}
          {((!results.users || results.users.length === 0) &&
            (!results.posts || results.posts.length === 0) &&
            !results.results) ||
            (results.results && results.results.length === 0 && (
              <p className="no-results">No results found</p>
            ))}
        </div>
      )}
    </div>
  );
};

export default Search;