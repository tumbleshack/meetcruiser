import {
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Box,
    Container,
    Paper,
    Typography,
} from '@mui/material';
import { ExpandMore, KeyboardArrowUp } from '@mui/icons-material';
import styled from '@emotion/styled';

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

const CurrentRaceAccordionSummary = (props) => { 
    const StyledAccordion = styled(AccordionSummary)(({ theme }) => ({
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.primary.contrastText,
    }))
    return (<StyledAccordion {...props} expandIcon={<ExpandMore style={{ color: 'white' }} />} />)
}

const SectionHeading = (props) => {
    return (
        <Box sx={{ marginTop: "4px", marginBottom: "4px" }} >
            <Typography>{props.text}</Typography>
        </Box>
    )
}

const Upcoming = (text) => {
    return (
        <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>{text}</AccordionSummary>
            <AccordionDetails >Contents</AccordionDetails>
        </Accordion>
    )
}

const dummyData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const RaceCardContent = (props) => {
    return (
        <Box sx={{ minHeight: props.height, display: 'flex', flexDirection: 'column', justifyContent: 'space-evenly', alignItems: 'stretch' }}>
            <Box sx={{ height: '1em' }} />
            <Typography width='100%' align='center' variant='h7'>CURRENT EVENT</Typography>
            <Typography width='100%' align='center' variant='h2'>22</Typography>
            <Typography width='100%' align='center' variant='h7'>6 & under 25 yd Butterfly</Typography>
            <Box sx={{ height: '2em' }} />
        </Box>
    )
}

export default function Cruisers(props) {
    return (
        <>
            <Container sx={{ marginTop: '4px', minHeight: layout.currentEvent.height }} >
                <Paper sx={{ height: layout.currentEvent.height }}> 
                    <RaceCardContent height={layout.currentEvent.box.height} >
                    </RaceCardContent>
                    <Accordion disableGutters>
                        <CurrentRaceAccordionSummary >Details</CurrentRaceAccordionSummary>
                        <AccordionDetails >Contents</AccordionDetails>
                    </Accordion>
                </Paper>
            </Container>
            <Container sx={{ minHeight: layout.nextEventHeight,}} >
                <SectionHeading text="NEXT RACE RACES" />
                {Upcoming('next race details')}
            </Container>
            <Container sx={{ minHeight: layout.followingEventHeight,}} >
                <SectionHeading text="UPCOMING RACES" />
                {dummyData.map((item) => Upcoming(item))}
            </Container>
        </>
    )
}