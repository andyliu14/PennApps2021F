import React from 'react';
import IconButton from '@material-ui/core/IconButton';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import { useState } from 'react';
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Dialog from '@material-ui/core/Dialog';
import Typography from '@material-ui/core/Typography';
import { blue } from '@material-ui/core/colors';
import axios from 'axios';
//import SimpleDialogDemo from './timeDialog';

// Dialog Components
const times = ['All', 'Expired', 'Future', 'Effective'];
const useStyles = makeStyles({
  avatar: {
    backgroundColor: blue[100],
    color: blue[600],
  },
});

function SimpleDialog(props) {
  const classes = useStyles();
  const { onClose, selectedValue, open } = props;

  const handleDialogClose = () => {
    onClose(selectedValue);
  };

  const handleListItemClick = (value) => {
    onClose(value);
  };

  return (
    <Dialog onClose={handleDialogClose} aria-labelledby="simple-dialog-title" open={open}>
      <DialogTitle id="simple-dialog-title">Which time period would you like to view laws from?</DialogTitle>
      <List>
        {times.map((time) => (
          <ListItem button onClick={() => handleListItemClick(time)} key={time}>
            <ListItemText primary={time} />
          </ListItem>
        ))}
      </List>
    </Dialog>
  );
}

SimpleDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  selectedValue: PropTypes.string.isRequired,
};


// Drop Down Menu components
const options = [
];

const ITEM_HEIGHT = 48;


export default function LongMenu() {
  // Dialog
  const [openDio, setOpen] = React.useState(false);
  const [selectedValue, setSelectedValue] = React.useState(times[1]);
  let url = "http://192.168.208.130:4901/api/v1/countries/getCountries"
  

  axios.get(url).then( res => {
    console.log(res.data)
      res.data.forEach(function(item) {
        if(!options.includes(item)) {
          options.push(item)
        }
      })
    });
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleDialogClose = (value) => {
    setOpen(false);
    setSelectedValue(value);
    window.open('http://localhost:3000/laws/' + selectedCountry + '/' + value);
  };
  const divRef = React.useRef();

  // Menu
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [selectedCountry, setSelectedCountry] = React.useState("");
  const open = Boolean(anchorEl);

  const handleButtonClick = (event) => {
    setAnchorEl(divRef.current);
  };

  const handleMenuItemClick = (event, option) => {
    setSelectedCountry(option);
    setAnchorEl(null);
    handleClickOpen();
    setOpen(true);
    console.log(option);
    handleClose();
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div ref = {divRef}>
      <Button 
        aria-label="more"
        aria-controls="long-menu"
        aria-haspopup="true"
        variant="contained" 
        onClick={handleButtonClick}
        color="primary"> 
        Select a Country
      </Button>

      <Menu
        id="long-menu"
        anchorEl={anchorEl}
        keepMounted
        open={open}
        onClose={handleClose}
        PaperProps={{
          style: {
            maxHeight: ITEM_HEIGHT * 4.5,
            width: '20ch',
          },
        }}
      >
        {options.map((option) => (
          <MenuItem 
            key={option} 
            selected={option === 'United States'} 
            onClick={(event) => handleMenuItemClick(event, option)}>
                {option}
          </MenuItem>
        ))}
      </Menu>

      <Typography variant="subtitle1">Selected: {selectedValue}</Typography>
      <SimpleDialog selectedValue={selectedValue} open={openDio} onClose={handleDialogClose} />
    </div>
  );
}
