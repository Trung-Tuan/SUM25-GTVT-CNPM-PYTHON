import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginRegister() {
    const [isLogin, setIsLogin] = useState(true);
    const navigate = useNavigate();

    // state cho login
    const [loginUser, setLoginUser] = useState("");
    const [loginPass, setLoginPass] = useState("");

    // state cho register
    const [regUser, setRegUser] = useState("");
    const [regEmail, setRegEmail] = useState("");
    const [regPass, setRegPass] = useState("");
    const [regConfirm, setRegConfirm] = useState("");

    const showRegister = () => setIsLogin(false);
    const showLogin = () => setIsLogin(true);

    const login = async () => {
        if (!loginUser || !loginPass) {
            alert("Vui lòng nhập đầy đủ thông tin!");
            return;
        }

        try {
            const res = await fetch("http://localhost:6868/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_name: loginUser, user_password: loginPass }),
            });

            const data = await res.json();

            if (res.status == 200) {
                localStorage.setItem("token", data.token);
                alert("Đăng nhập thành công!");
                navigate("/"); // Chuyển hướng đến trang chủ (chưa xong)
            } else if (res.status == 401) {
                alert(data.message || "Sai tài khoản hoặc mật khẩu!");
            }
            else if (res.status == 500) {
                alert("Lỗi server, vui lòng thử lại sau!");
            }
        } catch (err) {
            alert("Không kết nối được server!");
            console.error(err);
        }

    };

    const register = async () => {
        if (!regUser || !regEmail || !regPass || !regConfirm) {
            alert("Vui lòng nhập đầy đủ thông tin!");
            return;
        }

        if (regPass !== regConfirm) {
            alert("Mật khẩu xác nhận không khớp!");
            return;
        }

        try {
            const res = await fetch("http://localhost:6868/api/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_name: regUser, email: regEmail, user_password: regPass }),
            });

            const data = await res.json();

            if (res.ok) {
                alert("Đăng ký thành công!");
                showLogin();
            } else {
                alert(data.message || "Đăng ký thất bại!");
            }
        } catch (err) {
            alert("Không kết nối được server!");
            console.error(err);
        }
    };

    return (
        <div
            style={{
                fontFamily: "Arial, sans-serif",
                backgroundColor: "#ffffff",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                height: "100vh",
                margin: 0,
            }}
        >
            <div
                style={{
                    display: "flex",
                    width: "400px",
                    backgroundColor: "#fff",
                    borderRadius: "10px",
                    overflow: "hidden",
                    boxShadow: "0 4px 20px rgba(0, 0, 0, 0.1)",
                    flexDirection: "column",
                }}
            >
                {isLogin ? (
                    <div style={{ flex: 1, padding: "40px" }}>
                        <h2 style={{ marginBottom: "10px", fontSize: "24px" }}>Đăng nhập</h2>
                        <p style={{ marginBottom: "30px", color: "#555" }}>Đồ chơi giáo dục đa dạng</p>
                        <input
                            type="text"
                            placeholder="Username"
                            value={loginUser}
                            onChange={(e) => setLoginUser(e.target.value)}
                            style={inputStyle}
                        />
                        <input
                            type="password"
                            placeholder="Mật khẩu"
                            value={loginPass}
                            onChange={(e) => setLoginPass(e.target.value)}
                            style={inputStyle}
                        />
                        <button onClick={login} style={buttonStyle}>
                            Đăng nhập
                        </button>
                        <a href="#" onClick={showRegister} style={linkStyle}>
                            Đăng ký
                        </a>
                    </div>
                ) : (
                    <div style={{ flex: 1, padding: "40px" }}>
                        <h2 style={{ marginBottom: "10px", fontSize: "24px" }}>Đăng ký</h2>
                        <p style={{ marginBottom: "30px", color: "#555" }}>Tạo tài khoản mới để bắt đầu</p>
                        <input
                            type="text"
                            placeholder="Username"
                            value={regUser}
                            onChange={(e) => setRegUser(e.target.value)}
                            style={inputStyle}
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={regEmail}
                            onChange={(e) => setRegEmail(e.target.value)}
                            style={inputStyle}
                        />
                        <input
                            type="password"
                            placeholder="Mật khẩu"
                            value={regPass}
                            onChange={(e) => setRegPass(e.target.value)}
                            style={inputStyle}
                        />
                        <input
                            type="password"
                            placeholder="Xác nhận mật khẩu"
                            value={regConfirm}
                            onChange={(e) => setRegConfirm(e.target.value)}
                            style={inputStyle}
                        />
                        <button onClick={register} style={buttonStyle}>
                            Đăng ký
                        </button>
                        <a href="#" onClick={showLogin} style={linkStyle}>
                            Đăng nhập
                        </a>
                    </div>
                )}
            </div>
        </div>
    );
}

const inputStyle = {
    width: "100%",
    padding: "12px",
    marginBottom: "15px",
    border: "1px solid #ccc",
    borderRadius: "25px",
    fontSize: "14px",
};

const buttonStyle = {
    width: "100%",
    padding: "12px",
    backgroundColor: "#1976d2",
    color: "#fff",
    border: "none",
    borderRadius: "25px",
    fontSize: "16px",
    cursor: "pointer",
};

const linkStyle = {
    display: "block",
    marginTop: "10px",
    textAlign: "right",
    fontSize: "14px",
    color: "#1976d2",
    textDecoration: "none",
};
