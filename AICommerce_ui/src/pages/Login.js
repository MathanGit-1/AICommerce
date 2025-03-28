import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // ✅ Import useAuth

const Login = () => {
  const [userId, setUserId] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth(); // ✅ Get login from AuthContext

  const handleLogin = () => {
    if (userId.trim() === '') return alert('Please enter a User ID');
    login(userId); // ✅ Sets both localStorage + context state
    navigate('/recommendations'); // ✅ Redirect after login
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow-md w-80">
        <h2 className="text-xl font-bold mb-4 text-center">AICommerce Login</h2>
        <input
          type="text"
          placeholder="Enter User ID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          className="w-full border px-3 py-2 rounded mb-4"
        />
        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Login
        </button>
      </div>
    </div>
  );
};

export default Login;
