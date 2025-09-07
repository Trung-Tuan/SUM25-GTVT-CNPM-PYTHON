import React from "react";

const styles = {
    container: {
        background: "#f5f5f5",
        color: "#333",
        lineHeight: 1.5,
        padding: "20px",
        fontFamily: "Arial, sans-serif",
    },
    title: {
        textAlign: "center",
        margin: "20px 0",
        fontSize: "26px",
        color: "#ff5722",
    },
    products: {
        display: "flex",
        flexDirection: "column",
        gap: "15px",
        width: "90%",
        maxWidth: "900px",
        margin: "auto",
    },
    card: {
        display: "flex",
        gap: "15px",
        background: "#fff",
        padding: "15px",
        borderRadius: "12px",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        transition: "transform 0.2s, box-shadow 0.2s",
    },
    img: {
        width: "150px",
        height: "150px",
        borderRadius: "10px",
        objectFit: "cover",
    },
    info: { flex: 1 },
    price: { fontSize: "16px", fontWeight: "bold", color: "#e53935" },
    discount: {
        fontSize: "14px",
        color: "#777",
        marginLeft: "6px",
        textDecoration: "line-through",
    },
    rating: { fontSize: "14px", color: "#666", margin: "6px 0 12px" },
    actions: { display: "flex", gap: "10px" },
    btn: {
        flex: 1,
        padding: "8px 12px",
        border: "none",
        borderRadius: "8px",
        fontSize: "14px",
        cursor: "pointer",
        transition: "0.2s",
    },
    addCart: { background: "#ff9800", color: "white" },
    buyNow: { background: "#e53935", color: "white" },
};

const products = [
    {
        name: "Giỏ Đựng Đồ Chơi",
        price: "35.000₫",
        discount: "-41%",
        rating: "⭐ 4.9 | 1200 đã bán",
        img: "https://via.placeholder.com/200",
    },
    {
        name: "Sọt Nhựa Đựng Đồ",
        price: "50.000₫",
        discount: "-28%",
        rating: "⭐ 4.8 | 980 đã bán",
        img: "https://via.placeholder.com/200",
    },
    {
        name: "Xe lắp ráp",
        price: "100.000₫",
        discount: "-10%",
        rating: "⭐ 5.0 | 1K1 đã bán",
        img: "https://via.placeholder.com/200",
    },
    {
        name: "Xe điều khiển từ xa",
        price: "450.000₫",
        discount: "-20%",
        rating: "⭐ 4.7 | 3.2k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Búp bê Barbie công chúa",
        price: "250.000₫",
        discount: "-30%",
        rating: "⭐ 4.8 | 1.5k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Gấu bông Teddy 1m2",
        price: "320.000₫",
        discount: "-25%",
        rating: "⭐ 4.9 | 4.8k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Máy bay điều khiển mini",
        price: "550.000₫",
        discount: "-18%",
        rating: "⭐ 4.6 | 2.1k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Xếp hình 3D lâu đài",
        price: "200.000₫",
        discount: "-22%",
        rating: "⭐ 4.7 | 980 đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Bộ đồ chơi nấu ăn mini",
        price: "180.000₫",
        discount: "-10%",
        rating: "⭐ 4.8 | 3.3k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Bộ đường ray tàu hỏa",
        price: "420.000₫",
        discount: "-17%",
        rating: "⭐ 4.9 | 1.8k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Xe tải chở cát đồ chơi",
        price: "150.000₫",
        discount: "-12%",
        rating: "⭐ 4.5 | 700 đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Robot biến hình Optimus",
        price: "600.000₫",
        discount: "-20%",
        rating: "⭐ 4.9 | 6.3k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Xe cứu hỏa đồ chơi",
        price: "220.000₫",
        discount: "-15%",
        rating: "⭐ 4.7 | 1.2k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Bộ đồ chơi bác sĩ mini",
        price: "190.000₫",
        discount: "-12%",
        rating: "⭐ 4.8 | 2.4k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Cầu trượt mini trong nhà",
        price: "1.200.000₫",
        discount: "-20%",
        rating: "⭐ 4.9 | 900 đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Bảng vẽ thông minh LCD",
        price: "120.000₫",
        discount: "-18%",
        rating: "⭐ 4.6 | 3.1k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Đàn piano đồ chơi",
        price: "300.000₫",
        discount: "-25%",
        rating: "⭐ 4.7 | 2.2k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Xe bus đồ chơi phát nhạc",
        price: "270.000₫",
        discount: "-15%",
        rating: "⭐ 4.8 | 1.1k đã bán",
        img: "https://via.placeholder.com/150",
    },
    {
        name: "Bộ xếp hình gỗ thông minh",
        price: "180.000₫",
        discount: "-10%",
        rating: "⭐ 4.9 | 2.8k đã bán",
        img: "https://via.placeholder.com/150",
    },
];

const ProductList = () => {
    const handleAddCart = (name) => {
        alert(`✅ ${name} đã được thêm vào giỏ hàng!`);
    };

    const handleBuyNow = (name) => {
        alert(`🛒 Mua ngay: ${name}`);
    };

    return (
        <section style={styles.container}>
            <h2 style={styles.title}>Sản phẩm nổi bật</h2>
            <div style={styles.products}>
                {products.map((p, i) => (
                    <div key={i} style={styles.card}>
                        <img src={p.img} alt={p.name} style={styles.img} />
                        <div style={styles.info}>
                            <h3>{p.name}</h3>
                            <p>
                                <span style={styles.price}>{p.price}</span>
                                <span style={styles.discount}>{p.discount}</span>
                            </p>
                            <p style={styles.rating}>{p.rating}</p>
                            <div style={styles.actions}>
                                <button
                                    style={{ ...styles.btn, ...styles.addCart }}
                                    onClick={() => handleAddCart(p.name)}
                                >
                                    Thêm vào giỏ
                                </button>
                                <button
                                    style={{ ...styles.btn, ...styles.buyNow }}
                                    onClick={() => handleBuyNow(p.name)}
                                >
                                    Mua ngay
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

export default ProductList;