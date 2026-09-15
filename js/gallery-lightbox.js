(function () {
    const selectors = ['.spa-gallery-grid img', '.pool-photo-grid-inner img'];
    const images = Array.from(document.querySelectorAll(selectors.join(',')));
    if (!images.length) return;

    const lightbox = document.createElement('div');
    lightbox.className = 'elite-lightbox';
    lightbox.setAttribute('aria-hidden', 'true');
    lightbox.innerHTML = `
        <button class="elite-lightbox-close" type="button" aria-label="Închide imaginea">&times;</button>
        <button class="elite-lightbox-arrow elite-lightbox-prev" type="button" aria-label="Imaginea precedentă">&#8249;</button>
        <figure>
            <img src="" alt="">
            <figcaption></figcaption>
        </figure>
        <button class="elite-lightbox-arrow elite-lightbox-next" type="button" aria-label="Imaginea următoare">&#8250;</button>`;
    document.body.appendChild(lightbox);

    const enlargedImage = lightbox.querySelector('img');
    const caption = lightbox.querySelector('figcaption');
    let activeIndex = 0;
    let lastFocused = null;

    function show(index) {
        activeIndex = (index + images.length) % images.length;
        enlargedImage.src = images[activeIndex].src;
        enlargedImage.alt = images[activeIndex].alt;
        caption.textContent = images[activeIndex].alt;
    }

    function open(index) {
        lastFocused = document.activeElement;
        show(index);
        lightbox.classList.add('open');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.classList.add('lightbox-open');
        lightbox.querySelector('.elite-lightbox-close').focus();
    }

    function close() {
        lightbox.classList.remove('open');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('lightbox-open');
        if (lastFocused) lastFocused.focus();
    }

    images.forEach((image, index) => {
        image.tabIndex = 0;
        image.setAttribute('role', 'button');
        image.setAttribute('aria-label', `Mărește: ${image.alt}`);
        image.addEventListener('click', () => open(index));
        image.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                open(index);
            }
        });
    });

    lightbox.querySelector('.elite-lightbox-close').addEventListener('click', close);
    lightbox.querySelector('.elite-lightbox-prev').addEventListener('click', () => show(activeIndex - 1));
    lightbox.querySelector('.elite-lightbox-next').addEventListener('click', () => show(activeIndex + 1));
    lightbox.addEventListener('click', event => {
        if (event.target === lightbox) close();
    });
    document.addEventListener('keydown', event => {
        if (!lightbox.classList.contains('open')) return;
        if (event.key === 'Escape') close();
        if (event.key === 'ArrowLeft') show(activeIndex - 1);
        if (event.key === 'ArrowRight') show(activeIndex + 1);
    });
}());
