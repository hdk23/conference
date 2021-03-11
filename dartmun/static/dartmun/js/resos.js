console.log();

let wpSponsors = document.querySelectorAll("#wp-sponsor-list > div");
let wpSignatories = document.querySelectorAll("#wp-signatory-list > div");
let resoSponsors = document.querySelectorAll("#reso-sponsor-list > div");
let resoSignatories = document.querySelectorAll("#reso-signatory-list > div");

function toggleSponSig(event){
    console.log(event.target.parentNode.id);
    if (event.target.parentNode.id === `sponsor${event.target.value}`){
        let signatory = document.querySelector(`#signatory${event.target.value}`);
        signatory.hidden = event.target.checked;
    }
    else if (event.target.parentNode.id === `signatory${event.target.value}`){
        let sponsor = document.querySelector(`#sponsor${event.target.value}`);
        sponsor.hidden = event.target.checked;
    }
    else if (event.target.parentNode.id === `reso-sponsor${event.target.value}`){
        let signatory = document.querySelector(`#reso-signatory${event.target.value}`);
        signatory.hidden = event.target.checked;
    }
    else{
        let sponsor = document.querySelector(`#reso-sponsor${event.target.value}`);
        sponsor.hidden = event.target.checked;
    }
}

for (let sponsor of wpSponsors){
    sponsor.addEventListener('change', toggleSponSig);
}

for (let signatory of wpSignatories){
    signatory.addEventListener('change', toggleSponSig);
}

for (let sponsor of resoSponsors){
    sponsor.addEventListener('change', toggleSponSig);
}

for (let signatory of resoSignatories){
    signatory.addEventListener('change', toggleSponSig);
}