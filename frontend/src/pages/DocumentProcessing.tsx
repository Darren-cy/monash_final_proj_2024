import React, { useRef, useState } from "react";
import { Editor } from "@tinymce/tinymce-react";
import FileDisplay from "../components/FileDisplay";

const DocumentProcessing = () => {
  const [doc, setDoc] = useState("");
  const editorRef = useRef<any>(null);
  const apikey: string | undefined = import.meta.env.VITE_TINYMCE_API_KEY;
  const backendUrlApi: string | undefined = import.meta.env.VITE_BACKEND_API_URL
  const log = () => {
    if (editorRef.current) {
      console.log(editorRef.current.getContent());
      console.log(apikey);
      setDoc(editorRef.current.getContent());
    }
  };
  return (
    <>
      <div className="flex flex-wrap h-500">
      <FileDisplay fileUrl={`${backendUrlApi}/static/report.pdf`} side="left" />
      <FileDisplay fileUrl={`${backendUrlApi}/static/uploads/hello.pdf`} side="right" />
      </div>

      <div>
        <Editor
          apiKey={apikey}
          onInit={(_, editor) => (editorRef.current = editor)}
          initialValue="<p>This is the initial content of the editor.</p>"
          init={{
            height: 200,
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
        <button onClick={log}>Log editor content</button>
        {doc ? <pre>{doc}</pre> : null}
      </div>
    </>
  );
};

export default DocumentProcessing;
