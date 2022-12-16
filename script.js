// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyA4qtCd99knAzdZIPZhPqniE5dX0hyxeb0",
    authDomain: "securitycamera-be9c3.firebaseapp.com",
    databaseURL: "https://securitycamera-be9c3-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "securitycamera-be9c3",
    storageBucket: "securitycamera-be9c3.appspot.com",
    messagingSenderId: "825019759005",
    appId: "1:825019759005:web:b357a43ad2ce4c8fa79774"
};

firebase.initializeApp(firebaseConfig);

// Get a reference to the file storage service
const storage = firebase.storage();
// Get a reference to the database service
const database = firebase.database();

// Create camera database reference
const camRef = database.ref("file");

// Sync on any updates to the DB. THIS CODE RUNS EVERY TIME AN UPDATE OCCURS ON THE DB.
camRef.limitToLast(1).on("value", function(snapshot) {
  snapshot.forEach(function(childSnapshot) {
    const image = childSnapshot.val()["image"];
    const time = childSnapshot.val()["timestamp"];
    const storageRef = storage.ref(image);

    storageRef
      .getDownloadURL()
      .then(function(url) {
        console.log(url);
        document.getElementById("photo").src = url;
        document.getElementById("time").innerText = time;
      })
      .catch(function(error) {
        console.log(error);
      });
  });
});