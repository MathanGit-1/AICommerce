import React from 'react';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const { userId, logout } = useAuth();

  const handleLogout = () => {
    logout();
    window.location.href = '/login'; // optional: or use navigate if using useNavigate()
  };

  return (
    <header className="bg-white shadow p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold text-gray-800">AICommerce Dashboard</h1>
      <div className="flex items-center gap-4 text-sm text-gray-600">
        <span>Welcome, <span className="font-semibold">{userId}</span></span>
        <button
          onClick={handleLogout}
          className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>
    </header>
  );
};

export default Header;
