// timeout before a callback is called

let timeout;

// traversing the DOM and getting the input and span using their IDs

let password = document.getElementById('password')
let strengthBadge = document.getElementById('strength')
let confirmPassword = document.getElementById('confirmPassword')
let confirmPasswordBadge = document.getElementById('confirmPasswordMsg')
let emailId = document.getElementById('emailId')
let emailBadge = document.getElementById('emailIdMsg')
let name = document.getElementById('name')
let nameBadge = document.getElementById('nameMsg')

// The strong and weak password Regex pattern checker
let strongPassword = new RegExp('(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{8,})')
let mediumPassword = new RegExp('((?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))|((?=.*[a-z])(?=.*[0-9])(?=.*[^A-Za-z0-9])(?=.{6,}))')
let caps = new RegExp('((?=.*[A-Z]))')
let small = new RegExp('((?=.*[a-z]))')
let numbers = new RegExp('((?=.*[0-9]))')
let symbols = new RegExp('((?=.*[^A-Za-z0-9]))')
let lessThanEight = new RegExp('((?=.{8,}))')
let email = new RegExp('^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*(\\.\\w{2,3})+$')

function StrengthChecker(PasswordParameter){
    // We then change the badge's color and text based on the password strength

    if(strongPassword.test(PasswordParameter)) {
        strengthBadge.style.color = "green"
        strengthBadge.textContent = 'Strong'
    } else if(mediumPassword.test(PasswordParameter)){
        let msg = "Medium - "+ passwordValidationMessage(PasswordParameter)

        strengthBadge.style.color = 'blue'
        strengthBadge.textContent = msg
    } else{
        let msg = "Weak - " + passwordValidationMessage(PasswordParameter)
        strengthBadge.style.color = 'red'
        strengthBadge.textContent = msg
    }
}

function passwordValidationMessage(PasswordParameter){
    let msg =""
    if (! lessThanEight.test(PasswordParameter)){
          msg = msg + " Use 8 or more characters "
        }
        let msg2 = "with a mix of "
        let msg3 = ""
        if (! caps.test(PasswordParameter)){
          msg3 = msg3 + " caps"
        }
    if (! small.test(PasswordParameter)){
            if(msg3!=""){
               msg3 = msg3 + ", small letter"
            }
            else{
                msg3 = msg3 + " small letter"
            }

        }
    if (! numbers.test(PasswordParameter)){
        if(msg3!=""){
               msg3 = msg3 + ", number"
            }
            else{
                msg3 = msg3 + " number"
            }
        }
    if (! symbols.test(PasswordParameter)){
        if(msg3!=""){
               msg3 = msg3 + ", special character"
            }
            else{
                msg3 = msg3 + " special character"
            }
        }
    if (msg3!=""){
        msg = msg+msg2+msg3
    }
    return msg
}

function ConfirmPasswordChecker(confirmPassword, password){
    if (confirmPassword != password){
        confirmPasswordBadge.style.display ='block'
        confirmPasswordBadge.textContent = "Password is not matching"
    } else{
        confirmPasswordBadge.style.display ='none'
    }
}

function emailValidation(emailParameter){
    if (!email.test(emailParameter)){
        emailBadge.style.display ='block'
        emailBadge.textContent = "Email-Id not in proper format"
    }else{
        emailBadge.style.display ='none'
    }
}

function nameValidation(nameParameter){
    let msg = ""
    if (symbols.test(nameParameter)) {
        msg = "special characters"
    }
    if (numbers.test(nameParameter)){
        if(msg==""){
            msg=" numbers"
        }else{
            msg=msg+", numbers"
        }
    }
    if(msg!=""){
        nameBadge.style.display ='block'
        nameBadge.textContent = msg+ " are not allowed"
    }
    else{
        nameBadge.style.display ='none'
    }

}

// Adding an input event listener when a user types to the  password input
password.addEventListener("input", () => {

    //The badge is hidden by default, so we show it

    strengthBadge.style.display= 'block'
    clearTimeout(timeout);

    //Incase a user clears the text, the badge is hidden again

    if(password.value.length !== 0){
        //We then call the StrengChecker function as a callback then pass the typed password to it
        timeout = setTimeout(() => StrengthChecker(password.value), 500);
        strengthBadge.style.display != 'block'
    } else{
        strengthBadge.style.color = 'red'
        strengthBadge.textContent = 'Use 8 or more characters with a mix of letters, numbers & symbols'
    }
});

// Adding an input event listener when a user types to the confirm password input
confirmPassword.addEventListener("input",()=>{
    if(confirmPassword.value.length !=0){
        timeout = setTimeout(() => ConfirmPasswordChecker(confirmPassword.value, password.value), 500);
        confirmPasswordBadge.style.display != 'block'
    } else{
        strengthBadge.style.display = 'None'
    }
});

emailId.addEventListener("input", ()=>{
    if(emailId.value.length !=0){
        timeout = setTimeout(() => emailValidation(emailId.value), 500);
        emailBadge.style.display != 'block'
    } else{
        emailBadge.style.display = 'None'
    }
});

name.addEventListener("input", ()=>{
    if(name.value.length !=0){
        timeout = setTimeout(() => nameValidation(name.value), 500);
        nameBadge.style.display != 'block'
    } else{
        nameBadge.style.display = 'None'
    }
});