'use strict'

const profile = document.querySelector(".profile");
const addPicture = document.querySelector("#add-pic-input");


// if user is already added a profile picture
fetch('/profile-pic').then(response => response.json()).then(function(data){
    profile.style.backgroundImage = `url("../${data["path"]}")`
});


// if user is new and wants to add or change a profile picture
addPicture.addEventListener("change", function()
{
    // take the file from the input file element
    const file = addPicture.files[0]

    // check file fromat
    const fileNameFormat = file.name.slice(-4);

    if(fileNameFormat === ".png" || fileNameFormat === ".jpg")
    {
        // prepare the body of the http for the image file
        const formData = new FormData()
        formData.append("picture", file)
        
        // request the server
        fetch('/profile-pic', {
            method: 'POST',
            body: formData
        }).then(response => response.json()).then(function(data){

            // display the image
            profile.style.backgroundImage = `url("../${data["path"]}")`
        });
    }
});