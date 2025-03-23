using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

public class UserInteraction
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; }  // Maps to MongoDB's _id

    [BsonElement("user_id")]
    public string UserId { get; set; }

    [BsonElement("product_id")]
    public string ProductId { get; set; }

    [BsonElement("event_type")]
    public string EventType { get; set; }

    [BsonElement("timestamp")]
    public string Timestamp { get; set; }
}