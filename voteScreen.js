import * as React from 'react';
import { DataGrid} from '@material-ui/data-grid';
import { Button } from '@material-ui/core';
import { Typography } from '@material-ui/core';
import { FilePicker } from 'react-file-picker'
import { Grid } from '@material-ui/core';
import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';
import firebase from 'firebase';
import * as firebaseui from 'firebaseui'
import 'firebaseui/dist/firebaseui.css'
import axios from 'axios';
import { TextField } from '@material-ui/core';

class VoteScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            countryName: "",
            columns: [],
            rows: [],
            proposedFileName: "",
        };
        
    }
    handleChange = (e) => this.setState({ 
		proposedFileName: e.target.value 
	}) 
    componentDidMount() {
        let url = ""
        let cName = ""
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
            {
                field: "voteBtn",
                headerName: "Vote For",
                width: 150,
                disableClickEventBubbling: true,
                renderCell: (params) => {
                const onClick = () => {
                    firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
                        console.log(idToken)
                    }).catch(function(error) {
                        // Handle error
                    });
                    this.setState({"countryName": "Old"})
                };
        
                return <Button onClick={onClick}>Vote For</Button>;
                }
                },
                {
                    field: "voteAgainstBtn",
                    headerName: "Vote Against",
                    width: 200,
                    disableClickEventBubbling: true,
                    renderCell: (params) => {
                    const onClick = () => {
                        firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
                            console.log(idToken)
                        }).catch(function(error) {
                            // Handle error
                        });
                        this.setState({"countryName": "New"})
                    };
        
                    
                
                    return <Button onClick={onClick}>Vote Against</Button>;
                    }
                },
                {
                    field: "openFile",
                    headerName: "Open File",
                    width: 150,
                    disableClickEventBubbling: true,
                    renderCell: (params) => {
                    const onClick = () => {
                        firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
                            console.log(idToken)
                        }).catch(function(error) {
                            // Handle error
                        });
                        this.setState({"countryName": "Old"})
                        window.open("http://google.com")
                    };
            
                    return <Button onClick={onClick}>Open File</Button>;
                    }
                    },
                    {
                        field: "voteAgainstBtn",
                        headerName: "Vote Against",
                        width: 200,
                        disableClickEventBubbling: true,
                        renderCell: (params) => {
                        const onClick = () => {
                            firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
                                console.log(idToken)
                            }).catch(function(error) {
                                // Handle error
                            });
                            this.setState({"countryName": "New"})
                        };
            
                        return <Button onClick={onClick}>Vote Against</Button>;
                        }
                    }
            ]})
        firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(idToken => {
            url = "http://192.168.208.130:4901/api/v1/users/getUserCountry?token=" + idToken
            axios.get(url).then( res => {
                console.log(res.data)
                this.setState( {
                    countryName: res.data
                },  
                 () => {
                    url = "http://192.168.208.130:4901/api/v1/voting/listProposals?countryName=" + this.state.countryName

                    console.log(url)
                    axios.get(url).then( res => {
                        console.log(res)
                        if(res["data"] == '') {
                            this.setState( {
                                rows: []
                            })
                        } else {
                            let data = JSON.parse(res["data"])
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
                        });
                        
            })
        }).catch(function(error) {
            // Handle error
        });            
    }


    render() {
        const onClick = () => {
            firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(idToken => {
                console.log(idToken)
            }).catch(function(error) {
                // Handle error
            });
            this.setState({"countryName": "Old"})
        };

        
    return (
        <div style={{ height: 400, width: '100%' }}>
            <Typography variant="h1" component="h2" align = "center">
            {this.state.countryName + " Proposed Laws"}
            </Typography>
        <DataGrid
            rows={this.state.rows}
            columns={this.state.columns}
            pageSize={20}
        />
        <TextField 
            value={this.state.proposedFileName} 
            onChange={this.handleChange} 
        /> 
        <FilePicker
            extensions={['pdf']}
            onChange={FileObject => 
                firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(idToken => {
                    let url = "http://192.168.208.130:4901/api/v1/voting/initializeVote/"
                    var formData = new FormData()
                    formData.append("fileName", FileObject)
                    console.log(formData)
                    console.log(url)
                    axios.post(url, formData,{
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            file: FileObject,
                        }
                    })
                })
            }
            onError={errMsg => (console.log(errMsg))}
        >
            <Button>
            Propose Law
            </Button>
        </FilePicker>
        
         <Button>
             Create User
        </Button>   
        <Button>
             Create Country
        </Button>   

                
        </div>
    );
    
    }}
export default VoteScreen