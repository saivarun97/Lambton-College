var enable = document.getElementById("enable");

enable.addEventListener("click", async() => {
    let [tab] = await chrome.tabs.query({
        active: true,
        currentWindow: true
    });

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: detectAndBlurRecords
    });
});

function detectAndBlurRecords() {
    //mbr-text
    const textElements = document.getElementsByClassName("text");
    Array.prototype.forEach.call(textElements, async function(el) {
        const text = el.innerHTML;
        
        // // Call Flask API Here. Apply style if it is a spoiler.
        // http://20.25.82.123:5000/
        fetch("http://localhost:5000/predict", {
            method: "POST",
            body: JSON.stringify({
                comment: text,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
                    } 
        })
        .then(async (response) => {
           response_data= await response.json()
           console.log(response_data)
           if (response_data === "The review is a Spoiler") {
            console.log("true")
            el.parentNode.style.filter = 'blur(10px)';
          }
        })

        // // text show-more__control
      
        // const document_to_blue = document.getElementsByClassName("text");
        // console.log(document_to_blue.style)
        // document_to_blue.style.filter = 'blue(10px)';


        

        // el.parentNode.style.filter = 'blur(10px)';
    
    });
}