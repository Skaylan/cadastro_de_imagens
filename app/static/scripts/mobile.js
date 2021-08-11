const btn_mobile = document.getElementById('btn-mobile');

function toggle_menu(event){
    const nav = document.getElementById('nav');
    nav.classList.toggle('active');
    btn_mobile.classList.toggle('active');
}

btn_mobile.addEventListener('click', toggle_menu);