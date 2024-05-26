async function request_post(link, value) {
    const request_data = JSON.stringify(value)
    const response = await fetch(`${link}`,
    {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
        },
        body: request_data
    }
    )
    const data = await response.json()
    return data 
}

async function request_get(link) {
    const response = await fetch(`${link}`)
    const data = await response.json()
    return data 
}

function loader_block(parent_block, remove_loader) {
    let loader;
    if (remove_loader) {
        loader = parent_block.querySelector('.loader');
        loader.classList.remove('loader--active');
        setTimeout(() => {
            parent_block.removeChild(loader);
        }, 100)
    } else {
        loader = document.createElement('div');
        loader.classList.add('loader');
        parent_block.append(loader);
        setTimeout(() => {
            loader.classList.add('loader--active');
        }, 10)
    }
}

export {
    request_post,
    request_get,
    loader_block
}