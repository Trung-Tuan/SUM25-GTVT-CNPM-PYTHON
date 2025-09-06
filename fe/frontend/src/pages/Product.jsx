import { useState, useEffect } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import "../styles/Product.css"

export default function Products() {
    const navigate = useNavigate()
    const [searchParams] = useSearchParams()

    // State cho dữ liệu
    const [products, setProducts] = useState([])
    const [categories, setCategories] = useState([])
    const [loading, setLoading] = useState(true)
    const [token] = useState(localStorage.getItem("token"))

    // State cho search và filter
    const [searchQuery, setSearchQuery] = useState(searchParams.get("q") || "")
    const [searchResults, setSearchResults] = useState([])
    const [isSearching, setIsSearching] = useState(false)

    // State cho filter
    const [selectedCategory, setSelectedCategory] = useState("")
    const [priceRange, setPriceRange] = useState({ min: "", max: "" })
    const [selectedAgeRange, setSelectedAgeRange] = useState("")

    // State cho pagination
    const [currentPage, setCurrentPage] = useState(1)
    const [productsPerPage] = useState(12)

    // State cho sorting
    const [sortBy, setSortBy] = useState("name")
    const [sortOrder, setSortOrder] = useState("asc")

    // Load dữ liệu khi component mount
    useEffect(() => {
        loadCategories()
        loadProducts()

        // Nếu có query từ URL thì tự động search
        if (searchParams.get("q")) {
            setSearchQuery(searchParams.get("q"))
        }
    }, [searchParams])

    // API CALL: Lấy danh sách danh mục
    const loadCategories = async () => {
        try {
            const res = await fetch("http://localhost:6868/api/products", {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            })
            const data = await res.json()

            if (res.ok) {
                setCategories(data.categories || [])
            } else {
                console.error("Lỗi khi tải danh mục:", data.message)
            }
        } catch (err) {
            console.error("Không kết nối được server:", err)
        }
    }

    // API CALL: Lấy tất cả sản phẩm với filter
    const loadProducts = async () => {
        setLoading(true)
        try {
            let url = "http://localhost:6868/api/products?"
            const params = new URLSearchParams()

            // Thêm filter parameters
            if (selectedCategory) params.append("category_id", selectedCategory)
            if (priceRange.min) params.append("min_price", priceRange.min)
            if (priceRange.max) params.append("max_price", priceRange.max)
            if (selectedAgeRange) params.append("age_range", selectedAgeRange)
            if (sortBy) params.append("sort_by", sortBy)
            if (sortOrder) params.append("sort_order", sortOrder)

            url += params.toString()

            const res = await fetch(url, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            })
            const data = await res.json()

            if (res.ok) {
                setProducts(data.products || [])
            } else {
                console.error("Lỗi khi tải sản phẩm:", data.message)
            }
        } catch (err) {
            console.error("Không kết nối được server:", err)
        } finally {
            setLoading(false)
        }
    }

    // API CALL: Thêm sản phẩm vào giỏ hàng
    const addToCart = async (productId) => {
        const token = localStorage.getItem("token")
        if (!token) {
            alert("Vui lòng đăng nhập để thêm vào giỏ hàng!")
            navigate("/login")
            return
        }

        try {
            const res = await fetch("http://localhost:6868/api/cart/add", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ product_id: productId, quantity: 1 }),
            })
            const data = await res.json()

            if (res.ok) {
                alert("Đã thêm vào giỏ hàng!")
            } else {
                alert(data.message || "Không thể thêm vào giỏ hàng!")
            }
        } catch (err) {
            alert("Không kết nối được server!")
            console.error(err)
        }
    }

    // API CALL: Tìm kiếm sản phẩm
    const searchProducts = async (query) => {
        if (!query.trim()) {
            setSearchResults([])
            setIsSearching(false)
            return
        }

        setIsSearching(true)
        try {
            const res = await fetch(`http://localhost:6868/api/products/search?q=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            })
            const data = await res.json()

            if (res.ok) {
                setSearchResults(data.products || [])
            } else {
                console.error("Lỗi khi tìm kiếm:", data.message)
                setSearchResults([])
            }
        } catch (err) {
            console.error("Không kết nối được server:", err)
            setSearchResults([])
        } finally {
            setIsSearching(false)
        }
    }

    // Handle events
    const handleSearchChange = (e) => {
        const query = e.target.value
        setSearchQuery(query)

        // Debounce search
        clearTimeout(window.searchTimeout)
        window.searchTimeout = setTimeout(() => {
            searchProducts(query)
        }, 500)
    }

    const handleSearchSubmit = (e) => {
        e.preventDefault()
        if (searchQuery.trim()) {
            navigate(`/products?q=${encodeURIComponent(searchQuery)}`)
            // Reset trang về 1 khi search
            setCurrentPage(1)
        }
    }

    const handleFilterChange = () => {
        setCurrentPage(1) // Reset về trang 1 khi filter
        loadProducts()
    }

    useEffect(() => {
        handleFilterChange()
    }, [selectedCategory, priceRange, selectedAgeRange, sortBy, sortOrder])

    const handleLogout = () => {
        localStorage.removeItem("token")
        alert("Đã đăng xuất!")
        navigate("/")
    }

    const clearFilters = () => {
        setSelectedCategory("")
        setPriceRange({ min: "", max: "" })
        setSelectedAgeRange("")
        setSortBy("name")
        setSortOrder("asc")
    }

    // Navigation functions
    const viewProductDetail = (productId) => {
        navigate(`/product/${productId}`)
    }

    const goToCart = () => {
        navigate("/cart")
    }

    const goToLogin = () => {
        navigate("/login")
    }

    // Pagination logic
    const indexOfLastProduct = currentPage * productsPerPage
    const indexOfFirstProduct = indexOfLastProduct - productsPerPage
    const currentProducts = products.slice(indexOfFirstProduct, indexOfLastProduct)
    const totalPages = Math.ceil(products.length / productsPerPage)

    const paginate = (pageNumber) => setCurrentPage(pageNumber)

    if (loading) {
        return (
            <div className="loading-container">
                <p>Đang tải sản phẩm...</p>
            </div>
        )
    }

    return (
        <div className="products-container">
            {/* Header - giống như Home */}
            <header className="header">
                <div className="header-content">
                    <h1 className="logo" onClick={() => navigate("/")}>Cửa Hàng Đồ Chơi</h1>

                    <form onSubmit={handleSearchSubmit} className="search-form">
                        <div className="search-container">
                            <input
                                type="text"
                                placeholder="Tìm kiếm đồ chơi..."
                                value={searchQuery}
                                onChange={handleSearchChange}
                                className="search-input"
                            />
                            <button type="submit" className="search-button">
                                🔍
                            </button>

                            {searchQuery && (
                                <div className="search-dropdown">
                                    {isSearching ? (
                                        <div className="search-loading">Đang tìm kiếm...</div>
                                    ) : searchResults.length > 0 ? (
                                        <>
                                            {searchResults.slice(0, 5).map((product) => (
                                                <div
                                                    key={product.id}
                                                    className="search-result-item"
                                                    onClick={() => viewProductDetail(product.id)}
                                                >
                                                    <img
                                                        src={product.image || "/placeholder.svg?height=40&width=40&query=toy"}
                                                        alt={product.name}
                                                        className="search-result-image"
                                                    />
                                                    <div className="search-result-info">
                                                        <span className="search-result-name">{product.name}</span>
                                                        <span className="search-result-price">{product.price?.toLocaleString("vi-VN")}đ</span>
                                                    </div>
                                                </div>
                                            ))}
                                            {searchResults.length > 5 && (
                                                <div className="search-view-all">
                                                    Xem tất cả {searchResults.length} kết quả
                                                </div>
                                            )}
                                        </>
                                    ) : (
                                        <div className="search-no-results">Không tìm thấy sản phẩm nào</div>
                                    )}
                                </div>
                            )}
                        </div>
                    </form>

                    <nav className="nav">
                        <button onClick={() => navigate("/")} className="btn">
                            Trang chủ
                        </button>
                        <button onClick={() => navigate("/products")} className="btn">
                            Sản phẩm
                        </button>
                        <button onClick={goToCart} className="btn">Giỏ hàng</button>
                        {token ? (
                            <button onClick={handleLogout} className="btn">
                                Đăng xuất
                            </button>
                        ) : (
                            <button onClick={goToLogin} className="btn">
                                Đăng nhập
                            </button>
                        )}
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <div className="main-content">
                {/* Sidebar Filter */}
                <aside className="filter-sidebar">
                    <div className="filter-section">
                        <div className="filter-header">
                            <h3>Lọc sản phẩm</h3>
                            <button onClick={clearFilters} className="clear-filters-btn">
                                Xóa bộ lọc
                            </button>
                        </div>

                        {/* Category Filter */}
                        <div className="filter-group">
                            <h4>Danh mục</h4>
                            <select
                                value={selectedCategory}
                                onChange={(e) => setSelectedCategory(e.target.value)}
                                className="filter-select"
                            >
                                <option value="">Tất cả danh mục</option>
                                {categories.map((category) => (
                                    <option key={category.id} value={category.id}>
                                        {category.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Price Range Filter */}
                        <div className="filter-group">
                            <h4>Khoảng giá</h4>
                            <div className="price-range">
                                <input
                                    type="number"
                                    placeholder="Từ"
                                    value={priceRange.min}
                                    onChange={(e) => setPriceRange({ ...priceRange, min: e.target.value })}
                                    className="price-input"
                                />
                                <span>-</span>
                                <input
                                    type="number"
                                    placeholder="Đến"
                                    value={priceRange.max}
                                    onChange={(e) => setPriceRange({ ...priceRange, max: e.target.value })}
                                    className="price-input"
                                />
                            </div>
                        </div>

                        {/* Age Range Filter */}
                        <div className="filter-group">
                            <h4>Độ tuổi</h4>
                            <select
                                value={selectedAgeRange}
                                onChange={(e) => setSelectedAgeRange(e.target.value)}
                                className="filter-select"
                            >
                                <option value="">Tất cả độ tuổi</option>
                                <option value="0-2">0-2 tuổi</option>
                                <option value="3-5">3-5 tuổi</option>
                                <option value="6-8">6-8 tuổi</option>
                                <option value="9-12">9-12 tuổi</option>
                                <option value="13+">13+ tuổi</option>
                            </select>
                        </div>
                    </div>
                </aside>

                {/* Products Section */}
                <main className="products-section">
                    {/* Sort and Results Info */}
                    <div className="products-header">
                        <div className="results-info">
                            <h2>Tất cả sản phẩm ({products.length})</h2>
                            {searchQuery && (
                                <p>Kết quả tìm kiếm cho: "<strong>{searchQuery}</strong>"</p>
                            )}
                        </div>

                        <div className="sort-section">
                            <label>Sắp xếp theo:</label>
                            <select
                                value={`${sortBy}-${sortOrder}`}
                                onChange={(e) => {
                                    const [field, order] = e.target.value.split('-')
                                    setSortBy(field)
                                    setSortOrder(order)
                                }}
                                className="sort-select"
                            >
                                <option value="name-asc">Tên A-Z</option>
                                <option value="name-desc">Tên Z-A</option>
                                <option value="price-asc">Giá thấp đến cao</option>
                                <option value="price-desc">Giá cao đến thấp</option>
                                <option value="created_at-desc">Mới nhất</option>
                            </select>
                        </div>
                    </div>

                    {/* Products Grid */}
                    {currentProducts.length > 0 ? (
                        <>
                            <div className="products-grid">
                                {currentProducts.map((product) => (
                                    <div key={product.id} className="product-card">
                                        <img
                                            src={product.image || "/placeholder.svg?height=200&width=200&query=toy"}
                                            alt={product.name}
                                            className="product-image"
                                            onClick={() => viewProductDetail(product.id)}
                                        />
                                        <div className="product-info">
                                            <h4 className="product-name" onClick={() => viewProductDetail(product.id)}>
                                                {product.name}
                                            </h4>
                                            <p className="product-price">{product.price?.toLocaleString("vi-VN")}đ</p>
                                            {product.age_range && (
                                                <p className="product-age">Độ tuổi: {product.age_range}</p>
                                            )}
                                            <button onClick={() => addToCart(product.id)} className="add-to-cart-button">
                                                Thêm vào giỏ
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Pagination */}
                            {totalPages > 1 && (
                                <div className="pagination">
                                    <button
                                        onClick={() => paginate(currentPage - 1)}
                                        disabled={currentPage === 1}
                                        className="pagination-btn"
                                    >
                                        « Trước
                                    </button>

                                    {[...Array(totalPages)].map((_, index) => (
                                        <button
                                            key={index + 1}
                                            onClick={() => paginate(index + 1)}
                                            className={`pagination-btn ${currentPage === index + 1 ? 'active' : ''}`}
                                        >
                                            {index + 1}
                                        </button>
                                    ))}

                                    <button
                                        onClick={() => paginate(currentPage + 1)}
                                        disabled={currentPage === totalPages}
                                        className="pagination-btn"
                                    >
                                        Sau »
                                    </button>
                                </div>
                            )}
                        </>
                    ) : (
                        <div className="no-products">
                            <p>Không tìm thấy sản phẩm nào</p>
                            <button onClick={clearFilters} className="btn">
                                Xóa bộ lọc
                            </button>
                        </div>
                    )}
                </main>
            </div>

            {/* Footer */}
            <footer className="footer">
                <p>© 2024 Cửa Hàng Đồ Chơi. Tất cả quyền được bảo lưu.</p>
            </footer>
        </div>
    )
}