import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Journal from "./pages/Journal";
import Others from "./pages/Others";
import Thesis from "./pages/Thesis";
import Book from "./pages/Book";
import Proceedings from "./pages/Proceedings";
import Publication from "./pages/Publication";
import Author from "./pages/Author";
import Institution from "./pages/Institution";
import Conference from "./pages/Conference";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/journal" element={<Journal />} />
            <Route path="/others" element={<Others />} />
            <Route path="/thesis" element={<Thesis />} />
            <Route path="/book" element={<Book />} />
            <Route path="/proceedings" element={<Proceedings />} />
            <Route path="/publication" element={<Publication />} />
            <Route path="/author" element={<Author />} />
            <Route path="/institution" element={<Institution />} />
            <Route path="/conference" element={<Conference />} />
            <Route path="/" element={<Navigate to="/journal" replace />} />
            <Route path="*" element={<Navigate to="/journal" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
