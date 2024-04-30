import { Link } from 'react-router-dom'

const NavigationBar = () => {
  return (
    <nav className="bg-white shadow-md py-4">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <div className="flex space-x-4">
          <Link to="/" className="text-blue-500 hover:text-blue-700 font-semibold">Home</Link>
          <Link to="/dashboard" className="text-blue-500 hover:text-blue-700 font-semibold">Dashboard</Link>
          <Link to="/document-processing" className="text-blue-500 hover:text-blue-700 font-semibold">Document Processing</Link>
        </div>
        <div className="flex space-x-4">
          <Link to="/login" className="text-blue-500 hover:text-blue-700 font-semibold">Login</Link>
        </div>
      </div>
    </nav>
  )
}

export default NavigationBar