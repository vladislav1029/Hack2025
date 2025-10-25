import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { authAPI } from '../utils/api';
import './Profile.css';

const Profile = () => {
  const { user, getRoleName } = useAuth();
  const [userData, setUserData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const data = await authAPI.getCurrentUser();
        setUserData(data);
      } catch (error) {
        console.error('Error fetching user data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      fetchUserData();
    }
  }, [user]);

  if (loading) {
    return (
      <div className="profilePage">
        <div className="container">
          <div className="loading">Loading profile...</div>
        </div>
      </div>
    );
  }

  if (!userData) {
    return (
      <div className="profilePage">
        <div className="container">
          <div className="error">Error loading profile data</div>
        </div>
      </div>
    );
  }

  return (
    <div className="profilePage">
      <div className="container">
        <div className="profileHeader">
          <h1>Profile</h1>
        </div>

        <div className="profileContent">
          <div className="profileCard">
            <div className="profileAvatar">
              <div className="avatarIcon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>

            <div className="profileInfo">
              <div className="infoGroup">
                <label>Email:</label>
                <span>{userData.email}</span>
              </div>

              <div className="infoGroup">
                <label>User ID:</label>
                <span>{userData.oid}</span>
              </div>

              <div className="infoGroup">
                <label>Role:</label>
                <span className={`role role-${userData.role}`}>
                  {getRoleName(userData.role)}
                </span>
              </div>

              <div className="infoGroup">
                <label>Status:</label>
                <span className={`status ${userData.is_active ? 'active' : 'inactive'}`}>
                  {userData.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>

              <div className="infoGroup">
                <label>Verified:</label>
                <span className={`verification ${userData.is_verificate ? 'verified' : 'unverified'}`}>
                  {userData.is_verificate ? 'Verified' : 'Not Verified'}
                </span>
              </div>

              <div className="infoGroup">
                <label>Created:</label>
                <span>{new Date(userData.created_at).toLocaleDateString()}</span>
              </div>

              {userData.update_at && (
                <div className="infoGroup">
                  <label>Last Updated:</label>
                  <span>{new Date(userData.update_at).toLocaleDateString()}</span>
                </div>
              )}
            </div>
          </div>

          <div className="profileActions">
            <button className="actionButton primary">
              Edit Profile
            </button>
            <button className="actionButton secondary">
              Change Password
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
