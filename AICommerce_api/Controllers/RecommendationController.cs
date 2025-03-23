﻿using AICommerce.AICommerce_api.Models;
using AICommerce.WebAPI.Data.Repository;
using Microsoft.AspNetCore.Mvc;
using MongoDB.Driver;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Globalization;

namespace AICommerce.AICommerce_api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RecommendationController : ControllerBase
    {
        private readonly IMongoCollection<UserInteraction> _userInteractionCollection;
        private readonly IProductRepository _productRepository;
        private readonly HttpClient _httpClient;

        public RecommendationController(IProductRepository productRepository, IMongoClient mongoClient,HttpClient httpClient)
        {
            var database = mongoClient.GetDatabase("AICommerceDB");
            _productRepository = productRepository;
            _userInteractionCollection = database.GetCollection<UserInteraction>("user_interactions");
            _httpClient = httpClient;
        }

        [HttpGet("GetAllProducts")]
        public async Task<IActionResult> GetAllProducts()
        {
            var products = await _productRepository.GetAllProductsAsync();
            return Ok(products);
        }

        //[HttpGet("{id}")]
        //public async Task<IActionResult> GetProductById(string id)
        //{
        //    var product = await _productRepository.GetProductByIdAsync(id);
        //    if (product == null) return NotFound();
        //    return Ok(product);
        //}

        /// <summary>
        /// Get the recommended products based on the user id
        /// </summary>
        /// <param name="userId"></param>
        /// <returns></returns>
        [HttpGet("{userId}")]
        public async Task<IActionResult> GetRecommendedProducts(string userId)
        {
            var allViews = await _userInteractionCollection
                .Find(x => x.UserId == userId && x.EventType == "view")
                .ToListAsync();
            var lastView = allViews.OrderByDescending(x => DateTime.ParseExact(
                    x.Timestamp, "dd-MM-yyyy HH:mm", CultureInfo.InvariantCulture))
                .FirstOrDefault();

            if (lastView == null)
                return NotFound("No viewed product found");
            var productId = lastView.ProductId;

            var response = await _httpClient.GetAsync($"http://localhost:8001/recommend/{productId}");
            if (!response.IsSuccessStatusCode)
                return StatusCode((int)response.StatusCode, "AI Service error");

            var content = await response.Content.ReadAsStringAsync();
            var jsonObject = JsonConvert.DeserializeObject<JObject>(content);
            var recommendedProducts = jsonObject["recommended_products"].ToObject<List<Product>>();


            return Ok(recommendedProducts);
        }
    }
}