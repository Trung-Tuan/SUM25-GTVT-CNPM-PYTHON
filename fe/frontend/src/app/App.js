import React, { useState } from "react";
import LoginForm from "./../presentation/LoginForm";
import RegisterForm from "./../presentation/RegisterForm";


function App() {
    const [isLogin, setIsLogin] = useState(true);

    return (
        <div>
            {isLogin ? (
                <LoginForm onSwitch={() => setIsLogin(false)} />
            ) : (
                <RegisterForm onSwitch={() => setIsLogin(true)} />
            )}
        </div>
    );
}

export default App;
