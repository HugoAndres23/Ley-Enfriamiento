const start = document.getElementById("start");
const stop = document.getElementById("stop");
const temp_value = document.getElementById('temp-value');
const placaImage = document.getElementById("placa-image");
const table_container = document.getElementsByClassName("table_container")[0];
const posX = document.getElementById('pos-x');
const posY = document.getElementById('pos-y');
const tiempo = document.getElementById('tiempo');
const radio = document.getElementById('radio');

posX.addEventListener('input', () => validateInput(posX));
posY.addEventListener('input', () => validateInput(posY));

let intervalId;

start.addEventListener("click", async (event) => {
  event.preventDefault();

  intervalId = setInterval(async () => {
    const response = await fetch("/aplicar_soplete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        'temperatura': parseInt(temp_value.textContent),
        "posicion": [parseInt(posY.value), parseInt(posX.value)],
        "radio": parseInt(radio.value),
      }),
    });

    if (response.ok) {
      const data = await response.json();
      placaImage.src = `data:image/png;base64,${data.image}`;
      table_container.innerHTML = data.table;
      tiempo.textContent = parseInt(tiempo.textContent) + 1 + ' Segundos';
    } else {
      console.error("Error al actualizar la imagen de la placa.");
    }
  }, 1000);
});

stop.addEventListener("click", (event) => {
  event.preventDefault();

  if (intervalId) {
    clearInterval(intervalId);
  }
});

function updateTempValue(value) {
  temp_value.textContent = value + '°C';
}

function validateInput(input) {
  const min = parseInt(input.min);
  const max = parseInt(input.max);
  let value = parseInt(input.value);

  if (value < min) value = min;
  if (value > max) value = max;

  input.value = value;
}
