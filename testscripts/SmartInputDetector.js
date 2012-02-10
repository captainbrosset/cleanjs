if(!malica) {
	var malica = {};
}

/**
 * The SmartInputDetector is really not that smart in fact for now
 * It can only detect whether what is passed matches a URL to add a present or if it is just a piece of text description
 */
malica.SmartInputDetector = {
	/**
	 * @param {String} inputText The text as typed by the user, which we want to detect from
	 * @return {Object} Returns an object with 2 properties: url and description,
	 * depending on what we could parse, only one, both or none of them can be defined
	 */
	detect: function(inputText) {
		var result = {
			url: null,
			description: inputText
		};
		
		result = this._checkForUrlPatternAndUpdateObject(inputText, /http[s]*:\/\/[a-zA-Z0-9-\.\?=\/&_]+/igm, result)
		if(!result.url) {
			result = this._checkForUrlPatternAndUpdateObject(inputText, /www[a-zA-Z0-9-\.\?=\/&_]+/igm, result)
			if(result.url) {
				result.url = "http://" + result.url;
			}
		}
		
		return result;
	},
	
	_checkForUrlPatternAndUpdateObject: function(inputText, pattern, result) {
		var matches = inputText.match(pattern);
		if(matches) {
			// Only take first one for now
			result.url = matches[0];
			result.description = result.description.replace(result.url, "")
		}
		return result;
	}
};

//var res1 = malica.SmartInputDetector.detect("this is the description of a present");
/*
res1.url = undefined;
res1.description = "this is the description of a present";
*/
//var res2 = malica.SmartInputDetector.detect("www.amazon.fr/dvds/test");
/*
res2.url = "http://www.amazon.fr/dvds/test";
res2.description = undefined;
*/
//var res3 = malica.SmartInputDetector.detect("http://greatstuff.org/products/stereo-34-124.html?test=true");
/*
res3.url = "http://greatstuff.org/products/stereo-34-124.html?test=true";
res3.description = undefined;
*/
//var res4 = malica.SmartInputDetector.detect("And this is a tricky case with a description and a URL www.test.com/presents.html");
/*
res4.url = "http://www.test.com/presents.html";
res4.description = ""And this is a tricky case with a description and a URL";
*/
//var res5 = malica.SmartInputDetector.detect("Sometimes the url http://google.com/test/another/path?to=a&file is mixed into the description and there can be \n carriage returns");
/*
res5.url = "http://google.com/test/another/path?to=a&file";
res5.description = "Sometimes the url is mixed into the description and there can be \n carriage returns";
*/