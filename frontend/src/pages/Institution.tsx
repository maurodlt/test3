import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";

const Institution: React.FC = () => {
  return (
    <div id="page-institution-7">
    <div id="igquq9" style={{"display": "flex", "height": "100vh", "fontFamily": "Arial, sans-serif", "--chart-color-palette": "default"}}>
      <nav id="idlehw" style={{"width": "250px", "background": "linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", "color": "white", "padding": "20px", "overflowY": "auto", "display": "flex", "flexDirection": "column", "--chart-color-palette": "default"}}>
        <h2 id="ic9o8h" style={{"marginTop": "0", "fontSize": "24px", "marginBottom": "30px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"BESSER"}</h2>
        <div id="i6ev1m" style={{"display": "flex", "flexDirection": "column", "flex": "1", "--chart-color-palette": "default"}}>
          <a id="i1e0il" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/journal">{"Journal"}</a>
          <a id="i98twk" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/others">{"Others"}</a>
          <a id="iofoid" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/thesis">{"Thesis"}</a>
          <a id="iv8xkr" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/book">{"Book"}</a>
          <a id="itfjcd" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/proceedings">{"Proceedings"}</a>
          <a id="i71mha" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/publication">{"Publication"}</a>
          <a id="i22llh" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/author">{"Author"}</a>
          <a id="i1r19i" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "rgba(255,255,255,0.2)", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/institution">{"Institution"}</a>
          <a id="id2rel" style={{"color": "white", "textDecoration": "none", "padding": "10px 15px", "display": "block", "background": "transparent", "borderRadius": "4px", "marginBottom": "5px", "--chart-color-palette": "default"}} href="/conference">{"Conference"}</a>
        </div>
        <p id="ievwmk" style={{"marginTop": "auto", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.2)", "fontSize": "11px", "opacity": "0.8", "textAlign": "center", "--chart-color-palette": "default"}}>{"© 2026 BESSER. All rights reserved."}</p>
      </nav>
      <main id="iy79ks" style={{"flex": "1", "padding": "40px", "overflowY": "auto", "background": "#f5f5f5", "--chart-color-palette": "default"}}>
        <h1 id="ivhej9" style={{"marginTop": "0", "color": "#333", "fontSize": "32px", "marginBottom": "10px", "--chart-color-palette": "default"}}>{"Institution"}</h1>
        <p id="iiix2i" style={{"color": "#666", "marginBottom": "30px", "--chart-color-palette": "default"}}>{"Manage Institution data"}</p>
        <TableBlock id="table-institution-7" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Institution List" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "Country", "column_type": "field", "field": "country", "type": "str", "required": true}, {"label": "City", "column_type": "field", "field": "city", "type": "str", "required": true}, {"label": "Name", "column_type": "field", "field": "name", "type": "str", "required": true}, {"label": "Author", "column_type": "lookup", "path": "author", "entity": "Author", "field": "last_name", "type": "list", "required": false}, {"label": "Publication", "column_type": "lookup", "path": "publication", "entity": "Publication", "field": "year", "type": "list", "required": false}], "formColumns": [{"column_type": "field", "field": "country", "label": "country", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "city", "label": "city", "type": "str", "required": true, "defaultValue": null}, {"column_type": "field", "field": "name", "label": "name", "type": "str", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "author", "field": "author", "lookup_field": "last_name", "entity": "Author", "type": "list", "required": false}, {"column_type": "lookup", "path": "publication", "field": "publication", "lookup_field": "year", "entity": "Publication", "type": "list", "required": false}]}} dataBinding={{"entity": "Institution", "endpoint": "/institution/"}} />
      </main>
    </div>    </div>
  );
};

export default Institution;
