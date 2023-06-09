
// show or hide nav content if nav btn is clicked

if (document.readyState) {

    // get elements
    const navBtn = document.body.querySelector('.nav-btn');
    const closeNavBtn = document.body.querySelector('.top .btn-close');
    const navContent = document.body.querySelector('.nav-content');

    // show menu bar if menu button is clicked
    navBtn.addEventListener('click', () => {
        if (navContent.style.display == 'none') {
            navContent.style.display = 'block';
        }
    });

    // close menu bar if close button is clicked
    closeNavBtn.addEventListener('click', () => {
        if (navContent.style.display == 'block') {
            navContent.style.display = 'none';
        }
    });
}
