// Import FirebaseAuth and firebase.
import React, { useEffect, useState } from 'react';
import StyledFirebaseAuth from 'react-firebaseui/StyledFirebaseAuth';
import firebase from 'firebase';
import * as firebaseui from 'firebaseui'
import 'firebaseui/dist/firebaseui.css'
import VoteScreen from './voteScreen';

// Configure Firebase.
const config = {
    apiKey: "AIzaSyAcVtK8cNXHh8YzJNxLg1RWN9axL66QA9A",
    authDomain: "ikmr-ce98c.firebaseapp.com",
    databaseURL: "https://ikmr-ce98c-default-rtdb.firebaseio.com",
    projectId: "ikmr-ce98c",
    storageBucket: "ikmr-ce98c.appspot.com",
    messagingSenderId: "1049675605118",
    appId: "1:1049675605118:web:174953194f15d49d58e42f",
    measurementId: "G-9H3RKHXYKD"
  };
firebase.initializeApp(config);
firebaseui.auth.DisableSignUpConfig = {
    status: true
}

const disableconfig = {
    status: true
}


// Configure FirebaseUI.
const uiConfig = {
  // Popup signin flow rather than redirect flow.
  signInFlow: 'redirect',
  // We will display Google and Facebook as auth providers.
  signInOptions: [ {
    provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
    disableSignup: disableconfig
  }
  ],
  callbacks: {
    // Avoid redirects after sign-in.
    signInSuccessWithAuthResult: () => false,
  },
};

function SignInScreen() {
  const [isSignedIn, setIsSignedIn] = useState(false); // Local signed-in state.

  // Listen to the Firebase Auth state and set the local state.
  useEffect(() => {
    const unregisterAuthObserver = firebase.auth().onAuthStateChanged(user => {
      setIsSignedIn(!!user);
    });
    return () => unregisterAuthObserver(); // Make sure we un-register Firebase observers when the component unmounts.
  }, []);

  if (!isSignedIn) {
    return (
      <div>
        <StyledFirebaseAuth uiConfig={uiConfig} firebaseAuth={firebase.auth()} />
      </div>
    );
  }
  firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
    console.log(idToken)
  }).catch(function(error) {
    // Handle error
  });
  
  return (
      <VoteScreen></VoteScreen>
    
  );
}

export default SignInScreen;