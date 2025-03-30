import React, { useEffect, useState } from 'react';

const SentimentSummaryCard = () => {
  const [summary, setSummary] = useState({
    totalReviews: 0,
    positivePercentage: 0,
    negativePercentage: 0,
  });

  useEffect(() => {
    fetch('http://localhost:5152/api/Sentiment/sentiment_summary')
      .then((res) => res.json())
      .then((data) => {
        if (typeof data === 'string') {
          data = JSON.parse(data); // handle stringified JSON from .NET
        }
        setSummary(data);
      })
      .catch((err) => {
        console.error('Failed to load sentiment summary:', err);
      });
  }, []);

  return (
    <div className="bg-white shadow-md rounded p-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div className="text-center">
        <p className="text-gray-500 text-sm">Total Reviews</p>
        <p className="text-2xl font-bold">{summary.totalReviews}</p>
      </div>
      <div className="text-center">
        <p className="text-green-500 text-sm">Positive (%)</p>
        <p className="text-2xl font-bold">{summary.positivePercentage}%</p>
      </div>
      <div className="text-center">
        <p className="text-red-500 text-sm">Negative (%)</p>
        <p className="text-2xl font-bold">{summary.negativePercentage}%</p>
      </div>
    </div>
  );
};

export default SentimentSummaryCard;
