import React from 'react';

const Header = () => {
  const handleLogout = () => {
    localStorage.removeItem('userId');
    window.location.href = '/login'; // redirect to login
  };

  const userId = localStorage.getItem('userId');

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
