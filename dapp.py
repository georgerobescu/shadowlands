from contract.contract import Contract
from contract.weth import Weth
#from contract.ens import Ens
from contract.ens_registry import EnsRegistry
from contract.ens_resolver import EnsResolver
from contract.ens_reverse_resolver import EnsReverseResolver
from eth_utils import decode_hex, encode_hex
from credstick import Credstick, DeriveCredstickAddressError, OpenCredstickError, CloseCredstickError
import eth_node 


ERC20 = {
    'WETH': Weth
}

credstick = None

w3 = None


def register_w3_on_contracts():
    Contract.w3 = w3

# import pdb; pdb.set_trace()


# Both of these invocations have the same precise effect.  the .eth domain will be added
# if it is not already in the string.
#
# register_ens_resolver('ceilingcat')
# register_ens_resolver('ceilingcat.eth')
def register_ens_resolver(name):
    return push( 
        EnsRegistry.set_resolver(name) 
    )

def set_ens_resolver_address(name, address_target):
    return push(
        EnsResolver.set_address(name, address_target)
    )
   
def set_ens_reverse_lookup(name):
    return push(
        EnsReverseResolver.set_name(name)
    )
 

# send_erc20('WETH', '0xb75D1e62b10E4ba91315C4aA3fACc536f8A922F5', 0.01) 
def send_erc20(token, destination, amount):

    # NOTE
    # We borrow the web3 toWei method here.  We can do this because we assert 18
    # decimal places on all ERC contracts - or else they cannot load.
    # If I am able to figure out how to reliably get Decimal conversion working
    # for variable decimal place values on ERC20s, this can change.  So far things
    # are looking murky and I know I can trust the web3 code. (I hope)
    value = w3.toWei(amount, 'ether')

    return push(
        ERC20[token].transfer(destination, value)
    )


# send_ether('0xb75D1e62b10E4ba91315C4aA3fACc536f8A922F5', 0.01) 
def send_ether(destination, amount):
    tx_dict = build_send_tx(amount, destination)
    print("Unsigned transaction: ", tx_dict)
    signed_tx = credstick.signTx(tx_dict)
    print("Signed tx: ", signed_tx)
    rx = transact(signed_tx)
    print("tx receipt: ", rx)


def push( contract_function ):
    tx = contract_function.buildTransaction(defaultTxDict())
    signed_tx = credstick.signTx(tx)
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)


def build_send_tx(amt, recipient):
    return  dict(
        nonce=w3.eth.getTransactionCount(eth_node.ethAddress),
        gasPrice=w3.eth.gasPrice,
        gas=100000,
        to=decode_hex(recipient),
        value=w3.toWei(amt, 'ether'),
        data=b''
    )


def defaultTxDict():
    return dict(
        nonce=w3.eth.getTransactionCount(eth_node.ethAddress),
        gasPrice=w3.eth.gasPrice,
        gas=800000,
        value=0
    ) 

