import React, { useState, useEffect } from 'react';
import { apiClient } from '../utils/api.js';
import { toast } from 'react-toastify';
import './Templates.css';

const Templates = () => {
  const [stages, setStages] = useState([]);
  const [services, setServices] = useState([]);
  const [payments, setPayments] = useState([]);
  const [businessSegments, setBusinessSegments] = useState([]);
  const [costs, setCosts] = useState([]);
  const [evaluations, setEvaluations] = useState([]);
  const [revenueStatuses, setRevenueStatuses] = useState([]);
  const [costStatuses, setCostStatuses] = useState([]);
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
  const [costFormData, setCostFormData] = useState({
    name: ''
  });
  const [evaluationFormData, setEvaluationFormData] = useState({
    name: ''
  });
  const [revenueStatusFormData, setRevenueStatusFormData] = useState({
    name: ''
  });
  const [costStatusFormData, setCostStatusFormData] = useState({
    name: ''
  });

  // Edit mode state
  const [editingItem, setEditingItem] = useState(null);
  const [editFormData, setEditFormData] = useState({
    name: '',
    probability: 0
  });

  useEffect(() => {
    loadStages();
    loadServices();
    loadPayments();
    loadBusinessSegments();
    loadCosts();
    loadEvaluations();
    loadRevenueStatuses();
    loadCostStatuses();
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

  const loadCosts = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getCosts();
      setCosts(data);
    } catch (error) {
      toast.error('Failed to load costs');
      console.error('Error loading costs:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadEvaluations = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getEvaluations();
      setEvaluations(data);
    } catch (error) {
      toast.error('Failed to load evaluations');
      console.error('Error loading evaluations:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadRevenueStatuses = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getRevenueStatuses();
      setRevenueStatuses(data);
    } catch (error) {
      toast.error('Failed to load revenue statuses');
      console.error('Error loading revenue statuses:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCostStatuses = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getCostStatuses();
      setCostStatuses(data);
    } catch (error) {
      toast.error('Failed to load cost statuses');
      console.error('Error loading cost statuses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await apiClient.createStage(formData);
      toast.success('Stage created successfully');
      setFormData({ name: '', probability: 0 });
      loadStages();
    } catch (error) {
      toast.error('Failed to create stage');
      console.error('Error saving stage:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await apiClient.createService(serviceFormData);
      toast.success('Service created successfully');
      setServiceFormData({ name: '' });
      loadServices();
    } catch (error) {
      toast.error('Failed to create service');
      console.error('Error saving service:', error);
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

  const handleServiceInputChange = (e) => {
    const { name, value } = e.target;
    setServiceFormData(prev => ({
      ...prev,
      [name]: value
    }));
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
      await apiClient.createPayment(paymentFormData);
      toast.success('Payment created successfully');
      setPaymentFormData({ name: '' });
      loadPayments();
    } catch (error) {
      toast.error('Failed to create payment');
      console.error('Error saving payment:', error);
    } finally {
      setLoading(false);
    }
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
      await apiClient.createBusinessSegment(businessSegmentFormData);
      toast.success('Business segment created successfully');
      setBusinessSegmentFormData({ name: '' });
      loadBusinessSegments();
    } catch (error) {
      toast.error('Failed to create business segment');
      console.error('Error saving business segment:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCostInputChange = (e) => {
    const { name, value } = e.target;
    setCostFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCostSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await apiClient.createCost(costFormData);
      toast.success('Cost created successfully');
      setCostFormData({ name: '' });
      loadCosts();
    } catch (error) {
      toast.error('Failed to create cost');
      console.error('Error saving cost:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluationInputChange = (e) => {
    const { name, value } = e.target;
    setEvaluationFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEvaluationSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await apiClient.createEvaluation(evaluationFormData);
      toast.success('Evaluation created successfully');
      setEvaluationFormData({ name: '' });
      loadEvaluations();
    } catch (error) {
      toast.error('Failed to create evaluation');
      console.error('Error saving evaluation:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRevenueStatusInputChange = (e) => {
    const { name, value } = e.target;
    setRevenueStatusFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleRevenueStatusSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await apiClient.createRevenueStatus(revenueStatusFormData);
      toast.success('Revenue status created successfully');
      setRevenueStatusFormData({ name: '' });
      loadRevenueStatuses();
    } catch (error) {
      toast.error('Failed to create revenue status');
      console.error('Error saving revenue status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCostStatusInputChange = (e) => {
    const { name, value } = e.target;
    setCostStatusFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCostStatusSubmit = async (e) => {
    e.preventDefault();
    try {
      setLoading(true);
      await apiClient.createCostStatus(costStatusFormData);
      toast.success('Cost status created successfully');
      setCostStatusFormData({ name: '' });
      loadCostStatuses();
    } catch (error) {
      toast.error('Failed to create cost status');
      console.error('Error saving cost status:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle starting edit
  const handleEdit = (template) => {
    setEditingItem(`${template.typeId}-${template.oid}`);
    setEditFormData({
      name: template.name,
      probability: template.probability || 0
    });
  };

  // Handle canceling edit
  const handleCancelEdit = () => {
    setEditingItem(null);
    setEditFormData({ name: '', probability: 0 });
  };

  // Handle saving edit
  const handleSaveEdit = async (template) => {
    try {
      setLoading(true);
      const updateData = template.typeId === 'stage'
        ? { name: editFormData.name, probability: editFormData.probability }
        : { name: editFormData.name };

      let apiMethod;
      switch (template.typeId) {
        case 'stage':
          apiMethod = apiClient.updateStage;
          break;
        case 'service':
          apiMethod = apiClient.updateService;
          break;
        case 'payment':
          apiMethod = apiClient.updatePayment;
          break;
        case 'businessSegment':
          apiMethod = apiClient.updateBusinessSegment;
          break;
        case 'cost':
          apiMethod = apiClient.updateCost;
          break;
        case 'evaluation':
          apiMethod = apiClient.updateEvaluation;
          break;
        case 'revenueStatus':
          apiMethod = apiClient.updateRevenueStatus;
          break;
        case 'costStatus':
          apiMethod = apiClient.updateCostStatus;
          break;
        default:
          throw new Error('Unknown template type');
      }

      await apiMethod(template.oid, updateData);
      toast.success('Изменения сохранены успешно');

      // Reload data
      switch (template.typeId) {
        case 'stage':
          loadStages();
          break;
        case 'service':
          loadServices();
          break;
        case 'payment':
          loadPayments();
          break;
        case 'businessSegment':
          loadBusinessSegments();
          break;
        case 'cost':
          loadCosts();
          break;
        case 'evaluation':
          loadEvaluations();
          break;
        case 'revenueStatus':
          loadRevenueStatuses();
          break;
        case 'costStatus':
          loadCostStatuses();
          break;
      }

      handleCancelEdit();
    } catch (error) {
      toast.error('Ошибка при сохранении изменений');
      console.error('Error updating item:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle delete
  const handleDelete = async (template) => {
    if (!window.confirm(`Вы уверены, что хотите удалить "${template.name}"?`)) {
      return;
    }

    try {
      setLoading(true);

      let apiMethod;
      switch (template.typeId) {
        case 'stage':
          apiMethod = apiClient.deleteStage;
          break;
        case 'service':
          apiMethod = apiClient.deleteService;
          break;
        case 'payment':
          apiMethod = apiClient.deletePayment;
          break;
        case 'businessSegment':
          apiMethod = apiClient.deleteBusinessSegment;
          break;
        case 'cost':
          apiMethod = apiClient.deleteCost;
          break;
        case 'evaluation':
          apiMethod = apiClient.deleteEvaluation;
          break;
        case 'revenueStatus':
          apiMethod = apiClient.deleteRevenueStatus;
          break;
        case 'costStatus':
          apiMethod = apiClient.deleteCostStatus;
          break;
        default:
          throw new Error('Unknown template type');
      }

      await apiMethod(template.oid);
      toast.success('Элемент удален успешно');

      // Reload data
      switch (template.typeId) {
        case 'stage':
          loadStages();
          break;
        case 'service':
          loadServices();
          break;
        case 'payment':
          loadPayments();
          break;
        case 'businessSegment':
          loadBusinessSegments();
          break;
        case 'cost':
          loadCosts();
          break;
        case 'evaluation':
          loadEvaluations();
          break;
        case 'revenueStatus':
          loadRevenueStatuses();
          break;
        case 'costStatus':
          loadCostStatuses();
          break;
      }
    } catch (error) {
      toast.error('Ошибка при удалении элемента');
      console.error('Error deleting item:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle edit form input change
  const handleEditInputChange = (e) => {
    const { name, value } = e.target;
    setEditFormData(prev => ({
      ...prev,
      [name]: name === 'probability' ? parseFloat(value) || 0 : value
    }));
  };

  // Combine all template data into a single table
  const allTemplates = [
    ...stages.map(s => ({ ...s, type: 'Этап', typeId: 'stage' })),
    ...services.map(s => ({ ...s, type: 'Услуга', typeId: 'service' })),
    ...payments.map(p => ({ ...p, type: 'Платеж', typeId: 'payment' })),
    ...businessSegments.map(bs => ({ ...bs, type: 'Бизнес-сегмент', typeId: 'businessSegment' })),
    ...costs.map(c => ({ ...c, type: 'Затраты', typeId: 'cost' })),
    ...evaluations.map(e => ({ ...e, type: 'Оценка', typeId: 'evaluation' })),
    ...revenueStatuses.map(rs => ({ ...rs, type: 'Статус доходов', typeId: 'revenueStatus' })),
    ...costStatuses.map(cs => ({ ...cs, type: 'Статус затрат', typeId: 'costStatus' }))
  ];

  return (
    <div className="templatePanel">
      <h1>Управление справочниками</h1>

      <div className="templatesTableContainer">
        <table className="templatesTable">
          <thead>
            <tr>
              <th>Тип</th>
              <th>Название</th>
              <th>Дополнительная информация</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {/* Add new item rows */}
            <tr className="newItemRow">
              <td>Этап</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  placeholder="Название этапа"
                />
              </td>
              <td>
                <input
                  type="number"
                  name="probability"
                  value={formData.probability}
                  onChange={handleInputChange}
                  placeholder="Вероятность (%)"
                  min="0"
                  max="100"
                  step="0.1"
                />
              </td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Услуга</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={serviceFormData.name}
                  onChange={handleServiceInputChange}
                  placeholder="Название услуги"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleServiceSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Платеж</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={paymentFormData.name}
                  onChange={handlePaymentInputChange}
                  placeholder="Название платежа"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handlePaymentSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Бизнес-сегмент</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={businessSegmentFormData.name}
                  onChange={handleBusinessSegmentInputChange}
                  placeholder="Название бизнес-сегмента"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleBusinessSegmentSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Затраты</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={costFormData.name}
                  onChange={handleCostInputChange}
                  placeholder="Название затрат"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleCostSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Оценка</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={evaluationFormData.name}
                  onChange={handleEvaluationInputChange}
                  placeholder="Название оценки"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleEvaluationSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Статус доходов</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={revenueStatusFormData.name}
                  onChange={handleRevenueStatusInputChange}
                  placeholder="Название статуса доходов"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleRevenueStatusSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            <tr className="newItemRow">
              <td>Статус затрат</td>
              <td>
                <input
                  type="text"
                  name="name"
                  value={costStatusFormData.name}
                  onChange={handleCostStatusInputChange}
                  placeholder="Название статуса затрат"
                />
              </td>
              <td></td>
              <td>
                <button
                  type="button"
                  className="submitBtn"
                  onClick={handleCostStatusSubmit}
                  disabled={loading}
                >
                  {loading ? 'Создание...' : 'Создать'}
                </button>
              </td>
            </tr>

            {/* Display all existing items */}
            {allTemplates.map(template => {
              const isEditing = editingItem === `${template.typeId}-${template.oid}`;

              return (
                <tr key={`${template.typeId}-${template.oid}`}>
                  <td>{template.type}</td>
                  <td>
                    {isEditing ? (
                      <input
                        type="text"
                        name="name"
                        value={editFormData.name}
                        onChange={handleEditInputChange}
                        placeholder="Название"
                      />
                    ) : (
                      template.name
                    )}
                  </td>
                  <td>
                    {template.typeId === 'stage' && (
                      isEditing ? (
                        <input
                          type="number"
                          name="probability"
                          value={editFormData.probability}
                          onChange={handleEditInputChange}
                          placeholder="Вероятность (%)"
                          min="0"
                          max="100"
                          step="0.1"
                        />
                      ) : (
                        `Вероятность: ${template.probability}%`
                      )
                    )}
                  </td>
                  <td className="actionButtons">
                    {isEditing ? (
                      <>
                        <button
                          className="saveBtn"
                          onClick={() => handleSaveEdit(template)}
                          disabled={loading}
                        >
                          💾 Сохранить
                        </button>
                        <button
                          className="cancelBtn"
                          onClick={handleCancelEdit}
                          disabled={loading}
                        >
                          ❌ Отмена
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          className="editBtn"
                          onClick={() => handleEdit(template)}
                        >
                          ✏️ Редактировать
                        </button>
                        <button
                          className="deleteBtn"
                          onClick={() => handleDelete(template)}
                        >
                          🗑️ Удалить
                        </button>
                      </>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Templates;
