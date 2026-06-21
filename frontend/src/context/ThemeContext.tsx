import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext({
  isDark: false,
  toggleDark: () => {}
})

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [isDark, setIsDark] = useState(false)

  const toggleDark = () => {
    setIsDark(!isDark)
    document.documentElement.classList.toggle('dark')
  }

  return (
    <ThemeContext.Provider value={{ isDark, toggleDark }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => useContext(ThemeContext)