import { Button, Card, CardActions, CardContent, CardHeader, Grid, LinearProgress, Typography } from "@mui/material"
import { useQuery } from "react-query"
import axios from "axios"
import fileDownload from 'js-file-download'
import { Box } from "@mui/system"
import { useState } from "react"
import UploadCard from "../components/UploadCard"


const fetchUploads = async () => {
    const { data } = await axios.get("http://localhost/videos")
    console.log(data)
    return data
}






export default function Uploads() {

    const query = useQuery('uploaded videos', fetchUploads)
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


    return (
        <Grid container direction="row" rowSpacing={2} spacing={2}  >
            <Grid item sm={12} xl={12}><Typography variant="h4">Processed Files</Typography></Grid>
            {query.isSuccess ? query.data['files'].map((upload: any) => {
                return (
                    <Grid item key={upload.filename} >
                        <UploadCard upload={upload} />
                    </Grid>
                )
            }) : null}

        </Grid>

    )


}