import { Button, Card, CardActions, CardContent, CardHeader, LinearProgress, Typography } from "@mui/material"
import { Box } from "@mui/system"
import axios from "axios"
import fileDownload from "js-file-download"
import { useState } from "react"


export default function UploadCard({ upload }: any) {
    const [progressBarPercent, setProgressBarPercent] = useState(0)
    const [progressBarDisplay, setProgressBarDisplay] = useState(false)

    const downloadFile = (fileName: string) => {
        console.log("download file started")
        let filePath = `http://localhost/videos/processed/${fileName}`
        axios({
            method: "GET",
            url: filePath,
            responseType: 'blob',
            onDownloadProgress: (progressEvent) => {
                let percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total); // you can use this to show user percentage of file downloaded
                setProgressBarPercent(percentCompleted)
            }
        }).then((response) => {
            let filename = filePath.replace(/^.*[\\\/]/, '')
            let fileExtension;
            fileExtension = filePath.split('.');
            fileExtension = fileExtension[fileExtension.length - 1];
            fileDownload(response.data, `${filename}.${fileExtension}`);

        })
    }

    const downloadCSV = (fileName: string) => {
        console.log("download file started")
        let filePath = `http://localhost/csvdata/${fileName}`
        axios({
            method: "GET",
            url: filePath,
            responseType: 'blob',
            onDownloadProgress: (progressEvent) => {
                let percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total); // you can use this to show user percentage of file downloaded
                setProgressBarPercent(percentCompleted)
            }
        }).then((response) => {
            let filename = filePath.replace(/^.*[\\\/]/, '')
            let fileExtension;
            fileExtension = filePath.split('.');
            fileExtension = fileExtension[fileExtension.length - 1];
            fileDownload(response.data, `${filename}.${fileExtension}`);

        })
    }

    return (<Card>
        <CardHeader title={upload.filename} />
        <CardContent>
            {progressBarDisplay ? <>
                <Typography>Downloading File...</Typography>
                <Box sx={{ width: '100%' }}>
                    <LinearProgress variant="determinate" value={progressBarPercent} />
                </Box> </> : null}

        </CardContent>
        <CardActions disableSpacing>
            <Button onClick={() => {
                setProgressBarDisplay(true)
                downloadFile(`${upload.filename.split('.')[0]}_yolo_out.avi`)
            }}>Download Anotated Video</Button>
            <Button
                onClick={() => {

                    downloadCSV(`${upload.filename.split('.')[0]}_yolo_out.csv`)
                }}

            >Download CSV Data</Button>
        </CardActions>
    </Card>)
}