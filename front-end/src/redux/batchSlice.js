// Redux Imports
import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getBatchForModerator, sendResultForItemByModerator } from "../api";

// Toast Imports
import { toast } from "react-toastify";

// First, create the thunk
export const fetchBatchForModerator = createAsyncThunk(
  "batch/fetchByModeratorId",
  async (moderatorId, thunkAPI) => {
    const data = await getBatchForModerator(moderatorId);
    console.log(data);
    const state = thunkAPI.getState();
    console.log("state", state.batch.fetchStatus);
    console.log("timeToWait", "timeToWait" in data);

    const timeout_function = () => {
      console.log("TIMEOUT EXECUTED");
      thunkAPI.dispatch(fetchBatchForModerator(moderatorId));
    };

    if ("timeToWait" in data) {
      console.log("setting timeout for", data.timeToWait);
      setTimeout(timeout_function, data.timeToWait);
    }
    return data;
  }
);

export const returnResultForItemByModerator = createAsyncThunk(
  "batch/returnResultForItemByModerator",
  async ({ itemId, moderatorId, flagged, tags }, thunkAPI) => {
    const statusCode = await sendResultForItemByModerator(
      itemId,
      moderatorId,
      flagged,
      tags
    );

    console.log("status code", statusCode);
    if (statusCode === 200) {
      toast.dark(
        `Item ${itemId} ${flagged ? "accepted" : "rejected"} successfully!`,
        {
          position: "top-right",
          autoClose: 2000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
        }
      );
    }

    return statusCode;
  }
);

let initialState = {
  firstLoad: true,
  fetchStatus: "idle",
  batch: [
    {
      id: "INITIAL",
      text: "Loading...",
      bin: "high",
      scores: [
        { text: "Loading", value: 0 },
        { text: "Loading", value: 0 },
        { text: "Loading", value: 0 },
      ],
      tags: [],
      similarItems: [
        {
          text: "Loading...",
          tags: [],
          flagged: false,
        },
        {
          text: "Loading...",
          tags: [],
          flagged: false,
        },
        {
          text: "Loading...",
          tags: [],
          flagged: false,
        },
        {
          text: "Loading...",
          tags: [],
          flagged: false,
        },
      ],
    },
  ],
};

const batchSlice = createSlice({
  name: "batch",
  initialState,
  reducers: {
    // updateBatch: (state, action) => {
    //   console.log("update batch");
    //   const newBatch = action.payload.map((row) => {
    //     return JSON.parse(row);
    //   });
    //   const ids = new Set(state.batch.map((item) => item.id));
    //   let batch;
    //   if (state.firstLoad) {
    //     state.firstLoad = false;
    //     batch = [...newBatch];
    //   } else {
    //     batch = [
    //       ...state.batch,
    //       ...newBatch.filter((item) => !ids.has(item.id)),
    //     ];
    //   }

    //   state.batch = batch;
    //   state.firstLoad = false;
    //   console.log("newBatch", state.batch);
    // },
    removeItem: (state, action) => {
      console.log(action.payload);
      const { id } = action.payload;
      const batch = state.batch.filter((item) => {
        return item.id !== id;
      });

      state.batch = batch;
    },
  },
  extraReducers: {
    [fetchBatchForModerator.pending]: (state, action) => {},
    [fetchBatchForModerator.fulfilled]: (state, action) => {
      console.log("original payload", action.payload);

      if ("timeToWait" in action.payload) {
        state.fetchStatus = "wait";
      }

      if ("items" in action.payload) {
        state.fetchStatus = "idle";
        if (state.firstLoad) {
          state.firstLoad = false;
          state.batch.pop();
        }

        const { items } = action.payload;
        console.log("ITEMS", items);
        const restructedItems = items.map((value, index) => {
          return { ...value["_source"], id: value["_id"] };
        });
        console.log("restruct items", restructedItems);

        for (const item of restructedItems) {
          console.log(item);
          state.batch.push(item);
        }

        toast.success("New items received.");
      }
    },
    [fetchBatchForModerator.rejected]: (state, action) => {},
    [returnResultForItemByModerator.pending]: (state, action) => {},
    [returnResultForItemByModerator.fulfilled]: (state, action) => {
      console.log(action.payload);
    },
    [returnResultForItemByModerator.rejected]: (state, action) => {},
  },
});

export const { removeItem, updateBatch } = batchSlice.actions;
export default batchSlice.reducer;
