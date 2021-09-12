import * as React from 'react';
import { DataGrid} from '@material-ui/data-grid';
import { Button } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { Grid } from '@material-ui/core';
import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';
import firebase from 'firebase';
import * as firebaseui from 'firebaseui'
import 'firebaseui/dist/firebaseui.css'
import axios from 'axios'
import {render} from "react-dom";
import {Router, Route, IndexRoute, hashHistory} from "react-router";
// import { Viewer, Worker } from '@react-pdf-viewer/core';
// import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';

// import '@react-pdf-viewer/core/lib/styles/index.css';
// import '@react-pdf-viewer/default-layout/lib/styles/index.css';



class LawListing extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            countryName: "",
            filter: "",
            columns: [],
            rows: [],
            selectedFileName: ""
        };
    }

    componentDidMount() {
        
        // let url = "http://192.168.208.130:4901/api/v1/files/deleteFile" 
        let url = ""
        // axios.get(url)
        this.setState({ countryName: this.props.match.params.countryName } )
        this.setState({filter: this.props.match.params.filter})
        
        this.setState( {columns:   [
            {
                field: 'id',
                headerName: 'File Id',
                width: 200

            },
            {
                field: 'FileName',
                headerName: 'Law Name',
                width: 300,
            },
            {
                field: 'TimeStampRatified',
                headerName: 'Time Ratified',
                width: 300,
            },
            {
                field: 'TimeStampExpired',
                headerName: 'Time Expired',
                width: 300,
            },
            {
                field: 'TimeStampCreated',
                headerName: 'Time Created',
                width: 300,
            },
            // {
            //     field: 'TimeStampRatified',
            //     headerName: 'Ratified Time',
            //     width: 200,
            // },
            // {
            //     field: 'TimeStampExpired',
            //     headerName: 'Expired Time',
            //     type: 'number',
            //     width: 200,
            // },
            {
                field: "openFile",
                headerName: "Open File",
                width: 150,
                disableClickEventBubbling: false,
                renderCell: (params) => {
                const onClick = () => {

                    url = 'http://192.168.208.130:4901/api/v1/files/getFile?fileName=' + this.state.selectedFileName
                    window.open(url)
                    
                };
        
                return <Button onClick={onClick}>Open File</Button>;
                }
            }
            ]
        })
        url = "http://192.168.208.130:4901/api/v1/files/listFiles?countryName=" + this.props.match.params.countryName + "&filter=" + this.props.match.params.filter
        console.log(url)
        axios.get(url).then( res => {
            console.log(res)
            let data = res["data"]
            if(res["data"] == '') {
                this.setState( {
                    rows: []
                })
            } else {
                data.forEach(function(item) {
                    item["id"] = item["FileId"]
                    if(!item.hasOwnProperty("TimeStampRatified")) {
                        item["TimeStampRatified"] = "Ratified at Creation"
                    }
                    if(!item.hasOwnProperty("TimeStampExpired")) {
                        item["TimeStampExpired"] = "Indefinite"
                    }
                })
                this.setState( {
                    rows: data
                })
            }
            
        })
    //    this.setState({rows: [
    //     { id: 1, name: 'Codex Law 1', TimeStampRatified: '07-08-2021', TimeStampExpired: '03-02-2053' },
    //     { id: 2, name: 'Codex Law 2', TimeStampRatified: '07-08-2021', TimeStampExpired: '03-02-2053'},
    //     //   { id: 3, lastName: 'Lannister', firstName: 'Jaime', age: 45 },
    //     //   { id: 4, lastName: 'Stark', firstName: 'Arya', age: 16 },
    //     //   { id: 5, lastName: 'Targaryen', firstName: 'Daenerys', age: null },
    //     //   { id: 6, lastName: 'Melisandre', firstName: null, age: 150 },
    //     //   { id: 7, lastName: 'Clifford', firstName: 'Ferrara', age: 44 },
    //     //   { id: 8, lastName: 'Frances', firstName: 'Rossini', age: 36 },
    //     //   { id: 9, lastName: 'Roxie', firstName: 'Harvey', age: 65 },
    //     ]})
    }


    render() {
    return (
        <div style={{ height: 400, width: '100%' }}>
            <Typography variant="h1" component="h2" align = "Center">
            {this.state.countryName + " Official Laws"}
            </Typography>
        <DataGrid
            rows={this.state.rows}
            columns={this.state.columns}
            pageSize={20}
            checkboxSelection
            onSelectionModelChange={(ids) => {
                const selectedIDs = new Set(ids);
                const selectedRowData = this.state.rows.filter((row) =>
                  selectedIDs.has(row.id.toString())
                );
                console.log(selectedRowData[0]["FileName"]);
                this.setState({selectedFileName: selectedRowData[0]["FileName"]})
            }}/>
        {/* <Viewer></Viewer> */}
        </div>
    );

}}
export default LawListing