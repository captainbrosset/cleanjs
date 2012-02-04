function Apple (type) {
    this.type = type;
    this.color = "red";
    this.a = 1;
}

Apple.prototype.getInfo = function() {
    return this.color + ' ' + this.type + ' apple';
};