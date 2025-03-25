using System.Collections.Generic;
using System.Threading.Tasks;

namespace AICommerce.WebAPI.Data.Repository
{
    public interface IProductRepository
    {
        Task<IEnumerable<Product>> GetAllProductsAsync();
        Task<Product> GetProductByIdAsync(string id);
    }
}