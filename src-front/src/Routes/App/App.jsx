import { useContext, useEffect } from 'react';
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.min.css';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import './App.css';

import { UserContext } from '../../Context/AppContext';

export function loader() {
  return [];
}

function App() {
  const navigate = useNavigate();
  const location = useLocation();
  const {user} = useContext(UserContext);

  useEffect(() => {
    if ( user.isLoggedIn ) {
      navigate(location.pathname);
    } else {
      navigate('/login');
    }
  }, [user.isLoggedIn]);

  return (
    <div className="App">
      <Container>
      <Row>
        <Col>
        <header className="App-header">
          Header
        </header>
        </Col>
      </Row>

      <Row>
        <Col sm={1}>
          <Row><Link to='dashboard'>Dashboard</Link></Row>
          <Row><Link>Budgets</Link></Row>
          <Row><Link to='/accounts'>Accounts</Link></Row>
        </Col>
        <Col>
          <Outlet />
        </Col>
      </Row>
    </Container>
    </div>
  );
}

export default App;
