import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Thesis: React.FC = () => {
  return (
    <div id="page-thesis-2">
    <div id="idcp1i" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="ipzor7" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="iwi1vf" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="ivwv2q" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="ij9fu7" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/journal">{"Journal"}</a>
          <a id="ivrq0p" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/others">{"Others"}</a>
          <a id="ie8ivg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/thesis">{"Thesis"}</a>
          <a id="ieeshx" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/book">{"Book"}</a>
          <a id="in0lme" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/proceedings">{"Proceedings"}</a>
          <a id="iu9b2z" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/publication">{"Publication"}</a>
          <a id="ix148y" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
          <a id="ipbyjg" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/institution">{"Institution"}</a>
          <a id="i1izoj" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/conference">{"Conference"}</a>
        </div>
        <p id="i74c7a" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="i35s2u" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ihp0w9" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Thesis"}</h1>
        <p id="i02ejj" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Thesis data"}</p>
        <TableBlock id="table-thesis-2" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Thesis List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Month", "column_type": "field", "field": "month", "type": "str", "required": true}, {"label": "Address", "column_type": "field", "field": "address", "type": "str", "required": true}, {"label": "Type", "column_type": "field", "field": "type", "type": "str", "required": true}, {"label": "Note", "column_type": "field", "field": "note", "type": "str", "required": true}, {"label": "Year", "column_type": "field", "field": "year", "type": "int", "required": true}, {"label": "Title", "column_type": "field", "field": "title", "type": "str", "required": true}, {"label": "Author 1", "column_type": "lookup", "path": "author_1", "entity": "Author", "field": "last_name", "type": "list", "required": true}, {"label": "Institution 1", "column_type": "lookup", "path": "institution_1", "entity": "Institution", "field": "country", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "month", "label": "month", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "address", "label": "address", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "type", "label": "type", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "note", "label": "note", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "year", "label": "year", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "title", "label": "title", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "author_1", "field": "author_1", "lookup_field": "last_name", "entity": "Author", "type": "list", "required": true}, {"column_type": "lookup", "path": "institution_1", "field": "institution_1", "lookup_field": "country", "entity": "Institution", "type": "list", "required": false}]}} dataBinding={{"entity": "Thesis", "endpoint": "/thesis/"}} />
      </main>
    </div>    </div>
  );
};

export default Thesis;
