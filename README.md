# Censo Escolar 2025 - Paraíba (Extração de Dados e Aplicação Web)

Este repositório reúne os dois projetos da atividade de Programação Web I baseados nos microdados oficiais do Censo Escolar 2025 (INEP) para o estado da Paraíba (PB):

## Estrutura do Repositório

- **CensoEscolarDataApp/**: Script em Python (app.py) desenvolvido com pandas para filtrar as instituições de ensino da Paraíba, cruzar os dados de matrículas e gerar o arquivo estruturado ie_paraiba_2025.json.
- **CensoEscolarWeb/**: Aplicação frontend desenvolvida em React e React-Bootstrap contendo a página Home (carrossel de imagens e cartões informativos) e a página de Instituições de Ensino (ranking Top 10 ordenado pelo total de matrículas na Educação Básica - qt_mat_bas).

## Como executar o Frontend (CensoEscolarWeb)

    cd CensoEscolarWeb
    npm install
    npm run dev
