import { createContext, useContext, useMemo, useReducer, useState } from "react"
import { applyDelta, Event, hydrateClientStorage, useEventLoop, refs } from "/utils/state.js"

export const initialState = {"state": {"is_hydrated": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}}, "state.state": {"app_logged_in": false, "app_login_message": "", "app_password": "", "app_role": "", "app_username": "", "app_users_list": [], "backend_url": "http://localhost:5000/api", "connected": false, "create_db_message": "", "create_db_message_color": "green", "create_tb_message": "", "create_tb_message_color": "green", "database": "", "host": "localhost", "import_message": "", "import_message_color": "green", "import_target_table": "", "loading": false, "message": "", "message_color": "green", "new_db_name": "", "new_tb_columns": [{"name": "id", "type": "INT AUTO_INCREMENT PRIMARY KEY"}], "new_tb_name": "", "new_u_db": "", "new_u_host": "localhost", "new_u_mpass": "", "new_u_msg": "", "new_u_muser": "root", "new_u_name": "", "new_u_pass": "", "new_u_port": "3307", "new_u_role": "user", "password": "", "port": "3307", "query_message_color": "green", "query_result_columns": [], "query_result_data": [], "query_result_message": "", "schema": "", "selected_table": "", "sql_query": "", "tables": [], "user": "root"}}

export const ColorModeContext = createContext(null);
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {
  state: createContext(null),
  state__state: createContext(null),
}
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}}

export const onLoadInternalEvent = () => [Event('state.on_load_internal')]

export const initialEvents = () => [
    Event('state.hydrate', hydrateClientStorage(clientStorage)),
    ...onLoadInternalEvent()
]

export const isDevMode = true

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return (
    <UploadFilesContext.Provider value={[filesById, setFilesById]}>
      {children}
    </UploadFilesContext.Provider>
  )
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectError] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectError]}>
      {children}
    </EventLoopContext.Provider>
  )
}

export function StateProvider({ children }) {
  const [state, dispatch_state] = useReducer(applyDelta, initialState["state"])
  const [state__state, dispatch_state__state] = useReducer(applyDelta, initialState["state.state"])
  const dispatchers = useMemo(() => {
    return {
      "state": dispatch_state,
      "state.state": dispatch_state__state,
    }
  }, [])

  return (
    <StateContexts.state.Provider value={ state }>
    <StateContexts.state__state.Provider value={ state__state }>
      <DispatchContext.Provider value={dispatchers}>
        {children}
      </DispatchContext.Provider>
    </StateContexts.state__state.Provider>
    </StateContexts.state.Provider>
  )
}