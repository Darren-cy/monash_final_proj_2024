interface Attachment {
    id: number;
    name: string;
  }
  
  interface Submission {
    id: number;
    ctime: string;
    totalMarks: number;
    attachments: Attachment[];
    authors: Owner[];
    results: any[];
    feedback: any | null;
  }
  
  interface Owner {
    id: number;
    name: string;
  }
  
  interface Data {
    id: number;
    name: string;
    ctime: string;
    rubric: Attachment;
    owner: Owner;
    minMarks: number;
    maxMarks: number;
    submissions: Submission[];
  }
interface ResultCreate {
    value: number;
    criterion: number;
    comments: string | null;
}

  interface MarksCreate{
    results: ResultCreate[];
    feedback: string | null;
  }

  interface CriterionRead {
    id: number;
    name: string;
    minMarks: number;
    maxMarks: number;
  }

  export type { Attachment, Submission, Owner, Data, ResultCreate, MarksCreate, CriterionRead };