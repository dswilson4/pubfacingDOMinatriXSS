const toDomContentLoaded = performance.now();

var meta = document.createElement('meta');
//https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src

meta.httpEquiv = 'Content-Security-Policy';

// we need to enable unsafe-eval so we can rewrite the static inline event handlers to external scripta
meta.content = "script-src 'self' 'unsafe-inline' 'disable-dynamic' 'unsafe-eval' " + " * ";

document.getElementsByTagName('head')[0].appendChild(meta);

var tag = "*";
var tags = document.getElementsByTagName(tag);
console.log(tags);

console.log('before');

var original = document.createElement;

//https://developer.mozilla.org/en-US/docs/Web/API/Window/crypto
var array = new Uint32Array(1);
window.crypto.getRandomValues(array);

// (function hook) the document.createElement() function is overridden.
document.createElement = function (tag) {

      // call the function (createElement)...
      // from original document object. This needs to work for all tags,
      // so we createElement regardless of tag
      var element = original.call(document, tag);

      // only for script tags should a nonce value be set.
      if (tag.toLowerCase() === 'script') {
            element.setAttribute("nonce", array[0]);
            // element.setAttribute("nonceTest", (array[0] + 1).toString());

      }
      return element;
};

function afterDOMloaded() {

      meta.setAttribute("http-equiv", "Content-Security-Policy");

      // we need to enable unsafe-eval so we can rewrite the static inline event handlers to external scripta
      meta.setAttribute("content", "script-src 'unsafe-inline' 'unsafe-eval' " + "'nonce-" + array[0].toString() + "' *");

      // ------------ PERFORMANCE INDEX ------------
      console.log("before inline event handler conversion");
      const start = performance.now();

      // search by wildcard tag...should grab all nodes
      var tag = "*";
      var tags = document.getElementsByTagName(tag);
      // console.log(tags);

      for (var i=0; i<tags.length; i++) {

            var attributeNames = tags[i].getAttributeNames();

            var eventHandlerIndicies = [];
            var eventType = [];

            //populate array of indicies saving names of event handlers
            //specific to current DOM element
            for (j = 0; j < attributeNames.length; j++) {
                  // if (attributeNames[j].includes('on')) {
                  var attributeNameLength = attributeNames[j].length;
                  // check to ensure "onXXXX" is the format of the inline eventhandler
                  // in other words, the eventhandler should start with 'on'
                  // and should be greater than 2 in length.
                  if (attributeNames[j][0] == 'o' && attributeNames[j][1] == "n" && attributeNameLength > 2) {
                        eventHandlerIndicies.push(j);
                        eventType.push(attributeNames[j].slice(2));
                  }
            }

            // We need to loop through all attributes that are infact
            // inline event handlers
            for (z = 0; z < eventHandlerIndicies.length; z ++) {
                  var handler = attributeNames[eventHandlerIndicies[z]];
                  // console.log(handler);
                  var inlineString = tags[i].getAttribute(handler);
                  if (inlineString && typeof inlineString == "string") {
                        //create handler function
                        var fn = new Function(inlineString)

                        //actually add the eventListener to the tag
                        tags[i].addEventListener(eventType[z], fn, false);

                        //remove the inline handler
                        tags[i].removeAttribute(handler,0);
                  }
            }
      }

      const end = performance.now();
      console.log("After inline event handler conversion");

      let time = end - start; //in milliseconds
      console.log("Conversion time: " + time + ": " + window.location);

      // Second action...assigning nonce
      meta.setAttribute("http-equiv", "Content-Security-Policy");

      // We ABSOLUTELY MUST disable unsafe-eval at this point... only was necessary for the use
      // of new Function(...) for the conversion of inline event handlers (inlineString) to external event handlers...
      meta.setAttribute("content", "script-src 'self' 'unsafe-inline' " + "'nonce-" + array[0].toString() + "' " + "*")

}

window.addEventListener('DOMContentLoaded', (event) => {
      const domContentLoadedPoint = performance.now();
      let timeToDomContentLoaded = domContentLoadedPoint - toDomContentLoaded;
      console.log("Time to DOMContentLoaded: " + timeToDomContentLoaded + ": " + window.location + ": " + "test");
      afterDOMloaded();
});
