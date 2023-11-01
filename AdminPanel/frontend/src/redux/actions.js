import * as types from "./actionTypes";
import axios from "axios";

const API = "http://localhost:5000"

const getInpcs = (inpcs) => ({
    type: types.GET_INPCS,
    payload: inpcs,
});

const inpcAdded = (msg) => ({
    type: types.ADD_INPCS,
    payload: msg
});
const inpcDelete = (msg) => ({
    type: types.DELETE_INPCS,
    payload: msg
});

const getInpc = (inpcs) => ({
    type: types.GET_SINGLE_INPC,
    payload: inpcs,
});
const inpcUpdate = (msg) => ({
    type: types.UPDATE_INPCS,
    payload: msg,
});

export const loadInpcs = () => {
    return function (dispatch){
        axios
            .get(`${API}/inpcs`)
            .then((resp)=> dispatch(getInpcs(resp.data)))
            .catch((err)=> console.log(err));
    };
};

export const addInpc = (inpc) => {
    return function (dispatch){
        axios
            .post(`${API}/createInpc`, inpc)
            .then((resp)=> {
                dispatch(inpcAdded(resp.data.msg));
                dispatch(loadInpcs());
            })
            
            .catch((err)=> console.log(err));
    };
};

export const deleteInpc = (id) => {
    return function (dispatch){
        axios
            .delete(`${API}/inpcs/${id}`)
            .then((resp)=> {
                dispatch(inpcDelete(resp.data.msg));
                dispatch(loadInpcs());
            })
            
            .catch((err)=> console.log(err));
    };
};

export const loadSingleInpc = (id) => {
    return function (dispatch){
        axios
            .get(`${API}/inpc/${id}`)
            .then((resp)=> {
                dispatch(getInpc(resp.data));
            })
            
            .catch((err)=> console.log(err));
    };
};

export const updateInpc = (inpc, id) => {
    return function (dispatch){
        axios
            .put(`${API}/inpcs/${id}`, inpc)
            .then((resp)=> {
                dispatch(inpcUpdate(resp.data.msg));
                dispatch(loadInpcs());
            })
            
            .catch((err)=> console.log(err));
    };
};

export const loadCategories = () => {
    return async (dispatch) => {
      try {
        const response = await axios.get('/categories'); // Update with your API endpoint
        const categories = response.data;
        return categories;
      } catch (error) {
        throw error;
      }
    };
  };