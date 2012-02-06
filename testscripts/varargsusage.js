/**
 * This will be useful to check if the reviewers detect that multiply is used inside the function
 * that a and b as well but c not
 */
function computeSomething(multiply) {
	var a = multiply/2;
	var b = a*multiply+(multiply/multiply)
	var c = a+b;
	return b;
}