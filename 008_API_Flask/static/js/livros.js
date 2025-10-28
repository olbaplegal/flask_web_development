/*
- Busca e exibe a lista de livros que já existem no banco de dados.
- Captura os dados que o usuário digita no formulário e enviá para a API para criar um novo formulario.
- Mantem a página atualizada sem a necessidade de recarregá-la.
*/

// Define a URL base da API. Front e Back agora estão na mesma origem.
const url ='http://127.0.0.1:5000'

const formularioLivro = document.getElementById('form-livro');
const listaLivrosAdd = document.getElementById('lista-livros');

// FUNÇÃO PARA BUSCAR OS LIVROS NA API E EXIBIR NA TELA
const listaLivros = async () => {
    /*
    fetch* faz uma requisição HTTP(GET) para o endpoint /livros.
    async: transforma a função em uma função assíncrona. Permite o uso do 
    await, essa palavra-chave permite pausar a execução do código e esperar 
    que operações demoradas sejam concluídas.
    */
    try{
        const resposta = await fetch (`${url}/livros`);
        const livros = await resposta.json(); // Conversão para json

        // Limpa a lista atual
        listaLivrosAdd.innerHTML = '';

        // Para cada livro retornado pela API, cria um item na lista em HTML
        livros.forEach(livro => {
            const item = document.createElement('li');
            item.textContent = `${livro.id}: ${livro.titulo} - ${livro.autor}`;
            listaLivrosAdd.appendChild(item);
        });
    } catch (error) {
        console.error('Erro ao buscar livros: ', error);
        alert('Não foi possível carregar a lista de livros.')
    }
};

const insereLivro = async (event) => {
    event.preventDefault(); // Impede o comportamento padrão que é recarregar a página

    const titulo = document.getElementById('titulo').value;
    const autor = document.getElementById('autor').value;

    // Cria um objeto com os dados do livro
    const novoLivro = { titulo, autor };

    try {
        // fetch* faz uma requisição para o método POST
        const resposta = await fetch(`${url}/livros`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // arquivo JSON sendo enviado
            },
            body: JSON.stringify(novoLivro), // Converte um objeto Js para uma string JSON
        });

        if (resposta.ok) {
            alert('Livro adicionado com sucesso!');
            formularioLivro.reset();
            listaLivros();
        } else {
            alert('Erro ao adicionar livro.');
        }
    } catch (error) {
        console.error('Erro ao adicionar livro: ', error);
        alert('Ocorreu um erro de comunicação com a API.');
    }
};

// Adicionar um eventListener para o evento de 'submit' do formulario.
formularioLivro.addEventListener('submit', insereLivro);

listaLivros();
