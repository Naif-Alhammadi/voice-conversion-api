'use strict'

// file 
const inputFile = document.querySelector("#input-file");
const fileName = document.querySelector("#file-name");
let dragDrop = document.querySelector(".drag-drop-container");

// lists that can be done for the audio
const conversionList = document.querySelectorAll(".conversion-list");
let convertTo = "";
let userFile;

// display if the file is being selected or not
const listParagraph = document.querySelector("#conversion-p");

// listen for each valid audio conversion
conversionList.forEach(list => {
    list.addEventListener("click", function(e){
        convertTo = e.target.textContent;
        
        // if user choose a file
        if (userFile)
        {
            value = document.querySelector("#innumber").value;
            listParagraph.innerHTML = "";

            // process the voice according to the user's chosen list
            const formData = new FormData();
            formData.append("file" , userFile);
            formData.append("convertTo", convertTo);
            formData.append("value", value);


            fetch("/process",{
                method: "POST",
                body: formData
            }).then(response => response.json()).then(data => {

                // display the converted audio in the file preview section
                document.querySelector('#file-preview-audio').src = "";
                document.querySelector('#file-preview-audio').src = data["process_success"];


            }).catch(error => console.log(error));
        }

        // if user did not choose a file yet
        else 
        {
            listParagraph.innerHTML = "Choose file first";
        }
    });
});


// display the previous audio in wavesufer format
const wavesurfer = WaveSurfer.create({
    container: '#waveform', // connect the wave with the dev
    waveColor: '#1e0af8',   // the primary color
    progressColor: '#745ce9', // color when turing on
    cursorColor: '#adacb3',   // indctor color
    barWidth: 2,            // columns widht
    barRadius: 3            // around the edges
});


// on off button
document.querySelector('#playButton').addEventListener('click', () => {
    wavesurfer.playPause();
});


// drag drop file
const checkFileExtention = function(fileName)
{
    if(fileName.name.slice(-4) !== '.wav')
        return false

    return true
}

dragDrop.addEventListener('dragover', function(e)
{
    e.preventDefault();
});

dragDrop.addEventListener('drop', function(e)
{
    e.preventDefault();
    const fileSrc = document.querySelector('#file-preview-audio');
    const file = e.dataTransfer.files[0];
    const dropMessage = document.querySelector("#drag-drop-message");
    if(checkFileExtention(file))
    {
        fileSrc.src = URL.createObjectURL(file);
        fileName.innerHTML = file.name;
        dropMessage.innerHTML = "";
        userFile = file;
        wavesurfer.load(URL.createObjectURL(file));
    }

    else {
        dropMessage.innerHTML = "You have to enter a .wav file";
    }
});


// input file manually
inputFile.addEventListener("change", function(){
    const file = inputFile.files[0];
    const fileSrc = document.querySelector('#file-preview-audio');
    const dropMessage = document.querySelector("#drag-drop-message");

    if(checkFileExtention(file))
    {
        fileSrc.src = URL.createObjectURL(file);
        wavesurfer.load(URL.createObjectURL(file));
        dropMessage.innerHTML = "";
        fileName.innerHTML = file.name;
        userFile = file;
    }

    else {
        dropMessage.innerHTML = "You have to enter a .wav file";
    }
    
});

