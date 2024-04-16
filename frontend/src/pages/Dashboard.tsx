import React from "react";
import { Link, redirect, useNavigate } from "react-router-dom";

const Dashboard = () => {
  const assessments = [
    { id: 1, name: "Assessment 1", date: "2022-01-01" },
    { id: 2, name: "Assessment 2", date: "2022-02-01" },
    { id: 3, name: "Assessment 3", date: "2022-03-01" },
  ];

  return (
    <div>
      <div>Dashboard</div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Date</th>
            <th>Actions</th> {/* Added column for actions */}
          </tr>
        </thead>
        <tbody>
          {assessments.map((assessment) => (
            <tr key={assessment.id}>
              <td>{assessment.id}</td>
              <td>{assessment.name}</td>
              <td>{assessment.date}</td>
              <td>
                <Link to={`/document-processing`}>View</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <Link to="/document-processing">Document Processing</Link>
      <br />
      <Link to="/assessments">Go to Assessments</Link>
    </div>
  );
};

export default Dashboard;
