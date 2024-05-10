import { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";
import api from "../api";
import { FileUpload } from "primereact/fileupload";
interface Props {
  fileUrl: string;
  side: "left" | "right";
}

const FileDisplay = ({ fileUrl, side }: Props) => {
  const [fileType, setFileType] = useState<string>("");
  const backendUrl = import.meta.env.VITE_API_URL;


  useEffect(() => {
    const fetchFile = async () => {
      try {
        const response = await api.get(fileUrl);
        setFileType(response.headers["content-type"]);
      } catch (error) {
        console.error(error);
      }
    };
    fetchFile();
  }, [fileUrl]);

  return (
    <div
      className={`p-1 w-full h-full align-top outline-black outline-offset-2 outline-1  ${
        side === "left" ? "pr-1" : "pl-1"
      }`}
    >
      {(
        <div className="h-full">
          {fileType.includes("video") ? (
            <div className="w-full h-full overflow-auto resize" >
              <video controls src={fileUrl} className="w-full h-full"/>
            </div>
          ) : fileType.includes("image") ? (
            <img src={fileUrl} className="w-full h-full object-contain" alt="file" />
          ) : fileType.includes("audio") ? (
            <audio controls src={fileUrl} className="w-full h-full" />
          ) : fileType.includes("pdf") ? (
            <div className="w-full h-full overflow-scroll resize">
              <iframe src={fileUrl} className="w-full h-full" />
            </div>
          ) : (
            <div>
              <a href={fileUrl} target="_blank" rel="noopener noreferrer">
                <h1> None </h1>
              </a>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default FileDisplay;
