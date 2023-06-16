import { Manager } from "socket.io-client";
import { DefaultApi } from './api';
import axios from 'axios';

// "undefined" means the URL will be computed from the `window.location` object
const URL = process.env.NODE_ENV === 'production' ? undefined : 'http://localhost:5000';
const manager = new Manager(URL, {
    autoConnect: false,
});

export const socket = manager.socket("/test");

export const api = new DefaultApi(null, 'http://localhost:5000', axios);