
var script = document.createElement('script');

// this is to alert that the script element has been 'created'...
script.onload = function() {
  alert("incepted 1 deep");
};

// important given we want to be able to load scripts
// from various web based resources

script.setAttribute('src', "/Users/dalewilson/dev/research/jsLibrary/alrt.js");
document.getElementsByTagName('head')[0].appendChild(script);

console.log('hi in alrt');
