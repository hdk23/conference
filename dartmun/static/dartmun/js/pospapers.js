
var points = document.querySelectorAll("#scoring-sheet > tbody > tr > td > .points")
var paperScore = document.querySelector("#paper-score")

function updateTotal(event){
    var total = 0;
    for (var score of points){
        if (score.value != null)
            total += score.value;
    }
    paperScore.innerHTML = total;
    console.log(total);
}


for (var criterion of points){
    criterion.addEventListener('input', updateTotal);
}
