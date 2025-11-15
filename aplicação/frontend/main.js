const API_URL = "https://z9sp7511wd.execute-api.sa-east-1.amazonaws.com/dev/feedback";

function setStatus(text, ok = false) {
  const el = document.getElementById("status");
  el.textContent = text;
  el.className = `status ${ok ? "ok" : "err"}`;
}

document.getElementById("feedbackForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nome = document.getElementById("nome").value.trim();
  const email = document.getElementById("email").value.trim();
  const mensagem = document.getElementById("mensagem").value.trim();

  if (!nome || !email || !mensagem) {
    setStatus("Preencha todos os campos.");
    return;
  }

  setStatus("Enviando...", true);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nome, email, mensagem })
    });

    if (response.ok) {
      setStatus("Feedback enviado com sucesso!", true);
      document.getElementById("feedbackForm").reset();
    } else {
      const text = await response.text();
      setStatus(`Erro ao enviar: ${response.status} ${text}`);
    }
  } catch (err) {
    setStatus(`Falha de rede: ${err.message}`);
  }
});
