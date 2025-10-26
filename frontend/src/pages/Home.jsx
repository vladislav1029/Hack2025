import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import { apiClient } from '../utils/api';
import Card from '../components/Cards/Card';
import Modal from '../components/Modal/Modal';
import Filter from '../components/Filter/Filter';
import './Home.css';
import './CreateProject.css';

const Home = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm();
  const [expandedCards, setExpandedCards] = useState(new Set());
  const [modalLoading, setModalLoading] = useState(false);
  const [referenceData, setReferenceData] = useState({
    stages: [],
    services: [],
    users: [],
    payments: [],
    businessSegments: [],
    evaluations: []
  });
  const [cards, setCards] = useState([
    {
      id: 1,
      title: '',
      subtitle: '',
      price: '',
      deliveryTime: ''
    }
  ]);

  useEffect(() => {
    if (isModalOpen) {
      loadReferenceData();
    }
  }, [isModalOpen]);

  const loadReferenceData = async () => {
    try {
      setModalLoading(true);
      const [
        stages,
        services,
        users,
        payments,
        businessSegments,
        evaluations
      ] = await Promise.all([
        apiClient.getStages().catch(() => []),
        apiClient.getServices().catch(() => []),
        apiClient.getUsers().catch(() => []),
        apiClient.getPayments().catch(() => []),
        apiClient.getBusinessSegments().catch(() => []),
        apiClient.getEvaluations().catch(() => [])
      ]);

      setReferenceData({
        stages,
        services,
        users,
        payments,
        businessSegments,
        evaluations
      });
    } catch (error) {
      console.warn('Reference data loading failed:', error);
      // Don't show error toast, just use empty arrays
    } finally {
      setModalLoading(false);
    }
  };

  const onSubmit = async (data) => {
    try {
      setModalLoading(true);
      await apiClient.createProject(data);
      toast.success('Проект успешно создан!');
      setIsModalOpen(false);
    } catch (error) {
      toast.error('Не удалось создать проект');
    } finally {
      setModalLoading(false);
    }
  };

  const handleDeleteCard = (cardId) => {
    setCards(prevCards => prevCards.filter(card => card.id !== cardId));
  };

  const handleCardExpand = (cardId) => {
    setExpandedCards(prev => {
      const newSet = new Set(prev);
      if (newSet.has(cardId)) {
        newSet.delete(cardId);
      } else {
        newSet.add(cardId);
      }
      return newSet;
    });
  };

  return (
    <div className="homePage">
      <div className="container">
        <div className="content">
          <div className="filterContainer">
            <Filter />
          </div>
          <div className="cardsGrid">
            {cards.map(card => (
              card.title === '' ? (
                <Card
                  key={card.id}
                  title={card.title}
                  subtitle={card.subtitle}
                  price={card.price}
                  deliveryTime={card.deliveryTime}
                  buttonText="+"
                  onButtonClick={() => setIsModalOpen(true)}
                />
              ) : (
                <Card
                  key={card.id}
                  title={card.title}
                  subtitle={card.subtitle}
                  price={card.price}
                  deliveryTime={card.deliveryTime}
                  buttonText="-"
                  onButtonClick={() => handleDeleteCard(card.id)}
                  onExpand={() => handleCardExpand(card.id)}
                  isExpanded={expandedCards.has(card.id)}
                />
              )
            ))}
          </div>
        </div>
      </div>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <div className="modalContent">
          <h1>Создать новый проект</h1>
          {modalLoading ? (
            <div className="loading">Загрузка...</div>
          ) : (
            <form onSubmit={handleSubmit(onSubmit)} className="createProjectForm">
              {/* Basic Information */}
              <div className="formSection">
                <h2>Основная информация</h2>

                <div className="formGroup">
                  <label htmlFor="name">Название проекта*</label>
                  <input
                    id="name"
                    {...register('name', { required: 'Название проекта обязательно' })}
                    placeholder="Введите название проекта"
                  />
                  {errors.name && <span className="error">{errors.name.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="organization_name">Название организации*</label>
                  <input
                    id="organization_name"
                    {...register('organization_name', { required: 'Название организации обязательно' })}
                    placeholder="Введите название организации"
                  />
                  {errors.organization_name && <span className="error">{errors.organization_name.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="inn">ИНН*</label>
                  <input
                    id="inn"
                    {...register('inn', { required: 'ИНН обязателен' })}
                    placeholder="Введите ИНН"
                  />
                  {errors.inn && <span className="error">{errors.inn.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="industry_manager">Индустриальный менеджер</label>
                  <input
                    id="industry_manager"
                    {...register('industry_manager')}
                    placeholder="Введите индустриального менеджера"
                  />
                </div>

                <div className="formGroup">
                  <label htmlFor="project_number">Номер проекта</label>
                  <input
                    id="project_number"
                    {...register('project_number')}
                    placeholder="Введите номер проекта"
                  />
                </div>

                <div className="formGroup">
                  <label htmlFor="implementation_year">Год реализации</label>
                  <input
                    id="implementation_year"
                    type="number"
                    {...register('implementation_year', { valueAsNumber: true })}
                    placeholder="Введите год реализации"
                  />
                </div>
              </div>

              {/* References */}
              <div className="formSection">
                <h2>Справочники</h2>

                <div className="formGroup">
                  <label htmlFor="service_id">Услуга*</label>
                  <select
                    id="service_id"
                    {...register('service_id', { required: 'Услуга обязательна' })}
                  >
                    <option value="">Выберите услугу</option>
                    {referenceData.services.map(service => (
                      <option key={service.oid} value={service.oid}>
                        {service.name}
                      </option>
                    ))}
                  </select>
                  {errors.service_id && <span className="error">{errors.service_id.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="manager_id">Менеджер</label>
                  <input
                    id="manager_id"
                    {...register('manager_id')}
                    placeholder="Введите имя менеджера"
                  />
                </div>

                <div className="formGroup">
                  <label htmlFor="stage_id">Стадия*</label>
                  <select
                    id="stage_id"
                    {...register('stage_id', { required: 'Стадия обязательна' })}
                  >
                    <option value="">Выберите стадию</option>
                    {referenceData.stages.map(stage => (
                      <option key={stage.oid} value={stage.oid}>
                        {stage.name}
                      </option>
                    ))}
                  </select>
                  {errors.stage_id && <span className="error">{errors.stage_id.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="payment_type_id">Тип оплаты*</label>
                  <select
                    id="payment_type_id"
                    {...register('payment_type_id', { required: 'Тип оплаты обязателен' })}
                  >
                    <option value="">Выберите тип оплаты</option>
                    {referenceData.payments.map(payment => (
                      <option key={payment.oid} value={payment.oid}>
                        {payment.name}
                      </option>
                    ))}
                  </select>
                  {errors.payment_type_id && <span className="error">{errors.payment_type_id.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="business_segment_id">Бизнес-сегмент*</label>
                  <select
                    id="business_segment_id"
                    {...register('business_segment_id', { required: 'Бизнес-сегмент обязателен' })}
                  >
                    <option value="">Выберите бизнес-сегмент</option>
                    {referenceData.businessSegments.map(segment => (
                      <option key={segment.oid} value={segment.oid}>
                        {segment.name}
                      </option>
                    ))}
                  </select>
                  {errors.business_segment_id && <span className="error">{errors.business_segment_id.message}</span>}
                </div>

                <div className="formGroup">
                  <label htmlFor="accepted_for_evaluation_id">Принято для оценки</label>
                  <select
                    id="accepted_for_evaluation_id"
                    {...register('accepted_for_evaluation_id')}
                  >
                    <option value="">Выберите оценку</option>
                    {referenceData.evaluations.map(evaluation => (
                      <option key={evaluation.oid} value={evaluation.oid}>
                        {evaluation.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Status */}
              <div className="formSection">
                <h2>Информация о статусе</h2>

                <div className="formGroup">
                  <label htmlFor="current_status">Текущий статус</label>
                  <textarea
                    id="current_status"
                    {...register('current_status')}
                    placeholder="Введите текущий статус"
                    rows="3"
                  />
                </div>

                <div className="formGroup">
                  <label htmlFor="completed_this_period">Выполнено за период</label>
                  <textarea
                    id="completed_this_period"
                    {...register('completed_this_period')}
                    placeholder="Введите что было выполнено за период"
                    rows="3"
                  />
                </div>

                <div className="formGroup">
                  <label htmlFor="plans_next_period">Планы на следующий период</label>
                  <textarea
                    id="plans_next_period"
                    {...register('plans_next_period')}
                    placeholder="Введите планы на следующий период"
                    rows="3"
                  />
                </div>

                <div className="formGroup">
                  <label htmlFor="probability">Вероятность (%)</label>
                  <input
                    id="probability"
                    type="number"
                    min="0"
                    max="100"
                    {...register('probability', {
                      valueAsNumber: true,
                      min: { value: 0, message: 'Вероятность должна быть не менее 0' },
                      max: { value: 100, message: 'Вероятность должна быть не более 100' }
                    })}
                    placeholder="Введите вероятность (0-100)"
                  />
                  {errors.probability && <span className="error">{errors.probability.message}</span>}
                  {watch('probability') > 0 && (
                    <div className="probability-indicator">
                      Вероятность: {watch('probability')}%
                    </div>
                  )}
                </div>
              </div>

              {/* Booleans */}
              <div className="formSection">
                <h2>Флаги проекта</h2>

                <div className="formGroup checkboxGroup">
                  <label className="checkboxLabel">
                    <input
                      type="checkbox"
                      {...register('is_industry_solution')}
                    />
                    Индустриальное решение
                  </label>
                </div>

                <div className="formGroup checkboxGroup">
                  <label className="checkboxLabel">
                    <input
                      type="checkbox"
                      {...register('is_forecast_accepted')}
                    />
                    Прогноз принят
                  </label>
                </div>

                <div className="formGroup checkboxGroup">
                  <label className="checkboxLabel">
                    <input
                      type="checkbox"
                      {...register('is_dzo_implementation')}
                    />
                    Реализация ДЗО
                  </label>
                </div>

                <div className="formGroup checkboxGroup">
                  <label className="checkboxLabel">
                    <input
                      type="checkbox"
                      {...register('requires_management_control')}
                    />
                    Требует управления
                  </label>
                </div>
              </div>

              <button type="submit" className="submitBtn" disabled={modalLoading}>
                {modalLoading ? 'Создание...' : 'Создать проект'}
              </button>
            </form>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default Home;
