import React, { useEffect, useRef, useState } from "react";
import { Editor } from "@tinymce/tinymce-react";
import FileDisplay from "../components/FileDisplay";
import NavigationBar from "../components/NavigationBar";
import { ResizableBox } from "react-resizable";
import { useLocation } from "react-router-dom";
import "react-resizable/css/styles.css";
import api from "../api";
import {
  MarksCreate,
  ResultCreate,
  CriterionRead,
} from "../components/Schemas";

const DocumentProcessing = () => {
  const apikey = import.meta.env.VITE_TINYMCE_API_KEY;
  const backendUrlApi = import.meta.env.VITE_BACKEND_API_URL;
  const location = useLocation();
  const assessmentId = location.pathname.split("/")[2];
  const submissionId = location.pathname.split("/")[3];
  const editorRef = useRef(null as any);
  const [doc, setDoc] = useState("");
  const [mark, setMark] = useState("");
  const [fileID, setFileID] = useState<any>(null);
  const [rubricID, setRubricID] = useState<any>(null);
  const [criterias, setCriterias] = useState<CriterionRead[]>([]);

  useEffect(() => {
    fetchFileID(false);
    fetchFileID(true);
  }, []);

  const fetchFileID = async (isRubric: boolean) => {
    try {
      if (isRubric) {
        const response = await fetch(
          `${backendUrlApi}/assessment/${assessmentId}`
        );
        const jsonAssessment = await response.json();
        setRubricID(jsonAssessment.rubric.id);
        setCriterias(jsonAssessment.criteria);
      } else {
        const response = await fetch(
          `${backendUrlApi}/submission/${submissionId}`
        );
        const jsonData = await response.json();
        setFileID(jsonData.attachments[0].id);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const fetchResults = async () => {
    try {
      const response = await api.get(
        `${backendUrlApi}/submission/${submissionId}/mark`
      );
      console.log(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handleSubmit = async () => {
    try {
      const marks: MarksCreate = {
        results: [],
        feedback: doc,
      };
      const response = await api.post(
        `${backendUrlApi}/submission/${submissionId}/mark`,
        marks
      );
      console.log(response);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const log = () => {
    if (editorRef.current) {
      console.log(editorRef.current.getContent());
      setDoc(editorRef.current.getContent());
    }
  };

  return (
    <div className="bg-gradient-to-r from-cyan-300 to-blue-200 min-h-screen">
      <NavigationBar />
      <div className="p-6 text-black flex flex-col h-full">
        <div className="flex h-500">
          <div className="flex-1 pl-2 w-full">
            <h2 className="text-lg font-semibold mb-2">Student Submission</h2>
            <FileDisplay
              fileUrl={`${backendUrlApi}/document/${fileID}/download`}
              side="left"
            />
          </div>
          <div className="flex-1 pr-2 w-full">
            <h2 className="text-lg font-semibold mb-2">Rubrics</h2>
            <FileDisplay
              fileUrl={`${backendUrlApi}/document/${rubricID}/download`}
              side="right"
            />
          </div>
        </div>
        <div className="mt-2">
          <h2 className="text-lg font-semibold mb-2">Feedback and Marking</h2>
          <Editor
            apiKey={apikey}
            onInit={(_, editor) => (editorRef.current = editor)}
            initialValue="<p>Leave your feedback here...</p>"
            init={{
              height: 150,
              menubar: false,
              plugins: [
                "advlist autolink lists link image charmap print preview anchor",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime media table paste code help wordcount",
              ],
              toolbar:
                "undo redo | formatselect | " +
                "bold italic backcolor | alignleft aligncenter " +
                "alignright alignjustify | bullist numlist outdent indent | " +
                "removeformat | help",
              content_style:
                "body { font-family:Helvetica,Arial,sans-serif; font-size:14px }",
            }}
          />
          {criterias.map((criteria) => (
            <div key={criteria.id}>
              <h2 className="text-lg font-semibold mb-2">{criteria.name}</h2>
              <p>
                {criteria.minMarks} - {criteria.maxMarks}
              </p>
              <input
                type="number"
                placeholder="Enter mark"
                className="border border-gray-300 rounded p-2 w-1/4"
                onChange={(e) => setMark(e.target.value)}
              />
            </div>
          ))}
          <div className="mt-2">
            <button
              onClick={log}
              className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Submit Feedback
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentProcessing;
