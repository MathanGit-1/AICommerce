import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Login from './pages/Login';
import Sidebar from './components/Sidebar';
import ProductRecommendations from './pages/ProductRecommendations';
import Header from './components/Header';
import ProtectedRoute from './ProtectedRoute';
import { useAuth } from './context/AuthContext';
import SentimentAnalysis from './pages/SentimentAnalysis';


// ✅ Inner App component so we can use useLocation() safely
function AppContent() {
  const { userId } = useAuth(); // ✅ use auth context
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';

  return (
    <div className="flex">
      {!isLoginPage && <Sidebar />}
      <div className="flex-1 flex flex-col min-h-screen">
        {!isLoginPage && <Header />}
        <div className="p-4 flex-1">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              path="/recommendations"
              element={
                <ProtectedRoute>
                  <ProductRecommendations />
                </ProtectedRoute>
              }
            />
            <Route
              path="/sentiment"
              element={
                <ProtectedRoute>
                  <SentimentAnalysis />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </div>
    </div>
  );
}

// ✅ Wrap AppContent in Router
function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
