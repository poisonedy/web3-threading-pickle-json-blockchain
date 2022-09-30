from web3 import Web3
import threading
import logging

class blockchainConnector:

    def __init__(self, urlWeb3):
        self.web3 = Web3(Web3.HTTPProvider(urlWeb3))
        from web3.middleware import geth_poa_middleware
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

class logConnector:

    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)


class blockchain(blockchainConnector, logConnector):

    class block(blockchainConnector):
            def __init__(self, number, blockchainData):
                self.number = number
                self.dataStore = blockchainData["transactions"]


    class transaction(blockchainConnector):
        def __init__(self, transactionID, blockchainData):
            self.transactionID = transactionID
            self.dataStore = blockchainData["addresses"]


    class address(blockchainConnector):
        def __init__(self, addressPublicKey, blockchainData):
            self.addressPublicKey = addressPublicKey
            self.dataStore = blockchainData["contracts"]
    
    class contract(blockchainConnector):
        def __init__(self, addressPublicKey, blockchainData):
            self.addressPublicKey = addressPublicKey
            self.dataStore = blockchainData["contracts"]

    def __init__(self, urlWeb3):
        blockchainConnector.__init__(self, urlWeb3)
        logConnector.__init__(self)


        self.statuses = {"parse": True}
        

        self.blockchainData = {"lastblock":"0","blocks":{},"transactions":{},"addresses":{},"contracts":{}}
        self.blocks = self.blockchainData["blocks"]
        self.transactions = self.blockchainData["transactions"]
        self.addresses = self.blocks = self.blockchainData["addresses"]
        self.contracts = self.blocks = self.blockchainData["contracts"]

        


    @property
    def lastblock(self):
        self.blockchainData["lastblock"] = self.web3.eth.block_number
        return self.blockchainData["lastblock"]

    
    def parseblocks(self):
        self.lastprocessedblock = 0
        while self.statuses["parse"] is True:

            if self.lastprocessedblock < self.lastblock:
                logging.info ("Processing block: "+ str(self.lastprocessedblock) )
                self.data = self.web3.eth.get_block(self.lastprocessedblock)
                self.blocks = {self.lastprocessedblock:self.block(self.lastprocessedblock, self.data)}
                self.lastprocessedblock = self.lastprocessedblock + 1

    



polyChain = blockchain("https://polygon-mainnet.infura.io/v3/e209d7d77e934b32a98ab3fb700513e3")

def parse():
    polyChain.parseblocks()
logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)
def info ():
    while True:
        logging.info (polyChain.lastblock)
        logging.info (polyChain.lastprocessedblock)
        
myThr = threading.Thread(target=parse(), daemon=True)
myInfo = threading.Thread(target=info())



myThr.start()
myInfo.start()

        


                




        