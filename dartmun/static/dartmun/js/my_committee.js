// motion validation code
var votes_for = document.getElementById("votes-for");
var votes_against = document.getElementById("votes-against");
var vote_alert = document.getElementById("vote-alert");
var del_count = document.getElementById("del-count");

function validate_votes(event){
  if ((parseInt(votes_for.value, 10) + parseInt(votes_against.value, 10)) > del_count.value){
    vote_alert.innerHTML = "The number of votes exceeds the number of delegates present."
    vote_alert.hidden = false;
  }
  else
    vote_alert.hidden = true;
}

votes_for.addEventListener('input', validate_votes)
votes_against.addEventListener('input', validate_votes)

// add motion form code
var selectedMotion = document.getElementById("selected-motion");
var motion_alert = document.getElementById("motion-alert");

var duration = document.getElementById("duration");
var speakTime = document.getElementById("speak-time");
var duration_value = document.getElementById("duration-value");
var time_value = document.getElementById("time-value");
var purpose = document.getElementById("purpose");
var topic = document.getElementById("topic");
var selectedTopic = document.getElementById("selected-topic");

function show_inputs(event){
  const has_duration =["Move into a Moderated Caucus", "Move into an Unmoderated Caucus"]
  const has_speaktime =["Move into a Moderated Caucus", "Set the Speaking Time"]
  var motion_name = selectedMotion.options[selectedMotion.selectedIndex].text
  duration.hidden = !has_duration.includes(motion_name);
  speakTime.hidden = !has_speaktime.includes(motion_name);
  purpose.hidden = motion_name != "Move into a Moderated Caucus";
  topic.hidden = motion_name != "Set a Working Agenda";
}

function divisibility_check(event){
  if (duration_value.value * 60 % time_value.value){
    motion_alert.innerHTML = "The duration and speaking time must be divisible.";
    motion_alert.hidden = false;
  }
  else{
    motion_alert.hidden = true;
  }
}

selectedMotion.addEventListener('input', show_inputs)
selectedTopic.addEventListener('input', show_inputs)
duration.addEventListener('input', divisibility_check)
speakTime.addEventListener('input', divisibility_check)

// slider code
var slider = document.getElementById("myRange");
var output = document.getElementById("score");
output.innerHTML = slider.value; // Display the default slider value

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

