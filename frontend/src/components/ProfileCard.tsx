import NoProfile from '../assets/NoProfile.png'

export default function ProfCard() {
    const member = [
        {id: 0, name: "Abdullah Bin Fahad", roles: "Group Leader"},
        {id: 1, name: "Brian Mavenrich", roles: "Frontend Developer"},
        {id: 2, name: "Revy Syawal Rizki", roles: "Backend Developer"},
        {id: 3, name: "Rokeya Zaman", roles: "Data Engineer"},
        {id: 4, name: "Shayne Lorraine", roles: "UI/UX Design"}];

    return (
        <>
        {member.map((member) => (
        <div key={member.id} className="flex flex-col my-6 lg:my-0 mx-auto items-center bg-white border border-gray-200 rounded-2xl p-6 py-10 w-60 gap-4 duration-300 ease-in-out hover:scale-105 dark:bg-[#12223b] dark:border-[#101e36]">
            <div className='mx-auto text-center text-[#373737] dark:text-[#f9f9f9]'>
                <img src={NoProfile} alt="Profile" className='mx-auto w-20 h-20 rounded-full object-cover bg-gray-100'/>
                <h2 className='mt-5 text-[#2196F3] dark:opacity-80'>{member.name}</h2>
                <p className='opacity-60'>{member.roles}</p>
            </div>
        </div>
      ))}
      </>
        
    )
}