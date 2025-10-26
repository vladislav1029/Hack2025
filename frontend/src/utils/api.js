// API client for authentication and other backend operations
import axios from 'axios';
const API_BASE_URL = 'http://localhost:8000'; // FastAPI backend URL

class ApiError extends Error {
  constructor(message, status, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

// Create axios instance
const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include JWT token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry && !originalRequest.skipAuthRefresh) {
      // Check if user is logging out
      if (localStorage.getItem('logging_out')) {
        // Do not attempt refresh, just reject
        return Promise.reject(error);
      }
      originalRequest._retry = true;
      try {
        const refreshResponse = await axios.post(`${API_BASE_URL}/account/refresh`);
        const { access_token, token_type } = refreshResponse.data;
        localStorage.setItem('access_token', access_token);
        originalRequest.headers.Authorization = `${token_type.charAt(0).toUpperCase() + token_type.slice(1)} ${access_token}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

class ApiClient {
  async login(username, password) {
    try {
      const response = await axiosInstance.post('/account/login', new URLSearchParams({
        username,
        password,
        grant_type: 'password'
      }), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async register(email, password) {
    try {
      const response = await axiosInstance.post('/account/', { email, password });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getCurrentUser() {
    try {
      const response = await axiosInstance.get('/account/me');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async logout() {
    try {
      const response = await axiosInstance.post('/account/logout', {}, {
        skipAuthRefresh: true, // Skip auth refresh interceptor for logout
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async refreshToken() {
    try {
      const response = await axiosInstance.get('/account/refresh');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // File operations (if needed)
  async uploadFile(file, isPrivate = false) {
    const formData = new FormData();
    formData.append('file', file);

    const endpoint = isPrivate ? '/private/upload' : '/file/upload';

    try {
      const response = await axiosInstance.post(endpoint, formData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getFileList(isPrivate = false) {
    const endpoint = isPrivate ? '/private/list' : '/file/list';
    try {
      const response = await axiosInstance.get(endpoint);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getFileLink(filename, isPrivate = true) {
    if (!isPrivate) {
      throw new Error('Public files do not support temporary download links');
    }
    try {
      const response = await axiosInstance.get(`/private/link/${filename}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async downloadFile(tempLink) {
    try {
      const response = await axiosInstance.get(`/private/download/${tempLink}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Stages operations
  async getStages() {
    try {
      const response = await axiosInstance.get('/references/stages');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createStage(stageData) {
    try {
      const response = await axiosInstance.post('/references/stages', stageData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getStage(stageId) {
    try {
      const response = await axiosInstance.get(`/references/stages/${stageId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateStage(stageId, stageData) {
    try {
      const response = await axiosInstance.put(`/references/stages/${stageId}`, stageData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteStage(stageId) {
    try {
      const response = await axiosInstance.delete(`/references/stages/${stageId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Services operations
  async getServices() {
    try {
      const response = await axiosInstance.get('/references/service');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createService(serviceData) {
    try {
      const response = await axiosInstance.post('/references/service', serviceData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getService(serviceId) {
    try {
      const response = await axiosInstance.get(`/references/service/${serviceId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateService(serviceId, serviceData) {
    try {
      const response = await axiosInstance.put(`/references/service/${serviceId}`, serviceData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteService(serviceId) {
    try {
      const response = await axiosInstance.delete(`/references/service/${serviceId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Payment operations
  async getPayments() {
    try {
      const response = await axiosInstance.get('/references/payment');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createPayment(paymentData) {
    try {
      const response = await axiosInstance.post('/references/payment', paymentData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getPayment(paymentId) {
    try {
      const response = await axiosInstance.get(`/references/payment/${paymentId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updatePayment(paymentId, paymentData) {
    try {
      const response = await axiosInstance.put(`/references/payment/${paymentId}`, paymentData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deletePayment(paymentId) {
    try {
      const response = await axiosInstance.delete(`/references/payment/${paymentId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Business Segment operations
  async getBusinessSegments() {
    try {
      const response = await axiosInstance.get('/references/business_segment');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createBusinessSegment(businessSegmentData) {
    try {
      const response = await axiosInstance.post('/references/business_segment', businessSegmentData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getBusinessSegment(businessSegmentId) {
    try {
      const response = await axiosInstance.get(`/references/business_segment/${businessSegmentId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateBusinessSegment(businessSegmentId, businessSegmentData) {
    try {
      const response = await axiosInstance.put(`/references/business_segment/${businessSegmentId}`, businessSegmentData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteBusinessSegment(businessSegmentId) {
    try {
      const response = await axiosInstance.delete(`/references/business_segment/${businessSegmentId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Cost operations
  async getCosts() {
    try {
      const response = await axiosInstance.get('/references/cost');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createCost(costData) {
    try {
      const response = await axiosInstance.post('/references/cost', costData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getCost(costId) {
    try {
      const response = await axiosInstance.get(`/references/cost/${costId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateCost(costId, costData) {
    try {
      const response = await axiosInstance.put(`/references/cost/${costId}`, costData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteCost(costId) {
    try {
      const response = await axiosInstance.delete(`/references/cost/${costId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Evaluation operations
  async getEvaluations() {
    try {
      const response = await axiosInstance.get('/references/evaluation');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createEvaluation(evaluationData) {
    try {
      const response = await axiosInstance.post('/references/evaluation', evaluationData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getEvaluation(evaluationId) {
    try {
      const response = await axiosInstance.get(`/references/evaluation/${evaluationId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateEvaluation(evaluationId, evaluationData) {
    try {
      const response = await axiosInstance.put(`/references/evaluation/${evaluationId}`, evaluationData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteEvaluation(evaluationId) {
    try {
      const response = await axiosInstance.delete(`/references/evaluation/${evaluationId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Revenue Status operations
  async getRevenueStatuses() {
    try {
      const response = await axiosInstance.get('/references/revenue_status');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createRevenueStatus(revenueStatusData) {
    try {
      const response = await axiosInstance.post('/references/revenue_status', revenueStatusData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getRevenueStatus(revenueStatusId) {
    try {
      const response = await axiosInstance.get(`/references/revenue_status/${revenueStatusId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateRevenueStatus(revenueStatusId, revenueStatusData) {
    try {
      const response = await axiosInstance.put(`/references/revenue_status/${revenueStatusId}`, revenueStatusData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteRevenueStatus(revenueStatusId) {
    try {
      const response = await axiosInstance.delete(`/references/revenue_status/${revenueStatusId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  // Cost Status operations
  async getCostStatuses() {
    try {
      const response = await axiosInstance.get('/references/cost_status');
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async createCostStatus(costStatusData) {
    try {
      const response = await axiosInstance.post('/references/cost_status', costStatusData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async getCostStatus(costStatusId) {
    try {
      const response = await axiosInstance.get(`/references/cost_status/${costStatusId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async updateCostStatus(costStatusId, costStatusData) {
    try {
      const response = await axiosInstance.put(`/references/cost_status/${costStatusId}`, costStatusData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
  }

  async deleteCostStatus(costStatusId) {
    try {
      const response = await axiosInstance.delete(`/references/cost_status/${costStatusId}`);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data?.detail) {
        throw new ApiError(error.response.data.detail, error.response.status, error.response.data);
      }
      throw new ApiError(error.message, error.response?.status || 0);
    }
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
