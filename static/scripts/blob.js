'use strict'

// select html elements
const blob = document.querySelector("#blob");
const dispaly = document.querySelector("#file-preview-audio");

// declare variables for blob values
let x1 = 150;
let x2 = 200;
let x3 = 50;
let x4 = 0;

// declare variables for blob values dirctions
let dir = 1.5;
let dir2 = -1.5;

// current frame that being scheduled in the requestAnimationFrame function
let scheduleFrame = null;


// update blob values
function update()
{
    // increase/decrease values based on the dircation
    x1 += dir;
    x2 += dir;
    x3 += dir2;
    x4 += dir2;

    // change the dircation for the first value in the blob up-right
    if (x1 > 180 || x1 < 120)
    {
        dir *= -1;
    }

    // change the dircation for the first value in the blob bottom-right
    if (x2 > 230 || x2 < 170)
    {
        dir *= 1;
    }

    // change the dircation for the first value in the blob bottom-left

    if (x3 > 80 || x3 < 20)
    {
        dir2 *= -1;
    }

    // change the dircation for the first value in the blob up-left
    if (x4 > 30 || x4 < -30)
    {
        dir2 *= 1;
    }

    // set up the new values
    blob.setAttribute("d", `M 100, 20
            C ${x1}, 10 190, 50 180, 100
            C ${x2}, 150 150, 190 100, 180
            C ${x3}, 200 10, 150 20, 100
            C ${x4}, 50 50, 10 100, 20 Z
            "`);

    
    // take the current scheduledFrame
    // know the requestAnimationFrame from ChatGpt
    scheduleFrame = requestAnimationFrame(update);
}


// call the update function if and only if the audio is started to play
dispaly.addEventListener("play", function()
{
    update();
});


// cancel the current scheduled frame if and only if the audio is paused
dispaly.addEventListener("pause", function()
{
    cancelAnimationFrame(scheduleFrame);
    scheduleFrame = null;
});
