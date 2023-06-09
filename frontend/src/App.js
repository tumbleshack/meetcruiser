import axios from "axios";

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
    
    return (
        <>
            <Square value="Login" onSquareClick={loginFun}/>
            <Square value="Fetch" onSquareClick={secretInfo}/>
            <Square value="Logout" onSquareClick={logoutFun}/>
        </>
    ) 
        
}