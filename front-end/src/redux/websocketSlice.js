// Redux Imports
import { createSlice } from "@reduxjs/toolkit";

let initialState = {
  moderatorId: "",
};

const websocketSlice = createSlice({
  name: "websocket",
  initialState,
  reducers: {
    setModeratorId: (state, action) => {
      const { moderatorId } = action.payload;

      state.moderatorId = moderatorId;
    },
  },
});

export const { setModeratorId } = websocketSlice.actions;
export default websocketSlice.reducer;
