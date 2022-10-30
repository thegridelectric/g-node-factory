import string
import struct

import algosdk
import algosdk.abi
import pendulum


def check_is_algo_address_string_format(candidate: str):
    """
    Note: could use algosdk.encoding.is_valid_address instead.
    Leaving in for the moment to keep looking at algosdk.abi and understand
    how to use it.

    Throw ValueError if algorand AddressType decode(encode(c)) fails.

    The public key of a private/public Ed25519 key pairis transformed into an Algorand address,
    by adding a 4-byte checksum to the end of the public key and then encoding it
    in base32."""

    at = algosdk.abi.AddressType()
    try:
        result = at.decode(at.encode(candidate))
    except Exception as e:
        raise ValueError(f"Not AlgoAddressStringFormat: {e}")


def check_is_algo_private_key_format(candidate: str) -> bool:
    """The private key of a private/public Ed25519 key pair is transformed into an Algorand address,
    by adding a 4-byte checksum to the end of the public key and then encoding it
    in base32."""
    try:
        algosdk.account.address_from_private_key(candidate)
    except Exception as e:
        raise ValueError(f"Not AlgoSecretKeyFormat: {e} /n {candidate} ")
    return True


def check_is_algo_msg_pack_encoded(candidate: str):
    """Throw ValueError if algosdk.encoding.future_msg_decode(candidate)
    throws an error"""
    try:
        algosdk.encoding.future_msgpack_decode(candidate)
    except Exception as e:
        raise ValueError(f"Not AlgoMsgPackEncoded: {e} /n {candidate}")


def check_is_valid_asa_name(candidate: str):
    """Throw ValueError if not a string or longer than 32 chars"""
    try:
        l = len(candidate)
    except Exception as e:
        raise ValueError(f"Not ValidAsaName: {e} /n {candidate} ")
    if l > 32:
        raise ValueError(
            f"Not ValidAsaName: AsaNames must be <= 32 /n {candidate} is {len(candidate)}"
        )


def check_is_64_bit_hex(candidate):
    if len(candidate) != 8:
        raise ValueError(f" {candidate} Must be length 8, not {len(candidate)}")
    if not all(c in string.hexdigits for c in candidate):
        raise ValueError("Must be hex digits")


def check_is_bit(candidate):
    if candidate not in {0, 1}:
        raise ValueError(f"{e} must be either 0 or 1")


def check_is_lrd_alias_format(candidate: str):
    """Lowercase AlphanumericStrings separated by dots (i.e. periods), with most
    significant word to the left.  I.e. `dw1.ne` is the child of `dw1`.
    Checking the format cannot verify the significance of words. All
    words must be alphanumeric. Most significant word must start with
    an alphabet charecter


    Raises:
        ValueError: if candidate is not of lrd format (e.g. dw1.iso.me.apple)
    """
    try:
        x = candidate.split(".")
    except:
        raise ValueError("Failed to seperate into words with split'.'")
    first_word = x[0]
    first_char = first_word[0]
    if not first_char.isalpha():
        raise ValueError(
            f"Most significant word must start with alphabet char. Got '{word}'"
        )
    for word in x:
        if not word.isalnum():
            raise ValueError(
                f"words seperated by dots must be alphanumeric. Got '{word}'"
            )
    if not candidate.islower():
        raise ValueError(f"alias must be lowercase. Got '{candidate}'")


def check_is_lru_alias_format(candidate: str):
    """AlphanumericStrings separated by underscores, with most
    significant word to the left.  I.e. `dw1.ne` is the child of `dw1`.
    Checking the format cannot verify the significance of words. All
    words must be alphanumeric. Most significant word must start with
    an alphabet charecter"""
    try:
        x = candidate.split("_")
    except:
        return False
    for word in x:
        if not word.isalnum():
            return False
    return True


def check_is_positive_integer(candidate):
    if not isinstance(candidate, int):
        raise ValueError("Must be an integer")
    if candidate <= 0:
        raise ValueError("Must be positive integer")


def check_is_reasonable_unix_time_ms(candidate):
    if pendulum.parse("2000-01-01T00:00:00Z").int_timestamp * 1000 > candidate:
        raise ValueError("ReasonableUnixTimeMs must be after 2000 AD")
    if pendulum.parse("3000-01-01T00:00:00Z").int_timestamp * 1000 < candidate:
        raise ValueError("ReasonableUnixTimeMs must be before 3000 AD")


def check_is_reasonable_unix_time_s(candidate):
    if pendulum.parse("2000-01-01T00:00:00Z").int_timestamp > candidate:
        raise ValueError("ReasonableUnixTimeS must be after 2000 AD")
    if pendulum.parse("3000-01-01T00:00:00Z").int_timestamp < candidate:
        raise ValueError("ReasonableUnixTimeS must be before 3000 AD")


def check_is_unsigned_short(candidate):
    try:
        struct.pack("H", candidate)
    except:
        raise ValueError("requires 0 <= number <= 65535")


def check_is_short_integer(candidate):
    try:
        struct.pack("h", candidate)
    except:
        raise ValueError("short format requires (-32767 -1) <= number <= 32767")


def check_is_uuid_canonical_textual(candidate):
    """
    Raises:
        ValueError: if not of the format "f7d517d9-7d3f-47bd-bd5c-ee04f636da6f"
    """
    try:
        x = candidate.split("-")
    except AttributeError as e:
        raise ValueError(f"Failed to split on -: {e}")
    if len(x) != 5:
        raise ValueError(f"Did not have 5 words")
    for hex_word in x:
        try:
            y = int(hex_word, 16)
        except ValueError:
            raise ValueError("Words are not all hex")
    if len(x[0]) != 8:
        raise ValueError("Word 0  not of length 8")
    if len(x[1]) != 4:
        raise ValueError("Word 1 not of length 4")
    if len(x[2]) != 4:
        raise ValueError("Word 2 not of length 4")
    if len(x[3]) != 4:
        raise ValueError("Word 3 not of length 4")
    if len(x[4]) != 12:
        raise ValueError("Word 4 not of length 12")


def check_world_alias_matches_universe(g_node_alias: str, universe: str):
    """
    Raises:
        ValueError: if g_node_alias is not LRD format or if first word does not match universe
    """
    check_is_lrd_alias_format(g_node_alias)
    world_alias = g_node_alias.split(".")[0]
    if universe == "dev":
        if world_alias[0] != "d":
            raise ValueError(
                f"World alias for dev universe must start with d. Got {world_alias}"
            )
