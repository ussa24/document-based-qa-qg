import * as types from "./actionTypes";

const initialState = {
    inpcs: [],
    inpc: {},
    msg: "",
    };
    const inpcReducer = (state = initialState, action) => {
    switch (action.type) {
        case types.GET_INPCS:
            return{
                ...state,
                inpcs: action.payload,
            };
        case types.ADD_INPCS:
            case 'DELETE_INPC_SUCCESS':
                return {
                  ...state,
                  inpcs: state.inpcs.filter(item => item._id !== action.payload),
                  msg: 'Document deleted successfully.',
                };
        case types.UPDATE_INPCS:
            return{
                ...state,
                msg: action.payload,
            };
        case types.GET_SINGLE_INPC:
            return{
                ...state,
                inpc: action.payload,
            };
         default:
            return state;
    }
    };
    export default inpcReducer;