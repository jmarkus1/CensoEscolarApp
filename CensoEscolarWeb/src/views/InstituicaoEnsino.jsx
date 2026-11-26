import React, { useState, useEffect } from 'react';
import { Container, Table } from 'react-bootstrap';

// Importação direta do arquivo exigida pelo professor
import dadosJson from '../datasets/instituicoes.json';

const InstituicaoEnsino = () => {
  const [top10, setTop10] = useState([]);

  useEffect(() => {
    // Teste para ver se o React está a ler o ficheiro
    console.log("Total de escolas no JSON:", dadosJson.length);

    if (dadosJson && dadosJson.length > 0) {
      // Ordenar do maior para o menor
      const dadosOrdenados = [...dadosJson].sort((a, b) => {
        return Number(b.qt_mat_bas) - Number(a.qt_mat_bas);
      });
      
      // Cortar apenas as 10 primeiras
      setTop10(dadosOrdenados.slice(0, 10));
    }
  }, []);

  return (
    <Container className="my-5">
      <h2 className="text-center mb-4">Top 10 Instituições de Ensino - PB</h2>
      
      <Table striped bordered hover responsive className="shadow-sm">
        <thead className="table-dark">
          <tr>
            <th className="text-center"># Ranking</th>
            <th>Código INEP</th>
            <th>Nome da Instituição</th>
            <th>Município</th>
            <th className="text-end">Matrículas Totais</th>
          </tr>
        </thead>
        <tbody>
          {top10.length === 0 ? (
            <tr>
              <td colSpan="5" className="text-center text-danger fw-bold">
                Nenhum dado encontrado. Verifique a pasta src/datasets.
              </td>
            </tr>
          ) : (
            top10.map((ie, index) => (
              <tr key={ie.co_entidade || index}>
                <td className="text-center fw-bold">{index + 1}º</td>
                <td>{ie.co_entidade}</td>
                <td className="fw-semibold">{ie.no_entidade}</td>
                <td>{ie.no_municipio}</td>
                <td className="text-end fw-bold text-primary">
                  {ie.qt_mat_bas}
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </Container>
  );
};

export default InstituicaoEnsino;