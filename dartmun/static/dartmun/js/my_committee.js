// motion validation code
let votesFor = document.getElementById("votes-for");
let votesAgainst = document.getElementById("votes-against");
let voteAlert = document.getElementById("vote-alert");
let delCount = document.getElementById("del-count");
let voteButton = document.getElementById("vote-button");

function validate_votes(event){
  if ((parseInt(votesFor.value, 10) + parseInt(votesAgainst.value, 10)) > delCount.value){
    voteAlert.innerHTML = "The number of votes exceeds the number of delegates present."
    voteAlert.hidden = false;
    voteButton.disabled = true;
  }
  else{
    voteAlert.hidden = true;
    voteButton.disabled = false;
  }
}

votesFor.addEventListener('input', validate_votes)
votesAgainst.addEventListener('input', validate_votes)

// add motion form code
let selectedMotion = document.getElementById("selected-motion");
let motionAlert = document.getElementById("motion-alert");

let duration = document.getElementById("duration");
let durationValue = document.getElementById("duration-value");
let speakTime = document.getElementById("speak-time");
let timeValue = document.getElementById("time-value");
let purpose = document.getElementById("purpose");
let purposeValue = document.getElementById("purpose-value");
let wp = document.getElementById("wp");
let selectedWP = document.getElementById("selected-WP");
let reso = document.getElementById("reso");
let selectedReso = document.getElementById("selected-reso");
let amend = document.getElementById("amend");
let selectedAmend = document.getElementById("selected-amend");
let topic = document.getElementById("topic");
let selectedTopic = document.getElementById("selected-topic");
let discretion = document.getElementById("discretion");
let vote = document.getElementById("vote");


function hideSubmitBtns(element, value){
  if (!element.hidden && (value.value == 0 || value.value == "")) {
    discretion.disabled = true;
    vote.disabled = true;
  }
  else {
    discretion.disabled = false;
    vote.disabled = false;
  }
}

function submitBtnsAfterEdit(event){
  if (!event.target.hidden && event.target.value != 0){
    discretion.disabled = false;
    vote.disabled = false;
  }
  else{
    discretion.disabled = true;
    vote.disabled = true;
  }
}

function showInputs(event){
  const hasDuration =["Move into a Moderated Caucus", "Move into an Unmoderated Caucus"]
  const hasSpeakTime =["Move into a Moderated Caucus", "Set the Speaking Time"]
  let motionName = selectedMotion.options[selectedMotion.selectedIndex].text;
  speakTime.hidden = !hasSpeakTime.includes(motionName);
  hideSubmitBtns(speakTime, timeValue);
  purpose.hidden = motionName !== "Move into a Moderated Caucus";
  hideSubmitBtns(purpose, purposeValue);
  duration.hidden = !hasDuration.includes(motionName);
  hideSubmitBtns(duration, durationValue);
  topic.hidden = motionName !== "Set a Working Agenda";
  hideSubmitBtns(topic, selectedTopic);
  wp.hidden = motionName !== "Introduce a Working Paper";
  if (!wp.hidden)
    hideSubmitBtns(wp, selectedWP);
  reso.hidden = motionName !== "Introduce a Resolution";
  if (!reso.hidden)
    hideSubmitBtns(reso, selectedReso);
  amend.hidden = motionName !== "Introduce an Amendment";
  if (!amend.hidden)
    hideSubmitBtns(amend, selectedAmend);
}

function divisibility_check(event) {
  let motionName = selectedMotion.options[selectedMotion.selectedIndex].text;
  if (motionName === "Move into a Moderated Caucus") {
    if (!durationValue.value || !timeValue.value || (durationValue.value == 0 || timeValue.value == 0) || ! purposeValue.value) {
      discretion.disabled = true;
      vote.disabled = true;
    } else if (durationValue.value * 60 % timeValue.value) {
      motionAlert.innerHTML = "The duration and speaking time must be divisible.";
      motionAlert.hidden = false;
      discretion.disabled = true;
      vote.disabled = true;
    } else {
      motionAlert.hidden = true;
      discretion.disabled = false;
      vote.disabled = false;
    }
  }
}


selectedMotion.addEventListener('input', showInputs);
selectedTopic.addEventListener('input', showInputs);
selectedWP.addEventListener('input', showInputs);
selectedReso.addEventListener('input', showInputs);
selectedAmend.addEventListener('input', showInputs);
duration.addEventListener('input', submitBtnsAfterEdit);
speakTime.addEventListener('input', submitBtnsAfterEdit);
duration.addEventListener('input', divisibility_check);
speakTime.addEventListener('input', divisibility_check);
purposeValue.addEventListener('input', submitBtnsAfterEdit);


// slider code
let slider = document.getElementById("myRange");
let slider2 = document.getElementById("myRange2");
let output = document.getElementById("score");
let output2 = document.getElementById("score2");
output.innerHTML = slider.value; // Display the default slider value
output2.innerHTML = slider2.value;

// update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
  output.innerHTML = this.value;
  if (this.value == 0)
    output.style.color = "black";
  else if (this.value == 1)
    output.style.color = "red";
  else if (this.value == 2)
    output.style.color = "orange";
  else if (this.value == 3)
    output.style.color = "gold";
  else
    output.style.color = "green";
}

slider2.oninput = function() {
  output2.innerHTML = this.value;
  if (this.value == 0)
    output2.style.color = "black";
  else if (this.value == 1)
    output2.style.color = "red";
  else if (this.value == 2)
    output2.style.color = "orange";
  else if (this.value == 3)
    output2.style.color = "gold";
  else
    output2.style.color = "green";
}
