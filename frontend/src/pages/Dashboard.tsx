import React, { useState } from "react";
import { Link } from "react-router-dom";
import NavigationBar from "../components/NavigationBar";

const Dashboard = () => {
  const [assessments] = useState([
    { id: 1, fileName: "30221_euia", assessmentName: "Assessment 1", date: "2022-01-01", status: "Completed" },
    { id: 25, fileName: "23131_jknakds", assessmentName: "Assessment 2", date: "2022-02-01", status: "Pending" },
    { id: 3, fileName: "2134_sadgg", assessmentName: "Assessment 3", date: "2022-03-01", status: "In Review" },
  ]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });

  const sortedAssessments = React.useMemo(() => {
    const sortableItems = [...assessments];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [assessments, sortConfig]);

  const requestSort = key => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const SortIcon = ({ columnName }) => {
    if (sortConfig.key !== columnName) return null;
    return sortConfig.direction === 'ascending' ? '↑' : '↓';
  };

  return (
    <div className="bg-gradient-to-r from-cyan-300 to-blue-200 min-h-screen">
      <NavigationBar />
      <div className="p-6">
        <h1 className="text-xl font-semibold mb-4 text-black">Dashboard</h1>
        <div className="bg-white shadow-md rounded-lg p-4">
          <table className="min-w-full leading-normal border-collapse border border-gray-300">
            <thead>
              <tr>
                <th className="border-b border-gray-300 cursor-pointer p-2 text-left" onClick={() => requestSort('id')}>ID <SortIcon columnName="id" /></th>
                <th className="border-b border-gray-300 cursor-pointer p-2 text-left" onClick={() => requestSort('fileName')}>File Name <SortIcon columnName="fileName" /></th>
                <th className="border-b border-gray-300 cursor-pointer p-2 text-left" onClick={() => requestSort('assessmentName')}>Assessment Name <SortIcon columnName="assessmentName" /></th>
                <th className="border-b border-gray-300 cursor-pointer p-2 text-left" onClick={() => requestSort('date')}>Date <SortIcon columnName="date" /></th>
                <th className="border-b border-gray-300 cursor-pointer p-2 text-left" onClick={() => requestSort('status')}>Status <SortIcon columnName="status" /></th>
                <th className="border-b border-gray-300 p-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {sortedAssessments.map((assessment) => (
                <tr key={assessment.id} className="hover:bg-gray-100">
                  <td className="border-b border-gray-300 p-2">{assessment.id}</td>
                  <td className="border-b border-gray-300 p-2">{assessment.fileName}</td>
                  <td className="border-b border-gray-300 p-2">{assessment.assessmentName}</td>
                  <td className="border-b border-gray-300 p-2">{assessment.date}</td>
                  <td className="border-b border-gray-300 p-2">{assessment.status}</td>
                  <td className="border-b border-gray-300 p-2">
                    <Link to={`/document-processing`} className="text-blue-500 hover:text-blue-600">
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
