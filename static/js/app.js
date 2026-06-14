// Vanilla JavaScript enhancements for the Boutique Hotel Booking System.
// This file intentionally uses plain browser APIs only: no jQuery, no npm, no build tools.

document.addEventListener("DOMContentLoaded", () => {
  const normalise = (value) => (value || "").trim().toLowerCase();

  const setAlertMessage = (element, message) => {
    if (!element) return;
    element.textContent = message;
    element.classList.toggle("d-none", !message);
  };

  const parseDateValue = (input) => {
    if (!input || !input.value) return null;
    const parsedDate = new Date(`${input.value}T00:00:00`);
    return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
  };

  const setupStatusFilter = (filterId, rowSelector, emptyMessageId) => {
    const filter = document.getElementById(filterId);
    if (!filter) return;

    const rows = Array.from(document.querySelectorAll(rowSelector));
    const emptyMessage = document.getElementById(emptyMessageId);

    const applyFilter = () => {
      const selected = normalise(filter.value || "all");
      let visibleCount = 0;

      rows.forEach((row) => {
        const rowStatus = normalise(row.dataset.status);
        const isVisible = selected === "all" || rowStatus === selected;
        row.classList.toggle("d-none", !isVisible);
        row.setAttribute("aria-hidden", String(!isVisible));
        if (isVisible) visibleCount += 1;
      });

      if (emptyMessage) {
        const hasNoMatches = visibleCount === 0;
        emptyMessage.classList.toggle("d-none", !hasNoMatches);
        emptyMessage.setAttribute("aria-hidden", String(!hasNoMatches));
      }
    };

    filter.addEventListener("change", applyFilter);
    applyFilter();
  };

  setupStatusFilter("roomStatusFilter", "table tbody tr[data-status]", "roomFilterEmptyMessage");
  setupStatusFilter("bookingStatusFilter", "table tbody tr[data-status]", "bookingFilterEmptyMessage");

  const bookingForm = document.getElementById("addBookingForm");
  if (bookingForm) {
    const checkInInput = document.getElementById("checkInDate");
    const checkOutInput = document.getElementById("checkOutDate");
    const messageEl = document.getElementById("bookingDateValidationMessage");

    const today = new Date().toISOString().split("T")[0];
    if (checkInInput && !checkInInput.min) checkInInput.min = today;
    if (checkOutInput && !checkOutInput.min) checkOutInput.min = today;

    const updateCheckOutMinimum = () => {
      if (!checkInInput || !checkOutInput || !checkInInput.value) return;
      checkOutInput.min = checkInInput.value;

      if (checkOutInput.value && checkOutInput.value <= checkInInput.value) {
        checkOutInput.value = "";
      }
    };

    const validateBookingDates = () => {
      const checkInDate = parseDateValue(checkInInput);
      const checkOutDate = parseDateValue(checkOutInput);

      if (!checkInDate) {
        setAlertMessage(messageEl, "Check-in date is required.");
        return false;
      }

      if (!checkOutDate) {
        setAlertMessage(messageEl, "Check-out date is required.");
        return false;
      }

      if (checkOutDate <= checkInDate) {
        setAlertMessage(messageEl, "Check-out date must be after check-in date.");
        return false;
      }

      setAlertMessage(messageEl, "");
      return true;
    };

    if (checkInInput) {
      checkInInput.addEventListener("change", () => {
        updateCheckOutMinimum();
        validateBookingDates();
      });
    }

    if (checkOutInput) {
      checkOutInput.addEventListener("change", validateBookingDates);
    }

    bookingForm.addEventListener("submit", (event) => {
      if (!validateBookingDates()) {
        event.preventDefault();
      }
    });
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
