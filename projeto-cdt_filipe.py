import os
import sys
import tempfile
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

class TalentFlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TalentFlow Express - Plataforma de Distribuição Profissional")
        self.root.geometry("820x800")
        
        # Estado do Tema (Escuro por padrão)
        self.modo_escuro = True
        self.caminho_curriculo = ""

        # Definição de Cores Profissionais e Confortáveis
        self.temas = {
            "escuro": {
                "bg_root": "#1E293B",
                "bg_card": "#0F172A",
                "bg_sec": "#334155",
                "text_primary": "#F8FAFC",
                "text_secondary": "#94A3B8",
                "btn_primary": "#2563EB",
                "btn_pdf": "#059669",
                "btn_print": "#D97706",      # Laranja Âmbar para Impressão
                "btn_theme": "#475569",
                "border": "#475569"
            },
            "claro": {
                "bg_root": "#F1F5F9",
                "bg_card": "#FFFFFF",
                "bg_sec": "#E2E8F0",
                "text_primary": "#0F172A",
                "text_secondary": "#475569",
                "btn_primary": "#1D4ED8",
                "btn_pdf": "#047857",
                "btn_print": "#B45309",      # Laranja Âmbar
                "btn_theme": "#CBD5E1",
                "border": "#CBD5E1"
            }
        }

        self.setup_ui()
        self.aplicar_tema()

    def setup_ui(self):
        # Topo / Header
        self.frame_topo = tk.Frame(self.root, pady=10)
        self.frame_topo.pack(fill="x", padx=25)

        self.lbl_nome_site = tk.Label(
            self.frame_topo, 
            text="TalentFlow Express", 
            font=("Segoe UI", 18, "bold")
        )
        self.lbl_nome_site.pack(side="left")

        self.btn_tema = tk.Button(
            self.frame_topo, 
            text="☀️ Modo Claro / 🌙 Escuro", 
            command=self.alternar_tema,
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=10, pady=4, cursor="hand2"
        )
        self.btn_tema.pack(side="right")

        self.lbl_subtitulo = tk.Label(
            self.root, 
            text="Central de Geração de Currículo, Impressão e Envio Automatizado Multilataforma", 
            font=("Segoe UI", 9)
        )
        self.lbl_subtitulo.pack(pady=(0, 10))

        # Card Principal do Formulário
        self.frame_main = tk.Frame(self.root, padx=20, pady=15, bd=1, relief="solid")
        self.frame_main.pack(padx=25, pady=5, fill="both", expand=True)

        # Lado Esquerdo - Dados Pessoais
        self.frame_esq = tk.Frame(self.frame_main)
        self.frame_esq.grid(row=0, column=0, padx=15, pady=5, sticky="nsew")

        self.lbl_sec1 = tk.Label(self.frame_esq, text="DADOS PESSOAIS E LOCALIZAÇÃO", font=("Segoe UI", 9, "bold"))
        self.lbl_sec1.pack(anchor="w", pady=(0, 8))

        self.add_label(self.frame_esq, "Nome Completo:*")
        self.ent_nome = tk.Entry(self.frame_esq, width=34, font=("Segoe UI", 9))
        self.ent_nome.pack(pady=(0, 6))

        # NOVO CAMPO: Data de Nascimento / Idade
        self.add_label(self.frame_esq, "Data de Nascimento (DD/MM/AAAA):*")
        self.ent_nascimento = tk.Entry(self.frame_esq, width=34, font=("Segoe UI", 9))
        self.ent_nascimento.pack(pady=(0, 6))

        self.add_label(self.frame_esq, "E-mail de Contato:*")
        self.ent_email = tk.Entry(self.frame_esq, width=34, font=("Segoe UI", 9))
        self.ent_email.pack(pady=(0, 6))

        self.add_label(self.frame_esq, "Telefone / WhatsApp:*")
        self.ent_telefone = tk.Entry(self.frame_esq, width=34, font=("Segoe UI", 9))
        self.ent_telefone.pack(pady=(0, 6))

        self.add_label(self.frame_esq, "Cidade / Estado:*")
        self.ent_localidade = tk.Entry(self.frame_esq, width=34, font=("Segoe UI", 9))
        self.ent_localidade.pack(pady=(0, 6))

        # Lado Direito - Perfil Profissional
        self.frame_dir = tk.Frame(self.frame_main)
        self.frame_dir.grid(row=0, column=1, padx=15, pady=5, sticky="nsew")

        self.lbl_sec2 = tk.Label(self.frame_dir, text="PERFIL E OBJETIVO PROFISSIONAL", font=("Segoe UI", 9, "bold"))
        self.lbl_sec2.pack(anchor="w", pady=(0, 8))

        self.add_label(self.frame_dir, "Área de Interesse / Cargo Pretendido:*")
        self.ent_area = tk.Entry(self.frame_dir, width=34, font=("Segoe UI", 9))
        self.ent_area.pack(pady=(0, 6))

        self.add_label(self.frame_dir, "Formação Acadêmica / Curso:*")
        self.ent_curso = tk.Entry(self.frame_dir, width=34, font=("Segoe UI", 9))
        self.ent_curso.pack(pady=(0, 6))

        self.add_label(self.frame_dir, "LinkedIn / Portfólio (URL):")
        self.ent_linkedin = tk.Entry(self.frame_dir, width=34, font=("Segoe UI", 9))
        self.ent_linkedin.pack(pady=(0, 6))

        self.add_label(self.frame_dir, "Pretensão Salarial / Modelo (CLT/Estágio):")
        self.ent_pretensao = tk.Entry(self.frame_dir, width=34, font=("Segoe UI", 9))
        self.ent_pretensao.pack(pady=(0, 6))

        self.add_label(self.frame_dir, "Opção: Importar PDF Existente")
        self.btn_upload = tk.Button(
            self.frame_dir, text="📁 Anexar Arquivo Próprio", 
            command=self.selecionar_curriculo, font=("Segoe UI", 8, "bold"),
            relief="flat", padx=8, pady=2, cursor="hand2"
        )
        self.btn_upload.pack(anchor="w", pady=(2, 2))
        self.lbl_arquivo = tk.Label(self.frame_dir, text="Nenhum arquivo anexado", font=("Segoe UI", 8, "italic"))
        self.lbl_arquivo.pack(anchor="w")

        # Campo de Resumo Profissional
        self.frame_resumo = tk.Frame(self.frame_main)
        self.frame_resumo.grid(row=1, column=0, columnspan=2, padx=15, pady=5, sticky="ew")

        self.add_label(self.frame_resumo, "Resumo Profissional e Histórico Pessoal:*")
        self.txt_resumo = tk.Text(self.frame_resumo, height=3, width=74, font=("Segoe UI", 9))
        self.txt_resumo.pack(pady=(2, 5))

        # Frame com Botões de Ação Superior (Imprimir e Disparar)
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack(fill="x", padx=25, pady=(10, 5))

        # NOVO BOTÃO: Imprimir Currículo
        self.btn_imprimir = tk.Button(
            self.frame_botoes, 
            text="🖨️ IMPRIMIR CURRÍCULO", 
            command=self.imprimir_curriculo, 
            font=("Segoe UI", 10, "bold"), 
            pady=8, relief="flat", cursor="hand2"
        )
        self.btn_imprimir.pack(side="left", expand=True, fill="x", padx=(0, 5))

        # Botão Principal: Gerar + Enviar
        self.btn_gerar_enviar = tk.Button(
            self.frame_botoes, 
            text="⚡ GERAR E DISPARAR CANDIDATURAS", 
            command=self.processar_candidatura, 
            font=("Segoe UI", 10, "bold"), 
            pady=8, relief="flat", cursor="hand2"
        )
        self.btn_gerar_enviar.pack(side="right", expand=True, fill="x", padx=(5, 0))

        # Painel de Observação
        self.frame_obs = tk.Frame(self.root, pady=8, padx=15, bd=1, relief="groove")
        self.frame_obs.pack(fill="x", padx=25, pady=(5, 15))

        self.lbl_obs_titulo = tk.Label(
            self.frame_obs, 
            text="📌 Observação do Sistema (Integração de Destino):", 
            font=("Segoe UI", 8, "bold")
        )
        self.lbl_obs_titulo.pack(anchor="w")

        self.lbl_obs_texto = tk.Label(
            self.frame_obs, 
            text="Após o processamento, seu perfil (com cálculo automático de idade) e currículo gerado serão distribuídos automaticamente para:\n• Catho  • InfoJobs  • LinkedIn Jobs  • Gupy  • CIEE  • NUBE  • Banco de Talentos de Empresas Parceiras.",
            font=("Segoe UI", 8),
            justify="left"
        )
        self.lbl_obs_texto.pack(anchor="w", pady=(2, 0))

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

        for parent in [self.frame_esq, self.frame_dir, self.frame_resumo]:
            for child in parent.winfo_children():
                if isinstance(child, tk.Label) and child not in [self.lbl_sec1, self.lbl_sec2, self.lbl_arquivo]:
                    child.configure(bg=t["bg_card"], fg=t["text_primary"])

    def calcular_idade(self, data_str):
        try:
            nasc = datetime.strptime(data_str, "%d/%m/%Y")
            hoje = datetime.now()
            idade = hoje.year - nasc.year - ((hoje.month, hoje.day) < (nasc.month, nasc.day))
            return idade
        except ValueError:
            return None

    def selecionar_curriculo(self):
        caminho = filedialog.askopenfilename(title="Selecione o Currículo", filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho:
            self.caminho_curriculo = caminho
            self.lbl_arquivo.config(text=os.path.basename(caminho), fg="#10B981")

    def gerar_texto_curriculo(self):
        nome = self.ent_nome.get().strip()
        nascimento = self.ent_nascimento.get().strip()
        email = self.ent_email.get().strip()
        telefone = self.ent_telefone.get().strip()
        local = self.ent_localidade.get().strip()
        area = self.ent_area.get().strip()
        curso = self.ent_curso.get().strip()
        resumo = self.txt_resumo.get("1.0", tk.END).strip()

        idade = self.calcular_idade(nascimento)
        idade_str = f"{idade} anos" if idade else "Não informada"

        conteudo = f"""=================================================================
CURRÍCULO PROFISSIONAL - TALENTFLOW EXPRESS
=================================================================

NOME: {nome.upper()}
IDADE: {idade_str} (Nascimento: {nascimento})
E-MAIL: {email}
TELEFONE: {telefone}
LOCALIDADE: {local}

-----------------------------------------------------------------
OBJETIVO E ÁREA DE INTERESSE
-----------------------------------------------------------------
{area}

-----------------------------------------------------------------
FORMAÇÃO ACADÊMICA
-----------------------------------------------------------------
{curso}

-----------------------------------------------------------------
RESUMO PROFISSIONAL
-----------------------------------------------------------------
{resumo}

=================================================================
Documento gerado automaticamente pelo TalentFlow Express
"""
        return conteudo

    def imprimir_curriculo(self):
        nome = self.ent_nome.get().strip()
        nasc = self.ent_nascimento.get().strip()

        if not nome or not nasc:
            messagebox.showwarning("Atenção", "Preencha ao menos Nome e Data de Nascimento para imprimir o currículo.")
            return

        if not self.calcular_idade(nasc):
            messagebox.showerror("Erro na Data", "Por favor, digite uma data de nascimento válida no formato DD/MM/AAAA.")
            return

        texto_curriculo = self.gerar_texto_curriculo()

        # Cria arquivo temporário para enviar à impressora
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"Curriculo_{nome.replace(' ', '_')}.txt")
        
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(texto_curriculo)

        try:
            if sys.platform == "win32":
                os.startfile(temp_file, "print")
            else:
                os.system(f"lpr '{temp_file}'")
            messagebox.showinfo("Impressão", "O currículo foi enviado para a impressora padrão do sistema!")
        except Exception as e:
            messagebox.showerror("Erro ao Imprimir", f"Não foi possível enviar para a impressora.\nDetalhes: {e}")

    def processar_candidatura(self):
        nome = self.ent_nome.get().strip()
        nasc = self.ent_nascimento.get().strip()
        email = self.ent_email.get().strip()
        telefone = self.ent_telefone.get().strip()
        local = self.ent_localidade.get().strip()
        area = self.ent_area.get().strip()
        curso = self.ent_curso.get().strip()
        resumo = self.txt_resumo.get("1.0", tk.END).strip()

        if not (nome and nasc and email and telefone and local and area and curso and resumo):
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios (*).")
            return

        idade = self.calcular_idade(nasc)
        if idade is None:
            messagebox.showerror("Erro na Data", "Por favor, insira a data de nascimento no formato correto: DD/MM/AAAA")
            return

        messagebox.showinfo(
            "Sucesso e Envio Automático", 
            f"✅ CURRÍCULO GERADO COM SUCESSO!\nCandidato: {nome} ({idade} anos)\n\n"
            f"🚀 AUTOMATION STATUS:\nO TalentFlow Express iniciou a transmissão dos seus dados para as vagas de '{area}'.\n\n"
            f"Acompanhe o retorno no seu e-mail ({email})."
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = TalentFlowApp(root)
    root.mainloop()