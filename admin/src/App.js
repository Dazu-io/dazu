import React, { Component } from 'react';
import './App.css';

class App extends Component {

  constructor(){
    super();
    this.data = {
      "teste1": [
        "exemplo1", "exemplo2"
      ],
      "teste2": [
        "exemplo1", "exemplo2"
      ],
      "teste3": [
        "exemplo1", "exemplo2"
      ],
      "teste4": [
        "exemplo1", "exemplo2"
      ],
      "teste5": [
        "exemplo1", "exemplo2"
      ],
      "teste6": [
        "exemplo1", "exemplo2"
      ],
      "teste7": [
        "exemplo1", "exemplo2"
      ],
      "teste8": [
        "exemplo1", "exemplo2"
      ],
      "teste9": [
        "exemplo1", "exemplo2"
      ],
      "teste10": [
        "exemplo1", "exemplo2"
      ],
      "teste11": [
        "exemplo1", "exemplo2"
      ],
      "teste12": [
        "exemplo1", "exemplo2"
      ],
    };
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          Learn React
        </header>
        <div className="App-content">
          {Object.keys(this.data).map((k, v) => {
            return (<div key={{k}} className="card">{k}</div>);
          })}
        </div>
      </div>
    );
  }
}

export default App;
