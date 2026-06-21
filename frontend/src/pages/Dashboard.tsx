import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import Sidebar from "../components/Sidebar"
import Insights from '../components/AIinsights'

export default function Dashboard() {

        const demandData = [
            { date: '05 Dec', value: 80 },
            { date: '10 Dec', value: 120 },
            { date: '15 Dec', value: 100 },
            { date: '20 Dec', value: 160 },
            { date: '25 Dec', value: 140 },
            { date: '30 Dec', value: 180 },
        ]

        const weightData = [
            { label: 'Demand', value: 80, color: 'bg-green-400' },
            { label: 'Profit', value: 60, color: 'bg-yellow-400' },
            { label: 'Risk',   value: 40, color: 'bg-orange-400' },
            { label: 'Gap',    value: 20, color: 'bg-red-400' },
        ]
        
        return (
            <div className="flex min-h-screen bg-gray-50 dark:bg-[#12223b]">
                <Sidebar />
                
                <div className="flex-1 flex flex-col">
                    <div className="flex justify-between items-center px-8 py-4 bg-white border-b border-gray-200 dark:border-gray-700 dark:bg-[#101e36]">
                        <div className="flex items-center gap-2">
                            <span className="text-blue-500">(Company Logo)</span>
                            <span className="text-gray-900 dark:text-[#bcc2cc]">(Company Name)</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <select className="border border-gray-200 rounded-lg px-3 py-2 text-sm text-gray-600 dark:border-gray-700 dark:text-[#bcc2cc]">
                                <option>Last 7 Days</option>
                                <option>Last 30 Days</option>
                                <option>Last 90 Days</option>
                            </select>
                        </div>
                    </div>

            
                    <div className="p-8 flex flex-col gap-6">
                        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
                            <div className="bg-white rounded-2xl border border-gray-200 p-6 flex flex-col gap-2 dark:border-gray-700 dark:bg-[#12223b]">
                                <div className="text-purple-500 text-2xl">👥</div>
                                <p className="text-sm text-gray-500 dark:text-[#bcc2cc]">Opportunity Score</p>
                                <p className="text-3xl text-gray-900 dark:text-[#f9f9f9]">(Score)</p>
                            </div>

                            <div className="bg-white rounded-2xl border border-gray-200 p-6 flex flex-col gap-2 dark:border-gray-700 dark:bg-[#12223b]">
                                <div className="text-orange-400 text-2xl">📈</div>
                                <p className="text-sm text-gray-500 dark:text-[#bcc2cc]">Demand Trend</p>
                                <p className="text-3xl text-gray-900 dark:text-[#f9f9f9]">↑/↓ (Demand Percentage)</p>
                            </div>

                            <div className="bg-white rounded-2xl border border-gray-200 p-6 flex flex-col gap-2 dark:border-gray-700 dark:bg-[#12223b]">
                                <div className="text-green-500 text-2xl">💰</div>
                                <p className="text-sm text-gray-500 dark:text-[#bcc2cc]">Risk Level</p>
                                <p className="text-3xl dark:text-[#f9f9f9]">(Low/Mid/High)</p>
                            </div>

                            <div className="bg-white rounded-2xl border border-gray-200 p-6 flex flex-col gap-2 dark:border-gray-700 dark:bg-[#12223b]">
                                <div className="text-red-400 text-2xl">🛍</div>
                                <p className="text-sm text-gray-500 dark:text-[#bcc2cc]">Competition Gap</p>
                                <p className="text-3xl text-gray-900 dark:text-[#f9f9f9]">(Gap Percentage)</p>
                            </div>
                        </div>


                        <div className="bg-white rounded-2xl border border-gray-200 p-6 dark:border-gray-700 dark:bg-[#12223b]">
                            <h3 className="text-base text-gray-900 mb-6 dark:text-[#f9f9f9]">Demand Forecast (Days Option)</h3>
                                <ResponsiveContainer width="100%" height={200}>
                                    <AreaChart data={demandData}>
                                        <defs>
                                            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                            </linearGradient>
                                        </defs>
                                        <XAxis dataKey="date" tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                                        <YAxis tick={{ fontSize: 12 }} axisLine={false} tickLine={false} />
                                        <Tooltip />
                                        <Area
                                            type="monotone"
                                            dataKey="value"
                                            stroke="#3b82f6"
                                            fill="url(#colorValue)"
                                            strokeWidth={2}
                                        />
                                    </AreaChart>
                                </ResponsiveContainer>
                            <p className="text-center text-sm text-gray-400 mt-2">(December) Month</p>
                            <p className="text-center text-xs text-gray-400">Avg Goal Completion (79%)</p>
                        </div>


                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                            <div className="bg-white rounded-2xl border border-gray-200 p-6 dark:border-gray-700 p-6 dark:bg-[#12223b]">
                                <h3 className="text-base text-gray-900 mb-4 dark:text-[#f9f9f9]">Weight Breakdown</h3>
                                <div className="flex flex-col gap-3">
                                    {weightData.map((item) => (
                                        <div key={item.label} className="flex items-center gap-4">
                                            <span className="text-sm text-gray-500 w-16 dark:text-[#bcc2cc]">{item.label}</span>
                                            <div className="flex-1 bg-gray-100 rounded-full h-2">
                                                <div className={`${item.color} h-2 rounded-full`} style={{ width: `${item.value}%` }}/>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className='flex flex-1 flex-col'>
                                <Insights />
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        )
}