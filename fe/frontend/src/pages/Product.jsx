import React, { useState, useEffect } from 'react';
import "../styles/Product.css";

const Product = () => {
    // State management
    const [products, setProducts] = useState([]);
    const [filteredProducts, setFilteredProducts] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('');
    const [priceFilter, setPriceFilter] = useState('');
    const [sortFilter, setSortFilter] = useState('newest');

    const productsPerPage = 8;

    // TODO: API CALL - Fetch all products when component mounts
    useEffect(() => {
        fetchProducts();
    }, []);

    // TODO: API CALL - Fetch products from backend
    const fetchProducts = async () => {
        try {
            setLoading(true);

            const response = await fetch("http://localhost:6868/api/products");
            const data = await response.json();

            if (response.status == 200) {
                setProducts(data.products);
                setFilteredProducts(data.products);
            } else {
                setProducts([]);
                setFilteredProducts([]);
            }
        } catch (error) {
            console.error("Error fetching products:", error);
        } finally {
            setLoading(false);
        }
    };

    // TODO: API CALL - Search products
    const handleSearch = async (event) => {
        event.preventDefault();

        if (searchTerm.trim()) {
            try {
                setLoading(true);
                // Replace with actual API call
                // const response = await fetch(`/api/products/search?q=${encodeURIComponent(searchTerm)}`);
                // const data = await response.json();

                // Client-side filtering for demonstration
                const filtered = products.filter(product =>
                    product.name.toLowerCase().includes(searchTerm.toLowerCase())
                );

                setFilteredProducts(filtered);
                setCurrentPage(1);
            } catch (error) {
                console.error('Error searching products:', error);
            } finally {
                setLoading(false);
            }
        } else {
            setFilteredProducts(products);
            setCurrentPage(1);
        }
    };

    // TODO: API CALL - Filter and sort products
    const filterProducts = async () => {
        try {
            setLoading(true);

            // For server-side filtering, send parameters to API
            // const params = new URLSearchParams({
            //   category: categoryFilter,
            //   priceRange: priceFilter,
            //   sort: sortFilter,
            //   page: 1,
            //   limit: productsPerPage
            // });
            // const response = await fetch(`/api/products?${params}`);
            // const data = await response.json();

            // Client-side filtering for demonstration
            let filtered = [...products];

            // Filter by category
            if (categoryFilter) {
                filtered = filtered.filter(product => product.category === categoryFilter);
            }

            // Filter by price
            if (priceFilter) {
                if (priceFilter === '1000000+') {
                    filtered = filtered.filter(product => product.price >= 1000000);
                } else {
                    const [min, max] = priceFilter.split('-').map(Number);
                    filtered = filtered.filter(product =>
                        product.price >= min && product.price <= max
                    );
                }
            }

            // Sort products
            switch (sortFilter) {
                case 'price-low':
                    filtered.sort((a, b) => a.price - b.price);
                    break;
                case 'price-high':
                    filtered.sort((a, b) => b.price - a.price);
                    break;
                case 'popular':
                    filtered.sort((a, b) => b.reviews - a.reviews);
                    break;
                case 'rating':
                    filtered.sort((a, b) => b.rating - a.rating);
                    break;
                default: // newest
                    filtered.sort((a, b) => b.id - a.id);
            }

            setFilteredProducts(filtered);
            setCurrentPage(1);
        } catch (error) {
            console.error('Error filtering products:', error);
        } finally {
            setLoading(false);
        }
    };

    // TODO: API CALL - Add product to cart
    const addToCart = async (event, productId) => {
        event.stopPropagation();

        try {
            // Replace with actual API call
            // const response = await fetch('/api/cart/add', {
            //   method: 'POST',
            //   headers: {
            //     'Content-Type': 'application/json',
            //     'Authorization': `Bearer ${userToken}` // if authentication required
            //   },
            //   body: JSON.stringify({
            //     productId: productId,
            //     quantity: 1
            //   })
            // });

            // if (!response.ok) {
            //   throw new Error('Failed to add to cart');
            // }

            const product = products.find(p => p.id === productId);
            alert(`Đã thêm "${product.name}" vào giỏ hàng!`);

            // TODO: Update cart count in header/global state
            // updateCartCount();

        } catch (error) {
            console.error('Error adding to cart:', error);
            alert('Có lỗi xảy ra khi thêm sản phẩm vào giỏ hàng');
        }
    };

    // Pagination logic
    const changePage = (page) => {
        const totalPages = Math.ceil(filteredProducts.length / productsPerPage);
        if (page >= 1 && page <= totalPages) {
            setCurrentPage(page);
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    };

    // Utility functions
    const getBadgeText = (badge) => {
        switch (badge) {
            case 'hot': return 'HOT';
            case 'new': return 'MỚI';
            case 'sale': return 'GIẢM GIÁ';
            default: return '';
        }
    };

    const getCategoryName = (category) => {
        const categories = {
            'educational': 'Giáo dục',
            'action': 'Hành động',
            'puzzle': 'Xếp hình',
            'electronic': 'Điện tử',
            'creative': 'Sáng tạo'
        };
        return categories[category] || category;
    };

    const formatPrice = (price) => {
        return price.toLocaleString('vi-VN') + 'đ';
    };

    // TODO: API CALL - Navigate to product detail
    const viewProduct = (productId) => {
        // Use React Router for navigation
        // navigate(`/product/${productId}`);

        // Or if using Next.js
        // router.push(`/product/${productId}`);

        console.log(`Navigate to product detail: ${productId}`);
    };

    const goHome = () => {
        // Use React Router for navigation
        // navigate('/');

        // Or if using Next.js
        // router.push('/');

        console.log('Navigate to home page');
    };

    // Calculate pagination
    const startIndex = (currentPage - 1) * productsPerPage;
    const endIndex = Math.min(startIndex + productsPerPage, filteredProducts.length);
    const currentProducts = filteredProducts.slice(startIndex, endIndex);
    const totalPages = Math.ceil(filteredProducts.length / productsPerPage);

    if (loading) {
        return (
            <div className="homepage-container">
                <div className="loading-container">
                    <div>Đang tải sản phẩm...</div>
                </div>
            </div>
        );
    }

    return (
        <div className="homepage-container">
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <h1 className="logo" onClick={goHome}>Cửa Hàng Đồ Chơi</h1>

                    <form className="search-form" onSubmit={handleSearch}>
                        <div className="search-container">
                            <input
                                type="text"
                                className="search-input"
                                placeholder="Tìm kiếm đồ chơi..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                            <button type="submit" className="search-button">🔍</button>
                        </div>
                    </form>

                    <nav className="nav">
                        <button className="btn" onClick={goHome}>Trang chủ</button>
                        <button className="btn">Sản phẩm</button>
                        <button className="btn">Giỏ hàng</button>
                        <button className="btn">Đăng nhập</button>
                    </nav>
                </div>
            </header>

            {/* Product Page Content */}
            <main className="product-page">
                <h1 className="page-title">
                    {searchTerm ? `Kết quả tìm kiếm: "${searchTerm}"` : 'Tất cả sản phẩm'}
                </h1>

                {/* Filter Controls */}
                <div className="product-controls">
                    <div className="filter-section">
                        <select
                            className="filter-select"
                            value={categoryFilter}
                            onChange={(e) => {
                                setCategoryFilter(e.target.value);
                                filterProducts();
                            }}
                        >
                            <option value="">Tất cả danh mục</option>
                            <option value="educational">Đồ chơi giáo dục</option>
                            <option value="action">Đồ chơi hành động</option>
                            <option value="puzzle">Đồ chơi xếp hình</option>
                            <option value="electronic">Đồ chơi điện tử</option>
                            <option value="creative">Đồ chơi sáng tạo</option>
                        </select>

                        <select
                            className="filter-select"
                            value={priceFilter}
                            onChange={(e) => {
                                setPriceFilter(e.target.value);
                                filterProducts();
                            }}
                        >
                            <option value="">Tất cả giá</option>
                            <option value="0-100000">Dưới 100.000đ</option>
                            <option value="100000-300000">100.000đ - 300.000đ</option>
                            <option value="300000-500000">300.000đ - 500.000đ</option>
                            <option value="500000-1000000">500.000đ - 1.000.000đ</option>
                            <option value="1000000+">Trên 1.000.000đ</option>
                        </select>

                        <select
                            className="filter-select"
                            value={sortFilter}
                            onChange={(e) => {
                                setSortFilter(e.target.value);
                                filterProducts();
                            }}
                        >
                            <option value="newest">Mới nhất</option>
                            <option value="price-low">Giá thấp đến cao</option>
                            <option value="price-high">Giá cao đến thấp</option>
                            <option value="popular">Phổ biến nhất</option>
                            <option value="rating">Đánh giá cao nhất</option>
                        </select>
                    </div>

                    <div className="results-info">
                        Hiển thị {startIndex + 1}-{endIndex} trong tổng số {filteredProducts.length} sản phẩm
                    </div>
                </div>
                -------------------------------------------------------------------------
                {/* Products Grid */}
                <div className="products-grid">
                    {currentProducts.map(product => (
                        <div
                            key={product.id}
                            className="product-card"
                            onClick={() => viewProduct(product.id)}
                        >
                            <div className="product-image">
                                {product.badge && (
                                    <span className={`product-badge ${product.badge}`}>
                                        {getBadgeText(product.badge)}
                                    </span>
                                )}
                                {/* TODO: Replace with actual product image */}
                                {/* <img src={`/images/products/${product.image}`} alt={product.name} /> */}
                                <span>Hình ảnh sản phẩm</span>
                            </div>
                            <div className="product-info">
                                <div className="product-category">{getCategoryName(product.category)}</div>
                                <h3 className="product-name">{product.name}</h3>
                                <div className="product-rating">
                                    <span className="stars">
                                        {'★'.repeat(Math.floor(product.rating))}
                                        {'☆'.repeat(5 - Math.floor(product.rating))}
                                    </span>
                                    <span className="rating-count">({product.reviews})</span>
                                </div>
                                <div className="product-price">
                                    <span className="current-price">{formatPrice(product.price)}</span>
                                    {product.originalPrice && (
                                        <>
                                            <span className="original-price">{formatPrice(product.originalPrice)}</span>
                                            <span className="discount">
                                                -{Math.round((1 - product.price / product.originalPrice) * 100)}%
                                            </span>
                                        </>
                                    )}
                                </div>
                                <button
                                    className="add-to-cart-button"
                                    onClick={(e) => addToCart(e, product.id)}
                                >
                                    Thêm vào giỏ hàng
                                </button>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Pagination */}
                {totalPages > 1 && (
                    <div className="pagination">
                        <button
                            className="pagination-btn"
                            onClick={() => changePage(currentPage - 1)}
                            disabled={currentPage === 1}
                        >
                            ← Trước
                        </button>

                        {/* Page numbers */}
                        {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => i + 1).map(page => (
                            <button
                                key={page}
                                className={`pagination-btn ${page === currentPage ? 'active' : ''}`}
                                onClick={() => changePage(page)}
                            >
                                {page}
                            </button>
                        ))}

                        {totalPages > 5 && (
                            <>
                                <span>...</span>
                                <button
                                    className="pagination-btn"
                                    onClick={() => changePage(totalPages)}
                                >
                                    {totalPages}
                                </button>
                            </>
                        )}

                        <button
                            className="pagination-btn"
                            onClick={() => changePage(currentPage + 1)}
                            disabled={currentPage === totalPages}
                        >
                            Sau →
                        </button>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="footer">
                <p>&copy; 2024 Cửa Hàng Đồ Chơi. Tất cả quyền được bảo lưu.</p>
            </footer>
        </div>
    );
};

export default Product;