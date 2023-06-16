import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import { 
    AppBar,
    Box,
    Button,
    Fab,
    Fade,
    Toolbar,
    useScrollTrigger,
} from '@mui/material';
import { KeyboardArrowUp } from '@mui/icons-material';
import styled from '@emotion/styled';
import { useTheme } from '@mui/material/styles';
import { api } from './connect'; 
import Cruiser from './Cruise'

const FillerBox = styled(Box)(({ theme }) => ({
        backgroundColor: theme.palette.primary.main,
    })
)

function ScrollTop(props) {
    const { children, window } = props;
    // Note that you normally won't need to set the window ref as useScrollTrigger
    // will default to window.
    // This is only being set here because the demo is in an iframe.
    const trigger = useScrollTrigger({
      disableHysteresis: true,
      threshold: 100,
    });
  
    const handleClick = (event) => {
      const anchor = (event.target.ownerDocument || document).querySelector(
        '#back-to-top-anchor',
      );
  
      if (anchor) {
        anchor.scrollIntoView({
          block: 'center',
        });
      }
    };
  
    return (
      <Fade in={trigger}>
        <Box
          onClick={handleClick}
          role="presentation"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
        >
          {children}
        </Box>
      </Fade>
    );
}

function ElevationScroll(props) {
    const { children, window } = props;
    // Note that you normally won't need to set the window ref as useScrollTrigger
    // will default to window.
    // This is only being set here because the demo is in an iframe.
    const trigger = useScrollTrigger({
        disableHysteresis: true,
        threshold: 0,
    });

    return React.cloneElement(children, {
        elevation: trigger ? 4 : 0,
    });
}

const pullMeetData = () => {
    api.meetMeetIdGet(1).then((response) => {
        console.log(response.data);
    })
}

export default function App(props) {
    const theme = useTheme()
    return (
        <React.Fragment>
            <CssBaseline />
            <ElevationScroll {...props}>
                <AppBar>
                    <Toolbar>
                        <Button onClick={pullMeetData} width='100%' align='center' variant="h5" component="div">
                            Meet Cruiser
                        </Button>
                    </Toolbar>
                </AppBar>
            </ElevationScroll>
            <Toolbar id="back-to-top-anchor" />
            <Cruiser />
            <ScrollTop {...props}>
                <Fab size="small" aria-label="scroll back to top">
                    <KeyboardArrowUp />
                </Fab>
            </ScrollTop>
        </React.Fragment>
    );
}