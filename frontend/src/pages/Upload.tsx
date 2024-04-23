import { FileUpload } from "primereact/fileupload";

const Upload = () => {
  const backendUrl = import.meta.env.VITE_API_URL;
  return (
    <>
      <div className="card">
        <FileUpload
          name="file"
          url={`${backendUrl}/api/v1.0/upload`}
          accept="image/*,application/pdf,text/*,video/*,audio/*"
          maxFileSize={1024 * 1024 * 10} // 10MB
          emptyTemplate={
            <p className="m-0">Drag and drop files to here to upload.</p>
          }
        />
      </div>
    </>
  );
};

export default Upload;
