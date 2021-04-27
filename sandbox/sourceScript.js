element = document.getElementById("script1Target")
element.setAttribute('documentWriteScriptTest', 'True');

// test for if an element is written to have an inline event handler
// after the DOMcontentloaded event?

var btn = document.createElement("button");
btn.setAttribute("id", "inlineExternalScript");
btn.onclick = function() { alert('The external script, srouceScript.js, was loaded...it created the button you clicked and defined the alert content you read now.');};
btn.innerHTML = 'If you can see this button, the external script, sourceScript.js, has successfully executed and added a button to the DOM.'
document.body.appendChild(btn);
