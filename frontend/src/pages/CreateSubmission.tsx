import { useState } from "react";
import api from "../api";

interface Submission {
  attachments: number[];
  authors: number[];
}
interface Author {
  id: number;
  name: string;
}

const CreateSubmission = () => {
  const [author, setAuthor] = useState<Author>({
    id: 0,
    name: "",
  });
  const [submission, setSubmission] = useState<Submission>({
    attachments: [],
    authors: [],
  });

  const [assessment_id, setAssessmentId] = useState<number>(0);
  const handleAuthorSubmit = () => {
    api
      .post("/api/v1.0/person", { name: author.name })
      .then((response) => {
        alert("Author created successfully");
        setAuthor(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  };
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const file = e.target.files[0];
      const formData = new FormData();
      formData.append("file", file);
      api
        .post("/api/v1.0/document", formData)
        .then((response) => {
          setSubmission({ ...submission, attachments: [response.data.id] });
          alert("File uploaded successfully");
        })
        .catch((error) => {
          console.error(error);
        });
    }
  };
  const handleAuthorChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAuthor({ ...author, name: e.target.value });
  };
  const handleSubmissionSubmit = () => {
    // assessment_id =
    const url = `/api/v1.0/assessment/${assessment_id}/submission`;
    api
      .post(url, submission)
      .then((response) => {
        alert("Submission created successfully");
      })
      .catch((error) => {
        console.error(error);
      });
  };

  const handleChangeAsessmentId = (e: React.ChangeEvent<HTMLInputElement>) => {
    setAssessmentId(parseInt(e.target.value));
  };
  return (
    <div className="flex justify-center">
      {/* Left Form */}
      <div className="w-1/2 max-w-md mx-4">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h2 className="text-xl mb-4">Create author</h2>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="author_name"
            >
              Author Name
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="author_name"
              type="text"
              placeholder="Author Name"
              onChange={handleAuthorChange}
              required
            />
          </div>
          <div className="flex items-center justify-between">
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              onClick={handleAuthorSubmit} // Attach event handler
            >
              Create Author
            </button>
          </div>
        </form>

        {/* Display author */}
        {author != null && (
          <div className="bg-white shadow-md rounded p-4 mt-4">
            <h2 className="text-xl mb-4">Author</h2>
            <p>
              <span className="font-bold">ID:</span> {author.id}
            </p>
            <p>
              <span className="font-bold">Name:</span> {author.name}
            </p>
          </div>
        )}
      </div>

      {/* Right Form */}
      <div className="w-1/2 max-w-md mx-4">
        <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h2 className="text-xl mb-4">Create submission</h2>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="assessment_id"
            >
              Assessment ID
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="asessment_id"
              type="number"
              placeholder="Assessment ID"
              value={assessment_id}
              onChange={handleChangeAsessmentId}
              required
            />
          </div>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="file"
            >
              File
            </label>
            <input
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              id="file"
              type="file"
              placeholder="File"
              onChange={handleFileChange}
              required
            />
          </div>
          <div className="flex items-center justify-between">
            <button
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="button"
              onClick={handleSubmissionSubmit} // Attach event handler
            >
              Submit
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateSubmission;
