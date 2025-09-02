// Hiện form đăng ký / đăng nhập
const registerBox = document.getElementById("registerBox");
const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");

showRegister.addEventListener("click", (e) => {
    e.preventDefault();
    registerBox.style.display = "block";
});

showLogin.addEventListener("click", (e) => {
    e.preventDefault();
    registerBox.style.display = "none";
});

// Đăng ký (lưu vào localStorage)
document.getElementById("registerForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const user = document.getElementById("regUser").value;
    const pass = document.getElementById("regPass").value;

    if (localStorage.getItem(user)) {
        alert("Tài khoản đã tồn tại!");
    } else {
        localStorage.setItem(user, pass);
        alert("Đăng ký thành công!");
        registerBox.style.display = "none";
    }
});

// Đăng nhập (kiểm tra localStorage)
document.getElementById("loginForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const user = document.getElementById("loginUser").value;
    const pass = document.getElementById("loginPass").value;

    const savedPass = localStorage.getItem(user);
    if (savedPass && savedPass === pass) {
        alert("Đăng nhập thành công! Xin chào " + user);
        // Có thể redirect tới trang chính:
        // window.location.href = "home.html";
    } else {
        alert("Sai tài khoản hoặc mật khẩu!");
    }
});