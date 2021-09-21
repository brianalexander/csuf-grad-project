import { configureStore, getDefaultMiddleware } from "@reduxjs/toolkit";
import rootReducer from "./rootReducer";

const [
  thunk,
  immutableStateInvariant,
  serializableStateInvariant,
] = getDefaultMiddleware();

const store = configureStore({
  reducer: rootReducer,
  middleware: [thunk, immutableStateInvariant, serializableStateInvariant],
});

export default store;
