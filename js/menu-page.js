(function () {
    const data = window.restaurantMenuData || [];
    const categoryContainer = document.getElementById('restaurant-menu-categories');
    const navigation = document.getElementById('menu-category-nav');

    if (!categoryContainer || !navigation || !data.length) {
        return;
    }

    const grouped = data.reduce((categories, item) => {
        if (!categories.has(item.category)) {
            categories.set(item.category, []);
        }
        categories.get(item.category).push(item);
        return categories;
    }, new Map());

    function categoryId(name) {
        return 'categorie-' + name.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    }

    grouped.forEach((items, category) => {
        const id = categoryId(category);
        const link = document.createElement('a');
        link.href = '#' + id;
        link.textContent = category;
        navigation.appendChild(link);

        const section = document.createElement('section');
        section.className = 'menu-category';
        section.id = id;

        const heading = document.createElement('h3');
        heading.textContent = category;
        section.appendChild(heading);

        const grid = document.createElement('div');
        grid.className = 'menu-items-grid';
        items.forEach(item => {
            const card = document.createElement('article');
            card.className = 'menu-item-card';

            const image = document.createElement('img');
            image.src = item.image;
            image.alt = item.name;
            image.loading = 'lazy';
            image.width = 150;
            image.height = 150;

            const content = document.createElement('div');
            content.className = 'menu-item-content';
            const titleRow = document.createElement('div');
            titleRow.className = 'menu-item-title-row';
            const title = document.createElement('h4');
            title.textContent = item.name;
            const price = document.createElement('strong');
            price.textContent = item.price;
            titleRow.append(title, price);

            const description = document.createElement('p');
            description.textContent = item.description;
            content.append(titleRow, description);
            card.append(image, content);
            grid.appendChild(card);
        });
        section.appendChild(grid);
        categoryContainer.appendChild(section);
    });
}());
