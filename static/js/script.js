const formRange = document.getElementById("rangeId");
const formOutput = document.getElementById("rangeValue");
const currency = document.getElementById("currency");
//const caretUp = document.getElementById("caret-up");
//const caretDown = document.getElementById("caret-down");
//cart;
//const numberOfItems = document.getElementById("number-of-items");

const instock = 20;
const sold = 3;
const rateConverter = () => {
  if (currency.value === "Dollar") {
    formOutput.textContent = `$${formRange.value}`;
  } else if (currency.value === "Euro") {
    let valueInEuro = Math.round(parseInt(formRange.value)/1.17);
    formOutput.textContent = `€${valueInEuro}`;
  } else {
    let valueInNaria = Math.round(1675.4 * parseInt(formRange.value));
    formOutput.textContent = `₦${valueInNaria}`;
  }
};
// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })
})()

rateConverter();

formRange.addEventListener("input", () => {
  console.log(currency.value);
  rateConverter();
});
currency.addEventListener("click", () => {
  rateConverter();
});
