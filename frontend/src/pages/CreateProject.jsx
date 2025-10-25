import React from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import './CreateProject.css';

const CreateProject = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = (data) => {
    console.log(data);
    // Here you would typically send the data to an API
    toast.success('Project created successfully!');
    navigate('/');
  };

  return (
    <div className="createProjectPage">
      <div className="container">
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

          <button type="submit" className="submitBtn">Create Project</button>
        </form>
      </div>
    </div>
  );
};

export default CreateProject;
