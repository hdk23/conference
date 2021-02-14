var slider = document.getElementById("myRange");
var output = document.getElementById("score");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
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