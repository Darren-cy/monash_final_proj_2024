import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import api from "../api";
import { FileUpload } from "primereact/fileupload";
interface Props {
  fileUrl: string;
  side: "left" | "right";
}

const FileDisplay = ({ fileUrl, side }: Props) => {
  const [file, setFile] = useState<any | null>(null);
  const [fileType, setFileType] = useState<string>("");
  const backendUrl = import.meta.env.VITE_API_URL;


  useEffect(() => {
    const fetchFile = async () => {
      try {
        const response = await api.get(fileUrl);
        setFile(response.data);
        setFileType(response.headers["content-type"]);
      } catch (error) {
        console.error(error);
      }
    };
    fetchFile();
  }, [fileUrl]);

  const handleUpload = (event: any) => {
    const uploadedFile = event.files[0];
    const formData = new FormData();
    formData.append("file", uploadedFile, uploadedFile.name);
    api
      .post(`${backendUrl}/api/v1.0/upload`, formData)
      .then((response) => {
        setFile(response.data);
        setFileType(response.headers["content-type"]);
        window.location.reload();
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div
      className={`p-1 w-1/2 h-500 inline-block align-top outline-black outline-offset-2 outline-1  ${
        side === "left" ? "pr-1" : "pl-1"
      }`}
    >
      {file ? (
        <div>
          {fileType.includes("video") ? (
            <video controls src={fileUrl} />
          ) : fileType.includes("image") ? (
            <img src={fileUrl} />
          ) : fileType.includes("audio") ? (
            <audio controls src={fileUrl} />
          ) : fileType.includes("pdf") ? (
            <div className="w-full overflow-auto resize">
              <iframe src={fileUrl} height="100%" width="100%" />
            </div>
          ) : (
            <div>
              <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                <h1> None </h1>
              </a>
            </div>
          )}
        </div>
      ) : (
        <div>
          <div className="card">
            <FileUpload
              name="file"
              url={`${backendUrl}/api/v1.0/upload`}
              onUpload={handleUpload}
              accept="image/*,application/pdf,text/*,video/*,audio/*"
              maxFileSize={1024 * 1024 * 10} // 10MB
              emptyTemplate={
                <p className="m-0">Drag and drop files to here to upload.</p>
              }
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default FileDisplay;
