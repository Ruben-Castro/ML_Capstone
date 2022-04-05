import { Button, Card, CardActions, CardContent, CardHeader, Grid, LinearProgress, Typography } from "@mui/material"
import { useQuery } from "react-query"
import axios from "axios"
import fileDownload from 'js-file-download'
import { Box } from "@mui/system"
import { useState } from "react"
import UploadCard from "../components/UploadCard"


const fetchUploads = async () => {
    const { data } = await axios.get(`${process.env.REACT_APP_API_BASE_URL}/videos`)
    console.log(data)
    return data
}






export default function Uploads() {

    const query = useQuery('uploaded videos', fetchUploads)



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