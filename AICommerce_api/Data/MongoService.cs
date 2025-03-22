using MongoDB.Driver;
using Microsoft.Extensions.Configuration;
using AICommerce.AICommerce_api.Models;

public class MongoService
{
    private readonly IMongoDatabase _database;

    public MongoService(IConfiguration configuration)
    {
        var connectionString = configuration.GetValue<string>("MongoDB:ConnectionString");
        var client = new MongoClient(connectionString);
        _database = client.GetDatabase("AICommerceDB"); // Replace with your database name
    }

    public IMongoCollection<Product> GetProductsCollection()
    {
        return _database.GetCollection<Product>("Products"); // Replace with your collection name
    }
}