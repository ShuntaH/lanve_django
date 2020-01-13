document.addEventListener('DOMContentLoaded', () => {

    // Get all "tab" elements
    const $tabs = document.getElementsByClassName('tab');

    // Add a click event on each of them
    for (let i = 0; i < $tabs.length; i++) {
        $tabs[i].addEventListener('click', () => {
            // タブのclassの値を変更
            document.getElementsByClassName('is-active')[0].classList.remove('is-active');
            $tabs[i].classList.add('is-active');
            // コンテンツのclassの値を変更
            document.getElementsByClassName('is-hidden')[0].classList.remove('is-hidden');
            if (i === 0)
                document.getElementsByClassName('tab-content')[1].classList.add('is-hidden');
            else if (i === 1)
                document.getElementsByClassName('tab-content')[0].classList.add('is-hidden');
        });
    }
});