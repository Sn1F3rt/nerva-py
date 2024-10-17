from __future__ import annotations

from typing import Any, Dict, List, Optional

import aiohttp

__all__ = ["DaemonJSONRPC", "DaemonOther"]


class DaemonJSONRPC:
    """
    A class to interact with the Nerva daemon's JSON-RPC interface.

    Parameters
    ----------
    host : str, optional
        The host of the daemon.
    port : int, optional
        The port of the daemon.
    ssl : bool, optional
        Whether to use SSL.
    timeout : float, optional
        The timeout for the request.

    Attributes
    ----------
    url : str
        The URL of the daemon.
    timeout : float
        The timeout for the request.
    headers : Dict[str, str]
        The headers for the request.
    """

    __slots__ = ["url", "timeout", "headers"]

    def __init__(
        self,
        host: Optional[str] = "localhost",
        port: Optional[int] = 17566,
        ssl: Optional[bool] = False,
        timeout: Optional[float] = 10.0,
    ) -> None:
        self.url: str = f"{'https' if ssl else 'http'}://{host}:{port}"
        self.timeout: float = timeout
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}

    async def _request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/json_rpc",
                json={"jsonrpc": "2.0", "id": 0, "method": method, "params": params},
                headers=self.headers,
                timeout=self.timeout,
            ) as response:
                return await response.json(content_type=None)

    async def get_block_count(self) -> Dict[str, Any]:
        """
        Get the current block count.

        Returns
        -------
        dict
            The response from the daemon.
        """
        return await self._request("get_block_count", {})

    async def on_get_block_hash(self, height: int) -> Dict[str, Any]:
        """
        Get the block hash at a certain height.

        Parameters
        ----------
        height : int
            The height of the block.

        Returns
        -------
        dict
            The response from the daemon.

        """
        return await self._request("on_get_block_hash", {"height": height})

    async def get_block_template(
        self, wallet_address: str, reserve_size: int
    ) -> Dict[str, Any]:
        """
        Get a block template for mining.

        Parameters
        ----------
        wallet_address : str
            The wallet address to mine to.

        reserve_size : int
            The reserve size.

        Returns
        -------
        dict
            The response from the daemon.

        """
        return await self._request(
            "get_block_template",
            {"wallet_address": wallet_address, "reserve_size": reserve_size},
        )

    async def submit_block(self, block_blob: List[str]) -> Dict[str, Any]:
        """
        Submit a block to the network.

        Parameters
        ----------
        block_blob : List[str]
            The block blob to submit.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("submit_block", {"blob": block_blob})

    async def get_last_block_header(self) -> Dict[str, Any]:
        """
        Get the last block header.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_last_block_header", {})

    async def get_block_header_by_hash(self, block_hash: str) -> Dict[str, Any]:
        """
        Get the block header by hash.

        Parameters
        ----------
        block_hash : str
            The hash of the block.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_block_header_by_hash", {"hash": block_hash})

    async def get_block_header_by_height(self, height: int) -> Dict[str, Any]:
        """
        Get the block header by height.

        Parameters
        ----------
        height : int
            The height of the block.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_block_header_by_height", {"height": height})

    async def get_block_headers_range(
        self, start_height: int, end_height: int
    ) -> Dict[str, Any]:
        """
        Get a range of block headers.

        Parameters
        ----------
        start_height : int
            The start height.
        end_height : int
            The end height.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_block_headers_range",
            {"start_height": start_height, "end_height": end_height},
        )

    async def get_block(
        self, block_hash: Optional[str] = None, height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get a block by hash or height.

        Parameters
        ----------
        block_hash : str, optional
            The hash of the block.
        height : int, optional
            The height of the block.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        if block_hash and not height:
            return await self._request("get_block", {"hash": block_hash})

        elif height and not block_hash:
            return await self._request("get_block", {"height": height})

        else:
            raise ValueError("Either block_hash OR height must be provided.")

    async def get_connections(self) -> Dict[str, Any]:
        """
        Get the connections to the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_connections", {})

    async def get_info(self) -> Dict[str, Any]:
        """
        Get the information about the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_info", {})

    async def hard_fork_info(self) -> Dict[str, Any]:
        """
        Get the hard fork information.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("hard_fork_info", {})

    async def set_bans(self, bans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Set bans for the daemon.

        Parameters
        ----------
        bans : List[Dict[str, Any]]
            The bans to set. Each ban should be a dictionary with the following keys:
                - host : str
                    Host to ban (IP in A.B.C.D format).
                - ip : int, optional
                    IP to ban (int format).
                - ban : bool
                    Set `true` to ban, `false` to unban.
                - seconds : int
                    Time to ban in seconds.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("set_bans", {"bans": bans})

    async def get_bans(self) -> Dict[str, Any]:
        """
        Get the bans of the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_bans", {})

    async def flush_txpool(self, txids: Optional[list] = None) -> Dict[str, Any]:
        """
        Flush the transaction pool.

        Parameters
        ----------
        txids : list, optional
            The transaction IDs to flush. If not provided, all transactions will be flushed.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("flush_txpool", {"txids": txids or []})

    async def get_output_histogram(
        self,
        amounts: list,
        min_count: int,
        max_count: int,
        unlocked: bool,
        recent_cutoff: int,
    ) -> Dict[str, Any]:
        """
        Get the output histogram.

        Parameters
        ----------
        amounts : list
            The amounts to get the histogram for.
        min_count : int
            The minimum count.
        max_count : int
            The maximum count.
        unlocked : bool
            Whether to get the unlocked outputs.
        recent_cutoff : int
            The recent cutoff.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_output_histogram",
            {
                "amounts": amounts,
                "min_count": min_count,
                "max_count": max_count,
                "unlocked": unlocked,
                "recent_cutoff": recent_cutoff,
            },
        )

    async def get_version(self) -> Dict[str, Any]:
        """
        Get the version of the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_version", {})

    async def get_coinbase_tx_sum(self, height: int, count: int) -> Dict[str, Any]:
        """
        Get the coinbase transaction sum.

        Parameters
        ----------
        height : int
            The height of the block.
        count : int
            The count of blocks.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_coinbase_tx_sum", {"height": height, "count": count}
        )

    async def get_fee_estimate(
        self, grace_blocks: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get the fee estimate.

        Parameters
        ----------
        grace_blocks : int, optional
            The number of grace blocks.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_fee_estimate",
            {"grace_blocks": grace_blocks} if grace_blocks else {},
        )

    async def get_alternate_chains(self) -> Dict[str, Any]:
        """
        Get the alternate chains.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_alternate_chains", {})

    async def relay_tx(self, txids: list) -> Dict[str, Any]:
        """
        Relay transactions to the network.

        Parameters
        ----------
        txids : list
            The transaction IDs to relay.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("relay_tx", {"txids": txids})

    async def sync_info(self) -> Dict[str, Any]:
        """
        Get the sync information of the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("sync_info", {})

    async def get_txpool_backlog(self) -> Dict[str, Any]:
        """
        Get the transaction pool backlog.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_txpool_backlog", {})

    async def get_output_distribution(
        self,
        amounts: list[int],
        from_height: Optional[int] = 0,
        to_height: Optional[int] = 0,
        cumulative: Optional[bool] = False,
        binary: Optional[bool] = True,
        compress: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Get the output distribution.

        Parameters
        ----------
        amounts : list[int]
            The amounts to get the distribution for.
        from_height : int, optional
            The height to start from.
        to_height : int, optional
            The height to end at.
        cumulative : bool, optional
            Whether to get the cumulative distribution.
        binary : bool, optional
            Whether to get the binary distribution.
        compress : bool, optional
            Whether to compress the distribution.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_output_distribution",
            {
                "amounts": amounts,
                "from_height": from_height,
                "to_height": to_height,
                "cumulative": cumulative,
                "binary": binary,
                "compress": compress,
            },
        )

    async def prune_blockchain(self) -> Dict[str, Any]:
        """
        Prune the blockchain.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("prune_blockchain", {})

    async def flush_cache(self, bad_txs: Optional[bool] = False) -> Dict[str, Any]:
        """
        Flush the cache.

        Parameters
        ----------
        bad_txs : bool, optional
            Whether to flush the bad transactions.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("flush_cache", {"bad_txs": bad_txs})

    async def get_generated_coins(
        self, height: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get the generated coins.

        Parameters
        ----------
        height : int, optional
            The height.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_generated_coins", {"height": height} if height else {}
        )

    async def get_min_version(self) -> Dict[str, Any]:
        """
        Get the minimum version of the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_min_version", {})

    async def get_tx_pubkey(self, extra: str) -> Dict[str, Any]:
        """
        Get the transaction public key.

        Parameters
        ----------
        extra : str
            The extra data.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_tx_pubkey", {"extra": extra})

    async def decode_outputs(
        self, tx_hashes: list, sec_view_key: str, address: str
    ) -> Dict[str, Any]:
        """
        Decode the outputs of transactions.

        Parameters
        ----------
        tx_hashes : list
            The transaction hashes.
        sec_view_key : str
            The secret view key.
        address : str
            The address to decode.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "decode_outputs",
            {
                "tx_hashes": tx_hashes,
                "sec_view_key": sec_view_key,
                "address": address,
            },
        )

    async def add_peer(self, host: str) -> Dict[str, Any]:
        """
        Add a peer to the daemon.

        Parameters
        ----------
        host : str
            The host of the peer.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("add_peer", {"host": host})


class DaemonOther:
    """
    A class to interact with the Nerva daemon's independent endpoint methods.

    Parameters
    ----------
    host : str, optional
        The host of the daemon.
    port : int, optional
        The port of the daemon.
    ssl : bool, optional
        Whether to use SSL.
    timeout : float, optional
        The timeout for the request.

    Attributes
    ----------
    url : str
        The URL of the daemon.
    timeout : float
        The timeout for the request.
    headers : dict
        The headers for the request.

    """

    __slots__ = ["url", "timeout", "headers"]

    def __init__(
        self,
        host: Optional[str] = "localhost",
        port: Optional[int] = 17566,
        ssl: Optional[bool] = False,
        timeout: Optional[float] = 10.0,
    ):
        self.url = f"{'https' if ssl else 'http'}://{host}:{port}"
        self.timeout = timeout

        self.headers = {"Content-Type": "application/json"}

    async def _request(
        self, endpoint: str, params: Dict[str, Any]
    ) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.url}/{endpoint}",
                json=params,
                headers=self.headers,
                timeout=self.timeout,
            ) as response:
                return await response.json(content_type=None)

    async def get_height(self) -> Dict[str, Any]:
        """
        Get the current block height.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_height", {})

    async def get_blocks_bin(
        self, block_ids: list[str], start_height: int, prune: bool
    ) -> Dict[str, Any]:
        """
        Get a list of blocks.

        Parameters
        ----------
        block_ids : list[str]
            Binary list of block IDs.
        start_height : int
            The start height.
        prune : bool
            Whether to prune the blocks.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_blocks.bin",
            {"block_ids": block_ids, "start_height": start_height, "prune": prune},
        )

    async def get_blocks_by_height_bin(self, heights: List[int]) -> Dict[str, Any]:
        """
        Get a list of blocks by height.

        Parameters
        ----------
        heights : List[int]
            The block heights to get.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_blocks_by_height.bin", {"heights": heights})

    async def get_hashes_bin(
        self, block_ids: List[str], start_height: int
    ) -> Dict[str, Any]:
        """
        Get the hashes of blocks.

        Parameters
        ----------
        block_ids : list[str]
            Binary list of block IDs.
        start_height : int
            The start height.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_hashes.bin", {"block_ids": block_ids, "start_height": start_height}
        )

    async def get_o_indexes_bin(self, txid: str) -> Dict[str, Any]:
        """
        Get the output indexes of a transaction.

        Parameters
        ----------
        txid : str
            Binary transaction ID.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_o_indexes.bin", {"txid": txid})

    async def get_outs_bin(self, outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get the outputs.

        Parameters
        ----------
        outputs : List[Dict[str, Any]]
            List of outputs as dictionaries with the following keys:
                - amount : int
                    The amount.
                - index : int
                    The index.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_outs.bin", {"outputs": outputs})

    async def get_transactions(
        self,
        txs_hashes: list[str],
        decode_as_json: Optional[bool] = False,
        prune: Optional[bool] = False,
        split: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Get a list of transactions.

        Parameters
        ----------
        txs_hashes : list[str]
            List of transaction hashes.
        decode_as_json : bool, optional
            Whether to decode as JSON.
        prune : bool, optional
            Whether to prune the transactions.
        split : bool, optional
            Whether to split the transactions.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_transactions",
            {
                "txs_hashes": txs_hashes,
                "decode_as_json": decode_as_json,
                "prune": prune,
                "split": split,
            },
        )

    async def get_alt_blocks_hashes(self) -> Dict[str, Any]:
        """
        Get the hashes of alternate blocks.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_alt_blocks_hashes", {})

    async def is_key_image_spent(self, key_images: List[str]) -> Dict[str, Any]:
        """
        Check if key images are spent.

        Parameters
        ----------
        key_images : List[str]
            List of key images.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("is_key_image_spent", {"key_images": key_images})

    async def send_raw_transaction(
        self, tx_as_hex: str, do_not_relay: Optional[bool] = False
    ) -> Dict[str, Any]:
        """
        Send a raw transaction.

        Parameters
        ----------
        tx_as_hex : str
            The transaction as hex.
        do_not_relay : bool, optional
            Whether to relay the transaction.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "send_raw_transaction",
            {"tx_as_hex": tx_as_hex, "do_not_relay": do_not_relay},
        )

    async def start_mining(
        self,
        address: str,
        threads_count: int,
        do_background_mining: bool,
        ignore_battery: bool,
    ) -> Dict[str, Any]:
        """
        Start mining.

        Parameters
        ----------
        address : str
            The address to mine to.
        threads_count : int
            The number of threads.
        do_background_mining : bool
            Whether to mine in the background.
        ignore_battery : bool
            Whether to ignore the battery.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "start_mining",
            {
                "address": address,
                "threads_count": threads_count,
                "do_background_mining": do_background_mining,
                "ignore_battery": ignore_battery,
            },
        )

    async def set_donate_level(self, blocks: int) -> Dict[str, Any]:
        """
        Set the donate level.

        Parameters
        ----------
        blocks : int
            The number of blocks to donate.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("set_donate_level", {"blocks": blocks})

    async def stop_mining(self) -> Dict[str, Any]:
        """
        Stop mining.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("stop_mining", {})

    async def mining_status(self) -> Dict[str, Any]:
        """
        Get the mining status.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("mining_status", {})

    async def save_bc(self) -> Dict[str, Any]:
        """
        Save the blockchain.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("save_bc", {})

    async def get_peer_list(self) -> Dict[str, Any]:
        """
        Get the peer list.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_peer_list", {})

    async def get_public_nodes(self) -> Dict[str, Any]:
        """
        Get the public nodes.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_public_nodes", {})

    async def set_log_hash_rate(self, visible: bool) -> Dict[str, Any]:
        """
        Set the log hash rate.

        Parameters
        ----------
        visible : bool
            Whether to make the hash rate visible.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("set_log_hash_rate", {"visible": visible})

    async def set_log_level(self, level: int) -> Dict[str, Any]:
        """
        Set the log level.

        Parameters
        ----------
        level : int
            The log level.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("set_log_level", {"level": level})

    async def set_log_categories(self, categories: str) -> Dict[str, Any]:
        """
        Set the log categories.

        Parameters
        ----------
        categories : str
            The log categories.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("set_log_categories", {"categories": categories})

    async def get_transaction_pool(self) -> Dict[str, Any]:
        """
        Get the transaction pool.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_transaction_pool", {})

    async def get_transaction_pool_hashes_bin(self) -> Dict[str, Any]:
        """
        Get the transaction pool hashes.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_transaction_pool_hashes.bin", {})

    async def get_transaction_pool_hashes(self) -> Dict[str, Any]:
        """
        Get the transaction pool hashes.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_transaction_pool_hashes", {})

    async def get_transaction_pool_stats(self) -> Dict[str, Any]:
        """
        Get the transaction pool stats.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_transaction_pool_stats", {})

    async def set_bootstrap_daemon(
        self, address: str, username: str, password: str
    ) -> Dict[str, Any]:
        """
        Set the bootstrap daemon.

        Parameters
        ----------
        address : str
            The address of the daemon.
        username : str
            The username.
        password : str
            The password.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "set_bootstrap_daemon",
            {"address": address, "username": username, "password": password},
        )

    async def stop_daemon(self) -> Dict[str, Any]:
        """
        Stop the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("stop_daemon", {})

    async def get_info(self) -> Dict[str, Any]:
        """
        Get the information of the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_info", {})

    async def get_net_stats(self) -> Dict[str, Any]:
        """
        Get the network stats.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_net_stats", {})

    async def get_limit(self) -> Dict[str, Any]:
        """
        Get daemon bandwidth limits.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("get_limit", {})

    async def set_limit(self, limit_down: int, limit_up: int) -> Dict[str, Any]:
        """
        Set daemon bandwidth limits.

        Parameters
        ----------
        limit_down : int
            The download limit. (-1 to change to default; 0 for no change)
        limit_up : int
            The upload limit. (-1 to change to default; 0 for no change)

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "set_limit", {"limit_down": limit_down, "limit_up": limit_up}
        )

    async def out_peers(self) -> Dict[str, Any]:
        """
        Get the outgoing peers.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("out_peers", {})

    async def in_peers(self) -> Dict[str, Any]:
        """
        Get the incoming peers.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("in_peers", {})

    async def get_outs(
        self, outputs: List[Dict[str, Any]], get_txid: bool
    ) -> Dict[str, Any]:
        """
        Get outputs.

        Parameters
        ----------
        outputs : List[Dict[str, Any]]
            List of outputs as dictionaries with the following keys:
                - amount : int
                    The amount.
                - index : int
                    The index.
        get_txid : bool
            Whether to get the transaction ID.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_outs", {"outputs": outputs, "get_txid": get_txid}
        )

    async def update(self) -> Dict[str, Any]:
        """
        Update the daemon.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("update", {})

    async def get_output_distribution_bin(
        self,
        amounts: list[int],
        from_height: Optional[int] = 0,
        to_height: Optional[int] = 0,
        cumulative: Optional[bool] = False,
        binary: Optional[bool] = True,
        compress: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Get the output distribution.

        Parameters
        ----------
        amounts : list[int]
            The amounts to get the distribution for.
        from_height : int, optional
            The height to start from.
        to_height : int, optional
            The height to end at.
        cumulative : bool, optional
            Whether to get the cumulative distribution.
        binary : bool, optional
            Whether to get the binary distribution.
        compress : bool, optional
            Whether to compress the distribution.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request(
            "get_output_distribution.bin",
            {
                "amounts": amounts,
                "from_height": from_height,
                "to_height": to_height,
                "cumulative": cumulative,
                "binary": binary,
                "compress": compress,
            },
        )

    async def pop_blocks(self, nblocks: int) -> Dict[str, Any]:
        """
        Pop blocks from the blockchain.

        Parameters
        ----------
        nblocks : int
            The number of blocks to pop.

        Returns
        -------
        Dict[str, Any]
            The response from the daemon.

        """
        return await self._request("pop_blocks", {"nblocks": nblocks})
