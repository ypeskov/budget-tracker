import { useContext } from 'react';
import { Link } from 'react-router-dom';

import { UserContext } from '../Context/AppContext';
import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export default function Dashborad() {
  const {user} = useContext(UserContext);

  return (
    <>
      <Container>
        <Row>
          <Col>Dashboard</Col>
        </Row>
      </Container>
    </>
  );
}