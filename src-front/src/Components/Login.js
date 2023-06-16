import React, { useContext, useEffect } from 'react';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import { UserContext } from '../Context/AppContext';

const apiDomain = `${process.env.REACT_APP_API_URL}`;

function Login() {
  const {user, updateUser} = useContext(UserContext);

  async function tryLogin(event) {
    event.preventDefault();

    const emailLogin = 'user1@example.com';
    const passwordLogin = 'qqqqqq';

    try {
      const response = await fetch(`${apiDomain}/auth/login`, {
        'method': 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        'body': JSON.stringify({
          email: emailLogin,
          password: passwordLogin,
        })
      });
      const data = await response.json();
      console.log(data);
    } catch(err) {
      console.log(err);
    }
  };

  return (
    <div>
      { user.isLoggedIn ? 
      (
        <span>{JSON.stringify(user, null, 4)}</span>
      ) :
      (
        <Form onSubmit={tryLogin}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email" />
            <Form.Text className="text-muted">
              Enter your registered email
            </Form.Text>
          </Form.Group>
    
          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Password" />
          </Form.Group>
          {/* <Form.Group className="mb-3" controlId="formBasicCheckbox">
            <Form.Check type="checkbox" label="Check me out" />
          </Form.Group> */}
          <Button variant="primary" type="submit">
            Login
          </Button>
        </Form>
      )
    }
    </div>
  );
}

export default Login;