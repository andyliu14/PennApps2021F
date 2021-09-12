import logo from './logo.svg';
import './App.css';
import SignInScreen from './SignInScreen';
import React, { Component } from 'react';
import { BrowserRouter as Router, Switch, Route, BrowserRouter } from 'react-router-dom';
import HomeScreen from './HomeScreen';
import LawListing from './lawListing';

function App() {
  return (
    <div>
      <BrowserRouter>
      <Switch>
        {/* If the current URL is /about, this route is rendered
            while the rest are ignored */}
        <Route path="/login">
          <SignInScreen >
          </SignInScreen>
        </Route>

        {/* Note how these two routes are ordered. The more specific
            path="/contact/:id" comes before path="/contact" so that
            route will render when viewing an individual contact */}
        {/* <Route path="/contact/:id">
          <Contact />
        </Route> */}

        
        <Route exact path = {"/laws/:countryName/:filter"} component = {LawListing}/>   

        {/* If none of the previous routes render anything,
            this route acts as a fallback.

            Important: A route with path="/" will *always* match
            the URL because all URLs begin with a /. So that's
            why we put this one last of all */}
        <Route path="/">
          <HomeScreen></HomeScreen>
        </Route>

      </Switch>
      </BrowserRouter>
    </div>

  );
}

export default App;
