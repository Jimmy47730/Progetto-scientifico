const btn_home = document.getElementById("logo");
const btn_strumenti = document.getElementById("strumenti");
const btn_progetto = document.getElementById("progetto");
const btn_risultati = document.getElementById("risultati");
const btn_team = document.getElementById("team");
const btn_download = document.getElementById("download");

const btn_audio_comparator = document.getElementById('di-piu-btn1');
const target_audio_comparator = document.getElementById('audio-comparator-info');
const btn_zeromirror_creator = document.getElementById('di-piu-btn2');
const target_zeromirror_creator = document.getElementById('zeromirror-creator-info');

btn_home.addEventListener("click", function () {
	window.open("/", "_self");
});

btn_strumenti.addEventListener("click", function () {
	window.open("/strumenti", "_self");
});

btn_progetto.addEventListener("click", function () {
	window.open("/progetto", "_self");
});

btn_risultati.addEventListener("click", function () {
	window.open("/risultati", "_self");
});

btn_team.addEventListener("click", function () {
	window.open("/team", "_self");
});

btn_download.addEventListener("click", function () {
	window.open("/download", "_self");
});

btn_audio_comparator.addEventListener('click', function (e) {
	e.preventDefault();
	target_audio_comparator.scrollIntoView({ behavior: 'smooth', block: 'start' });
});

btn_zeromirror_creator.addEventListener('click', function (e) {
	e.preventDefault();
	target_zeromirror_creator.scrollIntoView({ behavior: 'smooth', block: 'start' });
});