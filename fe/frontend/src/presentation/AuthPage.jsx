import React, { useState } from "react";
import LoginForm from "./LoginForm";
import RegisterForm from "./RegisterForm";

export default function AuthPage() {
    const [isLogin, setIsLogin] = useState(true);

    return (
        <div style={styles.loginContainer}>
            <div style={styles.loginLeft}>
                {isLogin ? (
                    <LoginForm onSwitch={() => setIsLogin(false)} />
                ) : (
                    <RegisterForm onSwitch={() => setIsLogin(true)} />
                )}
            </div>

            <div style={styles.loginRight}>
                <h3>Hoặc đăng nhập với</h3>
                <p>Kết nối nhanh bằng tài khoản mạng xã hội</p>
                <div style={styles.socialIcons}>
                    <a
                        href="http://localhost:3000/api/auth/facebook"
                        style={{ ...styles.social, backgroundColor: "#1877f2", color: "#fff" }}
                    >
                        <i className="fab fa-facebook-f"></i>
                    </a>
                    <a
                        href="http://localhost:3000/api/auth/google"
                        style={{
                            ...styles.social,
                            backgroundColor: "#fff",
                            border: "1px solid #ccc",
                        }}
                    >
                        <i
                            className="fab fa-google"
                            style={{
                                fontSize: "22px",
                                background: "conic-gradient(from -45deg,#ea4335 0deg 90deg,#34a853 90deg 180deg,#4285f4 180deg 270deg,#fbbc05 270deg 360deg)",
                                WebkitBackgroundClip: "text",
                                WebkitTextFillColor: "transparent",
                            }}
                        ></i>
                    </a>
                </div>
            </div>
        </div>
    );
}

const styles = {
    loginContainer: {
        display: "flex",
        width: "800px",
        backgroundColor: "#fff",
        borderRadius: "10px",
        overflow: "hidden",
        boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
        fontFamily: "Arial, sans-serif",
        height: "auto",
        margin: "50px auto",
    },
    loginLeft: {
        flex: 1,
        padding: "40px",
        borderRight: "1px solid #ddd",
    },
    loginRight: {
        flex: 1,
        backgroundColor: "#e6f2ff",
        padding: "40px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
    },
    socialIcons: {
        display: "flex",
        gap: "20px",
        margin: "20px 0",
    },
    social: {
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        width: "45px",
        height: "45px",
        borderRadius: "50%",
        fontSize: "22px",
        textDecoration: "none",
    },
};
