import java.nio.charset.Charset;
import java.util.NoSuchElementException;
import java.util.Random;
import java.util.Scanner;
import java.util.function.Function;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;

public class App {

    /** Nome do arquivo de dados de produtos. O arquivo deve estar localizado na raiz do projeto */
    static String nomeArquivoProdutos;

    /** Nome do arquivo de clientes. O arquivo deve estar localizado na raiz do projeto */
    static String nomeArquivoClientes;
    
    /** Scanner para leitura de dados do teclado */
    static Scanner teclado;

    /** Aleatório para gerador de pedidos */
    static Random sorteio = new Random(42);

    /** Quantidade de produtos cadastrados atualmente na lista */
    static int quantosProdutos = 0;

    /** estruturas principais para armazenar produtos e clientes */
    static ABB<Integer, Produto> produtosPorId;
    static ABB<String, Produto> produtosPorNome;
    static ABB<Integer, Cliente> clientesPorId;
    
    /** Para associar produtos aos pedidos que os contêm */
    static TabelaHash<Produto, Lista<Pedido>> pedidosPorProduto;

    /** Para associar produtos aos clientes que os compraram */
    static TabelaHash<Produto, Lista<Cliente>> clientesPorProduto;

    static void limparTela() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    /** Gera um efeito de pausa na CLI. Espera por um enter para continuar */
    static void pausa() {
        System.out.println("Digite enter para continuar...");
        teclado.nextLine();
    }

    /** Cabeçalho principal da CLI do sistema */
    static void cabecalho() {
        limparTela();
        System.out.println("AEDs II COMÉRCIO DE COISINHAS");
        System.out.println("=============================");
    }
    
    static <T extends Number> T lerOpcao(String mensagem, Class<T> classe) {
        T valor;
        System.out.println(mensagem);
        try {
            valor = classe.getConstructor(String.class).newInstance(teclado.nextLine());
        } catch (Exception e) {
            return null;
        }
        return valor;
    }

    /** Imprime o menu principal, lê a opção do usuário e a retorna (int).
     * Perceba que poderia haver uma melhor modularização com a criação de uma classe Menu.
     * @return Um inteiro com a opção do usuário.
    */
    static int menu() {
        cabecalho();
        System.out.println("PRODUTOS E PEDIDOS");
        System.out.println("=======================================");
        System.out.println("1 - Procurar produtos, por id");
        System.out.println("2 - Recortar produtos, por descrição");
        System.out.println("3 - Pedidos de um produto, em arquivo");
        System.out.println("CLIENTES E PEDIDOS");
        System.out.println("=======================================");
        System.out.println("4 - Relatório de clientes, por id");
        System.out.println("5 - Nomes e documentos de clientes que compraram um produto");
        System.out.println("\n0 - Sair");
        System.out.print("Digite sua opção: ");
        return Integer.parseInt(teclado.nextLine());
    }

    static <T> ABB<T, Cliente> lerClientes(String nomeArquivoDados, Function<Cliente, T> extratora){
        AVL<T, Cliente> clientes = new AVL<>();
        int doc = 10_000;

        try (Scanner arq = new Scanner(new File(nomeArquivoDados), Charset.forName("UTF-8"))) {
            int quantNomes = Integer.parseInt(arq.nextLine());
            String[] nomes = new String[quantNomes];
            String[] sobrenomes = new String[quantNomes];
            for (int i = 0; i < quantNomes; i++) {
                String[] linha = arq.nextLine().split(" ");
                nomes[i] = linha[0];
                sobrenomes[i] = linha[1];
            }
            for (String nome : nomes) {
                for (String sobrenome : sobrenomes) {
                    String nomeCompleto = nome + " " + sobrenome;
                    Cliente cliente = new Cliente(nomeCompleto, doc++);
                    clientes.inserir(extratora.apply(cliente), cliente);
                }
            }
        } catch (IOException e) {
            Cliente cliente = new Cliente("João Silva", doc);
            clientes.inserir(extratora.apply(cliente), cliente);
        }

        return clientes;
    }

    static <T> ABB<T, Produto> lerProdutos(String nomeArquivoDados, Function<Produto, T> extratorDeChave) {
        Scanner arquivo = null;
        int numProdutos;
        String linha;
        Produto produto;
        ABB<T, Produto> produtosCadastrados;

        try {
            arquivo = new Scanner(new File(nomeArquivoDados), Charset.forName("UTF-8"));
            numProdutos = Integer.parseInt(arquivo.nextLine());
            produtosCadastrados = new AVL<>();

            for (int i = 0; i < numProdutos; i++) {
                linha = arquivo.nextLine();
                produto = Produto.criarDoTexto(linha);
                T chave = extratorDeChave.apply(produto);
                produtosCadastrados.inserir(chave, produto);
            }
            quantosProdutos = produtosCadastrados.tamanho();

        } catch (IOException e) {
            produtosCadastrados = null;
        } finally {
            if (arquivo != null) arquivo.close();
        }

        return produtosCadastrados;
    }

    public static Pedido pedidoComItensAleatorios() {
        Pedido novoPedido = new Pedido();
        int quantProdutos = sorteio.nextInt(8) + 1;
    
        int indiceSorteado = sorteio.nextInt(clientesPorId.tamanho());
        Cliente clienteSorteado = clientesPorId.obterPorIndice(indiceSorteado);
        clienteSorteado.adicionarPedido(novoPedido);
    
        for (int j = 0; j < quantProdutos; j++) {
            int idProduto = sorteio.nextInt(produtosPorId.tamanho()) + 10_000;
            Produto prod = produtosPorId.pesquisar(idProduto);
            novoPedido.incluirProduto(prod);
            inserirNaTabela(pedidosPorProduto, prod, novoPedido);
            inserirNaTabela(clientesPorProduto, prod, clienteSorteado);
        }
    
        return novoPedido;
    }
    

    

    static Produto localizarProdutoID() {
        cabecalho();
        System.out.println("LOCALIZANDO POR ID");
        int ID = lerOpcao("Digite o ID para busca", Integer.class);
        Produto localizado = localizarProduto(produtosPorId, ID);
        mostrarProduto(localizado);
        return localizado;
    }

    static <K> Produto localizarProduto(ABB<K, Produto> produtosCadastrados, K chave){
        cabecalho();
        Produto localizado = produtosCadastrados.pesquisar(chave);
        System.out.println("Tempo: " + produtosCadastrados.getTempo());
        System.out.println("Comparações: " + produtosCadastrados.getComparacoes());
        pausa();
        return localizado;
    }

    private static void mostrarProduto(Produto produto) {
        cabecalho();
        String mensagem = "Dados inválidos para o produto!";
        if (produto != null){
            mensagem = String.format("Dados do produto:\n%s", produto);
        }
        System.out.println(mensagem);
    }

    private static Lista<Pedido> gerarPedidos(int quantidade){
        Lista<Pedido> pedidos = new Lista<>();
        for (int i = 0; i < quantidade; i++) {
            Pedido ped = pedidoComItensAleatorios();
            pedidos.inserir(ped);
        }
        return pedidos;
    }

    private static <K,V> void inserirNaTabela(TabelaHash<K,Lista<V>> tabela, K chave, V dado){
        Lista<V> sublista;
        try {
            sublista = tabela.pesquisar(chave);
        } catch (NoSuchElementException nex) {
            sublista = new Lista<>();
            tabela.inserir(chave, sublista);
        }
        sublista.inserir(dado);
    }

    private static void recortarArvore(ABB<String, Produto> arvore) {
        cabecalho();
        System.out.print("Digite ponto de início do filtro: ");
        String descIni = teclado.nextLine();
        System.out.print("Digite ponto de fim do filtro: ");
        String descFim = teclado.nextLine();
        System.out.println(arvore.recortar(descIni, descFim));
    }

    static void pedidosDoProduto(){
        Produto produto = localizarProdutoID();
        String nomeArquivo = "RelatorioProduto" + produto.hashCode() + ".txt";
        try (FileWriter arquivoRelatorio = new FileWriter(nomeArquivo)) {
            Lista<Pedido> listaProd = pedidosPorProduto.pesquisar(produto);
            arquivoRelatorio.append(listaProd + "\n");
            System.out.println("Dados salvos em " + nomeArquivo);
        } catch (IOException e) {
            System.out.println("Problemas para criar o arquivo " + nomeArquivo + ". Tente novamente");
        }
    }

    static void clientesPorProduto(){
        Produto produto = localizarProdutoID();
        if (produto == null) {
            System.out.println("Produto não encontrado.");
            return;
        }
    
        System.out.println("Clientes que compraram o produto: " + produto);
        try {
            Lista<Cliente> listaClientes = clientesPorProduto.pesquisar(produto);
            int tamanho = listaClientes.tamanho();
            for (int i = 0; i < tamanho; i++) {
                Cliente cliente = listaClientes.obterPorIndice(i);
                System.out.println(cliente);
            }
        } catch (NoSuchElementException e) {
            System.out.println("Nenhum cliente comprou este produto.");
        }
    }
    

    public static void relatorioDeCliente(){
        cabecalho();
        System.out.println("RELATÓRIO DE CLIENTE POR DOCUMENTO");
        Integer doc = lerOpcao("Digite o número do documento do cliente:", Integer.class);
        if (doc == null) {
            System.out.println("Documento inválido.");
            return;
        }

        Cliente cliente = clientesPorId.pesquisar(doc);
        if (cliente == null) {
            System.out.println("Cliente não encontrado.");
            return;
        }

        System.out.println("Cliente: " + cliente);
        System.out.printf("Total gasto: R$ %.2f\n", cliente.totalGasto());

        System.out.println("Pedidos realizados:");
        for (Pedido p : cliente.getPedidos()) {
            System.out.println(p);
        }
    }

    static void configurarSistema(){
        nomeArquivoProdutos = "produtos.txt";
        nomeArquivoClientes = "nomes.txt";
        produtosPorId = lerProdutos(nomeArquivoProdutos, Produto::hashCode);
        clientesPorId = lerClientes(nomeArquivoClientes, Cliente::hashCode);
        produtosPorNome = new AVL<>(produtosPorId, prod -> prod.descricao, String::compareTo);
        pedidosPorProduto = new TabelaHash<>((int)(produtosPorId.tamanho() * 1.25));
        clientesPorProduto = new TabelaHash<>((int)(produtosPorId.tamanho() * 1.25));
        gerarPedidos(25000);
    }

    public static void main(String[] args) {
        teclado = new Scanner(System.in, Charset.forName("UTF-8"));
        configurarSistema();
        int opcao = -1;

        do {
            opcao = menu();
            switch (opcao) {
                case 1 -> localizarProdutoID();
                case 2 -> recortarArvore(produtosPorNome);
                case 3 -> pedidosDoProduto();
                case 4 -> relatorioDeCliente();
                case 5 -> clientesPorProduto();
            }
            pausa();
        } while (opcao != 0);

        teclado.close();
    }
}
