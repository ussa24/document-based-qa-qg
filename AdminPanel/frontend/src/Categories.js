

import React, { useEffect, useState } from 'react';
import { Button, ButtonGroup, Form } from 'react-bootstrap';


const Categories = () => {
    const [categories, setCategories] = useState([]);
    const [name, setName] = useState("");
  
    const fetchCategories = async () => {
      const response = await fetch("/categories");
      const data = await response.json();
      setCategories(data);
    };
  



  useEffect(() => {
    fetchCategories();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (name) {
      await fetch("/categories", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name }),
      });
      setName("");
      fetchCategories();
    }
  };

  const handleDelete = (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this category?");
    if (confirmDelete) {
      fetch(`/categories/${id}`, {
        method: "DELETE",
      })
        .then(() => fetchCategories()) // Fetch the updated list of categories after deletion
        .catch((error) => console.error("Error deleting category:", error));
    }
  };


  const handleGenerateClick = async (categoryName) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/generate_questions_all_pdfs/${categoryName}`);
      if (response.ok) {
        // Handle success, e.g., show a success message or perform other actions.
      } else {
        // Handle error, e.g., show an error message.
      }
    } catch (error) {
      console.error('Error:', error);
      // Handle network or other errors.
    }
  };

  return (
<div>
<div class="container">
    <div class="row">
        <div class="col-md-4">
        <h3>ADD CATEGORY</h3>
            <Form onSubmit={handleSubmit}>
                    <Form.Group>
                        <Form.Label>Name</Form.Label>
                        <Form.Control
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="Enter category name"
                        />
                    </Form.Group>
                    <div className="d-grid gap-2 mt-2">
                        <Button type="submit" >
                        Add Category              
                        </Button>
                    </div>
            </Form>
        </div>
    <div class="col-md-8">
        <h3>CATEGORIES</h3>
            <table id="userTable" class="table table-striped">
                        <tr>
                            <th>NO.</th>
                            <th>Name</th>
                            <th>Action</th>
                        </tr>
                        {categories.map((category, index) =>(
                            <tbody key={index}>
                                    <tr>
                                        <td>{index+1}</td>
                                        <td>{category.name}</td>
                                        <td>
                                            <ButtonGroup>
                                                    <Button style={{marginRight: "5px"}}
                                                    variant="danger"
                                                    onClick={() => handleDelete(category.id)}                                          >
                                                    Delete
                                                </Button>
                                            </ButtonGroup>
                                            <ButtonGroup>
                                              <Button
                                                variant="info"
                                                onClick={() => handleGenerateClick(category.name)}
                                              >
                                                Generate
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
}
export default Categories;
