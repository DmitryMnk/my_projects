import { 
    registration_first_step,
    confirmation,
    return_first_step,
    resend_confirmation, 
    run_timer 
} from "./functions.js";

const sendEmailButton = document.querySelector('.registration__send-confirmation');
const resendButton = document.querySelector('.registration__resend-confirmation');
const confirmEmailButton = document.querySelector('.registration__confirm-button');
const changeEmailButton = document.querySelector('.registration__change-email');
const timerBlock = document.querySelector('.registration__timer-timer');
const phoneInput = document.getElementById('id_phone');
const passwordInput = document.getElementById('id_password1');
const passwordInputParent = passwordInput.parentNode;

sendEmailButton.addEventListener('click', async () => {
    registration_first_step(sendEmailButton);
})

changeEmailButton.addEventListener('click', () => {
    return_first_step(sendEmailButton, timerBlock);
})

confirmEmailButton.addEventListener('click', () => {
    confirmation(timerBlock);
})

resendButton.addEventListener('click', () => {
    resend_confirmation(resendButton, timerBlock);
})

document.addEventListener('DOMContentLoaded', () => {
    if (timerBlock.textContent != '') {
        const timer = timerBlock.textContent.split(':')
        const timer_time = parseInt(timer[0]) * 60 + parseInt(timer[1])
        run_timer(timerBlock, timer_time, resendButton)
    }
    const messageBlock = document.createElement('div');
    const messageList = document.createElement('ul');
    const message1 = document.createElement('li');
    const message2 = document.createElement('li');
    const message3 = document.createElement('li');
    const message4 = document.createElement('li');

    messageBlock.classList.add('registration__message-block');
    messageList.classList.add('registration__message-list');
    message1.classList.add('registration__message-list-item');
    message2.classList.add('registration__message-list-item');
    message3.classList.add('registration__message-list-item');
    message4.classList.add('registration__message-list-item');

    message1.textContent = 'Требования к паролю:'
    message2.textContent = 'длина от 8 до 30 символов;'
    message3.textContent = 'состоит из символов латинского алфавита и цифр;'
    message4.textContent = 'отличается от e-mail и имени;'

    messageList.append(message1, message2, message3, message4);
    messageBlock.append(messageList);

    passwordInput.addEventListener('focus', () => {
        passwordInputParent.append(messageBlock);
        setTimeout(() => {
            messageBlock.classList.add('message-block--active');
        }, 10)
    })

    passwordInput.addEventListener('blur', () => {
        
        messageBlock.classList.remove('message-block--active');
        setTimeout(() => {
            passwordInputParent.removeChild(messageBlock);
        }, 210)
    })
})

phoneInput.addEventListener('focus', () => {
    if (phoneInput.value.length == 0) {
        phoneInput.value = '+7'
    }
    
})

phoneInput.addEventListener('input', () => {
    const value = phoneInput.value
    const length = value.length
    if (value[length - 1] == '+' && length > 1) {
        phoneInput.value = value.slice(0, -1);
    } else if (value[length - 1] < '0' || value[length - 1] > '9') {
        phoneInput.value = value.slice(0, -1);
    }

    
})