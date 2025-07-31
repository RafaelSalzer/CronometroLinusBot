from kivy.clock import Clock
import time

class Cronometro:
    def __init__(self):
        self.tempo_inicial = 0
        self.tempo_pausado = 0
        self.rodando = False
        self.evento = None
    
    def iniciar(self):
        if not self.rodando:
            self.rodando = True
            if self.tempo_pausado == 0:
                # Primeira vez iniciando
                self.tempo_inicial = time.time()
            else:
                # Retomando após pausa - ajusta o tempo inicial
                self.tempo_inicial = time.time() - self.tempo_pausado
            # Atualiza a cada 10ms para suavidade visual
            self.evento = Clock.schedule_interval(self.atualizar, 0.01)
    
    def pausar_cronometro(self):
        if self.rodando and self.evento:
            self.rodando = False
            self.evento.cancel()
            self.evento = None
            # Salva o tempo decorrido até agora
            self.tempo_pausado = time.time() - self.tempo_inicial
    
    def zerar_cronometro(self):
        self.pausar_cronometro()
        self.tempo_inicial = 0
        self.tempo_pausado = 0
        #print("zerei aqui")
    
    def obter_tempo_atual(self):
        """Retorna o tempo atual em segundos"""
        if self.rodando:
            return time.time() - self.tempo_inicial
        else:
            return self.tempo_pausado
    
    def atualizar(self, dt):
        # Este método é chamado apenas para atualizar a interface
        # O tempo real é calculado em obter_tempo_atual()
        pass
    
    def obter_tempo_formatado(self):
        """Retorna o tempo no formato MM:SS.mmm"""
        tempo_total = self.obter_tempo_atual()
        
        # Converte para minutos, segundos e milissegundos
        minutos = int(tempo_total // 60)
        segundos = int(tempo_total % 60)
        milissegundos = int((tempo_total % 1) * 1000)
        
        return f"{minutos:02d}:{segundos:02d}.{milissegundos:03d}"