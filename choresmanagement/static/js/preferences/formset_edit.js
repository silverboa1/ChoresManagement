document.addEventListener("DOMContentLoaded", function () {

  // Додавання форми
  document.querySelectorAll("[data-formset-add-btn]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const prefix = btn.getAttribute("data-formset-add-btn");
      const totalFormsInput = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);

      if (!totalFormsInput) {
        console.error(`❌ Не знайдено management_form для префікса: ${prefix}`);
        return;
      }

      let formCount = parseInt(totalFormsInput.value, 10);
      const container = document.querySelector(`[data-formset-container='${prefix}']`);
      const emptyFormTemplate = document.querySelector(`#empty-form-template-${prefix}`).innerHTML;

      const newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);
      container.insertAdjacentHTML("beforeend", newFormHtml);

      totalFormsInput.value = formCount + 1;

      attachRemoveHandlers(container);
    });
  });

  // 🔥 Обробник кнопок "✖"
  function attachRemoveHandlers(container) {
    container.querySelectorAll(".remove-form-btn").forEach(function (btn) {
      if (!btn.dataset.bound) { // 👈 уникаємо дублювання обробників
        btn.dataset.bound = "true";
        btn.addEventListener("click", function () {
          const formRow = btn.closest("[data-form]");
          const deleteCheckbox = formRow.querySelector("input[type='checkbox'][name$='-DELETE']");
          if (deleteCheckbox) {
            deleteCheckbox.checked = true;
          }
          formRow.style.display = "none";
        });
      }
    });
  }

  // Підключаємо видалення для вже наявних форм
  document.querySelectorAll("[data-formset-container]").forEach(function (container) {
    attachRemoveHandlers(container);
  });
}); 