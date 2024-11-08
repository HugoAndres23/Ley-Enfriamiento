document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".num");

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      const operation = button.getAttribute("data-operation");
      const pantalla = document.getElementById("pantalla");
      if (operation === "equal") {
        fetch("/calculadora", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ expression: pantalla.value }),
        })
          .then((response) => response.json())
          .then((result) => {
            pantalla.value = result;
          })
      } else if (operation === "clear") {
        pantalla.value = "";
      } else {
        pantalla.value += operation;
      }
    });
  });
});