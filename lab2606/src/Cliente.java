public class Cliente {

    private String nome;
    private int documento;
    private Pedido[] pedidos; 
    private int quantidadePedidos; 

    public Cliente(String nome, int documento){
        if (!nome.contains(" ") || nome.trim().split(" ").length != 2)
            throw new IllegalArgumentException("Favor cadastrar cliente com um nome e um sobrenome");
        if (documento < 10_000)
            throw new IllegalArgumentException("Documentos válidos devem ter pelo menos 5 dígitos");

        this.nome = nome;
        this.documento = documento;
        this.pedidos = new Pedido[100];
        this.quantidadePedidos = 0;
    }

    public void adicionarPedido(Pedido novo){
        if (novo == null)
            throw new IllegalArgumentException("Pedido não pode ser nulo");
        if (quantidadePedidos >= pedidos.length)
            redimensionar(); 
        pedidos[quantidadePedidos++] = novo;
    }

    private void redimensionar() {
        Pedido[] novoVetor = new Pedido[pedidos.length * 2];
        for (int i = 0; i < pedidos.length; i++) {
            novoVetor[i] = pedidos[i];
        }
        pedidos = novoVetor;
    }

    public double totalGasto(){
        double total = 0.0;
        for (int i = 0; i < quantidadePedidos; i++) {
            total += pedidos[i].valorFinal(); 
        }
        return total;
    }

    public Pedido[] getPedidos() {
        Pedido[] resultado = new Pedido[quantidadePedidos];
        for (int i = 0; i < quantidadePedidos; i++) {
            resultado[i] = pedidos[i];
        }
        return resultado;
    }

    @Override
    public String toString(){
        return nome + " (" + documento + ")";
    }

    @Override
    public int hashCode(){
        return documento;
    }
}
