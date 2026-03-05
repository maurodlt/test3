import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Author: React.FC = () => {
  return (
    <div id="page-author-6">
    <div id="il9uva" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ie9s7o" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="igasa2" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <a id="i5me5n" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/publication">{"Publication"}</a>
        <a id="i6eqtk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/institution">{"Institution"}</a>
        <a id="iihxp4" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
        <div id="ionn2b" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}} />
        <p id="ike13o" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="imm1xu" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="iqjsfn" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Author"}</h1>
        <p id="i5z94t" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Author data"}</p>
        <TableBlock id="table-author-6" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Author List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Last Name", "column_type": "field", "field": "last_name", "type": "str", "required": true}, {"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "Institution", "column_type": "lookup", "path": "institution", "entity": "Institution", "field": "country", "type": "list", "required": false}, {"label": "Publication 1", "column_type": "lookup", "path": "publication_1", "entity": "Publication", "field": "year", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "last_name", "label": "last_name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "institution", "field": "institution", "lookup_field": "country", "entity": "Institution", "type": "list", "required": false}, {"column_type": "lookup", "path": "publication_1", "field": "publication_1", "lookup_field": "year", "entity": "Publication", "type": "list", "required": false}]}} dataBinding={{"entity": "Author", "endpoint": "/author/"}} />
      </main>
    </div>    </div>
  );
};

export default Author;
