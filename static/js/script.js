function toggleMenu() {
  const navLinks = document.getElementById("navLinks");
  if (navLinks) {
    navLinks.classList.toggle("active");
  }
}




document.querySelectorAll(".paw-card").forEach((card) => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".paw-card").forEach((item) => {
      item.classList.remove("active");
    });
    card.classList.add("active");
  });
});



document.querySelectorAll(".step-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".step-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
  });
});