// frontend/src/components/UserRegistration.js
import React, { useState } from 'react';
import axios from 'axios';

const UserRegistration = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/register', formData);
      console.log(response.data);
    } catch (error) {
      console.error('Registration error:', error.response.data);
    }
  };

  return (
    <div>
      <h2>User Registration</h2>
      <form onSubmit={handleSubmit}>
        <label>Username:</label>
        <input type="text" name="username" onChange={handleChange} required />
        <br />
        <label>Email:</label>
        <input type="email" name="email" onChange={handleChange} required />
        <br />
        <label>Password:</label>
        <input type="password" name="password" onChange={handleChange} required />
        <br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default UserRegistration;
