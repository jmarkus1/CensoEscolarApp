import { Carousel } from 'react-bootstrap';
import './Carrossel.css';

const Carrossel = ({ itensCarrossel }) => {
  return (
    <Carousel>
      {itensCarrossel.map(({ srcImagem, titulo, descricao }, i) => {
        return (
          <Carousel.Item key={i}>
            <img className="carousel-img" src={srcImagem} />
            <Carousel.Caption>
              <h3>{titulo}</h3>
              <p>{descricao}</p>
            </Carousel.Caption>
          </Carousel.Item>
        );
      })}
    </Carousel>
  );
};

export default Carrossel;
