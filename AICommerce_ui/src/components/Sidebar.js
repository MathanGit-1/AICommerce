import React from 'react';
import { Link } from 'react-router-dom';
import{
    FaBoxOpen,
    FaThList,
    FaComments,
    FaShieldAlt,
    FaDollarSign,
    FaChartLine,
    FaRobot
} from 'react-icons/fa';

const Sidebar = () => {
    return (
      <div className="w-64 min-h-screen bg-gray-800 text-white flex flex-col">
        <div className="p-6 text-2xl font-bold border-b border-gray-700">
          AICommerce
        </div>
        <nav className="flex-1 p-4 space-y-4">
          <Link to="/" className="flex items-center gap-3 hover:text-blue-400">
            <FaBoxOpen /> Products
          </Link>
          <Link to="/recommendations" className="flex items-center gap-3 hover:text-blue-400">
            <FaThList /> Recommendations
          </Link>
          <Link to="/sentiment" className="flex items-center gap-3 hover:text-blue-400">
            <FaComments /> Sentiment Analysis
          </Link>
          <Link to="/fraud" className="flex items-center gap-3 hover:text-blue-400">
            <FaShieldAlt /> Fraud Detection
          </Link>
          <Link to="/pricing" className="flex items-center gap-3 hover:text-blue-400">
            <FaDollarSign /> Dynamic Pricing
          </Link>
          <Link to="/forecast" className="flex items-center gap-3 hover:text-blue-400">
            <FaChartLine /> Sales Forecasting
          </Link>
          <Link to="/chatbot" className="flex items-center gap-3 hover:text-blue-400">
            <FaRobot /> AI Chatbot
          </Link>
        </nav>
      </div>
    );
  };
  
  export default Sidebar;