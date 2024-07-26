/* eslint-disable react/react-in-jsx-scope */
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home/Home';
import About from './pages/About/About';
import Database from './pages/Database/Database';
import AdversarialSamples from './pages/AdversarialSamples/AdversarialSamples';
import DefenseModel from './pages/DefenseModel/DefenseModel';
import { AuthProvider } from './AuthContext';
import PrivateRoute from './PrivateRoute';

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<PrivateRoute />}>
            <Route index element={<About />} />
          </Route>
          <Route path="/database" element={<PrivateRoute />}>
            <Route index element={<Database />} />
          </Route>
          <Route path="/adversarial" element={<PrivateRoute />}>
            <Route index element={<AdversarialSamples />} />
          </Route>
          <Route path="/defense" element={<PrivateRoute />}>
            <Route index element={<DefenseModel />} />
          </Route>
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
