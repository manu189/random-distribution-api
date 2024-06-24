document.getElementById('distributionForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const names = document.getElementById('names').value.split(',').map(name => name.trim()).filter(name => name);
    const objects = document.getElementById('objects').value.split(',').map(object => object.trim()).filter(object => object);

    if (names.length === 0 || objects.length === 0) {
        alert("Please enter both names and objects.");
        return;
    }

    const urlParams = names.map(name => `names=${encodeURIComponent(name)}`).join('&') + '&' + objects.map(object => `objects=${encodeURIComponent(object)}`).join('&');
    window.location.href = `/distribute?${urlParams}`;
});
