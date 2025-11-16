const API_URL = "https://z9sp7511wd.execute-api.sa-east-1.amazonaws.com/dev/feedback";

function setStatus(text, type = "info", loading = false) {
  const el = document.getElementById("status");
  el.innerHTML = loading
    ? `<span class="spinner"></span> <span>${text}</span>`
    : `<i class="bi ${type === "ok" ? "bi-check-circle-fill" : type === "err" ? "bi-x-circle-fill" : "bi-info-circle"}"></i> <span>${text}</span>`;
  el.className = `status ${type}`;
}

function isValidEmail(email) {
  return /^[\w\.-]+@[\w\.-]+\.\w+$/.test(email) && email.endsWith('.com');
}

let mensagemTouched = false;

function updateEmailStatus() {
  const email = document.getElementById("email").value.trim();
  const el = document.getElementById("emailStatus");
  if (!email) {
    el.innerHTML = "";
    return;
  }
  if (isValidEmail(email)) {
    el.innerHTML = '<i class="bi bi-check-circle-fill" style="color:#0f766e"></i>';
  } else {
    el.innerHTML = '<i class="bi bi-x-circle-fill" style="color:#b91c1c"></i>';
  }
}

function updateMensagemStatus() {
  const mensagem = document.getElementById("mensagem").value.trim();
  const el = document.getElementById("mensagemStatus");
  if (!mensagem && mensagemTouched) {
    el.innerHTML = '<i class="bi bi-exclamation-circle-fill" style="color:#b91c1c"></i>';
  } else if (mensagem) {
    el.innerHTML = '<i class="bi bi-check-circle-fill" style="color:#0f766e"></i>';
  } else {
    el.innerHTML = '';
  }
}

const form = document.getElementById("feedbackForm");
const btnEnviar = document.getElementById("btnEnviar");

document.getElementById("email").addEventListener("input", updateEmailStatus);
document.getElementById("mensagem").addEventListener("input", updateMensagemStatus);
document.getElementById("mensagem").addEventListener("focus", function() {
  mensagemTouched = true;
  updateMensagemStatus();
});

// Inicializa status ao carregar
updateEmailStatus();
updateMensagemStatus();

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const mensagem = document.getElementById("mensagem").value.trim();

  if (!nome) {
    setStatus("Preencha o nome.", "err");
    document.getElementById("nome").focus();
    return;
  }
  if (!email) {
    setStatus("Preencha o e-mail.", "err");
    document.getElementById("email").focus();
    return;
  }
  if (!isValidEmail(email)) {
    setStatus("E-mail inválido.", "err");
    document.getElementById("email").focus();
    return;
  }
  if (!mensagem) {
    setStatus("Preencha a mensagem.", "err");
    document.getElementById("mensagem").focus();
    return;
  }
  if (nome.length > 100) {
    setStatus("Nome deve ter no máximo 100 caracteres.", "err");
    return;
  }
  if (email.length > 100) {
    setStatus("E-mail deve ter no máximo 100 caracteres.", "err");
    return;
  }
  if (mensagem.length > 1000) {
    setStatus("Mensagem deve ter no máximo 1000 caracteres.", "err");
    return;
  }

  setStatus("Enviando...", "info", true);
  btnEnviar.disabled = true;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, email, mensagem })
    });

    const respJson = await response.json();
    if (response.ok) {
      setStatus("Feedback enviado com sucesso! Obrigado por participar.", "ok");
      form.reset();
      updateEmailStatus();
      updateMensagemStatus();
    } else if (respJson.error) {
      setStatus(respJson.error, "err");
    } else {
      setStatus(`Erro ao enviar: ${response.status}`, "err");
    }
  } catch (err) {
    setStatus(`Falha de rede: ${err.message}`, "err");
  } finally {
    btnEnviar.disabled = false;
  }
});
