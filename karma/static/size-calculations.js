
function getPxFromVw(nbr, max) {
	var viewportWidth = document.documentElement.clientWidth;
	var px = nbr*viewportWidth/100;
	return Math.min(px, max);
}