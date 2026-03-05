import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Book: React.FC = () => {
  return (
    <div id="page-book-3">
    <div id="iogz0f" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="iy89zo" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="i7w927" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i70o26" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="iilce8" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/journal">{"Journal"}</a>
          <a id="i9dwsn" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/others">{"Others"}</a>
          <a id="itygfj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/thesis">{"Thesis"}</a>
          <a id="idkyci" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/book">{"Book"}</a>
          <a id="i5om46" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/proceedings">{"Proceedings"}</a>
          <a id="i0jc6e" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/publication">{"Publication"}</a>
          <a id="ite3ri" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
          <a id="ifd0sk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/institution">{"Institution"}</a>
          <a id="i7tg9y" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/conference">{"Conference"}</a>
        </div>
        <p id="ig2n4n" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ifw7lo" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iatwfl" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Book"}</h1>
        <p id="ix07uk" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Book data"}</p>
        <TableBlock id="table-book-3" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Book List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Address", "column_type": "field", "field": "address", "type": "str", "required": true}, {"label": "Publisher", "column_type": "field", "field": "publisher", "type": "str", "required": true}, {"label": "Year", "column_type": "field", "field": "year", "type": "int", "required": true}, {"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Author 1", "column_type": "lookup", "path": "author_1", "entity": "Author", "field": "last_name", "type": "list", "required": true}, {"label": "Institution 1", "column_type": "lookup", "path": "institution_1", "entity": "Institution", "field": "country", "type": "list", "required": true}], "formColumns": [{"column_type": "field", "field": "address", "label": "address", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "publisher", "label": "publisher", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "year", "label": "year", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "author_1", "field": "author_1", "lookup_field": "last_name", "entity": "Author", "type": "list", "required": true}, {"column_type": "lookup", "path": "institution_1", "field": "institution_1", "lookup_field": "country", "entity": "Institution", "type": "list", "required": true}]}} dataBinding={{"entity": "Book", "endpoint": "/book/"}} />
      </main>
    </div>    </div>
  );
};

export default Book;
