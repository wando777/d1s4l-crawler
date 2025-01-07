document
  .getElementById("scrape-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);

    fetch("/scrape", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = "";

        if (data.status === "success") {
          resultDiv.innerHTML = `<p>Scraping iniciado com sucesso. Use o ID <strong>${data.scrape_id}</strong> para verificar o status.</p>`;
        } else {
          resultDiv.innerHTML = `<p>Erro: ${data.message}</p>`;
        }
      });
  });

document
  .getElementById("search-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const scrapeId = document.getElementById("scrape-id").value;

    fetch(`/scrape/status/${scrapeId}`)
      .then((response) => response.json())
      .then((data) => {
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = "";

        if (data.status === "success") {
          displayResults(data.grupos_cotas, data.result);
        } else {
          resultDiv.innerHTML = `<p>${data.message}</p>`;
        }
      });
  });

function displayResults(gruposCotas, result) {
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  // Tabela de todas as cotas do scraping
  let tableHtml =
    "<h2>Todas as Cotas</h2><table class='table table-striped'><tr><th>Grupo</th><th>Cotas</th></tr>";
  for (const [grupo, cotas] of Object.entries(gruposCotas)) {
    tableHtml += `<tr><td>${grupo}</td><td>${cotas.join(", ")}</td></tr>`;
  }
  tableHtml += "</table>";
  resultDiv.innerHTML += tableHtml;

  // Tabela de resultado do GruposCotasProcessor
  tableHtml = "<h2>Resultado</h2><table class='table table-striped'><tr><th>Grupo</th><th>Cotas</th></tr>";
  if (Object.keys(result).length === 0) {
    tableHtml += "<tr><td colspan='2'>Não foram encontradas cotas.</td></tr>";
  } else {
    for (const [grupo, cotas] of Object.entries(result)) {
      tableHtml += `<tr><td>${grupo}</td><td>${cotas.join(", ")}</td></tr>`;
    }
  }
  tableHtml += "</table>";
  resultDiv.innerHTML += tableHtml;
}