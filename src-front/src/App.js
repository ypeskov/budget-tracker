import Container from 'react-bootstrap/Container';

import 'bootstrap/dist/css/bootstrap.min.css';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import './App.css';
import Login from './Components/Login';

function App() {
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
        <Col>
          <Login />
        </Col>
        <Col>
          <Login />
        </Col>
      </Row>
    </Container>
    </div>
  );
}

export default App;
