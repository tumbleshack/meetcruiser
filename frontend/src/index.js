import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import theme from './styles/theme';

import App from "./App";

const root = createRoot(document.getElementById("root"));
root.render(
    <ThemeProvider theme={theme}>
        <StrictMode>
            <CssBaseline />
            <App />
        </StrictMode>
    </ThemeProvider>
);