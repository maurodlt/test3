import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Others: React.FC = () => {
  return (
    <div id="page-others-1">
    <div id="ivv8l" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="i2yaa" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iqq83" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="iruoq" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ic02b" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/journal">{"Journal"}</a>
          <a id="ir6wv" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/others">{"Others"}</a>
          <a id="iz9od" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/thesis">{"Thesis"}</a>
          <a id="ideko" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/book">{"Book"}</a>
          <a id="iqsif" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/proceedings">{"Proceedings"}</a>
          <a id="ii4d3" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/publication">{"Publication"}</a>
          <a id="iobbg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
          <a id="i57eng" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/institution">{"Institution"}</a>
          <a id="ilap3d" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/conference">{"Conference"}</a>
        </div>
        <p id="i6aa5n" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="ibudjj" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ieiaoj" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Others"}</h1>
        <p id="ilf2le" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Others data"}</p>
        <TableBlock id="table-others-1" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Others List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Peer Reviewed", "column_type": "field", "field": "peer_reviewed", "type": "bool", "required": true}, {"label": "Link", "column_type": "field", "field": "link", "type": "str", "required": true}, {"label": "Server", "column_type": "field", "field": "server", "type": "str", "required": true}, {"label": "Year", "column_type": "field", "field": "year", "type": "int", "required": true}, {"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Author 1", "column_type": "lookup", "path": "author_1", "entity": "Author", "field": "last_name", "type": "list", "required": true}, {"label": "Institution 1", "column_type": "lookup", "path": "institution_1", "entity": "Institution", "field": "country", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "link", "label": "link", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "server", "label": "server", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "peer_reviewed", "label": "peer_reviewed", "type": "bool", "required": true, "defaultValue": null}, {"column_type": "field", "field": "year", "label": "year", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "author_1", "field": "author_1", "lookup_field": "last_name", "entity": "Author", "type": "list", "required": true}, {"column_type": "lookup", "path": "institution_1", "field": "institution_1", "lookup_field": "country", "entity": "Institution", "type": "list", "required": false}]}} dataBinding={{"entity": "Others", "endpoint": "/others/"}} />
      </main>
    </div>    </div>
  );
};

export default Others;
