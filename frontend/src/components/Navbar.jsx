import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated, removeAuthToken } from '../utils/auth';
import './Navbar.css';

const Navbar = () => {
  const navigate = useNavigate();
  const authenticated = isAuthenticated();

  const handleLogout = () => {
    removeAuthToken();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          News Portal
        </Link>
        <div className="navbar-menu">
          <Link to="/" className="navbar-link">Home</Link>
          {authenticated ? (
            <>
              <Link to="/recommendations" className="navbar-link">Recommendations</Link>
              <Link to="/profile" className="navbar-link">Profile</Link>
              <Link to="/admin" className="navbar-link">Admin</Link>
              <button onClick={handleLogout} className="navbar-button">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="navbar-link">Login</Link>
              <Link to="/register" className="navbar-link">Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;




