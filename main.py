from web3 import Web3
import threading
import logging
import time
import copy
import json
import pickle
import concurrent.futures

AbiDict ={'default':'[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"minTokensBeforeSwap","type":"uint256"}],"name":"MinTokensBeforeSwapUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"tokensSwapped","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethReceived","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"tokensIntoLiqudity","type":"uint256"}],"name":"SwapAndLiquify","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bool","name":"enabled","type":"bool"}],"name":"SwapAndLiquifyEnabledUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"_liquidityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_maxTxAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_taxFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"}],"name":"deliver","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"excludeFromReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"geUnlockTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInFee","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"includeInReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromFee","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"isExcludedFromReward","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"time","type":"uint256"}],"name":"lock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tAmount","type":"uint256"},{"internalType":"bool","name":"deductTransferFee","type":"bool"}],"name":"reflectionFromToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"liquidityFee","type":"uint256"}],"name":"setLiquidityFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"maxTxPercent","type":"uint256"}],"name":"setMaxTxPercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"_enabled","type":"bool"}],"name":"setSwapAndLiquifyEnabled","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"taxFee","type":"uint256"}],"name":"setTaxFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"swapAndLiquifyEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rAmount","type":"uint256"}],"name":"tokenFromReflection","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"uniswapV2Pair","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"uniswapV2Router","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
}

class blockchainConnector:

    def __init__(self, urlWeb3):
        self.urlWeb3 = urlWeb3
        self.web3 = Web3(Web3.HTTPProvider(urlWeb3))
        from web3.middleware import geth_poa_middleware
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        

class logConnector:

    def __init__(self):
        logging.basicConfig(level=logging.INFO,
                    format='(%(threadName)-9s) %(message)s',)


class blockchain(blockchainConnector, logConnector):

    class block(blockchainConnector, logConnector):

            def __init__(self, blockNumber, blockchainData, urlWeb3):
                blockchainConnector.__init__(self, urlWeb3)
                logConnector.__init__(self)

                self.blockChainData = blockchainData
                self.transactionsPointer = self.blockChainData['transactions']
                self.blockNumber = blockNumber
                self.blockTransactions  = self.web3.eth.get_block(self.blockNumber)              
                #logging.warning("Transactions in block " + str(self.blockNumber) + ": " + str(self.blockTransactions['transactions']))
                for item in self.blockTransactions['transactions']:
                    self.transactionsPointer[blockchain.transaction(item.hex(),self.blockChainData, self.urlWeb3)] = self.blockNumber

    class transaction(blockchainConnector):

        def __init__(self, transactionID, blockchainData, urlWeb3):
            blockchainConnector.__init__(self, urlWeb3)
 
            self.blockchainData = blockchainData
            self.transactionID = transactionID
            self.addressesPointer = self.blockchainData['addresses']
            self.transactionData = self.web3.eth.get_transaction(self.transactionID)
            self.fromAddress = self.transactionData['from']
            self.toAddress = self.transactionData['to']
            self.addressesPointer[self.fromAddress] = blockchain.address(self.fromAddress, self.blockchainData, self.urlWeb3)
            self.addressesPointer[self.toAddress] = blockchain.address(self.toAddress, self.blockchainData, self.urlWeb3)


    class address(blockchainConnector, logConnector):

        def __init__(self, addressPublicKey, blockchainData, urlWeb3):

            blockchainConnector.__init__(self, urlWeb3)
            self.blockchainData = blockchainData
            self.addressPublicKey = addressPublicKey
            self.contractStore = blockchainData["contracts"]
            self.getTokenIfContract()


        def getTokenIfContract(self):

         

            try:

                tokenAddress = str(self.web3.toChecksumAddress(self.addressPublicKey))
                tokenRouter = self.web3.eth.contract(tokenAddress, abi=json.loads(AbiDict['default']))

                self.nameTokenContract = tokenRouter.functions.name().call()
                logging.warning("Found Token Contract: " + self.nameTokenContract)
                self.contractStore[self.addressPublicKey] = blockchain.contract(self.addressPublicKey, self.blockchainData, self.urlWeb3 )
                #return self.nameTokenContract
                

            except:

                pass


    
    class contract(blockchainConnector):

        def __init__(self, addressPublicKey, blockchainData, urlWeb3):
            blockchainConnector.__init__(self, urlWeb3)
            self.addressPublicKey = addressPublicKey
            
            self.tokenRouter = self.web3.eth.contract(self.addressPublicKey, abi=json.loads(AbiDict['default']))
            self.tokenName = self.tokenRouter.functions.name().call()
            self.dataStore = blockchainData["contracts"]
            
            



####Blockchain
    def __init__(self, urlWeb3):
        blockchainConnector.__init__(self, urlWeb3)
        logConnector.__init__(self)


        self.statuses = {"parse": True}
        self._lastblock = 0
        self.lastprocessedblock = 0

        self.blockchainData = {"blocks":{},"transactions":{},"addresses":{},"contracts":{}}

        ####TRY LOAD CONTRACTS
        try:
            
            self.preload = self.preloadBlockChainData("contracts")
            for item in self.preload:
                self.blockchainData["contracts"][item]=self.contract(item, self.blockchainData, self.urlWeb3)

        except:

            pass

        finally:
            self.contracts = self.blockchainData["contracts"]

        
        ##TRY LOAD ADDRESSES
        try:
            
            self.preload = self.preloadBlockChainData("addresses")
            for item in self.preload:
                self.blockchainData["addresses"][item]=self.address(item, self.blockchainData, self.urlWeb3)

        except:

            pass

        finally:
            self.contracts = self.blockchainData["addresses"]

           ##TRY LOAD TRANSACTIONS
        try:
            
            self.preload = self.preloadBlockChainData("transactions")
            for item in self.preload:
                self.blockchainData["transactions"][item]=self.transaction(item, self.blockchainData, self.urlWeb3)

        except:

            pass

        finally:
            self.contracts = self.blockchainData["transactions"]
       ##TRY LOAD BLOCKS
        try:
            
            self.contractdict = self.preloadBlockChainData("blocks")
            trueblock = 0
            for item in self.contractdict:
                self.blockchainData["blocks"][item]=self.block(trueblock, item, self.blockchainData, self.urlWeb3)
                trueblock = trueblock + 1

        except:

            pass

        finally:
            self.contracts = self.blockchainData["blocks"]
       ##TRY LOAD LAST CHECKED BLOCK
        try:
            
            self.lastprocessedblock = self.preloadBlockChainData("lastcheckedblock")
        except:

            self.lastprocessedblock = 0

    
            


        


        self.blocks = self.blockchainData["blocks"]
        self.transactions = self.blockchainData["transactions"]
        self.addresses = self.blockchainData["addresses"]
        
        self._lastblock = 0

    def preloadBlockChainData(self, filename):
        self.blockchaindatafile = open(filename,'rb')
        self.loadedData = pickle.load(self.blockchaindatafile)
        self.blockchaindatafile.close()
        return self.loadedData

            


    @property
    def lastblock(self):
        
        self._lastblock = int(self.web3.eth.block_number)

        return self._lastblock



    
    def parseblocks(self):

        
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:

            while self.statuses["parse"] is True:

                for lastprocessbl in range(int(self.lastblock)):
                
                        future_to_cc = {executor.submit(self.insertBlock, self.lastprocessedblock)}
                        self.lastprocessedblock = self.lastprocessedblock + 1

                for future in concurrent.futures.as_completed(future_to_cc):
                    try:
                        lastprocessbl = future_to_cc[future]
                    except:
                        print ("Job Finished")
                    try:
                        data = future.result()

                    except Exception as exc:

                        print('%r generated an exception: %s' % (lastprocessbl, exc))
                    else:
                        print('%r page is %d bytes' % (lastprocessbl, len(data)))
#wait(futures)

                

    def insertBlock(self, lastprocessedblock):
        self.lastprocessedblock = lastprocessedblock

        logging.info ("Processing block "+ str(self.lastprocessedblock) + " of " + str(self._lastblock) )
        self.data = self.web3.eth.get_block(self.lastprocessedblock)

        self.blocks[self.lastprocessedblock] = blockchain.block(self.lastprocessedblock, self.blockchainData, self.urlWeb3)

    def printLastBlock(self):

        while True:

            logging.info (self.myLastblock)
            time.sleep(2)
    
    def showBlocks (self):

        self.blocksSnapshot = copy.deepcopy(self.blocks)
        myKeys = self.blocksSnapshot.keys()

        for item in myKeys:

            print (self.blocksSnapshot[item].blockNumber)

        del self.blocksSnapshot

    def shutdownBlockchain(self):
            self.statuses["parse"] = False
            self.blockchaindatafile = open("blockchain",'wb')
            pickle.dump(self.blockchainData, self.blockchaindatafile)
            self.blockchaindatafile.close()
if __name__ == '__main__':

 
        
    

    polyChain = blockchain("https://polygon-mainnet.infura.io/v3/e209d7d77e934b32a98ab3fb700513e3")

    
    
    #p1 = threading.Thread(target=polyChain.printLastBlock)
    p2 = threading.Thread(target=polyChain.parseblocks)
    #p3 = threading.Thread(target=polyChain.showBlocks)

    #p1.start()
    p2.start()

    while True:
        time.sleep (10)
        logging.info('Found ' + str(len(polyChain.blockchainData['contracts'].keys())) +' Token Contracts detected by now:')
        for item in polyChain.blockchainData['contracts'].keys():

            logging.info (polyChain.blockchainData['contracts'][item].tokenName + " with address: " + polyChain.blockchainData['contracts'][item].addressPublicKey)

        #print (polyChain.blockchainData)







 

  



                




        