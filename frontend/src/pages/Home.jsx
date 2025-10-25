import React from 'react';
import Card from '../components/Cards/Card';
import Filter from '../components/Filter/Filter';
import './Home.css';

const Home = () => {
  const cards = [
    {
      id: 1,
      title: 'Inter Pro',
      subtitle: 'Passeel, On rglame',
      price: '9590',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 2,
      title: 'Inter Pro',
      subtitle: 'Emerges, Fn rglame',
      price: '3990',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 3,
      title: 'SFor Pro',
      subtitle: 'Passeel, Fn rglame',
      price: '7990',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 4,
      title: 'Inter Pro',
      subtitle: 'Emsbee, Fn rglame',
      price: '3990',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 5,
      title: 'Inter Pro',
      subtitle: 'Daasseel, Fn rglame',
      price: '5990',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 6,
      title: 'Sliject Pro',
      subtitle: 'Dmer nge, Fn rglame',
      price: '5990',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 7,
      title: 'Inter Pro',
      subtitle: 'Passeel, On rglame',
      price: '9590',
      deliveryTime: 'Estimated Delivery Time'
    },
    {
      id: 8,
      title: 'Inter Pro',
      subtitle: 'Emerges, Fn rglame',
      price: '3990',
      deliveryTime: 'Estimated Delivery Time'
    }
  ];

  return (
    <div className="homePage">
      <div className="container">
        <div className="content">
          <div className="cardsGrid">
            {cards.map(card => (
              <Card
                key={card.id}
                title={card.title}
                subtitle={card.subtitle}
                price={card.price}
                deliveryTime={card.deliveryTime}
              />
            ))}
          </div>
          <div className="filterContainer">
            <Filter />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
