import React, { Component } from 'react';
import './App.css';
import data from './testdata.json';


const axios=require('axios')

class App extends Component {
    constructor() {
        super();
        this.state = {
            routerdata: data
        };
    }
    getjsondata() {
        this.state.routerdata=JSON.stringify(this.state.routerdata)
    }
    createTable(){
        let table=[];
        for(let i=0;i<data.nodes.length;i++){
            let children=[];
            for(let key in data.nodes[i]){
                if (data.nodes[i].hasOwnProperty(key)) {
                    let value=data.nodes[key];
                    children.push(<tr>{value}</tr>)
                }

            }
            table.push(<td>{children}</td>)
        }
        return table
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
