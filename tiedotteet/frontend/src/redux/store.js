import { createStore, applyMiddleware } from "redux";
import { createLogger } from "redux-logger";
import { createBrowserHistory } from "history";
import thunkMiddleware from "redux-thunk";
import rootReducer from "./reducer";

export const history = createBrowserHistory();

const loggerMiddleware = createLogger();
let middlewares = [thunkMiddleware];

if (process.env.NODE_ENV === "development") {
  middlewares = [...middlewares, loggerMiddleware];
}

const store = createStore(rootReducer, applyMiddleware(...middlewares));

export default store;
