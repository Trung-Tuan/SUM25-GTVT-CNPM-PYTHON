import React, { useState } from "react";

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [loginUser, setLoginUser] = useState("");
  const [loginPass, setLoginPass] = useState("");
  const [regUser, setRegUser] = useState("");
  const [regEmail, setRegEmail] = useState("");
  const [regPass, setRegPass] = useState("");

  const showRegister = () => setIsLogin(false);
  const showLogin = () => setIsLogin(true);

  const login = async () => {
    try {
      const res = await fetch("http://localhost:6868/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_name: loginUser, user_password: loginPass })
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("token", data.token);
        alert("Đăng nhập thành công!");
        window.location.href = "home.html";
      } else {
        alert(data.message || "Sai tài khoản hoặc mật khẩu!");
      }
    } catch (err) {
      alert("Không kết nối được server!");
      console.error(err);
    }
  };

  const register = async () => {
    try {
      const res = await fetch("http://localhost:6868/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_name: regUser,
          user_password: regPass,
          // confirm_password: regPass,
          email: regEmail
        })
      });

      const data = await res.json();

      if (res.ok) {
        alert("Đăng ký thành công!");
        showLogin();
      } else {
        alert(data.message || data.error || "Đăng ký thất bại!");
      }
    } catch (err) {
      alert("Không kết nối được server!");
      console.error(err);
    }
  };

  return (
    <div className="login-container" style={styles.loginContainer}>
      {isLogin ? (
        <div className="login-left" style={styles.loginLeft}>
          <h2>Đăng nhập</h2>
          <p>Đồ chơi giáo dục đa dạng</p>
          <input
            type="text"
            placeholder="Email hoặc Username"
            value={loginUser}
            onChange={(e) => setLoginUser(e.target.value)}
            required
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Mật khẩu"
            value={loginPass}
            onChange={(e) => setLoginPass(e.target.value)}
            required
            style={styles.input}
          />
          <button onClick={login} style={styles.button}>
            Đăng nhập
          </button>
          <a href="#" onClick={showRegister} style={styles.link}>
            Chưa có tài khoản? Đăng ký
          </a>
        </div>
      ) : (
        <div className="login-left" style={styles.loginLeft}>
          <h2>Đăng ký</h2>
          <p>Tạo tài khoản mới để bắt đầu</p>
          <input
            type="text"
            placeholder="Username"
            value={regUser}
            onChange={(e) => setRegUser(e.target.value)}
            required
            style={styles.input}
          />
          <input
            type="email"
            placeholder="Email"
            value={regEmail}
            onChange={(e) => setRegEmail(e.target.value)}
            required
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Mật khẩu"
            value={regPass}
            onChange={(e) => setRegPass(e.target.value)}
            required
            style={styles.input}
          />
          <button onClick={register} style={styles.button}>
            Đăng ký
          </button>
          <a href="#" onClick={showLogin} style={styles.link}>
            Đã có tài khoản? Đăng nhập
          </a>
        </div>
      )}

      <div className="login-right" style={styles.loginRight}>
        <h3>Hoặc đăng nhập với</h3>
        <p>Kết nối nhanh bằng tài khoản mạng xã hội</p>
        <div className="social-icons" style={styles.socialIcons}>
          <a href="http://localhost:3000/api/auth/facebook" className="facebook" style={{ ...styles.social, backgroundColor: "#1877f2", color: "#fff" }}>
            <i className="fab fa-facebook-f"></i>
          </a>
          <a href="http://localhost:3000/api/auth/google" className="google" style={{ ...styles.social, backgroundColor: "#fff", border: "1px solid #ccc" }}>
            <i className="fab fa-google" style={{ fontSize: "22px", background: "conic-gradient(from -45deg,#ea4335 0deg 90deg,#34a853 90deg 180deg,#4285f4 180deg 270deg,#fbbc05 270deg 360deg)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" }}></i>
          </a>
        </div>
      </div>
    </div>
  );
}

// CSS in JS
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

export default App;
