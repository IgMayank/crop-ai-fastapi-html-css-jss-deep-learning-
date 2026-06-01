const token =
    localStorage.getItem(
        "token"
    );



if(token){

    window.location.href =
        "index.html";
}
const loginBtn =
    document.getElementById(
        "loginBtn"
    );

loginBtn.addEventListener(
    "click",
    async () => {

        const username =
            document.getElementById(
                "username"
            ).value;

        const password =
            document.getElementById(
                "password"
            ).value;

        const response =
            await fetch(
                "http://127.0.0.1:8000/login",
                {
                    method:"POST",

                    headers:{
                        "Content-Type":
                        "application/x-www-form-urlencoded"
                    },

                    body:
                    `username=${username}&password=${password}`
                }
            );

        const data =
    await response.json();

if(!response.ok){

    document.getElementById(
        "loginMessage"
    ).innerText =
        data.detail ||
        "Login Failed";

    return;
}

localStorage.setItem(
    "token",
    data.access_token
);

window.location.href =
    "index.html";

    });