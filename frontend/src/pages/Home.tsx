import { useNavigate } from 'react-router-dom'
import DashboardPreview from '../assets/dashboard.png'
import About from '../components/About'

export default function Home() {
  const navigate = useNavigate()
  return (
    <div className='bg-white dark:bg-[#101e36]'>
      <section className="bg-blue-500 min-h-xl lg:min-h-screen w-max-screen lg:px-16 py-20 dark:bg-[#0e1a2e]">
        
        <div className="flex flex-col lg:flex-row items-center gap-10">
          
          <div className="flex-1 text-center lg:text-left">
            <h1 className="text-3xl lg:text-6xl text-white leading-tight mb-6">
              GLOBAL BUSINESS INTELLIGENCE, REDEFINED
            </h1>
            <p className="text-[#f9f9f9] text-base lg:text-lg mb-10 opacity-90">
              AI-Powered Cross-Border Product Intelligence
            </p>
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-blue-700 text-white px-8 py-3 rounded-lg text-base hover:bg-blue-800"
            >
              Explore The Market!
            </button>
          </div>

          <div className="hidden xl:flex flex-1 justify-center">
            <div className="bg-white rounded-2xl shadow-2xl w-180 h-96 flex items-center justify-center rotate-6">
              <img src={DashboardPreview} alt="Dashboard Preview" />
            </div>
          </div>

        </div>
      </section>

      <section id='about' className='bg-gray-10 min-h-screen py-5 lg:py-20 dark:bg-[#101e36]'>
        <About />
      </section>
    </div>
  )
}