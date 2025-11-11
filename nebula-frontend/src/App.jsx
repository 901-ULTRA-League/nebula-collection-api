import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./pages/Home";
import CardDetail from "./pages/CardDetail";
import Stats from "./pages/Stats";

export default function App() {
  return (
    <Router>
      <div className="min-h-screen">
        {/* NAVBAR */}
        <nav className="bg-[--color-panel] border-b border-gray-800 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <h1 className="text-3xl font-bold text-transparent bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text">
              Nebula Collection
            </h1>
            <div className="space-x-6 text-gray-300 text-lg">
              <Link className="hover:text-blue-400 transition" to="/">Home</Link>
              <Link className="hover:text-blue-400 transition" to="/stats">Stats</Link>
            </div>
          </div>
        </nav>

        {/* MAIN */}
        <main className="max-w-7xl mx-auto p-6">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/card/:number" element={<CardDetail />} />
            <Route path="/stats" element={<Stats />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
