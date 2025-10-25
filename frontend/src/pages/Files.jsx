import React, { useState, useEffect } from 'react';
import { apiClient } from '../utils/api';
import './Files.css';

const Files = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiClient.getFileList(false);
      setFiles(response || []);
    } catch (error) {
      console.error('Error fetching files:', error);
      setError('Failed to load files');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      await apiClient.uploadFile(file, false);
      await fetchFiles(); // Refresh the list
    } catch (error) {
      console.error('Error uploading file:', error);
      setError('Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (filename) => {
    try {
      const linkData = await apiClient.getFileLink(filename, false);
      if (linkData && linkData.temp_link) {
        window.open(linkData.temp_link, '_blank');
      }
    } catch (error) {
      console.error('Error getting file link:', error);
      setError('Failed to get download link');
    }
  };

  return (
    <div className="filesPage">
      <div className="container">
        <div className="filesHeader">
          <h1>Public Files</h1>
          <p>Upload and manage public files</p>
        </div>

        <div className="filesContent">
          {/* Upload Section */}
          <div className="uploadSection">
            <div className="uploadCard">
              <div className="uploadIcon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                  <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                  <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" strokeWidth="2"/>
                  <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" strokeWidth="2"/>
                  <polyline points="10,9 9,9 8,9" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </div>
              <div className="uploadContent">
                <h3>Upload File</h3>
                <p>Choose a file to upload to the public directory</p>
                <label className="uploadButton">
                  <input
                    type="file"
                    onChange={handleFileUpload}
                    disabled={uploading}
                    style={{ display: 'none' }}
                  />
                  {uploading ? 'Uploading...' : 'Choose File'}
                </label>
              </div>
            </div>
          </div>

          {/* Files List */}
          <div className="filesListSection">
            <div className="filesListHeader">
              <h2>Files ({files.length})</h2>
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
              <div className="loading">Loading files...</div>
            ) : files.length === 0 ? (
              <div className="emptyState">
                <div className="emptyIcon">
                  <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                    <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                  </svg>
                </div>
                <h3>No files found</h3>
                <p>Upload your first file to get started</p>
              </div>
            ) : (
              <div className="filesGrid">
                {files.map((file, index) => (
                  <div key={index} className="fileCard">
                    <div className="fileIcon">
                      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" strokeWidth="2"/>
                        <polyline points="14,2 14,8 20,8" stroke="currentColor" strokeWidth="2"/>
                      </svg>
                    </div>
                    <div className="fileInfo">
                      <div className="fileName">{file.name || file}</div>
                      <div className="fileSize">
                        {file.size ? `${(file.size / 1024).toFixed(1)} KB` : 'Unknown size'}
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
        </div>
      </div>
    </div>
  );
};

export default Files;
