import { useState, useEffect } from "react";
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
        setFileType(response.headers["content-type"])
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
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div
      style={{
        width: "50%",
        display: "inline-block",
        verticalAlign: "top",
      }}
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
            <iframe src={fileUrl} width="100%" height="500px" />
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
              uploadHandler={handleUpload}
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
