from mev_inspect.arbitrage import get_arbitrages
from mev_inspect.schemas.swaps import Swap
from mev_inspect.swaps import (
    UNISWAP_V2_PAIR_ABI_NAME,
    UNISWAP_V3_POOL_ABI_NAME,
)


def test_two_pool_arbitrage(get_transaction_hashes, get_addresses):
    block_number = 123
    [transaction_hash] = get_transaction_hashes(1)

    [
        account_address,
        first_pool_address,
        second_pool_address,
        first_token_address,
        second_token_address,
    ] = get_addresses(5)

    first_token_in_amount = 10
    first_token_out_amount = 10
    second_token_amount = 15

    swaps = [
        Swap(
            abi_name=UNISWAP_V2_PAIR_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[0],
            pool_address=first_pool_address,
            from_address=account_address,
            to_address=second_pool_address,
            token_in_address=first_token_address,
            token_in_amount=first_token_in_amount,
            token_out_address=second_token_address,
            token_out_amount=second_token_amount,
        ),
        Swap(
            abi_name=UNISWAP_V3_POOL_ABI_NAME,
            transaction_hash=transaction_hash,
            block_number=block_number,
            trace_address=[1],
            pool_address=second_pool_address,
            from_address=first_pool_address,
            to_address=account_address,
            token_in_address=second_token_address,
            token_in_amount=first_token_in_amount,
            token_out_address=first_token_address,
            token_out_amount=first_token_out_amount,
        ),
    ]

    arbitrages = get_arbitrages(swaps)

    assert len(arbitrages) == 1
