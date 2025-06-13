document.addEventListener("DOMContentLoaded", () => {
  const questions = [
    {
      name: "design",
      type: "checkbox",
      label: "ユーザー体験を向上させるために、どのようなデザイン思考を導入すべきですか？",
      options: ["共感", "問題定義", "アイデア出し", "プロトタイピング", "テスト"]
    },
    {
      name: "creative",
      type: "radio",
      label: "効果的な広告クリエイティブを制作するには、どのような要素を意識すべきですか？",
      options: ["印象的なビジュアル", "訴求力のあるコピー", "明確なターゲット設定"]
    },
    {
      name: "distribution",
      type: "select",
      label: "広告配信先を選定する際、どのようなデータや指標をもとに意思決定するのが良いですか？",
      options: ["CTRやCVR", "オーディエンスデータ", "リーチ数と頻度"]
    },
    {
      name: "validation",
      type: "textarea",
      label: "ペルソナ設計や顧客インサイトを抽出するために、どのような検証プロセスが有効でしょうか？"
    },
    {
      name: "competitive",
      type: "textarea",
      label: "自社サービスの市場優位性を、競合と比較してどのようにアピールすべきだと考えますか？"
    }
  ];

  const container = document.getElementById("question-area");

  questions.forEach(q => {
    const group = document.createElement("div");
    group.className = "form-group";

    const label = document.createElement("label");
    label.setAttribute("data-question", q.name);
    label.textContent = q.label;
    group.appendChild(label);

    if (q.type === "checkbox" || q.type === "radio") {
      const box = document.createElement("div");
      box.className = q.type === "checkbox" ? "checklist" : "radio-group";

      q.options.forEach(opt => {
        const input = document.createElement("input");
        input.type = q.type;
        input.name = q.name;
        input.value = opt;

        const optLabel = document.createElement("label");
        optLabel.appendChild(input);
        optLabel.append(` ${opt}`);
        box.appendChild(optLabel);
      });

      group.appendChild(box);
    } else if (q.type === "select") {
      const select = document.createElement("select");
      select.name = q.name;
      const defOpt = document.createElement("option");
      defOpt.value = "";
      defOpt.textContent = "選択してください";
      select.appendChild(defOpt);
      q.options.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt;
        option.textContent = opt;
        select.appendChild(option);
      });
      group.appendChild(select);
    } else if (q.type === "textarea") {
      const textarea = document.createElement("textarea");
      textarea.name = q.name;
      group.appendChild(textarea);
    }

    // loadingとresponseエリア
    const loading = document.createElement("div");
    loading.className = "loading";
    loading.id = `loading-${q.name}`;
    group.appendChild(loading);

    const response = document.createElement("div");
    response.className = "ai-response";
    response.id = `response-${q.name}`;
    group.appendChild(response);

    container.appendChild(group);
  });
});
