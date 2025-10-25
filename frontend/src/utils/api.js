// API client for authentication and other backend operations
const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

class ApiClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    // Add JWT token if available
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        let errorDetails = null;

        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorMessage;
          errorDetails = errorData;
        } catch (e) {
          // If response is not JSON, use status text
          errorMessage = response.statusText || errorMessage;
        }

        throw new ApiError(errorMessage, response.status, errorDetails);
      }

      // Handle empty responses
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }

      return await response.text();
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }

      // Network or other errors
      throw new ApiError(
        `Network error: ${error.message}`,
        0,
        { originalError: error }
      );
    }
  }

  // Authentication methods
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    return this.request('/account/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });
  }

  async register(email, password) {
    return this.request('/account/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async getCurrentUser() {
    return this.request('/account/me');
  }

  async logout() {
    return this.request('/account/logout', {
      method: 'POST',
    });
  }

  async refreshToken() {
    return this.request('/account/refresh');
  }

  // File operations (if needed)
  async uploadFile(file, isPrivate = false) {
    const formData = new FormData();
    formData.append('file', file);

    const endpoint = isPrivate ? '/private/upload' : '/file/upload';

    return this.request(endpoint, {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData,
    });
  }

  async getFileList(isPrivate = false) {
    const endpoint = isPrivate ? '/private/list' : '/file/list';
    return this.request(endpoint);
  }

  async getFileLink(filename, isPrivate = false) {
    const endpoint = isPrivate ? `/private/link/${filename}` : `/file/link/${filename}`;
    return this.request(endpoint);
  }

  async downloadFile(tempLink) {
    return this.request(`/private/download/${tempLink}`);
  }
}

// Create and export API client instance
export const apiClient = new ApiClient(API_BASE_URL);

// Export auth-specific API functions
export const authAPI = {
  login: (username, password) => apiClient.login(username, password),
  register: (email, password) => apiClient.register(email, password),
  getCurrentUser: () => apiClient.getCurrentUser(),
  logout: () => apiClient.logout(),
  refreshToken: () => apiClient.refreshToken(),
};

// Export ApiError for error handling
export { ApiError };
