import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import moment from "moment";
import NavigationBar from "../components/NavigationBar";
import PopUpPanel from "../components/PopUpPanel";
import { Data } from "../components/Schemas";

const Dashboard = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [assessments, setAssessments] = useState<Data[]>([]);

  const [sortConfig, setSortConfig] = useState({
    key: null,
    direction: "ascending",
  });
  const [assessment, setAssessment] = useState<Data | null>(null);

  const displayTable = (assessment: Data) => {
    return <PopUpPanel isOpen={isOpen} items={assessment.submissions} assessment_id={assessment.id} />;
  }

  const backendUrl = import.meta.env.VITE_BACKEND_API_URL;
  useEffect(() => {
    // Fetch assessment from the API
    const fetchData = async () => {
      try {
        const response = await fetch(`${backendUrl}/assessment`);
        const jsonData = await response.json();
        setAssessments(jsonData);
        console.log(jsonData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const sortedAssessments = React.useMemo(() => {
    const sortableItems = [...assessments];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        if (sortConfig.key !== null && a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (sortConfig.key !== null && a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [assessments, sortConfig]);

  const SortIcon = ({ columnName }: { columnName: string }) => {
    if (sortConfig.key !== columnName) return null;
    return sortConfig.direction === "ascending" ? "↑" : "↓";
  };

  function requestSort(arg0: string): void {
    throw new Error("Function not implemented.");
  }

  const handleClick = (assessment: Data) => {
    if (isOpen) {
      setIsOpen(false);
      setAssessment(null);
    }
    else {
      setIsOpen(true);
      setAssessment(assessment);
    }
  }

  return (
    <>
    <div className="bg-gradient-to-r from-cyan-300 to-blue-200 min-h-screen">
      <NavigationBar />
      <div className="p-6">
        <h1 className="text-xl font-semibold mb-4 text-black">Dashboard</h1>
        <div className="bg-white shadow-md rounded-lg p-4">
          <table className="min-w-full leading-normal border-collapse border border-gray-300 table-auto">
            <thead>
              <tr>
                <th
                  className="border-b border-gray-300 cursor-pointer p-2 text-left"
                  onClick={() => requestSort("assessment_id")}
                >
                  Assessment ID <SortIcon columnName="assessment_id" />
                </th>
                <th
                  className="border-b border-gray-300 cursor-pointer p-2 text-left"
                  onClick={() => requestSort("assessmentName")}
                >
                  Assessment Name <SortIcon columnName="assessmentName" />
                </th>
                <th
                  className="border-b border-gray-300 cursor-pointer p-2 text-left"
                  onClick={() => requestSort("fileName")}
                >
                  File Name <SortIcon columnName="fileName" />
                </th>
                <th
                  className="border-b border-gray-300 cursor-pointer p-2 text-left"
                  onClick={() => requestSort("date")}
                >
                  Created on <SortIcon columnName="date" />
                </th>
                <th
                  className="border-b border-gray-300 cursor-pointer p-2 text-left"
                  onClick={() => requestSort("no_submission")}
                >
                  No Submission <SortIcon columnName="no_submission" />
                </th>
                <th className="border-b border-gray-300 p-2 text-left">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {sortedAssessments.map((assessment) => (
                <tr key={assessment.id} className="hover:bg-gray-100">
                  
                  <td className="border-b border-gray-300 p-2">
                    {assessment.id}
                  </td>
                  <td className="border-b border-gray-300 p-2">
                    {assessment.name}
                  </td>
                  <td className="border-b border-gray-300 p-2">
                    {assessment.rubric.name}
                  </td>
                  <td className="border-b border-gray-300 p-2">
                    {moment(assessment.ctime).format("MMMM Do YYYY, h:mm:ss a")}
                  </td>
                  <td className="border-b border-gray-300 p-2">
                    {assessment.submissions.length}
                  </td>
                  <td className="border-b border-gray-300 p-2">
                    {/* <Link
                      to={`/document-processing/`}
                      className="text-blue-500 hover:text-blue-600"
                    >
                      View
                    </Link> */}


                    <button
                      onClick={() => handleClick(assessment)}
                      className="text-blue-500 hover:text-blue-600"
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
    {isOpen && assessment && displayTable(assessment)}
    </>
  );
};

export default Dashboard;
