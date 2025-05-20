import pyttsx3
import datetime
import speech_recognition as sr
import pause
import pyautogui as pa
import time
import pyperclip
import webbrowser
import os
import subprocess
import requests
import json
import random 
from personalidade import PersonalidadeJarvis
from typing import Optional, Dict, Callable, List


class Configuracoes:
    VELOCIDADE_FALA = 195
    VOZ_FALA = 0  
    LIMIAR_PAUSA = 1
    PALAVRA_ATIVACAO = 'jarvis'  


class TextoParaFala:
    def __init__(self):
        self.motor = pyttsx3.init()
        self.motor.setProperty("rate", 180)  
        self.motor.setProperty("volume", 0.9)
        
        try:
            voices = self.motor.getProperty('voices')
            self.motor.setProperty('voice', voices[2].id)  
        except:
            pass

    def falar(self, texto):
        print(f"Jarvis: {texto}")  # Exibe no terminal também
        self.motor.say(texto)
        self.motor.runAndWait()



class ReconhecedorDeVoz:
    def __init__(self):
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor.pause_threshold = Configuracoes.LIMIAR_PAUSA
    
    def ouvir(self) -> Optional[str]:
        with sr.Microphone() as fonte:
            print("Aguardando seu comando...")
            try:
                audio = self.reconhecedor.listen(fonte)
                print("Processando áudio...")
                texto = self.reconhecedor.recognize_google(audio, language='pt-BR')
                print(f"Comando reconhecido: {texto}")
                return texto.lower()
            except sr.UnknownValueError:
                print("Não foi possível entender o áudio")
                return None
            except sr.RequestError as erro:
                print(f"Erro no serviço de reconhecimento: {erro}")
                return None


class GerenciadorDeComandos:
    def __init__(self, sistema_fala: TextoParaFala, reconhecedor: ReconhecedorDeVoz):
        self.sistema_fala = sistema_fala
        self.reconhecedor = reconhecedor
        self.comandos = self._registrar_comandos()
    
    def _registrar_comandos(self) -> Dict[str, Callable]:
        return {
            'como você está': self._resposta_status,
            'status do sistema': self._resposta_status,
            'abrir navegador': self._abrir_navegador,
            'abrir youtube': self._abrir_youtube,
            'tocar música': self._reproduzir_musica,
            'que horas são': self._dizer_hora,
            'que dia é hoje': self._dizer_data,
            'pesquisar': self._pesquisar_web,
            'volte': self._retornar_temporizador,
            'obrigado': self._finalizar_assistente,
            'abrir aplicativo': self._abrir_aplicativo,
            'escrever nota': self._criar_nota,
            'ler nota': self._ler_notas,
            'previsão do tempo': self._previsao_tempo,
            'conte uma piada': self._contar_piada,
            'diagnóstico': self._verificar_sistemas
        }
    
    def processar_comando(self, comando: str) -> bool:
        """Processa o comando e retorna False para encerrar"""
        if comando is None:
            return True
        
        if Configuracoes.PALAVRA_ATIVACAO in comando:
            self.sistema_fala.falar("Estou lhe ouvindo!")
            return True
        
        for padrao, funcao in self.comandos.items():
            if padrao in comando:
                return funcao(comando)
        
        self.sistema_fala.falar("Desculpe, não entendi o comando. Pode repetir?")
        return True
    
   
    def _resposta_status(self, comando: str) -> bool:
        self.sistema_fala.falar(PersonalidadeJarvis.confirmacao())
        self.sistema_fala.falar("Status de todos os sistemas: operacionais. Como posso ajudar?")
        return True
    
    def _abrir_navegador(self, comando: str) -> bool:
        self.sistema_fala.falar("Abrindo navegador padrão")
        webbrowser.open('https://www.google.com')
        return True
    
    def _abrir_youtube(self, comando: str) -> bool:
        self.sistema_fala.falar("Acessando YouTube")
        webbrowser.open('https://www.youtube.com')
        return True
    
    def _reproduzir_musica(self, comando: str) -> bool:
        self.sistema_fala.falar("Reproduzindo música selecionada")
        webbrowser.open('https://youtube.com/playlist?list=PL_Q15fKxrBb7wo5SRxHbhk6ZL6zMYh5tH&si=xTC5mwP8jrNdftsh')
        return True
    
    def _dizer_hora(self, comando: str) -> bool:
        hora_atual = datetime.datetime.now().strftime("%I:%M")
        self.sistema_fala.falar(f"Horário atual: {hora_atual}")
        return True
    
    def _dizer_data(self, comando: str) -> bool:
        meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho",
            "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        agora = datetime.datetime.now()
        self.sistema_fala.falar(f"Hoje é dia {agora.day} de {meses[agora.month - 1]} de {agora.year}")
        return True
    
    def _pesquisar_web(self, comando: str) -> bool:
        termo = comando.replace('pesquisar', '').strip()
        if termo:
            self.sistema_fala.falar(f"Pesquisando: {termo}")
            webbrowser.open(f'https://www.google.com/search?q={termo}')
        else:
            self.sistema_fala.falar("Qual é o termo da pesquisa?")
            termo = self.reconhecedor.ouvir()
            if termo:
                webbrowser.open(f'https://www.google.com/search?q={termo}')
        return True
    
    def _retornar_temporizador(self, comando: str) -> bool:
        self.sistema_fala.falar("Defina o tempo de espera em segundos")
        while True:
            resposta = self.reconhecedor.ouvir()
            if resposta and resposta.isdigit():
                segundos = int(resposta)
                self.sistema_fala.falar(f"Retornando em {segundos} segundos")
                pause.seconds(segundos)
                self.sistema_fala.falar("Estou disponível novamente!")
                break
            else:
                self.sistema_fala.falar("Por favor, informe um número válido")
        return True
    
    def _finalizar_assistente(self, comando: str) -> bool:
        self.sistema_fala.falar(PersonalidadeJarvis.despedida())
        return False
    
    def _abrir_aplicativo(self, comando: str) -> bool:
        self.sistema_fala.falar("Qual aplicativo devo executar?")
        nome_app = self.reconhecedor.ouvir()
        if nome_app:
            try:
                os.startfile(nome_app)
                self.sistema_fala.falar(f"Iniciando {nome_app}")
            except Exception as erro:
                self.sistema_fala.falar(f"Falha ao abrir {nome_app}")
                print(f"Erro técnico: {erro}")
        return True
    
    def _criar_nota(self, comando: str) -> bool:
        self.sistema_fala.falar("Registrando nova anotação")
        nota = self.reconhecedor.ouvir()
        if nota:
            with open("notas.txt", "a") as arquivo:
                arquivo.write(f"{datetime.datetime.now()}: {nota}\n")
            self.sistema_fala.falar("Anotação armazenada com sucesso!")
        return True
    
    def _ler_notas(self, comando: str) -> bool:
        try:
            with open("notas.txt", "r") as arquivo:
                conteudo = arquivo.read()
            if conteudo:
                self.sistema_fala.falar("Anotações registradas:")
                self.sistema_fala.falar(conteudo)
            else:
                self.sistema_fala.falar("Nenhuma anotação encontrada")
        except FileNotFoundError:
            self.sistema_fala.falar("Arquivo de anotações não existe")
        return True
    
    def _previsao_tempo(self, comando: str) -> bool:
        self.sistema_fala.falar("Funcionalidade em desenvolvimento")
        return True
    
    def _contar_piada(self, comando: str) -> bool:
        self.sistema_fala.falar(PersonalidadeJarvis.piada())
        return True
    
    def _verificar_sistemas(self, comando: str) -> bool:
        sistemas = ["Sensores", "Propulsores", "IA", "Armamento", "Energia"]
        status = random.choice(["100% operacional", "95% eficiência", "necessita calibração"])
        self.sistema_fala.falar(f"Diagnóstico completo. {random.choice(sistemas)}: {status}")
        return True


def saudar_usuario() -> str:
    return PersonalidadeJarvis.saudacao()

def executar_assistente():
    sistema_fala = TextoParaFala()
    reconhecedor = ReconhecedorDeVoz()
    gerenciador = GerenciadorDeComandos(sistema_fala, reconhecedor)
    
    sistema_fala.falar(saudar_usuario())
    
    em_execucao = True
    while em_execucao:
        print("Pronto para receber comandos...")
        comando = reconhecedor.ouvir()
        em_execucao = gerenciador.processar_comando(comando)

if __name__ == "__main__":
    executar_assistente()
