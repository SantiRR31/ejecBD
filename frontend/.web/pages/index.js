/** @jsxImportSource @emotion/react */


import { Fragment, useContext, useRef } from "react"
import { ColorModeContext, EventLoopContext, StateContexts, UploadFilesContext } from "/utils/context"
import { Event, getBackendURL, isTrue, refs, set_val } from "/utils/state"
import { Badge as RadixThemesBadge, Box as RadixThemesBox, Button as RadixThemesButton, Callout as RadixThemesCallout, Card as RadixThemesCard, Container as RadixThemesContainer, Dialog as RadixThemesDialog, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Link as RadixThemesLink, ScrollArea as RadixThemesScrollArea, Select as RadixThemesSelect, Separator as RadixThemesSeparator, Table as RadixThemesTable, Tabs as RadixThemesTabs, Text as RadixThemesText, TextArea as RadixThemesTextArea, TextField as RadixThemesTextField, Theme as RadixThemesTheme } from "@radix-ui/themes"
import env from "/env.json"
import { CodeIcon as LucideCodeIcon, DatabaseIcon as LucideDatabaseIcon, DownloadIcon as LucideDownloadIcon, FileTextIcon as LucideFileTextIcon, InfoIcon as LucideInfoIcon, LogOutIcon as LucideLogOutIcon, PlayIcon as LucidePlayIcon, PlugIcon as LucidePlugIcon, PlusIcon as LucidePlusIcon, TableIcon as LucideTableIcon, TrashIcon as LucideTrashIcon, UploadIcon as LucideUploadIcon, UsersIcon as LucideUsersIcon, ZapIcon as LucideZapIcon } from "lucide-react"
import { DebounceInput } from "react-debounce-input"
import "@radix-ui/themes/styles.css"
import "gridjs/dist/theme/mermaid.css"
import theme from "/utils/theme.js"
import { PrismAsyncLight as SyntaxHighlighter } from "react-syntax-highlighter"
import oneLight from "react-syntax-highlighter/dist/cjs/styles/prism/one-light"
import oneDark from "react-syntax-highlighter/dist/cjs/styles/prism/one-dark"
import sql from "react-syntax-highlighter/dist/cjs/languages/prism/sql"
import { Grid as DataTableGrid } from "gridjs-react"
import NextLink from "next/link"
import ReactDropzone from "react-dropzone"
import { Box, Input } from "@chakra-ui/react"
import NextHead from "next/head"



export function Fragment_1762bb90abdb81b879b2a22edbbe01a1 () {
  const [addEvents, connectError] = useContext(EventLoopContext);


  return (
    <Fragment>
  {isTrue(connectError !== null) ? (
  <Fragment>
  <RadixThemesDialog.Root open={connectError !== null}>
  <RadixThemesDialog.Content>
  <RadixThemesDialog.Title>
  {`Connection Error`}
</RadixThemesDialog.Title>
  <RadixThemesText as={`p`}>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {getBackendURL(env.EVENT).href}
</RadixThemesText>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}
SyntaxHighlighter.registerLanguage('sql', sql)

export function Fragment_451db3e26a917de9fd2d6ad75e6bb897 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)
  const [addEvents, connectError] = useContext(EventLoopContext);
  const [filesById, setFilesById] = useContext(UploadFilesContext);
  const ref_db_upload = useRef(null); refs['ref_db_upload'] = ref_db_upload;
  const state__state = useContext(StateContexts.state__state)


  return (
    <Fragment>
  {isTrue(state__state.app_logged_in) ? (
  <Fragment>
  {isTrue(state__state.connected) ? (
  <Fragment>
  <RadixThemesBox css={{"width": "100%", "minHeight": "100vh", "background": "var(--gray-2)"}}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "paddingInlineStart": "2em", "paddingInlineEnd": "2em", "paddingTop": "1em", "paddingBottom": "1em", "background": "white", "borderBottom": "1px solid var(--gray-4)", "boxShadow": "sm", "flexDirection": "row"}} justify={`between`} gap={`2`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`4`}>
  <LucideDatabaseIcon css={{"color": "var(--accent-9)"}} size={32}>
  {`database`}
</LucideDatabaseIcon>
  <RadixThemesHeading size={`6`}>
  {`MariaDB Manager`}
</RadixThemesHeading>
  <RadixThemesBadge color={`indigo`} radius={`full`} size={`2`}>
  {isTrue(((state__state.database) !== (""))) ? state__state.database : `Servidor Raíz`}
</RadixThemesBadge>
  <RadixThemesBadge color={isTrue(((state__state.app_role) === ("admin"))) ? `red` : `teal`} radius={`full`} size={`2`}>
  {isTrue(((state__state.app_role) === ("admin"))) ? `Administrador` : `Lector`}
</RadixThemesBadge>
</RadixThemesFlex>
  <RadixThemesFlex align={`start`} css={{"flexDirection": "row"}} gap={`3`}>
  <Fragment>
  {isTrue(((state__state.app_role) === ("admin"))) ? (
  <Fragment>
  <RadixThemesButton color={`gray`} onClick={(_e) => addEvents([Event("state.state.disconnect_db", {})], (_e), {})} size={`2`} variant={`soft`}>
  <LucidePlugIcon css={{"color": "var(--current-color)"}}>
  {`plug`}
</LucidePlugIcon>
  {`Desconectar DB`}
</RadixThemesButton>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <RadixThemesButton color={`red`} onClick={(_e) => addEvents([Event("state.state.app_logout", {})], (_e), {})} size={`2`} variant={`soft`}>
  <LucideLogOutIcon css={{"color": "var(--current-color)"}}>
  {`log-out`}
</LucideLogOutIcon>
  {`Cerrar Sesión`}
</RadixThemesButton>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesContainer css={{"maxWidth": "1200px"}}>
  <RadixThemesCard css={{"width": "100%", "padding": "2em", "marginTop": "2em", "boxShadow": "md"}} size={`4`}>
  <RadixThemesTabs.Root css={{"width": "100%"}} defaultValue={`schema`}>
  <RadixThemesTabs.List css={{"marginBottom": "1em"}} size={`2`}>
  <RadixThemesTabs.Trigger value={`schema`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`2`}>
  <LucideTableIcon css={{"color": "var(--current-color)"}}>
  {`table`}
</LucideTableIcon>
  <RadixThemesText as={`p`}>
  {`Estructura`}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger value={`sql`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`2`}>
  <LucideCodeIcon css={{"color": "var(--current-color)"}}>
  {`code`}
</LucideCodeIcon>
  <RadixThemesText as={`p`}>
  {`Consola SQL`}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesTabs.Trigger>
  <Fragment>
  {isTrue(((state__state.app_role) === ("admin"))) ? (
  <Fragment>
  <RadixThemesTabs.Trigger value={`io`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`2`}>
  <LucideUploadIcon css={{"color": "var(--current-color)"}}>
  {`upload`}
</LucideUploadIcon>
  <RadixThemesText as={`p`}>
  {`Importar / Exportar`}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesTabs.Trigger>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Fragment>
  {isTrue(((state__state.app_role) === ("admin"))) ? (
  <Fragment>
  <RadixThemesTabs.Trigger value={`users`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`2`}>
  <LucideUsersIcon css={{"color": "var(--current-color)"}}>
  {`users`}
</LucideUsersIcon>
  <RadixThemesText as={`p`}>
  {`Usuarios App`}
</RadixThemesText>
</RadixThemesFlex>
</RadixThemesTabs.Trigger>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesTabs.List>
  <RadixThemesTabs.Content value={`schema`}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "alignItems": "start", "flexDirection": "column"}} gap={`4`}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "flexDirection": "row"}} justify={`between`} gap={`2`}>
  <RadixThemesHeading size={`5`} weight={`bold`}>
  {`Gestión de Tablas`}
</RadixThemesHeading>
  <Fragment>
  {isTrue(((state__state.app_role) === ("admin"))) ? (
  <Fragment>
  <RadixThemesDialog.Root>
  <RadixThemesDialog.Trigger>
  <RadixThemesButton color={`green`} size={`2`}>
  <LucidePlusIcon css={{"color": "var(--current-color)"}}>
  {`plus`}
</LucidePlusIcon>
  {`Nueva Tabla (Visual)`}
</RadixThemesButton>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"maxWidth": "600px"}}>
  <RadixThemesDialog.Title>
  {`Creador Visual de Tablas`}
</RadixThemesDialog.Title>
  <RadixThemesDialog.Description>
  {`Define el nombre y las columnas de tu nueva tabla.`}
</RadixThemesDialog.Description>
  <RadixThemesFlex align={`start`} css={{"flexDirection": "column"}} gap={`2`}>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Nombre de la tabla`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_tb_name", {value:_e0.target.value})], (_e0), {})} placeholder={`Ej. inventario_2024`} value={state__state.new_tb_name}/>
  <RadixThemesText as={`p`} css={{"marginTop": "1em"}} size={`2`} weight={`bold`}>
  {`Columnas`}
</RadixThemesText>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "flexDirection": "column"}} gap={`2`}>
  {state__state.new_tb_columns.map((col, idx) => (
  <RadixThemesFlex align={`start`} css={{"width": "100%", "alignItems": "center", "flexDirection": "row"}} key={idx} gap={`2`}>
  <DebounceInput css={{"width": "40%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.update_col_name", {val:_e0.target.value,idx:idx})], (_e0), {})} placeholder={`Nombre`} size={`2`} value={col["name"]}/>
  <RadixThemesSelect.Root onValueChange={(_e0) => addEvents([Event("state.state.update_col_type", {val:_e0,idx:idx})], (_e0), {})} size={`2`} value={col["type"]}>
  <RadixThemesSelect.Trigger css={{"width": "50%"}}/>
  <RadixThemesSelect.Content>
  <RadixThemesSelect.Group>
  {``}
  <RadixThemesSelect.Item value={`INT AUTO_INCREMENT PRIMARY KEY`}>
  {`INT AUTO_INCREMENT PRIMARY KEY`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`VARCHAR(255)`}>
  {`VARCHAR(255)`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`INT`}>
  {`INT`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`TEXT`}>
  {`TEXT`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`DATE`}>
  {`DATE`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`BOOLEAN`}>
  {`BOOLEAN`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`DECIMAL(10,2)`}>
  {`DECIMAL(10,2)`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`TIMESTAMP`}>
  {`TIMESTAMP`}
</RadixThemesSelect.Item>
</RadixThemesSelect.Group>
</RadixThemesSelect.Content>
</RadixThemesSelect.Root>
  <RadixThemesButton color={`red`} css={{"width": "10%"}} onClick={(_e) => addEvents([Event("state.state.remove_tb_column", {idx:idx})], (_e), {})} size={`2`} variant={`ghost`}>
  <LucideTrashIcon css={{"color": "var(--current-color)"}} size={16}>
  {`trash`}
</LucideTrashIcon>
</RadixThemesButton>
</RadixThemesFlex>
))}
</RadixThemesFlex>
  <RadixThemesButton color={`blue`} css={{"marginTop": "1em", "marginBottom": "1em"}} onClick={(_e) => addEvents([Event("state.state.add_tb_column", {})], (_e), {})} size={`2`} variant={`outline`}>
  <LucidePlusIcon css={{"color": "var(--current-color)"}}>
  {`plus`}
</LucidePlusIcon>
  {`Añadir Columna`}
</RadixThemesButton>
  <Fragment>
  {isTrue(state__state.create_tb_message) ? (
  <Fragment>
  <RadixThemesCallout.Root color={state__state.create_tb_message_color} css={{"icon": "info", "width": "100%"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.create_tb_message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "marginTop": "1em", "flexDirection": "row"}} justify={`between`} gap={`2`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Cerrar`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <RadixThemesButton color={`green`} css={{"isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.execute_create_table", {})], (_e), {})}>
  {`Construir y Crear Tabla`}
</RadixThemesButton>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
  <RadixThemesText as={`p`} color={`gray`} size={`2`}>
  {`Explora el esquema de las tablas de tu base de datos.`}
</RadixThemesText>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`4`}>
  <RadixThemesSelect.Root onValueChange={(_e0) => addEvents([Event("state.state.get_schema", {table_name:_e0})], (_e0), {})} size={`3`}>
  <RadixThemesSelect.Trigger css={{"width": "300px"}} placeholder={`Selecciona una tabla`}/>
  <RadixThemesSelect.Content>
  <RadixThemesSelect.Group>
  {``}
  {state__state.tables.map((item, index_efe375a01b46a1f2c495265a3b440b7a) => (
  <RadixThemesSelect.Item key={index_efe375a01b46a1f2c495265a3b440b7a} value={item}>
  {item}
</RadixThemesSelect.Item>
))}
</RadixThemesSelect.Group>
</RadixThemesSelect.Content>
</RadixThemesSelect.Root>
  <Fragment>
  {isTrue((((state__state.selected_table) !== ("")) && ((state__state.app_role) === ("admin")))) ? (
  <Fragment>
  <RadixThemesButton color={`red`} css={{"isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.drop_table", {})], (_e), {})} size={`3`} variant={`soft`}>
  <LucideTrashIcon css={{"color": "var(--current-color)"}}>
  {`trash`}
</LucideTrashIcon>
  {`Eliminar Tabla`}
</RadixThemesButton>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
  <Fragment>
  {isTrue(state__state.schema) ? (
  <Fragment>
  <RadixThemesBox css={{"width": "100%", "borderRadius": "md", "overflow": "hidden", "marginTop": "1em", "boxShadow": "sm"}}>
  <SyntaxHighlighter css={{"width": "100%"}} customStyle={{"width": "100%"}} language={`sql`} style={isTrue(((colorMode) === ("light"))) ? oneLight : oneDark} children={state__state.schema}/>
</RadixThemesBox>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content value={`sql`}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "alignItems": "start", "flexDirection": "column"}} gap={`4`}>
  <RadixThemesHeading size={`5`} weight={`bold`}>
  {`Ejecutar SQL`}
</RadixThemesHeading>
  <RadixThemesText as={`p`} color={`gray`} size={`2`}>
  {`Escribe comandos SELECT (si eres Admin, también INSERT, UPDATE, DELETE o CREATE).`}
</RadixThemesText>
  <DebounceInput css={{"height": "120px", "width": "100%", "fontFamily": "monospace"}} debounceTimeout={300} element={RadixThemesTextArea} onChange={(_e0) => addEvents([Event("state.state.set_sql_query", {value:_e0.target.value})], (_e0), {})} placeholder={`SELECT * FROM mi_tabla LIMIT 10;`} value={state__state.sql_query}/>
  <RadixThemesButton color={`indigo`} css={{"isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.execute_sql", {})], (_e), {})} size={`3`}>
  <LucidePlayIcon css={{"color": "var(--current-color)"}}>
  {`play`}
</LucidePlayIcon>
  {`Ejecutar Consulta`}
</RadixThemesButton>
  <Fragment>
  {isTrue(state__state.query_result_message) ? (
  <Fragment>
  <RadixThemesCallout.Root color={state__state.query_message_color} css={{"icon": "info", "width": "100%"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.query_result_message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Fragment>
  {isTrue(state__state.query_result_data) ? (
  <Fragment>
  <RadixThemesScrollArea css={{"maxWidth": "100%", "maxHeight": "400px", "border": "1px solid var(--gray-5)", "borderRadius": "md", "padding": "1em", "background": "white"}}>
  <DataTableGrid columns={state__state.query_result_columns} data={state__state.query_result_data} pagination={true} search={true} sort={true}/>
</RadixThemesScrollArea>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesTabs.Content>
  <Fragment>
  {isTrue(((state__state.app_role) === ("admin"))) ? (
  <Fragment>
  <RadixThemesTabs.Content value={`io`}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "alignItems": "start", "flexDirection": "column"}} gap={`4`}>
  <RadixThemesHeading size={`5`} weight={`bold`}>
  {`Exportar Datos`}
</RadixThemesHeading>
  <RadixThemesFlex align={`start`} css={{"flexDirection": "row"}} gap={`4`}>
  <RadixThemesLink asChild={true}>
  <NextLink css={{"isExternal": true}} href={`http://localhost:5000/api/export`} passHref={true}>
  <RadixThemesButton color={`indigo`} size={`3`} variant={`solid`}>
  <LucideDownloadIcon css={{"color": "var(--current-color)"}}>
  {`download`}
</LucideDownloadIcon>
  {`Backup BD Completa (.sql)`}
</RadixThemesButton>
</NextLink>
</RadixThemesLink>
  <RadixThemesLink asChild={true}>
  <NextLink css={{"isExternal": true}} href={`http://localhost:5000/api/export_csv/${state__state.selected_table}`} passHref={true}>
  <RadixThemesButton color={`teal`} disabled={((state__state.selected_table) === (""))} size={`3`} variant={`outline`}>
  <LucideFileTextIcon css={{"color": "var(--current-color)"}}>
  {`file-text`}
</LucideFileTextIcon>
  {`Tabla Actual (.csv)`}
</RadixThemesButton>
</NextLink>
</RadixThemesLink>
</RadixThemesFlex>
  <RadixThemesText as={`p`} color={`gray`} size={`2`}>
  {`Asegúrate de haber seleccionado una tabla en la pestaña Estructura antes de exportar a CSV.`}
</RadixThemesText>
  <RadixThemesSeparator css={{"marginTop": "2em", "marginBottom": "2em"}} size={`4`}/>
  <RadixThemesHeading size={`5`} weight={`bold`}>
  {`Importar Datos`}
</RadixThemesHeading>
  <RadixThemesText as={`p`} color={`gray`} size={`2`}>
  {`Sube un archivo .sql para restaurar, o un archivo .csv para volcar datos.`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%", "maxWidth": "400px"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_import_target_table", {value:_e0.target.value})], (_e0), {})} placeholder={`Nombre de tabla destino (solo requerido si subes un .csv)`} size={`3`} value={state__state.import_target_table}/>
  <ReactDropzone accept={{"text/csv": [".csv"], "application/sql": [".sql"]}} id={`db_upload`} multiple={false} onDrop={e => setFilesById(filesById => ({...filesById, db_upload: e}))} ref={ref_db_upload}>
  {({ getRootProps, getInputProps }) => (
    <Box id={`db_upload`} ref={ref_db_upload} sx={{"border": "2px dashed var(--gray-6)", "borderRadius": "xl", "padding": "3em", "width": "100%", "cursor": "pointer", "_hover": {"background": "var(--gray-3)"}}} {...getRootProps()}>
    <Input type={`file`} {...getInputProps()}/>
    <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "column"}} gap={`2`}>
    <LucideUploadIcon css={{"color": "var(--gray-9)"}} size={32}>
    {`upload`}
  </LucideUploadIcon>
    <RadixThemesText as={`p`} size={`3`} weight={`bold`}>
    {`Selecciona el archivo o arrástralo aquí`}
  </RadixThemesText>
    <RadixThemesText as={`p`} css={{"color": "var(--gray-9)"}} size={`2`}>
    {`Soporta .sql y .csv`}
  </RadixThemesText>
  </RadixThemesFlex>
  </Box>
  )}
</ReactDropzone>
  <RadixThemesButton color={`orange`} css={{"isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.handle_upload", {files:filesById.db_upload,upload_id:`db_upload`}, "uploadFiles")], (_e), {})} size={`3`}>
  {`⬆ Subir e Importar`}
</RadixThemesButton>
  <Fragment>
  {isTrue(state__state.import_message) ? (
  <Fragment>
  <RadixThemesCallout.Root color={state__state.import_message_color} css={{"icon": "info", "width": "100%"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.import_message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesTabs.Content>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Fragment>
  {isTrue(((state__state.app_role) === ("admin"))) ? (
  <Fragment>
  <RadixThemesTabs.Content value={`users`}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "alignItems": "start", "flexDirection": "column"}} gap={`2`}>
  <RadixThemesHeading size={`5`} weight={`bold`}>
  {`Gestión de Usuarios`}
</RadixThemesHeading>
  <RadixThemesText as={`p`} color={`gray`} size={`2`}>
  {`Crea usuarios de la App asignándoles acceso seguro a MariaDB.`}
</RadixThemesText>
  <RadixThemesDialog.Root>
  <RadixThemesDialog.Trigger>
  <RadixThemesButton color={`green`} css={{"marginTop": "1em", "marginBottom": "1em"}} size={`3`}>
  <LucidePlusIcon css={{"color": "var(--current-color)"}}>
  {`plus`}
</LucidePlusIcon>
  {`Nuevo Usuario`}
</RadixThemesButton>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"maxWidth": "450px"}}>
  <RadixThemesDialog.Title>
  {`Añadir Usuario`}
</RadixThemesDialog.Title>
  <RadixThemesFlex align={`start`} css={{"flexDirection": "column"}} gap={`2`}>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_name", {value:_e0.target.value})], (_e0), {})} placeholder={`Nombre de Usuario Web`} value={state__state.new_u_name}/>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_pass", {value:_e0.target.value})], (_e0), {})} placeholder={`Contraseña Web`} type={`password`} value={state__state.new_u_pass}/>
  <RadixThemesSelect.Root onValueChange={(_e0) => addEvents([Event("state.state.set_new_u_role", {value:_e0})], (_e0), {})} value={state__state.new_u_role}>
  <RadixThemesSelect.Trigger/>
  <RadixThemesSelect.Content>
  <RadixThemesSelect.Group>
  {``}
  <RadixThemesSelect.Item value={`user`}>
  {`user`}
</RadixThemesSelect.Item>
  <RadixThemesSelect.Item value={`admin`}>
  {`admin`}
</RadixThemesSelect.Item>
</RadixThemesSelect.Group>
</RadixThemesSelect.Content>
</RadixThemesSelect.Root>
  <Fragment>
  {isTrue(((state__state.new_u_role) === ("user"))) ? (
  <Fragment>
  <RadixThemesFlex align={`start`} css={{"flexDirection": "column"}} gap={`2`}>
  <RadixThemesText as={`p`} css={{"marginTop": "1em"}} size={`1`} weight={`bold`}>
  {`Conexión Auto-Asignada de MariaDB:`}
</RadixThemesText>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_host", {value:_e0.target.value})], (_e0), {})} placeholder={`Host (ej. localhost)`} value={state__state.new_u_host}/>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_port", {value:_e0.target.value})], (_e0), {})} placeholder={`Port (ej. 3307)`} value={state__state.new_u_port}/>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_muser", {value:_e0.target.value})], (_e0), {})} placeholder={`Usuario MariaDB`} value={state__state.new_u_muser}/>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_mpass", {value:_e0.target.value})], (_e0), {})} placeholder={`Contraseña MariaDB`} type={`password`} value={state__state.new_u_mpass}/>
  <DebounceInput debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_u_db", {value:_e0.target.value})], (_e0), {})} placeholder={`Base de Datos`} value={state__state.new_u_db}/>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <Fragment>
  {isTrue(state__state.new_u_msg) ? (
  <Fragment>
  <RadixThemesCallout.Root css={{"icon": "info"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.new_u_msg}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "marginTop": "1em", "flexDirection": "row"}} justify={`between`} gap={`2`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} variant={`soft`}>
  {`Cerrar`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <RadixThemesButton color={`green`} css={{"isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.create_app_user", {})], (_e), {})}>
  {`Crear Creadencial`}
</RadixThemesButton>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
  <RadixThemesTable.Root css={{"width": "100%"}} variant={`surface`}>
  <RadixThemesTable.Header>
  <RadixThemesTable.Row>
  <RadixThemesTable.ColumnHeaderCell>
  {`ID`}
</RadixThemesTable.ColumnHeaderCell>
  <RadixThemesTable.ColumnHeaderCell>
  {`Usuario`}
</RadixThemesTable.ColumnHeaderCell>
  <RadixThemesTable.ColumnHeaderCell>
  {`Rol`}
</RadixThemesTable.ColumnHeaderCell>
  <RadixThemesTable.ColumnHeaderCell>
  {`DB Base`}
</RadixThemesTable.ColumnHeaderCell>
  <RadixThemesTable.ColumnHeaderCell>
  {`Acción`}
</RadixThemesTable.ColumnHeaderCell>
</RadixThemesTable.Row>
</RadixThemesTable.Header>
  <RadixThemesTable.Body>
  {state__state.app_users_list.map((u, index_3951c4dad12863ffe930daab5a945232) => (
  <RadixThemesTable.Row key={index_3951c4dad12863ffe930daab5a945232}>
  <RadixThemesTable.Cell>
  {u["id"]}
</RadixThemesTable.Cell>
  <RadixThemesTable.Cell>
  {u["username"]}
</RadixThemesTable.Cell>
  <RadixThemesTable.Cell>
  {u["role"]}
</RadixThemesTable.Cell>
  <RadixThemesTable.Cell>
  {u["maria_db"]}
</RadixThemesTable.Cell>
  <RadixThemesTable.Cell>
  <RadixThemesButton color={`red`} onClick={(_e) => addEvents([Event("state.state.delete_app_user", {uid:u["id"]})], (_e), {})} size={`1`} variant={`ghost`}>
  <LucideTrashIcon css={{"color": "var(--current-color)"}} size={16}>
  {`trash`}
</LucideTrashIcon>
</RadixThemesButton>
</RadixThemesTable.Cell>
</RadixThemesTable.Row>
))}
</RadixThemesTable.Body>
</RadixThemesTable.Root>
</RadixThemesFlex>
</RadixThemesTabs.Content>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesTabs.Root>
</RadixThemesCard>
</RadixThemesContainer>
</RadixThemesBox>
</Fragment>
) : (
  <Fragment>
  <RadixThemesFlex css={{"minHeight": "100vh", "width": "100vw", "background": "var(--gray-2)", "display": "flex", "alignItems": "center", "justifyContent": "center"}}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "column"}} gap={`4`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "row"}} gap={`4`}>
  <LucideDatabaseIcon css={{"color": "var(--accent-9)"}} size={48}>
  {`database`}
</LucideDatabaseIcon>
  <RadixThemesHeading align={`center`} size={`9`}>
  {`Gestor de MariaDB`}
</RadixThemesHeading>
</RadixThemesFlex>
  <RadixThemesText align={`center`} as={`p`} color={`gray`} size={`4`}>
  {`Administración de bases de datos elegante y veloz`}
</RadixThemesText>
  <RadixThemesBox css={{"height": "1em"}}/>
  <RadixThemesCard css={{"width": "450px", "boxShadow": "lg"}} size={`4`}>
  <RadixThemesFlex align={`start`} css={{"width": "100%", "alignItems": "stretch", "flexDirection": "column"}} gap={`3`}>
  <RadixThemesHeading size={`5`} weight={`bold`}>
  {`Conexión Manual`}
</RadixThemesHeading>
  <RadixThemesText as={`p`} color={`gray`} size={`2`}>
  {`Ingresa las credenciales de tu servidor`}
</RadixThemesText>
  <RadixThemesBox css={{"height": "0.5em"}}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Host`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_host", {value:_e0.target.value})], (_e0), {})} placeholder={`Ej. localhost`} size={`3`} value={state__state.host}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Puerto`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_port", {value:_e0.target.value})], (_e0), {})} placeholder={`Ej. 3306`} size={`3`} value={state__state.port}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Usuario`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_user", {value:_e0.target.value})], (_e0), {})} placeholder={`Ej. root`} size={`3`} value={state__state.user}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Contraseña`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_password", {value:_e0.target.value})], (_e0), {})} placeholder={`Tu contraseña`} size={`3`} type={`password`} value={state__state.password}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Base de Datos`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_database", {value:_e0.target.value})], (_e0), {})} placeholder={`(Opcional) Vacío para servidor raíz`} size={`3`} value={state__state.database}/>
  <RadixThemesBox css={{"height": "0.5em"}}/>
  <RadixThemesButton color={`indigo`} css={{"isLoading": state__state.loading, "width": "100%"}} onClick={(_e) => addEvents([Event("state.state.connect_db", {})], (_e), {})} size={`3`}>
  <LucideZapIcon css={{"color": "var(--current-color)"}}>
  {`zap`}
</LucideZapIcon>
  {`Conectar al Servidor`}
</RadixThemesButton>
  <RadixThemesDialog.Root>
  <RadixThemesDialog.Trigger>
  <RadixThemesButton color={`gray`} css={{"width": "100%"}} size={`3`} variant={`soft`}>
  <LucidePlusIcon css={{"color": "var(--current-color)"}}>
  {`plus`}
</LucidePlusIcon>
  {`Crear Nueva Base de Datos`}
</RadixThemesButton>
</RadixThemesDialog.Trigger>
  <RadixThemesDialog.Content css={{"maxWidth": "400px"}}>
  <RadixThemesDialog.Title>
  {`Crear Base de Datos desde Cero`}
</RadixThemesDialog.Title>
  <RadixThemesDialog.Description>
  {`Ingresa el nombre de la nueva base de datos. Una vez creada, te conectaremos directamente a ella.`}
</RadixThemesDialog.Description>
  <RadixThemesFlex align={`start`} css={{"flexDirection": "column"}} gap={`2`}>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_new_db_name", {value:_e0.target.value})], (_e0), {})} placeholder={`Ejemplo: mi_nuevo_sistema`} size={`3`} value={state__state.new_db_name}/>
  <Fragment>
  {isTrue(state__state.create_db_message) ? (
  <Fragment>
  <RadixThemesCallout.Root color={state__state.create_db_message_color} css={{"icon": "info", "width": "100%"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.create_db_message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  <RadixThemesFlex align={`start`} css={{"marginTop": "1em", "width": "100%", "flexDirection": "row"}} justify={`between`} gap={`2`}>
  <RadixThemesDialog.Close>
  <RadixThemesButton color={`gray`} size={`3`} variant={`soft`}>
  {`Cancelar`}
</RadixThemesButton>
</RadixThemesDialog.Close>
  <RadixThemesButton color={`green`} css={{"isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.create_database", {})], (_e), {})} size={`3`}>
  {`Crear y Conectar`}
</RadixThemesButton>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
  <Fragment>
  {isTrue(state__state.message) ? (
  <Fragment>
  <RadixThemesCallout.Root color={state__state.message_color} css={{"icon": "info", "width": "100%"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesCard>
</RadixThemesFlex>
</RadixThemesFlex>
</Fragment>
)}
</Fragment>
) : (
  <Fragment>
  <RadixThemesFlex css={{"minHeight": "100vh", "width": "100vw", "background": "var(--gray-2)", "display": "flex", "alignItems": "center", "justifyContent": "center"}}>
  <RadixThemesCard css={{"width": "400px", "boxShadow": "lg"}} size={`4`}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "start", "flexDirection": "column"}} gap={`3`}>
  <RadixThemesFlex css={{"width": "100%", "display": "flex", "alignItems": "center", "justifyContent": "center"}}>
  <RadixThemesFlex align={`start`} css={{"alignItems": "center", "flexDirection": "column"}} gap={`2`}>
  <LucideUsersIcon css={{"color": "var(--accent-9)"}} size={48}>
  {`users`}
</LucideUsersIcon>
  <RadixThemesHeading size={`7`}>
  {`Acceso al Manager`}
</RadixThemesHeading>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesText align={`center`} as={`p`} color={`gray`} size={`2`}>
  {`Inicia sesión para administrar MariaDB`}
</RadixThemesText>
  <RadixThemesBox css={{"height": "1em"}}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Usuario`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_app_username", {value:_e0.target.value})], (_e0), {})} placeholder={`Añade tu cuenta web`} size={`3`} value={state__state.app_username}/>
  <RadixThemesText as={`p`} size={`2`} weight={`bold`}>
  {`Contraseña`}
</RadixThemesText>
  <DebounceInput css={{"width": "100%"}} debounceTimeout={300} element={RadixThemesTextField.Input} onChange={(_e0) => addEvents([Event("state.state.set_app_password", {value:_e0.target.value})], (_e0), {})} placeholder={`Tu clave secreta`} size={`3`} type={`password`} value={state__state.app_password}/>
  <RadixThemesBox css={{"height": "0.5em"}}/>
  <RadixThemesButton color={`indigo`} css={{"width": "100%", "isLoading": state__state.loading}} onClick={(_e) => addEvents([Event("state.state.do_app_login", {})], (_e), {})} size={`3`}>
  {`Ingresar`}
</RadixThemesButton>
  <Fragment>
  {isTrue(state__state.app_login_message) ? (
  <Fragment>
  <RadixThemesCallout.Root color={`red`} css={{"icon": "info", "width": "100%"}}>
  <RadixThemesCallout.Icon>
  <LucideInfoIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text>
  {state__state.app_login_message}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
</RadixThemesFlex>
</RadixThemesCard>
</RadixThemesFlex>
</Fragment>
)}
</Fragment>
  )
}

export default function Component() {

  return (
    <Fragment>
  <Fragment_1762bb90abdb81b879b2a22edbbe01a1/>
  <Fragment_451db3e26a917de9fd2d6ad75e6bb897/>
  <NextHead>
  <title>
  {`MariaDB Manager`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
