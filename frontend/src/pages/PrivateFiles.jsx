import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { apiClient } from '../utils/api';
import './PrivateFiles.css';

const PrivateFiles = () => {
  const { user, isAuthenticated } = useAuth();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchFiles();
    }
  }, [isAuthenticated]);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getFileList(true);
      setFiles(response || []);
    } catch (error) {
      console.error('Error fetching private files:', error);
      setError('Failed to load private files');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      await apiClient.uploadFile(file, true);
      await fetchFiles(); // Refresh the list
    } catch (error) {
      console.error('Error uploading private file:', error);
      setError('Failed to upload private file');
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (filename) => {
    try {
      const linkData = await apiClient.getFileLink(filename, true);
      if (linkData && linkData.temp_link) {
        window.open(linkData.temp_link, '_blank');
      }
    } catch (error) {
      console.error('Error getting private file link:', error);
      setError('Failed to get download link');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="privateFilesPage">
        <div className="container">
          <div className="accessDenied">
            <div className="accessIcon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                <circle cx="12" cy="16" r="1" stroke="currentColor" strokeWidth="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </div>
            <h2>Access Denied</h2>
            <p>You need to be logged in to access private files.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="privateFilesPage">
      <div className="container">
        <div className="privateFilesHeader">
          <h1>Private Files</h1>
          <p>Secure file management for authenticated users</p>
          <div className="userInfo">
            <span className="userBadge">
              Logged in as: {user?.email} ({user?.role === 0 ? 'Administrator' : user?.role === 1 ? 'Manager' : 'User'})
            </span>
          </div>
        </div>

        <div className="privateFilesContent">
          {/* Upload Section */}
          <div className="uploadSection">
            <div className="uploadCard private">
              <div className="uploadIcon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                  <circle cx="12" cy="16" r="1" stroke="currentColor" strokeWidth="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <div className="uploadContent">
                <h3>Upload Private File</h3>
                <p>Securely upload files that only you can access</p>
                <label className="uploadButton">
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    disabled={uploading}
                    style={{ display: 'none' }}
                  />
                  {uploading ? 'Uploading...' : 'Choose Private File'}
                </label>
              </div>
            </div>
          </div>

          {/* Files List */}
          <div className="filesListSection">
            <div className="filesListHeader">
              <h2>Private Files ({files.length})</h2>
              <button className="refreshButton" onClick={fetchFiles}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <polyline points="23 4 23 10 17 10" stroke="currentColor" strokeWidth="2"/>
                  <path d="M20.49 15A9 9 0 1 1 5.64 5.64L23 10" stroke="currentColor" strokeWidth="2"/>
                </svg>
                Refresh
              </button>
            </div>

            {error && (
              <div className="errorMessage">
                {error}
                <button onClick={() => setError(null)}>×</button>
              </div>
            )}

            {loading ? (
              <div className="loading">Loading private files...</div>
            ) : files.length === 0 ? (
              <div className="emptyState">
                <div className="emptyIcon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                    <circle cx="12" cy="16" r="1" stroke="currentColor" strokeWidth="2"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </div>
                <h3>No private files found</h3>
                <p>Your secure files will appear here</p>
              </div>
            ) : (
              <div className="filesGrid">
                {files.map((file, index) => (
                  <div key={index} className="fileCard private">
                    <div className="fileIcon private">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" strokeWidth="2"/>
                        <circle cx="12" cy="16" r="1" stroke="currentColor" strokeWidth="2"/>
                        <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <div className="fileInfo">
                      <div className="fileName">{file.name || file}</div>
                      <div className="fileSize">
                        {file.size ? `${(file.size / 1024).toFixed(1)} KB` : 'Unknown size'}
                      </div>
                      <div className="fileSecurity">
                        <span className="securityBadge">🔒 Private</span>
                      </div>
                    </div>
                    <div className="fileActions">
                      <button
                        className="downloadButton"
                        onClick={() => handleDownload(file.name || file)}
                        title="Download"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" stroke="currentColor" strokeWidth="2"/>
                          <polyline points="7,10 12,15 17,10" stroke="currentColor" strokeWidth="2"/>
                          <line x1="12" y1="15" x2="12" y2="3" stroke="currentColor" strokeWidth="2"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* User Management Section */}
          {user?.role === 0 && (
            <div className="userManagementSection">
              <div className="managementCard">
                <div className="managementContent">
                  <h2>Шаблоны</h2>
                  <div className="managementForm">
                    <div className="formGroup">
                      <label htmlFor="adminTemplateName">Template Name</label>
                      <input
                        type="text"
                        id="adminTemplateName"
                        placeholder="Enter template name"
                      />
                    </div>

                    <div className="formGroup">
                      <label htmlFor="adminTemplateDescription">Template Description</label>
                      <textarea
                        id="adminTemplateDescription"
                        placeholder="Enter template description"
                        rows="4"
                      />
                    </div>

                    <div className="formGroup">
                      <label htmlFor="adminTemplateCategory">Template Category</label>
                      <select id="adminTemplateCategory">
                        <option value="">Select category</option>
                        <option value="web">Web</option>
                        <option value="mobile">Mobile</option>
                        <option value="desktop">Desktop</option>
                        <option value="other">Other</option>
                      </select>
                    </div>

                    <div className="formGroup">
                      <label htmlFor="adminTemplateTags">Template Tags</label>
                      <input
                        type="text"
                        id="adminTemplateTags"
                        placeholder="Enter tags separated by commas"
                      />
                    </div>

                    <button className="actionButton primary">Create Template</button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PrivateFiles;
