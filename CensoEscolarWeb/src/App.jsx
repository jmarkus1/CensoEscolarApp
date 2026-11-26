import { BrowserRouter, Route, Routes } from 'react-router';
import Home from './views/Home';
import InstituicaoEnsino from './views/InstituicaoEnsino';
import MainLayout from './layouts/MainLayout';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          <Route path="instituicoesensino" element={<InstituicaoEnsino />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
