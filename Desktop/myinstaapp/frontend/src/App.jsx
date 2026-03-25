import React, { useState } from "react";
import { AuthProvider } from "./context/AuthContext";
import Feed from "./components/Feed";
import Profile from "./components/Profile";
import Search from "./components/search";
import Notifications from "./components/Notifications";
import "./App.css";

function App() {
    const [currentPage, setCurrentPage] = useState("feed"); // feed, profile, search, notifications
    const [selectedUserId, setSelectedUserId] = useState(1);

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
            default:
                return <Feed />;
        }
    };

    return (
        <AuthProvider>
            <div className="app-container">
                {/* Navigation Bar */}
                <nav className="navbar">
                    <div className="navbar-brand">
                        <h1 className="logo">📸 InstaClone</h1>
                    </div>

                    <div className="navbar-menu">
                        <button
                            className={`nav-btn ${currentPage === "feed" ? "active" : ""}`}
                            onClick={() => setCurrentPage("feed")}
                        >
                            🏠 Feed
                        </button>
                        <button
                            className={`nav-btn ${currentPage === "search" ? "active" : ""}`}
                            onClick={() => setCurrentPage("search")}
                        >
                            🔍 Search
                        </button>
                        <button
                            className={`nav-btn ${currentPage === "notifications" ? "active" : ""}`}
                            onClick={() => setCurrentPage("notifications")}
                        >
                            🔔 Notifications
                        </button>
                        <button
                            className={`nav-btn ${currentPage === "profile" ? "active" : ""}`}
                            onClick={() => {
                                setCurrentPage("profile");
                                setSelectedUserId(1); // Current user's profile
                            }}
                        >
                            👤 Profile
                        </button>
                    </div>

                    <div className="navbar-right">
                        <button className="logout-btn">Logout</button>
                    </div>
                </nav>

                {/* Main Content */}
                <main className="main-content">
                    {renderPage()}
                </main>

                {/* Sidebar (Optional) */}
                <aside className="sidebar">
                    <div className="sidebar-card">
                        <h3>Suggestions</h3>
                        <p>Follow more users to see suggestions</p>
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