import { combineReducers } from "@reduxjs/toolkit";
import websocketReducer from "./websocketSlice";
import batchReducer from "./batchSlice";

const rootReducer = combineReducers({
  websocket: websocketReducer,
  batch: batchReducer,
});

export default rootReducer;
