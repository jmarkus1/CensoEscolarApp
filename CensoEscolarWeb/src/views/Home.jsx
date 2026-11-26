import { Button, Card, Col, Container, Row } from 'react-bootstrap';
import Carrossel from '../components/Carrossel';

const Home = () => {
  let itensCarrossel = [
    {
      srcImagem:
        'https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=1471&auto=format&fit=crop',
      titulo: 'Censo Escolar Paraíba 2025',
      descricao:
        'Panorama estatístico completo da educação básica nas escolas públicas e privadas do estado da Paraíba.',
    },
    {
      srcImagem:
        'https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=1631&auto=format&fit=crop',
      titulo: 'Ranking de Instituições',
      descricao: 'Consulta detalhada das 10 maiores Instituições de Ensino da Paraíba em número de matrículas.',
    },
  ];

  return (
    <>
      {/* Carrossel */}
      <Carrossel itensCarrossel={itensCarrossel}></Carrossel>

      {/* Cards de Informação */}
      <Container className="mt-4 mb-4">
        <Row>
          <Col md={4} className="mb-3">
            <Card className="h-100 shadow-sm">
              <Card.Img
                variant="top"
                src="https://images.unsplash.com/photo-1588072432836-e10032774350?q=80&w=1172&auto=format&fit=crop"
              />
              <Card.Body className="d-flex flex-column">
                <Card.Title>Ranking Top 10 IEs</Card.Title>
                <Card.Text>
                  Lista ordenada das 10 maiores instituições de ensino da Paraíba com base no total de matrículas (qt_mat_bas).
                </Card.Text>
                <Button variant="primary" className="mt-auto">Ver Ranking</Button>
              </Card.Body>
            </Card>
          </Col>

          <Col md={4} className="mb-3">
            <Card className="h-100 shadow-sm">
              <Card.Img
                variant="top"
                src="https://images.unsplash.com/photo-1778489769184-45868633c527?q=80&w=1170&auto=format&fit=crop"
              />
              <Card.Body className="d-flex flex-column">
                <Card.Title>Educação Básica PB</Card.Title>
                <Card.Text>
                  Dados detalhados por etapas: Educação Infantil, Ensino Fundamental, Médio, Profissional e EJA.
                </Card.Text>
                <Button variant="primary" className="mt-auto">Saiba Mais</Button>
              </Card.Body>
            </Card>
          </Col>

          <Col md={4} className="mb-3">
            <Card className="h-100 shadow-sm">
              <Card.Img
                variant="top"
                src="https://plus.unsplash.com/premium_photo-1661688307556-61310f23a42c?q=80&w=1332&auto=format&fit=crop"
              />
              <Card.Body className="d-flex flex-column">
                <Card.Title>Divisão Territorial</Card.Title>
                <Card.Text>
                  Mapeamento com informações organizadas por municípios, microrregiões e mesorregiões do estado.
                </Card.Text>
                <Button variant="primary" className="mt-auto">Explorar Dados</Button>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Home;