import React, { useState } from "react";
import { registerUser } from "../domain/usecases/registerUser";
import { AuthRepository } from "../data/AuthRepository";

const authRepo = new AuthRepository();

export default function RegisterForm({ onSwitch }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleRegister = async () => {
        try {
            const data = await registerUser(authRepo, {
                user_name: username,
                user_password: password,
                email: email,
            });

            if (data.success) {
                alert(data.message || "Đăng ký thành công!");
                onSwitch();
            } else {
                alert(data.message || "Đăng ký thất bại!");
            }
        } catch (err) {
            alert("Không kết nối được server!");
            console.error(err);
        }
    };

    return (
        <>
            <h2>Đăng ký</h2>
            <p>Tạo tài khoản mới để bắt đầu</p>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                style={styles.input}
            />
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
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
            <button onClick={handleRegister} style={styles.button}>
                Đăng ký
            </button>
            <a onClick={onSwitch} style={styles.link}>
                Đã có tài khoản? Đăng nhập
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
