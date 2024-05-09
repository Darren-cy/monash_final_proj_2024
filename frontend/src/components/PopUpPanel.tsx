import {Submission} from '../components/Schemas'
const PopUpPanel = ({isOpen, items}: {isOpen: boolean,items:Submission[]}) => {
    if (!isOpen) return null;
    return (
      <div
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white rounded shadow-lg p-4">
        <table className="table-fixed w-full">
          <thead>
            <tr className="bg-gray-100">
                <th className="border px-4 py-2">ID</th>
                <th className="border px-4 py-2">Created On</th>
                <th className="border px-4 py-2">Total Marks</th>
                <th className="border px-4 py-2">Attachments</th>
                <th className="border px-4 py-2">Authors</th>
                <th className="border px-4 py-2">Results</th>
                <th className="border px-4 py-2">Feedback</th>
                <th className='border px-4 py-2'>Actions</th> 
            </tr>
          </thead>
          <tbody>
            {items.map((item,index) => (
              <tr key={(item.id).toString()} className={index % 2 === 0 ? 'bg-gray-100' : ''}>
                <td className="border px-4 py-2">{item.id}</td>
                <td className="border px-4 py-2">{item.ctime}</td>
                <td className="border px-4 py-2">{item.totalMarks}</td>
                <td className="border px-4 py-2">{item.attachments.map((attachment) => attachment.name).join(', ')}</td>
                <td className="border px-4 py-2">{item.authors.map((author) => author.name).join(', ')}</td>
                <td className="border px-4 py-2">{item.results.map((result) => result.marks).join(', ')}</td>
                <td className="border px-4 py-2">{item.feedback}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
}

export default PopUpPanel