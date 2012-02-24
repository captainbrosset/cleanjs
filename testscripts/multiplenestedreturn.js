function getFallbackMarkup (eventName, delegateId, wrapTarget) {
	if (aria.core.Browser.isIE) {
		this.getFallbackMarkup = function (eventName, delegateId, wrapTarget) {
			wrapTarget = wrapTarget ? "true" : "false";
			return " on" + eventName + "=\"aria.utils.Delegate.directCall(event, '" + delegateId + "', " + wrapTarget + ", this)\"";
		}
	} else {
		this.getFallbackMarkup = function (eventName, delegateId, wrapTarget) { 
			var calledFunction = "directCall";
			wrapTarget = wrapTarget ? "true" : "false";
			if ('mouseleave' == eventName || 'mouseenter' == eventName) {
				// Mouseleave/enter exists only in IE, we can emulate them in all other browsers
				eventName = 'mouseleave' == eventName ? 'mouseout' : 'mouseover';
				calledFunction = "mouseMovement";
			}
			return " on" + eventName + "=\"aria.utils.Delegate." + calledFunction + "(event, '" + delegateId + "', " + wrapTarget + ", this)\"";
		}
	}
	return this.getFallbackMarkup(eventName, delegateId, wrapTarget);
};