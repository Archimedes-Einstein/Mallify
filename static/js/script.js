const formRange = document.getElementById("rangeId");
const formOutput = document.getElementById("rangeValue");
const currency = document.getElementById("currency");
const closeButton = document.querySelector('.btn-close')
const toast = document.querySelector('.toast')
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
const observer = new IntersectionObserver((entries)=>{
    entries.forEach((entry)=>{
        if(entry.isIntersecting){
            console.log(entry)
        }
    })
},{})
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
closeButton.addEventListener('click',()=>{
    toast.classList.toggle('remove-toast')
})