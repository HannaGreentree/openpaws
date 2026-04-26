/* =========================
   CASE DETAIL GALLERY
========================= */
function initCaseGallery() {
  const mainImage = document.getElementById("caseMainImage");
  const thumbButtons = document.querySelectorAll(".case-gallery-thumb-button");

  if (!mainImage || !thumbButtons.length) return;

  thumbButtons.forEach(function (button) {
    button.addEventListener("click", function (event) {
      event.preventDefault();

      const imageUrl = this.getAttribute("data-image-url");
      if (!imageUrl) return;

      mainImage.src = imageUrl;

      thumbButtons.forEach(function (btn) {
        btn.classList.remove("is-active");
      });

      this.classList.add("is-active");
    });
  });
}

/* =========================
   IMAGE MODAL
========================= */
function openImage(imageUrl) {
  const modal = document.getElementById("imageModal");
  const modalImage = document.getElementById("modalImage");

  if (!modal || !modalImage) return;

  modalImage.src = imageUrl;
  modal.style.display = "flex";
}

function closeImage() {
  const modal = document.getElementById("imageModal");

  if (modal) {
    modal.style.display = "none";
  }
}

/* =========================
   MOBILE MENU
========================= */
function initMobileMenu() {
  const menuToggle = document.querySelector(".menu-toggle");
  const mobileNav = document.querySelector(".mobile-nav");

  if (!menuToggle || !mobileNav) return;

  menuToggle.addEventListener("click", function () {
    mobileNav.classList.toggle("mobile-nav-open");

    const isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isExpanded));
  });
}

/* =========================
   CARD INTERACTIONS
========================= */
function setActiveCard(selector) {
  const cards = document.querySelectorAll(selector);

  if (!cards.length) return;

  cards.forEach(function (card) {
    card.addEventListener("click", function () {
      cards.forEach(function (item) {
        item.classList.remove("active");
      });

      card.classList.add("active");
    });
  });
}

/* =========================
   QUICK AMOUNT BUTTONS
========================= */
function initQuickAmounts() {
  const amountInput = document.getElementById("amount");
  const quickButtons = document.querySelectorAll(".quick-amount-btn");

  if (!amountInput || !quickButtons.length) return;

  quickButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      const amount = this.getAttribute("data-amount");
      if (!amount) return;

      amountInput.value = amount;

      quickButtons.forEach(function (btn) {
        btn.classList.remove("is-active");
      });

      this.classList.add("is-active");
    });
  });

  amountInput.addEventListener("input", function () {
    quickButtons.forEach(function (btn) {
      if (btn.getAttribute("data-amount") === amountInput.value) {
        btn.classList.add("is-active");
      } else {
        btn.classList.remove("is-active");
      }
    });
  });
}

/* =========================
   INITIALISE INTERACTIONS
========================= */
document.addEventListener("DOMContentLoaded", function () {
  initMobileMenu();
  initCaseGallery();
  initQuickAmounts();
  setActiveCard(".paw-card");
  setActiveCard(".step-card");
});