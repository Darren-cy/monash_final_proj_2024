import React from 'react'
import { Link } from 'react-router-dom'

const NavigationBar = () => {
  return (
    <nav>
      <Link to="/">Home </Link>

      <Link to="/dashboard">Dashboard </Link>

      <Link to="/document-processing">Document Processing </Link>

      <Link to="/login">Login </Link>

      <Link to="/register">Register </Link>

    </nav>
  )
}

export default NavigationBar