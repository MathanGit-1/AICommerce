import SentimentSummaryCard from '../components/SentimentSummaryCard';
import ProductSentimentBarChart from '../components/ProductSentimentBarChart';

const SentimentAnalysis = () => {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4">💬 Sentiment Analysis</h2>
      
      <SentimentSummaryCard />
      <div className="mt-8">
        <ProductSentimentBarChart />
      </div>
    </div>
  );
};

export default SentimentAnalysis;
