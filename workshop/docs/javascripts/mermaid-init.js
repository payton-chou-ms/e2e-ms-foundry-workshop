mermaid.initialize({
  startOnLoad: false,
});

document$.subscribe(() => {
  const mermaidBlocks = document.querySelectorAll("pre.mermaid");

  mermaidBlocks.forEach((block) => {
    const source = block.querySelector("code")?.textContent ?? block.textContent;

    if (!source) {
      return;
    }

    const container = document.createElement("div");
    container.className = "mermaid";
    container.textContent = source;
    block.replaceWith(container);
  });

  mermaid.run({
    querySelector: ".mermaid",
  });
});