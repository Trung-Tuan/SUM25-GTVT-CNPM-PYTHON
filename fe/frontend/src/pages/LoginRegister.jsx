import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/LoginRegister.css";

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

            if (res.status === 200) {
                localStorage.setItem("token", data.token);
                alert("Đăng nhập thành công!");
                navigate("/");
            } else if (res.status === 401) {
                alert("Sai tài khoản hoặc mật khẩu!"); // data.message = message json từ BE
            } else if (res.status === 500) {
                alert("Sai tài khoản hoặc mật khẩu!");
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
            } else if (res.status === 400) {
                alert("Đăng ký thất bại!\nTài khoản đã tồn tại");
            }
            else {
                alert("Đăng ký thất bại!\nTài khoản và mật khẩu phải dài hơn 6 ký tự !")
            }
        } catch (err) {
            alert("Không kết nối được server!");
            console.error(err);
        }
    };

    return (
        <div className="login-register-container">
            <div className="form-box">
                {isLogin ? (
                    <div className="form-content">
                        <h2>Đăng nhập</h2>
                        <p>Đồ chơi giáo dục đa dạng</p>
                        <input
                            type="text"
                            placeholder="Tài khoản"
                            value={loginUser}
                            onChange={(e) => setLoginUser(e.target.value)}
                            className="input-field"
                        />
                        <input
                            type="password"
                            placeholder="Mật khẩu"
                            value={loginPass}
                            onChange={(e) => setLoginPass(e.target.value)}
                            className="input-field"
                        />
                        <button onClick={login} className="btn-submit">
                            Đăng nhập
                        </button>
                        <a href="#" onClick={showRegister} className="switch-link">
                            Đăng ký
                        </a>
                    </div>
                ) : (
                    <div className="form-content">
                        <h2>Đăng ký</h2>
                        <p>Tạo tài khoản mới để bắt đầu</p>
                        <input
                            type="text"
                            placeholder="Tài khoản"
                            value={regUser}
                            onChange={(e) => setRegUser(e.target.value)}
                            className="input-field"
                        />
                        <input
                            type="email"
                            placeholder="Email"
                            value={regEmail}
                            onChange={(e) => setRegEmail(e.target.value)}
                            className="input-field"
                        />
                        <input
                            type="password"
                            placeholder="Mật khẩu"
                            value={regPass}
                            onChange={(e) => setRegPass(e.target.value)}
                            className="input-field"
                        />
                        <input
                            type="password"
                            placeholder="Xác nhận mật khẩu"
                            value={regConfirm}
                            onChange={(e) => setRegConfirm(e.target.value)}
                            className="input-field"
                        />
                        <button onClick={register} className="btn-submit">
                            Đăng ký
                        </button>
                        <a href="#" onClick={showLogin} className="switch-link">
                            Đăng nhập
                        </a>
                    </div>
                )}
            </div>
        </div>
    );
}
