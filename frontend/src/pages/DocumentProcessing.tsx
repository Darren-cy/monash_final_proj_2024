import React, { useRef, useState } from "react";
import { Editor } from "@tinymce/tinymce-react";
import FileDisplay from "../components/FileDisplay";
import NavigationBar from "../components/NavigationBar";
import { ResizableBox } from "react-resizable";
import "react-resizable/css/styles.css";

const DocumentProcessing = () => {
  const [doc, setDoc] = useState("");
  const [mark, setMark] = useState("");
  const editorRef = useRef(null);
  const apikey = import.meta.env.VITE_TINYMCE_API_KEY;
  const backendUrlApi = import.meta.env.VITE_BACKEND_API_URL;

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
        <ResizableBox className="flex-grow" height={300} width={Infinity} axis="y" resizeHandles={['s']} >
          <div className="flex h-full">
            <ResizableBox className="w-1/2" width={200} height={Infinity} axis="x" resizeHandles={['e']}>
              <div className="flex flex-col h-full pr-2">
                <h2 className="text-lg font-semibold mb-2">Student Submission</h2>
                <FileDisplay fileUrl={`${backendUrlApi}/static/report.pdf`} />
              </div>
            </ResizableBox>
            <div className="flex-1 pl-2">
              <h2 className="text-lg font-semibold mb-2">Rubrics</h2>
              <FileDisplay fileUrl={`${backendUrlApi}/static/uploads/hello.pdf`} />
            </div>
          </div>
        </ResizableBox>
        <div className="mt-2">
          <h2 className="text-lg font-semibold mb-2">Feedback and Marking</h2>
          <Editor
            apiKey={apikey}
            onInit={(_, editor) => editorRef.current = editor}
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
          <div className="mt-2 flex justify-between items-center">
            
            <input
              type="text"
              placeholder="Enter mark"
              value={mark}
              onChange={e => setMark(e.target.value)}
              className="border p-1 rounded"
            />
            <button onClick={log} className="mt-8 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">Submit Feedback</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentProcessing;
