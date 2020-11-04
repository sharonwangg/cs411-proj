import React, {Component} from "react";
import { render } from "react-dom";


export default class Login extends Component {
    
    constructor(props) {
        super(props)
        this.state = {isLoginOpen: true, isRegisterOpen: false};
    }

    showLoginBox(){
        this.setState({isLoginOpen: true, isRegisterOpen: false});
    }

    showRegisterBox(){
        this.setState({isRegisterOpen: true, isLoginOpen: false});
    }

    render(){
    return (
        <div className = "root-container">

            <div className = "box-controller">
                <div className = {"controller " + (this.state.isLoginOpen ? "selected-controller" : "")} onClick = {this.showLoginBox.bind(this)}>
                    Login
                </div>
                <div className = {"controller " + (this.state.isLoginOpen ? "selected-controller" : "")} onClick = {this.showRegisterBox.bind(this)}>
                    Register
                </div>
            </div>

            <div className = "box-container">
                {this.state.isLoginOpen && <LoginBox />}
                {this.state.isRegisterOpen && <RegisterBox />}
            </div>
        </div>
    ); 
    }
}

class LoginBox extends Component{
    constructor(props){
        super(props);
        this.state= {};
    }

    submitLogin(e){
        
    }
    render(){
    return(
        <div className = "inner-container">
            <div className= "header">
                Login
            </div>

            <div className = "box">

                <div className = 'input-group'>
                    <label htmlFor = "username">
                        Username
                    </label>
                    <input type = "text" name =  "username" className = "login-input" placeholder = "Username">
                    </input>
                </div>

                <div className = 'input-group'>
                    <label htmlFor = "password">
                        Password
                    </label>
                    <input type = "password" name =  "password" className = "login-input" placeholder = "Password">
                    </input>
                </div>

                <button type = "button" className = "login-btn" onClick = {this.submitLogin.bind(this)}>
                    Login
                </button>
            </div>
        </div>   
    );
    }
}

class RegisterBox extends Component{
    constructor(props){
        super(props);
        this.state= {
            username: "",
            email: "",
            age: "",
            password: "",
        };
    }

    onUsernameChange(e){
        this.setState({username: e.target.value});
    }

    onEmailChange(e){
        this.setState({email: e.target.value});
    }

    onAgeChange(e){
        this.setState({age: e.target.value});
    }
    
    onPasswordChange(e){
        this.setState({password: e.target.value});
    }

    submitRegister(e){
        
    }
    render(){
    return(
        <div className = "inner-container">
            <div className= "header">
                Register
            </div>
            <form actiom = "/" methods = "POST">

                <div className = 'form-group'>
                    <label htmlFor = "username">
                        Username
                    </label>
                    <input type = "text" name =  "username" className = "login-input" placeholder = "Username" onChange = {this.onUsernameChange.bind(this)}>
                    </input>
                </div>

                <div className = 'form-group'>
                    <label htmlFor = "email">
                        E-mail
                    </label>
                    <input type = "text" name =  "email" className = "login-input" placeholder = "Email" onChange = {this.onEmailChange.bind(this)}>
                    </input>
                </div>

                <div className = 'form-group'>
                    <label htmlFor = "age">
                        Age
                    </label>
                    <input type = "text" name =  "age" className = "login-input" placeholder = "Age" onChange = {this.onAgeChange.bind(this)}>
                    </input>
                </div>

                <div className = 'form-group'>
                    <label htmlFor = "password">
                        Password
                    </label>
                    <input type = "password" name =  "password" className = "login-input" placeholder = "Password" onChange = {this.onPasswordChange.bind(this)}>
                    </input>
                </div>

                <button type = "button" className = "login-btn" onClick = {this.submitRegister.bind(this)}>
                    Register
                </button>
            </form>
        </div> 
    );  
    }
}

