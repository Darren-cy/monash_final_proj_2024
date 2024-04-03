import React from "react";
import { Routes, Route, Navigation, BrowserRouter} from "react-router-dom"
import NotFound from "./components/NotFound";



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path ="*" element={<NotFound />}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
