import { combineReducers } from "redux";
import inpcReducer from "./reducer";
const rootReducer = combineReducers({
data: inpcReducer,
});
export default rootReducer;