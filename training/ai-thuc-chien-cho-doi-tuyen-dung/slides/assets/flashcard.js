(function () {
  const widgetSelector = "[data-dz-flashcard]";

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function parseData(widget) {
    const source = widget.querySelector(".dz-flashcard__data");
    if (!source) return null;

    try {
      const payload = JSON.parse(source.textContent || "{}");
      if (!Array.isArray(payload.cards) || payload.cards.length === 0) return null;
      return payload;
    } catch (error) {
      console.error("Invalid dz flashcard payload", error);
      return null;
    }
  }

  function createNode(tagName, className, text) {
    const node = document.createElement(tagName);
    if (className) node.className = className;
    if (typeof text === "string") node.textContent = text;
    return node;
  }

  function createButton(className, label, type) {
    const button = createNode("button", className, label);
    button.type = type || "button";
    return button;
  }

  function initWidget(widget) {
    const data = parseData(widget);
    if (!data) return;

    const labels = {
      title: data.title || "Flashcards",
      sources: data.sourcesLabel || "",
      reveal: data.revealLabel || "See answer",
      hide: data.hideLabel || "Hide answer",
      hint: data.hintLabel || "Click card to flip",
      prev: data.prevLabel || "←",
      next: data.nextLabel || "→",
      wrong: data.wrongLabel || "✕",
      correct: data.correctLabel || "✓",
      menu: data.menuLabel || "•••",
    };

    const state = {
      index: 0,
      revealed: false,
      marks: new Array(data.cards.length).fill(null),
    };

    widget.classList.add("dz-flashcard");
    widget.setAttribute("tabindex", "0");
    widget.setAttribute("role", "group");
    widget.setAttribute("aria-label", labels.title);

    const header = createNode("div", "dz-flashcard__header");
    const headingBlock = createNode("div");
    const title = createNode("h3", "dz-flashcard__title", labels.title);
    const sources = createNode("p", "dz-flashcard__sources", labels.sources);
    const menu = createNode("div", "dz-flashcard__menu", labels.menu);
    menu.setAttribute("aria-hidden", "true");
    headingBlock.append(title);
    if (labels.sources) headingBlock.append(sources);
    header.append(headingBlock, menu);

    const stage = createNode("div", "dz-flashcard__stage");
    const card = createNode("div", "dz-flashcard__card");
    card.setAttribute("role", "button");
    card.setAttribute("tabindex", "0");
    card.setAttribute("aria-pressed", "false");

    const count = createNode("div", "dz-flashcard__count");
    const front = createNode("div", "dz-flashcard__face");
    const term = createNode("p", "dz-flashcard__term");
    front.append(term);

    const back = createNode("div", "dz-flashcard__face");
    const answer = createNode("p", "dz-flashcard__answer");
    back.append(answer);

    const toggle = createButton("dz-flashcard__toggle", labels.reveal);
    const hint = createNode("p", "dz-flashcard__hint", labels.hint);

    card.append(count, front, back, toggle);
    stage.append(card, hint);

    const footer = createNode("div", "dz-flashcard__footer");
    const prev = createButton("dz-flashcard__nav-button", labels.prev);
    const wrong = createButton("dz-flashcard__score-button dz-flashcard__score-button--wrong", labels.wrong);
    const wrongValue = createNode("span", "dz-flashcard__score-value", "0");
    wrong.append(wrongValue);

    const correct = createButton("dz-flashcard__score-button dz-flashcard__score-button--correct", labels.correct);
    const correctValue = createNode("span", "dz-flashcard__score-value", "0");
    correct.append(correctValue);

    const next = createButton("dz-flashcard__nav-button", labels.next);
    footer.append(prev, wrong, correct, next);

    widget.replaceChildren(header, stage, footer);

    function getCard() {
      return data.cards[state.index] || data.cards[0];
    }

    function getScore(markType) {
      return state.marks.filter((mark) => mark === markType).length;
    }

    function render() {
      const current = getCard();
      count.textContent = `${state.index + 1} / ${data.cards.length}`;
      term.textContent = current.term || "";
      answer.textContent = current.answer || "";
      front.hidden = state.revealed;
      back.hidden = !state.revealed;
      toggle.textContent = state.revealed ? labels.hide : labels.reveal;
      toggle.setAttribute("aria-label", state.revealed ? labels.hide : labels.reveal);
      card.setAttribute("aria-label", state.revealed ? `Answer: ${current.answer || ""}` : `Keyword: ${current.term || ""}`);
      card.setAttribute("aria-pressed", state.revealed ? "true" : "false");
      wrongValue.textContent = String(getScore("wrong"));
      correctValue.textContent = String(getScore("correct"));
      prev.disabled = state.index === 0;
      next.disabled = state.index === data.cards.length - 1;
    }

    function reveal(nextValue) {
      state.revealed = typeof nextValue === "boolean" ? nextValue : !state.revealed;
      render();
    }

    function go(delta) {
      const nextIndex = clamp(state.index + delta, 0, data.cards.length - 1);
      if (nextIndex === state.index) return;
      state.index = nextIndex;
      state.revealed = false;
      render();
    }

    function mark(type) {
      state.marks[state.index] = type;
      render();
      if (state.index < data.cards.length - 1) {
        go(1);
      }
    }

    function stop(event) {
      event.preventDefault();
      event.stopPropagation();
    }

    card.addEventListener("click", (event) => {
      stop(event);
      reveal();
      widget.focus();
    });

    card.addEventListener("keydown", (event) => {
      if (event.key !== "Enter" && event.key !== " ") return;
      stop(event);
      reveal();
    });

    toggle.addEventListener("click", (event) => {
      stop(event);
      reveal();
    });

    prev.addEventListener("click", (event) => {
      stop(event);
      go(-1);
      widget.focus();
    });

    next.addEventListener("click", (event) => {
      stop(event);
      go(1);
      widget.focus();
    });

    wrong.addEventListener("click", (event) => {
      stop(event);
      mark("wrong");
      widget.focus();
    });

    correct.addEventListener("click", (event) => {
      stop(event);
      mark("correct");
      widget.focus();
    });

    widget.addEventListener("pointerdown", () => {
      widget.focus();
    });

    widget.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        stop(event);
        go(-1);
        return;
      }

      if (event.key === "ArrowRight") {
        stop(event);
        go(1);
        return;
      }

      if (event.key === "Enter" || event.key === " ") {
        stop(event);
        reveal();
      }
    });

    render();
  }

  document.querySelectorAll(widgetSelector).forEach(initWidget);
})();
