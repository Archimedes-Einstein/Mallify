const formRange = document.getElementById("rangeId");
const formOutput = document.getElementById("rangeValue");
const currency = document.getElementById("currency");
const caretUp = document.getElementById("caret-up");
const caretDown = document.getElementById("caret-down");
cart;
const numberOfItems = document.getElementById("number-of-items");

const instock = 20;
const sold = 3;
const rateConverter = () => {
  if (currency.value === "Dollar") {
    formOutput.textContent = `$${formRange.value}`;
  } else if (currency.value === "Euro") {
    let valueInEuro = Math.round(1.17 * parseInt(formRange.value));
    formOutput.textContent = `€${valueInEuro}`;
  } else {
    let valueInNaria = Math.round(1675.4 * parseInt(formRange.value));
    formOutput.textContent = `₦${valueInNaria}`;
  }
};

caretDown.addEventListener("click", () => {
  let caretValue = parseInt(numberOfItems.textContent);
  if (caretValue > 1) {
    numberOfItems.textContent = `${caretValue - 1}`;
  }
  // console.log(caretValue);
});
caretUp.addEventListener("click", () => {
  let caretValue2 = parseInt(numberOfItems.textContent);
  if (caretValue2 < instock) {
    numberOfItems.textContent = `${caretValue2 + 1}`;
  }
});
rateConverter();

formRange.addEventListener("input", () => {
  console.log(currency.value);
  rateConverter();
});
currency.addEventListener("click", () => {
  rateConverter();
});
