// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IdentityStorage {
    // Mapping to store if a face hash has already been registered
    mapping(bytes32 => bool) public registeredHashes;
    // Mapping to link a user wallet address to their face hash
    mapping(address => bytes32) public userToHash;

    event IdentityRegistered(address indexed user, bytes32 faceHash);

    // Function to register a new identity
    function registerIdentity(bytes32 _faceHash) public {
        // Check if this face has already been registered by anyone
        require(!registeredHashes[_faceHash], "This identity is already registered!");
        // Check if this wallet address already has an identity
        require(userToHash[msg.sender] == bytes32(0), "This wallet already has an identity!");

        registeredHashes[_faceHash] = true;
        userToHash[msg.sender] = _faceHash;

        emit IdentityRegistered(msg.sender, _faceHash);
    }

    // Helper to check if a hash exists
    function isHashRegistered(bytes32 _hash) public view returns (bool) {
        return registeredHashes[_hash];
    }
}