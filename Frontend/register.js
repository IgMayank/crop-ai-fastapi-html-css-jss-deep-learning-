const registerBtn =
    document.getElementById(
        "registerBtn"
    );


registerBtn.addEventListener(
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

        const email =
            document.getElementById(
                "email"
            ).value;

        const message =
            document.getElementById(
                "registerMessage"
            );

        
        try{

            const formData = new FormData();

            formData.append(
                "username",
                username
            );

            formData.append(
                "email",
                email
            );

            formData.append(
                "password",
                password
            );

const response =
    await fetch(
        "https://crop-0tmt.onrender.com/register",
        {
            method:"POST",
            body: formData
        }
    );
    const data =
    await response.json();

if(!response.ok){

    document.getElementById(
        "registerMessage"
    ).innerText =
        data.detail;

    return;
}

            

            message.innerText =
                data.message;

            if(response.ok){

                localStorage.setItem(
                "token",
                data.access_token
                );

                window.location.href =
                    "index.html";
}
        }catch(error){

            console.error(error);

            message.innerText =
                "Registration Failed";
        }
    }
);