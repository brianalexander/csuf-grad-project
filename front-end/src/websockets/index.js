import store from "../redux/store";
import { setStatus } from "../redux/websocketSlice";
import { updateBatch } from "../redux/batchSlice";

const registerWebSockets = (connectionURI = "ws://localhost:8080") => {
  socket = new WebSocket(connectionURI);

  socket.onopen = function (evt) {
    console.log(`Successfully connected to ${connectionURI}`);
    store.dispatch(setStatus(WebSocket.OPEN));
  };

  socket.onclose = function (evt) {
    console.log(`Disconnected.`);
    store.dispatch(setStatus(WebSocket.CLOSED));
  };

  socket.onmessage = ({ data: message }) => {
    const { type, payload } = JSON.parse(message);
    // console.log(type, payload);
    switch (type) {
      case "ping":
        // console.log("websocket", "ping", payload);
        break;
      case "getBatchResponse":
        console.log("websocket", "getBatchResponse", payload);
        store.dispatch(updateBatch(payload));
        break;
      default:
        break;
    }
  };
};

export let socket;
export default registerWebSockets;
