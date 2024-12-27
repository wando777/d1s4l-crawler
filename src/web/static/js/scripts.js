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

    // Etapa 1: Login
    fetch("/scrape/login", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          const botId = data.bot_id;
          localStorage.setItem("bot_id", botId);
          // Etapa 2: Navegar para a página de dados
          return fetch("/scrape/navigate", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ bot_id: botId }),
          });
        } else {
          throw new Error(data.message);
        }
      })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          const botId = localStorage.getItem("bot_id");
          // Etapa 3: Selecionar opções e buscar dados
          return fetch("/scrape/select_options", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ bot_id: botId }),
          });
        } else {
          throw new Error(data.message);
        }
      })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // Etapa 4: Iniciar o polling para clicar nos links
          return clickLinksPolling();
        } else {
          throw new Error(data.message);
        }
      })
      .then(() => {
        const botId = localStorage.getItem("bot_id");
        const sorteio = localStorage.getItem("sorteio");
        // Etapa 5: Extrair dados e processar resultados
        return fetch("/scrape/extract", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ bot_id: botId, sorteio: sorteio }),
        });
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
      })
      .catch((error) => {
        // Ocultar o elemento de "loading" em caso de erro
        document.getElementById("overlay").style.display = "none";
        document.getElementById("loading").style.display = "none";
        alert("Erro: " + error.message);
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

function clickLinksPolling() {
  return new Promise((resolve, reject) => {
    function poll() {
      const botId = localStorage.getItem("bot_id");
      fetch("/scrape/click_links", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ bot_id: botId }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            if (data.message === "More links to click") {
              setTimeout(poll, 1000); // Poll novamente após 1 segundo
            } else {
              resolve();
            }
          } else {
            reject(new Error(data.message));
          }
        })
        .catch((error) => {
          reject(error);
        });
    }
    poll();
  });
}
