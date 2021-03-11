
let points = document.querySelectorAll("#scoring-sheet > tbody > tr > td > .points")
let paperScore = document.querySelector("#paper-score")

function updateTotal(event){
    let total = 0;
    for (let score of points){
        if (score.value != null)
            total += score.value;
    }
    paperScore.innerHTML = total;
    console.log(total);
}


for (var criterion of points){
    criterion.addEventListener('change', updateTotal);
}
