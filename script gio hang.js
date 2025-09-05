document.addEventListener("DOMContentLoaded", () => {
    const addCartButtons = document.querySelectorAll(".add-cart");
    const buyNowButtons = document.querySelectorAll(".buy-now");

    addCartButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            alert("✅ Sản phẩm đã được thêm vào giỏ hàng!");
        });
    });

    buyNowButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            alert("🛒 Chuyển tới trang thanh toán...");
        });
    });
});