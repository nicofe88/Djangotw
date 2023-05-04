let loadUserData = () => {
	return (
		JSON.parse(localStorage.getItem("data")) || {
			loggedInUser: "null",
			loggedInName: "null"
		}
	);
};

let appState = loadUserData();

const getData = async () => {

	document.getElementById("displayHandle").innerText =
		`@${appState.loggedInUser}`;
	document.getElementById("displayName").innerText =
		`${appState.loggedInName}`;
}

getData();

let textArea = document.getElementById('contentsBox');
let tweetList = []
let id = 0;

let countChar = () => {
	let remainingChar = 140 - textArea.value.length;
	if (remainingChar < 0) {
		document.getElementById('charCountArea').innerHTML = `${remainingChar}`.fontcolor('red');

	} else {
		document.getElementById('charCountArea').innerHTML = `${remainingChar}`.fontcolor('white');

	}
}

textArea.addEventListener('input', countChar);



function validateForm() {
    let x = document.forms["valForm"]["{{ form.username }}"].value;
    let y = document.forms["valForm"]["{{ form.password }}"].value;

    if (x == "") {
        alert("Por favor, complete el campo Username");
        return false;
    }
    if (y == "") {
        alert("Por favor, complete el campo Password");
        return false;
    }

    alert("Muchas gracias. Nos contactaremos a la brevedad.");

}