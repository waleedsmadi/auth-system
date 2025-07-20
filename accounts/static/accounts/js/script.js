// Re send button counter to make it enabled
window.onload = () => {

let btn = document.getElementById('resend-btn');

btn.classList.add('disabled');
btn.textContent = '';
for(let i=10; i>=1; i--){

    setTimeout(()=> {
        btn.textContent = i;
    }, (10 - i) * 1000)
}

setTimeout(function() {
    btn.textContent = `Re-send`;
    btn.classList.remove('disabled');
}, 10000)

}



