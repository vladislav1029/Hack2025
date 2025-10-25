import React, { useState, useEffect } from 'react';
import { apiClient } from '../utils/api.js';
import { toast } from 'react-toastify';
import './Templates.css';

const Templates = () => {
  const [stages, setStages] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    probability: 0
  });
  const [serviceFormData, setServiceFormData] = useState({
    name: ''
  });
  const [editingStage, setEditingStage] = useState(null);
  const [editingService, setEditingService] = useState(null);

  useEffect(() => {
    loadStages();
    loadServices();
  }, []);

  const loadStages = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getStages();
      setStages(data);
    } catch (error) {
      toast.error('Failed to load stages');
      console.error('Error loading stages:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadServices = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getServices();
      setServices(data);
    } catch (error) {
      toast.error('Failed to load services');
      console.error('Error loading services:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'probability' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingStage) {
        await apiClient.updateStage(editingStage.oid, formData);
        toast.success('Stage updated successfully');
      } else {
        await apiClient.createStage(formData);
        toast.success('Stage created successfully');
      }
      setFormData({ name: '', probability: 0 });
      setEditingStage(null);
      loadStages();
    } catch (error) {
      toast.error(editingStage ? 'Failed to update stage' : 'Failed to create stage');
      console.error('Error saving stage:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (stage) => {
    setFormData({
      name: stage.name,
      probability: stage.probability
    });
    setEditingStage(stage);
  };

  const handleCancel = () => {
    setFormData({ name: '', probability: 0 });
    setEditingStage(null);
  };

  const handleServiceInputChange = (e) => {
    const { name, value } = e.target;
    setServiceFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleServiceSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingService) {
        await apiClient.updateService(editingService.oid, serviceFormData);
        toast.success('Service updated successfully');
      } else {
        await apiClient.createService(serviceFormData);
        toast.success('Service created successfully');
      }
      setServiceFormData({ name: '' });
      setEditingService(null);
      loadServices();
    } catch (error) {
      toast.error(editingService ? 'Failed to update service' : 'Failed to create service');
      console.error('Error saving service:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceEdit = (service) => {
    setServiceFormData({
      name: service.name
    });
    setEditingService(service);
  };

  const handleServiceDelete = async (serviceId) => {
    try {
      setLoading(true);
      await apiClient.deleteService(serviceId);
      toast.success('Service deleted successfully');
      loadServices();
    } catch (error) {
      toast.error('Failed to delete service');
      console.error('Error deleting service:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceCancel = () => {
    setServiceFormData({ name: '' });
    setEditingService(null);
  };

  return (
    <div className="templatePanel">
      <h1>References Management</h1>

      {/* Stage Form */}
      <div className="templateForm">
        <div className="formGroup">
          <label htmlFor="name">Stage Name</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="Enter stage name"
          />
        </div>

        <div className="formGroup">
          <label htmlFor="probability">Probability (%)</label>
          <input
            type="number"
            id="probability"
            name="probability"
            value={formData.probability}
            onChange={handleInputChange}
            placeholder="Enter probability"
            min="0"
            max="100"
            step="0.1"
          />
        </div>

        <div className="formActions">
          <button
            type="submit"
            className="submitBtn"
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? (editingStage ? 'Updating...' : 'Creating...') : (editingStage ? 'Update Stage' : 'Create Stage')}
          </button>
          {editingStage && (
            <button
              type="button"
              className="cancelBtn"
              onClick={handleCancel}
            >
              Cancel
            </button>
          )}
        </div>
      </div>

      {/* Stages List */}
      <div className="stagesList">
        <h2>Existing Stages</h2>
        {loading && stages.length === 0 ? (
          <p>Loading stages...</p>
        ) : stages.length > 0 ? (
          <div className="stagesGrid">
            {stages.map(stage => (
              <div key={stage.oid} className="stageCard">
                <h3>{stage.name}</h3>
                <p>Probability: {stage.probability}%</p>
                <button
                  onClick={() => handleEdit(stage)}
                  className="editBtn"
                >
                  Edit
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p>No stages found</p>
        )}
      </div>

      {/* Service Form */}
      <div className="templateForm">
        <div className="formGroup">
          <label htmlFor="serviceName">Service Name</label>
          <input
            type="text"
            id="serviceName"
            name="name"
            value={serviceFormData.name}
            onChange={handleServiceInputChange}
            placeholder="Enter service name"
          />
        </div>

        <div className="formActions">
          <button
            type="submit"
            className="submitBtn"
            onClick={handleServiceSubmit}
            disabled={loading}
          >
            {loading ? (editingService ? 'Updating...' : 'Creating...') : (editingService ? 'Update Service' : 'Create Service')}
          </button>
          {editingService && (
            <button
              type="button"
              className="cancelBtn"
              onClick={handleServiceCancel}
            >
              Cancel
            </button>
          )}
        </div>
      </div>

      {/* Services List */}
      <div className="stagesList">
        <h2>Existing Services</h2>
        {loading && services.length === 0 ? (
          <p>Loading services...</p>
        ) : services.length > 0 ? (
          <div className="stagesGrid">
            {services.map(service => (
              <div key={service.oid} className="stageCard">
                <h3>{service.name}</h3>
                <div className="serviceActions">
                  <button
                    onClick={() => handleServiceEdit(service)}
                    className="editBtn"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleServiceDelete(service.oid)}
                    className="deleteBtn"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No services found</p>
        )}
      </div>
    </div>
  );
};

export default Templates;
