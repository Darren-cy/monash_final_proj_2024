import React from 'react'
import { Link } from 'react-router-dom'

const Dashboard = () => {
  return (
    <div>
      <div>Dashboard</div>
      <Link to="/document-processing">Document Processing</Link>
    </div>
  )
}

export default Dashboard