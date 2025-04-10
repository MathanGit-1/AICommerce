import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts';

const ProductSentimentBarChart = () => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5152/api/Sentiment/sentiment_by_product')
      .then((res) => res.json())
      .then((data) => {
        if (typeof data === 'string') data = JSON.parse(data);
        setChartData(data);
      })
      .catch((err) => {
        console.error('Failed to load product sentiment data:', err);
      });
  }, []);

  return (
    <div className="bg-white shadow-md rounded p-6">
      <h3 className="text-lg font-semibold mb-4">📊 Product-wise Sentiment</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="product_name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="positive" fill="#4ade80" name="Positive" />
          <Bar dataKey="negative" fill="#f87171" name="Negative" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default ProductSentimentBarChart;
