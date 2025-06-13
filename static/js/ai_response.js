document.addEventListener("DOMContentLoaded", () => {
  const inputSelectors = [
    { name: "design", type: "checkbox" },
    { name: "creative", type: "radio" },
    { name: "distribution", type: "select" },
    { name: "validation", type: "textarea" },
    { name: "competitive", type: "textarea" }
  ];

  let lock = false;
  const previousValues = {};

  inputSelectors.forEach(({ name, type }) => {
    const elements = document.querySelectorAll(`[name="${name}"]`);
    const loadingEl = document.getElementById(`loading-${name}`);
    const responseEl = document.getElementById(`response-${name}`);
    const questionLabel = document.querySelector(`[data-question="${name}"]`);

    const handleInput = async () => {
      if (!loadingEl || !responseEl || !questionLabel || lock) return;

      let value = "";
      if (type === "checkbox") {
        value = Array.from(elements)
          .filter(el => el.checked)
          .map(el => el.value)
          .join("・");
      } else if (type === "radio") {
        const selected = Array.from(elements).find(el => el.checked);
        value = selected ? selected.value : "";
      } else {
        value = elements[0]?.value || "";
      }

      if (!value.trim() || value === previousValues[name]) {
        return;
      }

      previousValues[name] = value;
      const questionText = questionLabel.innerText.trim();

      loadingEl.style.display = "inline-block";
      loadingEl.innerHTML = `<img src="/static/img/loading.gif" alt="loading" width="24">`;
      responseEl.textContent = "";

      lock = true;
      try {
        const res = await fetch(`/ai-response`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            question_key: name,
            question_text: questionText,
            user_input: value
          })
        });

        const json = await res.json();
        if (json && json.answer) {
          const short = json.answer.length > 100
            ? json.answer.substring(0, 100) + "…"
            : json.answer;
          responseEl.textContent = short;
        } else {
          responseEl.textContent = "回答が取得できませんでした";
        }
      } catch (e) {
        console.error("AI取得エラー:", e);
        responseEl.textContent = "エラーが発生しました";
      } finally {
        loadingEl.style.display = "none";
        setTimeout(() => {
          lock = false;
        }, 3000);
      }
    };

    elements.forEach(el => {
      el.addEventListener(
        type === "textarea" || type === "select" ? "input" : "change",
        handleInput
      );
    });
  });
});
