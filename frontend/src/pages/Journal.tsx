import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Journal: React.FC = () => {
  return (
    <div id="page-journal-0">
    <div id="iiibb" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ip87j" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="io1or" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iaihh" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i73kg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/publication">{"Publication"}</a>
          <a id="ibxbf" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/institution">{"Institution"}</a>
          <a id="iuw2p" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
        </div>
        <p id="ivd6r" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iwp9g" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ina11" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Journal"}</h1>
        <p id="ix0al" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Journal data"}</p>
        <TableBlock id="table-journal-0" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Journal List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Pages", "column_type": "field", "field": "pages", "type": "str", "required": true}, {"label": "Month", "column_type": "field", "field": "month", "type": "str", "required": true}, {"label": "Note", "column_type": "field", "field": "note", "type": "str", "required": true}, {"label": "Volume", "column_type": "field", "field": "volume", "type": "str", "required": true}, {"label": "Journal", "column_type": "field", "field": "journal", "type": "str", "required": true}, {"label": "Number", "column_type": "field", "field": "number", "type": "str", "required": true}, {"label": "Year", "column_type": "field", "field": "year", "type": "int", "required": true}, {"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Author 1", "column_type": "lookup", "path": "author_1", "entity": "Author", "field": "last_name", "type": "list", "required": true}, {"label": "Institution 1", "column_type": "lookup", "path": "institution_1", "entity": "Institution", "field": "country", "type": "list", "required": true}], "formColumns": [{"column_type": "field", "field": "pages", "label": "pages", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "month", "label": "month", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "note", "label": "note", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "volume", "label": "volume", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "journal", "label": "journal", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "number", "label": "number", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "year", "label": "year", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "author_1", "field": "author_1", "lookup_field": "name", "entity": "Author", "type": "list", "required": true}, {"column_type": "lookup", "path": "institution_1", "field": "institution_1", "lookup_field": "country", "entity": "Institution", "type": "list", "required": true}]}} dataBinding={{"entity": "Journal", "endpoint": "/journal/"}} />
      </main>
    </div>    </div>
  );
};

export default Journal;
