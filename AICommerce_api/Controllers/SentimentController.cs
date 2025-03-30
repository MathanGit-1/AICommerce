using AICommerce.WebAPI.Data.Repository;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using System.Net.Http;

namespace AICommerce.WebAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SentimentController : Controller
    {
        private readonly IMongoCollection<UserInteraction> _userInteractionCollection;
        private readonly IProductRepository _productRepository;
        private readonly HttpClient _httpClient;

        public SentimentController(IMongoClient mongoClient, HttpClient httpClient)
        {
            var database = mongoClient.GetDatabase("AICommerceDB");
            _userInteractionCollection = database.GetCollection<UserInteraction>("user_interactions");
            _httpClient = httpClient;
        }

        [HttpPost]
        public async Task<IActionResult> PredictSentiment()
        {
            var response = await _httpClient.PostAsync("http://localhost:8000/analyze_sentiment", null);

            if (response.IsSuccessStatusCode)
            {
                string result = await response.Content.ReadAsStringAsync();
                return Ok(new { message = "Sentiment prediction completed", result });
            }

            return StatusCode(500, "Error while calling Python sentiment service.");

        }

        /// <summary>
        /// Get the sentiment
        /// </summary>
        /// <returns></returns>
        [HttpGet("sentiment_summary")]
        public async Task<IActionResult> GetSentimentSummary()
        {
            var response = await _httpClient.GetAsync("http://localhost:8000/sentiment_summary");

            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadAsStringAsync();
                return Ok(result); // Or deserialize to a proper DTO
            }

            return StatusCode(500, "Failed to get sentiment summary");
        }

        [HttpGet("sentiment_by_product")]
        public async Task<IActionResult> GetSentimentByProduct()
        {
            var response = await _httpClient.GetAsync("http://localhost:8000/sentiment_by_product");

            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content.ReadAsStringAsync();
                return Ok(result); // You can also deserialize into a DTO if needed
            }

            return StatusCode(500, "Failed to get product-wise sentiment summary");
        }
    }
}
