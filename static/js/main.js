const start = document.getElementById("start");
const temp_value = document.getElementById('temp-value')
const placaImage = document.getElementById("placa-image");

start.addEventListener("click", async (event) => {
  event.preventDefault();

  setInterval(async () => {
    const response = await fetch("/aplicar_soplete", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        'temperatura' : parseInt(temp_value.textContent)
      }),
    });

    if (response.ok) {
      const data = await response.json();
      placaImage.src = `data:image/png;base64,${data.image}`;
    } else {
      console.error("Error al actualizar la imagen de la placa.");
    }
  }, 1000);
});

function updateTempValue(value) {
  temp_value.textContent = value + '°C';
}