import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import ProductAnalysis from './pages/ProductAnalysis'
import Dashboard from './pages/Dashboard'
import Trends from './pages/Trends'
import Footer from './components/Footer'
import { ThemeProvider } from './context/ThemeContext'
import { useState } from 'react'

function App() {
  const [isDark, setIsDark] = useState(false)

  const toggleDark = () => {
  setIsDark(!isDark)
  if (!isDark) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}
  
  return (
    <div className={isDark ? 'dark' : ''}>
      <ThemeProvider>
        <BrowserRouter>
          <Navbar isDark={isDark} toggleDark={toggleDark} />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyze" element={<ProductAnalysis />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/trends" element={<Trends />} />
          </Routes>
          <Footer />
        </BrowserRouter>
      </ThemeProvider>
    </div>
  )
}

export default App
