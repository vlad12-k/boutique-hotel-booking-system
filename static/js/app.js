document.addEventListener("DOMContentLoaded", () => {
  const normalise = (value) => (value || "").trim().toLowerCase();

  const setupStatusFilter = (filterId, rowSelector) => {
    const filter = document.getElementById(filterId);
    if (!filter) return;

    const rows = document.querySelectorAll(rowSelector);
    const applyFilter = () => {
      const selected = normalise(filter.value);
      rows.forEach((row) => {
        const rowStatus = normalise(row.dataset.status);
        const isVisible = selected === "all" || rowStatus === selected;
        row.classList.toggle("d-none", !isVisible);
      });
    };

    filter.addEventListener("change", applyFilter);
    applyFilter();
  };

  setupStatusFilter("roomStatusFilter", "table tbody tr[data-status]");
  setupStatusFilter("bookingStatusFilter", "table tbody tr[data-status]");

  const bookingForm = document.getElementById("addBookingForm");
  if (bookingForm) {
    const checkInInput = document.getElementById("checkInDate");
    const checkOutInput = document.getElementById("checkOutDate");
    const messageEl = document.getElementById("bookingDateValidationMessage");

    const showValidationMessage = (message) => {
      if (!messageEl) return;
      messageEl.textContent = message;
      messageEl.classList.toggle("d-none", !message);
    };

    const validateBookingDates = () => {
      const checkIn = checkInInput ? checkInInput.value : "";
      const checkOut = checkOutInput ? checkOutInput.value : "";

      if (!checkIn) {
        showValidationMessage("Check-in date is required.");
        return false;
      }

      if (!checkOut) {
        showValidationMessage("Check-out date is required.");
        return false;
      }

      if (checkOut <= checkIn) {
        showValidationMessage("Check-out date must be after check-in date.");
        return false;
      }

      showValidationMessage("");
      return true;
    };

    bookingForm.addEventListener("submit", (event) => {
      if (!validateBookingDates()) {
        event.preventDefault();
      }
    });

    if (checkInInput) checkInInput.addEventListener("change", validateBookingDates);
    if (checkOutInput) checkOutInput.addEventListener("change", validateBookingDates);
  }

  const cancelForms = document.querySelectorAll(".js-cancel-booking-form");
  cancelForms.forEach((form) => {
    form.addEventListener("submit", (event) => {
      const confirmed = window.confirm("Are you sure you want to cancel this booking?");
      if (!confirmed) {
        event.preventDefault();
      }
    });
  });
});
