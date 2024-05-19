// Função para adicionar campos dinamicamente
function addField() {
  // Verifica se já existem 5 campos adicionados
  if (document.querySelectorAll('.item').length >= 10) {
      alert("Você já adicionou o máximo de itens.");
      return;
  }

  // Cria um novo elemento de div
  var newItem = document.createElement("div");
  newItem.classList.add("item");

  // Adiciona o HTML dos campos conforme o modelo
  newItem.innerHTML = `
      <label for="item">Item:</label>
      <input type="text" name="item[]" required>
      <label for="conforme">Conforme:</label>
      <select name="conforme[]" required>
          <option value="">Selecione um valor</option>
          <option value="Conforme">Conforme</option>
          <option value="Não Conforme">Não Conforme</option>
      </select><br><br>
  `;

  // Adiciona o novo elemento ao formulário
  document.getElementById("flexible-items").appendChild(newItem);
}