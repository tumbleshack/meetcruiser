import { red } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

// A custom theme for this app
const theme = createTheme({
    components: {
        MuiContainer: {
            defaultProps: {
                maxWidth: 'xs',
            },
            styleOverrides: {
                root: {
                    marginTop: '12px',
                    marginBottom: '12px',
                }
            }
        },
        MuiAppBar: {
            defaultProps: {
                color: '',
            }
        }
    },
    palette: {
        primary: {
            main: '#556cd6',
        },
        secondary: {
            main: '#19857b',
        },
        error: {
            main: red.A400,
        },
    },
});

export default theme;