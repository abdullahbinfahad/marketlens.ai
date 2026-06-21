import Sidebar from '../components/Sidebar'
import { useNavigate } from 'react-router-dom'
import Insights from '../components/AIinsights'


export default function ProdAnalysis() {
    const navigate = useNavigate()
    return (
        <div className="flex min-h-screen bg-gray-50 dark:bg-[#12223b]">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <div className="flex-1 flex flex-col items-center px-8 py-12 gap-6">

                    <div className="w-full max-w-2xl flex items-center border border-gray-200 rounded-xl bg-white px-4 py-3 gap-3 dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700">
                        <span className="text-gray-400 dark:text-[#bcc2cc]">🔍</span>
                        <input
                            type="text"
                            placeholder="Search Product Name"
                            className="flex-1 text-sm text-gray-700 outline-none dark:text-[#bcc2cc]"
                        />
                    </div>
                    
                    <div className="w-full max-w-2xl flex flex-col gap-2">
                        <label className="text-sm text-gray-700 dark:text-[#f9f9f9]">Target Country</label>
                        <select className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-700 bg-white focus:outline-none focus:border-blue-500 dark:text-[#bcc2cc] dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700">
                            <option>United States</option>
                            <option>United Kingdom</option>
                            <option>Germany</option>
                            <option>Japan</option>
                            <option>Australia</option>
                            <option>China</option>
                        </select>
                    </div>

                    <div className="w-full max-w-2xl flex flex-col gap-2">
                        <label className="text-sm text-gray-700 dark:text-[#f9f9f9]">Category</label>
                        <select className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-700 bg-white focus:outline-none focus:border-blue-500 dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700 dark:text-[#bcc2cc]">
                            <option>Electronics</option>
                            <option>Fashion</option>
                            <option>Home & Garden</option>
                            <option>Sports</option>
                            <option>Beauty</option>
                        </select>
                    </div>

                    <button
                        onClick={() => navigate('/dashboard')}
                        className="w-full max-w-2xl text-white px-8 py-3 rounded-xl text-sm bg-blue-600 hover:bg-blue-700"
                    >
                        Run Analysis
                    </button>

                    <div className='pt-10 w-full flex flex-1 flex-col'>
                        <Insights />
                    </div>
                </div>
            </div>
        </div>
    )
}