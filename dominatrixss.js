// keep this around...may be useful for overriding any
// other methods from the original document object...
var original = document.createElement;

//https://developer.mozilla.org/en-US/docs/Web/API/Window/crypto
var array = new Uint32Array(1);
window.crypto.getRandomValues(array);
// console.log(array[0]);

// (function hook) the document.createElement() function is overridden.
// src: https://stackoverflow.com/questions/50768596/hook-document-createelement-script-to-change-srcr
document.createElement = function (tag) {
      // call the function (createElement)...
      // from original document object. This needs to work for all tags,
      // so we createElement regardless of tag
      var element = original.call(document, tag);
      // console.log('Confirms document.createElement has been modified');

      // only for script tags should a nonce value be set.
      if (tag.toLowerCase() === 'script') {
            element.setAttribute("nonce", array[0]);
            // element.setAttribute("nonceTest", (array[0] + 1).toString());
            // console.log('in control structure to set nonce for script...');
      }
      return element;
};

// we need to check if the dom content has loaded...
// it is the 'interactive' specification that indicate DOM content has loaded
// src: https://stackoverflow.com/questions/9457891/how-to-detect-if-domcontentloaded-was-fired

function afterDOMloaded() {
      var meta = document.createElement('meta');
      //https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src

      meta.httpEquiv = 'Content-Security-Policy';

      // we need to enable unsafe-eval so we can rewrite the static inline event handlers to external scripta
      meta.content= "script-src 'unsafe-inline' 'unsafe-eval' " + "'nonce-" + array[0].toString() + "' *";

      document.getElementsByTagName('head')[0].appendChild(meta);

      // search by wildcard tag...should grab all nodes
      var tag = "*";
      var tags = document.getElementsByTagName(tag);
      // console.log(tags);

      for (var i=0; i<tags.length; i++) {

            // we want to see all the attribute names of each node...
            // this will allow us to tell if a given attribute is an event handler...
            // ex: onclick=myfunc()
            var attributeNames = tags[i].getAttributeNames();

            // console.log('---attributeNames---')
            // console.log(attributeNames)
            // console.log('---attributeNames---')

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

      // Second action...assigning nonce
      meta.setAttribute("http-equiv", "Content-Security-Policy");
      // meta.setAttribute("content", "script-src " + "'nonce-" + array[0].toString() + "'");

      // We ABSOLUTELY MUST disable unsafe-eval at this point... only was necessary for the use
      // of new Function(...) for the conversion of inline event handlers (inlineString) to external event handlers...
      meta.setAttribute("content", "script-src 'self' 'unsafe-inline' " + "'nonce-" + array[0].toString() + "' " + "*")

}

if (document.readyState === 'loading') {  // Loading hasn't finished yet
document.addEventListener('DOMContentLoaded', afterDOMloaded);
} else {  // `DOMContentLoaded` has already fired
afterDOMloaded();
}
