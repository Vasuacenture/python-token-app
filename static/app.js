const form = document.querySelector("#token-form");
const labelInput = document.querySelector("#label");
const generateButton = document.querySelector("#generate-button");
const result = document.querySelector("#result");
const message = document.querySelector("#message");
const tokenPanel = document.querySelector("#token-panel");
const tokenValue = document.querySelector("#token-value");
const copyButton = document.querySelector("#copy-button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.hidden = false;
  tokenPanel.hidden = true;
  message.className = "result-message";
  message.textContent = "Generating your token...";
  generateButton.disabled = true;

  try {
    const response = await fetch("/api/token", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ label: labelInput.value }),
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.error || "The token could not be generated.");
    }

    tokenValue.textContent = payload.token;
    tokenPanel.hidden = false;
    message.textContent = `Token created for "${payload.label}".`;
    message.classList.add("success");
  } catch (error) {
    message.textContent = error instanceof Error
      ? error.message
      : "Something went wrong. Please try again.";
    message.classList.add("error");
  } finally {
    generateButton.disabled = false;
  }
});

copyButton.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(tokenValue.textContent);
    copyButton.textContent = "Copied";
  } catch {
    message.textContent = "Copy was unavailable. Select and copy the token instead.";
    message.classList.add("error");
  }
});
