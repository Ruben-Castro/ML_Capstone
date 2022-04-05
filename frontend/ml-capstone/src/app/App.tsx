import { Button, Grid, Typography } from "@mui/material";
import { useDropzone } from "react-dropzone";
import { Route, Routes } from "react-router-dom";
import styled from 'styled-components';
import Navbar from "./components/Navbar";
import Layout from "./layout/Layout";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Uploads from "./pages/Uploads";

const getColor = (props: any) => {
  if (props.isDragAccept) {
    return '#00e676';
  }
  if (props.isDragReject) {
    return '#ff1744';
  }
  if (props.isFocused) {
    return '#2196f3';
  }
  return '#eeeeee';
}

const Container = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-width: 2px;
  border-radius: 2px;
  border-color: ${(props: any) => getColor(props)};
border-style: dashed;
background-color: #fafafa;
color: #bdbdbd;
outline: none;
transition: border .24s ease -in -out;
`;



function App() {


  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path='upload' element={<Upload />} />
        <Route path="uploads" element={<Uploads />} />
      </Routes>
    </Layout>
  );
}

export default App;
