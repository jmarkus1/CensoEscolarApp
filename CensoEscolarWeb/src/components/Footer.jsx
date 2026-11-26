import { HeartIcon } from '@phosphor-icons/react';
import { Container, Row, Col, Nav } from 'react-bootstrap';
import { FaSchool } from 'react-icons/fa';

import {
  IoHomeOutline,
  IoPersonOutline,
  IoMailOutline,
  IoSchoolOutline,
} from 'react-icons/io5';

const Footer = () => {
  return (
    <footer
      className="bg-opacity-70 text-light py-4 mt-5"
      style={{ backgroundColor: '#003f69' }}
    >
      <Container>
        <Row>
          {/* Coluna esquerda */}
          <Col xs={12} md={6}>
            <FaSchool />{' '}
            <HeartIcon
              style={{ marginRight: '3px' }}
              color="#AE2983"
              weight="fill"
              size={32}
            />{' '}
            Censo Escolar
          </Col>

          {/* Coluna direita */}
          <Col xs={12} md={6}>
            <h5 className="mb-3">Links úteis</h5>

            <Nav className="flex-column">
              <Nav.Link
                href="/"
                className="text-light d-flex align-items-center gap-2 mb-2"
              >
                <IoHomeOutline size={32} />
                Home
              </Nav.Link>

              <Nav.Link
                href="/sobre"
                className="text-light d-flex align-items-center gap-2 mb-2"
              >
                <IoPersonOutline size={32} />
                Sobre
              </Nav.Link>

              <Nav.Link
                href="/contato"
                className="text-light d-flex align-items-center gap-2"
              >
                <IoMailOutline size={32} />
                Contato
              </Nav.Link>
            </Nav>
          </Col>
        </Row>

        <hr className="border-secondary my-4" />

        {/* Rodapé inferior */}
        <Row>
          <Col className="text-center">
            © {new Date().getFullYear()} Censo Escolar - IFPB - Todos os
            direitos reservados.
          </Col>
        </Row>
      </Container>
    </footer>
  );
};

export default Footer;
