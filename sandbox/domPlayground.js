// keep this around...may be useful for overriding any
// other methods from the original document object...
var original = document.createElement;

//https://developer.mozilla.org/en-US/docs/Web/API/Window/crypto
var array = new Uint32Array(1);
var array = new Uint32Array(1);
window.crypto.getRandomValues(array);

//set a fixed nonce for testing
array[0] = 1111111111;
// console.log(array[0]);

// (function hook) the document.createElement() function is overridden.
// src: https://stackoverflow.com/questions/50768596/hook-document-createelement-script-to-change-srcr
document.createElement = function (tag) {
      // call the function (createElement)...
      // from original document object. This needs to work for all tags,
      // so we createElement regardless of tag
      var element = original.call(document, tag);
      console.log('Confirms document.createElement has been modified');

      // only for script tags should a nonce value be set.
      if (tag.toLowerCase() === 'script') {
            // TRY with and without nonce offest to observe
            // behavior of scripts loaded with document.createElement,
            // watch for looping onLoad.
            element.setAttribute("nonce", array[0]+1);
            // element.setAttribute("nonce", array[0]);

            // element.setAttribute("nonceTest", (array[0] + 1).toString());
            console.log('in control structure to set nonce for script...');
            // Object.defineProperty(HTMLScriptElement.prototype, 'nonce', {
            //       set: function(newValue) {
            //       // element.setAttribute('nonce', array[0]);
            //       // this.setAttribute("nonce", (array[0] + 1).toString());
            //       // this.setAttribute("hi", (array[0] + 1).toString());
            // }
        // });
      }
      return element;
};

// we need to check if the dom content has loaded...
// it is the 'interactive' specification that indicate DOM content has loaded
// src: https://stackoverflow.com/questions/9457891/how-to-detect-if-domcontentloaded-was-fired

function afterDOMloaded() {
  var meta = document.createElement('meta');
  //https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src

  // meta.httpEquiv = 'Content-Security-Policy';

  // we need to enable unsafe-eval so we can rewrite the static inline event handlers to external scripta
  meta.content= "script-src 'unsafe-inline' 'unsafe-eval' * ";

  document.getElementsByTagName('head')[0].appendChild(meta);

  // search by wildcard tag...should graph all nodes


  // Second action...assigning nonce
  meta.setAttribute("http-equiv", "Content-Security-Policy");
  // meta.setAttribute("content", "script-src " + "'nonce-" + array[0].toString() + "'");
  meta.setAttribute("content", "script-src " + "'nonce-" + array[0].toString() + "'")

}

if (document.readyState === 'loading') {  // Loading hasn't finished yet
document.addEventListener('DOMContentLoaded', afterDOMloaded);
} else {  // `DOMContentLoaded` has already fired
afterDOMloaded();
}
