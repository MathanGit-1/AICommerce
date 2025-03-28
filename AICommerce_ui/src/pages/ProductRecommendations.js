import React, { useState, useEffect } from 'react';

const ProductRecommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true); // ✅ loading state

  const handleFetch = async (id) => {
    try {
      setLoading(true); // ✅ start loading
      const res = await fetch(`http://localhost:5152/api/recommendation/${id}`);
      if (!res.ok) throw new Error('Something went wrong');
      const data = await res.json();
      setRecommendations(data);
      setError('');
    } catch (err) {
      setError('Failed to load recommendations.');
      console.error(err);
    } finally {
      setLoading(false); // ✅ stop loading
    }
  };

  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      handleFetch(storedUserId);
    }
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">📦 Product Recommendations</h2>

      {loading ? (
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
          <p className="ml-3 text-blue-600">Loading recommendations...</p>
        </div>
      ) : error ? (
        <p className="text-red-500 mb-4">{error}</p>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {recommendations.map((product) => (
            <div key={product.id} className="border rounded p-3 shadow">
              <img
                src={product.image_url || '/images/placeholder.png'}
                alt={product.name}
                className="w-full h-32 object-cover mb-2"
              />
              <h4 className="font-semibold">{product.name}</h4>
              <p className="text-gray-600">₹{product.price}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProductRecommendations;
