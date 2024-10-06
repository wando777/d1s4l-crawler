document
  .getElementById("scrape-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);

    // Salvar os dados do formulário no localStorage
    localStorage.setItem("username", formData.get("username"));
    localStorage.setItem("sorteio", formData.get("sorteio"));

    // Mostrar o elemento de "loading"
    document.getElementById("overlay").style.display = "block";
    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    fetch("/scrape", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        // Ocultar o elemento de "loading"
        document.getElementById("overlay").style.display = "none";
        document.getElementById("loading").style.display = "none";
        document.getElementById("result").style.display = "block";

        if (data.status === "success") {
          displayResults(data.grupos_cotas, data.result);
        } else {
          alert("Erro: " + data.message);
        }
      });
  });

// Função para preencher o formulário com os dados do localStorage
function populateForm() {
  if (localStorage.getItem("username")) {
    document.getElementById("username").value =
      localStorage.getItem("username");
  }
  if (localStorage.getItem("sorteio")) {
    document.getElementById("sorteio").value = localStorage.getItem("sorteio");
  }
}

// Chamar a função para preencher o formulário quando a página carregar
window.onload = populateForm;

function displayResults(gruposCotas, result) {
  const resultDiv = document.getElementById("result");
  resultDiv.innerHTML = "";

  // Tabela de todas as cotas do scraping
  let tableHtml =
    "<h2>Todas as Cotas</h2><table><tr><th>Grupo</th><th>Cotas</th></tr>";
  for (const [grupo, cotas] of Object.entries(gruposCotas)) {
    tableHtml += `<tr><td>${grupo}</td><td>${cotas.join(", ")}</td></tr>`;
  }
  tableHtml += "</table>";
  resultDiv.innerHTML += tableHtml;

  // Tabela de resultado do GruposCotasProcessor
  tableHtml = "<h2>Resultado</h2><table><tr><th>Grupo</th><th>Cotas</th></tr>";
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
