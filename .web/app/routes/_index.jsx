import {Fragment,useCallback,useContext,useEffect} from "react"
import {ClientSide,EventLoopContext,StateContexts} from "$/utils/context"
import {ReflexEvent,isTrue} from "$/utils/state"
import {Box as RadixThemesBox,Button as RadixThemesButton,Card as RadixThemesCard,Flex as RadixThemesFlex,Grid as RadixThemesGrid,Heading as RadixThemesHeading,ScrollArea as RadixThemesScrollArea,Separator as RadixThemesSeparator,Text as RadixThemesText,TextArea as RadixThemesTextArea,TextField as RadixThemesTextField} from "@radix-ui/themes"
import {ArrowUpDown as LucideArrowUpDown,Database as LucideDatabase,Download as LucideDownload,FileCode as LucideFileCode,FileSpreadsheet as LucideFileSpreadsheet,Play as LucidePlay,RefreshCw as LucideRefreshCw,Search as LucideSearch,Table as LucideTable,Terminal as LucideTerminal,Trash2 as LucideTrash2,Upload as LucideUpload} from "lucide-react"
import {PrismAsyncLight as SyntaxHighlighter} from "react-syntax-highlighter"
import "gridjs/dist/theme/mermaid.css"
import {jsx} from "@emotion/react"

const DataTableGrid = ClientSide(() => import('gridjs-react').then((mod) => mod.Grid))


function Flex_dd5c9462724c2b04f94ca71a05c32cb7 () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_dc83e9e8f3f9cfee213e48ab0aa1d533 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_tab", ({ ["tab"] : "explorer" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["padding"] : "0.75em", ["borderRadius"] : "10px", ["width"] : "100%", ["cursor"] : "pointer", ["backgroundColor"] : ((reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_?.valueOf?.() === "explorer"?.valueOf?.()) ? "#334155" : "transparent"), ["color"] : ((reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_?.valueOf?.() === "explorer"?.valueOf?.()) ? "#38bdf8" : "white"), ["transition"] : "all 0.2s", ["&:hover"] : ({ ["backgroundColor"] : "#1e293b", ["color"] : "#38bdf8" }) }),direction:"row",onClick:on_click_dc83e9e8f3f9cfee213e48ab0aa1d533,gap:"3"},jsx(LucideSearch,{size:20},),jsx(RadixThemesText,{as:"p",size:"3",weight:"medium"},"Explorador"))
  )
}


function Flex_40703b823f7a8658270da0b638b80ccd () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_026f8218a84c866235d4026a910cdaf1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_tab", ({ ["tab"] : "sql" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["padding"] : "0.75em", ["borderRadius"] : "10px", ["width"] : "100%", ["cursor"] : "pointer", ["backgroundColor"] : ((reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_?.valueOf?.() === "sql"?.valueOf?.()) ? "#334155" : "transparent"), ["color"] : ((reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_?.valueOf?.() === "sql"?.valueOf?.()) ? "#38bdf8" : "white"), ["transition"] : "all 0.2s", ["&:hover"] : ({ ["backgroundColor"] : "#1e293b", ["color"] : "#38bdf8" }) }),direction:"row",onClick:on_click_026f8218a84c866235d4026a910cdaf1,gap:"3"},jsx(LucideTerminal,{size:20},),jsx(RadixThemesText,{as:"p",size:"3",weight:"medium"},"Consola SQL"))
  )
}


function Flex_573d2c78a4c57677511a74aa08a18b51 () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_114333f7052a2e6e153cbc22695b7c25 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_tab", ({ ["tab"] : "io" }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["padding"] : "0.75em", ["borderRadius"] : "10px", ["width"] : "100%", ["cursor"] : "pointer", ["backgroundColor"] : ((reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_?.valueOf?.() === "io"?.valueOf?.()) ? "#334155" : "transparent"), ["color"] : ((reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_?.valueOf?.() === "io"?.valueOf?.()) ? "#38bdf8" : "white"), ["transition"] : "all 0.2s", ["&:hover"] : ({ ["backgroundColor"] : "#1e293b", ["color"] : "#38bdf8" }) }),direction:"row",onClick:on_click_114333f7052a2e6e153cbc22695b7c25,gap:"3"},jsx(LucideArrowUpDown,{size:20},),jsx(RadixThemesText,{as:"p",size:"3",weight:"medium"},"Datos IO"))
  )
}


function Text_068de294a3894396750ac8abe1793b3c () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)



  return (
    jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},(isTrue(reflex___state____state__maria_manager___state____app_state.dbname_rx_state_) ? reflex___state____state__maria_manager___state____app_state.dbname_rx_state_ : "Sin BD"))
  )
}


function Button_cd6a240f3050c027c097f1448ac4a87b () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_2684fc36db7607e4720eb21df14ac909 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.logout", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{color:"gray",css:({ ["width"] : "100%" }),onClick:on_click_2684fc36db7607e4720eb21df14ac909,size:"1",variant:"ghost"},"Cerrar Sesi\u00f3n")
  )
}


function Fragment_db95d3574422fa4e9fc7592b4b2c365b () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    jsx(Fragment,{},(() => {
  switch (JSON.stringify(reflex___state____state__maria_manager___state____app_state.current_tab_rx_state_)) {
    case JSON.stringify("explorer"):
      return jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "start" }),direction:"row",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "240px", ["paddingRight"] : "1.5em", ["borderRight"] : "1px solid #1e2937" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2",weight:"bold"},"TABLAS"),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(LucideRefreshCw,{css:({ ["cursor"] : "pointer", ["color"] : "gray" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.load_tables", ({  }), ({  })))], [_e], ({  })))),size:14},)),jsx(RadixThemesSeparator,{css:({ ["color"] : "#334155" }),size:"4"},),jsx(RadixThemesScrollArea,{css:({ ["height"] : "65vh" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"1"},Array.prototype.map.call(reflex___state____state__maria_manager___state____app_state.tables_rx_state_ ?? [],((table_rx_state_,index_3d99977b704683e90fb2fc2b7c793cf7)=>(jsx(RadixThemesButton,{color:"sky",css:({ ["width"] : "100%", ["justify"] : "start", ["color"] : ((reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_?.valueOf?.() === table_rx_state_?.valueOf?.()) ? "white" : "#cbd5e1"), ["&:hover"] : ({ ["backgroundColor"] : "#1e293b", ["color"] : "#38bdf8" }) }),key:index_3d99977b704683e90fb2fc2b7c793cf7,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.select_table", ({ ["table_name"] : table_rx_state_ }), ({  })))], [_e], ({  })))),size:"2",variant:((reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_?.valueOf?.() === table_rx_state_?.valueOf?.()) ? "solid" : "ghost")},table_rx_state_))))))),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["flex"] : "1", ["paddingLeft"] : "2em" }),direction:"column",gap:"3"},jsx(Fragment,{},(isTrue(reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_)?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "stretch" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(LucideFileCode,{css:({ ["color"] : "#38bdf8" }),size:24},),jsx(RadixThemesHeading,{size:"6"},reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.drop_selected_table", ({  }), ({  })))], [_e], ({  })))),size:"2",variant:"soft"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(LucideTrash2,{size:16},),jsx(RadixThemesText,{as:"p"},"Eliminar")))),jsx(SyntaxHighlighter,{children:reflex___state____state__maria_manager___state____app_state.selected_schema_rx_state_,css:({ ["width"] : "100%", ["borderRadius"] : "12px", ["marginTop"] : "1em" }),language:"sql",style:"dracula"},)))):(jsx(Fragment,{},jsx(RadixThemesFlex,{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%", ["height"] : "60vh" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"column",gap:"3"},jsx(LucideSearch,{css:({ ["color"] : "#1e2937" }),size:48},),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" })},"Selecciona una tabla para explorar su estructura")))))))));
      break;
    case JSON.stringify("sql"):
      return jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"4"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center", ["marginBottom"] : "1em" }),direction:"row",gap:"3"},jsx(LucideTerminal,{css:({ ["color"] : "#38bdf8" }),size:24},),jsx(RadixThemesHeading,{size:"6"},"Consola de Comandos SQL")),jsx(RadixThemesTextArea,{css:({ ["& textarea"] : null, ["height"] : "200px", ["width"] : "100%", ["backgroundColor"] : "#020617", ["border"] : "1px solid #1e2937", ["color"] : "#38bdf8", ["fontFamily"] : "monospace", ["--default-font-family"] : "monospace" }),onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_sql_query", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:"SELECT * FROM usuarios WHERE activo = 1;"},),jsx(RadixThemesButton,{color:"sky",css:({ ["width"] : "100%" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.execute_sql", ({  }), ({  })))], [_e], ({  })))),size:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(LucidePlay,{size:16},),jsx(RadixThemesText,{as:"p"},"EJECUTAR SENTENCIA"))),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#fbbf24", ["marginTop"] : "0.5em" }),size:"2"},reflex___state____state__maria_manager___state____app_state.sql_error_rx_state_),jsx(RadixThemesSeparator,{css:({ ["marginTop"] : "2em", ["marginBottom"] : "2em", ["color"] : "#1e2937" }),size:"4"},),jsx(Fragment,{},((reflex___state____state__maria_manager___state____app_state.sql_columns_rx_state_.length > 0)?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"2"},jsx(LucideTable,{css:({ ["color"] : "gray" }),size:18},),jsx(RadixThemesText,{as:"p",size:"3",weight:"bold"},"Resultados de la Consulta")),jsx(RadixThemesBox,{css:({ ["padding"] : "1em", ["backgroundColor"] : "#0f172a", ["border"] : "1px solid #1e2937", ["borderRadius"] : "12px", ["width"] : "100%" })},jsx(DataTableGrid,{columns:reflex___state____state__maria_manager___state____app_state.sql_columns_rx_state_,css:({ ["width"] : "100%" }),data:reflex___state____state__maria_manager___state____app_state.sql_results_rx_state_,pagination:true,resizable:true,search:true,sort:true},))))):(jsx(Fragment,{},jsx(RadixThemesFlex,{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%", ["padding"] : "3em" })},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2"},"Los resultados aparecer\u00e1n aqu\u00ed tras la ejecuci\u00f3n")))))));
      break;
    case JSON.stringify("io"):
      return jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["marginBottom"] : "2em" }),direction:"row",gap:"3"},jsx(LucideArrowUpDown,{css:({ ["color"] : "#38bdf8" }),size:24},),jsx(RadixThemesHeading,{size:"6"},"Importaci\u00f3n y Exportaci\u00f3n de Datos")),jsx(RadixThemesGrid,{columns:"2",css:({ ["width"] : "100%" }),gap:"5"},jsx(RadixThemesCard,{css:({ ["padding"] : "1.5em", ["backgroundColor"] : "#111827", ["border"] : "1px solid #1e2937" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"column",gap:"4"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(LucideDatabase,{css:({ ["color"] : "#818cf8" })},),jsx(RadixThemesText,{as:"p",weight:"bold"},"Respaldo General SQL")),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2"},"Clona toda la base de datos en un solo archivo."),jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_export_sql_path", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:"C:/respaldos/backup.sql"},),jsx(RadixThemesButton,{css:({ ["width"] : "100%" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.export_sql_backup", ({  }), ({  })))], [_e], ({  })))),variant:"surface"},"Generar Backup .SQL"),jsx(RadixThemesSeparator,{size:"4"},),jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_import_sql_path", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:"C:/descargas/migracion.sql"},),jsx(RadixThemesButton,{color:"sky",css:({ ["width"] : "100%" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.import_sql_backup", ({  }), ({  })))], [_e], ({  })))),variant:"soft"},"Restaurar desde SQL"))),jsx(RadixThemesCard,{css:({ ["padding"] : "1.5em", ["backgroundColor"] : "#111827", ["border"] : "1px solid #1e2937" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"column",gap:"4"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(LucideFileSpreadsheet,{css:({ ["color"] : "#34d399" })},),jsx(RadixThemesText,{as:"p",weight:"bold"},"Manejo de Bloques CSV")),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2"},"Mueve datos de tablas espec\u00edficas."),jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_target_table_csv", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:"Nombre de la tabla"},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(RadixThemesTextField.Root,{css:({ ["flex"] : "1" }),onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_export_csv_path", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:"Destino .csv"},),jsx(RadixThemesButton,{onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.export_csv_table", ({  }), ({  })))], [_e], ({  }))))},jsx(LucideDownload,{},))),jsx(RadixThemesSeparator,{size:"4"},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(RadixThemesTextField.Root,{css:({ ["flex"] : "1" }),onChange:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_import_csv_path", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))),placeholder:"Origen .csv"},),jsx(RadixThemesButton,{color:"green",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.import_csv_table", ({  }), ({  })))], [_e], ({  }))))},jsx(LucideUpload,{},)))))),jsx(RadixThemesBox,{css:({ ["marginTop"] : "1em" })},jsx(RadixThemesText,{as:"p",css:({ ["color"] : (reflex___state____state__maria_manager___state____app_state.io_is_error_rx_state_ ? "#f87171" : "#34d399") }),weight:"bold"},reflex___state____state__maria_manager___state____app_state.io_message_rx_state_)));
      break;
    default:
      return jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "start" }),direction:"row",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "240px", ["paddingRight"] : "1.5em", ["borderRight"] : "1px solid #1e2937" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"2",weight:"bold"},"TABLAS"),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(LucideRefreshCw,{css:({ ["cursor"] : "pointer", ["color"] : "gray" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.load_tables", ({  }), ({  })))], [_e], ({  })))),size:14},)),jsx(RadixThemesSeparator,{css:({ ["color"] : "#334155" }),size:"4"},),jsx(RadixThemesScrollArea,{css:({ ["height"] : "65vh" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"1"},Array.prototype.map.call(reflex___state____state__maria_manager___state____app_state.tables_rx_state_ ?? [],((table_rx_state_,index_3d99977b704683e90fb2fc2b7c793cf7)=>(jsx(RadixThemesButton,{color:"sky",css:({ ["width"] : "100%", ["justify"] : "start", ["color"] : ((reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_?.valueOf?.() === table_rx_state_?.valueOf?.()) ? "white" : "#cbd5e1"), ["&:hover"] : ({ ["backgroundColor"] : "#1e293b", ["color"] : "#38bdf8" }) }),key:index_3d99977b704683e90fb2fc2b7c793cf7,onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.select_table", ({ ["table_name"] : table_rx_state_ }), ({  })))], [_e], ({  })))),size:"2",variant:((reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_?.valueOf?.() === table_rx_state_?.valueOf?.()) ? "solid" : "ghost")},table_rx_state_))))))),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["flex"] : "1", ["paddingLeft"] : "2em" }),direction:"column",gap:"3"},jsx(Fragment,{},(isTrue(reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_)?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "stretch" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(LucideFileCode,{css:({ ["color"] : "#38bdf8" }),size:24},),jsx(RadixThemesHeading,{size:"6"},reflex___state____state__maria_manager___state____app_state.selected_table_rx_state_),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(RadixThemesButton,{color:"red",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.drop_selected_table", ({  }), ({  })))], [_e], ({  })))),size:"2",variant:"soft"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(LucideTrash2,{size:16},),jsx(RadixThemesText,{as:"p"},"Eliminar")))),jsx(SyntaxHighlighter,{children:reflex___state____state__maria_manager___state____app_state.selected_schema_rx_state_,css:({ ["width"] : "100%", ["borderRadius"] : "12px", ["marginTop"] : "1em" }),language:"sql",style:"dracula"},)))):(jsx(Fragment,{},jsx(RadixThemesFlex,{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%", ["height"] : "60vh" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"column",gap:"3"},jsx(LucideSearch,{css:({ ["color"] : "#1e2937" }),size:48},),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" })},"Selecciona una tabla para explorar su estructura")))))))));
      break;
  }
})())
  )
}


function Text_d9fe0de12210eac7254fc0a0130081fc () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)



  return (
    jsx(RadixThemesText,{as:"p",css:({ ["color"] : "#f87171" }),size:"2",weight:"bold"},reflex___state____state__maria_manager___state____app_state.error_msg_rx_state_)
  )
}


function Textfield__root_1c6e7c7abdffdd0e25a03fcfef21e2d3 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_cb0c8490be775ab31294048638501272 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_host", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),defaultValue:"localhost",onChange:on_change_cb0c8490be775ab31294048638501272,placeholder:"Host"},)
  )
}


function Textfield__root_cf07413ee0ae17433b6580dd3c5c4168 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_0476629d7407383785bba699e65b4be2 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_port", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),defaultValue:"3307",onChange:on_change_0476629d7407383785bba699e65b4be2,placeholder:"Puerto"},)
  )
}


function Textfield__root_f874368ac95c3596b7a703aea6504aa4 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_a174cb665e6a167aa9d98def3cce6a1c = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_user", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),defaultValue:"root",onChange:on_change_a174cb665e6a167aa9d98def3cce6a1c,placeholder:"Usuario"},)
  )
}


function Textfield__root_a8c931719fe77f795ca15bb5f39622a9 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_9b4889f0c740a6b3004c1603673d1630 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_password", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),onChange:on_change_9b4889f0c740a6b3004c1603673d1630,placeholder:"Password",type:"password"},)
  )
}


function Textfield__root_3763d90b41809be4be4d91d01f38c638 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_change_bdd283d9c0dc1ff25aab1f836904f765 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.set_dbname", ({ ["val"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesTextField.Root,{css:({ ["width"] : "100%" }),onChange:on_change_bdd283d9c0dc1ff25aab1f836904f765,placeholder:"Base de datos"},)
  )
}


function Button_d91c1177a7a874b58a257e7831552046 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

const on_click_3ef76a95ec590a7cf79ba590bbd99e78 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.maria_manager___state____app_state.connect_db", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])

  return (
    jsx(RadixThemesButton,{color:"sky",css:({ ["width"] : "100%", ["marginTop"] : "1em" }),onClick:on_click_3ef76a95ec590a7cf79ba590bbd99e78,size:"3"},"CONECTAR AHORA")
  )
}


function Fragment_3d821695305c604e4cae4d30b9501283 () {
  const reflex___state____state__maria_manager___state____app_state = useContext(StateContexts.reflex___state____state__maria_manager___state____app_state)



  return (
    jsx(Fragment,{},(reflex___state____state__maria_manager___state____app_state.connected_rx_state_?(jsx(Fragment,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%", ["height"] : "100vh" }),direction:"row",gap:"0"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "240px", ["height"] : "100vh", ["backgroundColor"] : "#020617", ["padding"] : "1.5em", ["alignItems"] : "start", ["borderRight"] : "1px solid #1e2937" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center", ["paddingTop"] : "1.5em", ["paddingBottom"] : "1.5em" }),direction:"row",gap:"2"},jsx(LucideDatabase,{css:({ ["color"] : "#38bdf8" }),size:24},),jsx(RadixThemesHeading,{css:({ ["color"] : "white" }),size:"5"},"MariaDB")),jsx(Flex_dd5c9462724c2b04f94ca71a05c32cb7,{},),jsx(Flex_40703b823f7a8658270da0b638b80ccd,{},),jsx(Flex_573d2c78a4c57677511a74aa08a18b51,{},),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"2"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"row",gap:"2"},jsx(RadixThemesBox,{css:({ ["width"] : "8px", ["height"] : "8px", ["borderRadius"] : "50%", ["backgroundColor"] : "#10b981" })},),jsx(Text_068de294a3894396750ac8abe1793b3c,{},)),jsx(Button_cd6a240f3050c027c097f1448ac4a87b,{},))),jsx(RadixThemesBox,{css:({ ["flex"] : "1", ["backgroundColor"] : "#030712" })},jsx(RadixThemesScrollArea,{css:({ ["height"] : "100vh" })},jsx(RadixThemesBox,{css:({ ["padding"] : "3em", ["maxWidth"] : "1200px", ["margin"] : "0 auto" })},jsx(Fragment_db95d3574422fa4e9fc7592b4b2c365b,{},))))))):(jsx(Fragment,{},jsx(RadixThemesFlex,{css:({ ["display"] : "flex", ["alignItems"] : "center", ["justifyContent"] : "center", ["width"] : "100%", ["height"] : "100vh", ["background"] : "radial-gradient(circle at top left, #0f172a 0%, #020617 100%)" })},jsx(RadixThemesBox,{css:({ ["padding"] : "2.5em", ["borderRadius"] : "24px", ["boxShadow"] : "0px 20px 50px rgba(0,0,0,0.8)", ["backgroundColor"] : "#111827", ["border"] : "1px solid #1f2937", ["width"] : "400px" })},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["width"] : "100%" }),direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",css:({ ["alignItems"] : "center" }),direction:"row",gap:"3"},jsx(LucideDatabase,{css:({ ["color"] : "#38bdf8" }),size:32},),jsx(RadixThemesHeading,{css:({ ["color"] : "white" }),size:"7"},"MariaDB Manager")),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray", ["marginBottom"] : "1.5em" })},"Acceso Seguro al Servidor"),jsx(Text_d9fe0de12210eac7254fc0a0130081fc,{},),jsx(Textfield__root_1c6e7c7abdffdd0e25a03fcfef21e2d3,{},),jsx(Textfield__root_cf07413ee0ae17433b6580dd3c5c4168,{},),jsx(Textfield__root_f874368ac95c3596b7a703aea6504aa4,{},),jsx(Textfield__root_a8c931719fe77f795ca15bb5f39622a9,{},),jsx(Textfield__root_3763d90b41809be4be4d91d01f38c638,{},),jsx(Button_d91c1177a7a874b58a257e7831552046,{},))))))))
  )
}


export default function Component() {





  return (
    jsx(Fragment,{},jsx(Fragment_3d821695305c604e4cae4d30b9501283,{},),jsx("title",{},"MariaDB Web Manager"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}