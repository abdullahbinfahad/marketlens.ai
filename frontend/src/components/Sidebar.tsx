import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

export default function Sidebar() {
    const navigate = useNavigate()
    const location = useLocation()
    const isActive = (path: string) => location.pathname === path
    const [isOpen, setIsOpen] = useState(false)

    const links = [
        { path: '/dashboard', icon: '📊', label: 'Dashboard' },
        { path: '/analyze', icon: '🔍', label: 'Product Analysis' },
        { path: '/trends', icon: '📈', label: 'Trends' },
        { path: '/history', icon: '🕐', label: 'History' },
    ]

    return (
        <>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="md:hidden fixed top-20 left-4 z-50 bg-blue-600 text-white p-2 rounded-xl shadow-lg"
            >
                {isOpen ? '✕' : '☰'}
            </button>

            <div className={`
                fixed md:static top-0 left-0 h-full z-40
                w-60 bg-white border-r border-gray-200 p-6 flex flex-col gap-2 min-h-screen
                dark:border-gray-700 dark:bg-[#0e1a2e]
                transition-transform duration-300
                ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
            `}>
                {links.map((link) => (
                    <button
                        key={link.path}
                        onClick={() => { navigate(link.path); setIsOpen(false) }}
                        className={`flex items-center gap-3 px-4 py-3 rounded-xl text-left ${
                            isActive(link.path)
                            ? 'bg-blue-50 text-blue-600 dark:bg-[#101e36]'
                            : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-[#12223b] dark:text-[#bcc2cc]'
                        }`}
                    >
                        {link.icon} {link.label}
                    </button>
                ))}
            </div>

            {isOpen && (
                <div
                    onClick={() => setIsOpen(false)}
                    className="md:hidden fixed inset-0 bg-black opacity-40 z-30"
                />
            )}
        </>
    )
}