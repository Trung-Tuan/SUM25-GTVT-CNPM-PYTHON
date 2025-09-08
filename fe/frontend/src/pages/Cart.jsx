import { useState, useEffect, useCallback } from "react"
import { useNavigate } from "react-router-dom"
import "../styles/Cart.css"

export default function Cart() {
    const navigate = useNavigate()
    const [cartItems, setCartItems] = useState([])
    const [loading, setLoading] = useState(true)
    const [token] = useState(localStorage.getItem("token"))

    // Load giỏ hàng khi component mount
    useEffect(() => {
        if (token) {
            loadCart()
        } else {
            setLoading(false)
        }
    }, [token, loadCart])

    // API CALL: Lấy giỏ hàng của user
    const loadCart = useCallback(async () => {
        try {
            const res = await fetch("http://localhost:6868/api/cart", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            })
            const data = await res.json()

            if (res.ok) {
                setCartItems(data.cart?.items || [])
            } else {
                console.error("Lỗi khi tải giỏ hàng:", data.error)
                setCartItems([])
            }
        } catch (err) {
            console.error("Không kết nối được server:", err)
            setCartItems([])
        } finally {
            setLoading(false)
        }
    }, [token])

    // API CALL: Cập nhật số lượng sản phẩm trong giỏ hàng
    const updateQuantity = async (productId, newQuantity, itemType = 'buy') => {
        if (newQuantity < 1) {
            removeFromCart(productId, itemType)
            return
        }

        try {
            const res = await fetch("http://localhost:6868/api/cart/update", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: newQuantity,
                    item_type: itemType
                }),
            })
            const data = await res.json()

            if (res.ok) {
                // Cập nhật lại giỏ hàng
                loadCart()
            } else {
                alert(data.error || "Không thể cập nhật số lượng!")
            }
        } catch (err) {
            alert("Không kết nối được server!")
            console.error(err)
        }
    }

    // API CALL: Xóa sản phẩm khỏi giỏ hàng
    const removeFromCart = async (productId, itemType = 'buy') => {
        try {
            const res = await fetch("http://localhost:6868/api/cart/remove", {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({
                    product_id: productId,
                    item_type: itemType
                }),
            })
            const data = await res.json()

            if (res.ok) {
                // Cập nhật lại giỏ hàng
                loadCart()
            } else {
                alert(data.error || "Không thể xóa sản phẩm!")
            }
        } catch (err) {
            alert("Không kết nối được server!")
            console.error(err)
        }
    }

    // Tính tổng giá trị giỏ hàng
    const calculateTotal = () => {
        return cartItems.reduce((total, item) => {
            return total + (item.total_price || 0)
        }, 0)
    }

    // Navigation functions
    const goToLogin = () => {
        navigate("/login")
    }

    const goToHome = () => {
        navigate("/")
    }

    const goToProducts = () => {
        navigate("/products")
    }

    const handleCheckout = () => {
        if (cartItems.length === 0) {
            alert("Giỏ hàng trống!")
            return
        }
        // TODO: Implement checkout logic
        alert("Tính năng thanh toán đang được phát triển!")
    }

    const handleLogout = () => {
        localStorage.removeItem("token")
        alert("Đã đăng xuất!")
        navigate("/")
    }

    if (!token) {
        return (
            <div className="cart-container">
                <header className="header">
                    <div className="header-content">
                        <h1 className="logo" onClick={goToHome}>Cửa Hàng Đồ Chơi</h1>
                        <nav className="nav">
                            <button onClick={goToHome} className="btn">Trang chủ</button>
                            <button onClick={goToProducts} className="btn">Sản phẩm</button>
                            <button onClick={goToLogin} className="btn">Đăng nhập</button>
                        </nav>
                    </div>
                </header>
                <div className="login-required">
                    <h2>Vui lòng đăng nhập để xem giỏ hàng</h2>
                    <button onClick={goToLogin} className="btn">Đăng nhập</button>
                </div>
            </div>
        )
    }

    if (loading) {
        return (
            <div className="cart-container">
                <header className="header">
                    <div className="header-content">
                        <h1 className="logo" onClick={goToHome}>Cửa Hàng Đồ Chơi</h1>
                        <nav className="nav">
                            <button onClick={goToHome} className="btn">Trang chủ</button>
                            <button onClick={goToProducts} className="btn">Sản phẩm</button>
                            <button onClick={handleLogout} className="btn">Đăng xuất</button>
                        </nav>
                    </div>
                </header>
                <div className="loading-container">
                    <p>Đang tải giỏ hàng...</p>
                </div>
            </div>
        )
    }

    return (
        <div className="cart-container">
            {/* Header - giống như Home */}
            <header className="header">
                <div className="header-content">
                    <h1 className="logo" onClick={goToHome}>Cửa Hàng Đồ Chơi</h1>
                    <nav className="nav">
                        <button onClick={goToHome} className="btn">Trang chủ</button>
                        <button onClick={goToProducts} className="btn">Sản phẩm</button>
                        <button onClick={() => navigate("/cart")} className="btn">Giỏ hàng</button>
                        <button onClick={handleLogout} className="btn">Đăng xuất</button>
                    </nav>
                </div>
            </header>

            {/* Main Content */}
            <div className="cart-content">
                <div className="cart-header">
                    <h2>Giỏ hàng của bạn</h2>
                    <p className="cart-count">{cartItems.length} sản phẩm</p>
                </div>

                {cartItems.length === 0 ? (
                    <div className="empty-cart">
                        <div className="empty-cart-icon">🛒</div>
                        <h3>Giỏ hàng trống</h3>
                        <p>Hãy thêm một số sản phẩm vào giỏ hàng của bạn!</p>
                        <button onClick={goToProducts} className="btn">Mua sắm ngay</button>
                    </div>
                ) : (
                    <>
                        {/* Cart Items */}
                        <div className="cart-items">
                            {cartItems.map((item) => (
                                <div key={`${item.product_id}-${item.item_type}`} className="cart-item">
                                    <div className="item-image">
                                        <img
                                            src={item.product?.image || "/placeholder.svg?height=100&width=100&query=toy"}
                                            alt={item.product?.name}
                                        />
                                    </div>
                                    <div className="item-details">
                                        <h4 className="item-name">{item.product?.name}</h4>
                                        <p className="item-price">{item.product?.price?.toLocaleString("vi-VN")}đ</p>
                                        {item.item_type === 'rent' && (
                                            <p className="item-rental">Thuê {item.rental_days} ngày</p>
                                        )}
                                    </div>
                                    <div className="item-controls">
                                        <div className="quantity-controls">
                                            <button
                                                onClick={() => updateQuantity(item.product_id, item.quantity - 1, item.item_type)}
                                                className="quantity-btn"
                                            >
                                                -
                                            </button>
                                            <span className="quantity">{item.quantity}</span>
                                            <button
                                                onClick={() => updateQuantity(item.product_id, item.quantity + 1, item.item_type)}
                                                className="quantity-btn"
                                            >
                                                +
                                            </button>
                                        </div>
                                        <div className="item-total">
                                            {item.total_price?.toLocaleString("vi-VN")}đ
                                        </div>
                                        <button
                                            onClick={() => removeFromCart(item.product_id, item.item_type)}
                                            className="remove-btn"
                                        >
                                            Xóa
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {/* Cart Summary */}
                        <div className="cart-summary">
                            <div className="summary-row">
                                <span>Tạm tính:</span>
                                <span>{calculateTotal().toLocaleString("vi-VN")}đ</span>
                            </div>
                            <div className="summary-row total">
                                <span>Tổng cộng:</span>
                                <span>{calculateTotal().toLocaleString("vi-VN")}đ</span>
                            </div>
                            <button onClick={handleCheckout} className="checkout-btn">
                                Thanh toán
                            </button>
                        </div>
                    </>
                )}
            </div>

            {/* Footer */}
            <footer className="footer">
                <p>© 2024 Cửa Hàng Đồ Chơi. Tất cả quyền được bảo lưu.</p>
            </footer>
        </div>
    )
}
