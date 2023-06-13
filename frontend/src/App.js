import axios from "axios";
import { socket } from './socket.js';
import { useEffect } from 'react';

function Square({ value, onSquareClick }) {
    return (
        <button className="square" onClick={onSquareClick}>
            {value}
        </button>
    );
}

export default function Board() {

    const secretInfo = () => {
        console.log("Square clicked");

        axios.get("http://localhost:5000/secret").then((response) => {
            console.log(response.data);
        });
    }

    const loginFun = () => {
        console.log("Login clicked");

        axios.post("http://localhost:5000/api/auth/login", {
            email: "test@me.com",
            password: "password",
            submit: "Login"
        }).then((response) => {
            console.log(response.data);
        });
    }

    const logoutFun = () => {
        console.log("Logout clicked");

        axios.post("http://localhost:5000/api/auth/logout", {
            submit: "Logout"
        }).then((response) => {
            console.log(response.data);
        });
    }

    const socketConnect = () => {
        console.log("Connect clicked");
        socket.connect();
    }

    const socketDisconnect = () => {
        console.log("Disconnect clicked");
        socket.disconnect();
    }

    const emitEvent = () => {
        console.log("Emit clicked");
        socket.emit("my_event", "Hello World");
    }

    useEffect(() => {
        console.log("Setting up socket listener");
        socket.on("my_response", (data) => {
            console.log("Received data from server");
            console.log(data);
        });

        return () => {
            console.log("Cleaning up socket listener");
            socket.off("my_response");
        }

    }, [socket]);
    
    return (
        <>
            <Square value="Login" onSquareClick={loginFun}/>
            <Square value="FetchApi" onSquareClick={secretInfo}/>
            <Square value="Logout" onSquareClick={logoutFun}/>
            <Square value="ConnectSocket" onSquareClick={socketConnect}/>
            <Square value="EmitSocketEvent" onSquareClick={emitEvent}/>
            <Square value="DisconnectSocket" onSquareClick={socketDisconnect}/>
        </>
    ) 
        
}