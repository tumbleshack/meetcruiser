import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import styled from '@emotion/styled';

const FillerBox = styled(Box)(({ theme }) => ({
        backgroundColor: 'blue',
    })
)

const layout = {
    logoHeight: '4em',
    currentEventHeight: '16em',
    nextEventHeight: '4em',
    followingEventHeight: '50em',
}

export default function SimpleContainer() {
    return (
        <React.Fragment>
            <CssBaseline />
            <Container sx={{ minHeight: layout.logoHeight }} >
                <FillerBox sx={{ height: layout.logoHeight }} />
            </Container>
            <Container sx={{ minHeight: layout.currentEventHeight,}} >
                <FillerBox sx={{ height: layout.currentEventHeight }} />
            </Container>
            <Container sx={{ minHeight: layout.nextEventHeight,}} >
                <FillerBox sx={{ height: layout.nextEventHeight }} />
            </Container>
            <Container sx={{ minHeight: layout.followingEventHeight,}} >
                <FillerBox sx={{ height: layout.followingEventHeight }} />
            </Container>
        </React.Fragment>
    );
}