import random
import datetime

class PersonalidadeJarvis:
    @staticmethod
    def saudacao() -> str:
        hora = datetime.datetime.now().hour
        if 5 <= hora < 12:
            return "Bom dia, senhor. Sistemas operacionais funcionando normalmente."
        elif 12 <= hora < 18:
            return "Boa tarde. Todos os protocolos de segurança estão ativos."
        else:
            return "Boa noite. O traje está pronto para uso quando precisar."

    @staticmethod
    def confirmacao() -> str:
        frases = [
            "Como desejar, senhor.",
            "Processando... concluído.",
            "Imediatamente, senhor.",
            "Executando sua ordem."
        ]
        return random.choice(frases)

    @staticmethod
    def erro() -> str:
        frases = [
            "Desculpe, senhor. Parece que encontrei uma dificuldade nessa requisição.",
            "Recomendo verificar esse comando novamente.",
            "Meus protocolos não permitem essa ação no momento."
        ]
        return random.choice(frases)

    @staticmethod
    def despedida() -> str:
        return "Encerrando protocolos. Tenha um excelente dia, senhor."

    @staticmethod
    def piada() -> str:
        piadas = [
            "Por que o Homem de Ferro não usa Windows? Porque ele prefere sistemas 'armor-dáveis'.",
            "Sabia que minha versão 2.0 foi cancelada? Eles disseram que eu era 'demasiado inteligente'."
        ]
        return random.choice(piadas)