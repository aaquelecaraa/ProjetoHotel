import streamlit as st
from datetime import date

from backend.database import criar_tabelas
from backend.gerenciador_reservas import GerenciadorDeReservas

# Garante que as tabelas existam ao iniciar o app
criar_tabelas()
gerenciador = GerenciadorDeReservas()


# ─────────────────────────────────────────
# CONFIGURAÇÃO BÁSICA DA PÁGINA
# ─────────────────────────────────────────
st.set_page_config(page_title="Sistema de Hospedagem", layout="wide")
st.title("🏨 Sistema de Hospedagem - Projeto POO")


# ─────────────────────────────────────────
# MENU LATERAL
# ─────────────────────────────────────────
menu = st.sidebar.radio(
    "Navegação",
    (
        "Cadastrar Cliente",
        "Cadastrar Quarto",
        "Criar Reserva",
        "Listar Clientes",
        "Listar Quartos",
        "Listar Reservas",
        "Exportar para CSV",
    )
)


# ─────────────────────────────────────────
# 1. CADASTRAR CLIENTE
# ─────────────────────────────────────────
if menu == "Cadastrar Cliente":
    st.header("Cadastrar Cliente")

    with st.form("form_cadastrar_cliente"):
        nome = st.text_input("Nome")
        telefone = st.text_input("Telefone")
        email = st.text_input("E-mail")

        enviado = st.form_submit_button("Salvar Cliente")

    if enviado:
        if not nome or not telefone or not email:
            st.error("Preencha todos os campos!")
        else:
            cliente = gerenciador.criar_cliente(nome, telefone, email)
            if cliente:
                st.success(f"Cliente cadastrado com sucesso! ID: {cliente.id}")
            else:
                st.error("Erro ao cadastrar cliente.")


# ─────────────────────────────────────────
# 2. CADASTRAR QUARTO
# ─────────────────────────────────────────
elif menu == "Cadastrar Quarto":
    st.header("Cadastrar Quarto")

    with st.form("form_cadastrar_quarto"):
        numero = st.number_input("Número do quarto", min_value=1, step=1)
        tipo = st.selectbox("Tipo do quarto", ["single", "double", "suite"])
        preco_diaria = st.number_input("Preço por diária (R$)", min_value=0.0, step=10.0)
        status = st.selectbox("Status", ["disponivel", "ocupado", "manutencao"])

        enviado = st.form_submit_button("Salvar Quarto")

    if enviado:
        quarto = gerenciador.criar_quarto(
            numero=int(numero),
            tipo=tipo,
            preco_diaria=float(preco_diaria),
            status=status,
        )
        if quarto:
            st.success(f"Quarto cadastrado com sucesso! ID: {quarto.id}")
        else:
            st.error("Erro ao cadastrar quarto.")


# ─────────────────────────────────────────
# 3. CRIAR RESERVA
# ─────────────────────────────────────────
elif menu == "Criar Reserva":
    st.header("Criar Reserva")

    clientes = gerenciador.listar_clientes()
    quartos = gerenciador.listar_quartos()

    if not clientes:
        st.warning("Nenhum cliente cadastrado. Cadastre um cliente primeiro.")
    elif not quartos:
        st.warning("Nenhum quarto cadastrado. Cadastre um quarto primeiro.")
    else:
        # Selecionar cliente
        opcoes_clientes = {f"{c.id} - {c.nome}": c.id for c in clientes}
        cliente_escolhido = st.selectbox(
            "Selecione o cliente",
            list(opcoes_clientes.keys()),
        )
        cliente_id = opcoes_clientes[cliente_escolhido]

        # Selecionar quarto
        opcoes_quartos = {f"{q.id} - Quarto {q.numero} ({q.tipo})": q.id for q in quartos}
        quarto_escolhido = st.selectbox(
            "Selecione o quarto",
            list(opcoes_quartos.keys()),
        )
        quarto_id = opcoes_quartos[quarto_escolhido]

        # Datas
        col1, col2 = st.columns(2)
        with col1:
            data_checkin = st.date_input("Data de check-in", value=date.today())
        with col2:
            data_checkout = st.date_input("Data de check-out", value=date.today())

        if data_checkout <= data_checkin:
            st.error("A data de check-out deve ser depois da data de check-in.")
        else:
            if st.button("Verificar disponibilidade e criar reserva"):
                disponivel = gerenciador.verificar_disponibilidade(
                    quarto_id,
                    data_checkin,
                    data_checkout,
                )
                if not disponivel:
                    st.error("Quarto NÃO está disponível neste período.")
                else:
                    reserva = gerenciador.criar_reserva(
                        cliente_id=cliente_id,
                        quarto_id=quarto_id,
                        data_checkin=data_checkin,
                        data_checkout=data_checkout,
                    )
                    if reserva:
                        st.success(f"Reserva criada com sucesso! ID: {reserva.id}")
                    else:
                        st.error("Erro ao criar reserva.")


# ─────────────────────────────────────────
# 4. LISTAR CLIENTES
# ─────────────────────────────────────────
elif menu == "Listar Clientes":
    st.header("Lista de Clientes")
    clientes = gerenciador.listar_clientes()

    if not clientes:
        st.info("Nenhum cliente cadastrado.")
    else:
        dados = [c.to_dict() for c in clientes]
        st.dataframe(dados)


# ─────────────────────────────────────────
# 5. LISTAR QUARTOS
# ─────────────────────────────────────────
elif menu == "Listar Quartos":
    st.header("Lista de Quartos")
    quartos = gerenciador.listar_quartos()

    if not quartos:
        st.info("Nenhum quarto cadastrado.")
    else:
        dados = [q.to_dict() for q in quartos]
        st.dataframe(dados)


# ─────────────────────────────────────────
# 6. LISTAR RESERVAS (COM CANCELAMENTO / EDIÇÃO SIMPLES)
# ─────────────────────────────────────────
elif menu == "Listar Reservas":
    st.header("Lista de Reservas")
    reservas = gerenciador.listar_reservas()

    if not reservas:
        st.info("Nenhuma reserva cadastrada.")
    else:
        # Mostrar como tabela
        dados = [r.to_dict() for r in reservas]
        st.dataframe(dados)

        st.subheader("Cancelar ou modificar reserva")
        ids_reservas = [r.id for r in reservas]
        reserva_id = st.selectbox("Selecione o ID da reserva", ids_reservas)

        col1, col2 = st.columns(2)

        # Cancelar
        with col1:
            if st.button("Cancelar reserva selecionada"):
                ok = gerenciador.cancelar_reserva(reserva_id)
                if ok:
                    st.success("Reserva cancelada com sucesso.")
                else:
                    st.error("Erro ao cancelar reserva.")

        # Modificar (apenas datas, para não complicar demais)
        with col2:
            st.write("Modificar datas da reserva")
            nova_data_checkin = st.date_input("Novo check-in")
            nova_data_checkout = st.date_input("Novo check-out")

            if nova_data_checkout <= nova_data_checkin:
                st.warning("Data de check-out deve ser depois do check-in.")
            else:
                if st.button("Salvar nova data"):
                    ok = gerenciador.modificar_reserva(
                        reserva_id,
                        {
                            "data_checkin": nova_data_checkin,
                            "data_checkout": nova_data_checkout,
                        },
                    )
                    if ok:
                        st.success("Reserva modificada com sucesso.")
                    else:
                        st.error("Erro ao modificar reserva.")


# ─────────────────────────────────────────
# 7. EXPORTAR PARA CSV
# ─────────────────────────────────────────
elif menu == "Exportar para CSV":
    st.header("Exportar dados para CSV")

    if st.button("Exportar Clientes"):
        gerenciador.exportar_clientes_para_csv()
        st.success("Clientes exportados para csv_data/clientes.csv")

    if st.button("Exportar Quartos"):
        gerenciador.exportar_quartos_para_csv()
        st.success("Quartos exportados para csv_data/quartos.csv")

    if st.button("Exportar Reservas"):
        gerenciador.exportar_reservas_para_csv()
        st.success("Reservas exportadas para csv_data/reservas.csv")