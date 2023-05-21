document.addEventListener("DOMContentLoaded", function () {
    const dropdownButton = document.getElementById("user-menu-button");
    const dropdownMenu = document.getElementById("dropdown-menu");
  
    dropdownButton.addEventListener("click", function () {
      dropdownMenu.classList.toggle("hidden");
    });
  
    document.addEventListener("click", function (event) {
      const targetElement = event.target;
      if (!targetElement.closest("#user-menu-button")) {
        dropdownMenu.classList.add("hidden");
      }
    });
  });