const btn_mobile = document.getElementById('btn-mobile');

function toggle_menu(event) {
    const nav = document.getElementById('nav');
    nav.classList.toggle('active');
    btn_mobile.classList.toggle('active');
}

btn_mobile.addEventListener('click', toggle_menu);


// function currentPageHighlight(elementId) {
//     let HeaderButton = document.querySelector(elementId);
//     HeaderButton.addEventListener('click', () => {
//         HeaderButton.classList.toggle('active');
//     })
// }

// currentPageHighlight('#explore');