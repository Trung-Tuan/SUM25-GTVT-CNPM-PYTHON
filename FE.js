function showRegister() {
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("registerForm").style.display = "block";
}

// Quay lại form đăng nhập
function showLogin() {
    document.getElementById("loginForm").style.display = "block";
    document.getElementById("registerForm").style.display = "none";
}

// ✅ Login demo
function login() {
    const username = document.getElementById("loginUser").value.trim();
    const password = document.getElementById("loginPass").value.trim();

    if (!username || !password) {
        alert("Vui lòng nhập đầy đủ thông tin!");
        return;
    }

    if (username === "admin" && password === "123") {
        alert("Đăng nhập thành công!");
        window.location.href = "home.html"; // demo chuyển sang trang chính
    } else {
        alert("Sai tài khoản hoặc mật khẩu!");
    }
}


function register() {
    const username = document.getElementById("regUser").value.trim();
    const email = document.getElementById("regEmail").value.trim();
    const password = document.getElementById("regPass").value.trim();
    const confirm = document.getElementById("regConfirm").value.trim();

    if (!username || !email || !password || !confirm) {
        alert("Vui lòng nhập đầy đủ thông tin!");
        return;
    }

    if (password !== confirm) {
        alert("Mật khẩu xác nhận không khớp!");
        return;
    }

    alert("Đăng ký thành công! Hãy đăng nhập.");
    showLogin(); // Sau khi đăng ký xong tự quay về login
}