/**
 * Begin chainable HTML
 * @param html whatever html elements they want, e.g. "<div class='content'><p>"
 * @constructor
 */
function ChainableHtmlOptions() {
    this.id = "";
    this.class = "";
    this.style = "";
    this.onclick = "";
    this.type = "";
    this.placeholder = "";
}
ChainableHtmlOptions.prototype.get = function(key) {
    return (this.hasOwnProperty(key) ? this[key] : "");
};
function ChainableHtml(html) {
    if (html)
        this.html = html;
    else
        this.html = "";
}
function _insertChain(existingHtml, tag, options) {
    return (existingHtml + "<" + tag + " id='" + options.get('id') + "' class='" + options.get('class') + "' style='" + options.get('style') + "'>");
}
function _insertInputChain(existingHtml, _id, _class, _type, _placeholder, _style) {
    return (existingHtml + "<input id='" + _id + "' class='" + _class + "' type='" + _type + "' placeholder='" + _placeholder + "' style='" + _style + "'/>");
}
function _endChain(existingHtml, tag) {
    return (existingHtml + "</" + tag + ">");
}
ChainableHtml.prototype.div = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "div", _id, _class, _style);
};
ChainableHtml.prototype.ediv = function() {
    this.html = _endChain(this.html, "div");
};
ChainableHtml.prototype.p = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "p", _id, _class, _style);
};
ChainableHtml.prototype.ep = function() {
    this.html = _endChain(this.html, "p");
};
ChainableHtml.prototype.span = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "span", _id, _class, _style);
};
ChainableHtml.prototype.espan = function() {
    this.html = _endChain("span");
};
ChainableHtml.prototype.h1 = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "h1", _id, _class, _style);
};
ChainableHtml.prototype.eh1 = function() {
    this.html = _endChain(this.html, "h1");
};
ChainableHtml.prototype.h2 = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "h2", _id, _class, _style);
};
ChainableHtml.prototype.eh2 = function() {
    this.html = _endChain(this.html, "h2");
};
ChainableHtml.prototype.h3 = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "h3", _id, _class, _style);
};
ChainableHtml.prototype.eh3 = function() {
    this.html = _endChain(this.html, "h3");
};
ChainableHtml.prototype.h4 = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "h4", _id, _class, _style);
};
ChainableHtml.prototype.eh4 = function() {
    this.html = _endChain(this.html, "h4");
};
ChainableHtml.prototype.input = function(_id, _class, _type, _placeholder, _style) {
    this.html = _insertInputChain(_id, _class, _type, _placeholder, _style);
};
ChainableHtml.prototype.ul = function(_id, _class, _style) {
    this.html = _insertChain(this.html, "ul", _id, _class, _style);
};
ChainableHtml.prototype.eul = function(_id, _class, _style) {
    this.html = _endChain("ul");
};
ChainableHtml.prototype.li = function(_id, _class, _style, _onclick, _text) {
    this.html = _insertChainClick(this.html, "li", _id, _class, _style, _onclick, _text);
};
ChainableHtml.prototype.eli = function() {
    this.html = _endChain("li");
};