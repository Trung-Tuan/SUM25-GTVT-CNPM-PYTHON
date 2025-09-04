import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import LoginRegister from "./pages/LoginRegister";
import HomePage from "./pages/Home";
import Product from "./pages/Product";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginRegister />} />
        <Route path="/products" element={<Product />} />
      </Routes>
    </Router>
  );
}

export default App;