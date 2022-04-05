import { useDropzone } from "react-dropzone";
import styled from 'styled-components';
import axios from 'axios';
import { useMutation, useQueryClient } from 'react-query'
import { Alert, Snackbar } from "@mui/material";
import { useCallback, useState } from "react";



const addFiles = async (files: any) => {
    let formData = new FormData();

    files.forEach((file: any) => {
        console.log(`file: ${file.path}`)
        formData.append("files", file, file.path)
    });
    console.log("keys")
    console.log(formData.keys);

    axios.post(`${process.env.REACT_APP_API_BASE_URL}/uploadvideos`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then((response) => console.log(response)).catch((err) => console.log(`error: ${err}`))
}

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

export default function Upload() {

    const [snackbarOpen, setSnackbarOpen] = useState(false);

    const onDrop = useCallback(acceptedFiles => {
        console.log(acceptedFiles)
        mutation.mutate(acceptedFiles)
    }, [])
    const queryClient = useQueryClient()
    // When this mutation succeeds, invalidate any queries with the `todos` or `reminders` query key
    const mutation = useMutation(addFiles, {
        onSuccess: () => {
            queryClient.invalidateQueries('uploads')
        },
    })


    const { acceptedFiles, getRootProps, getInputProps, fileRejections, isFocused,
        isDragAccept,
        isDragReject } = useDropzone(
            {
                accept: 'video/mp4',
                onDrop: onDrop
            }


        )


    const acceptedFileItems = acceptedFiles.map((file: any) => {
        return (
            <li key={file.path}>
                {file.path} - {file.size} bytes
            </li>
        )
    });


    const fileRejectionItems = fileRejections.map(({ file, errors }: any) => {
        return (
            <li key={file.path}>
                {file.path} - {file.size} bytes
                <ul>
                    {errors.map((e: any) => {
                        return <li key={e.code}>{e.message}</li>
                    }
                    )}
                </ul>
            </li>
        )
    });


    return <section className="container">
        <Container {...getRootProps({ isFocused, isDragAccept, isDragReject })}>
            <input {...getInputProps()} />
            <p>Drag 'n' drop some files here, or click to select files</p>
            <em>(Only .mp4 files accepted)</em>
        </Container>


        <Snackbar
            open={mutation.isSuccess && snackbarOpen == false}
            autoHideDuration={6000}
            onClose={() => { setSnackbarOpen(false) }}
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
            <Alert severity="success" sx={{ width: '100%' }}>
                message Files uploaded successfully
            </Alert>
        </Snackbar>

        <Snackbar
            open={mutation.isError}
            autoHideDuration={6000}
            message="Files uploaded successfully"
        />

        <aside>
            <h4>Accepted files</h4>
            <ul>{acceptedFileItems}</ul>
            <h4>Rejected files</h4>
            <ul>{fileRejectionItems}</ul>
        </aside>
    </section>
}