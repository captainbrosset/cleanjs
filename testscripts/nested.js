function initSomeStuff() {
    var test = document.getElementById("test");
    var self = this;
    test.onclick = function() {
        alert(self._prop)
    }
};