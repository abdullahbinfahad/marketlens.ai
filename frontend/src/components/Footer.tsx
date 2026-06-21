export default function Footer() {
return (
    <footer className="bg-blue-500 text-white px-0 md:px-16 py-8 md:py-12 dark:bg-gray-900" id="contact">
 
      <div className="block justify-between ml-10 md:ml-0 gap-4 md:gap-10 mb-10 md:flex">

        <div className="flex flex-col mb-4 md:mb-0 gap-0 md:gap-2 w-3xs md:max-w-xs">
          <div className="flex items-center gap-2">
            <span className="text-white text-sm md:text-xl">👁</span>
            <span className="font-bold text-sm md:text-lg">MarketLens <span className="text-white">AI</span></span>
          </div>
          <p style={{color: "white"}} className="text-xs md:text-sm">
            AI-powered cross-border product intelligence for global sellers.
          </p>
        </div>

        <div className="flex flex-col mb-4 md:mb-0 gap-0 md:gap-3">
          <h3 style={{color: "white"}} className="font-semibold text-xs md:text-sm">Quick Links</h3>
          <a href="/" className="opacity-80 text-xs md:text-sm hover:opacity-100">Home</a>
          <a href="/analyze" className="opacity-80 text-xs md:text-sm hover:opacity-100">Product Analysis</a>
          <a href="/trends" className="opacity-80 text-xs md:text-sm hover:opacity-100">Trends</a>
          <a href="/about" className="opacity-80 text-xs md:text-sm hover:opacity-100">About Us</a>
        </div>

        <div className="flex flex-col gap-0 md:gap-3">
          <h3 style={{color: "white"}} className="font-semibold text-xs md:text-sm">Contact Us</h3>
          <p style={{color: "white"}} className="text-gray-100 text-xs md:text-sm">📧 contact@marketlens-ai.com</p>
          <p style={{color: "white"}} className="text-gray-100 text-xs md:text-sm">📍 Jiangsu, China</p>
        </div>

      </div>

      <div className="opacity-80 border-t border-white pt-6 text-center text-gray-100 text-xs">
        © 2025 MarketLens AI. All rights reserved.
      </div>

    </footer>
  )
}