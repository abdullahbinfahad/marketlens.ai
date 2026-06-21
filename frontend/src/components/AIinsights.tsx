export default function Insights() {
    const insights = [
            { text: '#New Category Add', time: 'last week' },
            { text: 'Smart Phone buy with back-part', time: '3d ago' },
            { text: 'Purchase report', time: '4d ago' },
            { text: 'New Product Add', time: '5d ago' },
            { text: 'Product tag Add', time: '5d ago' },
        ]

    return (
        <div className="bg-white rounded-2xl border border-gray-200 p-7 dark:border-gray-700 dark:bg-[#12223b]">
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-base text-gray-900 dark:text-[#f9f9f9]">AI Insights</h2>
            </div>
            <div className="flex flex-col gap-3">
                {insights.map((item, index) => (
                    <div key={index} className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <div className="w-2 h-2 bg-blue-400 rounded-full" />
                            <span className="text-sm text-gray-700 dark:text-[#bcc2cc]">{item.text}</span>
                        </div>
                        <span className="text-xs text-gray-400 dark:text-[#bcc2cc]">{item.time}</span>
                    </div>
                ))}
            </div>
        </div>
    )
}