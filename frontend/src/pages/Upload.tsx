import React, { useState } from "react";
import { FileUpload, FileUploadUploadEvent } from "primereact/fileupload";

const Upload = () => {
  const backendUrl = import.meta.env.VITE_API_URL;
  return (
    <div>
      <div className="card">
        <FileUpload
          name="file"
          url={`${backendUrl}/upload`}
          accept="image/*,application/pdf,text/*,video/*,audio/*"
          maxFileSize={1024 * 1024 * 10} // 10MB
          emptyTemplate={
            <p className="m-0">Drag and drop files to here to upload.</p>
          }
        />
      </div>
    </div>
  );
};

export default Upload;
