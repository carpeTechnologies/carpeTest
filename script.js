/*Variables for the multitude of elements needed for interacting with the page below. Group into sections based on relationship to each other.
The interaction with most is simply grabbing some text from an input or changing the element's interactibility (i.e. making it so the other job field only shows when thtat role is selected).
*/
const Name = document.getElementById('name');
const Email = document.getElementById('email');
const jobRole = document.getElementById('title');
const otherJobRole = document.getElementById('other-job-role');
const designOption = document.getElementById('design');
const colorOptionList = document.getElementById('color');

// The elements below relate to the activities fieldset section and the prices. They will be used in that function below to change the displayed price based on which activities the user has selected and keep track of the price through any changes to it.

const activities = document.getElementById('activities');
let totalCost = 0;
const total = document.getElementById("activities-cost");

//Of these two, activityBox gets used far more as it is the main element used to select the checboxes for verifying the activities section further down while the label is only used briefly in setting the focus for those checkboxes.

const activityBox = document.querySelectorAll('input[type="checkbox"]');
const activityLabel = document.querySelectorAll('.activities label');

/*
These elements contain the various references to the payment method pieces as well as the form which are used when the user selects a payment method to decide what should be shown.
*/

const payment = document.getElementById('payment');
const card = document.getElementById('credit-card');
const paypal = document.getElementById('paypal');
const bitcoin = document.getElementById('bitcoin');
const cardNum = document.getElementById('cc-num');
const zip = document.getElementById('zip');
const cvv = document.getElementById('cvv');
const form = document.querySelector('form');

const nameErr = document.getElementById('name-hint');
const nameLabel = Name.parentNode;
const emailErr = document.getElementById('email-hint');
const emailLabel = Email.parentNode;
const activityErr = document.getElementById('activities-hint');
const cardErr = document.getElementById('cc-hint');
const cardLabel = cardNum.parentNode;
const zipErr = document.getElementById('zip-hint');
const zipLabel = zip.parentNode;
const cvvErr = document.getElementById('cvv-hint');
const cvvLabel = cvv.parentNode;

/*
The basic setup elements for the sections requiring setup is established here with the other field for job role set to be hidden (as it is only supposed to be visible if other is chosen in the associated dropdown).
The payment methods are also set to select the credit card payment method and hide all others.
*/

Name.focus();
otherJobRole.style.display = 'none';
paypal.style.display = 'none';
bitcoin.style.display = 'none';
payment[1].setAttribute('selected', 'selected');

//In this section, the conditions for showing and hiding the job role other field are established. In will now show that field only if the element with a value of 'other' is selected in the job role dropdown.

jobRole.addEventListener('change', () => {
    if(jobRole.value === 'other') {
        otherJobRole.style.display = '';
    } else {
        otherJobRole.style.display = 'none';
    }
});

/*
The section below links the choosable colors to the theme. By default, the color list is disabled and cannot be interacted with.
It is enabled when a design is chosen from that dropdown however, which colors will be present on the list changes based on which design is selected with a set list of colors for each design.
*/

colorOptionList.disabled  = true;

designOption.addEventListener('change', () => {
    colorOptionList.disabled = false;
    const design = designOption.value;

    for(let i = 0; i < colorOptionList.options.length; i++){
        const theme = colorOptionList.options[i].getAttribute('data-theme');
        
        if (theme === design){
            colorOptionList.options[i].style.display = '';
            colorOptionList.options[i].selected = true;
        } else{
            colorOptionList.options[i].style.display = 'none';
            colorOptionList.options[i].selected = false;
        }
    }
});

/*
The below section interacts with the totalCost variable from above to listen for any change to the activities section. It also contains a variable that interacts with the function parameter and grabs its' data cost attribute.
After acquiring the cost from its' attribute, the function checks to see if the target element's state is being changed to be checked or unchecked. If it is being checked then the value of the data cost attribute is added to the totalCost
variable before using that information to modify the text value of the total cost displayed at the bottom of the section. If an element is being unchecked then it subtracts from totalCost instead.

In addition, this section contains two parallel forEach loops to access the day and time of the various elements and disable the checkboxes that are at conflicting times to the one(s) already selected.
*/

activities.addEventListener('change', (event) => {
    const dataTarget = parseInt(event.target.getAttribute('data-cost'));
    const time = event.target.getAttribute('data-day-and-time');

    if(event.target.checked) {
            activityBox.forEach((eventTime) => {
                const eventVal = eventTime.getAttribute('data-day-and-time');
                if(eventTime !== event.target && eventVal === time) {
                        eventTime.disabled = true;
                        eventTime.parentNode.classList.add('disabled');
                    }
            });
        totalCost += dataTarget;
        total.innerHTML = `Total: $${totalCost}`;
    } else if(!event.target.checked) {
        activityBox.forEach((eventTime) => {
            const eventVal = eventTime.getAttribute('data-day-and-time');
            if(eventTime !== event.target && eventVal === time) {
                    eventTime.disabled = false;
                    eventTime.parentNode.classList.remove('disabled');
                }
        });

        totalCost -= dataTarget;
        total.innerHTML = `Total: $${totalCost}`;
    }
});

//This section checks which payment method is chosen and modifies the display accordingly so that only that element is displayed.

payment.addEventListener('change', () => {
    if (payment.value == 'credit-card') {
        card.style.display = '';
        paypal.style.display = 'none';
        bitcoin.style.display = 'none';
    } else if (payment.value == 'paypal') {
        card.style.display = 'none';
        paypal.style.display = '';
        bitcoin.style.display = 'none';
    } else if (payment.value == 'bitcoin') {
        card.style.display = 'none';
        paypal.style.display = 'none';
        bitcoin.style.display = '';
    }
});

//The following function only checks one thing. All it wants to know is if the name field is blank. If there is text in the name input field then nothing changes. If it is empty then it will display a red border and an error message warning that a name is required.

function nameValid(Name, nameErr, nameLabel) {
    const nameVal = Name.value.trim();
    if (nameVal === '') {
        nameErr.style.display = 'block';
        nameLabel.classList.add('not-valid');
        nameLabel.classList.remove('valid');
        return false;
    } else {
        nameErr.style.display = 'none';
        nameLabel.classList.add('valid');
        nameLabel.classList.remove('not-valid');
        return true;
    }
}

/*
Validation of the email field is twofold. The two things being checked for are that it has an email in the field and if it is correctly formatted to be considered an email.
If either of these are not true then an error border and message are displayed warning the user to enter a valid email address.
*/

function emailValid(Email, emailErr, emailLabel) {
    const regex = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(Email.value);
    if(Email.value === '' || !regex) {
        emailErr.style.display = 'block';
        emailLabel.classList.add('not-valid');
        emailLabel.classList.remove('valid');
        return false;
    } else {
        emailErr.style.display = 'none';
        emailLabel.classList.add('valid');
        emailLabel.classList.remove('not-valid');
        return true;
    }
}

function activityValid() {
        
    if(totalCost !== 0) {
            activityErr.style.display = 'none';
            activities.classList.add('valid');
            activities.classList.remove('not-valid');
            return true;
    } else {
        activityErr.style.display = 'block';
        activities.classList.add('not-valid');
        activities.classList.remove('valid');
        return false;
    }
}

/*
Checking for a valid credit card number is relatively simple, for the most part. This function first wants to know if the user has entered a card number.
If they have then the next thing to confirm is the length as this function requires a credit card number to be all numbers and between 13 and 16 characters long.
If either of these conditions fail to validate as being true, the section will display an error border and a warning message which varies depending on the type of failure.
*/

function cardValid(cardNum, cardErr, cardLabel) {
    const regexCC = /^\d{13,16}$/.test(cardNum.value);
    if(cardNum.value === '') {
        cardErr.innerHTML = 'Card number is required';
        cardErr.style.display = 'block';
        cardLabel.classList.add('not-valid');
        cardLabel.classList.remove('valid');
        return false;
    } else if (!regexCC) {
            cardErr.innerHTML = 'Credit card number must be between 13 - 16 digits';
            cardErr.style.display = 'block';
            cardLabel.classList.add('not-valid');
            cardLabel.classList.remove('valid');
            return false;
    } else {
            cardErr.style.display = 'none';
            cardLabel.classList.add('valid');
            cardLabel.classList.remove('not-valid');
            return true;
    }
}

//The zip and cvv validations are nearly identical in function. Both will only accept inputs of a specific length (5 for the zip and 3 for the cvv) and will display an error border and message if any other value is provided.

function zipValid(zip, zipErr, zipLabel) {
    const regexZip = /^\d{5}$/.test(zip.value);
    if(!regexZip) {
        zipErr.innerHTML = 'Zip code must be 5 digits';
        zipErr.style.display = 'block';
        zipLabel.classList.add('not-valid');
        zipLabel.classList.remove('valid');
        return false;
    }
    else {
        zipErr.style.display = 'none';
        zipLabel.classList.add('valid');
        zipLabel.classList.remove('not-valid');
        return true;
    }
}

function cvvValid(cvv, cvvErr, cvvLabel) {
    const regexCvv = /^\d{3}$/.test(cvv.value);
    if(!regexCvv) {
        cvvErr.innerHTML = 'CVV must be 3 digits';
        cvvErr.style.display = 'block';
        cvvLabel.classList.add('not-valid');
        cvvLabel.classList.remove('valid');
        return false;
    } else {
        cvvErr.style.display = 'none';
        cvvLabel.classList.add('valid');
        cvvLabel.classList.remove('not-valid');
        return true;
    }
}

/*The elements below are callbacks set up for the express purpose of enabling live validation of the various fields.
If a user enters a field and starts interacting with it then it will validate as they do so while applying and removing the relevant error messages as needed.
*/

Name.addEventListener('keyup', () => {
    nameValid(Name, nameErr, nameLabel);
});

Email.addEventListener('keyup', () => {
    emailValid(Email, emailErr, emailLabel);
});

activities.addEventListener('change', () => {
    activityValid();
})

cardNum.addEventListener('keyup', () => {
    cardValid(cardNum, cardErr, cardLabel);
});

zip.addEventListener('keyup', () => {
    zipValid(zip, zipErr, zipLabel);
});

cvv.addEventListener('keyup', () => {
    cvvValid(cvv, cvvErr, cvvLabel);
});

/*
Primarily the form event listener just exists to check that a value of true is returned by a validation function prior to allowing the form to submit
but it has to do a bit of extra work for the payment method in the form of confirming that it is set to credit card before running any other type of validation so that a user
who tries to enter a credit card and gets an error but then switches to paypal is capable of submitting the form.
*/

form.addEventListener('submit', (e) => {
    if(!nameValid(Name, nameErr, nameLabel)) {
        e.preventDefault();
    }
    if(!emailValid(Email, emailErr, emailLabel)) {
        e.preventDefault();
    }
    if(!activityValid()) {
        e.preventDefault();
    }
    let paymentCC = false;
    if(payment.value == 'credit-card') {
        paymentCC = true;
    } else {
        paymentCC = false;
    }
        if(!cardValid(cardNum, cardErr, cardLabel) && paymentCC == true) {
            e.preventDefault();
        }
        if(!zipValid(zip, zipErr, zipLabel) && paymentCC == true) {
            e.preventDefault();
        }
        if(!cvvValid(cvv, cvvErr, cvvLabel) && paymentCC == true) {
            e.preventDefault();
        }
});

function activityFocus() {
    for(let i = 0; i < activityBox.length; i++) {
        activityBox[i].addEventListener('focus', (event) => {
            if(event) {
                activityLabel[i].classList.add('focus');
            }
        });
        activityBox[i].addEventListener('blur', (event) => {
            if(event) {
                activityLabel[i].classList.remove('focus');
            }
        });
    }
}

activityFocus();
