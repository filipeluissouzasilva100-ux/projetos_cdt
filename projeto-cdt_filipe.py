import tkinter as tk
from tkinter import messagebox

class ImpulseWorkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ImpulseWork - Aceleração de Carreiras")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Estado dos Dados
        self.dados_usuario = {}
        self.etapa_atual = 0

        # Temas de Cores
        self.temas = {
            "escuro": {
                "bg_base": "#0F172A",
                "bg_card": "#1E293B",
                "accent": "#6366F1",
                "text_primary": "#F8FAFC",
                "text_secondary": "#94A3B8",
                "entry_bg": "#0F172A",
                "entry_fg": "#F8FAFC",
                "border": "#334155"
            },
            "claro": {
                "bg_base": "#B4D5F6",
                "bg_card": "#FFFFFF",
                "accent": "#0284C7",
                "text_primary": "#0F172A",
                "text_secondary": "#475569",
                "entry_bg": "#F8FAFC",
                "entry_fg": "#0F172A",
                "border": "#CBD5E1"
            }
        }
        self.tema_atual = "escuro"

        # Contentor Principal Único
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)

        # Definição do Fluxo de Telas
        self.etapas = [
            self.criar_tela_boas_vindas,
            self.criar_etapa_dados_pessoais,
            self.criar_etapa_contato_endereco,
            self.criar_etapa_perfil_profissional,
            self.criar_etapa_objetivo_resumo,
            self.criar_etapa_previsualizacao
        ]

        self.carregar_etapa()

    def alternar_tema(self):
        self.tema_atual = "claro" if self.tema_atual == "escuro" else "escuro"
        self.carregar_etapa()

    def limpar_tela(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def carregar_etapa(self):
        self.limpar_tela()
        cor = self.temas[self.tema_atual]
        self.main_container.configure(bg=cor["bg_base"])

        # BARRA SUPERIOR (HEADER FIXO)
        top_bar = tk.Frame(self.main_container, bg=cor["bg_base"])
        top_bar.pack(fill="x", padx=30, pady=15)

        title_lbl = tk.Label(top_bar, text="⚡ ImpulseWork", font=("Segoe UI", 16, "bold"), fg=cor["accent"], bg=cor["bg_base"])
        title_lbl.pack(side="left")

        btn_tema = tk.Button(
            top_bar, 
            text=f"Modo {'☀️ Claro' if self.tema_atual == 'escuro' else '🌙 Escuro'}", 
            command=self.alternar_tema,
            font=("Segoe UI", 9, "bold"),
            bg=cor["bg_card"], 
            fg=cor["text_primary"],
            bd=1, relief="solid", padx=12, pady=5, cursor="hand2"
        )
        btn_tema.pack(side="right")

        # BARRA DE PROGRESSO
        if self.etapa_atual > 0:
            progress_frame = tk.Frame(self.main_container, bg=cor["bg_base"])
            progress_frame.pack(pady=5)
            
            passos = ["1. Pessoais", "2. Contato", "3. Perfil", "4. Resumo", "5. Confirmação"]
            for idx, passo in enumerate(passos, 1):
                is_active = (idx == self.etapa_atual)
                is_done = (idx < self.etapa_atual)
                
                fg_col = cor["accent"] if (is_active or is_done) else cor["text_secondary"]
                font_style = ("Segoe UI", 9, "bold" if is_active else "normal")
                
                lbl_passo = tk.Label(progress_frame, text=f"{passo} {'✓' if is_done else ''}  ", font=font_style, fg=fg_col, bg=cor["bg_base"])
                lbl_passo.pack(side="left", padx=4)

        # PAINEL CENTRAL
        self.card_container = tk.Frame(self.main_container, bg=cor["bg_card"], padx=30, pady=25, highlightbackground=cor["border"], highlightthickness=1)
        self.card_container.pack(pady=15, padx=50, fill="both", expand=True)

        self.etapas[self.etapa_atual]()

    # --- TELA 0: BOAS-VINDAS ---
    def criar_tela_boas_vindas(self):
        cor = self.temas[self.tema_atual]

        lbl = tk.Label(self.card_container, text="Impulsione o seu futuro profissional 🚀", font=("Segoe UI", 18, "bold"), bg=cor["bg_card"], fg=cor["text_primary"])
        lbl.pack(pady=(10, 5))

        sub_lbl = tk.Label(self.card_container, text="Crie o seu perfil de alto impacto e envie para as melhores empresas em minutos.", font=("Segoe UI", 10), bg=cor["bg_card"], fg=cor["text_secondary"])
        sub_lbl.pack(pady=(0, 20))

        info_txt = "O ImpulseWork simplifica a criação e distribuição do seu currículo.\nPreencha as informações divididas por passos rápidos e simples."
        lbl_info = tk.Label(self.card_container, text=info_txt, font=("Segoe UI", 10), bg=cor["bg_card"], fg=cor["text_primary"], justify="center")
        lbl_info.pack(pady=15)

        btn_sobre = tk.Button(self.card_container, text="ℹ️ Sobre o App / Mais Informações", command=self.abrir_tela_sobre, bg=cor["entry_bg"], fg=cor["text_primary"], bd=1, relief="solid", padx=15, pady=8, cursor="hand2")
        btn_sobre.pack(pady=10)

        btn_iniciar = tk.Button(self.card_container, text="Começar Agora ➔", command=self.proxima_etapa, font=("Segoe UI", 11, "bold"), bg=cor["accent"], fg="#FFFFFF", bd=0, padx=25, pady=10, cursor="hand2")
        btn_iniciar.pack(pady=20)

    # --- TELA EXCLUSIVA DE INFORMAÇÕES/SOBRE ---
    def abrir_tela_sobre(self):
        self.limpar_tela()
        cor = self.temas[self.tema_atual]
        self.main_container.configure(bg=cor["bg_base"])

        card = tk.Frame(self.main_container, bg=cor["bg_card"], padx=30, pady=30, highlightbackground=cor["border"], highlightthickness=1)
        card.pack(pady=40, padx=50, fill="both", expand=True)

        tk.Label(card, text="Sobre o ImpulseWork", font=("Segoe UI", 18, "bold"), bg=cor["bg_card"], fg=cor["text_primary"]).pack(anchor="w", pady=(0, 15))

        texto = (
            "O ImpulseWork é uma plataforma desenvolvida para conectar talentos diretamente "
            "com oportunidades de trabalho em todo o país.\n\n"
            "Como funciona:\n"
            "1. Você preenche seus dados estruturados por etapas.\n"
            "2. Nosso sistema valida as informações e gera um currículo otimizado.\n"
            "3. Você revisa a pré-visualização completa antes do envio.\n"
            "4. O perfil é distribuído automaticamente para bases de parceiros e recrutadores.\n\n"
            "Segurança de Dados:\n"
            "Todas as informações fornecidas são protegidas e usadas unicamente para o propósito "
            "de candidatura profissional."
        )

        lbl_texto = tk.Label(card, text=texto, font=("Segoe UI", 10), bg=cor["bg_card"], fg=cor["text_primary"], justify="left", wraplength=700)
        lbl_texto.pack(anchor="w", pady=10)

        btn_voltar = tk.Button(card, text="← Voltar ao Início", command=self.carregar_etapa, bg=cor["accent"], fg="#FFFFFF", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=8, cursor="hand2")
        btn_voltar.pack(anchor="w", pady=20)

    # --- ETAPA 1: DADOS PESSOAIS ---
    def criar_etapa_dados_pessoais(self):
        cor = self.temas[self.tema_atual]

        tk.Label(self.card_container, text="1. Dados Pessoais", font=("Segoe UI", 14, "bold"), bg=cor["bg_card"], fg=cor["text_primary"]).pack(anchor="w", pady=(0, 15))

        tk.Label(self.card_container, text="Nome Completo:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_nome = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_nome.pack(fill="x", pady=(2, 12), ipady=5)
        ent_nome.insert(0, self.dados_usuario.get("nome", ""))

        tk.Label(self.card_container, text="Data de Nascimento (somente números):*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_nasc = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_nasc.pack(fill="x", pady=(2, 12), ipady=5)
        ent_nasc.insert(0, self.dados_usuario.get("nascimento", ""))

        def salvar_e_avancar():
            if not ent_nome.get().strip() or not ent_nasc.get().strip():
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios antes de continuar.")
                return
            self.dados_usuario["nome"] = ent_nome.get().strip()
            self.dados_usuario["nascimento"] = ent_nasc.get().strip()
            self.proxima_etapa()

        self.criar_botoes_navegacao(salvar_e_avancar)

    # --- ETAPA 2: CONTATO E ENDEREÇO ---
    def criar_etapa_contato_endereco(self):
        cor = self.temas[self.tema_atual]

        tk.Label(self.card_container, text="2. Contato e Endereço", font=("Segoe UI", 14, "bold"), bg=cor["bg_card"], fg=cor["text_primary"]).pack(anchor="w", pady=(0, 15))

        tk.Label(self.card_container, text="E-mail de Contato:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_email = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_email.pack(fill="x", pady=(2, 10), ipady=5)
        ent_email.insert(0, self.dados_usuario.get("email", ""))

        tk.Label(self.card_container, text="Telefone / WhatsApp:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_tel = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_tel.pack(fill="x", pady=(2, 10), ipady=5)
        ent_tel.insert(0, self.dados_usuario.get("telefone", ""))

        tk.Label(self.card_container, text="Logradouro / Rua:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_rua = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_rua.pack(fill="x", pady=(2, 10), ipady=5)
        ent_rua.insert(0, self.dados_usuario.get("rua", ""))

        def salvar_e_avancar():
            if not ent_email.get().strip() or not ent_tel.get().strip() or not ent_rua.get().strip():
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios antes de continuar.")
                return
            self.dados_usuario["email"] = ent_email.get().strip()
            self.dados_usuario["telefone"] = ent_tel.get().strip()
            self.dados_usuario["rua"] = ent_rua.get().strip()
            self.proxima_etapa()

        self.criar_botoes_navegacao(salvar_e_avancar)

    # --- ETAPA 3: PERFIL PROFISSIONAL ---
    def criar_etapa_perfil_profissional(self):
        cor = self.temas[self.tema_atual]

        tk.Label(self.card_container, text="3. Perfil Profissional", font=("Segoe UI", 14, "bold"), bg=cor["bg_card"], fg=cor["text_primary"]).pack(anchor="w", pady=(0, 15))

        tk.Label(self.card_container, text="Área de Interesse:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_area = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_area.pack(fill="x", pady=(2, 10), ipady=5)
        ent_area.insert(0, self.dados_usuario.get("area", ""))

        tk.Label(self.card_container, text="Cargo Pretendido:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        ent_cargo = tk.Entry(self.card_container, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        ent_cargo.pack(fill="x", pady=(2, 10), ipady=5)
        ent_cargo.insert(0, self.dados_usuario.get("cargo", ""))

        def salvar_e_avancar():
            if not ent_area.get().strip() or not ent_cargo.get().strip():
                messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios antes de continuar.")
                return
            self.dados_usuario["area"] = ent_area.get().strip()
            self.dados_usuario["cargo"] = ent_cargo.get().strip()
            self.proxima_etapa()

        self.criar_botoes_navegacao(salvar_e_avancar)

    # --- ETAPA 4: OBJETIVO E RESUMO ---
    def criar_etapa_objetivo_resumo(self):
        cor = self.temas[self.tema_atual]

        tk.Label(self.card_container, text="4. Objetivo e Resumo", font=("Segoe UI", 14, "bold"), bg=cor["bg_card"], fg=cor["text_primary"]).pack(anchor="w", pady=(0, 15))

        tk.Label(self.card_container, text="Resumo Profissional / Objetivos:*", bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w")
        txt_resumo = tk.Text(self.card_container, height=5, bg=cor["entry_bg"], fg=cor["entry_fg"], insertbackground=cor["entry_fg"], bd=1, relief="solid")
        txt_resumo.pack(fill="x", pady=(2, 15))
        txt_resumo.insert("1.0", self.dados_usuario.get("resumo", ""))

        def salvar_e_avancar():
            resumo_texto = txt_resumo.get("1.0", tk.END).strip()
            if not resumo_texto:
                messagebox.showwarning("Atenção", "Por favor, digite o seu resumo profissional antes de avançar.")
                return
            self.dados_usuario["resumo"] = resumo_texto
            self.proxima_etapa()

        self.criar_botoes_navegacao(salvar_e_avancar)

    # --- ETAPA 5: PRÉ-VISUALIZAÇÃO E CONFIRMAÇÃO DO CURRÍCULO ---
    def criar_etapa_previsualizacao(self):
        cor = self.temas[self.tema_atual]

        tk.Label(self.card_container, text="📄 Confirmação do Currículo", font=("Segoe UI", 14, "bold"), bg=cor["bg_card"], fg=cor["text_primary"]).pack(anchor="w", pady=(0, 5))
        tk.Label(self.card_container, text="Revise como o seu perfil será enviado às empresas:", font=("Segoe UI", 9), bg=cor["bg_card"], fg=cor["text_secondary"]).pack(anchor="w", pady=(0, 15))

        # Quadro imitando a folha de currículo
        preview_box = tk.Frame(self.card_container, bg=cor["entry_bg"], bd=1, relief="solid", padx=20, pady=15)
        preview_box.pack(fill="both", expand=True, pady=5)

        nome = self.dados_usuario.get('nome', 'N/A')
        cargo = self.dados_usuario.get('cargo', 'N/A')
        area = self.dados_usuario.get('area', 'N/A')
        email = self.dados_usuario.get('email', 'N/A')
        tel = self.dados_usuario.get('telefone', 'N/A')
        rua = self.dados_usuario.get('rua', 'N/A')
        nasc = self.dados_usuario.get('nascimento', 'N/A')
        resumo = self.dados_usuario.get('resumo', 'N/A')

        tk.Label(preview_box, text=nome.upper(), font=("Segoe UI", 13, "bold"), bg=cor["entry_bg"], fg=cor["text_primary"]).pack(anchor="w")
        tk.Label(preview_box, text=f"{cargo} | Área: {area}", font=("Segoe UI", 10, "bold"), bg=cor["entry_bg"], fg=cor["accent"]).pack(anchor="w", pady=(0, 10))

        contato_txt = f"📧 {email}  |  📱 {tel}  |  📍 {rua}  |  🎂 Nasc: {nasc}"
        tk.Label(preview_box, text=contato_txt, font=("Segoe UI", 9), bg=cor["entry_bg"], fg=cor["text_secondary"]).pack(anchor="w", pady=(0, 10))

        tk.Label(preview_box, text="RESUMO PROFISSIONAL", font=("Segoe UI", 9, "bold"), bg=cor["entry_bg"], fg=cor["text_primary"]).pack(anchor="w", pady=(5, 2))
        tk.Label(preview_box, text=resumo, font=("Segoe UI", 9), bg=cor["entry_bg"], fg=cor["text_primary"], justify="left", wraplength=600).pack(anchor="w")

        def finalizar_envio():
            messagebox.showinfo("Sucesso!", "Currículo confirmado e enviado com sucesso! O ImpulseWork iniciou o disparo para as empresas.")

        btn_frame = tk.Frame(self.card_container, bg=cor["bg_card"])
        btn_frame.pack(fill="x", pady=(15, 0))

        btn_voltar = tk.Button(btn_frame, text="← Editar Dados", command=self.etapa_anterior, bg=cor["entry_bg"], fg=cor["text_primary"], bd=1, relief="solid", padx=15, pady=8, cursor="hand2")
        btn_voltar.pack(side="left")
        
        btn_confirmar = tk.Button(btn_frame, text="🚀 Confirmar e Enviar Currículo", command=finalizar_envio, bg="#10B981", fg="#FFFFFF", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
        btn_confirmar.pack(side="right")

    # --- BOTÕES DE NAVEGAÇÃO ---
    def criar_botoes_navegacao(self, acao_proximo):
        cor = self.temas[self.tema_atual]
        btn_frame = tk.Frame(self.card_container, bg=cor["bg_card"])
        btn_frame.pack(fill="x", pady=(20, 0))

        if self.etapa_atual > 0:
            btn_voltar = tk.Button(btn_frame, text="← Voltar", command=self.etapa_anterior, bg=cor["entry_bg"], fg=cor["text_primary"], bd=1, relief="solid", padx=15, pady=8, cursor="hand2")
            btn_voltar.pack(side="left")

        btn_continuar = tk.Button(btn_frame, text="Continuar ➔", command=acao_proximo, bg=cor["accent"], fg="#FFFFFF", font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=10, cursor="hand2")
        btn_continuar.pack(side="right")

    def proxima_etapa(self):
        if self.etapa_atual < len(self.etapas) - 1:
            self.etapa_atual += 1
            self.carregar_etapa()

    def etapa_anterior(self):
        if self.etapa_atual > 0:
            self.etapa_atual -= 1
            self.carregar_etapa()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImpulseWorkApp(root)
    root.mainloop()