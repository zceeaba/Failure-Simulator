import React, { Component } from 'react';
import './App.css';

const axios=require('axios')

class App extends Component {
    constructor() {
        super();
        this.state = {
            routerdata: []
        };
    }
    getjsondata() {
        this.state.routerdata="hey bro"
        /*
        axios.get('./testdata.json') // JSON File Path
            .then( response => {
                this.setState({
                    routerdata: response.data
                });
            })
            .catch(function (error) {
                console.log(error);
            });
         */
    }
  render() {
        this.getjsondata();
        const routerdata=this.state.routerdata;
        return(
            <div className="App">
                <p>{routerdata}</p>
                <p>This is the router data</p>
            </div>
        );
  }
}

export default App;
