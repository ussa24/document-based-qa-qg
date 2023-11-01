

import React, { useEffect, useState } from 'react';
import { Button, ButtonGroup, Form } from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import { addInpc, deleteInpc, loadSingleInpc, loadInpcs, updateInpc } from './redux/actions';
import { ToastContainer, toast } from 'react-toastify';
import axios from 'axios'; // Import Axios


const Dashboard = () => {
  const initialState = {
    name: '',
    description: '',
    category: '',
  };

  const [state, setState] = useState(initialState);
  const [editMode, setEditMode] = useState(false);
  const [inpcId, setInpcId] = useState(null);

  const [categories, setCategories] = useState([]);

  useEffect(() => {
    // Fetch categories from backend
    fetch("/categories")
      .then(response => response.json())
      .then(data => setCategories(data))
      .catch(error => console.error("Error fetching categories:", error));
  }, []);

  const dispatch = useDispatch();
  const { inpcs, msg, inpc} = useSelector((state) => state.data);

  const { name, description, category } = state;

  const handleChange = (e) => {
    let { name, value } = e.target;
    setState({ ...state, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!name || !description) {
      toast.error("Please fill all inputs");
    } else {
      const formData = new FormData();
      formData.append("name", name);
      formData.append("description", description);
      formData.append("category", category);
      formData.append("filePdf", state.filePdf); // Append the file here
  
      if (!editMode) {
        dispatch(addInpc(formData));
      } else {
        dispatch(updateInpc(formData, inpcId));
        setEditMode(false);
        setInpcId(null);
      }
  
      setState({
        name: "",
        description: "",
        category: "",
        filePdf: null, // Reset the file input after submission
      });
    }
  };
  

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this document? ")) {
      dispatch(deleteInpc(id));
    }
  };

  const handleUpdate = (id) => {
      dispatch(loadSingleInpc(id));
      setInpcId(id);
      setEditMode(true);
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setState({ ...state, filePdf: file });
  };
  


  useEffect(() => {
    if (msg) {
      toast.success(msg);
    }
  }, [msg]);

  useEffect(() => {
    dispatch(loadInpcs());
  }, []); // Add dispatch to the dependency array

  useEffect(() => {
    if (inpc) {
      setState({...inpc})
    }
  }, [inpc]);

  const handleValidateClick = () => {
    // Make an HTTP GET request to the FastAPI endpoint
    axios.get('http://127.0.0.1:8000/validate_all')
      .then(response => {
        // Handle the response here (e.g., show a message)
        console.log('Validation response:', response.data);
      })
      .catch(error => {
        // Handle any errors here
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <div class="container">
  <div class="row">

    <div class="col-md-4">
      <h3>ADD FILE</h3>
      <Form onSubmit={handleSubmit}>
                <Form.Group>
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                    type="text"
                    placeholder="name"
                    name="name"
                    value={name || ""}
                    onChange={handleChange}
                    />
                </Form.Group>
                <Form.Group>
                    <Form.Label>description</Form.Label>
                    <Form.Control
                    type="text"
                    placeholder="description"
                    name="description"
                    value={description || ""}
                    onChange={handleChange}
                    />
                </Form.Group>
                <Form.Group>
  <Form.Label>File</Form.Label>
  <Form.Control
    type="file"
    name="filePdf"
    accept=".pdf"
    onChange={handleFileChange}
  />
</Form.Group>
<Form.Group>
        <Form.Label>Category</Form.Label>
        <Form.Control
    as="select"
    name="category" // Change to the appropriate field name
    value={category || ""}
    onChange={handleChange}
  >
          <option value="">Select a category</option>
          {categories.map(category => (
            <option key={category.name} value={category.name}>
              {category.name}
            </option>
          ))}
        </Form.Control>
      </Form.Group>
                <div className="d-grid gap-2 mt-2">
                    <Button type="submit" variant="primary" size="lg">
                        {editMode ? "Update" : "Submit"}
                    </Button>
                </div>
    
         </Form>
         <br></br><br></br><br></br>
        <center><img src="https://cdn-icons-png.flaticon.com/512/10466/10466000.png" width="100" height="100" /></center>
         <ButtonGroup>
           <Button variant="warning" onClick={handleValidateClick}>
               Calculate scores
              </Button>
          </ButtonGroup>
    </div>
    <div class="col-md-8">
      <h3>FILES</h3>
      <table id="userTable" class="table table-striped">
                    <tr>
                        <th>NO.</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>file</th>
                        <th>file</th>

                        <th>Action</th>
                    </tr>
                    {inpcs && inpcs.map((item, index) =>(
                        <tbody key={index}>
                                <tr>
                                    <td>{index+1}</td>
                                    <td>{item.name}</td>
                                    <td>{item.description}</td>
                                    <td>{item.category}</td>

                                    <td>{item.filePdf}</td>

                                    <td>
                                        <ButtonGroup>
                                                <Button style={{marginRight: "5px"}}
                                                 variant="danger"
                                                 onClick={() => handleDelete(item._id)}
                                                >
                                                Delete
                                            </Button>
                                            <Button variant="secondary"
                                            onClick={() => handleUpdate(item._id)}>
                                                Update
                                            </Button>
                                        </ButtonGroup>
                                    </td>
                                    </tr>
    
                     </tbody>
                          ))}
      </table>
    </div>
  </div>
</div>
    </div>
    
        );
        };

export default Dashboard;
