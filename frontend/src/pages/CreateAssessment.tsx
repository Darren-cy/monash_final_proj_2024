import React, { useState } from "react";
import api from "../api";
import {Link, Navigate, useNavigate} from "react-router-dom";

interface AssessmentPost {
  name: string;
  rubric: number;
  criteria: [];
}

interface Criteria {
  name: string;
  min: number;
  max: number;
  assessment_id: number;
}

interface User {
    id: number;
    name: string;
  }

interface Document {
    id: number;
    name: string;
    type: string;
    ctime: string;
    size: number;
    owner: User;
    downloadURL: string;
}

const CreateAssessment = () => {
  const [assessment, setAssessment] = useState<AssessmentPost>({
    name: "",
    rubric: 0,
    criteria: [],
  });

  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setAssessment({ ...assessment, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    api
      .post("/api/v1.0/assessment", assessment)
      .then((response) => {
        alert("Assessment created successfully");
    })
    .catch((error) => {
        console.error(error);
    });
    navigate("/dashboard");
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const file = e.target.files[0];
      const formData = new FormData();
      formData.append("file", file);
        api.post("/api/v1.0/document", formData)
            .then((response) => {
            setAssessment({ ...assessment, rubric: response.data.id });
            alert("File uploaded successfully");
            })
            .catch((error) => {
            console.error(error);
            });
    }
}

return (
<div className="max-w-lg mx-auto border border-gray-300 p-6 rounded-md">
    <h1 className="text-2xl font-bold mb-4">Create Assessment</h1>
    <form onSubmit={handleSubmit} className="space-y-4">
        <div>
            <label className="block mb-1">
                <span className="text-gray-700">Name:</span>
                <input
                    type="text"
                    name="name"
                    value={assessment.name}
                    onChange={handleChange}
                    className="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                />
            </label>
        </div>
        <div>
            <label className="block mb-1">
                <span className="text-gray-700">Rubric File:</span>
                <input
                    type="file"
                    name="rubric_file"
                    onChange={handleFileChange}
                    className="block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
                    required
                />
            </label>
        </div>
        <button type="submit" className="w-full py-2 px-4 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:bg-indigo-700">
            Submit
        </button>
    </form>
</div>


);
};

export default CreateAssessment;
