
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Sidebar from './components/Sidebar';
import ProductRecommendations from './pages/ProductRecommendations';
// import Products from './pages/Products';
// import SentimentAnalysis from './pages/SentimentAnalysis';
// import FraudDetection from './pages/FraudDetection';
// import DynamicPricing from './pages/DynamicPricing';
// import SalesForecasting from './pages/SalesForecasting';
// import Chatbot from './pages/Chatbot';
import Header from './components/Header';

function App() {
  const userId = localStorage.getItem('userId');
if (!userId && window.location.pathname !== '/login') {
  window.location.href = '/login';
}

  return (
    <Router>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 flex flex-col min-h-screen">
          <Header />
          <div className="p-4 flex-1">
          <Routes>
          <Route path="/login" element={<Login />} />
            {/* <Route path="/" element={<Products />} /> */}
            <Route
  path="/recommendations"
  element={
    localStorage.getItem('userId') ? <ProductRecommendations /> : <Navigate to="/login" replace />
  }
/>            {/* <Route path="/sentiment" element={<SentimentAnalysis />} />
            <Route path="/fraud" element={<FraudDetection />} />
            <Route path="/pricing" element={<DynamicPricing />} />
            <Route path="/forecast" element={<SalesForecasting />} />
            <Route path="/chatbot" element={<Chatbot />} />
            <Route path="/login" element={<Login />} /> */}
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}
export default App;
