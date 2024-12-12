function toggleMenu() {
    const menu = document.getElementById("nav-menu");
    if (menu.style.display === "flex") {
        menu.style.display = "none";
    } else {
        menu.style.display = "flex";
    }
}



function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    // Toggle visibility of the menu
    if (menu.style.display === 'flex') {
        menu.style.display = 'none';
    } else {
        menu.style.display = 'flex';
        menu.style.justifyContent = 'center'; // Center items horizontally
        menu.style.alignItems = 'center';    // Center items vertically
    }
}