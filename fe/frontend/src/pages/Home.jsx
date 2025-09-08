import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import "../styles/Home.css"

export default function Homepage() {
    const navigate = useNavigate()
    // const [products, setProducts] = useState([])
    // const [categories, setCategories] = useState([])
    const [featuredProducts, setFeaturedProducts] = useState([])
    const [loading, setLoading] = useState(true)
    const [searchQuery, setSearchQuery] = useState("")
    const [searchResults, setSearchResults] = useState([])
    const [isSearching, setIsSearching] = useState(false)
    const [token, setToken] = useState(localStorage.getItem("token"))
    // Load dữ liệu khi component mount
    useEffect(() => {
        // loadCategories()
        loadFeaturedProducts()
        // loadProducts()
    }, [])

    // API CALL: Lấy danh sách danh mục
    // const loadCategories = async () => {
    //     try {
    //         const res = await fetch("http://localhost:6868/api/categories", {
    //             method: "GET",
    //             headers: { "Content-Type": "application/json" },
    //         })
    //         const data = await res.json()

    //         if (res.ok) {
    //             setCategories(data.categories || [])
    //         } else {
    //             console.error("Lỗi khi tải danh mục:", data.message)
    //         }
    //     } catch (err) {
    //         console.error("Không kết nối được server:", err)
    //     }
    // }

    // API CALL: Lấy sản phẩm nổi bật
    const loadFeaturedProducts = async () => {
        try {
            const res = await fetch("http://localhost:6868/api/products/featured", {
                method: "GET",
                headers: { "Content-Type": "application/json" },
            })
            const data = await res.json()

            if (res.ok) {
                console.log("API featured products:", data.featured_products);
                setFeaturedProducts(data.featured_products || [])
            } else {
                console.error("Lỗi khi tải sản phẩm nổi bật:", data.message)
            }
        } catch (err) {
            console.error("Không kết nối được server:", err)
        } finally {
            setLoading(false)
        }
    }

    // API CALL: Lấy tất cả sản phẩm
    // const loadProducts = async () => {
    //     try {
    //         const res = await fetch("http://localhost:6868/api/products", {
    //             method: "GET",
    //             headers: { "Content-Type": "application/json" },
    //         })
    //         const data = await res.json()

    //         if (res.ok) {
    //             setProducts(data.products || [])
    //         } else {
    //             console.error("Lỗi khi tải sản phẩm:", data.message)
    //         }
    //     } catch (err) {
    //         console.error("Không kết nối được server:", err)
    //     } finally {
    //         setLoading(false)
    //     }
    // }

    // API CALL: Thêm sản phẩm vào giỏ hàng
    const addToCart = async (productId) => {
        const token = localStorage.getItem("token")
        if (!token) {
            alert("Vui lòng đăng nhập để thêm vào giỏ hàng!")
            // NAVIGATE: Chuyển đến trang đăng nhập
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

    const handleSearchChange = (e) => {
        const query = e.target.value
        setSearchQuery(query)

        // Debounce search - chờ 500ms sau khi user ngừng gõ
        clearTimeout(window.searchTimeout)
        window.searchTimeout = setTimeout(() => {
            searchProducts(query)
        }, 500)
    }

    const handleSearchSubmit = (e) => {
        e.preventDefault()
        if (searchQuery.trim()) {
            // NAVIGATE: Chuyển đến trang kết quả tìm kiếm
            navigate(`/search?q=${encodeURIComponent(searchQuery)}`)
        }
    }

    const handleLogout = () => {
        localStorage.removeItem("token")
        setToken(null)  // cập nhật lại state để UI re-render
        alert("Đã đăng xuất!")
        navigate("/")
    }


    // NAVIGATE: Chuyển đến trang chi tiết sản phẩm
    const viewProductDetail = (productId) => {
        navigate(`/product/${productId}`)
    }

    // NAVIGATE: Chuyển đến trang danh mục
    // const viewCategory = (categoryId) => {
    //     navigate(`/category/${categoryId}`)
    // }

    // NAVIGATE: Chuyển đến trang giỏ hàng
    const goToCart = () => {
        navigate("/cart")
    }

    // NAVIGATE: Chuyển đến trang đăng nhập
    const goToLogin = () => {
        navigate("/login")
    }

    if (loading) {
        return (
            <div className="loading-container">
                <p>Đang tải...</p>
            </div>
        )
    }

    return (
        <div className="homepage-container">
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <h1 className="logo">Cửa Hàng Đồ Chơi</h1>

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
                                                <div
                                                    className="search-view-all"
                                                    onClick={() => handleSearchSubmit({ preventDefault: () => { } })}
                                                >
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
                        <button onClick={() => document.getElementById("products-section")?.scrollIntoView({ behavior: "smooth" })} className="btn">
                            Xem sản phẩm
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

            {/* Hero Section */}
            <section className="hero">
                <h2 className="hero-title">Đồ chơi giáo dục đa dạng</h2>
                <p className="hero-subtitle">Khám phá thế giới đồ chơi thú vị cho bé yêu</p>
                <button onClick={() => document.getElementById("products-section")?.scrollIntoView({ behavior: "smooth" })}
                    className="hero-button"
                >
                    Xem sản phẩm
                </button>
            </section>

            {/* Categories Section
            <section className="section">
                <h3 className="section-title">Danh mục sản phẩm</h3>
                <div className="categories-grid">
                    {categories.map((category) => (
                        <div key={category.id} className="category-card" onClick={() => viewCategory(category.id)}>
                            <img
                                src={category.image || "/placeholder.svg?height=150&width=150&query=toy category"}
                                alt={category.name}
                                className="category-image"
                            />
                            <h4 className="category-name">{category.name}</h4>
                        </div>
                    ))}
                </div>
            </section> */}

            {/* danh sách sản phẩm nổi bật: */}
            <section className="section">
                <h3 className="section-title">Sản phẩm nổi bật</h3>
                <div className="products-grid">
                    {featuredProducts.map((product) => (
                        <div key={product.id} className="product-card">
                            <img
                                src={`/images/${product.image}`}
                                alt={product.name}
                                className="product-image"
                                onClick={() => viewProductDetail(product.id)}
                            />
                            <div className="product-info">
                                <h4 className="product-name" onClick={() => viewProductDetail(product.id)}>
                                    {product.name}
                                </h4>
                                <p className="product-price">{product.price?.toLocaleString("vi-VN")}đ</p>
                                <button onClick={() => addToCart(product.id)} className="add-to-cart-button">
                                    Thêm vào giỏ
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            </section>
            {/* View More Products Button */}
            <section id="products-section" className="section">
                <div className="view-more">
                    <button onClick={() => navigate("/products")} className="view-more-button">
                        Xem tất cả sản phẩm
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <p>© 2024 Cửa Hàng Đồ Chơi. Tất cả quyền được bảo lưu.</p>
            </footer>
        </div>
    )
}
