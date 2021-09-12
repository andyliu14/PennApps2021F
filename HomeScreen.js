import * as React from 'react';
import { DataGrid} from '@material-ui/data-grid';
import { Button } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { Grid } from '@material-ui/core';
import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';
import firebase from 'firebase';
import * as firebaseui from 'firebaseui'
import 'firebaseui/dist/firebaseui.css'
import LongMenu from './countryMenu';
import logo from './logo.svg';

import {useState} from 'react'
import './App.css';


class HomeScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [{
                first_name: "Out"

            }, {
                first_name: "In"
            }]
        };
    }

    componentDidMount() {
       
    }


    render() {
    // const [searchTerm, setSearchTerm] = useState("");
    return (
        <div className="App">
        <Typography variant="h1" gutterBottom>
          Welcome to Lex Eterna!
      </Typography>
      
      <LongMenu/>

      {/* <input type = "text" placeholder = "Search..." onChange = {event => setSearchTerm(event.target.value)} />
      {this.state.data.filter((val) => {
        if (searchTerm == "") {
          return val
        } else if (val.first_name.toLowerCase().includes(searchTerm.toLowerCase())) {
          return val
        }
      }).map((val, key) => {
        return (
          <div className = "user" key = {key}> 
            <p> {val.first_name} </p>
          </div>
        );
      })} */}
        </div>
    );
    
    }}
export default HomeScreen