import { useContext, useEffect } from 'react';
import { Link } from 'react-router-dom';

import { UserContext } from '../Context/AppContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

const apiDomain = `${process.env.REACT_APP_API_URL}`;

export default function Dashborad() {
  const {user, updateUser} = useContext(UserContext);

  async function getProfile() {
    const response = await fetch(`${apiDomain}/auth/profile`, {
      headers: {
        "auth-token": user.accessToken
      },
    });
  
    const data = await response.json();
    updateUser(data);
  }
  useEffect(() => {
    getProfile();
  }, []);
  return (
    <>
      <Container>
        <Row>Email: {user.email}</Row>
        <Row>First Name: {user.firstName}</Row>
        <Row>Last Name: {user.lastName}</Row>
      </Container>
    </>
  );
}