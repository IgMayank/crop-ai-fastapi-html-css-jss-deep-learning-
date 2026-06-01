console.log("SCRIPT RELOADED AT:", new Date().toLocaleTimeString());
window.addEventListener(
    "beforeunload",
    () => {
        console.log("PAGE RELOAD DETECTED");
    }
);
console.log(
    "PAGE LOADED AT:",
    new Date().toLocaleTimeString()
);
const token =
    localStorage.getItem(
        "token"
    );

if(!token){

    window.location.href =
        "login.html";
}
async function loadDashboard(){

    try{

        const token =
            localStorage.getItem(
                "token"
            );

        const response =
            await fetch(
                "http://127.0.0.1:8000/my-history",
                {
                    headers:{
                        "Authorization":
                        `Bearer ${token}`
                    }
                }
            );

        const predictions =
            await response.json();

        const total =
            predictions.length;

        const healthy =
            predictions.filter(
                p =>
                    p.disease &&
                    p.disease.toLowerCase() ===
                    "healthy"
            ).length;

        const diseased =
            total - healthy;

        document.getElementById(
            "totalPredictions"
        ).innerText =
            total;

        document.getElementById(
            "healthyCount"
        ).innerText =
            healthy;

        document.getElementById(
            "diseasedCount"
        ).innerText =
            diseased;

    }catch(error){

        console.error(
            "Dashboard Error:",
            error
        );
    }
}
console.log("JS Loaded");   
const imageInput = document.getElementById("imageInput");

const browseBtn = document.getElementById("browseBtn");

const dropArea = document.getElementById("dropArea");

const previewContainer =
    document.getElementById("previewContainer");

const predictBtn =
    document.getElementById("predictBtn");

let selectedFiles = [];

browseBtn.addEventListener("click", () => {

    imageInput.click();

});

imageInput.addEventListener("change", (event) => {

    selectedFiles =
        Array.from(event.target.files);

    showPreview();
});

dropArea.addEventListener("dragover", (event) => {

    event.preventDefault();

    dropArea.classList.add("dragover");
});

dropArea.addEventListener("dragleave", () => {

    dropArea.classList.remove("dragover");
});

dropArea.addEventListener("drop", (event) => {

    event.preventDefault();

    dropArea.classList.remove("dragover");

    selectedFiles =
        Array.from(event.dataTransfer.files);

    showPreview();
});

function showPreview(){

    previewContainer.innerHTML = "";

    selectedFiles.forEach((file) => {

        const card =
            document.createElement("div");

        card.className = "preview-card";

        const img =
            document.createElement("img");

        img.src =
            URL.createObjectURL(file);

        card.appendChild(img);

        previewContainer.appendChild(card);
    });
}

predictBtn.addEventListener(
    "click",
    async (event) => {
         event.preventDefault();

    if(selectedFiles.length === 0){

        alert("Please select images");

        return;
    }

    previewContainer.innerHTML = "";

    for(const file of selectedFiles){

        const formData = new FormData();

        formData.append("file", file);

        const card =
            document.createElement("div");

        card.className = "preview-card";

        const img =
            document.createElement("img");

        img.src =
            URL.createObjectURL(file);

        card.appendChild(img);

        const result =
            document.createElement("div");

        result.className = "result-text";

        result.innerHTML = "Predicting...";

        card.appendChild(result);

        previewContainer.appendChild(card);
   

        try{

           const token =
                localStorage.getItem(
                    "token"
                );

            

            const response = await fetch(
                "http://127.0.0.1:8000/predict",
                {
                    method: "POST",

                    headers: {
                        "Authorization":
                        `Bearer ${token}`
                    },

                    body: formData
                }
            );

            const data = await response.json();

            

            result.innerHTML = `
    <div class="prediction-result">

        <h3>
             Prediction Result
        </h3>

        <p>
            <strong>Crop:</strong>
            ${data.crop}
        </p>

        <p>
            <strong>Disease:</strong>
            ${data.disease}
        </p>

        <p>
            <strong>Confidence:</strong>
            ${data.confidence}%
        </p>

        <p>
            <strong>Status:</strong>
            ${
                (data.disease || "").toLowerCase() === "healthy"
                ? "Healthy ✅"
                : "Diseased ⚠️"
            }
        </p>

        <div class="message-box">
            ${data.message}
        </div>

    </div>
`;
await loadDashboard();
        }catch(error){

            console.error(error);

            result.innerHTML =
                "Prediction Failed";
        }
    }
});
// const data =
//     await response.json();

// if(!response.ok){

//     alert(
//         data.detail?.[0]?.msg ||
//         data.detail ||
//         "Something went wrong"
//     );

//     return;
// }
const logoutBtn =
    document.getElementById(
        "logoutBtn"
    );

    logoutBtn.addEventListener(
        "click",
        () => {

        localStorage.removeItem(
            "token"
        );

        window.location.href =
            "login.html";
    }
);
loadDashboard();