function removeDesign(designId) {
    const designBox = document.getElementById(designId);
    if (designBox) {
        designBox.remove();
    }
}
