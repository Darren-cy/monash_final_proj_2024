import { Submission } from "../components/Schemas";
import moment from "moment";
import { useNavigate } from "react-router-dom";
const PopUpPanel = ({
  isOpen,
  items,
  assessment_id,
}: {
  isOpen: boolean;
  items: Submission[];
  assessment_id: number;
}) => {
  const navigate = useNavigate();
  if (!isOpen) return null;
  return (
    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded shadow-lg p-4">
      <table className=" w-full table-auto">
        <thead className="">
          <tr className="bg-gray-100">
            <th className="border px-4 py-2">ID</th>
            <th className="border px-4 py-2">Submitted On</th>
            <th className="border px-4 py-2">Total Marks</th>
            <th className="border px-4 py-2">Attachments</th>
            <th className="border px-4 py-2">Authors</th>
            <th className="border px-4 py-2">Results</th>
            <th className="border px-4 py-2">Feedback</th>
            <th className="border px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, index) => (
            <tr
              key={item.id.toString()}
              className={index % 2 === 0 ? "bg-gray-100" : ""}
            >
              <td className="border px-4 py-2 ">{item.id}</td>
              <td className="border px-4 py-2 ">{moment(item.ctime).format("MMMM Do YYYY, h:mm:ss a")}</td>
              <td className="border px-4 py-2 ">{item.totalMarks}</td>
              <td className="border px-4 py-2  wrap text-wrap">
                {item.attachments.map((attachment) => attachment.name).join("")}
              </td>
              <td className="border px-4 py-2">
                {item.authors.map((author) => author.name).join("")}
              </td>
              <td className="border px-4 py-2">
                {item.results.map((result) => result.marks).join("")}
              </td>
              <td className="border  wrap text-ellipsis">{item.feedback}</td>
              <td className="border px-4 py-2">
                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                  onClick={() => navigate(`/document-processing/${assessment_id}/${item.id}`)}
                >
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PopUpPanel;
