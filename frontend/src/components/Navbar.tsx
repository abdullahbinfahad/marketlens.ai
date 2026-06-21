import { useState } from "react"
interface NavbarProps {
  isDark: boolean
  toggleDark: () => void
}

export default function Navbar({ isDark, toggleDark }: NavbarProps) {
    const [menuOpen, setMenuOpen] = useState(false)
    return (
        <nav className="flex flex-wrap justify-between items-center px-4 py-3 md:px-6 md:py-5 bg-gray-900">
            <div className="flex items-center gap-2">
                <a href="/">
                    <span className="text-blue-400 text-sm md:text-2xl">👁</span>
                    <span className="text-white text-sm md:text-xl">
                        MarketLens <span className="text-blue-400">AI</span>
                    </span>
                </a>
            </div>

            <div className="flex items-center gap-2 md:hidden">
                <button onClick={toggleDark} className="text-white text-md px-3 py-2 rounded-full bg-gray-700">
                    {isDark ? '☀️' : '🌙'}
                </button>
                <button onClick={() => setMenuOpen(!menuOpen)} className="text-white text-md px-4 py-2 rounded-full bg-gray-700">
                    {menuOpen ? '✕' : '☰'}
                </button>
            </div>

            <div className="hidden md:flex items-center gap-3">
                <a href="/#about" className="text-white text-sm px-4 py-2 rounded-full bg-gray-700 hover:bg-gray-600">
                    About us
                </a>
                <a href="#contact" className="text-white text-sm px-4 py-2 rounded-full bg-gray-700 hover:bg-gray-600">
                    Contact us
                </a>
                <a href="/dashboard" className="text-white text-sm px-5 py-2 rounded-full bg-blue-600 hover:bg-blue-700">
                    Start a Project
                </a>
                <button onClick={toggleDark} className="text-white text-xl px-3 py-2 rounded-full bg-gray-700 hover:bg-gray-600">
                    {isDark ? '☀️' : '🌙'}
                </button>
            </div>

            {menuOpen && (
                <div className="w-full flex flex-col gap-2 mt-4 md:hidden">
                    <a href="/#about" className="text-white text-sm px-4 py-3 rounded-xl bg-gray-700">About us</a>
                    <a href="#contact" className="text-white text-sm px-4 py-3 rounded-xl bg-gray-700">Contact us</a>
                    <a href="/dashboard" className="text-white text-sm px-4 py-3 rounded-xl bg-blue-600">Start a Project</a>
                </div>
            )}

        </nav>
    )
}