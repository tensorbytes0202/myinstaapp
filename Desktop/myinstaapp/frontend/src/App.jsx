import React, { useState } from "react";
import { AuthProvider } from "./context/AuthContext";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import CreatePost from "./pages/CreatePost";

import Feed from "./components/Feed";
import Profile from "./components/Profile";
import Search from "./components/Search";
import Notifications from "./components/Notifications";

import "./App.css";

function App() {
  const [currentPage, setCurrentPage] = useState("feed");
  const [selectedUserId, setSelectedUserId] = useState(1);

  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("access_token")
  );

  const [showSignup, setShowSignup] = useState(false);

  // 🔥 Logout fix
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsLoggedIn(false);
  };

  // 🔥 Auth screen
  if (!isLoggedIn) {
    return (
      <div className="auth-wrapper">
        {showSignup ? (
          <>
            <Signup />
            <p onClick={() => setShowSignup(false)}>
              Already have an account? Login
            </p>
          </>
        ) : (
          <>
            <Login onLogin={() => setIsLoggedIn(true)} />
            <p onClick={() => setShowSignup(true)}>
              Don't have an account? Signup
            </p>
          </>
        )}
      </div>
    );
  }

  // 🔥 Page rendering
  const renderPage = () => {
    switch (currentPage) {
      case "feed":
        return <Feed />;
      case "profile":
        return <Profile userId={selectedUserId} />;
      case "search":
        return <Search />;
      case "notifications":
        return <Notifications />;
      case "create":
        return <CreatePost />;
      default:
        return <Feed />;
    }
  };

  return (
    <AuthProvider>
      <div className="app-container">

        {/* 🔹 Navbar */}
        <nav className="navbar">
          <h1 className="logo">📸 InstaClone</h1>

          <div className="navbar-menu">
            <button onClick={() => setCurrentPage("feed")}>🏠 Feed</button>
            <button onClick={() => setCurrentPage("search")}>🔍 Search</button>
            <button onClick={() => setCurrentPage("create")}>➕ Create</button>
            <button onClick={() => setCurrentPage("notifications")}>🔔</button>
            <button
              onClick={() => {
                setCurrentPage("profile");
                setSelectedUserId(1);
              }}
            >
              👤 Profile
            </button>
          </div>

          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </nav>

        {/* 🔹 Main */}
        <main className="main-content">{renderPage()}</main>

        {/* 🔹 Sidebar */}
        <aside className="sidebar">
          <div className="sidebar-card">
            <h3>Suggestions</h3>
            <p>Follow more users</p>
          </div>

          <div className="sidebar-card">
            <h3>Trending</h3>
            <ul>
              <li>#travel</li>
              <li>#photography</li>
              <li>#food</li>
            </ul>
          </div>
        </aside>
      </div>
    </AuthProvider>
  );
}

export default App;