import logging 

logging.basicConfig(
    level=logging.INFO, # Define o nível mínimo de mensagem a ser exibido
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", # Define o formato da mensagem
)
logger = logging.getLogger("main")

