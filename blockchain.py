import json
import hashlib
import sys
from time import time
from uuid import uuid4
from flask import Flask, jsonify

class Blockchain():
    """defience a block chain on one machine"""
    def __init__(self):
        self.chain = []
        self.current_trxs = []
        self.new_block(previous_hash=1, proof=100)
        
    def new_block(self , proof , previous_hash=None):
        """create a new block """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'trxs': self.current_trxs,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
       }
        self.current_trxs = []
       
        self.chain.append(block)
        return block  
      
    def new_trx(self , sender , recipient , amount):
        """add a new trx to the mempool"""
        self.current_trxs.append({'sender': sender, 'recipient': recipient,
                                 'amount': amount})
        return self.last_block['index'] + 1
        
    @staticmethod
    def hash(block):
        """hash a block"""
        block_string = json.dump(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    @property   
    def last_block(self):
        """ return last block"""
        pass
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """checks if this proof is fine or not"""
        this_proof = '{proof}{last_proof}'.encode()
        this_proof_hash = hashlib.sha256(this_proof).hexdigest()
        return this_proof_hash[:4] == '0000'
     
    def proof_of_work(self, last_proof):
        """shows that the work is done"""
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
            
        return proof
    
 app = Flask(__name__)
 
 node_id = str(uuid4())
 
 blockchain = Blockchain()
 
 @app.route('/mine')
 def mine():
     """this will mine one block and 
     will add it to the chain
     """
     return "I will mine!"
 @app.route('/trxs/new', methods=['POST'])
 def new_trx():
     """will add a new trx """
     return 'a new trx added'
 
 @app.route('/chain')
 def full_chain():
     """returns th full chain"""
     res = {
         'chain': blockchain.chain,
         'length': len(blcokchain.chain),
         
    }
    return jsonify(res), 200
 
 
 if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1])
 