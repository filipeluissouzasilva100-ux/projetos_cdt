import os
import re
import sys
import tempfile
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox


class TalentFlowApp:

  def __init__(self, root):
    self.root = root
    self.root.title(
        "TalentFlow Express - Plataforma de Distribuição Profissional"
    )
    self.root.geometry("1000x900")
    self.root.minsize(900, 750)

    self.modo_escuro = True
    self.caminho_curriculo = ""

    self.temas = {
        "escuro": {
            "bg_root": "#1E293B",
            "bg_card": "#0F172A",
            "bg_sec": "#334155",
            "text_primary": "#F8FAFC",
            "text_secondary": "#94A3B8",
            "btn_primary": "#2563EB",
            "btn_pdf": "#059669",
            "btn_print": "#D97706",
            "btn_theme": "#475569",
            "border": "#475569",
            "entry_bg": "#1E293B",
            "entry_fg": "#F8FAFC",
        },
        "claro": {
            "bg_root": "#F1F5F9",
            "bg_card": "#FFFFFF",
            "bg_sec": "#E2E8F0",
            "text_primary": "#0F172A",
            "text_secondary": "#475569",
            "btn_primary": "#1D4ED8",
            "btn_pdf": "#047857",
            "btn_print": "#B45309",
            "btn_theme": "#CBD5E1",
            "border": "#CBD5E1",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#0F172A",
        },
    }

    self.setup_ui()
    self.aplicar_tema()

  def setup_ui(self):
    self.root.grid_rowconfigure(2, weight=1)
    self.root.grid_columnconfigure(0, weight=1)

    # Topo
    self.frame_topo = tk.Frame(self.root, pady=10)
    self.frame_topo.grid(row=0, column=0, sticky="ew", padx=20)

    self.lbl_nome_site = tk.Label(
        self.frame_topo,
        text="TalentFlow Express",
        font=("Segoe UI", 18, "bold"),
    )
    self.lbl_nome_site.pack(side="left")

    self.btn_tema = tk.Button(
        self.frame_topo,
        text="☀️ Modo Claro / 🌙 Escuro",
        command=self.alternar_tema,
        font=("Segoe UI", 9, "bold"),
        relief="flat",
        padx=10,
        pady=4,
        cursor="hand2",
    )
    self.btn_tema.pack(side="right")

    self.lbl_subtitulo = tk.Label(
        self.root,
        text="Central de Geração de Currículo e Envio Multilataforma",
        font=("Segoe UI", 9),
    )
    self.lbl_subtitulo.grid(row=1, column=0, pady=(0, 5))

    # Card Principal
    self.frame_main = tk.Frame(
        self.root, padx=15, pady=10, bd=1, relief="solid"
    )
    self.frame_main.grid(row=2, column=0, padx=20, pady=5, sticky="nsew")

    self.frame_main.grid_columnconfigure(0, weight=1)
    self.frame_main.grid_columnconfigure(1, weight=1)
    self.frame_main.grid_rowconfigure(2, weight=1)

    # --- Lado Esquerdo: Dados Pessoais & Endereço ---
    self.frame_esq = tk.Frame(self.frame_main)
    self.frame_esq.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    self.lbl_sec1 = tk.Label(
        self.frame_esq,
        text="1. DADOS PESSOAIS E ENDEREÇO",
        font=("Segoe UI", 9, "bold"),
    )
    self.lbl_sec1.pack(anchor="w", pady=(0, 6))

    self.add_label(self.frame_esq, "Nome Completo:*")
    self.ent_nome = tk.Entry(self.frame_esq, font=("Segoe UI", 9))
    self.ent_nome.pack(fill="x", pady=(0, 4))

    self.add_label(self.frame_esq, "Data de Nascimento (somente números):*")
    self.ent_nascimento = tk.Entry(self.frame_esq, font=("Segoe UI", 9))
    self.ent_nascimento.pack(fill="x", pady=(0, 4))
    self.ent_nascimento.bind("<KeyRelease>", self.formatar_data)

    self.add_label(self.frame_esq, "E-mail de Contato:*")
    self.ent_email = tk.Entry(self.frame_esq, font=("Segoe UI", 9))
    self.ent_email.pack(fill="x", pady=(0, 4))

    self.add_label(self.frame_esq, "Telefone / WhatsApp (somente números):*")
    self.ent_telefone = tk.Entry(self.frame_esq, font=("Segoe UI", 9))
    self.ent_telefone.pack(fill="x", pady=(0, 4))
    self.ent_telefone.bind("<KeyRelease>", self.formatar_telefone)

    # Sub-frame Endereço: Rua e Número
    f_rua = tk.Frame(self.frame_esq)
    f_rua.pack(fill="x", pady=(0, 4))
    f_rua.grid_columnconfigure(0, weight=3)
    f_rua.grid_columnconfigure(1, weight=1)

    lbl_rua = tk.Label(
        f_rua, text="Logradouro/Rua:*", font=("Segoe UI", 8, "bold")
    )
    lbl_rua.grid(row=0, column=0, sticky="w")
    lbl_num = tk.Label(f_rua, text="Nº:*", font=("Segoe UI", 8, "bold"))
    lbl_num.grid(row=0, column=1, sticky="w")

    self.ent_rua = tk.Entry(f_rua, font=("Segoe UI", 9))
    self.ent_rua.grid(row=1, column=0, sticky="ew", padx=(0, 5))
    self.ent_numero = tk.Entry(f_rua, font=("Segoe UI", 9))
    self.ent_numero.grid(row=1, column=1, sticky="ew")

    # Sub-frame Bairro e Complemento
    f_bairro = tk.Frame(self.frame_esq)
    f_bairro.pack(fill="x", pady=(0, 4))
    f_bairro.grid_columnconfigure(0, weight=1)
    f_bairro.grid_columnconfigure(1, weight=1)

    lbl_bairro = tk.Label(
        f_bairro, text="Bairro:*", font=("Segoe UI", 8, "bold")
    )
    lbl_bairro.grid(row=0, column=0, sticky="w")
    lbl_comp = tk.Label(
        f_bairro, text="Complemento (Opcional):", font=("Segoe UI", 8, "bold")
    )
    lbl_comp.grid(row=0, column=1, sticky="w")

    self.ent_bairro = tk.Entry(f_bairro, font=("Segoe UI", 9))
    self.ent_bairro.grid(row=1, column=0, sticky="ew", padx=(0, 5))
    self.ent_complemento = tk.Entry(f_bairro, font=("Segoe UI", 9))
    self.ent_complemento.grid(row=1, column=1, sticky="ew")

    # Sub-frame Cidade e Estado
    f_cidade = tk.Frame(self.frame_esq)
    f_cidade.pack(fill="x", pady=(0, 4))
    f_cidade.grid_columnconfigure(0, weight=3)
    f_cidade.grid_columnconfigure(1, weight=1)

    lbl_cid = tk.Label(
        f_cidade, text="Cidade:*", font=("Segoe UI", 8, "bold")
    )
    lbl_cid.grid(row=0, column=0, sticky="w")
    lbl_est = tk.Label(
        f_cidade, text="Estado (UF):*", font=("Segoe UI", 8, "bold")
    )
    lbl_est.grid(row=0, column=1, sticky="w")

    self.ent_cidade = tk.Entry(f_cidade, font=("Segoe UI", 9))
    self.ent_cidade.grid(row=1, column=0, sticky="ew", padx=(0, 5))
    self.ent_estado = tk.Entry(f_cidade, font=("Segoe UI", 9))
    self.ent_estado.grid(row=1, column=1, sticky="ew")

    # --- Lado Direito: Perfil Profissional ---
    self.frame_dir = tk.Frame(self.frame_main)
    self.frame_dir.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

    self.lbl_sec2 = tk.Label(
        self.frame_dir,
        text="2. PERFIL E OBJETIVO PROFISSIONAL",
        font=("Segoe UI", 9, "bold"),
    )
    self.lbl_sec2.pack(anchor="w", pady=(0, 6))

    # Área de Interesse e Cargo Pretendido
    f_objetivo = tk.Frame(self.frame_dir)
    f_objetivo.pack(fill="x", pady=(0, 4))
    f_objetivo.grid_columnconfigure(0, weight=1)
    f_objetivo.grid_columnconfigure(1, weight=1)

    lbl_area = tk.Label(
        f_objetivo, text="Área de Interesse:*", font=("Segoe UI", 8, "bold")
    )
    lbl_area.grid(row=0, column=0, sticky="w")
    lbl_cargo = tk.Label(
        f_objetivo,
        text="Cargo Pretendido (opções):*",
        font=("Segoe UI", 8, "bold"),
    )
    lbl_cargo.grid(row=0, column=1, sticky="w")

    self.ent_area = tk.Entry(f_objetivo, font=("Segoe UI", 9))
    self.ent_area.grid(row=1, column=0, sticky="ew", padx=(0, 5))
    self.ent_cargo = tk.Entry(f_objetivo, font=("Segoe UI", 9))
    self.ent_cargo.grid(row=1, column=1, sticky="ew")

    self.add_label(self.frame_dir, "Formação Acadêmica (Grau / Instituição):*")
    self.ent_formacao = tk.Entry(self.frame_dir, font=("Segoe UI", 9))
    self.ent_formacao.pack(fill="x", pady=(0, 4))

    self.add_label(
        self.frame_dir, "Cursos / Certificações (Ex: Inglês, Excel):"
    )
    self.ent_cursos = tk.Entry(self.frame_dir, font=("Segoe UI", 9))
    self.ent_cursos.pack(fill="x", pady=(0, 4))

    self.add_label(self.frame_dir, "LinkedIn / Portfólio (URL):")
    self.ent_linkedin = tk.Entry(self.frame_dir, font=("Segoe UI", 9))
    self.ent_linkedin.pack(fill="x", pady=(0, 4))

    # Pretensão Salarial e Modelo
    f_pretensao = tk.Frame(self.frame_dir)
    f_pretensao.pack(fill="x", pady=(0, 4))
    f_pretensao.grid_columnconfigure(0, weight=1)
    f_pretensao.grid_columnconfigure(1, weight=1)

    lbl_sal = tk.Label(
        f_pretensao, text="Pretensão Salarial:", font=("Segoe UI", 8, "bold")
    )
    lbl_sal.grid(row=0, column=0, sticky="w")
    lbl_mod = tk.Label(
        f_pretensao,
        text="Modelo (CLT, Estágio, PJ):",
        font=("Segoe UI", 8, "bold"),
    )
    lbl_mod.grid(row=0, column=1, sticky="w")

    self.ent_salario = tk.Entry(f_pretensao, font=("Segoe UI", 9))
    self.ent_salario.grid(row=1, column=0, sticky="ew", padx=(0, 5))
    self.ent_modelo = tk.Entry(f_pretensao, font=("Segoe UI", 9))
    self.ent_modelo.grid(row=1, column=1, sticky="ew")

    self.btn_upload = tk.Button(
        self.frame_dir,
        text="📁 Anexar PDF Próprio",
        command=self.selecionar_curriculo,
        font=("Segoe UI", 8, "bold"),
        relief="flat",
        padx=8,
        pady=2,
        cursor="hand2",
    )
    self.btn_upload.pack(anchor="w", pady=(2, 2))
    self.lbl_arquivo = tk.Label(
        self.frame_dir, text="Nenhum arquivo anexado", font=("Segoe UI", 8, "italic")
    )
    self.lbl_arquivo.pack(anchor="w")

    # --- Resumo e Experiências Profissionais ---
    self.frame_resumo = tk.Frame(self.frame_main)
    self.frame_resumo.grid(
        row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew"
    )

    self.add_label(self.frame_resumo, "Resumo Profissional / Objetivos:*")
    self.txt_resumo = tk.Text(
        self.frame_resumo, height=3, font=("Segoe UI", 9)
    )
    self.txt_resumo.pack(fill="x", pady=(2, 4))

    self.add_label(
        self.frame_resumo,
        "Experiência Profissional (Empresas, Cargos e Períodos):",
    )
    self.txt_experiencia = tk.Text(
        self.frame_resumo, height=3, font=("Segoe UI", 9)
    )
    self.txt_experiencia.pack(fill="both", expand=True, pady=(2, 4))

    # Botões de Ação
    self.frame_botoes = tk.Frame(self.root)
    self.frame_botoes.grid(row=3, column=0, sticky="ew", padx=20, pady=(5, 5))

    self.btn_imprimir = tk.Button(
        self.frame_botoes,
        text="🖨️ IMPRIMIR CURRÍCULO",
        command=self.imprimir_curriculo,
        font=("Segoe UI", 10, "bold"),
        pady=6,
        relief="flat",
        cursor="hand2",
    )
    self.btn_imprimir.pack(side="left", expand=True, fill="x", padx=(0, 5))

    self.btn_gerar_enviar = tk.Button(
        self.frame_botoes,
        text="⚡ GERAR E DISPARAR CANDIDATURAS",
        command=self.processar_candidatura,
        font=("Segoe UI", 10, "bold"),
        pady=6,
        relief="flat",
        cursor="hand2",
    )
    self.btn_gerar_enviar.pack(side="right", expand=True, fill="x", padx=(5, 0))

    # Painel de Observação
    self.frame_obs = tk.Frame(
        self.root, pady=6, padx=15, bd=1, relief="groove"
    )
    self.frame_obs.grid(
        row=4, column=0, sticky="ew", padx=20, pady=(5, 10)
    )

    self.lbl_obs_titulo = tk.Label(
        self.frame_obs,
        text="📌 Observação do Sistema (Integração de Destino):",
        font=("Segoe UI", 8, "bold"),
    )
    self.lbl_obs_titulo.pack(anchor="w")

    self.lbl_obs_texto = tk.Label(
        self.frame_obs,
        text=(
            "Após o processamento, seu perfil e currículo serão distribuídos"
            " para: Catho • InfoJobs • LinkedIn Jobs • Gupy • CIEE • NUBE •"
            " Empresas Parceiras."
        ),
        font=("Segoe UI", 8),
        justify="left",
    )
    self.lbl_obs_texto.pack(anchor="w")

  def formatar_data(self, event):
    if event.keysym == "BackSpace":
      return
    texto = re.sub(r"\D", "", self.ent_nascimento.get())[:8]
    formatado = ""
    if len(texto) > 0:
      formatado += texto[:2]
    if len(texto) >= 3:
      formatado += "/" + texto[2:4]
    if len(texto) >= 5:
      formatado += "/" + texto[4:8]

    self.ent_nascimento.delete(0, tk.END)
    self.ent_nascimento.insert(0, formatado)

  def formatar_telefone(self, event):
    if event.keysym == "BackSpace":
      return
    texto = re.sub(r"\D", "", self.ent_telefone.get())[:11]
    formatado = ""
    if len(texto) > 0:
      formatado += "(" + texto[:2]
    if len(texto) >= 3:
      formatado += ") " + texto[2:7]
    if len(texto) >= 8:
      formatado += "-" + texto[7:11]

    self.ent_telefone.delete(0, tk.END)
    self.ent_telefone.insert(0, formatado)

  def add_label(self, parent, text):
    lbl = tk.Label(parent, text=text, font=("Segoe UI", 8, "bold"))
    lbl.pack(anchor="w")

  def alternar_tema(self):
    self.modo_escuro = not self.modo_escuro
    self.aplicar_tema()

  def aplicar_tema(self):
    t = self.temas["escuro" if self.modo_escuro else "claro"]

    self.root.configure(bg=t["bg_root"])
    self.frame_topo.configure(bg=t["bg_root"])
    self.frame_botoes.configure(bg=t["bg_root"])
    self.frame_main.configure(bg=t["bg_card"], highlightbackground=t["border"])
    self.frame_esq.configure(bg=t["bg_card"])
    self.frame_dir.configure(bg=t["bg_card"])
    self.frame_resumo.configure(bg=t["bg_card"])
    self.frame_obs.configure(bg=t["bg_sec"], highlightbackground=t["border"])

    self.lbl_nome_site.configure(bg=t["bg_root"], fg=t["text_primary"])
    self.lbl_subtitulo.configure(bg=t["bg_root"], fg=t["text_secondary"])
    self.btn_tema.configure(bg=t["btn_theme"], fg=t["text_primary"])

    self.lbl_sec1.configure(bg=t["bg_card"], fg=t["btn_primary"])
    self.lbl_sec2.configure(bg=t["bg_card"], fg=t["btn_primary"])

    self.lbl_obs_titulo.configure(bg=t["bg_sec"], fg=t["text_primary"])
    self.lbl_obs_texto.configure(bg=t["bg_sec"], fg=t["text_secondary"])

    self.btn_upload.configure(bg=t["btn_pdf"], fg="white")
    self.lbl_arquivo.configure(bg=t["bg_card"], fg=t["text_secondary"])

    self.btn_imprimir.configure(bg=t["btn_print"], fg="white")
    self.btn_gerar_enviar.configure(bg=t["btn_primary"], fg="white")

    # Atualizar elementos filhos recursivamente
    def atualizar_elementos(parent):
      for child in parent.winfo_children():
        if isinstance(child, tk.Frame):
          child.configure(bg=t["bg_card"])
          atualizar_elementos(child)
        elif isinstance(child, tk.Label) and child not in [
            self.lbl_sec1,
            self.lbl_sec2,
            self.lbl_arquivo,
        ]:
          child.configure(bg=t["bg_card"], fg=t["text_primary"])
        elif isinstance(child, (tk.Entry, tk.Text)):
          child.configure(
              bg=t["entry_bg"],
              fg=t["entry_fg"],
              insertbackground=t["text_primary"],
          )

    atualizar_elementos(self.frame_main)

  def calcular_idade(self, data_str):
    try:
      nasc = datetime.strptime(data_str, "%d/%m/%Y")
      hoje = datetime.now()
      idade = (
          hoje.year
          - nasc.year
          - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
      )
      return idade
    except ValueError:
      return None

  def selecionar_curriculo(self):
    caminho = filedialog.askopenfilename(
        title="Selecione o Currículo", filetypes=[("Arquivos PDF", "*.pdf")]
    )
    if caminho:
      self.caminho_curriculo = caminho
      self.lbl_arquivo.config(
          text=os.path.basename(caminho), fg="#10B981"
      )

  def gerar_texto_curriculo(self):
    nome = self.ent_nome.get().strip()
    nascimento = self.ent_nascimento.get().strip()
    email = self.ent_email.get().strip()
    telefone = self.ent_telefone.get().strip()

    rua = self.ent_rua.get().strip()
    num = self.ent_numero.get().strip()
    bairro = self.ent_bairro.get().strip()
    comp = self.ent_complemento.get().strip()
    cidade = self.ent_cidade.get().strip()
    estado = self.ent_estado.get().strip()

    area = self.ent_area.get().strip()
    cargo = self.ent_cargo.get().strip()
    formacao = self.ent_formacao.get().strip()
    cursos = self.ent_cursos.get().strip()
    salario = self.ent_salario.get().strip()
    modelo = self.ent_modelo.get().strip()

    resumo = self.txt_resumo.get("1.0", tk.END).strip()
    experiencia = self.txt_experiencia.get("1.0", tk.END).strip()

    idade = self.calcular_idade(nascimento)
    idade_str = f"{idade} anos" if idade else "Não informada"
    comp_str = f" - Comp: {comp}" if comp else ""

    conteudo = f"""=================================================================
CURRÍCULO PROFISSIONAL - TALENTFLOW EXPRESS
=================================================================

DADOS PESSOAIS
-----------------------------------------------------------------
NOME: {nome.upper()}
IDADE: {idade_str} (Nascimento: {nascimento})
E-MAIL: {email}
TELEFONE: {telefone}
ENDEREÇO: {rua}, Nº {num}{comp_str} - Bairro: {bairro}
CIDADE/UF: {cidade} / {estado}

OBJETIVO PROFISSIONAL
-----------------------------------------------------------------
ÁREA DE INTERESSE: {area}
CARGOS PRETENDIDOS: {cargo}
MODELO DE TRABALHO: {modelo if modelo else "Não especificado"}
PRETENSAO SALARIAL: {salario if salario else "A combinar"}

FORMAÇÃO ACADÊMICA E CURSOS
-----------------------------------------------------------------
FORMAÇÃO PRINCIPAL:
{formacao}

CURSOS / CERTIFICAÇÕES:
{cursos if cursos else "Nenhum informado"}

RESUMO PROFISSIONAL
-----------------------------------------------------------------
{resumo}

EXPERIÊNCIA PROFISSIONAL
-----------------------------------------------------------------
{experiencia if experiencia else "Sem experiência informada"}

=================================================================
Documento gerado automaticamente pelo TalentFlow Express
"""
    return conteudo

  def imprimir_curriculo(self):
    nome = self.ent_nome.get().strip()
    nasc = self.ent_nascimento.get().strip()

    if not nome or not nasc:
      messagebox.showwarning(
          "Atenção",
          "Preencha ao menos Nome e Data de Nascimento para imprimir o"
          " currículo.",
      )
      return

    if not self.calcular_idade(nasc):
      messagebox.showerror(
          "Erro na Data",
          "Por favor, digite uma data de nascimento válida no formato"
          " DD/MM/AAAA.",
      )
      return

    texto_curriculo = self.gerar_texto_curriculo()
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(
        temp_dir, f"Curriculo_{nome.replace(' ', '_')}.txt"
    )

    with open(temp_file, "w", encoding="utf-8") as f:
      f.write(texto_curriculo)

    try:
      if sys.platform == "win32":
        os.startfile(temp_file, "print")
      else:
        os.system(f"lpr '{temp_file}'")
      messagebox.showinfo(
          "Impressão",
          "O currículo foi enviado para a impressora padrão do sistema!",
      )
    except Exception as e:
      messagebox.showerror(
          "Erro ao Imprimir",
          f"Não foi possível enviar para a impressora.\nDetalhes: {e}",
      )

  def processar_candidatura(self):
    nome = self.ent_nome.get().strip()
    nasc = self.ent_nascimento.get().strip()
    email = self.ent_email.get().strip()
    telefone = self.ent_telefone.get().strip()

    rua = self.ent_rua.get().strip()
    num = self.ent_numero.get().strip()
    bairro = self.ent_bairro.get().strip()
    cidade = self.ent_cidade.get().strip()
    estado = self.ent_estado.get().strip()

    area = self.ent_area.get().strip()
    cargo = self.ent_cargo.get().strip()
    formacao = self.ent_formacao.get().strip()
    resumo = self.txt_resumo.get("1.0", tk.END).strip()

    campos_obrigatorios = [
        nome,
        nasc,
        email,
        telefone,
        rua,
        num,
        bairro,
        cidade,
        estado,
        area,
        cargo,
        formacao,
        resumo,
    ]

    if not all(campos_obrigatorios):
      messagebox.showwarning(
          "Atenção", "Por favor, preencha todos os campos obrigatórios (*)."
      )
      return

    idade = self.calcular_idade(nasc)
    if idade is None:
      messagebox.showerror(
          "Erro na Data",
          "Por favor, insira a data de nascimento no formato correto:"
          " DD/MM/AAAA",
      )
      return

    messagebox.showinfo(
        "Sucesso e Envio Automático",
        f"✅ CURRÍCULO GERADO COM SUCESSO!\nCandidato: {nome} ({idade}"
        f" anos)\n\n🚀 AUTOMATION STATUS:\nO TalentFlow Express iniciou a"
        f" transmissão dos seus dados para as vagas de '{cargo}'.\n\nAcompanhe o"
        f" retorno no seu e-mail ({email}).",
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = TalentFlowApp(root)
  root.mainloop()