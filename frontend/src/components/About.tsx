import Empower from '../assets/empower.png'
import Adaptability from '../assets/adaptability.jpg'
import ProfCard from './ProfileCard'

export default function About() {
    return (
        <div className="items-center bg-white dark:bg-[#101e36]">


            <div className='flex w-full min-h-60 lg:min-h-150 bg-gray-100 dark:bg-[#12223b]'>
                <div className="w-xs lg:w-5xl my-auto mx-auto text-center">
                    <span className="text-blue-400 text-2xl lg:text-4xl">👁</span>
                    <span className="text-gray-800 text-2xl lg:text-4xl dark:text-[#f9f9f9]">
                        MarketLens <span className="text-gray-800 dark:text-[#f9f9f9]">AI</span>
                    </span>
                    <p className='text-[#7a7a7a] mt-5 text-xs dark:text-[#bcc2cc] lg:text-xl'>MarketLens AI is an AI analytics platform for cross-border sellers. We built it to fix common seller problems and pain points: messy data, manual review reading, lack of standardized product scoring, and expensive industry tools.</p>
                </div>
            </div>


            <div className="w-full max-w-2xs lg:max-w-2xl xl:max-w-5xl mx-auto my-6 mt-0 lg:mt-24 text-[#373737] dark:text-[#bcc2cc]">
                <div className='flex gap-10 my-6'>
                    <div className='my-auto'>
                        <h2 className='text-[#2196F3]'>Our Mission</h2>
                        <p className='text-justify'>Empower cross-border sellers with accessible, accurate AI market intelligence that turns scattered product data and customer reviews into clear, data-backed product selection decisions to cut inventory risk and lift global sales profitability.</p>
                    </div>
                    <img src={Empower} alt="Empower" className='hidden lg:block w-9/20 rounded-xl'/>
                </div>
                <div className='block lg:flex gap-10 my-6'>
                    <img src={Adaptability} alt="Grow" className='hidden lg:block w-9/20 rounded-xl'/>
                    <div className='my-auto'>
                        <h2 className='text-[#2196F3]'>Our Vision</h2>
                        <p className='text-justify'>Grow into an all-in-one self-improving AI decision engine for every cross-border merchant that constantly adapts to:</p>
                        <ul style={{listStyle: 'circle'}} className='mt-2 pl-5 text-1'>
                            <li>Global market shifts</li>
                            <li>Changing consumer sentiment</li>
                            <li>Evolving competitive landscapes</li>
                        </ul>
                    </div>
                    <img src={Adaptability} alt="Grow" className='my-10 rounded-xl block lg:hidden'/>
                </div>
            </div>


            <div className="w-full p-12 my-6 mt-36 bg-gray-100 dark:bg-[#12223b]">
                <div className='w-full max-w-6xl mx-auto'>
                    <h2 className='text-center text-[#2196F3]'>Meet Our Team</h2>
                    <div className='block lg:flex gap-5 my-6'>
                        <ProfCard />
                    </div>
                </div>
            </div>
        </div>
    )
}