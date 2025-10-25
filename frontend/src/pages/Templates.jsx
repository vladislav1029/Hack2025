import React, { useState, useEffect } from 'react';
import { apiClient } from '../utils/api.js';
import { toast } from 'react-toastify';
import './Templates.css';

const Templates = () => {
  const [stages, setStages] = useState([]);
  const [services, setServices] = useState([]);
  const [payments, setPayments] = useState([]);
  const [businessSegments, setBusinessSegments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    probability: 0
  });
  const [serviceFormData, setServiceFormData] = useState({
    name: ''
  });
  const [paymentFormData, setPaymentFormData] = useState({
    name: ''
  });
  const [businessSegmentFormData, setBusinessSegmentFormData] = useState({
    name: ''
  });
  const [editingStage, setEditingStage] = useState(null);
  const [editingService, setEditingService] = useState(null);
  const [editingPayment, setEditingPayment] = useState(null);
  const [editingBusinessSegment, setEditingBusinessSegment] = useState(null);

  useEffect(() => {
    loadStages();
    loadServices();
    loadPayments();
    loadBusinessSegments();
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

  const loadPayments = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getPayments();
      setPayments(data);
    } catch (error) {
      toast.error('Failed to load payments');
      console.error('Error loading payments:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadBusinessSegments = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getBusinessSegments();
      setBusinessSegments(data);
    } catch (error) {
      toast.error('Failed to load business segments');
      console.error('Error loading business segments:', error);
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

  const handleStageDelete = async (stageId) => {
    try {
      setLoading(true);
      await apiClient.deleteStage(stageId);
      toast.success('Stage deleted successfully');
      loadStages();
    } catch (error) {
      toast.error('Failed to delete stage');
      console.error('Error deleting stage:', error);
    } finally {
      setLoading(false);
    }
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

  const handlePaymentInputChange = (e) => {
    const { name, value } = e.target;
    setPaymentFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePaymentSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingPayment) {
        await apiClient.updatePayment(editingPayment.oid, paymentFormData);
        toast.success('Payment updated successfully');
      } else {
        await apiClient.createPayment(paymentFormData);
        toast.success('Payment created successfully');
      }
      setPaymentFormData({ name: '' });
      setEditingPayment(null);
      loadPayments();
    } catch (error) {
      toast.error(editingPayment ? 'Failed to update payment' : 'Failed to create payment');
      console.error('Error saving payment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentEdit = (payment) => {
    setPaymentFormData({
      name: payment.name
    });
    setEditingPayment(payment);
  };

  const handlePaymentDelete = async (paymentId) => {
    try {
      setLoading(true);
      await apiClient.deletePayment(paymentId);
      toast.success('Payment deleted successfully');
      loadPayments();
    } catch (error) {
      toast.error('Failed to delete payment');
      console.error('Error deleting payment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentCancel = () => {
    setPaymentFormData({ name: '' });
    setEditingPayment(null);
  };

  const handleBusinessSegmentInputChange = (e) => {
    const { name, value } = e.target;
    setBusinessSegmentFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleBusinessSegmentSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      if (editingBusinessSegment) {
        await apiClient.updateBusinessSegment(editingBusinessSegment.oid, businessSegmentFormData);
        toast.success('Business segment updated successfully');
      } else {
        await apiClient.createBusinessSegment(businessSegmentFormData);
        toast.success('Business segment created successfully');
      }
      setBusinessSegmentFormData({ name: '' });
      setEditingBusinessSegment(null);
      loadBusinessSegments();
    } catch (error) {
      toast.error(editingBusinessSegment ? 'Failed to update business segment' : 'Failed to create business segment');
      console.error('Error saving business segment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBusinessSegmentEdit = (businessSegment) => {
    setBusinessSegmentFormData({
      name: businessSegment.name
    });
    setEditingBusinessSegment(businessSegment);
  };

  const handleBusinessSegmentDelete = async (businessSegmentId) => {
    try {
      setLoading(true);
      await apiClient.deleteBusinessSegment(businessSegmentId);
      toast.success('Business segment deleted successfully');
      loadBusinessSegments();
    } catch (error) {
      toast.error('Failed to delete business segment');
      console.error('Error deleting business segment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBusinessSegmentCancel = () => {
    setBusinessSegmentFormData({ name: '' });
    setEditingBusinessSegment(null);
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
                <div className="serviceActions">
                  <button
                    onClick={() => handleEdit(stage)}
                    className="editBtn"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleStageDelete(stage.oid)}
                    className="deleteBtn"
                  >
                    Delete
                  </button>
                </div>
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

      {/* Payment Form */}
      <div className="templateForm">
        <div className="formGroup">
          <label htmlFor="paymentName">Payment Name</label>
          <input
            type="text"
            id="paymentName"
            name="name"
            value={paymentFormData.name}
            onChange={handlePaymentInputChange}
            placeholder="Enter payment name"
          />
        </div>

        <div className="formActions">
          <button
            type="submit"
            className="submitBtn"
            onClick={handlePaymentSubmit}
            disabled={loading}
          >
            {loading ? (editingPayment ? 'Updating...' : 'Creating...') : (editingPayment ? 'Update Payment' : 'Create Payment')}
          </button>
          {editingPayment && (
            <button
              type="button"
              className="cancelBtn"
              onClick={handlePaymentCancel}
            >
              Cancel
            </button>
          )}
        </div>
      </div>

      {/* Payments List */}
      <div className="stagesList">
        <h2>Existing Payments</h2>
        {loading && payments.length === 0 ? (
          <p>Loading payments...</p>
        ) : payments.length > 0 ? (
          <div className="stagesGrid">
            {payments.map(payment => (
              <div key={payment.oid} className="stageCard">
                <h3>{payment.name}</h3>
                <div className="serviceActions">
                  <button
                    onClick={() => handlePaymentEdit(payment)}
                    className="editBtn"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handlePaymentDelete(payment.oid)}
                    className="deleteBtn"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No payments found</p>
        )}
      </div>

      {/* Business Segment Form */}
      <div className="templateForm">
        <div className="formGroup">
          <label htmlFor="businessSegmentName">Business Segment Name</label>
          <input
            type="text"
            id="businessSegmentName"
            name="name"
            value={businessSegmentFormData.name}
            onChange={handleBusinessSegmentInputChange}
            placeholder="Enter business segment name"
          />
        </div>

        <div className="formActions">
          <button
            type="submit"
            className="submitBtn"
            onClick={handleBusinessSegmentSubmit}
            disabled={loading}
          >
            {loading ? (editingBusinessSegment ? 'Updating...' : 'Creating...') : (editingBusinessSegment ? 'Update Business Segment' : 'Create Business Segment')}
          </button>
          {editingBusinessSegment && (
            <button
              type="button"
              className="cancelBtn"
              onClick={handleBusinessSegmentCancel}
            >
              Cancel
            </button>
          )}
        </div>
      </div>

      {/* Business Segments List */}
      <div className="stagesList">
        <h2>Existing Business Segments</h2>
        {loading && businessSegments.length === 0 ? (
          <p>Loading business segments...</p>
        ) : businessSegments.length > 0 ? (
          <div className="stagesGrid">
            {businessSegments.map(businessSegment => (
              <div key={businessSegment.oid} className="stageCard">
                <h3>{businessSegment.name}</h3>
                <div className="serviceActions">
                  <button
                    onClick={() => handleBusinessSegmentEdit(businessSegment)}
                    className="editBtn"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleBusinessSegmentDelete(businessSegment.oid)}
                    className="deleteBtn"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p>No business segments found</p>
        )}
      </div>
    </div>
  );
};

export default Templates;
