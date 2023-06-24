import { Manager } from "socket.io-client";
import { ApiMeetApi } from './api';
import axios from 'axios';

// "undefined" means the URL will be computed from the `window.location` object
// const URL = process.env.NODE_ENV === 'production' ? undefined : 'http://localhost:5000';
const URL = process.env.REACT_APP_MEETCRUISER_API_URL;
const manager = new Manager(URL, {
    autoConnect: false,
});

export const socket = manager.socket("/test");

export const api = new ApiMeetApi(null, URL, axios);