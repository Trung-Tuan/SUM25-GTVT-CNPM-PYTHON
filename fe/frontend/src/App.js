import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import LoginRegister from "./pages/LoginRegister";
import HomePage from "./pages/Home";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginRegister />} />
      </Routes>
    </Router>
  );
}

export default App;