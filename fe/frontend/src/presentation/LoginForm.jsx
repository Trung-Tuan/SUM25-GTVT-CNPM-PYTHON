import React, { useState } from "react";
import { loginUser } from "../domain/usecases/loginUser";
import { AuthRepository } from "../data/AuthRepository";

const authRepo = new AuthRepository();

export default function LoginForm({ onSwitch }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async () => {
        try {
            const data = await loginUser(authRepo, {
                user_name: username,
                user_password: password,
            });

            if (data.success) {
                alert(data.message || "Đăng nhập thành công!");
            } else {
                alert(data.message || "Sai tài khoản hoặc mật khẩu!");
            }
        } catch (err) {
            alert("Không kết nối được server!");
            console.error(err);
        }
    };

    return (
        <>
            <h2>Đăng nhập</h2>
            <p>Đồ chơi giáo dục đa dạng</p>
            <input
                type="text"
                placeholder="Email hoặc Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={styles.input}
            />
            <input
                type="password"
                placeholder="Mật khẩu"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                style={styles.input}
            />
            <button onClick={handleLogin} style={styles.button}>
                Đăng nhập
            </button>
            <a onClick={onSwitch} style={styles.link}>
                Chưa có tài khoản? Đăng ký
            </a>
        </>
    );
}

const styles = {
    input: {
        width: "100%",
        padding: "12px",
        marginBottom: "15px",
        border: "1px solid #ccc",
        borderRadius: "25px",
        fontSize: "14px",
    },
    button: {
        width: "100%",
        padding: "12px",
        backgroundColor: "#1976d2",
        color: "#fff",
        border: "none",
        borderRadius: "25px",
        fontSize: "16px",
        cursor: "pointer",
    },
    link: {
        display: "block",
        marginTop: "10px",
        textAlign: "right",
        fontSize: "14px",
        color: "#1976d2",
        textDecoration: "none",
        cursor: "pointer",
    },
};
