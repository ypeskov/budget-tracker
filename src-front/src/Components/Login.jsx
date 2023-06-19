import { useContext, useState } from 'react';
import { useNavigate, } from 'react-router-dom';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

import { UserContext } from '../Context/AppContext';

const apiDomain = `${process.env.REACT_APP_API_URL}`;

function Login() {
  const {updateUser} = useContext(UserContext);
  const navigate = useNavigate();

  async function tryLogin(event) {
    event.preventDefault();

    try {
      const response = await fetch(`${apiDomain}/auth/login`, {
        'method': 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        'body': JSON.stringify({
          email: email,
          password: password,
        })
      });
      const data = await response.json();
      if (data.access_token) {
        updateUser({
          isLoggedIn: true,
          accessToken: data.access_token,
        });

        navigate('/dashboard');
      }
    } catch(err) {
      console.log(err);
    }
  };

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const processEmailChange = (event) => {
    setEmail(event.target.value);
  }

  const processPasswordChange = (event) => {
    setPassword(event.target.value);
  }

  return (
    <div>
      <Form onSubmit={tryLogin}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" 
                        placeholder="Enter email" 
                        value={email} 
                        onChange={processEmailChange} />
          <Form.Text className="text-muted">
            Enter your registered email
          </Form.Text>
        </Form.Group>
  
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" 
                        placeholder="Password" 
                        value={password}
                        onChange={processPasswordChange} />
        </Form.Group>
        {/* <Form.Group className="mb-3" controlId="formBasicCheckbox">
          <Form.Check type="checkbox" label="Check me out" />
        </Form.Group> */}
        <Button variant="primary" type="submit">
          Login
        </Button>
      </Form>
    </div>
  );
}

export default Login;