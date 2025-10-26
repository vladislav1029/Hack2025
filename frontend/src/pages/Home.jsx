import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'react-toastify';
import Card from '../components/Cards/Card';
import Modal from '../components/Modal/Modal';
import Filter from '../components/Filter/Filter';
import './Home.css';

const Home = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm();
  const [expandedCards, setExpandedCards] = useState(new Set());
  const [cards, setCards] = useState([
    {
      id: 1,
      title: 'Inter Pro',
      subtitle: 'Passeel, On rglame',
      price: '9590',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-15')
    },
    {
      id: 2,
      title: 'Inter Pro',
      subtitle: 'Emerges, Fn rglame',
      price: '3990',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-20')
    },
    {
      id: 3,
      title: 'SFor Pro',
      subtitle: 'Passeel, Fn rglame',
      price: '7990',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-10')
    },
    {
      id: 4,
      title: 'Inter Pro',
      subtitle: 'Emsbee, Fn rglame',
      price: '3990',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-25')
    },
    {
      id: 5,
      title: 'Inter Pro',
      subtitle: 'Daasseel, Fn rglame',
      price: '5990',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-12')
    },
    {
      id: 6,
      title: 'Sliject Pro',
      subtitle: 'Dmer nge, Fn rglame',
      price: '5990',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-18')
    },
    {
      id: 7,
      title: 'Inter Pro',
      subtitle: 'Passeel, On rglame',
      price: '9590',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-08')
    },
    {
      id: 8,
      title: 'Inter Pro',
      subtitle: 'Emerges, Fn rglame',
      price: '3990',
      deliveryTime: 'Estimated Delivery Time',
      date: new Date('2025-01-22')
    },
    {
      id: 9,
      title: '',
      subtitle: '',
      price: '',
      deliveryTime: ''
    }
  ]);

  const onSubmit = (data) => {
    // Add new card to the list
    const newCard = {
      id: Date.now(), // Use timestamp as unique ID
      title: data.title,
      subtitle: data.subtitle,
      price: data.price.toString(),
      deliveryTime: data.deliveryTime
    };
    setCards(prevCards => [...prevCards.filter(card => card.title !== ''), newCard]); // Remove empty cards and add new one
    console.log(data);
    toast.success('Project created successfully!');
    setIsModalOpen(false);
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
          <h1>Create New Project</h1>
          <form onSubmit={handleSubmit(onSubmit)} className="createProjectForm">
            <div className="formGroup">
              <label htmlFor="title">Title</label>
              <input
                id="title"
                {...register('title', { required: 'Title is required' })}
                placeholder="Enter project title"
              />
              {errors.title && <span className="error">{errors.title.message}</span>}
            </div>

            <div className="formGroup">
              <label htmlFor="subtitle">Subtitle</label>
              <input
                id="subtitle"
                {...register('subtitle', { required: 'Subtitle is required' })}
                placeholder="Enter project subtitle"
              />
              {errors.subtitle && <span className="error">{errors.subtitle.message}</span>}
            </div>

            <div className="formGroup">
              <label htmlFor="price">Price</label>
              <input
                id="price"
                type="number"
                {...register('price', { required: 'Price is required', min: { value: 0, message: 'Price must be positive' } })}
                placeholder="Enter price"
              />
              {errors.price && <span className="error">{errors.price.message}</span>}
            </div>

            <div className="formGroup">
              <label htmlFor="deliveryTime">Delivery Time</label>
              <input
                id="deliveryTime"
                {...register('deliveryTime', { required: 'Delivery time is required' })}
                placeholder="Enter estimated delivery time"
              />
              {errors.deliveryTime && <span className="error">{errors.deliveryTime.message}</span>}
            </div>

            <button type="submit" className="submitBtn">&#10003;</button>
          </form>
        </div>
      </Modal>
    </div>
  );
};

export default Home;
