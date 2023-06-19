import {
    Accordion,
    AccordionSummary,
    AccordionDetails,
    Alert,
    AlertTitle,
    Box,
    Container,
    Paper,
    Skeleton,
    Typography,
} from '@mui/material';
import { ExpandMore } from '@mui/icons-material';
import styled from '@emotion/styled';
import { bound, startDescriptionText, startNumberText } from './utils'

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

const Upcoming = (props) => {
    return (
        <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'flex-end' }} >
                    <Typography variant='body2'>{props.description}</Typography>
                    <Typography variant='body2'>{props.text}</Typography>
                </Box>
            </AccordionSummary>
            <AccordionDetails>Contents</AccordionDetails>
        </Accordion>
    )
}

const dummyData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

const RaceCardContent = (props) => {
    console.log(props.start)
    return (
        <Box sx={{ minHeight: props.height, display: 'flex', flexDirection: 'column', justifyContent: 'space-evenly', alignItems: 'stretch' }}>
            <Box sx={{ height: '1em' }} />
            <Typography width='100%' align='center' variant='h7'>CURRENT EVENT</Typography>
            <Typography width='100%' align='center' variant='h2'>{startNumberText(props.start)}</Typography>
            <Typography width='100%' align='center' variant='h7'>{startDescriptionText(props.start)}</Typography>
            <Box sx={{ height: '2em' }} />
        </Box>
    )
}

export default function Cruisers(props) {
    if (!props.meetData && !props.pullAttempted) {
        return (
            <>
                <Container sx={{ marginTop: '4px', height: layout.currentEvent.minHeight }} >
                    <Skeleton variant="rounded" width="100%" height="100%" />
                </Container>
                <Container sx={{ height: layout.nextEventHeight}} >
                    <Skeleton variant="rounded" width="100%" height="100%" />
                </Container>
                <Container sx={{ marginTop: '40px', height: layout.nextEventHeight}} >
                    <Skeleton variant="rounded" width="100%" height="100%" />
                </Container>
                <Container sx={{ height: layout.nextEventHeight}} >
                    <Skeleton variant="rounded" width="100%" height="100%" />
                </Container>
                <Container sx={{ height: layout.nextEventHeight}} >
                    <Skeleton variant="rounded" width="100%" height="100%" />
                </Container>
            </>
        )
    }  else if (props.meetData) {
        const nextStart = props.meetData.starts[props.meetData.current_start + 1]
        const nextText = startNumberText(nextStart)
        const nextDescription = startDescriptionText(nextStart)
        let twoStartsAheadIdx = bound(0, props.meetData.current_start + 2, props.meetData.starts.length);
        var upcomingAccordions = [];
        let upcomingStarts = props.meetData.starts.slice(twoStartsAheadIdx)
        upcomingStarts.forEach(start => {
            const text = startNumberText(start)
            const description = startDescriptionText(start)
            upcomingAccordions.push(
                <Upcoming text={text} description={description} />
            )
        });
        if (upcomingStarts.length === 0) {
            upcomingAccordions.push(
                <Upcoming text={"None :)"} />
            )
        }

        return (
            <>
                <Container sx={{ marginTop: '4px', minHeight: layout.currentEvent.minHeight }} >
                    <Paper sx={{ height: layout.currentEvent.height }}> 
                        <RaceCardContent start={props.meetData.starts[props.meetData.current_start]} height={layout.currentEvent.box.height} >
                        </RaceCardContent>
                        <Accordion disableGutters>
                            <CurrentRaceAccordionSummary >Details</CurrentRaceAccordionSummary>
                            <AccordionDetails >Contents</AccordionDetails>
                        </Accordion>
                    </Paper>
                </Container>
                <Container sx={{ minHeight: layout.nextEventHeight,}} >
                    <SectionHeading text="NEXT RACE RACES" />
                    <Upcoming text={nextText} description={nextDescription} />
                </Container>
                <Container sx={{ minHeight: layout.followingEventHeight,}} >
                    <SectionHeading text="UPCOMING RACES" />
                    {upcomingAccordions}
                </Container>
            </>
        ) 
    } else {
        return (
            <Alert sx={{ width:"100%" }} severity="error">
                <AlertTitle>Error</AlertTitle>
                Failed to fetch meet data. <a href="mailto:kedronhillscruisers@gmail.com"><strong>Report this incident.</strong></a>
            </Alert>
        )
    }
}