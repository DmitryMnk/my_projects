import { 
    request_post,
    request_get,
    loader_block
} from "../../../../static/base/base_js/base.js";
const emailInput = document.querySelector('.registration__mail-input');
const errorMessage = document.querySelector('.registration__step-error');
const firstStep = document.querySelector('.registration-first-step');
const secondStep = document.querySelector('.registration-second-step');
const thirdStep = document.querySelector('.registration-third-step');
const emailText = document.querySelector('.registration__email-text');
const section = document.querySelector('.registration');

function registration_first_step(sendButton) {
    const data = {
        'email': emailInput.value
    }
    loader_block(section, false)

    request_post('api/check_email/' ,data).then(response => {
        if (response.access) {
            errorMessage.textContent = '';
            emailText.textContent = emailInput.value
            firstStep.classList.toggle('step--active');
            setTimeout(() => {
                firstStep.classList.toggle('step-display--off');
                secondStep.classList.toggle('step-display--off');
            }, 200)
            setTimeout(() => {
                secondStep.classList.toggle('step--active');
            }, 220)
        
        } else {
            errorMessage.textContent = response.error[0]
        }
    }).finally(() => {
        loader_block(section, true)
    })
    
}

function return_first_step(sendButton, timerBlock) {
    loader_block(section, false)
    request_get('api/check_email/').then(response => {
        errorMessage.textContent = '';
        console.log(response)
        if (response.timer_run) {
            run_timer(timerBlock, response.timer, sendButton)
        }
        secondStep.classList.toggle('step--active');
        setTimeout(() => {
            secondStep.classList.toggle('step-display--off');
            firstStep.classList.toggle('step-display--off');
        }, 200)
        setTimeout(() => {
            firstStep.classList.toggle('step--active');
        }, 220)
    }).finally(() => {
        loader_block(section, true)
    });
    
}

async function confirmation(timerBlock) {
    const codeInput = document.querySelector('.registration__confirm-input');
    const errorMessage = document.querySelector('.step-error-bottom');
    const data = JSON.stringify({
        'code': codeInput.value
    })

    loader_block(section, false)
    const response = confirm_email(data).then(response => {
        if (response.access) {
            timerBlock.style.display = 'none';
            secondStep.classList.toggle('step--active');
            setTimeout(() => {
                secondStep.classList.toggle('step-display--off');
                thirdStep.classList.toggle('step-display--off');
            }, 200)
            setTimeout(() => {
                thirdStep.classList.toggle('step--active');
            }, 220)
            
        } else {
            errorMessage.textContent = response.error
            codeInput.value = ''
        }
    }).finally(() => {
        loader_block(section, true);
    })
    
}

function resend_confirmation(button, timerBlock) {
    const resendMessage = document.querySelector('.registration__resand-message');
    if (!timerBlock.textContent) {
        request_get('api/send_activation_code/').then(response => {
            let timer_time = response.timer
            if (response.access) {
                resendMessage.textContent = 'Письмо отправленно еще раз. Проверьте Ваш почтовый ящик';
                if (response.timer_run) {
                   run_timer(timerBlock, response.timer, button); 
                }
                

            } else {
                resendMessage.textContent = `Письмо можно отправить повторно после окончания работы таймера.`;
                run_timer(timerBlock, response.timer, button);
            }
        })
    
    }
}

function run_timer(timerBlock, timer_time, button) {
    timerBlock.style.opacity = '1'
    button.disabled = true
    const timer = setInterval(() => {
        timerBlock.textContent = timer_value(timer_time)
        timer_time -= 1
        if (timer_time < 0) {
            timerBlock.textContent = ''
            button.disabled = false
            clearInterval(timer)
        }
    }, 1000)
}

function timer_value(time_sec) {
    let timer_first = Math.floor(time_sec / 60);
    let timer_second = time_sec % 60;
    if (timer_first != 0) {
        timer_first = `0${timer_first}`
    } else {
        timer_first = '00'
    }

    if (timer_second < 10) {
        timer_second = `0${timer_second}`
    }

    return `${timer_first}:${timer_second}`
}

async function confirm_email(value) {
    const response = await fetch("api/confirm_email/",
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
        },
        body: value
    }
    )
    const data = await response.json()
    return data 
}

export {
    registration_first_step,
    confirmation,
    resend_confirmation,
    run_timer,
    return_first_step,
}