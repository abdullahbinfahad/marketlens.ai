import Sidebar from '../components/Sidebar'
import {
  AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts'

const demandData = [
  { date: '05 Dec', value: 80 },
  { date: '10 Dec', value: 120 },
  { date: '15 Dec', value: 100 },
  { date: '20 Dec', value: 160 },
  { date: '25 Dec', value: 140 },
]

const sentimentData = [
  { platform: 'Linux',   value: 40 },
  { platform: 'Mac',     value: 80 },
  { platform: 'iOS',     value: 100 },
  { platform: 'Windows', value: 243 },
  { platform: 'Android', value: 60 },
  { platform: 'Other',   value: 30 },
]

const complaintsData = [
  { country: 'US',        value: 90 },
  { country: 'Canada',    value: 60 },
  { country: 'Mexico',    value: 75 },
  { country: 'China',     value: 50 },
  { country: 'Japan',     value: 40 },
  { country: 'Australia', value: 35 },
]

export default function Trends() {
    return (
        <div className="flex min-h-screen bg-gray-50 dark:bg-[#12223b]">
            <Sidebar />
            <div className="flex-1 flex flex-col">


                <div className="flex p-2 md:p-8 flex flex-col gap-6">
                    <div className="flex flex-col gap-4">
                        <div className="flex items-center border border-gray-200 rounded-xl bg-white px-4 py-3 gap-3 dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700">
                            <span className="text-gray-400 dark:text-[#bcc2cc]">🔍</span>
                            <input
                                type="text"
                                placeholder="Search Product Name"
                                className="flex-1 text-sm text-gray-700 outline-none dark:text-[#bcc2cc]"
                            />
                        </div>
                        <div className="block md:flex gap-4">
                            <div className="mb-4 md:mb-0 flex flex-col gap-1 flex-1">
                                <label className="text-xs text-gray-500 dark:text-[#f9f9f9]">Date</label>
                                <select className="border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-700 bg-white focus:outline-none dark:text-[#bcc2cc] dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700">
                                    <option>Last 30 Days</option>
                                    <option>Last 7 Days</option>
                                    <option>Last 90 Days</option>
                                </select>
                            </div>
                            <div className="mb-4 md:mb-0 flex flex-col gap-1 flex-1">
                                <label className="text-xs text-gray-500 dark:text-[#f9f9f9]">Target Country</label>
                                <select className="border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-700 bg-white focus:outline-none dark:text-[#bcc2cc] dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700">
                                    <option>United States</option>
                                    <option>China</option>
                                    <option>Germany</option>
                                    <option>Japan</option>
                                </select>
                            </div>
                            <div className="mb-4 md:mb-0 flex flex-col gap-1 flex-1">
                                <label className="text-xs text-gray-500 dark:text-[#f9f9f9]">Category</label>
                                <select className="border border-gray-200 rounded-xl px-4 py-2 text-sm text-gray-700 bg-white focus:outline-none dark:text-[#bcc2cc] dark:bg-[#12223b] dark:active:bg-[#101e36] dark:border-gray-700">
                                    <option>Electronics</option>
                                    <option>Fashion</option>
                                    <option>Sports</option>
                                </select>
                            </div>
                        </div>
                    </div>


                    <div className="bg-white rounded-2xl border border-gray-200 p-6 dark:bg-[#12223b] dark:border-gray-700">
                        <h3 className="text-base text-gray-900 mb-6 dark:text-[#f9f9f9]">Demand Forecast (30 Days)</h3>
                        <ResponsiveContainer width="100%" height={180}>
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
                                <Area type="monotone" dataKey="value" stroke="#3b82f6" fill="url(#colorValue)" strokeWidth={2} />
                            </AreaChart>
                        </ResponsiveContainer>
                        <p className="text-center text-sm text-gray-400 mt-2 dark:text-[#bcc2cc]">December Month</p>
                        <p className="text-center text-xs text-gray-400 dark:text-[#bcc2cc]">Avg Goal Completion 79%</p>
                    </div>


                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-white rounded-2xl border border-gray-200 p-6 dark:bg-[#12223b] dark:border-gray-700">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-base text-blue-500">Sentiment Trends</h3>
                                <button className="text-gray-400">···</button>
                            </div>
                            <ResponsiveContainer width="100%" height={180}>
                                <BarChart data={sentimentData}>
                                    <XAxis dataKey="platform" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                                    <YAxis hide />
                                    <Tooltip />
                                    <Bar dataKey="value" fill="#2196F3" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>


                        <div className="bg-white rounded-2xl border border-gray-200 p-6 dark:bg-[#12223b] dark:border-gray-700">
                            <div className="flex justify-between items-center mb-4">
                                <h3 className="text-base text-red-400">Top Complaints</h3>
                                <button className="text-gray-400">···</button>
                            </div>
                            <ResponsiveContainer width="100%" height={180}>
                                <BarChart data={complaintsData}>
                                    <XAxis dataKey="country" tick={{ fontSize: 11 }} axisLine={false} tickLine={false} />
                                    <YAxis hide />
                                    <Tooltip />
                                    <Bar dataKey="value" fill="#2196F3" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>


                    </div>
                </div>
            </div>
        </div>
    )
}