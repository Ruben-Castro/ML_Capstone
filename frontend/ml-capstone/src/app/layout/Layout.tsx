import { Box } from "@mui/system";
import { ReactChildren, ReactComponentElement } from "react";
import Navbar from "../components/Navbar";

interface Props {
    children: any;
}
export default function Layout({ children }: Props) {

    return (
        <>
            <Navbar />
            <div style={{ height: "85px" }}></div>
            <Box sx={{ width: "100%" }}>
                {children}
            </Box>

        </>
    )
}