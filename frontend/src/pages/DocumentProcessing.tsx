import React, { useRef, useState } from "react";
import { Editor } from "@tinymce/tinymce-react";

const DocumentProcessing = () => {
  const [doc, setDoc] = useState("");
  const editorRef = useRef<any>(null);
  const apikey: string | undefined  = import.meta.env.REACT_APP_TINYMCE_API_KEY;
  const log = () => {
    if (editorRef.current) {
      console.log(editorRef.current.getContent());
      setDoc(editorRef.current.getContent());
    }
  };
  return (
    <div>
      <div>
        <iframe
          src="https://mozilla.github.io/pdf.js/web/viewer.html"
          style={{
            width: "50%",
            height: "600px",
            border: "none",
            marginTop: "20px",
          }}
        ></iframe>
        <iframe
          src="https://mozilla.github.io/pdf.js/web/viewer.html"
          style={{
            width: "50%",
            height: "600px",
            border: "none",
            marginTop: "20px",
          }}
        ></iframe>
      </div>
      <div>
        <Editor
          apiKey={apikey}
          onInit={(evt, editor) => (editorRef.current = editor)}
          initialValue="<p>This is the initial content of the editor.</p>"
          init={{
            height: 500,
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
    </div>
  );
};

export default DocumentProcessing;
