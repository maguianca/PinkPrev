import './App.css'
import FileUploader from './components/FileUploader';
import MainLayout from './components/MainLayout';
import Navbar from './components/Navbar';
import { GlobalStyles } from "./components/styles/MyGlobalStyle.style";

function App() {


  return (
    <>
      <GlobalStyles />
      <Navbar />
      <MainLayout />
    </>
  );
}

export default App
