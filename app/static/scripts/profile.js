const asideButton = document.querySelector('#aside-button')


let toggle_aside = (event) => {
    const asideBar = document.querySelector('#aside')
    asideBar.classList.toggle('active')

}

asideButton.addEventListener('click', toggle_aside)