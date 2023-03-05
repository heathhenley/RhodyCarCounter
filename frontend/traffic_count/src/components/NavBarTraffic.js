import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import { Link } from "react-router-dom";


function NavBarTraffic() {
  return (
    <Navbar bg="light" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Rhody Car Counter</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Table</Nav.Link>
            <Nav.Link as={Link} to="/map">Map</Nav.Link>
            <Nav.Link href="https://rhodycarcounter-production.up.railway.app/docs">API</Nav.Link>
            <Nav.Link href="https://github.com/heathhenley/RhodyCarCounter">GitHub</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>);
}

export default NavBarTraffic;