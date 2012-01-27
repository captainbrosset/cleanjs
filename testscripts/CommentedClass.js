var my = {package: {}}

/**
 * @class my.package.MyClass
 * This class is used to store the data model on the client, using local storage or session storage depending on the case.
 * If the setting is set to LOCAL, then local storage is used, otherwise session storage is used
 */
my.package.MyClass = function(setting) {
	this.setting = setting;
};

// Set the setting
my.package.MyClass.prototype.setSetting = function(setting) {
	this._setting = setting;
};