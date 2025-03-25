using Newtonsoft.Json;

public class Product
{
    [JsonProperty("id")] // Comes from FastAPI as ObjectId string
    public string Id { get; set; }

    [JsonProperty("product_id")]
    public string ProductId { get; set; }

    [JsonProperty("name")]
    public string Name { get; set; }

    [JsonProperty("category")]
    public string Category { get; set; }

    [JsonProperty("brand")]
    public string Brand { get; set; }

    [JsonProperty("price")]
    public double Price { get; set; }

    [JsonProperty("image_url")]
    public string Image_url { get; set; }
}
