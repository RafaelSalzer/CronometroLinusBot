from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.core.window import Window
import threading
from websocket import WebSocketApp
import Equipes
import Cronometro
#Falta: / Armazenar os tempos da equipe selecionada / Resetar tudo no final / Parar o cronometro do tempo total quando chegar em 3  n / Ver um jeito de deixar as
#voltas invisiveis quando não tiver nenhuma volta registrada / 


LabelBase.register(name="Titulo", fn_regular="fonts/Lovelo Black.otf")

class MyWidget(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.equipes = [Equipes.Equipe("Cavaleiros das Trevas", "Preta"), Equipes.Equipe("Droga, é o Brian", "Cinza"),
                        Equipes.Equipe("RUST-EZE", "Vermelha"), Equipes.Equipe("Laranja Mecânica", "Laranja"),
                        Equipes.Equipe("Os Vigaristas", "Roxa"), Equipes.Equipe("S. C. O. O. B. Y", "Verde"), 
                        Equipes.Equipe("Charmbots", "Rosa")]
        self.selecionar = 0
        self.cronometroTempoTotal = Cronometro.Cronometro()
        self.cronometroTempoVolta = Cronometro.Cronometro()
        self.volta = 1
        self.inicio = True
        self.ws = None
        # Inicializar WebSocket após a interface estar pronta
        Clock.schedule_once(self.iniciar_websocket, 0.1)  
        Clock.schedule_once(self.configurar_interface, 0.05)
        self.eventoTextoTempoTotal = None
        self.eventoTextoTempoVolta = None
    
    def configurar_interface(self, dt=None):
        """Configura a interface após estar totalmente carregada"""
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()
    
    def iniciar_websocket(self, dt=None):
        """Inicializa a conexão WebSocket com o ESP32"""
        
        def on_message(ws, message):
            print(f"Mensagem recebida: {message}")
            if message == "Passou" and self.inicio:
                self.inicio = False
                self.cronometroTempoVolta.iniciar()
                self.eventoTextoTempoVolta = Clock.schedule_interval(self.altera_texto_tempo_volta, 0.01)
            elif message == "Passou" and not self.inicio:
            
                if self.volta == 1:
                    self.ids.volta1.text = f"volta {self.volta}: {self.cronometroTempoVolta.obter_tempo_formatado()}"
                    self.volta += 1
                    #self.ids.volta1.opacity = 1
                
                elif self.volta == 2:
                    self.ids.volta2.text = f"volta {self.volta}: {self.cronometroTempoVolta.obter_tempo_formatado()}"
                    self.volta += 1
                    #self.ids.volta2.opacity = 1

                elif self.volta == 3:
                    self.ids.volta3.text = f"volta {self.volta}: {self.cronometroTempoVolta.obter_tempo_formatado()}"
                    self.volta += 1
                    #self.ids.volta3.opacity = 1

                elif self.volta == 4:
                    self.ids.volta4.text = f"volta {self.volta}: {self.cronometroTempoVolta.obter_tempo_formatado()}"
                    self.volta += 1
                    #self.ids.volta4.opacity = 1

                elif self.volta == 5:
                    self.ids.volta5.text = f"volta {self.volta}: {self.cronometroTempoVolta.obter_tempo_formatado()}"
                    self.volta += 1
                    #self.ids.volta5.opacity = 1

                
                # Para o cronômetro da volta
                self.cronometroTempoVolta.zerar_cronometro()
                self.cronometroTempoVolta.iniciar()
                self.eventoTextoTempoVolta = Clock.schedule_interval(self.altera_texto_tempo_volta, 0.01)

        def on_error(ws, error):
            print(f"Erro WebSocket: {error}")

        def on_close(ws, close_status_code, close_msg):
            print("Conexão WebSocket encerrada")

        def on_open(ws):
            print("Conectado ao WebSocket do ESP32")
            
        try:
            ws_url = "ws://192.168.4.1:81"
            self.ws = WebSocketApp(ws_url,
                                   on_message=on_message,
                                   on_error=on_error,
                                   on_close=on_close,
                                   on_open=on_open)

            # Executar WebSocket em thread separada
            def run_websocket():
                self.ws.run_forever()
                
            thread = threading.Thread(target=run_websocket)
            thread.daemon = True
            thread.start()
            print("WebSocket iniciado em thread separada")
            
        except Exception as e:
            print(f"Erro ao iniciar WebSocket: {e}")
                
            
    def selecionar_equipe_direita(self):
        self.selecionar += 1
        if self.selecionar >= len(self.equipes):
            self.selecionar = 0
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()
        
    def selecionar_equipe_esquerda(self):
        self.selecionar -= 1
        if self.selecionar < 0:
            self.selecionar = len(self.equipes) - 1
        self.ids.tituloEquipe.text = self.equipes[self.selecionar].exibeTitulo()

    def iniciar_cronometro(self):
        self.cronometroTempoTotal.iniciar()
        self.eventoTextoTempoTotal = Clock.schedule_interval(self.altera_texto_tempo_total, 0.01)
        self.ids.botaoEsquerda.disabled = True
        self.ids.botaoDireita.disabled = True

    def altera_texto_tempo_total(self, dt):
        tempo = self.cronometroTempoTotal.obter_tempo_atual()

        self.ids.tempoTotal.text = self.cronometroTempoTotal.obter_tempo_formatado()

        if tempo >= 180:  ## ta dando um erreinho de alguns milisegundos, mas a logica funciona
            self.cronometroTempoTotal.pausar_cronometro()
            if getattr(self, 'eventoTextoTempoTotal', None):
                self.eventoTextoTempoTotal.cancel()
                self.eventoTextoTempoTotal = None

    
                
    def altera_texto_tempo_volta(self, dt):
        self.ids.tempoVolta.text = self.cronometroTempoVolta.obter_tempo_formatado()
        
    def zerar_cronometro(self):
        self.cronometroTempoTotal.zerar_cronometro()
        self.ids.tempoTotal.text = "00:00.000"
        #self.ids.
        if self.eventoTextoTempoTotal:
            self.eventoTextoTempoTotal.cancel()
            self.eventoTextoTempoTotal = None
        self.ids.botaoEsquerda.disabled = False
        self.ids.botaoDireita.disabled = False
        if self.eventoTextoTempoVolta is not None:
            self.zerar_cronometro_volta()

    def zerar_cronometro_volta(self):
        self.cronometroTempoVolta.zerar_cronometro()
        self.ids.tempoVolta.text = "00:00.000"
        if self.eventoTextoTempoVolta:    
            self.eventoTextoTempoVolta.cancel()
            self.eventoTextoTempoVolta = None
        self.inicio = True
        
        

class cronometroLinusApp(MDApp):
    def build(self):
        # Configurar tela cheia
        Window.fullscreen = 'auto'
        return MyWidget()
    
if __name__ == '__main__':  
    cronometroLinusApp().run()