const toDomContentLoaded = performance.now();

window.addEventListener('DOMContentLoaded', (event) => {
      const domContentLoadedPoint = performance.now();
      let timeToDomContentLoaded = domContentLoadedPoint - toDomContentLoaded;
      console.log("Time to DOMContentLoaded: " + timeToDomContentLoaded + ": " + window.location + ": " + "overhead");
});
