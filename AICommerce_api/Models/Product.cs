using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;

namespace AICommerce.AICommerce_api.Models
{
    public class Product
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string? Id { get; set; }

        [BsonElement("product_id")]
        public string ProductId { get; set; }

        [BsonElement("name")]
        public string Name { get; set; }

        [BsonElement("category")]
        public string Category { get; set; }

        [BsonElement("brand")]
        public string Brand { get; set; }

        [BsonElement("price")]
        public double Price { get; set; }
    }
}