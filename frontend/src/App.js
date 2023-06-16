import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import { 
    AppBar,
    Box,
    Container, 
    Paper,
    Accordion,
    AccordionSummary,
    AccordionDetails, 
    Fab,
    Fade,
    Toolbar,
    Typography,
    useScrollTrigger,
} from '@mui/material';
import { ExpandMore, KeyboardArrowUp } from '@mui/icons-material';
import styled from '@emotion/styled';
import { useTheme } from '@mui/material/styles';

const FillerBox = styled(Box)(({ theme }) => ({
        backgroundColor: theme.palette.primary.main,
    })
)

const CurrentRaceAccordionSummary = (props) => { 
    const StyledAccordion = styled(AccordionSummary)(({ theme }) => ({
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.primary.contrastText,
    }))
    return (<StyledAccordion {...props} expandIcon={<ExpandMore style={{ color: 'white' }} />} />)
}

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

const layout = {
    logoHeight: '4em',
    currentEvent: { 
        minHeight: '16em',
        accordion: {
            height: '2em',
        },
        box: {
            height: '14em',
        }
    },
    nextEventHeight: '4em',
    followingEventHeight: '50em',
}

const dummyData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const Upcoming = (text) => {
    return (
        <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>{text}</AccordionSummary>
            <AccordionDetails >Contents</AccordionDetails>
        </Accordion>
    )
}

export default function SimpleContainer(props) {
    const theme = useTheme()
    return (
        <React.Fragment>
            <CssBaseline />
            <ElevationScroll {...props}>
                <AppBar>
                    <Toolbar>
                        <Typography variant="h6" component="div">
                            Logo
                        </Typography>
                    </Toolbar>
                </AppBar>
            </ElevationScroll>
            <Toolbar id="back-to-top-anchor" />
            <Container sx={{ minHeight: layout.currentEvent.height }} >
                <Paper sx={{ height: layout.currentEvent.height }}> 
                    <Box sx={{ height: layout.currentEvent.box.height }}>
                    </Box>
                    <Accordion disableGutters>
                        <CurrentRaceAccordionSummary >Summary</CurrentRaceAccordionSummary>
                        <AccordionDetails >Contents</AccordionDetails>
                    </Accordion>
                </Paper>
            </Container>
            <Container sx={{ minHeight: layout.nextEventHeight,}} >
                <Typography>NEXT RACE RACES</Typography>
                {Upcoming('next race details')}
            </Container>
            <Container sx={{ minHeight: layout.followingEventHeight,}} >
                <Typography>UPCOMING RACES</Typography>
                {dummyData.map((item) => Upcoming(item))}
            </Container>
            <ScrollTop {...props}>
                <Fab size="small" aria-label="scroll back to top">
                    <KeyboardArrowUp />
                </Fab>
            </ScrollTop>
        </React.Fragment>
    );
}