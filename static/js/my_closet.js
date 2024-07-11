function updateCurrentTheme() {
    const themeFilter = document.getElementById('theme-filter');
    const currentTheme = document.getElementById('current-theme');
    currentTheme.textContent = `Current Theme: ${themeFilter.value}`;
}

function removeDesign(designId) {
    const designBox = document.getElementById(designId);
    designBox.remove();
}
